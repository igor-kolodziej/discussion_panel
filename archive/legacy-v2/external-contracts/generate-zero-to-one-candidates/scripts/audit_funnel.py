#!/usr/bin/env python3
"""Fail-closed structural audit for Zero-to-One candidate-generation runs.

The auditor checks provenance, freeze timing, context isolation, resource
reconciliation, and shadow routing. It never scores ideas or infers semantic
ancestry from similar names.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import re
import sys
import tempfile
import unittest
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SCHEMA_VERSION = "audit-funnel-v1"
RUN_SCHEMA_V2 = "zt1-generation-run-v2"
CHILD_TRUST_BUNDLE_SCHEMA_V2 = "zt1-child-trust-bundle-v2"
DEVELOPMENT_CONTRACT_SCHEMA_V2 = "zt1-development-contract-v2"
PROTECTION_ANCHOR_SCHEMA = "zt1-protection-anchor-v1"
FREEZE_SEAL_SCHEMA = "zt1-freeze-seal-v1"
PROTECTION_ANCHOR_SCHEMA_V2 = "zt1-protection-anchor-v2"
FREEZE_SEAL_SCHEMA_V2 = "zt1-freeze-seal-v2"
WORKFLOW_PROFILE_V2 = "zt1-auditor-workflow-v2"
PREFREEZE_MANIFEST_SNAPSHOT_V2 = "00c_pre_freeze_manifest_snapshot.jsonl"
CONTRACT_PROFILE = "zt1-fixed-v1"
WORKFLOW_PROFILE_FILE_PATHS_V2 = {
    "blind-search-protocol": "/Users/igor/.codex/skills/generate-zero-to-one-candidates/references/blind-search-protocol.md",
    "audit-funnel": "/Users/igor/.codex/skills/generate-zero-to-one-candidates/scripts/audit_funnel.py",
    "v2-candidate-development": "/Users/igor/Desktop/discussion_panel/utilities/v2_candidate_development.py",
    "v2-matched-experiment-manager": "/Users/igor/Desktop/discussion_panel/utilities/v2_matched_experiment_manager.py",
}
V2_PROTECTION_ANCHOR_FIELDS = {
    "schema",
    "contract_profile",
    "workflow_profile",
    "workflow_files",
    "run_id",
    "scope_id",
    "run_dir",
    "development_contract_path",
    "development_contract_sha256",
    "created_at",
    "block_semantics",
    "files",
    "blocks",
}
V2_PROTECTION_ANCHOR_FILE_FIELDS = {"id", "path", "sha256"}
V2_PROTECTION_ANCHOR_BLOCK_FIELDS = {
    "id",
    "path",
    "start_marker",
    "end_marker",
    "sha256",
}
V2_PROTECTION_ANCHOR_WORKFLOW_FILE_FIELDS = {"id", "path", "sha256"}
V2_FREEZE_SEAL_BASE_FIELDS = {
    "schema",
    "run_id",
    "scope_id",
    "run_dir",
    "protection_anchor_sha256",
    "mode",
    "run_profile",
    "arm",
    "routing_state",
    "cohort_kind",
    "wave_index",
    "selection_policy",
    "seed",
    "candidate_order_seed",
    "parent_scope_id",
    "matched_pilot",
    "model",
    "reasoning_effort",
    "development_contract_sha256",
    "results_visibility",
    "manifest_snapshot_path",
    "manifest_snapshot_sha256",
    "sealed_at",
    "finalists",
}
V2_FREEZE_SEAL_FINALIST_FIELDS = {
    "finalist_id",
    "arm",
    "artifact_path",
    "frozen_at",
    "sha256",
}
TRACKING_QUERY_PARAMETER_NAMES = {
    "dclid",
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "msclkid",
}
MANIFEST_RECORD_TYPES = {
    "run",
    "agent",
    "allocation",
    "query",
    "source_open",
    "tool_event",
    "checkpoint",
}
LEDGER_RECORD_TYPES = {"problem", "mapping", "evidence", "level2", "finalist"}
DEFAULT_PROTECTED_FILE_PATHS = {
    "founder-profile": "/Users/igor/Desktop/discussion_panel/PERSONALITY_SITUATION.md",
    "success-safety-contract": "/Users/igor/Desktop/discussion_panel/COMMUNICATION_AND_GENERAL_RULES.md",
    "goal": "/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_GOAL.md",
    "validator": "/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt",
    "orchestration-prompt": "/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_AGENT_PROMPT.md",
    "generator-skill": "/Users/igor/.codex/skills/generate-zero-to-one-candidates/SKILL.md",
    "evaluator-skill": "/Users/igor/.codex/skills/evaluate-zero-to-one/SKILL.md",
    "pivot-skill": "/Users/igor/.codex/skills/pivot-zero-to-one/SKILL.md",
}
REQUIRED_PROTECTED_BLOCK_IDS = {
    "validation-gates": ("## Validation Gates", "## Workflow")
}
REQUIRED_PROTECTED_BLOCKS = set(REQUIRED_PROTECTED_BLOCK_IDS.values())
RAW_HEADING = re.compile(r"^#{3,6}\s+([A-Za-z][A-Za-z0-9_-]*\d+)\s+(?:—|-)\s+.+$")
ALLOWED_DISPOSITIONS = {"retained", "merged", "rejected", "unresolved"}
ALLOWED_EVIDENCE_STATUSES = {
    "verified",
    "interpreted",
    "counsel-required",
    "unknown",
    "contradicted",
}
LIVE_CREATIVE_ROLES = {
    "taboo_space_explorer",
    "incentive_hacker",
    "incumbent_attacker",
    "rule_structure_analyst",
    "first_principles_extremist",
}
SHADOW_ISLAND_ROLES = {
    "customer_workarounds": "evidence_scout_customer_workarounds",
    "spend_procurement": "evidence_scout_spend_procurement",
    "operational_failure": "evidence_scout_operational_failure",
    "incumbent_economics_channels": "evidence_scout_incumbent_economics_channels",
    "technical_scientific_change": "evidence_scout_technical_scientific_change",
    "rules_finance_assets_transitions": "evidence_scout_rules_finance_assets_transitions",
}
INVERSION_DIMENSIONS = {
    "payer",
    "owner",
    "timing",
    "channel",
    "transaction_unit",
    "geography",
    "financing",
    "liability",
    "make_buy_boundary",
}
PROVENANCE_STAGES = {"problem_discovery", "direct_concept", "inversion", "recombination"}
LEVEL2_DEVELOPMENT_STATUSES = {"complete", "early_stop"}
LEVEL2_EARLY_STOP_CODES = {
    "illegal_or_unsafe_indispensability",
    "directly_falsified_premise",
}
ISOLATED_STAGES = {
    "problem_discovery",
    "generation",
    "direct_concept",
    "inversion",
    "recombination",
    "history_compressor",
    "cartography",
    "cluster_audit",
    "level1",
    "provisional_selector",
    "selector",
    "tail_challenger",
    "level2",
    "finalist_selector",
    "fact_closure",
    "dossier",
}
KNOWN_STAGES = set(ISOLATED_STAGES)
RESEARCH_STAGES = {"generation", "problem_discovery", "level2", "fact_closure"}
ZERO_QUERY_STAGES = KNOWN_STAGES - RESEARCH_STAGES
ALLOCATION_STAGES = RESEARCH_STAGES | ZERO_QUERY_STAGES
V2_CONTEXT_CLASSES = {
    "founder_constraints",
    "safety_legal",
    "neutral_evidence",
    "history",
}
V2_RESEARCH_TOOLS = {"web_search"}
V2_RESEARCH_TOOL_EVENT_TYPES = {"tool_call"}
V2_AGENT_FIELDS = {
    "record_type",
    "scope_id",
    "agent_id",
    "arm",
    "stage",
    "role",
    "fork_turns",
    "context_classes",
    "context_files",
    "allowlisted_files",
    "files_read",
    "model",
    "reasoning_effort",
    "metering_basis",
    "started_at",
    "ended_at",
    "resources",
    "assigned_ids",
    "output_ids",
}
V2_DEVELOPMENT_TRACE_FIELDS = {
    "trace_path",
    "trace_sha256",
    "trace_entity_id",
    "trace_task_name",
}
V2_ALLOCATION_FIELDS = {
    "record_type",
    "scope_id",
    "allocation_id",
    "agent_id",
    "arm",
    "stage",
    "entity_ids",
    "created_at",
    "metering_basis",
    "resources",
    "query_cap",
    "used_unique_queries",
    "unused_queries",
}
V2_QUERY_FIELDS = {
    "record_type",
    "scope_id",
    "query_id",
    "allocation_id",
    "agent_id",
    "arm",
    "stage",
    "query",
    "entity_ids",
    "occurred_at",
}
V2_TOOL_EVENT_FIELDS = {
    "record_type",
    "scope_id",
    "call_id",
    "query_id",
    "allocation_id",
    "agent_id",
    "arm",
    "stage",
    "tool",
    "event_type",
    "occurred_at",
}
V2_SOURCE_OPEN_FIELDS = {
    "record_type",
    "scope_id",
    "source_event_id",
    "query_id",
    "call_id",
    "allocation_id",
    "agent_id",
    "arm",
    "stage",
    "url",
    "entity_ids",
    "evidence_ids",
    "occurred_at",
}
LIVE_V2_STAGE_ROLES = {
    "generation": LIVE_CREATIVE_ROLES,
    "history_compressor": {"neutral_history_compressor"},
    "cartography": {"semantic_cartographer"},
    "cluster_audit": {"anti_overmerge_auditor"},
    "level1": {"canonicalizer"},
    "level2": {"level2_researcher"},
    "fact_closure": {"fact_closure_researcher"},
}
LIVE_V2_STAGE_COUNTS = {
    "generation": 5,
    "history_compressor": 1,
    "cartography": 1,
    "cluster_audit": 1,
    "level1": 1,
    "level2": 12,
    "fact_closure": 6,
}
SHADOW_V2_STAGE_ROLES = {
    "problem_discovery": set(SHADOW_ISLAND_ROLES.values()),
    "direct_concept": {"direct_builder_1", "direct_builder_2", "direct_builder_3"},
    "inversion": {"assumption_inverter"},
    "recombination": {"cross_domain_recombiner"},
    "history_compressor": {"neutral_history_compressor"},
    "cartography": {"semantic_cartographer"},
    "cluster_audit": {"anti_overmerge_auditor"},
    "level1": {"canonicalizer"},
    "provisional_selector": {"isolated_provisional_selector"},
    "selector": {"commercial_ranker", "economics_ranker"},
    "tail_challenger": {"tail_recall_challenger"},
    "level2": {"level2_researcher"},
    "finalist_selector": {"isolated_finalist_selector"},
    "fact_closure": {"fact_closure_researcher"},
}
SHADOW_V2_STAGE_COUNTS = {
    "problem_discovery": 6,
    "direct_concept": 3,
    "inversion": 2,
    "recombination": 2,
    "history_compressor": 1,
    "cartography": 1,
    "cluster_audit": 1,
    "level1": 1,
    "provisional_selector": 1,
    "selector": 2,
    "tail_challenger": 1,
    "level2": 12,
    "finalist_selector": 1,
    "fact_closure": 6,
}
KNOWN_ARMS = {"live", "shadow", "matched_baseline"}
RUN_PROFILES_V2 = {
    "ordinary_audited_funnel",
    "operational_live_with_shadow",
    "v2_matched_nonrouting",
}
ROUTING_STATES_V2 = {"enabled", "frozen_nonrouting"}
COHORT_KINDS_V2 = {"initial", "regeneration"}
CHILD_RELATIONSHIPS_V2 = {"shadow_child", "regeneration"}
CHILD_FINALIZATION_FIELDS_V2 = {
    "manifest_sha256",
    "freeze_seal_sha256",
    "audit_report_path",
    "audit_report_sha256",
    "audit_status",
}
CHILD_DECLARATION_FIELDS_V2 = {
    "scope_id",
    "relative_path",
    "relationship",
    "run_profile",
    "mode",
    "arm",
    "routing_state",
    "cohort_kind",
    "manifest_sha256",
    "development_contract_sha256",
    "protection_anchor_sha256",
    "freeze_seal_sha256",
    "audit_report_path",
    "audit_report_sha256",
    "audit_status",
    "model",
    "reasoning_effort",
    "results_visibility",
    "registered_at",
}
AUDIT_CHECKPOINTS = {"selection", "freeze", "shadow-dispatch", "evaluation"}
DEVELOPMENT_METRIC_KEYS = (
    "level2_queries",
    "level2_sources",
    "fact_closure_queries",
    "fact_closure_sources",
    "development_input_tokens",
    "development_output_tokens",
    "development_elapsed_minutes",
    "level2_mean_words",
    "frozen_mean_words",
)
EXACT_METERING_BASES = {"tool_reported", "trace_derived_exact"}
LIVE_STATE_CHAIN_V2 = (
    "registered",
    "raw_frozen",
    "history_frozen",
    "mapped",
    "cluster_audited",
    "level2_cohort_sealed",
    "level2_complete",
    "fact_closure_cohort_sealed",
    "closure_complete",
    "frozen",
    "complete",
)
SHADOW_STATE_CHAIN_V2 = (
    "registered",
    "problem_cards_frozen",
    "direct_concepts_frozen",
    "transformations_frozen",
    "mapped",
    "level1_frozen",
    "provisional_order_sealed",
    "ballots_sealed",
    "level2_cohort_sealed",
    "level2_complete",
    "fact_closure_cohort_sealed",
    "closure_complete",
    "frozen",
    "complete",
)
ALLOWED_RUN_STATUSES = {
    "registered",
    "generating",
    "mapped",
    "level1",
    "level2",
    "frozen",
    "resource_exhausted",
    "complete",
}
REQUIRED_BUDGET_KEYS = {
    "unique_queries",
    "uncached_input_tokens",
    "output_tokens",
    "elapsed_minutes",
    "max_concurrency",
}
MATCHED_RESOURCE_CAPS = {
    "unique_queries": 300,
    "uncached_input_tokens": 10_000_000,
    "output_tokens": 700_000,
    "elapsed_minutes": 180,
    "max_concurrency": 3,
}
MATCHED_AGGREGATE_OPPORTUNITY = {
    "raw": 48,
    "level2": 12,
    "fact_closure": 6,
    "frozen": 6,
    "discovery_queries": 108,
    "level2_queries": 144,
    "fact_closure_queries": 48,
    "total_queries": 300,
}
MATCHED_CANDIDATE_BUDGETS = {
    "level2": {
        "uncached_input_tokens": 112_000,
        "output_tokens": 20_000,
        "elapsed_minutes": 15,
    },
    "fact_closure": {
        "uncached_input_tokens": 96_000,
        "output_tokens": 20_000,
        "elapsed_minutes": 12,
    },
}
MATCHED_CANDIDATE_LIVE_STOP_THRESHOLDS = {
    "level2": {
        "uncached_input_tokens": 92_000,
        "output_tokens": 11_000,
        "elapsed_minutes": 14,
    },
    "fact_closure": {
        "uncached_input_tokens": 76_000,
        "output_tokens": 11_000,
        "elapsed_minutes": 11,
    },
}
MATCHED_METERING_MONITOR = {
    "poll_interval_milliseconds": 1_000,
    "controller": "blocking_direct_trace_monitor",
    "trace_discovery": "recent_scope_scan_then_direct_path",
    "interrupt_channel": "controller_result_to_root_collaboration_interrupt",
    "stop_action": "interrupt_candidate_agent_and_fail_stage_admission",
    "empirical_max_observed_uncached_token_event_jump": 16_633,
    "empirical_max_observed_output_token_event_jump": 8_204,
    "minimum_uncached_reserve_tokens": 20_000,
    "minimum_output_reserve_tokens": 9_000,
}
MATCHED_DOSSIER_PROSE_WORD_RANGES = {
    "level2": {
        "minimum": 900,
        "maximum": 1_500,
        "minimum_per_section": 75,
    },
    "frozen": {
        "minimum": 1_100,
        "maximum": 1_800,
        "minimum_per_section": 100,
    },
}
DOSSIER_MEASUREMENT_CONTRACT = {
    "counted_sections": [
        "## Customer Loss And Payer Evidence",
        "## Proposed Transaction And Paid Trigger",
        "## Acquisition Route",
        "## Incumbent Substitute And Route-Around",
        "## Unit Economics And Sensitivity",
        "## Control Point Or Compounding Asset",
        "## Execution Dependencies And Cheapest Proof",
        "## Decision-Critical Unknowns And Contradictions",
    ],
    "excluded_material": [
        "title",
        "section_headings",
        "evidence_and_sources",
        "source_ledgers",
        "telemetry",
        "machine_metadata",
    ],
}
DEVELOPMENT_CONTRACT_FIELDS_V2 = {
    "schema",
    "contract_id",
    "level2_sections",
    "frozen_sections",
    "evidence_statuses",
    "stage_query_caps",
    "aggregate_opportunity",
    "candidate_budgets",
    "candidate_live_stop_thresholds",
    "metering_monitor",
    "dossier_prose_word_ranges",
    "dossier_measurement",
    "fact_closure_schema",
    "query_source_opportunity",
}
AGGREGATE_OPPORTUNITY_FIELDS_V2 = set(MATCHED_AGGREGATE_OPPORTUNITY)
V2_RUN_MATERIALIZED_FIELDS = {
    "lifecycle_state",
    "status",
    "ended_at",
    "completed_at",
    "declared_child_scopes",
    "file_read_log_complete",
    "tool_event_log_complete",
    "resource_totals",
    "shadow_results_released_at",
    "failure_receipt_path",
    "failure_receipt_sha256",
}
V2_RUN_FIELDS = {
    "record_type",
    "schema",
    "run_id",
    "run_profile",
    "scope_id",
    "mode",
    "arm",
    "routing_state",
    "cohort_kind",
    "wave_index",
    "selection_policy",
    "lifecycle_state",
    "started_at",
    "deadline_at",
    "ended_at",
    "model",
    "reasoning_effort",
    "results_visibility",
    "seed",
    "candidate_order_seed",
    "development_contract_path",
    "development_contract_sha256",
    "parent_scope_id",
    "declared_child_scopes",
    "file_read_log_complete",
    "tool_event_log_complete",
    "protected_files",
    "protected_blocks",
    "budgets",
    "resource_totals",
    "fact_closure_selected_at",
    "fact_closure_candidates_file",
    "fact_closure_candidates_sha256",
    "live_finalists_frozen_at",
    # Optional compatibility mirrors; when present they must reconcile.
    "status",
    "matched_pilot",
    "shadow_only",
    "validation_eligible",
    "shadow_can_route_to_validation",
    # Profile-specific immutable lineage/selection bindings.
    "live_arm_freeze_seal_sha256",
    "live_arm_run_dir",
    "main_provisional_file",
    "main_provisional_frozen_at",
    "main_provisional_sha256",
    "initial_freeze_seal_sha256",
    # Narrowly materialized terminal integration fields.
    "completed_at",
    "shadow_results_released_at",
    "failure_receipt_path",
    "failure_receipt_sha256",
}
V2_LEDGER_FIELDS_BY_TYPE: dict[str, set[str]] = {
    "problem": {
        "record_type",
        "problem_id",
        "source_island",
        "creator_agent_id",
        "evidence_ids",
    },
    "mapping": {
        "record_type",
        "raw_id",
        "direction_id",
        "cluster_id",
        "disposition",
        "reason",
        "creator_agent_id",
        "concept_type",
        "parent_ids",
        "operation",
    },
    "level2": {
        "record_type",
        "concept_id",
        "selection_category",
        "selected_at",
        "completed_at",
        "development_status",
        "artifact_path",
        "sha256",
        "evidence_ids",
        "early_stop_code",
        "early_stop_reason",
        "backfill_reason",
    },
    "finalist": {
        "record_type",
        "finalist_id",
        "direction_id",
        "raw_ids",
        "evidence_ids",
        "frozen_at",
        "arm",
        "shadow_only",
        "validation_eligible",
        "artifact_path",
        "sha256",
    },
    "evidence": {
        "record_type",
        "scope_id",
        "allocation_id",
        "agent_id",
        "arm",
        "stage",
        "evidence_id",
        "direction_id",
        "concept_id",
        "entity_ids",
        "source_event_ids",
        "recorded_at",
        "decision_critical",
        "status",
        "proposition",
        "source",
        "source_date",
        "cheapest_resolving_test",
        "supersedes_evidence_id",
    },
}
V2_CHECKPOINT_FIELDS = {
    "record_type",
    "checkpoint_id",
    "state",
    "predecessor_id",
    "occurred_at",
    "completed_agent_ids",
    "file_read_log_complete",
    "tool_event_log_complete",
    "resource_totals",
    "artifacts",
}
V2_CHECKPOINT_RESOURCE_FIELDS = {
    "unique_queries",
    "uncached_input_tokens",
    "output_tokens",
    "elapsed_microseconds",
}
REQUIRED_AGENT_RESOURCE_KEYS = {
    "uncached_input_tokens",
    "output_tokens",
    "elapsed_minutes",
}
V2_AGENT_RESOURCE_KEYS = {
    "uncached_input_tokens",
    "output_tokens",
    "elapsed_microseconds",
}
FORBIDDEN_CONTEXT_CLASSES = {
    "scores",
    "validator_feedback",
    "other_agent_output",
    "selection_decision",
    "full_parent_transcript",
    "generator_reasoning",
    "prior_evaluation",
    "thresholds",
    "rejection_rhetoric",
}
CREATIVE_OR_SELECTOR_STAGES = ISOLATED_STAGES - {"history_compressor"}
PROHIBITED_CONTEXT_MARKERS = (
    "personalities/zerotoone.txt",
    "evaluate-zero-to-one",
    "pivot-zero-to-one",
    "tried_ideas_and_failures_brain.md",
    "evaluation_",
    "advisory",
    "panel_result",
    "validator_feedback",
)
PROHIBITED_PACKET_PATTERNS = (
    re.compile(r"personalities/zerotoone\.txt", re.IGNORECASE),
    re.compile(r"holistic-11-v1", re.IGNORECASE),
    re.compile(r"(?:strictly\s*)?>\s*8\.3", re.IGNORECASE),
    re.compile(r">=\s*8\.2", re.IGNORECASE),
    re.compile(r"interaction adjustment", re.IGNORECASE),
    re.compile(r"official lower simulated score", re.IGNORECASE),
    re.compile(r"customer pain and willingness to pay:\s*15%", re.IGNORECASE),
    re.compile(r"business model and economics:\s*22%", re.IGNORECASE),
    re.compile(r"\b(?:prior|previous|historical)\s+(?:validator|advisory|evaluator)\s+score\b", re.IGNORECASE),
    re.compile(r"\b(?:validator|advisory|evaluator)\s+score\s*[:=]?\s*\d", re.IGNORECASE),
    re.compile(r"\bevaluator objections?\b", re.IGNORECASE),
    re.compile(r"\b(?:historical|prior|previous) rejection rhetoric\b", re.IGNORECASE),
    re.compile(r"\bpass threshold\b", re.IGNORECASE),
)
REGENERATION_CONTAMINATION_PATTERNS = (
    re.compile(
        r"\b(?:advisory[ _-]+)?evaluator(?:'s)?[ _-]+(?:feedback|output|result|assessment|objection|recommendation|score|ranking|verdict|decision|notes?|ranked|scored|selected|accepted|rejected)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\badvisory[ _-]+evaluation[ _-]+(?:feedback|output|result|assessment|recommendation|score|ranking|verdict|decision)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:feedback|output|result|assessment|objection|recommendation|score|ranking|verdict|decision)[ _-]+(?:from|by)[ _-]+(?:the[ _-]+)?(?:advisory[ _-]+)?evaluator\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bvalidator(?:'s)?[ _-]+(?:feedback|output|result|objection|recommendation|score|verdict|decision)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:feedback|output|result|objection|recommendation|score|verdict|decision)[ _-]+(?:from|by)[ _-]+(?:the[ _-]+)?validator\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:judge(?:[ _-]+panel)?|panel)(?:'s)?[ _-]+(?:ranking|rankings|ranked|score|scores|scored|verdict|selection|recommendation|result|results)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bshadow(?:[ _-]+only)?[ _-]+(?:output|outputs|result|results|finding|findings|ranking|rankings|score|scores|selection|selections|shortlist|finalist|finalists|candidate|candidates|cohort)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bmatched(?:[ _-]+(?:baseline|arm|cohort|pilot))?[ _-]+(?:output|outputs|result|results|finding|findings|ranking|rankings|score|scores|selection|selections|shortlist|finalist|finalists)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?im)^\s*(?:[-*]\s*)?(?:advisory[ _-]+)?evaluator\s*(?::|[—–]|-\s)",
    ),
)
SHADOW_FORBIDDEN_TOOLS = {
    "evaluate-zero-to-one",
    "pivot-zero-to-one",
    "simulated-panel",
    "simulated-judge",
    "working-chat-validator",
    "fresh-chat-validator",
    "zero-to-one-chatbot",
    "validator",
    "validate",
    "validation",
    "judge",
    "evaluator",
    "evaluation",
    "score",
    "scorecard",
    "adjudicate",
    "adjudicator",
    "adjudication",
    "working-chat",
    "fresh-chat",
    "real-chat",
}
SHADOW_QUERY_CAPS = {
    "problem_discovery": 108,
    "level2": 144,
    "fact_closure": 48,
}
DOWNSTREAM_ARTIFACT_TOKENS = (
    "evaluat",
    "advisory",
    "pivot",
    "panel",
    "simulated",
    "working_chat",
    "fresh_chat",
    "validator",
    "confirmed_idea",
    "chatbot",
    "judge",
    "score",
    "adjudicat",
    "validation",
    "real_chat",
    "real-chat",
    "realchat",
    "working-chat",
    "workingchat",
    "fresh-chat",
    "freshchat",
    "zero_to_one",
    "zero-to-one",
    "confirmed-idea",
)
REQUIRED_LEVEL2_SECTIONS = (
    "## Customer Loss And Payer Evidence",
    "## Proposed Transaction And Paid Trigger",
    "## Acquisition Route",
    "## Incumbent Substitute And Route-Around",
    "## Unit Economics And Sensitivity",
    "## Control Point Or Compounding Asset",
    "## Execution Dependencies And Cheapest Proof",
    "## Decision-Critical Unknowns And Contradictions",
    "## Evidence And Sources",
)
COUNTED_DOSSIER_SECTIONS = REQUIRED_LEVEL2_SECTIONS[:-1]


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    artifact: str = ""
    line: int | None = None
    node_ids: tuple[str, ...] = ()


@dataclass
class AuditReport:
    run_id: str
    status: str
    findings: list[Finding]
    counts: dict[str, Any]
    resources: dict[str, Any]
    adapter: str = "native-v1"

    def to_json(self) -> str:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "adapter": self.adapter,
            "status": self.status,
            "counts": self.counts,
            "resources": self.resources,
            "findings": [asdict(item) for item in self.findings],
        }
        return json.dumps(payload, indent=2, sort_keys=True)


@dataclass(frozen=True)
class ProfileSpec:
    """Typed routing semantics; comparison metadata never selects a profile."""

    name: str
    allowed_contracts: frozenset[tuple[str, str, str, str]]
    permits_declared_children: bool
    downstream_allowed: bool


PROFILE_SPECS_V2 = {
    "ordinary_audited_funnel": ProfileSpec(
        "ordinary_audited_funnel",
        frozenset(
            {
                ("audited_funnel", "live", "enabled", "initial"),
                ("audited_funnel", "live", "enabled", "regeneration"),
            }
        ),
        True,
        True,
    ),
    "operational_live_with_shadow": ProfileSpec(
        "operational_live_with_shadow",
        frozenset(
            {
                ("audited_funnel", "live", "enabled", "initial"),
                (
                    "archipelago_lite_shadow",
                    "shadow",
                    "frozen_nonrouting",
                    "initial",
                ),
            }
        ),
        True,
        True,
    ),
    "v2_matched_nonrouting": ProfileSpec(
        "v2_matched_nonrouting",
        frozenset(
            {
                (
                    "audited_funnel",
                    "matched_baseline",
                    "frozen_nonrouting",
                    "initial",
                ),
                (
                    "archipelago_lite_shadow",
                    "shadow",
                    "frozen_nonrouting",
                    "initial",
                ),
            }
        ),
        True,
        False,
    ),
}


def _finding_sort_key(item: Finding) -> tuple[Any, ...]:
    rank = {"ERROR": 0, "UNKNOWN": 1, "WARNING": 2, "INFO": 3}
    return (
        rank.get(item.severity, 9),
        item.code,
        item.artifact,
        item.line or 0,
        item.node_ids,
    )


def _status(findings: Iterable[Finding], strict: bool = False) -> str:
    severities = {item.severity for item in findings}
    if "ERROR" in severities or (strict and "WARNING" in severities):
        return "FAIL"
    if "UNKNOWN" in severities:
        return "INCOMPLETE"
    if "WARNING" in severities:
        return "PASS_WITH_WARNINGS"
    return "PASS"


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def _elapsed_microseconds(start: datetime, end: datetime) -> int | None:
    """Return an exact UTC duration in integer microseconds."""
    start_utc = start.astimezone(timezone.utc)
    end_utc = end.astimezone(timezone.utc)
    if end_utc < start_utc:
        return None
    delta = end_utc - start_utc
    return (
        delta.days * 86_400_000_000
        + delta.seconds * 1_000_000
        + delta.microseconds
    )


def _v2_state_reached(run_record: dict[str, Any], state: str) -> bool:
    chain = (
        SHADOW_STATE_CHAIN_V2
        if run_record.get("mode") == "archipelago_lite_shadow"
        else LIVE_STATE_CHAIN_V2
    )
    lifecycle = run_record.get("lifecycle_state")
    try:
        return chain.index(str(lifecycle)) >= chain.index(state)
    except ValueError:
        return False


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _json_payload_sha256(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_json_bytes(payload)).hexdigest()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
    except (OSError, ValueError):
        return False
    return True


def _has_symlink_component(path: Path) -> bool:
    """Return true if any existing component in an absolute path is a symlink."""
    absolute = path if path.is_absolute() else path.absolute()
    cursor = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        cursor = cursor / part
        try:
            if cursor.is_symlink():
                return True
        except OSError:
            return True
    return False


def _required_file_id(
    path_value: Any,
    required_paths: dict[str, str] | None = None,
) -> str | None:
    if not isinstance(path_value, str):
        return None
    profile = required_paths or DEFAULT_PROTECTED_FILE_PATHS
    try:
        normalized = str(Path(path_value).resolve(strict=False))
    except OSError:
        return None
    matches = [
        contract_id
        for contract_id, expected_path in profile.items()
        if normalized == str(Path(expected_path).resolve(strict=False))
    ]
    return matches[0] if len(matches) == 1 else None


def _is_downstream_artifact(
    relative: Path,
    *,
    allowed_finalist_paths: set[str],
) -> bool:
    normalized_path = relative.as_posix().casefold()
    name = relative.name.casefold()
    if normalized_path in allowed_finalist_paths:
        return False
    if any(token in name for token in DOWNSTREAM_ARTIFACT_TOKENS):
        return True
    if "finalist" in name and "selector" not in name and "decision" not in name:
        return True
    return False


def _marker_block_sha256(path: Path, start_marker: str, end_marker: str) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    start_token = (start_marker + "\n").encode("utf-8")
    end_token = (end_marker + "\n").encode("utf-8")
    if data.count(start_token) != 1 or data.count(end_token) != 1:
        return None
    start = data.index(start_token)
    end = data.index(end_token, start + len(start_token))
    return hashlib.sha256(data[start:end]).hexdigest()


def _normalize_query(query: Any) -> str:
    if not isinstance(query, str):
        return ""
    return " ".join(query.casefold().split())


def _normalize_source_url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        return ""
    compact = "".join(value.strip().split())
    try:
        parsed = urlsplit(compact)
    except ValueError:
        return ""
    if not parsed.scheme or not parsed.netloc:
        return ""
    retained_query = sorted(
        (
            (key, item_value)
            for key, item_value in parse_qsl(
                parsed.query, keep_blank_values=True
            )
            if not key.casefold().startswith("utm_")
            and key.casefold() not in TRACKING_QUERY_PARAMETER_NAMES
        ),
        key=lambda item: (item[0], item[1]),
    )
    return urlunsplit(
        (
            parsed.scheme.casefold(),
            parsed.netloc.casefold(),
            parsed.path,
            urlencode(retained_query, doseq=True),
            "",
        )
    )


def _level2_section_issues(text: str) -> list[str]:
    """Return structural problems in a standardized Level-2 dossier."""
    lines = text.splitlines()
    positions: list[int] = []
    issues: list[str] = []
    for heading in REQUIRED_LEVEL2_SECTIONS:
        matches = [index for index, line in enumerate(lines) if line.strip() == heading]
        if len(matches) != 1:
            issues.append(f"{heading!r} occurs {len(matches)} times")
        else:
            positions.append(matches[0])
    if len(positions) != len(REQUIRED_LEVEL2_SECTIONS):
        return issues
    if positions != sorted(positions):
        issues.append("required sections are out of order")
        return issues
    for index, heading in enumerate(REQUIRED_LEVEL2_SECTIONS):
        start = positions[index] + 1
        end = positions[index + 1] if index + 1 < len(positions) else len(lines)
        body = lines[start:end]
        if not any(
            line.strip() and not re.match(r"^#{1,6}\s", line.strip())
            for line in body
        ):
            issues.append(f"{heading!r} has no nonblank body")
    return issues


def _is_nonnegative_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) >= 0
    )


def _is_nonnegative_int(value: Any) -> bool:
    """Accept exact machine integers, excluding bool's int subclass."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _typed_value_equal(actual: Any, expected: Any) -> bool:
    """Compare a closed JSON value without Python's bool/int or int/float aliasing."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _typed_value_equal(actual[key], expected[key]) for key in expected
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _typed_value_equal(left, right)
            for left, right in zip(actual, expected)
        )
    return actual == expected


def _canonical_tool_name(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    text = value.strip().casefold().lstrip("$")
    text = re.sub(r"^(?:[^:/\s]+::|[^:/\s]+/)+", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def _valid_string_list(value: Any, *, allow_empty: bool = False) -> tuple[list[str], bool]:
    if not isinstance(value, list):
        return [], False
    if not value and not allow_empty:
        return [], False
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return [], False
    return [item.strip() for item in value], True


def _safe_path(run_dir: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = run_dir / candidate
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(run_dir.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def _canonical_run_path(run_dir: Path, value: Any) -> tuple[Path | None, str | None]:
    path = _safe_path(run_dir, value)
    if path is None:
        return None, None
    return path, path.relative_to(run_dir.resolve()).as_posix()


def _relative_display(path: Path, root: Path) -> str:
    """Return a stable diagnostic path without letting alias mismatches abort audit."""
    try:
        return path.resolve(strict=False).relative_to(
            root.resolve(strict=False)
        ).as_posix()
    except (OSError, ValueError):
        return path.name


def _read_jsonl(path: Path, findings: list[Finding]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        findings.append(
            Finding("ARTIFACT_UNREADABLE", "UNKNOWN", str(exc), path.name)
        )
        return records
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            findings.append(
                Finding(
                    "JSONL_INVALID",
                    "ERROR",
                    f"Invalid JSON: {exc.msg}",
                    path.name,
                    number,
                )
            )
            continue
        if not isinstance(value, dict):
            findings.append(
                Finding(
                    "JSONL_RECORD_NOT_OBJECT",
                    "ERROR",
                    "Each JSONL line must be an object.",
                    path.name,
                    number,
                )
            )
            continue
        value["_line"] = number
        records.append(value)
    return records


def _extract_raw_ids(path: Path, findings: list[Finding]) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        findings.append(Finding("RAW_POOL_UNREADABLE", "UNKNOWN", str(exc), path.name))
        return []
    ids: list[str] = []
    for number, line in enumerate(lines, 1):
        match = RAW_HEADING.match(line.strip())
        if match:
            ids.append(match.group(1))
    if not ids:
        findings.append(
            Finding(
                "RAW_IDS_UNPARSEABLE",
                "UNKNOWN",
                "No stable raw IDs were found in Markdown headings.",
                path.name,
            )
        )
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    for raw_id in duplicates:
        findings.append(
            Finding(
                "RAW_ID_DUPLICATE",
                "ERROR",
                f"Raw ID {raw_id} appears more than once.",
                path.name,
                node_ids=(raw_id,),
            )
        )
    return ids


def _pick_raw_pool(run_dir: Path) -> Path | None:
    for name in ("02a_raw_pool.md", "02a_adversarial_raw_pool.md"):
        candidate = run_dir / name
        if candidate.is_file() and not candidate.is_symlink():
            return candidate
    return None


def _wall_minutes(run_record: dict[str, Any]) -> float | None:
    start = _parse_timestamp(run_record.get("started_at"))
    end = _parse_timestamp(run_record.get("ended_at"))
    if start is None or end is None or end < start:
        return None
    return (end - start).total_seconds() / 60.0


def _max_concurrency(agent_records: list[dict[str, Any]]) -> int | None:
    events: list[tuple[datetime, int]] = []
    for record in agent_records:
        start = _parse_timestamp(record.get("started_at"))
        end = _parse_timestamp(record.get("ended_at"))
        if start is None or end is None or end < start:
            return None
        events.append((start, 1))
        events.append((end, -1))
    active = 0
    maximum = 0
    for _timestamp, delta in sorted(events, key=lambda item: (item[0], item[1])):
        active += delta
        maximum = max(maximum, active)
    return maximum


@dataclass(frozen=True)
class LegacyProfileEvidence:
    """A legacy profile is usable only when every independent routing witness agrees."""

    profile_name: str | None
    findings: tuple[Finding, ...]


@dataclass(frozen=True)
class _LegacyTypedRoute:
    route: str | None
    contradictions: tuple[str, ...]
    gaps: tuple[str, ...]


def _legacy_typed_route(
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
) -> _LegacyTypedRoute:
    """Read legacy routing from typed agents and finalists, never comparison metadata."""
    contradictions: list[str] = []
    gaps: list[str] = []
    mode = run_record.get("mode")
    agents = [
        record
        for record in manifest_records
        if record.get("record_type") == "agent"
    ]
    finalists = [
        record for record in ledger_records if record.get("record_type") == "finalist"
    ]
    if not agents:
        gaps.append("no typed agents establish an arm")
    if not finalists:
        gaps.append("no typed finalists establish routing eligibility")

    agent_arms = [record.get("arm") for record in agents]
    finalist_arms = [record.get("arm") for record in finalists]
    route: str | None = None
    if agents and not all(isinstance(value, str) for value in agent_arms):
        gaps.append("one or more typed agents omit a string arm")
    elif agents:
        arm_set = set(agent_arms)
        if len(arm_set) != 1:
            contradictions.append(
                f"typed agents span incompatible arms {sorted(str(value) for value in arm_set)}"
            )
        else:
            sole_arm = next(iter(arm_set))
            if mode == "audited_funnel" and sole_arm in {"live", "matched_baseline"}:
                route = str(sole_arm)
            elif mode == "archipelago_lite_shadow" and sole_arm == "shadow":
                route = "shadow"
            else:
                contradictions.append(
                    f"mode {mode!r} is incompatible with typed agent arm {sole_arm!r}"
                )

    if finalists and not all(isinstance(value, str) for value in finalist_arms):
        gaps.append("one or more typed finalists omit a string arm")
    elif finalists and route is not None:
        finalist_arm_set = set(finalist_arms)
        if finalist_arm_set != {route}:
            contradictions.append(
                f"typed finalist arms {sorted(str(value) for value in finalist_arm_set)} disagree with agent arm {route!r}"
            )

    if route is not None:
        stages = {
            record.get("stage")
            for record in agents
            if isinstance(record.get("stage"), str)
        }
        required_stages = (
            {"problem_discovery", "direct_concept"}
            if route == "shadow"
            else {"generation"}
        )
        missing_stages = sorted(required_stages - stages)
        if missing_stages:
            gaps.append(
                f"typed agents do not establish required {route} stages {missing_stages}"
            )

        expected_eligibility = route == "live"
        for finalist in finalists:
            finalist_id = finalist.get("finalist_id")
            eligibility = finalist.get("validation_eligible")
            if eligibility is not expected_eligibility:
                contradictions.append(
                    f"finalist {finalist_id!r} validation_eligible={eligibility!r} contradicts {route} routing"
                )
            if route in {"shadow", "matched_baseline"} and finalist.get("shadow_only") is not True:
                contradictions.append(
                    f"nonrouting finalist {finalist_id!r} does not explicitly set shadow_only=true"
                )
            artifact_path = finalist.get("artifact_path")
            if not isinstance(artifact_path, str) or not artifact_path.strip():
                gaps.append(f"finalist {finalist_id!r} has no typed artifact namespace")
                continue
            basename = Path(artifact_path).name.casefold()
            live_namespace = basename.startswith("finalist_")
            shadow_namespace = basename.startswith("shadow_finalist_")
            matched_namespace = basename.startswith("baseline_shadow_finalist_")
            namespace_matches = (
                live_namespace
                if route == "live"
                else shadow_namespace
                if route == "shadow"
                else matched_namespace
            )
            if namespace_matches:
                continue
            if live_namespace or shadow_namespace or matched_namespace:
                contradictions.append(
                    f"finalist {finalist_id!r} uses a namespace belonging to another routing arm"
                )
            else:
                gaps.append(
                    f"finalist {finalist_id!r} artifact namespace does not prove {route} routing"
                )

    return _LegacyTypedRoute(route, tuple(contradictions), tuple(gaps))


def _legacy_load_child_records(
    child_dir: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[dict[str, Any]], str | None]:
    """Load only the two machine ledgers needed to prove a legacy child relationship."""
    manifest_path = child_dir / "00a_context_and_resource_manifest.jsonl"
    ledger_path = child_dir / "02b_raw_to_direction_ledger.jsonl"
    if (
        manifest_path.is_symlink()
        or ledger_path.is_symlink()
        or not manifest_path.is_file()
        or not ledger_path.is_file()
    ):
        return None, [], [], "child machine manifest or provenance ledger is missing/non-regular"
    local_findings: list[Finding] = []
    manifest_records = _read_jsonl(manifest_path, local_findings)
    ledger_records = _read_jsonl(ledger_path, local_findings)
    if local_findings:
        return None, manifest_records, ledger_records, "child machine records are malformed"
    run_records = [
        record for record in manifest_records if record.get("record_type") == "run"
    ]
    if len(run_records) != 1:
        return None, manifest_records, ledger_records, "child does not contain exactly one run record"
    return run_records[0], manifest_records, ledger_records, None


def _legacy_profile_evidence(
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
    run_dir: Path,
    *,
    freeze_seal: dict[str, Any] | None,
    freeze_seal_sha256: str | None,
    live_arm_freeze_seal: dict[str, Any] | None,
    live_arm_freeze_seal_sha256: str | None,
) -> LegacyProfileEvidence:
    """Map a V1 scope only after typed routing, mirrors, and seal links agree."""
    contradictions: list[tuple[str, str]] = []
    gaps: list[str] = []
    typed = _legacy_typed_route(run_record, manifest_records, ledger_records)
    contradictions.extend(("LEGACY_ROUTING_CONTRADICTION", message) for message in typed.contradictions)
    gaps.extend(typed.gaps)
    route = typed.route

    child_names = ("shadow_archipelago_lite", "matched_audited_baseline")
    child_dirs = [run_dir / name for name in child_names if (run_dir / name).exists()]
    profile_name: str | None = None
    if route == "live":
        profile_name = (
            "operational_live_with_shadow"
            if child_dirs
            else "ordinary_audited_funnel"
        )
    elif route in {"shadow", "matched_baseline"}:
        profile_name = "v2_matched_nonrouting"

    expected_mirrors: dict[str, bool] | None = None
    if profile_name == "ordinary_audited_funnel":
        expected_mirrors = {
            "matched_pilot": False,
            "shadow_only": False,
            "validation_eligible": True,
            "shadow_can_route_to_validation": False,
        }
    elif profile_name == "operational_live_with_shadow":
        expected_mirrors = {
            "matched_pilot": True,
            "shadow_only": False,
            "validation_eligible": True,
            "shadow_can_route_to_validation": False,
        }
    elif profile_name == "v2_matched_nonrouting":
        expected_mirrors = {
            "matched_pilot": True,
            "shadow_only": True,
            "validation_eligible": False,
            "shadow_can_route_to_validation": False,
        }
    if expected_mirrors is not None:
        for key, expected in expected_mirrors.items():
            value = run_record.get(key)
            if not isinstance(value, bool):
                gaps.append(f"run compatibility mirror {key!r} is absent or untyped")
            elif value is not expected:
                contradictions.append(
                    (
                        "LEGACY_ROUTING_CONTRADICTION",
                        f"run compatibility mirror {key}={value!r} contradicts typed {route} routing",
                    )
                )

    expected_seal_matched = profile_name in {
        "operational_live_with_shadow",
        "v2_matched_nonrouting",
    }
    if not isinstance(freeze_seal, dict) or not isinstance(freeze_seal_sha256, str):
        gaps.append("the independently pinned scope freeze seal is unavailable")
    else:
        own_seal_mismatch = (
            _json_payload_sha256(freeze_seal) != freeze_seal_sha256
            or freeze_seal.get("schema") != FREEZE_SEAL_SCHEMA
            or freeze_seal.get("run_id") != run_dir.name
            or freeze_seal.get("run_dir") != str(run_dir.resolve())
            or freeze_seal.get("mode") != run_record.get("mode")
            or freeze_seal.get("model") != run_record.get("model")
            or freeze_seal.get("reasoning_effort") != run_record.get("reasoning_effort")
        )
        if own_seal_mismatch:
            contradictions.append(
                (
                    "LEGACY_ROUTING_CONTRADICTION",
                    "the independently pinned scope freeze seal disagrees with the typed run identity",
                )
            )
        if profile_name is not None and freeze_seal.get("matched_pilot") is not expected_seal_matched:
            contradictions.append(
                (
                    "LEGACY_ROUTING_CONTRADICTION",
                    "the independently pinned scope freeze seal contradicts the proved legacy profile",
                )
            )
        ledger_finalists = {
            (
                record.get("finalist_id"),
                record.get("arm"),
                record.get("artifact_path"),
            )
            for record in ledger_records
            if record.get("record_type") == "finalist"
        }
        seal_entries = freeze_seal.get("finalists")
        if not isinstance(seal_entries, list) or not all(
            isinstance(item, dict) for item in seal_entries
        ):
            gaps.append("the scope freeze seal has no typed finalist set")
        else:
            sealed_finalists = {
                (
                    item.get("finalist_id"),
                    item.get("arm"),
                    item.get("artifact_path"),
                )
                for item in seal_entries
            }
            if sealed_finalists != ledger_finalists:
                contradictions.append(
                    (
                        "LEGACY_ROUTING_CONTRADICTION",
                        "the scope freeze seal finalist identities/arms/namespaces disagree with the ledger",
                    )
                )

    if route == "live" and child_dirs:
        for child_dir in child_dirs:
            child_name = child_dir.name
            if child_dir.is_symlink() or not child_dir.is_dir():
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} is not a regular owned directory",
                    )
                )
                continue
            child_run, child_manifest, child_ledger, child_error = _legacy_load_child_records(child_dir)
            if child_error is not None or child_run is None:
                gaps.append(f"comparison child {child_name!r}: {child_error}")
                continue
            child_typed = _legacy_typed_route(child_run, child_manifest, child_ledger)
            expected_child_route = (
                "shadow" if child_name == "shadow_archipelago_lite" else "matched_baseline"
            )
            if child_typed.contradictions:
                contradictions.extend(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r}: {message}",
                    )
                    for message in child_typed.contradictions
                )
            if child_typed.gaps:
                gaps.extend(
                    f"comparison child {child_name!r}: {message}"
                    for message in child_typed.gaps
                )
            if child_typed.route is not None and child_typed.route != expected_child_route:
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} proves {child_typed.route!r}, not {expected_child_route!r}",
                    )
                )
            child_expected_mode = (
                "archipelago_lite_shadow"
                if expected_child_route == "shadow"
                else "audited_funnel"
            )
            if child_run.get("mode") != child_expected_mode:
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} declares an incompatible mode",
                    )
                )
            if child_run.get("status") != "complete":
                gaps.append(f"comparison child {child_name!r} is not explicitly complete")
            if child_run.get("live_arm_run_dir") != str(run_dir.resolve()):
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} reverse-links a different live scope",
                    )
                )
            child_pin = child_run.get("live_arm_freeze_seal_sha256")
            if not isinstance(child_pin, str):
                gaps.append(f"comparison child {child_name!r} omits its live freeze-seal reverse pin")
            elif isinstance(freeze_seal_sha256, str) and child_pin != freeze_seal_sha256:
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} reverse pin disagrees with the supplied live freeze seal",
                    )
                )
            if (
                child_run.get("model") != run_record.get("model")
                or child_run.get("reasoning_effort") != run_record.get("reasoning_effort")
            ):
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        f"comparison child {child_name!r} uses a different model or reasoning effort",
                    )
                )
            for key, expected in {
                "matched_pilot": True,
                "shadow_only": True,
                "validation_eligible": False,
                "shadow_can_route_to_validation": False,
            }.items():
                value = child_run.get(key)
                if not isinstance(value, bool):
                    gaps.append(
                        f"comparison child {child_name!r} omits compatibility mirror {key!r}"
                    )
                elif value is not expected:
                    contradictions.append(
                        (
                            "LEGACY_SHADOW_LINK_CONTRADICTION",
                            f"comparison child {child_name!r} compatibility mirror {key} contradicts nonrouting",
                        )
                    )

    if route in {"shadow", "matched_baseline"}:
        if child_dirs:
            contradictions.append(
                (
                    "LEGACY_SHADOW_LINK_CONTRADICTION",
                    "a nonrouting legacy scope contains a nested comparison child",
                )
            )
        run_live_pin = run_record.get("live_arm_freeze_seal_sha256")
        run_live_dir = run_record.get("live_arm_run_dir")
        if not isinstance(run_live_pin, str) or not isinstance(run_live_dir, str):
            gaps.append("the nonrouting scope omits its live-arm reverse link")
        if not isinstance(live_arm_freeze_seal, dict) or not isinstance(
            live_arm_freeze_seal_sha256, str
        ):
            gaps.append("the independently pinned live-arm freeze seal is unavailable")
        else:
            live_root = (
                Path(run_live_dir).resolve(strict=False)
                if isinstance(run_live_dir, str) and Path(run_live_dir).is_absolute()
                else None
            )
            external_mismatch = (
                _json_payload_sha256(live_arm_freeze_seal)
                != live_arm_freeze_seal_sha256
                or run_live_pin != live_arm_freeze_seal_sha256
                or live_arm_freeze_seal.get("schema") != FREEZE_SEAL_SCHEMA
                or live_arm_freeze_seal.get("mode") != "audited_funnel"
                or live_arm_freeze_seal.get("matched_pilot") is not True
                or live_arm_freeze_seal.get("run_dir") != run_live_dir
                or live_root is None
                or live_root == run_dir.resolve()
                or not live_root.is_dir()
                or live_arm_freeze_seal.get("run_id") != live_root.name
                or live_arm_freeze_seal.get("model") != run_record.get("model")
                or live_arm_freeze_seal.get("reasoning_effort")
                != run_record.get("reasoning_effort")
            )
            if external_mismatch:
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        "the nonrouting scope reverse link disagrees with the independently pinned live-arm seal",
                    )
                )
            live_finalists = live_arm_freeze_seal.get("finalists")
            if not isinstance(live_finalists, list) or not live_finalists:
                gaps.append("the live-arm seal has no typed finalist set")
            elif not all(
                isinstance(item, dict)
                and item.get("arm") == "live"
                and isinstance(item.get("finalist_id"), str)
                and isinstance(item.get("artifact_path"), str)
                and Path(str(item.get("artifact_path"))).name.casefold().startswith(
                    "finalist_"
                )
                for item in live_finalists
            ):
                contradictions.append(
                    (
                        "LEGACY_SHADOW_LINK_CONTRADICTION",
                        "the independently pinned live-arm seal contains non-live or ambiguous finalist identities/namespaces",
                    )
                )

    evidence_findings = [
        Finding(code, "ERROR", message, "00a_context_and_resource_manifest.jsonl", run_record.get("_line"))
        for code, message in contradictions
    ]
    if gaps:
        evidence_findings.append(
            Finding(
                "LEGACY_PROFILE_INCOMPLETE",
                "UNKNOWN",
                "Legacy routing cannot be mapped without reconstruction: "
                + "; ".join(sorted(set(gaps))),
                "00a_context_and_resource_manifest.jsonl",
                run_record.get("_line"),
            )
        )
    if contradictions or gaps or profile_name is None:
        profile_name = None
        if profile_name is None and not contradictions and not gaps:
            evidence_findings.append(
                Finding(
                    "LEGACY_PROFILE_INCOMPLETE",
                    "UNKNOWN",
                    "Typed legacy routing does not establish a supported profile.",
                    "00a_context_and_resource_manifest.jsonl",
                    run_record.get("_line"),
                )
            )
    return LegacyProfileEvidence(profile_name, tuple(evidence_findings))


def _strict_relative_directory(run_dir: Path, value: Any) -> tuple[Path, str] | None:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return None
    relative = Path(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        return None
    unresolved = run_dir / relative
    try:
        resolved = unresolved.resolve(strict=False)
        resolved.relative_to(run_dir.resolve())
    except (OSError, ValueError):
        return None
    if unresolved.is_symlink() or not resolved.is_dir():
        return None
    cursor = run_dir
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return None
    return resolved, relative.as_posix().rstrip("/")


def _strict_reserved_child_directory(
    run_dir: Path, value: Any
) -> tuple[Path, str] | None:
    """Resolve an as-yet-unmaterialized child reservation without following links."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return None
    relative = Path(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        return None
    canonical_root = run_dir.resolve()
    unresolved = canonical_root / relative
    try:
        resolved = unresolved.resolve(strict=False)
        resolved.relative_to(canonical_root)
    except (OSError, ValueError):
        return None
    cursor = canonical_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return None
        if cursor.exists() and not cursor.is_dir():
            return None
    return resolved, relative.as_posix().rstrip("/")


def _is_v2_shadow_dispatch_prefix(
    run_record: dict[str, Any], checkpoint: str | None
) -> bool:
    if checkpoint != "shadow-dispatch" or run_record.get("schema") != RUN_SCHEMA_V2:
        return False
    identity = (
        run_record.get("run_profile"),
        run_record.get("mode"),
        run_record.get("arm"),
        run_record.get("routing_state"),
        run_record.get("cohort_kind"),
    )
    return identity in {
        (
            "operational_live_with_shadow",
            "audited_funnel",
            "live",
            "enabled",
            "initial",
        ),
        (
            "v2_matched_nonrouting",
            "audited_funnel",
            "matched_baseline",
            "frozen_nonrouting",
            "initial",
        ),
    }


def _declared_child_relative_paths(
    run_dir: Path, run_record: dict[str, Any]
) -> set[str]:
    result: set[str] = set()
    declarations = run_record.get("declared_child_scopes")
    if not isinstance(declarations, list):
        return result
    for declaration in declarations:
        if not isinstance(declaration, dict):
            continue
        parsed = _strict_relative_directory(run_dir, declaration.get("relative_path"))
        if parsed is not None:
            result.add(parsed[1])
    return result


def _legacy_excluded_relative_paths(run_dir: Path) -> set[str]:
    result: set[str] = set()
    for relative in (
        "shadow_archipelago_lite",
        "matched_audited_baseline",
        "regeneration_wave_2",
        "context/regeneration_wave_2",
    ):
        if (run_dir / relative).is_dir():
            result.add(relative)
    try:
        children = tuple(run_dir.iterdir())
    except OSError:
        return result
    for child in children:
        if child.is_dir() and "regeneration" in child.name.casefold():
            result.add(child.name)
    return result


def _relative_is_excluded(relative: Path | str, excluded_roots: set[str]) -> bool:
    relative_path = Path(relative)
    for root in excluded_roots:
        try:
            relative_path.relative_to(Path(root))
        except ValueError:
            continue
        return True
    return False


def _owned_files(run_dir: Path, excluded_roots: set[str]) -> Iterable[Path]:
    """Walk parent-owned files while pruning registered child scope directories."""
    for current, directory_names, file_names in os.walk(run_dir, followlinks=False):
        current_path = Path(current)
        retained_directories: list[str] = []
        for name in directory_names:
            candidate = current_path / name
            try:
                relative = candidate.relative_to(run_dir)
            except ValueError:
                continue
            if candidate.is_symlink() or _relative_is_excluded(relative, excluded_roots):
                continue
            retained_directories.append(name)
        directory_names[:] = retained_directories
        for name in file_names:
            candidate = current_path / name
            try:
                relative = candidate.relative_to(run_dir)
            except ValueError:
                continue
            if not _relative_is_excluded(relative, excluded_roots):
                yield candidate


def _audit_owned_symlinks(
    run_dir: Path, excluded_roots: set[str], findings: list[Finding]
) -> None:
    """Fail closed on links without traversing or reading their targets."""
    for current, directory_names, file_names in os.walk(run_dir, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for name in directory_names:
            candidate = current_path / name
            relative = candidate.relative_to(run_dir)
            if _relative_is_excluded(relative, excluded_roots):
                continue
            if candidate.is_symlink():
                findings.append(
                    Finding(
                        "OWNED_SCOPE_SYMLINK_FORBIDDEN",
                        "ERROR",
                        "An owned scope contains a symlinked directory; escaped content is not read.",
                        relative.as_posix(),
                    )
                )
                continue
            retained.append(name)
        directory_names[:] = retained
        for name in file_names:
            candidate = current_path / name
            relative = candidate.relative_to(run_dir)
            if (
                not _relative_is_excluded(relative, excluded_roots)
                and candidate.is_symlink()
            ):
                findings.append(
                    Finding(
                        "OWNED_SCOPE_SYMLINK_FORBIDDEN",
                        "ERROR",
                        "An owned scope contains a symlinked file; escaped content is not read.",
                        relative.as_posix(),
                    )
                )


def _v2_immutable_run_view(record: dict[str, Any]) -> dict[str, Any]:
    """Return fields that registration/freeze may never materialize later."""
    return {
        key: value
        for key, value in record.items()
        if key not in V2_RUN_MATERIALIZED_FIELDS and key != "_line"
    }


LEDGER_ID_FIELDS_BY_TYPE: dict[str, tuple[str, ...]] = {
    "problem": ("problem_id",),
    "mapping": ("raw_id", "direction_id", "cluster_id"),
    "level2": ("concept_id",),
    "finalist": ("finalist_id",),
    "evidence": ("evidence_id",),
}
MANIFEST_ID_FIELDS_BY_TYPE: dict[str, tuple[str, ...]] = {
    "run": ("run_id", "scope_id"),
    "agent": ("agent_id",),
    "allocation": ("allocation_id",),
    "query": ("query_id",),
    "tool_event": ("call_id",),
    "source_open": ("source_event_id",),
    "checkpoint": ("checkpoint_id",),
}


def _typed_id_registry(
    records: list[dict[str, Any]],
    fields_by_type: dict[str, tuple[str, ...]],
) -> dict[str, set[str]]:
    """Collect identifiers only from the record kind that structurally owns them."""
    result = {record_type: set() for record_type in fields_by_type}
    for record in records:
        record_type = record.get("record_type")
        if not isinstance(record_type, str) or record_type not in fields_by_type:
            continue
        for key in fields_by_type[record_type]:
            value = record.get(key)
            if isinstance(value, str) and value.strip():
                result[record_type].add(value.strip())
    return result


def _typed_ledger_id_registry(
    ledger_records: list[dict[str, Any]],
) -> dict[str, set[str]]:
    return _typed_id_registry(ledger_records, LEDGER_ID_FIELDS_BY_TYPE)


def _typed_record_field_ids(
    records: list[dict[str, Any]], record_type: str, field: str
) -> set[str]:
    if field not in LEDGER_ID_FIELDS_BY_TYPE.get(record_type, ()):
        return set()
    return {
        value.strip()
        for record in records
        if record.get("record_type") == record_type
        and isinstance((value := record.get(field)), str)
        and value.strip()
    }


def _typed_manifest_id_registry(
    manifest_records: list[dict[str, Any]],
) -> dict[str, set[str]]:
    return _typed_id_registry(manifest_records, MANIFEST_ID_FIELDS_BY_TYPE)


def _scope_entity_ids(ledger_records: list[dict[str, Any]]) -> set[str]:
    """Return structural entity IDs; evidence IDs never certify entity ancestry."""
    registry = _typed_ledger_id_registry(ledger_records)
    return set().union(
        registry["problem"],
        registry["mapping"],
        registry["level2"],
        registry["finalist"],
    )


def _scope_ledger_machine_ids(ledger_records: list[dict[str, Any]]) -> set[str]:
    registry = _typed_ledger_id_registry(ledger_records)
    return set().union(*registry.values())


def _scope_machine_ids(
    manifest_records: list[dict[str, Any]], ledger_records: list[dict[str, Any]]
) -> set[str]:
    manifest_registry = _typed_manifest_id_registry(manifest_records)
    return _scope_ledger_machine_ids(ledger_records) | set().union(
        *manifest_registry.values()
    )


def _scope_cross_scope_machine_ids(
    manifest_records: list[dict[str, Any]], ledger_records: list[dict[str, Any]]
) -> set[str]:
    """IDs whose identity must be globally unique across a composite run.

    Checkpoint IDs are ordered scope-local state labels and may intentionally use
    the same canonical names in separate scopes.
    """
    registry = _typed_manifest_id_registry(manifest_records)
    return _scope_ledger_machine_ids(ledger_records) | set().union(
        *(values for record_type, values in registry.items() if record_type != "checkpoint")
    )


def _strict_run_file(
    run_dir: Path, value: Any, excluded_roots: set[str] | None = None
) -> tuple[Path, str] | None:
    """Return a regular, non-symlink, run-owned file from a strict relative path."""
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return None
    relative = Path(value)
    if any(part in {"", ".", ".."} for part in relative.parts):
        return None
    if excluded_roots and _relative_is_excluded(relative, excluded_roots):
        return None
    unresolved = run_dir / relative
    cursor = run_dir
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return None
    try:
        resolved = unresolved.resolve(strict=True)
        resolved.relative_to(run_dir.resolve())
    except (OSError, ValueError):
        return None
    if not resolved.is_file():
        return None
    return resolved, relative.as_posix()


def _as_decimal(value: Any) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    if not parsed.is_finite() or parsed < 0:
        return None
    return parsed


def _word_count(path: Path) -> int | None:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return None
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def _dossier_prose_section_word_counts(
    path: Path, counted_sections: Iterable[str]
) -> dict[str, int] | None:
    """Count each persuasive section body, excluding headings and source metadata."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return None
    lines = text.splitlines()
    section_starts = {
        line.strip(): index
        for index, line in enumerate(lines)
        if line.strip().startswith("## ")
    }
    section_words: dict[str, int] = {}
    for heading in counted_sections:
        start = section_starts.get(heading)
        if start is None:
            return None
        end = next(
            (
                index
                for index in range(start + 1, len(lines))
                if lines[index].strip().startswith("## ")
            ),
            len(lines),
        )
        body = "\n".join(
            line
            for line in lines[start + 1 : end]
            if not line.strip().startswith("#")
        )
        section_words[heading] = len(
            re.findall(r"\b[\w'-]+\b", body, flags=re.UNICODE)
        )
    return section_words


def _dossier_prose_word_count(
    path: Path, counted_sections: Iterable[str]
) -> int | None:
    """Count all persuasive section-body prose under the neutral contract."""
    section_words = _dossier_prose_section_word_counts(path, counted_sections)
    return sum(section_words.values()) if section_words is not None else None


def _normalized_title(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return " ".join(match.group(1).casefold().split())
    return ""


def _meaningful_paragraphs(text: str) -> set[str]:
    paragraphs: set[str] = set()
    for paragraph in re.split(r"\n\s*\n", text):
        normalized = " ".join(paragraph.casefold().split())
        if (
            len(normalized) >= 80
            and len(normalized.split()) >= 12
            and not normalized.startswith(("{", "[", "#"))
        ):
            paragraphs.add(normalized)
    return paragraphs


def _expected_v2_freeze_seal_fields(
    *, arm: Any, cohort_kind: Any
) -> set[str]:
    fields = set(V2_FREEZE_SEAL_BASE_FIELDS)
    if arm == "shadow":
        fields.add("live_arm_freeze_seal_sha256")
    if cohort_kind == "regeneration":
        fields.add("initial_freeze_seal_sha256")
    return fields


def _validate_v2_protection_anchor_fields(
    protection_anchor: dict[str, Any], findings: list[Finding]
) -> None:
    observed_fields = set(protection_anchor)
    if observed_fields != V2_PROTECTION_ANCHOR_FIELDS:
        findings.append(
            Finding(
                "V2_PROTECTION_ANCHOR_FIELDS_INVALID",
                "ERROR",
                "V2 protection anchor must use the exact closed top-level schema; "
                f"missing={sorted(V2_PROTECTION_ANCHOR_FIELDS - observed_fields)}, "
                f"extra={sorted(observed_fields - V2_PROTECTION_ANCHOR_FIELDS)}.",
            )
        )
    entry_contracts = (
        (
            "files",
            V2_PROTECTION_ANCHOR_FILE_FIELDS,
            "PROTECTION_ANCHOR_FILE_INVALID",
        ),
        (
            "blocks",
            V2_PROTECTION_ANCHOR_BLOCK_FIELDS,
            "PROTECTION_ANCHOR_BLOCK_INVALID",
        ),
        (
            "workflow_files",
            V2_PROTECTION_ANCHOR_WORKFLOW_FILE_FIELDS,
            "WORKFLOW_PROFILE_FILE_INVALID",
        ),
    )
    for field, expected_fields, code in entry_contracts:
        entries = protection_anchor.get(field)
        if not isinstance(entries, list):
            findings.append(
                Finding(
                    code,
                    "ERROR",
                    f"V2 protection-anchor {field} must be a list of exact closed entries.",
                )
            )
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or set(entry) != expected_fields:
                observed_entry_fields = set(entry) if isinstance(entry, dict) else set()
                findings.append(
                    Finding(
                        code,
                        "ERROR",
                        f"V2 protection-anchor {field}[{index}] must use exact keys; "
                        f"missing={sorted(expected_fields - observed_entry_fields)}, "
                        f"extra={sorted(observed_entry_fields - expected_fields)}.",
                    )
                )


def _validate_v2_freeze_seal_fields(
    freeze_seal: dict[str, Any],
    findings: list[Finding],
    *,
    expected_arm: Any = None,
    expected_cohort_kind: Any = None,
) -> None:
    arm = freeze_seal.get("arm") if expected_arm is None else expected_arm
    cohort_kind = (
        freeze_seal.get("cohort_kind")
        if expected_cohort_kind is None
        else expected_cohort_kind
    )
    expected_fields = _expected_v2_freeze_seal_fields(
        arm=arm, cohort_kind=cohort_kind
    )
    observed_fields = set(freeze_seal)
    if observed_fields != expected_fields:
        findings.append(
            Finding(
                "V2_FREEZE_SEAL_FIELDS_INVALID",
                "ERROR",
                "V2 freeze seal must use the exact profile-conditional top-level schema; "
                f"missing={sorted(expected_fields - observed_fields)}, "
                f"extra={sorted(observed_fields - expected_fields)}.",
            )
        )
    finalists = freeze_seal.get("finalists")
    if not isinstance(finalists, list):
        findings.append(
            Finding(
                "V2_FREEZE_SEAL_FINALIST_FIELDS_INVALID",
                "ERROR",
                "V2 freeze-seal finalists must be a list of exact closed entries.",
            )
        )
    else:
        for index, finalist in enumerate(finalists):
            if (
                not isinstance(finalist, dict)
                or set(finalist) != V2_FREEZE_SEAL_FINALIST_FIELDS
            ):
                observed_finalist_fields = (
                    set(finalist) if isinstance(finalist, dict) else set()
                )
                findings.append(
                    Finding(
                        "V2_FREEZE_SEAL_FINALIST_FIELDS_INVALID",
                        "ERROR",
                        f"V2 freeze-seal finalists[{index}] must use exact keys; "
                        f"missing={sorted(V2_FREEZE_SEAL_FINALIST_FIELDS - observed_finalist_fields)}, "
                        f"extra={sorted(observed_finalist_fields - V2_FREEZE_SEAL_FINALIST_FIELDS)}.",
                    )
                )
    expected_matched_pilot = freeze_seal.get("run_profile") in {
        "operational_live_with_shadow",
        "v2_matched_nonrouting",
    }
    if freeze_seal.get("matched_pilot") is not expected_matched_pilot:
        findings.append(
            Finding(
                "V2_FREEZE_SEAL_COMPATIBILITY_MISMATCH",
                "ERROR",
                "V2 freeze-seal matched_pilot must exactly mirror its authoritative run_profile.",
            )
        )


def _audit_v2_terminal_lifecycle_times(
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    findings: list[Finding],
    *,
    artifact: str = "00a_context_and_resource_manifest.jsonl",
) -> None:
    lifecycle_state = run_record.get("lifecycle_state")
    started_at = _parse_timestamp(run_record.get("started_at"))
    deadline_at = _parse_timestamp(run_record.get("deadline_at"))
    ended_at = _parse_timestamp(run_record.get("ended_at"))
    checkpoints = [
        record
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
    ]
    last_checkpoint_at = (
        _parse_timestamp(checkpoints[-1].get("occurred_at")) if checkpoints else None
    )
    if (
        started_at is None
        or deadline_at is None
        or deadline_at <= started_at
    ):
        findings.append(
            Finding(
                "V2_DEADLINE_INVALID",
                "ERROR",
                "V2 started_at and deadline_at must be actual offset-aware timestamps with deadline_at later than started_at.",
                artifact,
                run_record.get("_line"),
            )
        )
    complete_checkpoints = [
        record
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
        and record.get("state") == "complete"
    ]
    if lifecycle_state != "complete":
        if run_record.get("completed_at") is not None:
            findings.append(
                Finding(
                    "V2_COMPLETED_AT_PREFIX_INVALID",
                    "ERROR",
                    "A non-complete V2 lifecycle prefix cannot claim a non-null completed_at.",
                    artifact,
                    run_record.get("_line"),
                )
            )
        if run_record.get("ended_at") is not None and (
            ended_at is None
            or started_at is None
            or ended_at < started_at
            or (last_checkpoint_at is not None and ended_at < last_checkpoint_at)
            or (deadline_at is not None and ended_at > deadline_at)
        ):
            findings.append(
                Finding(
                    "V2_ACTUAL_END_TIME_INVALID",
                    "ERROR",
                    "A stopped V2 prefix may record only its actual end time, after its last checkpoint and no later than deadline_at.",
                    artifact,
                    run_record.get("_line"),
                )
            )
        return
    checkpoint_time = (
        _parse_timestamp(complete_checkpoints[0].get("occurred_at"))
        if len(complete_checkpoints) == 1
        else None
    )
    completed_at = (
        _parse_timestamp(run_record.get("completed_at"))
        if "completed_at" in run_record
        else checkpoint_time
    )
    if (
        len(complete_checkpoints) != 1
        or checkpoint_time is None
        or ended_at != checkpoint_time
        or completed_at != checkpoint_time
    ):
        findings.append(
            Finding(
                "V2_TERMINAL_TIME_MISMATCH",
                "ERROR",
                "Completed V2 ended_at and optional completed_at must equal the sole complete checkpoint occurred_at.",
                artifact,
                run_record.get("_line"),
            )
        )


def _audit_v2_regeneration_initial_seal(
    run_record: dict[str, Any],
    regeneration_freeze_seal: dict[str, Any] | None,
    initial_freeze_seal: dict[str, Any] | None,
    initial_freeze_seal_sha256: str | None,
    findings: list[Finding],
    *,
    artifact: str = "00a_context_and_resource_manifest.jsonl",
) -> None:
    if run_record.get("cohort_kind") != "regeneration":
        return
    if not isinstance(initial_freeze_seal, dict) or not isinstance(
        initial_freeze_seal_sha256, str
    ):
        findings.append(
            Finding(
                "INITIAL_FREEZE_SEAL_MISSING",
                "UNKNOWN",
                "A standalone regeneration audit requires the independently pinned initial-root V2 freeze seal.",
                artifact,
                run_record.get("_line"),
            )
        )
        return
    pin_valid = bool(
        re.fullmatch(r"[0-9a-f]{64}", initial_freeze_seal_sha256)
        and _json_payload_sha256(initial_freeze_seal)
        == initial_freeze_seal_sha256
    )
    schema_findings: list[Finding] = []
    _validate_v2_freeze_seal_fields(
        initial_freeze_seal,
        schema_findings,
        expected_arm="live",
        expected_cohort_kind="initial",
    )
    if not pin_valid or schema_findings:
        findings.extend(schema_findings)
        findings.append(
            Finding(
                "INITIAL_FREEZE_SEAL_INVALID",
                "ERROR",
                "The supplied initial freeze seal has an invalid digest or is not the exact closed V2 initial-live seal schema.",
                artifact,
                run_record.get("_line"),
            )
        )
    initial_run_dir_value = initial_freeze_seal.get("run_dir")
    initial_run_dir = (
        Path(initial_run_dir_value)
        if isinstance(initial_run_dir_value, str)
        and Path(initial_run_dir_value).is_absolute()
        else None
    )
    parent_scope_id = run_record.get("parent_scope_id")
    run_initial_pin = run_record.get("initial_freeze_seal_sha256")
    regeneration_seal_pin = (
        regeneration_freeze_seal.get("initial_freeze_seal_sha256")
        if isinstance(regeneration_freeze_seal, dict)
        else None
    )
    lineage_invalid = (
        not pin_valid
        or initial_freeze_seal.get("schema") != FREEZE_SEAL_SCHEMA_V2
        or initial_freeze_seal.get("mode") != "audited_funnel"
        or initial_freeze_seal.get("arm") != "live"
        or initial_freeze_seal.get("cohort_kind") != "initial"
        or initial_freeze_seal.get("routing_state") != "enabled"
        or initial_freeze_seal.get("scope_id") != parent_scope_id
        or initial_freeze_seal.get("parent_scope_id") is not None
        or initial_run_dir is None
        or initial_freeze_seal.get("run_id")
        != (initial_run_dir.name if initial_run_dir is not None else None)
        or _parse_timestamp(initial_freeze_seal.get("sealed_at")) is None
        or initial_freeze_seal_sha256 != run_initial_pin
        or (
            isinstance(regeneration_freeze_seal, dict)
            and initial_freeze_seal_sha256 != regeneration_seal_pin
        )
    )
    if lineage_invalid:
        findings.append(
            Finding(
                "INITIAL_FREEZE_SEAL_LINEAGE_MISMATCH",
                "ERROR",
                "Regeneration run and seal must bind one independently pinned enabled initial live audited-funnel seal whose scope_id equals parent_scope_id.",
                artifact,
                run_record.get("_line"),
            )
        )


def audit_run(
    run_dir: Path,
    strict: bool = False,
    *,
    protection_anchor: dict[str, Any] | None = None,
    protection_anchor_sha256: str | None = None,
    child_protection_anchor: dict[str, Any] | None = None,
    child_protection_anchor_sha256: str | None = None,
    freeze_seal: dict[str, Any] | None = None,
    freeze_seal_sha256: str | None = None,
    live_arm_freeze_seal: dict[str, Any] | None = None,
    live_arm_freeze_seal_sha256: str | None = None,
    initial_freeze_seal: dict[str, Any] | None = None,
    initial_freeze_seal_sha256: str | None = None,
    child_trust_bundle: dict[str, Any] | None = None,
    child_trust_bundle_sha256: str | None = None,
    checkpoint: str | None = None,
    _fixed_contract_paths: dict[str, str] | None = None,
    _scope_stack: tuple[str, ...] = (),
) -> AuditReport:
    supplied_run_dir = run_dir if run_dir.is_absolute() else run_dir.absolute()
    supplied_scope_has_symlink = _has_symlink_component(supplied_run_dir)
    run_dir = supplied_run_dir.resolve()
    findings: list[Finding] = []
    child_protection_supplied = (
        child_protection_anchor is not None
        or child_protection_anchor_sha256 is not None
    )
    child_protection_pair_complete = (
        isinstance(child_protection_anchor, dict)
        and isinstance(child_protection_anchor_sha256, str)
    )
    if checkpoint == "shadow-dispatch" and not child_protection_pair_complete:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_CHILD_PROTECTION_MISSING",
                "ERROR",
                "shadow-dispatch requires one independently pinned child protection-anchor payload and SHA-256 pin.",
                "00a_context_and_resource_manifest.jsonl",
            )
        )
    elif checkpoint != "shadow-dispatch" and child_protection_supplied:
        findings.append(
            Finding(
                "CHILD_PROTECTION_ANCHOR_CHECKPOINT_INVALID",
                "ERROR",
                "Child protection-anchor trust input is valid only for checkpoint=shadow-dispatch.",
                "00a_context_and_resource_manifest.jsonl",
            )
        )
    if supplied_scope_has_symlink:
        findings.append(
            Finding(
                "ROOT_SCOPE_SYMLINK_COMPONENT",
                "ERROR",
                "The audited root path contains a symlink component; scope ownership must be canonical before traversal.",
                str(supplied_run_dir),
            )
        )
    counts: dict[str, Any] = {}
    resources: dict[str, Any] = {}
    required_protected_paths = dict(
        _fixed_contract_paths or DEFAULT_PROTECTED_FILE_PATHS
    )
    if set(required_protected_paths) != set(DEFAULT_PROTECTED_FILE_PATHS):
        findings.append(
            Finding(
                "FIXED_CONTRACT_PROFILE_INVALID",
                "ERROR",
                "The fixed-contract path profile has missing or unknown contract IDs.",
            )
        )

    raw_path = _pick_raw_pool(run_dir)
    if raw_path is None:
        for raw_name in ("02a_raw_pool.md", "02a_adversarial_raw_pool.md"):
            if (run_dir / raw_name).is_symlink():
                findings.append(
                    Finding(
                        "ROOT_MACHINE_FILE_SYMLINK",
                        "ERROR",
                        "The raw pool must be a run-owned regular non-symlink file.",
                        raw_name,
                    )
                )
        findings.append(
            Finding("RAW_POOL_MISSING", "UNKNOWN", "No supported raw-pool artifact exists.")
        )
        raw_ids: list[str] = []
    else:
        raw_ids = _extract_raw_ids(raw_path, findings)
    raw_set = set(raw_ids)
    counts["raw"] = len(raw_ids)

    human_manifest = run_dir / "00_run_manifest.md"
    if not human_manifest.is_file() or human_manifest.is_symlink():
        findings.append(
            Finding(
                "RUN_MANIFEST_MISSING",
                "UNKNOWN",
                "The human-readable run contract is missing.",
                human_manifest.name,
            )
        )

    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    manifest_regular = manifest_path.is_file() and not manifest_path.is_symlink()
    ledger_regular = ledger_path.is_file() and not ledger_path.is_symlink()
    for machine_path in (manifest_path, ledger_path):
        if machine_path.is_symlink():
            findings.append(
                Finding(
                    "ROOT_MACHINE_FILE_SYMLINK",
                    "ERROR",
                    "Root machine artifacts must be run-owned regular non-symlink files.",
                    machine_path.name,
                )
            )
    manifest_records = _read_jsonl(manifest_path, findings) if manifest_regular else []
    ledger_records = _read_jsonl(ledger_path, findings) if ledger_regular else []
    if not manifest_regular:
        findings.append(
            Finding(
                "CONTEXT_MANIFEST_MISSING",
                "UNKNOWN",
                "Context and resource provenance cannot be verified.",
                manifest_path.name,
            )
        )
    if not ledger_regular:
        findings.append(
            Finding(
                "PROVENANCE_LEDGER_MISSING",
                "UNKNOWN",
                "Raw mappings, evidence timing, and finalist ancestry cannot be verified.",
                ledger_path.name,
            )
        )

    for record in manifest_records:
        record_type = record.get("record_type")
        if not isinstance(record_type, str) or record_type not in MANIFEST_RECORD_TYPES:
            findings.append(
                Finding(
                    "MANIFEST_RECORD_TYPE_INVALID",
                    "ERROR",
                    f"Unsupported manifest record_type {record_type!r}.",
                    manifest_path.name,
                    record.get("_line"),
                )
            )
    for record in ledger_records:
        record_type = record.get("record_type")
        if not isinstance(record_type, str) or record_type not in LEDGER_RECORD_TYPES:
            findings.append(
                Finding(
                    "LEDGER_RECORD_TYPE_INVALID",
                    "ERROR",
                    f"Unsupported ledger record_type {record_type!r}.",
                    ledger_path.name,
                    record.get("_line"),
                )
            )

    run_records = [r for r in manifest_records if r.get("record_type") == "run"]
    if len(run_records) != 1:
        findings.append(
            Finding(
                "RUN_RECORD_COUNT",
                "UNKNOWN" if not run_records else "ERROR",
                f"Expected one run record; found {len(run_records)}.",
                manifest_path.name,
            )
        )
        run_record: dict[str, Any] = {}
    else:
        run_record = run_records[0]
    is_v2 = run_record.get("schema") == RUN_SCHEMA_V2
    legacy_evidence = (
        None
        if is_v2
        else _legacy_profile_evidence(
            run_record,
            manifest_records,
            ledger_records,
            run_dir,
            freeze_seal=freeze_seal,
            freeze_seal_sha256=freeze_seal_sha256,
            live_arm_freeze_seal=live_arm_freeze_seal,
            live_arm_freeze_seal_sha256=live_arm_freeze_seal_sha256,
        )
    )
    legacy_profile = legacy_evidence.profile_name if legacy_evidence is not None else None
    if legacy_evidence is not None:
        findings.extend(legacy_evidence.findings)
    profile_name = run_record.get("run_profile") if is_v2 else legacy_profile
    mode = run_record.get("mode", "unknown")
    run_status = (
        run_record.get("lifecycle_state") if is_v2 else run_record.get("status")
    )
    allowed_lifecycle_states = (
        set(LIVE_STATE_CHAIN_V2) | set(SHADOW_STATE_CHAIN_V2)
        if is_v2
        else ALLOWED_RUN_STATUSES
    )
    if run_record and (
        not isinstance(run_status, str) or run_status not in allowed_lifecycle_states
    ):
        findings.append(
            Finding(
                "RUN_STATUS_INVALID",
                "ERROR",
                f"Unsupported run lifecycle status {run_status!r}.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    elif run_record and run_status != "complete" and not (is_v2 and checkpoint):
        findings.append(
            Finding(
                "RUN_NOT_COMPLETE",
                "UNKNOWN",
                f"Run lifecycle status is {run_status!r}; completion invariants are not yet certifiable.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    complete = run_status == "complete"
    matched_pilot = profile_name == "v2_matched_nonrouting"
    excluded_scope_roots = (
        _declared_child_relative_paths(run_dir, run_record)
        if is_v2
        else _legacy_excluded_relative_paths(run_dir)
    )
    if run_record and (
        not isinstance(mode, str) or mode not in {"audited_funnel", "archipelago_lite_shadow"}
    ):
        findings.append(
            Finding(
                "RUN_MODE_INVALID",
                "ERROR",
                f"Unsupported generation mode {mode!r}.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    if run_record and not is_v2 and mode == "archipelago_lite_shadow" and run_record.get("matched_pilot") is not True:
        findings.append(
            Finding(
                "SHADOW_MATCHED_PILOT_REQUIRED",
                "ERROR",
                "archipelago_lite_shadow is a matched-only diagnostic mode and must declare matched_pilot=true.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    if run_record and run_record.get("file_read_log_complete") is not True:
        findings.append(
            Finding(
                "FILE_READ_LOG_COMPLETENESS_UNKNOWN",
                "UNKNOWN",
                "Run record must attest that every agent file read was logged.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    if run_record and run_record.get("tool_event_log_complete") is not True:
        findings.append(
            Finding(
                "TOOL_EVENT_LOG_COMPLETENESS_UNKNOWN",
                "UNKNOWN",
                "Run record must attest that every in-window tool event was logged.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )

    run_start = _parse_timestamp(run_record.get("started_at"))
    run_end = _parse_timestamp(run_record.get("ended_at"))
    run_boundary = (
        run_end
        if run_end is not None
        else _parse_timestamp(run_record.get("deadline_at")) if is_v2 else None
    )
    if run_record and (run_start is None or run_boundary is None):
        findings.append(
            Finding(
                "RUN_WINDOW_UNKNOWN",
                "UNKNOWN",
                "Run start and its actual end or planned deadline must be offset-aware timestamps.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    elif run_start is not None and run_boundary is not None and run_boundary < run_start:
        findings.append(
            Finding(
                "RUN_WINDOW_INVALID",
                "ERROR",
                "Run end precedes run start.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )

    anchor_files_by_path: dict[str, dict[str, Any]] = {}
    anchor_blocks_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}
    sealed_finalists_by_id: dict[str, dict[str, Any]] = {}
    trust_inputs_present = all(
        (
            isinstance(protection_anchor, dict),
            isinstance(protection_anchor_sha256, str),
            isinstance(freeze_seal, dict),
            isinstance(freeze_seal_sha256, str),
        )
    )
    pre_freeze_checkpoint = is_v2 and checkpoint in {"selection", "freeze"}
    if not trust_inputs_present:
        if not (
            pre_freeze_checkpoint
            and isinstance(protection_anchor, dict)
            and isinstance(protection_anchor_sha256, str)
        ):
            findings.append(
                Finding(
                    "EXTERNAL_TRUST_PINS_MISSING",
                    "UNKNOWN",
                    "A completed native audit needs externally pinned pre-run protection and post-freeze seal snapshots; pre-freeze checkpoints still require the protection pin.",
                    manifest_path.name,
                )
            )
    else:
        assert protection_anchor is not None
        assert protection_anchor_sha256 is not None
        assert freeze_seal is not None
        assert freeze_seal_sha256 is not None
        if _json_payload_sha256(protection_anchor) != protection_anchor_sha256:
            findings.append(
                Finding(
                    "PROTECTION_ANCHOR_PAYLOAD_HASH_MISMATCH",
                    "ERROR",
                    "The supplied protection-anchor payload does not match its SHA-256 pin.",
                )
            )
        if _json_payload_sha256(freeze_seal) != freeze_seal_sha256:
            findings.append(
                Finding(
                    "FREEZE_SEAL_PAYLOAD_HASH_MISMATCH",
                    "ERROR",
                    "The supplied freeze-seal payload does not match its SHA-256 pin.",
                )
            )
        if not re.fullmatch(r"[0-9a-f]{64}", protection_anchor_sha256):
            findings.append(
                Finding(
                    "PROTECTION_ANCHOR_PIN_INVALID",
                    "ERROR",
                    "Protection anchor SHA-256 pin must be a lowercase 64-character digest.",
                )
            )
        if not re.fullmatch(r"[0-9a-f]{64}", freeze_seal_sha256):
            findings.append(
                Finding(
                    "FREEZE_SEAL_PIN_INVALID",
                    "ERROR",
                    "Freeze-seal SHA-256 pin must be a lowercase 64-character digest.",
                )
            )
        expected_anchor_schema = (
            PROTECTION_ANCHOR_SCHEMA_V2 if is_v2 else PROTECTION_ANCHOR_SCHEMA
        )
        if protection_anchor.get("schema") != expected_anchor_schema:
            findings.append(
                Finding("PROTECTION_ANCHOR_SCHEMA_INVALID", "ERROR", "Unsupported protection anchor schema.")
            )
        if protection_anchor.get("contract_profile") != CONTRACT_PROFILE:
            findings.append(
                Finding("PROTECTION_ANCHOR_PROFILE_INVALID", "ERROR", "Protection anchor does not use the required fixed-contract profile.")
            )
        if protection_anchor.get("run_id") != run_dir.name:
            findings.append(
                Finding("PROTECTION_ANCHOR_RUN_MISMATCH", "ERROR", "Protection anchor belongs to another run.")
            )
        if protection_anchor.get("run_dir") != str(run_dir):
            findings.append(
                Finding("PROTECTION_ANCHOR_PATH_MISMATCH", "ERROR", "Protection anchor is not bound to the canonical run directory.")
            )
        anchor_created_at = _parse_timestamp(protection_anchor.get("created_at"))
        if anchor_created_at is None or (
            run_start is not None and anchor_created_at > run_start
        ):
            findings.append(
                Finding("PROTECTION_ANCHOR_TIME_INVALID", "ERROR", "Protection anchor must be created no later than run start.")
            )
        if protection_anchor.get("block_semantics") != "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1":
            findings.append(
                Finding("PROTECTION_ANCHOR_BLOCK_SEMANTICS_INVALID", "ERROR", "Protection anchor block semantics are missing or unsupported.")
            )

        anchor_file_ids: set[str] = set()
        anchor_files = protection_anchor.get("files")
        if not isinstance(anchor_files, list):
            findings.append(
                Finding("PROTECTION_ANCHOR_FILES_INVALID", "ERROR", "Protection anchor files must be a list.")
            )
        else:
            for item in anchor_files:
                if not isinstance(item, dict):
                    findings.append(Finding("PROTECTION_ANCHOR_FILE_INVALID", "ERROR", "Protection anchor file entries must be objects."))
                    continue
                contract_id = item.get("id")
                raw_path_value = item.get("path")
                digest = item.get("sha256")
                if (
                    not isinstance(contract_id, str)
                    or contract_id not in required_protected_paths
                    or not isinstance(raw_path_value, str)
                    or not Path(raw_path_value).is_absolute()
                    or _is_within(Path(raw_path_value), run_dir)
                    or not isinstance(digest, str)
                    or not re.fullmatch(r"[0-9a-f]{64}", digest)
                ):
                    findings.append(Finding("PROTECTION_ANCHOR_FILE_INVALID", "ERROR", "Protection anchor file entry is malformed or unknown."))
                    continue
                resolved_key = str(Path(raw_path_value).resolve(strict=False))
                if contract_id in anchor_file_ids or resolved_key in anchor_files_by_path:
                    findings.append(Finding("PROTECTION_ANCHOR_FILE_DUPLICATE", "ERROR", f"Protection anchor duplicates {contract_id}."))
                    continue
                expected_path = str(
                    Path(required_protected_paths[contract_id]).resolve(strict=False)
                )
                if resolved_key != expected_path:
                    findings.append(Finding("PROTECTION_ANCHOR_FILE_PATH_INVALID", "ERROR", f"Protection anchor ID {contract_id} is not bound to its exact canonical path."))
                anchor_file_ids.add(contract_id)
                anchor_files_by_path[resolved_key] = item
        missing_anchor_file_ids = sorted(set(required_protected_paths) - anchor_file_ids)
        if missing_anchor_file_ids:
            findings.append(Finding("PROTECTION_ANCHOR_FILE_SET_INCOMPLETE", "ERROR", f"Protection anchor omits fixed contracts: {missing_anchor_file_ids}."))

        anchor_block_ids: set[str] = set()
        anchor_blocks = protection_anchor.get("blocks")
        if not isinstance(anchor_blocks, list):
            findings.append(Finding("PROTECTION_ANCHOR_BLOCKS_INVALID", "ERROR", "Protection anchor blocks must be a list."))
        else:
            for item in anchor_blocks:
                if not isinstance(item, dict):
                    findings.append(Finding("PROTECTION_ANCHOR_BLOCK_INVALID", "ERROR", "Protection anchor block entries must be objects."))
                    continue
                block_id = item.get("id")
                raw_path_value = item.get("path")
                start_marker = item.get("start_marker")
                end_marker = item.get("end_marker")
                digest = item.get("sha256")
                if (
                    not isinstance(block_id, str)
                    or block_id not in REQUIRED_PROTECTED_BLOCK_IDS
                    or not isinstance(raw_path_value, str)
                    or not Path(raw_path_value).is_absolute()
                    or _is_within(Path(raw_path_value), run_dir)
                    or not isinstance(start_marker, str)
                    or not isinstance(end_marker, str)
                    or not isinstance(digest, str)
                    or not re.fullmatch(r"[0-9a-f]{64}", digest)
                ):
                    findings.append(Finding("PROTECTION_ANCHOR_BLOCK_INVALID", "ERROR", "Protection anchor block entry is malformed or unknown."))
                    continue
                if (start_marker, end_marker) != REQUIRED_PROTECTED_BLOCK_IDS[block_id]:
                    findings.append(Finding("PROTECTION_ANCHOR_BLOCK_MARKERS_INVALID", "ERROR", f"Protection anchor block {block_id} uses the wrong marker pair."))
                key = (str(Path(raw_path_value).resolve(strict=False)), start_marker, end_marker)
                if key[0] != str(
                    Path(required_protected_paths["orchestration-prompt"]).resolve(
                        strict=False
                    )
                ):
                    findings.append(
                        Finding(
                            "PROTECTION_ANCHOR_BLOCK_PATH_INVALID",
                            "ERROR",
                            "Protected validation block is not bound to the exact canonical orchestration prompt.",
                        )
                    )
                if block_id in anchor_block_ids or key in anchor_blocks_by_key:
                    findings.append(Finding("PROTECTION_ANCHOR_BLOCK_DUPLICATE", "ERROR", f"Protection anchor duplicates {block_id}."))
                    continue
                anchor_block_ids.add(block_id)
                anchor_blocks_by_key[key] = item
        missing_anchor_block_ids = sorted(set(REQUIRED_PROTECTED_BLOCK_IDS) - anchor_block_ids)
        if missing_anchor_block_ids:
            findings.append(Finding("PROTECTION_ANCHOR_BLOCK_SET_INCOMPLETE", "ERROR", f"Protection anchor omits required blocks: {missing_anchor_block_ids}."))

        expected_freeze_schema = FREEZE_SEAL_SCHEMA_V2 if is_v2 else FREEZE_SEAL_SCHEMA
        if freeze_seal.get("schema") != expected_freeze_schema:
            findings.append(Finding("FREEZE_SEAL_SCHEMA_INVALID", "ERROR", "Unsupported freeze-seal schema."))
        if freeze_seal.get("run_id") != run_dir.name or freeze_seal.get("run_dir") != str(run_dir):
            findings.append(Finding("FREEZE_SEAL_RUN_MISMATCH", "ERROR", "Freeze seal belongs to another run or directory."))
        freeze_identity_mismatch = (
            freeze_seal.get("mode") != mode
            or freeze_seal.get("model") != run_record.get("model")
            or freeze_seal.get("reasoning_effort") != run_record.get("reasoning_effort")
        )
        if is_v2:
            freeze_identity_mismatch = freeze_identity_mismatch or any(
                freeze_seal.get(key) != run_record.get(key)
                for key in (
                    "run_profile",
                    "scope_id",
                    "arm",
                    "routing_state",
                    "cohort_kind",
                    "wave_index",
                    "selection_policy",
                    "seed",
                    "candidate_order_seed",
                    "parent_scope_id",
                    "results_visibility",
                    "development_contract_sha256",
                )
            )
            if run_record.get("arm") == "shadow":
                freeze_identity_mismatch = freeze_identity_mismatch or (
                    freeze_seal.get("live_arm_freeze_seal_sha256")
                    != run_record.get("live_arm_freeze_seal_sha256")
                )
            if run_record.get("cohort_kind") == "regeneration":
                freeze_identity_mismatch = freeze_identity_mismatch or (
                    freeze_seal.get("parent_scope_id") != run_record.get("parent_scope_id")
                    or freeze_seal.get("initial_freeze_seal_sha256")
                    != run_record.get("initial_freeze_seal_sha256")
                )
        else:
            freeze_identity_mismatch = (
                freeze_identity_mismatch
                or freeze_seal.get("matched_pilot")
                is not (run_record.get("matched_pilot") is True)
            )
        if freeze_identity_mismatch:
            findings.append(Finding("FREEZE_SEAL_RUN_CONTRACT_MISMATCH", "ERROR", "Freeze seal does not bind the exact run profile, scope, routing state, model, and reasoning effort."))
        if freeze_seal.get("protection_anchor_sha256") != protection_anchor_sha256:
            findings.append(Finding("FREEZE_SEAL_ANCHOR_MISMATCH", "ERROR", "Freeze seal is not bound to the supplied protection-anchor pin."))
        sealed_at = _parse_timestamp(freeze_seal.get("sealed_at"))
        if sealed_at is None or (
            run_start is not None
            and run_end is not None
            and not (run_start <= sealed_at <= run_end)
        ):
            findings.append(Finding("FREEZE_SEAL_TIME_INVALID", "ERROR", "Freeze seal needs an in-window offset-aware sealed_at timestamp."))
        seal_entries = freeze_seal.get("finalists")
        if not isinstance(seal_entries, list):
            findings.append(Finding("FREEZE_SEAL_FINALISTS_INVALID", "ERROR", "Freeze-seal finalists must be a list."))
        else:
            for item in seal_entries:
                if not isinstance(item, dict):
                    findings.append(Finding("FREEZE_SEAL_FINALIST_INVALID", "ERROR", "Freeze-seal finalist entries must be objects."))
                    continue
                finalist_id = item.get("finalist_id")
                if not isinstance(finalist_id, str) or not finalist_id.strip():
                    findings.append(Finding("FREEZE_SEAL_FINALIST_INVALID", "ERROR", "Freeze-seal finalist has no stable ID."))
                    continue
                if finalist_id in sealed_finalists_by_id:
                    findings.append(Finding("FREEZE_SEAL_FINALIST_DUPLICATE", "ERROR", f"Freeze seal duplicates {finalist_id}."))
                sealed_finalists_by_id[finalist_id] = item

    if pre_freeze_checkpoint and isinstance(protection_anchor, dict):
        for item in protection_anchor.get("files", []):
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                anchor_files_by_path[str(Path(item["path"]).resolve(strict=False))] = item
        for item in protection_anchor.get("blocks", []):
            if (
                isinstance(item, dict)
                and isinstance(item.get("path"), str)
                and isinstance(item.get("start_marker"), str)
                and isinstance(item.get("end_marker"), str)
            ):
                key = (
                    str(Path(item["path"]).resolve(strict=False)),
                    item["start_marker"],
                    item["end_marker"],
                )
                anchor_blocks_by_key[key] = item

    def check_run_time(
        value: Any,
        *,
        code: str,
        label: str,
        artifact: str,
        line: int | None,
        ids: tuple[str, ...] = (),
        missing_severity: str = "UNKNOWN",
    ) -> datetime | None:
        parsed = _parse_timestamp(value)
        if parsed is None:
            findings.append(
                Finding(
                    f"{code}_TIME_UNKNOWN",
                    missing_severity,
                    f"{label} lacks an offset-aware timestamp.",
                    artifact,
                    line,
                    ids,
                )
            )
            return None
        if run_start is not None and run_end is not None and not (run_start <= parsed <= run_end):
            findings.append(
                Finding(
                    f"{code}_OUTSIDE_RUN_WINDOW",
                    "ERROR",
                    f"{label} timestamp {parsed.isoformat()} is outside the declared run window.",
                    artifact,
                    line,
                    ids,
                )
            )
        return parsed

    protected_files = run_record.get("protected_files")
    protected_blocks = run_record.get("protected_blocks")
    if not isinstance(protected_files, list) or not isinstance(protected_blocks, list):
        findings.append(
            Finding(
                "PROTECTED_CONTRACT_HASHES_UNKNOWN",
                "UNKNOWN",
                "Run record must declare protected_files and protected_blocks.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    elif not protected_files or not protected_blocks:
        findings.append(
            Finding(
                "PROTECTED_CONTRACT_SET_EMPTY",
                "ERROR",
                "Completed runs must bind all required protected files and validator-routing blocks before execution.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    else:
        observed_protected_ids: set[str] = set()
        for item in protected_files:
            if not isinstance(item, dict):
                findings.append(
                    Finding(
                        "PROTECTED_FILE_RECORD_INVALID",
                        "ERROR",
                        "protected_files entries must be objects.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
                continue
            raw_path_value = item.get("path")
            protected_path = Path(raw_path_value) if isinstance(raw_path_value, str) else None
            if protected_path is not None and not protected_path.is_absolute():
                protected_path = run_dir / protected_path
            contract_id = _required_file_id(raw_path_value, required_protected_paths)
            if contract_id is None:
                findings.append(
                    Finding(
                        "PROTECTED_FILE_CANONICAL_PATH_INVALID",
                        "ERROR",
                        f"Protected file is not one of the exact canonical fixed-contract paths: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif contract_id in observed_protected_ids:
                findings.append(
                    Finding(
                        "PROTECTED_FILE_ID_DUPLICATE",
                        "ERROR",
                        f"Protected file inventory duplicates fixed contract {contract_id}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            else:
                observed_protected_ids.add(contract_id)
            anchor_item = (
                anchor_files_by_path.get(str(protected_path.resolve(strict=False)))
                if protected_path is not None
                else None
            )
            pre_hash = item.get("pre_run_sha256")
            post_hash = item.get("sha256")
            captured_at = _parse_timestamp(item.get("captured_at"))
            if (
                not isinstance(pre_hash, str)
                or not re.fullmatch(r"[0-9a-f]{64}", pre_hash)
                or not isinstance(post_hash, str)
                or not re.fullmatch(r"[0-9a-f]{64}", post_hash)
            ):
                findings.append(
                    Finding(
                        "PROTECTED_FILE_SNAPSHOT_INVALID",
                        "ERROR",
                        f"Protected file must record lowercase pre-run and post-run SHA-256 values: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif pre_hash != post_hash:
                findings.append(
                    Finding(
                        "PROTECTED_FILE_CHANGED_DURING_RUN",
                        "ERROR",
                        f"Protected file pre/post hashes differ: {raw_path_value}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if trust_inputs_present:
                if anchor_item is None:
                    findings.append(
                        Finding(
                            "PROTECTED_FILE_NOT_EXTERNALLY_ANCHORED",
                            "ERROR",
                            f"Protected file path is absent from the externally pinned anchor: {raw_path_value!r}.",
                            manifest_path.name,
                            run_record.get("_line"),
                        )
                    )
                elif pre_hash != anchor_item.get("sha256"):
                    findings.append(
                        Finding(
                            "PROTECTED_FILE_EXTERNAL_ANCHOR_MISMATCH",
                            "ERROR",
                            f"Manifest-local pre-run hash does not match the externally pinned anchor: {raw_path_value}.",
                            manifest_path.name,
                            run_record.get("_line"),
                        )
                    )
            if captured_at is None or (run_start is not None and captured_at > run_start):
                findings.append(
                    Finding(
                        "PROTECTED_FILE_SNAPSHOT_TIME_INVALID",
                        "ERROR",
                        f"Protected file snapshot must be timestamped no later than run start: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if protected_path is None or not protected_path.is_file():
                findings.append(
                    Finding(
                        "PROTECTED_FILE_MISSING",
                        "ERROR",
                        f"Protected file is missing: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif post_hash != _sha256(protected_path):
                findings.append(
                    Finding(
                        "PROTECTED_FILE_HASH_MISMATCH",
                        "ERROR",
                        f"Protected file hash changed: {raw_path_value}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
        missing_protected_ids = sorted(
            set(required_protected_paths) - observed_protected_ids
        )
        if missing_protected_ids:
            findings.append(
                Finding(
                    "PROTECTED_FILE_SET_INCOMPLETE",
                    "ERROR",
                    f"Protected file inventory is missing required contracts: {missing_protected_ids}.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        observed_block_markers: set[tuple[str, str]] = set()
        for item in protected_blocks:
            if not isinstance(item, dict):
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_RECORD_INVALID",
                        "ERROR",
                        "protected_blocks entries must be objects.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
                continue
            raw_path_value = item.get("path")
            start_marker = item.get("start_marker")
            end_marker = item.get("end_marker")
            normalized_block_path = (
                Path(raw_path_value).as_posix().casefold()
                if isinstance(raw_path_value, str)
                else ""
            )
            if not normalized_block_path.endswith("prompts/new_idea_agent_prompt.md"):
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_PATH_INVALID",
                        "ERROR",
                        "Protected validation marker blocks must bind prompts/NEW_IDEA_AGENT_PROMPT.md.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if isinstance(start_marker, str) and isinstance(end_marker, str):
                observed_block_markers.add((start_marker, end_marker))
            protected_path = Path(raw_path_value) if isinstance(raw_path_value, str) else None
            if protected_path is not None and not protected_path.is_absolute():
                protected_path = run_dir / protected_path
            anchor_key = (
                (
                    str(protected_path.resolve(strict=False)),
                    str(start_marker or ""),
                    str(end_marker or ""),
                )
                if protected_path is not None
                else None
            )
            anchor_item = anchor_blocks_by_key.get(anchor_key) if anchor_key is not None else None
            block_hash = (
                _marker_block_sha256(
                    protected_path,
                    str(start_marker or ""),
                    str(end_marker or ""),
                )
                if protected_path is not None and protected_path.is_file()
                else None
            )
            pre_hash = item.get("pre_run_sha256")
            post_hash = item.get("sha256")
            captured_at = _parse_timestamp(item.get("captured_at"))
            if (
                not isinstance(pre_hash, str)
                or not re.fullmatch(r"[0-9a-f]{64}", pre_hash)
                or not isinstance(post_hash, str)
                or not re.fullmatch(r"[0-9a-f]{64}", post_hash)
            ):
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_SNAPSHOT_INVALID",
                        "ERROR",
                        f"Protected block must record lowercase pre-run and post-run SHA-256 values: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif pre_hash != post_hash:
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_CHANGED_DURING_RUN",
                        "ERROR",
                        f"Protected block pre/post hashes differ: {raw_path_value}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if trust_inputs_present:
                if anchor_item is None:
                    findings.append(
                        Finding(
                            "PROTECTED_BLOCK_NOT_EXTERNALLY_ANCHORED",
                            "ERROR",
                            f"Protected block is absent from the externally pinned anchor: {raw_path_value!r}.",
                            manifest_path.name,
                            run_record.get("_line"),
                        )
                    )
                elif pre_hash != anchor_item.get("sha256"):
                    findings.append(
                        Finding(
                            "PROTECTED_BLOCK_EXTERNAL_ANCHOR_MISMATCH",
                            "ERROR",
                            f"Manifest-local block hash does not match the externally pinned anchor: {raw_path_value}.",
                            manifest_path.name,
                            run_record.get("_line"),
                        )
                    )
            if captured_at is None or (run_start is not None and captured_at > run_start):
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_SNAPSHOT_TIME_INVALID",
                        "ERROR",
                        f"Protected block snapshot must be timestamped no later than run start: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if block_hash is None:
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_UNREADABLE",
                        "ERROR",
                        f"Protected marker block is missing or ambiguous: {raw_path_value!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif post_hash != block_hash:
                findings.append(
                    Finding(
                        "PROTECTED_BLOCK_HASH_MISMATCH",
                        "ERROR",
                        f"Protected marker block hash changed: {raw_path_value}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
        missing_block_markers = sorted(REQUIRED_PROTECTED_BLOCKS - observed_block_markers)
        if missing_block_markers:
            findings.append(
                Finding(
                    "PROTECTED_BLOCK_SET_INCOMPLETE",
                    "ERROR",
                    f"Protected block inventory is missing required marker pairs: {missing_block_markers}.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )

    mappings = [r for r in ledger_records if r.get("record_type") == "mapping"]
    mapping_by_raw: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for mapping in mappings:
        raw_id = mapping.get("raw_id")
        direction_id = mapping.get("direction_id")
        if not isinstance(raw_id, str) or not raw_id:
            findings.append(
                Finding(
                    "MAPPING_RAW_ID_MISSING",
                    "ERROR",
                    "Mapping has no raw_id.",
                    ledger_path.name,
                    mapping.get("_line"),
                )
            )
            continue
        mapping_by_raw[raw_id].append(mapping)
        if mode == "archipelago_lite_shadow":
            creator_agent_id = mapping.get("creator_agent_id")
            if not isinstance(creator_agent_id, str) or not creator_agent_id.strip():
                findings.append(
                    Finding(
                        "CONCEPT_CREATOR_MISSING",
                        "ERROR",
                        f"Raw concept {raw_id} has no creator_agent_id.",
                        ledger_path.name,
                        mapping.get("_line"),
                        (raw_id,),
                    )
                )
        if raw_id not in raw_set:
            findings.append(
                Finding(
                    "RAW_ID_UNKNOWN",
                    "ERROR",
                    f"Mapping references unknown raw ID {raw_id}.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )
        if not isinstance(direction_id, str) or not direction_id:
            findings.append(
                Finding(
                    "DIRECTION_ID_MISSING",
                    "ERROR",
                    f"Mapping for {raw_id} has no direction_id.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )
        cluster_id = mapping.get("cluster_id")
        if not isinstance(cluster_id, str) or not cluster_id.strip():
            findings.append(
                Finding(
                    "MAPPING_CLUSTER_ID_MISSING",
                    "ERROR",
                    f"Mapping for {raw_id} has no reversible cluster_id.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )
        reason = mapping.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            findings.append(
                Finding(
                    "MAPPING_REASON_MISSING",
                    "ERROR",
                    f"Mapping for {raw_id} has no field-level disposition or merge rationale.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )
        disposition = mapping.get("disposition")
        if not isinstance(disposition, str) or disposition not in ALLOWED_DISPOSITIONS:
            findings.append(
                Finding(
                    "DISPOSITION_INVALID",
                    "ERROR",
                    f"Mapping for {raw_id} has invalid disposition {disposition!r}.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )
        elif disposition == "unresolved":
            findings.append(
                Finding(
                    "DISPOSITION_UNRESOLVED",
                    "INFO",
                    f"Raw ID {raw_id} is preserved with unresolved disposition.",
                    ledger_path.name,
                    mapping.get("_line"),
                    (raw_id,),
                )
            )

    for raw_id in sorted(raw_set):
        mapped = mapping_by_raw.get(raw_id, [])
        if not mapped:
            findings.append(
                Finding(
                    "RAW_UNACCOUNTED",
                    "ERROR",
                    f"Raw ID {raw_id} has no mapping.",
                    ledger_path.name,
                    node_ids=(raw_id,),
                )
            )
        elif len(mapped) > 1:
            findings.append(
                Finding(
                    "RAW_MAPPING_DUPLICATE",
                    "ERROR",
                    f"Raw ID {raw_id} has {len(mapped)} primary mappings.",
                    ledger_path.name,
                    node_ids=(raw_id,),
                )
            )

    direction_ids = {
        r.get("direction_id")
        for r in mappings
        if isinstance(r.get("direction_id"), str) and r.get("direction_id")
    }
    counts["directions"] = len(direction_ids)
    counts["mappings"] = len(mappings)

    evidence_records = [r for r in ledger_records if r.get("record_type") == "evidence"]
    evidence_by_id: dict[str, dict[str, Any]] = {}
    source_records_for_lineage = [
        record
        for record in manifest_records
        if record.get("record_type") == "source_open"
    ]
    source_record_by_id = {
        record.get("source_event_id"): record
        for record in source_records_for_lineage
        if isinstance(record.get("source_event_id"), str)
    }
    for evidence in evidence_records:
        evidence_id = evidence.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            findings.append(
                Finding(
                    "EVIDENCE_ID_MISSING",
                    "ERROR",
                    "Evidence record has no evidence_id.",
                    ledger_path.name,
                    evidence.get("_line"),
                )
            )
        elif evidence_id in evidence_by_id:
            findings.append(
                Finding(
                    "EVIDENCE_ID_DUPLICATE",
                    "ERROR",
                    f"Evidence ID {evidence_id} is duplicated.",
                    ledger_path.name,
                    evidence.get("_line"),
                    (evidence_id,),
                )
            )
        else:
            evidence_by_id[evidence_id] = evidence
            for field_name in ("proposition", "source", "cheapest_resolving_test"):
                value = evidence.get(field_name)
                if not isinstance(value, str) or not value.strip():
                    findings.append(
                        Finding(
                            "EVIDENCE_FIELD_MISSING",
                            "ERROR",
                            f"Evidence {evidence_id} lacks required field {field_name}.",
                            ledger_path.name,
                            evidence.get("_line"),
                            (evidence_id,),
                        )
                    )
            status = evidence.get("status")
            if not isinstance(status, str) or status not in ALLOWED_EVIDENCE_STATUSES:
                findings.append(
                    Finding(
                        "EVIDENCE_STATUS_INVALID",
                        "ERROR",
                        f"Evidence {evidence_id} has invalid status {status!r}.",
                        ledger_path.name,
                        evidence.get("_line"),
                        (evidence_id,),
                    )
                )
            if not isinstance(evidence.get("decision_critical"), bool):
                findings.append(
                    Finding(
                        "EVIDENCE_DECISION_FLAG_INVALID",
                        "ERROR",
                        f"Evidence {evidence_id} must declare boolean decision_critical.",
                        ledger_path.name,
                        evidence.get("_line"),
                        (evidence_id,),
                    )
                )
            evidence_entity_ids, evidence_entities_valid = _valid_string_list(
                evidence.get("entity_ids")
            )
            if not evidence_entities_valid:
                findings.append(
                    Finding(
                        "EVIDENCE_ENTITY_IDS_INVALID",
                        "ERROR",
                        f"Evidence {evidence_id} must name every problem/concept entity it supports.",
                        ledger_path.name,
                        evidence.get("_line"),
                        (evidence_id,),
                    )
                )
            direction_id = evidence.get("direction_id")
            if not isinstance(direction_id, str) or direction_id not in direction_ids:
                findings.append(
                    Finding(
                        "EVIDENCE_DIRECTION_UNKNOWN",
                        "ERROR",
                        f"Evidence {evidence_id} references unknown direction {direction_id!r}.",
                        ledger_path.name,
                        evidence.get("_line"),
                        (evidence_id,),
                    )
                )
            check_run_time(
                evidence.get("recorded_at"),
                code="EVIDENCE",
                label=f"Evidence {evidence_id}",
                artifact=ledger_path.name,
                line=evidence.get("_line"),
                ids=(evidence_id,),
            )

    finalist_records = [r for r in ledger_records if r.get("record_type") == "finalist"]
    seen_finalists: set[str] = set()
    finalist_hashes: dict[str, str] = {}
    finalist_times: dict[str, datetime] = {}
    for finalist in finalist_records:
        line = finalist.get("_line")
        finalist_id = finalist.get("finalist_id")
        if not isinstance(finalist_id, str) or not finalist_id.strip():
            findings.append(
                Finding("FINALIST_ID_MISSING", "ERROR", "Finalist record has no valid finalist_id.", ledger_path.name, line)
            )
            continue
        finalist_id = finalist_id.strip()
        if finalist_id in seen_finalists:
            findings.append(
                Finding("FINALIST_ID_DUPLICATE", "ERROR", f"Finalist ID {finalist_id} is duplicated.", ledger_path.name, line, (finalist_id,))
            )
        seen_finalists.add(finalist_id)

        direction_id = finalist.get("direction_id")
        if not isinstance(direction_id, str) or not direction_id.strip():
            findings.append(
                Finding("FINALIST_DIRECTION_INVALID", "ERROR", f"Finalist {finalist_id} has no valid direction ID.", ledger_path.name, line, (finalist_id,))
            )
            direction_id = ""
        elif direction_id not in direction_ids:
            findings.append(
                Finding("FINALIST_DIRECTION_UNKNOWN", "ERROR", f"Finalist {finalist_id} references unknown direction {direction_id!r}.", ledger_path.name, line, (finalist_id,))
            )

        ancestry, ancestry_valid = _valid_string_list(finalist.get("raw_ids"))
        if not ancestry_valid:
            findings.append(
                Finding("FINALIST_NO_RAW_ANCESTOR", "ERROR", f"Finalist {finalist_id} raw_ids must be a non-empty list of strings.", ledger_path.name, line, (finalist_id,))
            )
        for raw_id in ancestry:
            if raw_id not in raw_set:
                findings.append(
                    Finding("FINALIST_RAW_UNKNOWN", "ERROR", f"Finalist {finalist_id} references unknown raw ID {raw_id!r}.", ledger_path.name, line, (finalist_id, raw_id))
                )
                continue
            raw_mappings = mapping_by_raw.get(raw_id, [])
            if len(raw_mappings) != 1:
                continue
            mapped = raw_mappings[0]
            mapped_direction = mapped.get("direction_id")
            if mapped_direction != direction_id:
                findings.append(
                    Finding("FINALIST_ANCESTRY_DIRECTION_MISMATCH", "ERROR", f"Raw ID {raw_id} maps to {mapped_direction}, not {direction_id}.", ledger_path.name, line, (finalist_id, raw_id))
                )
            if mapped.get("disposition") not in {"retained", "merged"}:
                findings.append(
                    Finding("FINALIST_ANCESTRY_INELIGIBLE", "ERROR", f"Raw ID {raw_id} has disposition {mapped.get('disposition')!r} and cannot support a finalist.", ledger_path.name, line, (finalist_id, raw_id))
                )

        frozen_at = check_run_time(
            finalist.get("frozen_at"),
            code="FINALIST_FREEZE",
            label=f"Finalist {finalist_id} freeze",
            artifact=ledger_path.name,
            line=line,
            ids=(finalist_id,),
        )
        if frozen_at is not None:
            finalist_times[finalist_id] = frozen_at

        raw_artifact_value = finalist.get("artifact_path")
        unresolved_artifact = (
            run_dir / raw_artifact_value
            if isinstance(raw_artifact_value, str) and not Path(raw_artifact_value).is_absolute()
            else Path(raw_artifact_value)
            if isinstance(raw_artifact_value, str)
            else None
        )
        artifact_path, artifact_rel = _canonical_run_path(run_dir, raw_artifact_value)
        declared_hash = finalist.get("sha256")
        if artifact_path is None or artifact_rel is None:
            findings.append(
                Finding("FINALIST_ARTIFACT_PATH_INVALID", "ERROR", f"Finalist {finalist_id} has no safe artifact_path inside the run folder.", ledger_path.name, line, (finalist_id,))
            )
        elif not artifact_path.is_file():
            findings.append(
                Finding("FINALIST_ARTIFACT_MISSING", "ERROR", f"Finalist {finalist_id} artifact does not exist: {artifact_rel}.", ledger_path.name, line, (finalist_id,))
            )
        elif unresolved_artifact is not None and unresolved_artifact.is_symlink():
            findings.append(
                Finding("FINALIST_ARTIFACT_SYMLINK", "ERROR", f"Finalist {finalist_id} artifact must be a regular non-symlink file.", artifact_rel, node_ids=(finalist_id,))
            )
        elif not isinstance(declared_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            findings.append(
                Finding("FINALIST_HASH_INVALID", "ERROR", f"Finalist {finalist_id} must declare a lowercase SHA-256 hash.", ledger_path.name, line, (finalist_id,))
            )
        else:
            observed_hash = _sha256(artifact_path)
            if declared_hash != observed_hash:
                findings.append(
                    Finding("FINALIST_HASH_MISMATCH", "ERROR", f"Finalist {finalist_id} artifact hash does not match frozen content.", artifact_rel, node_ids=(finalist_id,))
                )
            previous = finalist_hashes.get(declared_hash)
            if previous is not None and previous != finalist_id:
                findings.append(
                    Finding("FINALIST_CONTENT_DUPLICATE", "ERROR", f"Finalists {previous} and {finalist_id} have identical frozen content.", artifact_rel, node_ids=(previous, finalist_id))
                )
            finalist_hashes[declared_hash] = finalist_id

        if (
            artifact_path is not None
            and artifact_path.is_file()
            and finalist.get("arm") in {"shadow", "matched_baseline"}
        ):
            try:
                finalist_text = artifact_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                finalist_text = ""
            if any(
                pattern.search(finalist_text)
                for pattern in PROHIBITED_PACKET_PATTERNS
            ):
                findings.append(
                    Finding(
                        "NONROUTING_FINALIST_PROHIBITED_CONTENT",
                        "ERROR",
                        f"Non-routing finalist {finalist_id} contains prohibited validator, score, threshold, or evaluator material.",
                        artifact_rel or "",
                        node_ids=(finalist_id,),
                    )
                )

        if trust_inputs_present:
            sealed_item = sealed_finalists_by_id.get(finalist_id)
            if sealed_item is None:
                findings.append(
                    Finding("FINALIST_EXTERNAL_SEAL_MISSING", "ERROR", f"Finalist {finalist_id} is absent from the externally pinned freeze seal.", ledger_path.name, line, (finalist_id,))
                )
            else:
                expected_fields = {
                    "arm": finalist.get("arm"),
                    "artifact_path": artifact_rel,
                    "frozen_at": finalist.get("frozen_at"),
                    "sha256": declared_hash,
                }
                mismatches = sorted(
                    field
                    for field, expected in expected_fields.items()
                    if sealed_item.get(field) != expected
                )
                if mismatches:
                    findings.append(
                        Finding("FINALIST_EXTERNAL_SEAL_MISMATCH", "ERROR", f"Finalist {finalist_id} differs from the externally pinned seal in fields {mismatches}.", ledger_path.name, line, (finalist_id,))
                    )
                sealed_at = _parse_timestamp(freeze_seal.get("sealed_at")) if isinstance(freeze_seal, dict) else None
                if frozen_at is not None and sealed_at is not None and (
                    sealed_at <= frozen_at if is_v2 else sealed_at < frozen_at
                ):
                    findings.append(
                        Finding("FINALIST_SEALED_BEFORE_FREEZE", "ERROR", f"Finalist {finalist_id} freeze must be strictly earlier than the externally pinned V2 seal.", ledger_path.name, line, (finalist_id,))
                    )

        evidence_ids, evidence_valid = _valid_string_list(finalist.get("evidence_ids"))
        if not evidence_valid:
            findings.append(
                Finding("FINALIST_EVIDENCE_MISSING", "UNKNOWN", f"Finalist {finalist_id} must cite a non-empty string list of decision-critical evidence IDs.", ledger_path.name, line, (finalist_id,))
            )
        has_decision_critical = False
        has_qualifying_decision_critical = False
        for evidence_id in evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                findings.append(
                    Finding("FINALIST_EVIDENCE_UNKNOWN", "ERROR", f"Finalist {finalist_id} cites unknown evidence {evidence_id!r}.", ledger_path.name, line, (finalist_id, evidence_id))
                )
                continue
            is_decision_critical = evidence.get("decision_critical") is True
            has_decision_critical |= is_decision_critical
            has_qualifying_decision_critical |= (
                is_decision_critical
                and evidence.get("status") != "contradicted"
            )
            if evidence.get("direction_id") != direction_id:
                findings.append(
                    Finding("FINALIST_EVIDENCE_DIRECTION_MISMATCH", "ERROR", f"Evidence {evidence_id} is not linked to finalist direction {direction_id}.", ledger_path.name, evidence.get("_line"), (finalist_id, evidence_id))
                )
            recorded_at = _parse_timestamp(evidence.get("recorded_at"))
            if recorded_at is not None and frozen_at is not None and recorded_at > frozen_at:
                findings.append(
                    Finding("EVIDENCE_RECORDED_AFTER_FREEZE", "ERROR", f"Evidence {evidence_id} was recorded after finalist {finalist_id} froze.", ledger_path.name, evidence.get("_line"), (finalist_id, evidence_id))
                )
        if evidence_ids and not has_decision_critical:
            findings.append(
                Finding("FINALIST_DECISION_CRITICAL_EVIDENCE_MISSING", "UNKNOWN", f"Finalist {finalist_id} cites no evidence marked decision_critical.", ledger_path.name, line, (finalist_id,))
            )
        elif (
            evidence_ids
            and has_decision_critical
            and not has_qualifying_decision_critical
        ):
            findings.append(
                Finding(
                    "FINALIST_DECISION_CRITICAL_EVIDENCE_CONTRADICTED",
                    "UNKNOWN",
                    f"Finalist {finalist_id}'s only decision-critical evidence is explicitly contradicted; development remains recorded, but freeze support is incomplete.",
                    ledger_path.name,
                    line,
                    (finalist_id,),
                )
            )
        finalist_arm = finalist.get("arm")
        if isinstance(finalist_arm, str) and finalist_arm in {"shadow", "matched_baseline"} and finalist.get("validation_eligible") is not False:
            findings.append(
                Finding("NONROUTING_FINALIST_ELIGIBILITY_INVALID", "ERROR", f"Non-routing finalist {finalist_id} must set validation_eligible to false.", ledger_path.name, line, (finalist_id,))
            )

    counts["finalists"] = len(finalist_records)
    counts["evidence"] = len(evidence_records)

    if trust_inputs_present:
        ledger_finalist_ids = {
            record.get("finalist_id")
            for record in finalist_records
            if isinstance(record.get("finalist_id"), str)
        }
        sealed_finalist_ids = set(sealed_finalists_by_id)
        if ledger_finalist_ids != sealed_finalist_ids:
            findings.append(
                Finding(
                    "FREEZE_SEAL_FINALIST_SET_MISMATCH",
                    "ERROR",
                    f"Freeze-seal finalist IDs differ from the ledger; missing={sorted(ledger_finalist_ids - sealed_finalist_ids)}, extra={sorted(sealed_finalist_ids - ledger_finalist_ids)}.",
                    ledger_path.name,
                )
            )
        ledger_artifacts = {
            relative
            for record in finalist_records
            for _path, relative in [_canonical_run_path(run_dir, record.get("artifact_path"))]
            if relative is not None
        }
        if is_v2 and run_record.get("cohort_kind") == "regeneration":
            wave_index = run_record.get("wave_index")
            wave_pattern = re.compile(
                rf"^wave{wave_index}_candidate_.+\.md$"
                if isinstance(wave_index, int) and not isinstance(wave_index, bool)
                else r"a^"
            )
            candidate_like_pattern = re.compile(
                r"^(?:wave[1-9][0-9]*_candidate_|finalist_|shadow_finalist_|baseline_shadow_finalist_).+\.md$"
            )
            owned_candidate_like = {
                path.relative_to(run_dir).as_posix()
                for path in _owned_files(run_dir, excluded_scope_roots)
                if path.is_file() and candidate_like_pattern.match(path.name)
            }
            discovered_candidate_artifacts = {
                relative
                for relative in owned_candidate_like
                if wave_pattern.match(Path(relative).name)
            }
            wrong_namespace = sorted(owned_candidate_like - discovered_candidate_artifacts)
            if wrong_namespace:
                findings.append(
                    Finding(
                        "REGENERATION_CANDIDATE_NAMESPACE_MISMATCH",
                        "ERROR",
                        f"Regeneration contains candidate artifacts outside wave{wave_index}_candidate_*.md: {wrong_namespace}.",
                    )
                )
        else:
            candidate_name_patterns = (
                re.compile(r"^finalist_.*\.md$"),
                re.compile(r"^shadow_finalist_.*\.md$"),
                re.compile(r"^baseline_shadow_finalist_.*\.md$"),
            )
            discovered_candidate_artifacts = {
                path.relative_to(run_dir).as_posix()
                for path in _owned_files(run_dir, excluded_scope_roots)
                if path.is_file()
                and any(pattern.match(path.name) for pattern in candidate_name_patterns)
            }
        if ledger_artifacts != discovered_candidate_artifacts:
            findings.append(
                Finding(
                    "FREEZE_SEAL_ARTIFACT_SET_MISMATCH",
                    "ERROR",
                    f"Candidate dossier artifacts differ from the sealed ledger; missing={sorted(ledger_artifacts - discovered_candidate_artifacts)}, extra={sorted(discovered_candidate_artifacts - ledger_artifacts)}.",
                    ledger_path.name,
                )
            )

    problem_records = [r for r in ledger_records if r.get("record_type") == "problem"]
    problem_ids: list[str] = []
    for problem in problem_records:
        problem_id = problem.get("problem_id")
        if not isinstance(problem_id, str) or not problem_id.strip():
            findings.append(
                Finding("PROBLEM_ID_INVALID", "ERROR", "Problem record has no valid problem_id.", ledger_path.name, problem.get("_line"))
            )
            continue
        problem_id = problem_id.strip()
        problem_ids.append(problem_id)
        if mode == "archipelago_lite_shadow":
            creator_agent_id = problem.get("creator_agent_id")
            if not isinstance(creator_agent_id, str) or not creator_agent_id.strip():
                findings.append(
                    Finding(
                        "PROBLEM_CREATOR_MISSING",
                        "ERROR",
                        f"Problem card {problem_id} has no creator_agent_id.",
                        ledger_path.name,
                        problem.get("_line"),
                        (problem_id,),
                    )
                )
        problem_evidence_ids, problem_evidence_valid = _valid_string_list(
            problem.get("evidence_ids")
        )
        if not problem_evidence_valid:
            findings.append(
                Finding(
                    "PROBLEM_EVIDENCE_MISSING",
                    "ERROR" if mode == "archipelago_lite_shadow" and complete else "UNKNOWN",
                    f"Problem card {problem_id} must cite at least one typed evidence ID.",
                    ledger_path.name,
                    problem.get("_line"),
                    (problem_id,),
                )
            )
        else:
            unknown_problem_evidence = sorted(
                set(problem_evidence_ids) - set(evidence_by_id)
            )
            if unknown_problem_evidence:
                findings.append(
                    Finding(
                        "PROBLEM_EVIDENCE_UNKNOWN",
                        "ERROR",
                        f"Problem card {problem_id} cites unknown evidence {unknown_problem_evidence}.",
                        ledger_path.name,
                        problem.get("_line"),
                        (problem_id,),
                    )
                )
            for evidence_id in problem_evidence_ids:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    continue
                evidence_entities, evidence_entities_valid = _valid_string_list(
                    evidence.get("entity_ids")
                )
                if not evidence_entities_valid or problem_id not in evidence_entities:
                    findings.append(
                        Finding(
                            "PROBLEM_EVIDENCE_ENTITY_MISMATCH",
                            "ERROR",
                            f"Evidence {evidence_id} does not explicitly support problem card {problem_id}.",
                            ledger_path.name,
                            problem.get("_line"),
                            (problem_id, evidence_id),
                        )
                    )
                source_ids, source_ids_valid = _valid_string_list(
                    evidence.get("source_event_ids")
                )
                has_reciprocal_source = False
                if source_ids_valid:
                    for source_id in source_ids:
                        source_record = source_record_by_id.get(source_id)
                        if source_record is None:
                            continue
                        source_entities, source_entities_valid = _valid_string_list(
                            source_record.get("entity_ids")
                        )
                        source_evidence, source_evidence_valid = _valid_string_list(
                            source_record.get("evidence_ids")
                        )
                        if (
                            source_entities_valid
                            and source_evidence_valid
                            and problem_id in source_entities
                            and evidence_id in source_evidence
                        ):
                            has_reciprocal_source = True
                            break
                if not has_reciprocal_source:
                    findings.append(
                        Finding(
                            "PROBLEM_SOURCE_LINEAGE_MISSING",
                            "ERROR",
                            f"Problem card {problem_id} lacks a reciprocal source-open link for evidence {evidence_id}.",
                            ledger_path.name,
                            problem.get("_line"),
                            (problem_id, evidence_id),
                        )
                    )
    if len(problem_ids) != len(set(problem_ids)):
        findings.append(
            Finding("PROBLEM_ID_DUPLICATE", "ERROR", "Problem IDs must be globally unique.", ledger_path.name)
        )
    problem_set = set(problem_ids)

    level2_records = [r for r in ledger_records if r.get("record_type") == "level2"]
    level2_ids: list[str] = []
    level2_status_by_id: dict[str, str] = {}
    level2_completed_at_by_id: dict[str, datetime] = {}
    level2_artifact_paths: dict[str, str] = {}
    level2_artifact_hashes: dict[str, str] = {}
    for level2_record in level2_records:
        concept_id = level2_record.get("concept_id")
        if not isinstance(concept_id, str) or not concept_id.strip():
            findings.append(
                Finding("LEVEL2_ID_INVALID", "ERROR", "Level-2 record has no valid concept_id.", ledger_path.name, level2_record.get("_line"))
            )
            continue
        concept_id = concept_id.strip()
        level2_ids.append(concept_id)
        allowed_level2_ids = raw_set if mode == "archipelago_lite_shadow" else raw_set | direction_ids
        if concept_id not in allowed_level2_ids:
            findings.append(
                Finding("LEVEL2_ID_UNKNOWN", "ERROR", f"Level-2 record references unknown concept or direction {concept_id}.", ledger_path.name, level2_record.get("_line"), (concept_id,))
            )
        selected_at = check_run_time(
            level2_record.get("selected_at"),
            code="LEVEL2_SELECTION",
            label=f"Level-2 selection {concept_id}",
            artifact=ledger_path.name,
            line=level2_record.get("_line"),
            ids=(concept_id,),
        )
        development_status = level2_record.get("development_status")
        if isinstance(development_status, str):
            level2_status_by_id[concept_id] = development_status
        if development_status not in LEVEL2_DEVELOPMENT_STATUSES:
            findings.append(
                Finding(
                    "LEVEL2_DEVELOPMENT_STATUS_INVALID",
                    "ERROR",
                    f"Level-2 record {concept_id} must declare complete or an allowed early stop.",
                    ledger_path.name,
                    level2_record.get("_line"),
                    (concept_id,),
                )
            )
        if development_status == "early_stop" and level2_record.get("early_stop_code") not in LEVEL2_EARLY_STOP_CODES:
            findings.append(
                Finding(
                    "LEVEL2_EARLY_STOP_CODE_INVALID",
                    "ERROR",
                    f"Level-2 early stop {concept_id} lacks an allowed causal stop code.",
                    ledger_path.name,
                    level2_record.get("_line"),
                    (concept_id,),
                )
            )
        completed_at = check_run_time(
            level2_record.get("completed_at"),
            code="LEVEL2_COMPLETION",
            label=f"Level-2 dossier {concept_id}",
            artifact=ledger_path.name,
            line=level2_record.get("_line"),
            ids=(concept_id,),
        )
        if completed_at is not None:
            level2_completed_at_by_id[concept_id] = completed_at
        if (
            selected_at is not None
            and completed_at is not None
            and completed_at < selected_at
        ):
            findings.append(
                Finding(
                    "LEVEL2_COMPLETION_PRECEDES_SELECTION",
                    "ERROR",
                    f"Level-2 dossier {concept_id} completed before it was selected.",
                    ledger_path.name,
                    level2_record.get("_line"),
                    (concept_id,),
                )
            )
        if development_status == "complete":
            raw_level2_path = level2_record.get("artifact_path")
            unresolved_level2_path = (
                run_dir / raw_level2_path
                if isinstance(raw_level2_path, str)
                and not Path(raw_level2_path).is_absolute()
                else Path(raw_level2_path)
                if isinstance(raw_level2_path, str)
                else None
            )
            level2_path, level2_relative = _canonical_run_path(
                run_dir, raw_level2_path
            )
            level2_hash = level2_record.get("sha256")
            if level2_path is None or level2_relative is None:
                findings.append(
                    Finding("LEVEL2_ARTIFACT_PATH_INVALID", "ERROR", f"Level-2 dossier {concept_id} has no safe artifact path.", ledger_path.name, level2_record.get("_line"), (concept_id,))
                )
            elif not level2_path.is_file():
                findings.append(
                    Finding("LEVEL2_ARTIFACT_MISSING", "ERROR", f"Level-2 dossier {concept_id} is missing: {level2_relative}.", ledger_path.name, level2_record.get("_line"), (concept_id,))
                )
            elif unresolved_level2_path is not None and unresolved_level2_path.is_symlink():
                findings.append(
                    Finding("LEVEL2_ARTIFACT_SYMLINK", "ERROR", f"Level-2 dossier {concept_id} must be a regular non-symlink file.", level2_relative, node_ids=(concept_id,))
                )
            elif not isinstance(level2_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", level2_hash):
                findings.append(
                    Finding("LEVEL2_HASH_INVALID", "ERROR", f"Level-2 dossier {concept_id} lacks a valid SHA-256.", ledger_path.name, level2_record.get("_line"), (concept_id,))
                )
            elif _sha256(level2_path) != level2_hash:
                findings.append(
                    Finding("LEVEL2_HASH_MISMATCH", "ERROR", f"Level-2 dossier {concept_id} does not match its recorded hash.", level2_relative, node_ids=(concept_id,))
                )
            else:
                canonical_level2_path = str(level2_path.resolve())
                previous_path_id = level2_artifact_paths.get(canonical_level2_path)
                if previous_path_id is not None:
                    findings.append(
                        Finding("LEVEL2_ARTIFACT_PATH_DUPLICATE", "ERROR", f"Level-2 concepts {previous_path_id} and {concept_id} share one dossier path.", level2_relative, node_ids=(previous_path_id, concept_id))
                    )
                level2_artifact_paths[canonical_level2_path] = concept_id
                previous_hash_id = level2_artifact_hashes.get(level2_hash)
                if previous_hash_id is not None:
                    findings.append(
                        Finding("LEVEL2_CONTENT_DUPLICATE", "ERROR", f"Level-2 concepts {previous_hash_id} and {concept_id} have identical dossier content.", level2_relative, node_ids=(previous_hash_id, concept_id))
                    )
                level2_artifact_hashes[level2_hash] = concept_id
                try:
                    dossier_text = level2_path.read_text(encoding="utf-8")
                except (OSError, UnicodeError):
                    dossier_text = ""
                # The standardized deep-dossier schema is a V2 development
                # contract.  Legacy V1 evidence remains readable under its
                # frozen schema instead of being retroactively upgraded.
                section_issues = (
                    _level2_section_issues(dossier_text) if is_v2 else []
                )
                if (
                    not dossier_text.strip()
                    or concept_id not in dossier_text
                    or section_issues
                ):
                    findings.append(
                        Finding(
                            "LEVEL2_DOSSIER_SCHEMA_INVALID",
                            "ERROR",
                            f"Level-2 dossier {concept_id} must bind its concept ID and contain each standardized section once, in order, with a nonblank body; issues {section_issues}.",
                            level2_relative,
                            node_ids=(concept_id,),
                        )
                    )
                if any(
                    pattern.search(dossier_text)
                    for pattern in PROHIBITED_PACKET_PATTERNS
                ):
                    findings.append(
                        Finding(
                            "LEVEL2_PROHIBITED_CONTENT",
                            "ERROR",
                            f"Level-2 dossier {concept_id} contains prohibited validator, score, threshold, or evaluator material.",
                            level2_relative,
                            node_ids=(concept_id,),
                        )
                    )
        elif development_status == "early_stop" and level2_record.get("artifact_path") is not None:
            findings.append(
                Finding("LEVEL2_EARLY_STOP_ARTIFACT_UNEXPECTED", "WARNING", f"Level-2 early stop {concept_id} also declares a dossier artifact; verify the stop was not retrofitted.", ledger_path.name, level2_record.get("_line"), (concept_id,))
            )
    if len(level2_ids) != len(set(level2_ids)):
        findings.append(
            Finding("LEVEL2_ID_DUPLICATE", "ERROR", "Level-2 concept IDs must be unique.", ledger_path.name)
        )
    level2_set = set(level2_ids)
    if (mode == "archipelago_lite_shadow" or matched_pilot) and not is_v2:
        for finalist in finalist_records:
            finalist_id = finalist.get("finalist_id")
            finalist_raw_ids, finalist_raw_ids_valid = _valid_string_list(
                finalist.get("raw_ids")
            )
            level2_ancestors = (
                set(finalist_raw_ids) & level2_set
                if finalist_raw_ids_valid
                else set()
            )
            finalist_direction_id = finalist.get("direction_id")
            if (
                isinstance(finalist_direction_id, str)
                and finalist_direction_id in level2_set
            ):
                level2_ancestors.add(finalist_direction_id)
            if not level2_ancestors or any(
                level2_status_by_id.get(concept_id) != "complete"
                for concept_id in level2_ancestors
            ):
                findings.append(
                    Finding(
                        "FINALIST_LEVEL2_NOT_COMPLETE",
                        "ERROR",
                        f"Non-routing finalist {finalist_id!r} must descend from a completed Level-2 dossier.",
                        ledger_path.name,
                        finalist.get("_line"),
                        (str(finalist_id),),
                    )
                )

    if (
        complete
        and is_v2
        and mode == "audited_funnel"
        and run_record.get("cohort_kind") == "initial"
        and profile_name in {"operational_live_with_shadow", "v2_matched_nonrouting"}
    ):
        exact_counts = {
            "raw": (len(raw_ids), 48),
            "level2": (len(level2_set), 12),
            "finalists": (len(finalist_records), 6),
        }
        for label, (observed, required) in exact_counts.items():
            if observed != required:
                findings.append(Finding("MATCHED_INITIAL_COUNT_MISMATCH", "ERROR", f"Matched initial scope requires exactly {required} {label}; found {observed}."))
        if not 12 <= len(direction_ids) <= 20:
            findings.append(Finding("MATCHED_INITIAL_DIRECTION_COUNT", "ERROR", f"Matched initial scope requires 12–20 researched directions; found {len(direction_ids)}."))

    if complete and mode == "audited_funnel":
        if is_v2 and run_record.get("cohort_kind") == "regeneration":
            observed_wave_indices: set[int] = set()
            if len(finalist_records) != 6:
                findings.append(
                    Finding(
                        "REGENERATION_FINALIST_COUNT_MISMATCH",
                        "ERROR",
                        f"A regeneration wave must register and seal exactly 6 finalists; found {len(finalist_records)}.",
                        ledger_path.name,
                    )
                )
            for finalist in finalist_records:
                if finalist.get("arm") != run_record.get("arm"):
                    findings.append(
                        Finding(
                            "REGENERATION_FINALIST_ARM_INVALID",
                            "ERROR",
                            f"Regeneration finalist {finalist.get('finalist_id')} must use the run's exact arm.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                artifact_name = Path(str(finalist.get("artifact_path", ""))).name
                wave_match = re.fullmatch(
                    r"wave([1-9][0-9]*)_candidate_.+\.md",
                    artifact_name,
                )
                if wave_match is None:
                    findings.append(
                        Finding(
                            "REGENERATION_FINALIST_FILENAME_INVALID",
                            "ERROR",
                            f"Regeneration finalist {finalist.get('finalist_id')} must use wave{{wave_index}}_candidate_*.md in its owned child scope.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                else:
                    observed_wave_indices.add(int(wave_match.group(1)))
            if len(observed_wave_indices) != 1:
                findings.append(
                    Finding(
                        "REGENERATION_FINALIST_NAMESPACE_MISMATCH",
                        "ERROR",
                        "All regeneration finalists must share one explicit wave-specific candidate namespace.",
                        ledger_path.name,
                    )
                )
            declared_wave_index = run_record.get("wave_index")
            if declared_wave_index is not None and (
                not isinstance(declared_wave_index, int)
                or isinstance(declared_wave_index, bool)
                or declared_wave_index not in observed_wave_indices
            ):
                findings.append(
                    Finding(
                        "REGENERATION_WAVE_INDEX_INVALID",
                        "ERROR",
                        "When present, wave_index must exactly match the finalist namespace.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
        elif matched_pilot:
            expected = {
                "raw": (len(raw_ids), 48),
                "level2": (len(level2_set), 12),
                "finalists": (len(finalist_records), 6),
            }
            for label, (observed, required) in expected.items():
                if observed != required:
                    findings.append(
                        Finding(
                            "MATCHED_BASELINE_COUNT_MISMATCH",
                            "ERROR",
                            f"Expected {required} {label}; found {observed}.",
                        )
                    )
            if not 12 <= len(direction_ids) <= 20:
                findings.append(
                    Finding(
                        "MATCHED_BASELINE_DIRECTION_COUNT",
                        "ERROR",
                        f"Expected 12–20 directions before selecting 12 Level-2 dossiers; found {len(direction_ids)}.",
                    )
                )
            if run_record.get("validation_eligible") is not False:
                findings.append(
                    Finding(
                        "MATCHED_BASELINE_ROUTING_NOT_DISABLED",
                        "ERROR",
                        "Matched baseline diagnostic must set validation_eligible to false.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            if run_record.get("shadow_only") is not True:
                findings.append(
                    Finding(
                        "MATCHED_BASELINE_SHADOW_TAG_MISSING",
                        "ERROR",
                        "Matched baseline diagnostic must set shadow_only to true.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            for finalist in finalist_records:
                if finalist.get("validation_eligible") is not False:
                    findings.append(
                        Finding(
                            "MATCHED_BASELINE_FINALIST_ELIGIBLE",
                            "ERROR",
                            f"Matched baseline finalist {finalist.get('finalist_id')} is validation-eligible.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                if finalist.get("arm") != "matched_baseline":
                    findings.append(
                        Finding(
                            "MATCHED_BASELINE_FINALIST_ARM_INVALID",
                            "ERROR",
                            f"Matched baseline finalist {finalist.get('finalist_id')} must use arm matched_baseline.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                if finalist.get("shadow_only") is not True:
                    findings.append(
                        Finding(
                            "MATCHED_BASELINE_FINALIST_SHADOW_TAG_MISSING",
                            "ERROR",
                            f"Matched baseline finalist {finalist.get('finalist_id')} must set shadow_only to true.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                artifact_name = Path(str(finalist.get("artifact_path", ""))).name
                if not artifact_name.startswith("baseline_shadow_finalist_") or not artifact_name.endswith(".md"):
                    findings.append(
                        Finding(
                            "MATCHED_BASELINE_FINALIST_FILENAME_INVALID",
                            "ERROR",
                            f"Matched baseline finalist {finalist.get('finalist_id')} must use baseline_shadow_finalist_*.md.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
        else:
            if not 40 <= len(raw_ids) <= 60:
                findings.append(
                    Finding("LIVE_RAW_COUNT", "ERROR", f"Expected 40–60 raw IDs; found {len(raw_ids)}.")
                )
            if not 10 <= len(direction_ids) <= 20:
                findings.append(
                    Finding(
                        "LIVE_DIRECTION_COUNT",
                        "ERROR",
                        f"Expected 10–20 directions; found {len(direction_ids)}.",
                    )
                )
            if not 3 <= len(finalist_records) <= 6:
                findings.append(
                    Finding(
                        "LIVE_FINALIST_COUNT",
                        "ERROR",
                        f"Expected 3–6 finalists; found {len(finalist_records)}.",
                    )
                )
            for finalist in finalist_records:
                if finalist.get("arm") != "live":
                    findings.append(
                        Finding(
                            "LIVE_FINALIST_ARM_INVALID",
                            "ERROR",
                            f"Live finalist {finalist.get('finalist_id')} must use arm live.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                if finalist.get("validation_eligible") is not True:
                    findings.append(
                        Finding(
                            "LIVE_FINALIST_ELIGIBILITY_INVALID",
                            "ERROR",
                            f"Live finalist {finalist.get('finalist_id')} must explicitly remain eligible for the unchanged downstream route.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
                artifact_name = Path(str(finalist.get("artifact_path", ""))).name
                if not artifact_name.startswith("finalist_") or not artifact_name.endswith(".md"):
                    findings.append(
                        Finding(
                            "LIVE_FINALIST_FILENAME_INVALID",
                            "ERROR",
                            f"Live finalist {finalist.get('finalist_id')} must use finalist_*.md.",
                            ledger_path.name,
                            finalist.get("_line"),
                        )
                    )
    elif complete and mode == "archipelago_lite_shadow":
        concept_types = Counter(
            r.get("concept_type")
            for r in mappings
            if isinstance(r.get("concept_type"), str)
        )
        expected = {
            "raw": (len(raw_ids), 48),
            "problems": (len(problem_set), 36),
            "direct": (concept_types.get("direct", 0), 36),
            "inversion": (concept_types.get("inversion", 0), 6),
            "recombination": (concept_types.get("recombination", 0), 6),
            "level2": (len(level2_set), 12),
            "finalists": (len(finalist_records), 6),
        }
        for label, (observed, required) in expected.items():
            if observed != required:
                findings.append(
                    Finding(
                        "SHADOW_COUNT_MISMATCH",
                        "ERROR",
                        f"Expected {required} {label}; found {observed}.",
                    )
                )
        island_values: list[str] = []
        for problem in problem_records:
            island = problem.get("source_island")
            if not isinstance(island, str) or island not in SHADOW_ISLAND_ROLES:
                findings.append(
                    Finding("SHADOW_SOURCE_ISLAND_INVALID", "ERROR", "Every problem card must use one exact approved evidence-island ID.", ledger_path.name, problem.get("_line"))
                )
            else:
                island_values.append(island)
        island_counts = Counter(island_values)
        expected_problem_ids = {
            f"P-{island}-{index:02d}"
            for island in SHADOW_ISLAND_ROLES
            for index in range(1, 7)
        }
        if island_counts != Counter({island: 6 for island in SHADOW_ISLAND_ROLES}):
            findings.append(
                Finding(
                    "SHADOW_ISLAND_COUNT_MISMATCH",
                    "ERROR",
                    f"Expected six islands with six problem cards each; found {dict(island_counts)}.",
                )
            )
        if problem_set != expected_problem_ids:
            findings.append(
                Finding(
                    "SHADOW_PROBLEM_ID_SET_MISMATCH",
                    "ERROR",
                    f"Problem IDs must be exactly P-<island>-01..06; missing={sorted(expected_problem_ids - problem_set)}, extra={sorted(problem_set - expected_problem_ids)}.",
                    ledger_path.name,
                )
            )
        for finalist in finalist_records:
            finalist_raw_ids, valid_finalist_raw_ids = _valid_string_list(finalist.get("raw_ids"))
            if not valid_finalist_raw_ids or len(finalist_raw_ids) != 1:
                findings.append(
                    Finding(
                        "SHADOW_FINALIST_ANCESTRY_COUNT_INVALID",
                        "ERROR",
                        f"Finalist {finalist.get('finalist_id')} must bind to exactly one Level-2 concept.",
                        ledger_path.name,
                        finalist.get("_line"),
                    )
                )
            if finalist.get("arm") != "shadow":
                findings.append(
                    Finding(
                        "SHADOW_FINALIST_ARM_INVALID",
                        "ERROR",
                        f"Finalist {finalist.get('finalist_id')} is not marked shadow.",
                        ledger_path.name,
                        finalist.get("_line"),
                    )
                )
            if finalist.get("shadow_only") is not True:
                findings.append(
                    Finding(
                        "SHADOW_FINALIST_TAG_MISSING",
                        "ERROR",
                        f"Finalist {finalist.get('finalist_id')} must set shadow_only to true.",
                        ledger_path.name,
                        finalist.get("_line"),
                    )
                )
            artifact_name = Path(str(finalist.get("artifact_path", ""))).name
            if (
                not (is_v2 and run_record.get("cohort_kind") == "regeneration")
                and (
                    not artifact_name.startswith("shadow_finalist_")
                    or not artifact_name.endswith(".md")
                )
            ):
                findings.append(
                    Finding(
                        "SHADOW_FINALIST_FILENAME_INVALID",
                        "ERROR",
                        f"Finalist {finalist.get('finalist_id')} must use shadow_finalist_*.md.",
                        ledger_path.name,
                        finalist.get("_line"),
                    )
                )
            if not valid_finalist_raw_ids or not set(finalist_raw_ids) & level2_set:
                findings.append(
                    Finding(
                        "SHADOW_FINALIST_NOT_LEVEL2",
                        "ERROR",
                        f"Finalist {finalist.get('finalist_id')} has no Level-2 ancestor.",
                        ledger_path.name,
                        finalist.get("_line"),
                    )
                )
        problem_island_by_id = {
            problem.get("problem_id"): problem.get("source_island")
            for problem in problem_records
            if isinstance(problem.get("problem_id"), str)
            and problem.get("source_island") in SHADOW_ISLAND_ROLES
        }
        direct_problem_by_id: dict[str, str] = {}
        for item in mappings:
            if item.get("concept_type") != "direct" or not isinstance(item.get("raw_id"), str):
                continue
            item_parents, item_parents_valid = _valid_string_list(item.get("parent_ids"))
            if item_parents_valid and len(item_parents) == 1 and item_parents[0] in problem_set:
                direct_problem_by_id[item["raw_id"]] = item_parents[0]

        for mapping in mappings:
            concept_type = mapping.get("concept_type")
            parent_ids = mapping.get("parent_ids")
            if not isinstance(concept_type, str) or concept_type not in {"direct", "inversion", "recombination"}:
                findings.append(
                    Finding(
                        "SHADOW_CONCEPT_TYPE_INVALID",
                        "ERROR",
                        f"Raw concept {mapping.get('raw_id')} has invalid concept_type {concept_type!r}.",
                        ledger_path.name,
                        mapping.get("_line"),
                    )
                )
            else:
                typed_parent_ids, parents_valid = _valid_string_list(parent_ids)
                direct_ids = {
                    item.get("raw_id")
                    for item in mappings
                    if item.get("concept_type") == "direct" and isinstance(item.get("raw_id"), str)
                }
                known_parent_ids = raw_set | problem_set
                if not parents_valid or any(parent not in known_parent_ids for parent in typed_parent_ids):
                    findings.append(
                        Finding(
                            "SHADOW_CONCEPT_PARENT_INVALID",
                            "ERROR",
                            f"Raw concept {mapping.get('raw_id')} has invalid or unknown parent IDs.",
                            ledger_path.name,
                            mapping.get("_line"),
                        )
                    )
                elif concept_type == "direct" and (
                    len(typed_parent_ids) != 1 or typed_parent_ids[0] not in problem_set
                ):
                    findings.append(
                        Finding("SHADOW_DIRECT_PARENT_INVALID", "ERROR", f"Direct concept {mapping.get('raw_id')} must have exactly one problem-card parent.", ledger_path.name, mapping.get("_line"))
                    )
                elif concept_type == "inversion":
                    if not typed_parent_ids or any(parent not in direct_ids for parent in typed_parent_ids):
                        findings.append(
                            Finding("SHADOW_INVERSION_PARENT_INVALID", "ERROR", f"Inversion {mapping.get('raw_id')} must transform direct concepts only.", ledger_path.name, mapping.get("_line"))
                        )
                    operation = mapping.get("operation")
                    required_operation_fields = ("assumption", "causal_benefit", "new_risk")
                    if (
                        not isinstance(operation, dict)
                        or operation.get("dimension") not in INVERSION_DIMENSIONS
                        or any(not isinstance(operation.get(field), str) or not operation.get(field).strip() for field in required_operation_fields)
                    ):
                        findings.append(
                            Finding("SHADOW_INVERSION_OPERATION_INVALID", "ERROR", f"Inversion {mapping.get('raw_id')} lacks a typed assumption inversion, causal benefit, or new risk.", ledger_path.name, mapping.get("_line"))
                        )
                elif concept_type == "recombination":
                    if len(set(typed_parent_ids)) < 2:
                        findings.append(
                            Finding("SHADOW_RECOMBINATION_PARENT_INVALID", "ERROR", f"Recombination {mapping.get('raw_id')} must name at least two distinct parents.", ledger_path.name, mapping.get("_line"))
                        )
                    parent_islands: set[str] = set()
                    for parent in typed_parent_ids:
                        problem_parent = parent if parent in problem_island_by_id else direct_problem_by_id.get(parent)
                        island = problem_island_by_id.get(problem_parent) if problem_parent is not None else None
                        if isinstance(island, str):
                            parent_islands.add(island)
                    if len(parent_islands) < 2:
                        findings.append(
                            Finding("SHADOW_RECOMBINATION_ISLANDS_INVALID", "ERROR", f"Recombination {mapping.get('raw_id')} must transfer across at least two distinct evidence islands.", ledger_path.name, mapping.get("_line"))
                        )
                    operation = mapping.get("operation")
                    if (
                        not isinstance(operation, dict)
                        or not isinstance(operation.get("transferred_mechanism"), str)
                        or not operation.get("transferred_mechanism").strip()
                        or not isinstance(operation.get("analogy_break"), str)
                        or not operation.get("analogy_break").strip()
                    ):
                        findings.append(
                            Finding("SHADOW_RECOMBINATION_OPERATION_INVALID", "ERROR", f"Recombination {mapping.get('raw_id')} lacks a transferred mechanism or analogy-break risk.", ledger_path.name, mapping.get("_line"))
                        )
            if not isinstance(parent_ids, list) or not parent_ids:
                findings.append(
                    Finding(
                        "SHADOW_CONCEPT_PARENT_MISSING",
                        "ERROR",
                        f"Raw concept {mapping.get('raw_id')} has no parent IDs.",
                        ledger_path.name,
                        mapping.get("_line"),
                    )
                    )
        category_counts = Counter()
        allowed_categories = {
            "main_provisional",
            "selector_or_challenger",
            "rejected",
            "near_cutoff",
            "singleton",
        }
        for level2_record in level2_records:
            category = level2_record.get("selection_category")
            if not isinstance(category, str) or category not in allowed_categories:
                findings.append(
                    Finding(
                        "SHADOW_LEVEL2_CATEGORY_INVALID",
                        "ERROR",
                        f"Level-2 concept {level2_record.get('concept_id')} has invalid selection_category {category!r}.",
                        ledger_path.name,
                        level2_record.get("_line"),
                    )
                )
            else:
                category_counts[category] += 1
        required_categories = {
            "main_provisional": 6,
            "selector_or_challenger": 3,
            "rejected": 1,
            "near_cutoff": 1,
            "singleton": 1,
        }
        if category_counts != Counter(required_categories):
            findings.append(
                Finding(
                    "SHADOW_LEVEL2_CATEGORY_COUNTS",
                    "ERROR",
                    f"Expected Level-2 categories {required_categories}; found {dict(category_counts)}.",
                    ledger_path.name,
                )
            )
        if run_record.get("shadow_can_route_to_validation") is not False:
            findings.append(
                Finding(
                    "SHADOW_ROUTING_NOT_DISABLED",
                    "ERROR",
                    "Shadow run must set shadow_can_route_to_validation to false.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        if run_record.get("shadow_only") is not True:
            findings.append(
                Finding(
                    "SHADOW_RUN_TAG_MISSING",
                    "ERROR",
                    "Shadow run must set shadow_only to true.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        if run_record.get("validation_eligible") is not False:
            findings.append(
                Finding(
                    "SHADOW_RUN_ELIGIBILITY_INVALID",
                    "ERROR",
                    "Shadow run must set validation_eligible to false.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )

    agent_records = [r for r in manifest_records if r.get("record_type") == "agent"]
    if complete and not agent_records:
        findings.append(
            Finding("AGENT_PROVENANCE_MISSING", "ERROR", "A completed run must contain agent provenance records.", manifest_path.name)
        )
    agent_by_id: dict[str, dict[str, Any]] = {}
    agent_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    for agent in agent_records:
        line = agent.get("_line")
        raw_agent_id = agent.get("agent_id")
        if not isinstance(raw_agent_id, str) or not raw_agent_id.strip():
            findings.append(
                Finding("AGENT_ID_INVALID", "ERROR", "Agent record has no valid agent_id.", manifest_path.name, line)
            )
            continue
        agent_id = raw_agent_id.strip()
        if agent_id in agent_by_id:
            findings.append(
                Finding("AGENT_ID_DUPLICATE", "ERROR", f"Agent ID {agent_id} is duplicated.", manifest_path.name, line, (agent_id,))
            )
        else:
            agent_by_id[agent_id] = agent

        stage = agent.get("stage")
        arm = agent.get("arm")
        role = agent.get("role")
        if not isinstance(stage, str) or stage not in KNOWN_STAGES:
            findings.append(
                Finding("AGENT_STAGE_INVALID", "ERROR", f"Agent {agent_id} has unsupported stage {stage!r}.", manifest_path.name, line, (agent_id,))
            )
        if not isinstance(arm, str) or arm not in KNOWN_ARMS:
            findings.append(
                Finding("AGENT_ARM_INVALID", "ERROR", f"Agent {agent_id} has unsupported arm {arm!r}.", manifest_path.name, line, (agent_id,))
            )
        if not isinstance(role, str) or not role.strip():
            findings.append(
                Finding("AGENT_ROLE_INVALID", "ERROR", f"Agent {agent_id} must declare a role.", manifest_path.name, line, (agent_id,))
            )
        if isinstance(stage, str) and (stage in PROVENANCE_STAGES or stage == "generation"):
            assigned_ids, assigned_valid = _valid_string_list(agent.get("assigned_ids"))
            output_ids, outputs_valid = _valid_string_list(agent.get("output_ids"))
            if not assigned_valid:
                findings.append(
                    Finding("AGENT_ASSIGNMENT_IDS_INVALID", "ERROR", f"Creative agent {agent_id} must declare non-empty assigned_ids.", manifest_path.name, line, (agent_id,))
                )
            if not outputs_valid:
                findings.append(
                    Finding("AGENT_OUTPUT_IDS_INVALID", "ERROR", f"Creative agent {agent_id} must declare non-empty output_ids.", manifest_path.name, line, (agent_id,))
                )
        if isinstance(stage, str) and stage in ISOLATED_STAGES and agent.get("fork_turns") != "none":
            findings.append(
                Finding("FORBIDDEN_CONTEXT_FORK", "ERROR", f"Agent {agent_id} at stage {stage} must use fork_turns=none.", manifest_path.name, line, (agent_id,))
            )

        started_at = check_run_time(agent.get("started_at"), code="AGENT_START", label=f"Agent {agent_id} start", artifact=manifest_path.name, line=line, ids=(agent_id,))
        ended_at = check_run_time(agent.get("ended_at"), code="AGENT_END", label=f"Agent {agent_id} end", artifact=manifest_path.name, line=line, ids=(agent_id,))
        if started_at is not None and ended_at is not None and ended_at < started_at:
            findings.append(
                Finding("AGENT_TIME_ORDER_INVALID", "ERROR", f"Agent {agent_id} ends before it starts.", manifest_path.name, line, (agent_id,))
            )
        agent_times[agent_id] = (started_at, ended_at)

        if matched_pilot and mode == "audited_funnel" and arm != "matched_baseline":
            findings.append(
                Finding(
                    "MATCHED_BASELINE_AGENT_ARM_INVALID",
                    "ERROR",
                    f"Matched baseline agent {agent_id} must use arm matched_baseline.",
                    manifest_path.name,
                    line,
                    (agent_id,),
                )
            )
        if not matched_pilot and mode == "audited_funnel" and arm != "live":
            findings.append(
                Finding(
                    "LIVE_AGENT_ARM_INVALID",
                    "ERROR",
                    f"Live agent {agent_id} must use arm live.",
                    manifest_path.name,
                    line,
                    (agent_id,),
                )
            )

        context_classes, context_classes_valid = _valid_string_list(agent.get("context_classes"), allow_empty=True)
        if not context_classes_valid:
            findings.append(
                Finding("CONTEXT_CLASSES_UNKNOWN", "UNKNOWN", f"Agent {agent_id} lacks a typed context_classes inventory.", manifest_path.name, line, (agent_id,))
            )
            context_classes = []
        denied_classes = set(context_classes) & FORBIDDEN_CONTEXT_CLASSES
        if isinstance(stage, str) and stage in CREATIVE_OR_SELECTOR_STAGES and "history" in context_classes:
            denied_classes.add("history")
        if denied_classes:
            findings.append(
                Finding("FORBIDDEN_CONTEXT_CLASS", "ERROR", f"Agent {agent_id} received forbidden context classes: {sorted(denied_classes)}.", manifest_path.name, line, (agent_id,))
            )

        allowlisted, allowlisted_valid = _valid_string_list(agent.get("allowlisted_files"), allow_empty=True)
        files_read, files_read_valid = _valid_string_list(agent.get("files_read"), allow_empty=True)
        if not allowlisted_valid or not files_read_valid:
            findings.append(
                Finding("CONTEXT_READ_LOG_UNKNOWN", "UNKNOWN", f"Agent {agent_id} lacks typed allowlisted_files or files_read.", manifest_path.name, line, (agent_id,))
            )
            allowlisted = allowlisted if allowlisted_valid else []
            files_read = files_read if files_read_valid else []

        allowlisted_paths: set[str] = set()
        for value in allowlisted:
            _path, relative = _canonical_run_path(run_dir, value)
            if relative is None:
                findings.append(
                    Finding("CONTEXT_ALLOWLIST_PATH_INVALID", "ERROR", f"Agent {agent_id} allowlist path escapes the run folder: {value!r}.", manifest_path.name, line, (agent_id,))
                )
            else:
                allowlisted_paths.add(relative)
        read_paths: dict[str, Path] = {}
        for value in files_read:
            path, relative = _canonical_run_path(run_dir, value)
            if path is None or relative is None:
                findings.append(
                    Finding("CONTEXT_READ_PATH_INVALID", "ERROR", f"Agent {agent_id} read path escapes the run folder: {value!r}.", manifest_path.name, line, (agent_id,))
                )
            else:
                read_paths[relative] = path

        context_files = agent.get("context_files")
        hashed_paths: dict[str, Path] = {}
        if not isinstance(context_files, list) or not context_files:
            findings.append(
                Finding("CONTEXT_PACKET_UNKNOWN", "UNKNOWN", f"Agent {agent_id} has no hashed context packet inventory.", manifest_path.name, line, (agent_id,))
            )
        else:
            for item in context_files:
                if not isinstance(item, dict):
                    findings.append(
                        Finding("CONTEXT_PACKET_INVALID", "ERROR", f"Agent {agent_id} has an invalid context_files entry.", manifest_path.name, line, (agent_id,))
                    )
                    continue
                context_path, relative = _canonical_run_path(run_dir, item.get("path"))
                if context_path is None or relative is None:
                    findings.append(
                        Finding("CONTEXT_PACKET_PATH_ESCAPE", "ERROR", f"Agent {agent_id} context path is outside the run folder.", manifest_path.name, line, (agent_id,))
                    )
                    continue
                if relative in hashed_paths:
                    findings.append(
                        Finding("CONTEXT_PACKET_PATH_DUPLICATE", "ERROR", f"Agent {agent_id} declares context path {relative} more than once.", manifest_path.name, line, (agent_id,))
                    )
                hashed_paths[relative] = context_path
                if not context_path.is_file():
                    findings.append(
                        Finding("CONTEXT_PACKET_MISSING", "ERROR", f"Agent {agent_id} context packet does not exist: {relative}.", manifest_path.name, line, (agent_id,))
                    )
                elif item.get("sha256") != _sha256(context_path):
                    findings.append(
                        Finding("CONTEXT_PACKET_HASH_MISMATCH", "ERROR", f"Agent {agent_id} context packet hash does not match: {relative}.", manifest_path.name, line, (agent_id,))
                    )

        for relative, path in sorted(read_paths.items()):
            if relative not in allowlisted_paths:
                findings.append(
                    Finding("CONTEXT_FILE_NOT_ALLOWLISTED", "ERROR", f"Agent {agent_id} read non-allowlisted path {relative}.", manifest_path.name, line, (agent_id,))
                )
            if relative not in hashed_paths:
                findings.append(
                    Finding("CONTEXT_READ_NOT_HASHED", "ERROR", f"Agent {agent_id} read path {relative} without a matching hashed context_files entry.", manifest_path.name, line, (agent_id,))
                )
        for relative, path in sorted(hashed_paths.items()):
            if relative not in allowlisted_paths:
                findings.append(
                    Finding(
                        "CONTEXT_PACKET_NOT_ALLOWLISTED",
                        "ERROR",
                        f"Agent {agent_id} received non-allowlisted context packet {relative}.",
                        manifest_path.name,
                        line,
                        (agent_id,),
                    )
                )
            if isinstance(stage, str) and stage in CREATIVE_OR_SELECTOR_STAGES:
                lowered = relative.casefold()
                if any(marker in lowered for marker in PROHIBITED_CONTEXT_MARKERS):
                    findings.append(
                        Finding("FORBIDDEN_CONTEXT_FILE", "ERROR", f"Agent {agent_id} received prohibited context {relative}.", manifest_path.name, line, (agent_id,))
                    )
                if not path.is_file():
                    findings.append(
                        Finding("CONTEXT_PACKET_MISSING", "ERROR", f"Agent {agent_id} received missing context packet {relative}.", manifest_path.name, line, (agent_id,))
                    )
                else:
                    try:
                        packet_text = path.read_text(encoding="utf-8-sig")
                    except (OSError, UnicodeError):
                        findings.append(
                            Finding("CONTEXT_PACKET_CONTENT_UNKNOWN", "UNKNOWN", f"Agent {agent_id} context content is unreadable: {relative}.", relative, node_ids=(agent_id,))
                        )
                    else:
                        if any(pattern.search(packet_text) for pattern in PROHIBITED_PACKET_PATTERNS):
                            findings.append(
                                Finding("FORBIDDEN_CONTEXT_CONTENT", "ERROR", f"Agent {agent_id} packet contains prohibited validator, score, objection, or rejection material.", relative, node_ids=(agent_id,))
                            )

        resources_record = agent.get("resources")
        if not isinstance(resources_record, dict):
            findings.append(
                Finding("AGENT_RESOURCE_TELEMETRY_UNKNOWN", "UNKNOWN", f"Agent {agent_id} lacks a resources object.", manifest_path.name, line, (agent_id,))
            )
        else:
            agent_resource_keys = (
                V2_AGENT_RESOURCE_KEYS if is_v2 else REQUIRED_AGENT_RESOURCE_KEYS
            )
            for key in agent_resource_keys:
                value = resources_record.get(key)
                if value is None:
                    findings.append(
                        Finding("AGENT_RESOURCE_MISSING", "UNKNOWN", f"Agent {agent_id} lacks resource field {key}.", manifest_path.name, line, (agent_id,))
                    )
                elif not _is_nonnegative_number(value):
                    findings.append(
                        Finding("AGENT_RESOURCE_INVALID", "ERROR", f"Agent {agent_id} resource {key} must be finite and nonnegative.", manifest_path.name, line, (agent_id,))
                    )
            reported_elapsed = resources_record.get(
                "elapsed_microseconds" if is_v2 else "elapsed_minutes"
            )
            if (
                started_at is not None
                and ended_at is not None
                and ended_at >= started_at
                and _is_nonnegative_number(reported_elapsed)
            ):
                observed_elapsed = (
                    _elapsed_microseconds(started_at, ended_at)
                    if is_v2
                    else (ended_at - started_at).total_seconds() / 60.0
                )
                elapsed_matches = (
                    isinstance(reported_elapsed, int)
                    and not isinstance(reported_elapsed, bool)
                    and reported_elapsed == observed_elapsed
                    if is_v2
                    else math.isclose(
                        float(reported_elapsed),
                        float(observed_elapsed),
                        rel_tol=0.0,
                        abs_tol=1e-6,
                    )
                )
                if not elapsed_matches:
                    findings.append(
                        Finding(
                            "AGENT_ELAPSED_MISMATCH",
                            "ERROR",
                            f"Agent {agent_id} reports {reported_elapsed} elapsed units; timestamps show {observed_elapsed}.",
                            manifest_path.name,
                            line,
                            (agent_id,),
                        )
                    )

    if complete and mode == "archipelago_lite_shadow":
        problem_creator: dict[str, str] = {
            record.get("problem_id"): record.get("creator_agent_id")
            for record in problem_records
            if isinstance(record.get("problem_id"), str)
            and isinstance(record.get("creator_agent_id"), str)
        }
        concept_creator: dict[str, str] = {
            record.get("raw_id"): record.get("creator_agent_id")
            for record in mappings
            if isinstance(record.get("raw_id"), str)
            and isinstance(record.get("creator_agent_id"), str)
        }
        creative_agents = [
            agent
            for agent in agent_records
            if agent.get("stage") in PROVENANCE_STAGES
        ]
        all_reported_outputs: list[str] = []
        direct_parent_multiset: list[str] = []
        for agent in creative_agents:
            agent_id = str(agent.get("agent_id"))
            stage = agent.get("stage")
            assigned_ids, assigned_valid = _valid_string_list(agent.get("assigned_ids"))
            output_ids, outputs_valid = _valid_string_list(agent.get("output_ids"))
            if not assigned_valid or not outputs_valid:
                continue
            all_reported_outputs.extend(output_ids)
            ledger_outputs = {
                entity_id
                for entity_id, creator in (
                    problem_creator.items() if stage == "problem_discovery" else concept_creator.items()
                )
                if creator == agent_id
            }
            if set(output_ids) != ledger_outputs:
                findings.append(
                    Finding("AGENT_OUTPUT_LEDGER_MISMATCH", "ERROR", f"Creative agent {agent_id} output_ids do not equal its ledger-created entities.", manifest_path.name, agent.get("_line"), (agent_id,))
                )
            if stage == "problem_discovery":
                island_id = agent.get("island_id")
                if island_id not in SHADOW_ISLAND_ROLES or agent.get("role") != SHADOW_ISLAND_ROLES.get(island_id):
                    findings.append(
                        Finding("SHADOW_SCOUT_ISLAND_ROLE_INVALID", "ERROR", f"Scout {agent_id} must bind one exact island ID to its exact role.", manifest_path.name, agent.get("_line"), (agent_id,))
                    )
                    continue
                expected_ids = {f"P-{island_id}-{index:02d}" for index in range(1, 7)}
                if set(assigned_ids) != expected_ids or set(output_ids) != expected_ids:
                    findings.append(
                        Finding("SHADOW_SCOUT_OUTPUT_SET_INVALID", "ERROR", f"Scout {agent_id} must be assigned and output exactly six cards from island {island_id}.", manifest_path.name, agent.get("_line"), (agent_id,))
                    )
            elif stage == "direct_concept":
                if len(assigned_ids) != 12 or len(output_ids) != 12:
                    findings.append(
                        Finding("SHADOW_DIRECT_BUILDER_COUNT_INVALID", "ERROR", f"Direct builder {agent_id} must receive 12 problems and output 12 concepts.", manifest_path.name, agent.get("_line"), (agent_id,))
                    )
                for output_id in output_ids:
                    mapping = next((item for item in mappings if item.get("raw_id") == output_id), None)
                    parents, parents_valid = _valid_string_list(mapping.get("parent_ids")) if isinstance(mapping, dict) else ([], False)
                    if mapping is None or mapping.get("concept_type") != "direct" or not parents_valid or len(parents) != 1 or parents[0] not in assigned_ids:
                        findings.append(
                            Finding("SHADOW_DIRECT_ASSIGNMENT_MISMATCH", "ERROR", f"Direct builder {agent_id} output {output_id} does not consume exactly one assigned problem.", manifest_path.name, agent.get("_line"), (agent_id, output_id))
                        )
                    else:
                        direct_parent_multiset.append(parents[0])
            elif stage in {"inversion", "recombination"}:
                if len(output_ids) != 3:
                    findings.append(
                        Finding("SHADOW_TRANSFORMER_OUTPUT_COUNT_INVALID", "ERROR", f"Transformer {agent_id} must output exactly three concepts.", manifest_path.name, agent.get("_line"), (agent_id,))
                    )
                for output_id in output_ids:
                    mapping = next((item for item in mappings if item.get("raw_id") == output_id), None)
                    parents, parents_valid = _valid_string_list(mapping.get("parent_ids")) if isinstance(mapping, dict) else ([], False)
                    expected_type = "inversion" if stage == "inversion" else "recombination"
                    if mapping is None or mapping.get("concept_type") != expected_type or not parents_valid or not set(parents).issubset(set(assigned_ids)):
                        findings.append(
                            Finding("SHADOW_TRANSFORMER_ASSIGNMENT_MISMATCH", "ERROR", f"Transformer {agent_id} output {output_id} is not derived solely from assigned parents.", manifest_path.name, agent.get("_line"), (agent_id, output_id))
                        )
        if len(all_reported_outputs) != len(set(all_reported_outputs)):
            findings.append(Finding("SHADOW_CREATIVE_OUTPUT_DUPLICATE", "ERROR", "Creative output IDs are claimed by more than one agent.", manifest_path.name))
        if Counter(direct_parent_multiset) != Counter({problem_id: 1 for problem_id in problem_set}):
            findings.append(
                Finding("SHADOW_DIRECT_PROBLEM_PARTITION_INVALID", "ERROR", "Direct-builder parents must use every one of the 36 problem cards exactly once.", manifest_path.name)
            )

    if complete and mode == "audited_funnel":
        generation_agents = [
            agent for agent in agent_records if agent.get("stage") == "generation"
        ]
        observed_roles = {
            agent.get("role")
            for agent in generation_agents
            if isinstance(agent.get("role"), str)
        }
        if len(generation_agents) != 5 or observed_roles != LIVE_CREATIVE_ROLES:
            findings.append(
                Finding(
                    "LIVE_CREATIVE_ROLE_SET_INVALID",
                    "ERROR",
                    f"Audited Funnel requires exactly the five registered creative roles; found {sorted(observed_roles)} across {len(generation_agents)} agents.",
                    manifest_path.name,
                )
            )
        generation_output_ids: list[str] = []
        for agent in generation_agents:
            outputs, outputs_valid = _valid_string_list(agent.get("output_ids"))
            if outputs_valid:
                generation_output_ids.extend(outputs)
        if Counter(generation_output_ids) != Counter({raw_id: 1 for raw_id in raw_set}):
            findings.append(
                Finding("LIVE_GENERATOR_OUTPUT_PARTITION_INVALID", "ERROR", "The five live generator output_ids must partition every raw hypothesis exactly once.", manifest_path.name)
            )
        generation_ends = [
            agent_times.get(str(agent.get("agent_id")), (None, None))[1]
            for agent in generation_agents
        ]
        if (
            not generation_ends
            or any(value is None for value in generation_ends)
            or not finalist_times
        ):
            findings.append(
                Finding(
                    "LIVE_SELECTION_ORDER_UNKNOWN",
                    "UNKNOWN",
                    "Cannot prove that all five live generators completed before finalist freeze.",
                    manifest_path.name,
                )
            )
        elif max(value for value in generation_ends if value is not None) > min(finalist_times.values()):
            findings.append(
                Finding(
                    "LIVE_SELECTION_ORDER_INVALID",
                    "ERROR",
                    "At least one live finalist froze before all five generators completed.",
                    manifest_path.name,
                )
            )

    query_records = [r for r in manifest_records if r.get("record_type") == "query"]
    source_records = [r for r in manifest_records if r.get("record_type") == "source_open"]
    entity_registry = raw_set | direction_ids | problem_set
    query_by_id: dict[str, dict[str, Any]] = {}
    query_entities: dict[str, set[str]] = {}
    query_times: dict[str, datetime] = {}
    for record in query_records:
        line = record.get("_line")
        query_id = record.get("query_id")
        if not isinstance(query_id, str) or not query_id.strip():
            findings.append(
                Finding("QUERY_ID_MISSING", "ERROR", "Query record has no valid query_id.", manifest_path.name, line)
            )
            continue
        query_id = query_id.strip()
        if query_id in query_by_id:
            findings.append(
                Finding("QUERY_ID_DUPLICATE", "ERROR", f"Query ID {query_id} is duplicated.", manifest_path.name, line, (query_id,))
            )
        else:
            query_by_id[query_id] = record
        if not _normalize_query(record.get("query")):
            findings.append(
                Finding(
                    "QUERY_TEXT_INVALID",
                    "ERROR",
                    f"Query {query_id} has empty or invalid query text.",
                    manifest_path.name,
                    line,
                    (query_id,),
                )
            )
        agent_id = record.get("agent_id")
        if not isinstance(agent_id, str) or agent_id not in agent_by_id:
            findings.append(
                Finding("QUERY_AGENT_UNKNOWN", "ERROR", f"Query {query_id} references unknown agent {agent_id!r}.", manifest_path.name, line, (query_id,))
            )
        else:
            agent = agent_by_id[agent_id]
            if record.get("stage") != agent.get("stage") or record.get("arm") != agent.get("arm"):
                findings.append(
                    Finding("QUERY_AGENT_CONTEXT_MISMATCH", "ERROR", f"Query {query_id} stage/arm differs from its agent record.", manifest_path.name, line, (query_id, agent_id))
                )
        query_time = check_run_time(record.get("occurred_at"), code="QUERY", label=f"Query {query_id}", artifact=manifest_path.name, line=line, ids=(query_id,))
        if query_time is not None:
            query_times[query_id] = query_time
            agent_interval = agent_times.get(str(agent_id), (None, None))
            if (
                agent_interval[0] is None
                or agent_interval[1] is None
                or not (agent_interval[0] <= query_time <= agent_interval[1])
            ):
                findings.append(
                    Finding("QUERY_OUTSIDE_AGENT_INTERVAL", "ERROR", f"Query {query_id} occurred outside its owning agent's interval.", manifest_path.name, line, (query_id, str(agent_id)))
                )
        entity_ids, entity_ids_valid = _valid_string_list(record.get("entity_ids"))
        if not entity_ids_valid:
            findings.append(
                Finding("QUERY_ENTITY_LINK_MISSING", "UNKNOWN", f"Query {query_id} must link to typed problem, concept, or direction IDs.", manifest_path.name, line, (query_id,))
            )
            entity_ids = []
        unknown_entities = sorted(set(entity_ids) - entity_registry)
        if unknown_entities:
            findings.append(
                Finding("QUERY_ENTITY_UNKNOWN", "ERROR", f"Query {query_id} references unknown entities {unknown_entities}.", manifest_path.name, line, (query_id,))
            )
        query_entities[query_id] = set(entity_ids)

    source_by_id: dict[str, dict[str, Any]] = {}
    source_entities: dict[str, set[str]] = {}
    source_times: dict[str, datetime] = {}
    for record in source_records:
        line = record.get("_line")
        source_id = record.get("source_event_id")
        if not isinstance(source_id, str) or not source_id.strip():
            findings.append(
                Finding("SOURCE_EVENT_ID_MISSING", "ERROR", "Source-open record has no valid source_event_id.", manifest_path.name, line)
            )
            continue
        source_id = source_id.strip()
        if source_id in source_by_id:
            findings.append(
                Finding("SOURCE_EVENT_ID_DUPLICATE", "ERROR", f"Source event ID {source_id} is duplicated.", manifest_path.name, line, (source_id,))
            )
        else:
            source_by_id[source_id] = record
        url = record.get("url")
        if not isinstance(url, str) or not re.fullmatch(r"https?://\S+", url.strip()):
            findings.append(
                Finding(
                    "SOURCE_URL_INVALID",
                    "ERROR",
                    f"Source event {source_id} must record an HTTP(S) URL.",
                    manifest_path.name,
                    line,
                    (source_id,),
                )
            )
        query_id = record.get("query_id")
        if not isinstance(query_id, str) or query_id not in query_by_id:
            findings.append(
                Finding("SOURCE_QUERY_UNKNOWN", "ERROR", f"Source event {source_id} references unknown query {query_id!r}.", manifest_path.name, line, (source_id,))
            )
        agent_id = record.get("agent_id")
        if not isinstance(agent_id, str) or agent_id not in agent_by_id:
            findings.append(
                Finding("SOURCE_AGENT_UNKNOWN", "ERROR", f"Source event {source_id} references unknown agent {agent_id!r}.", manifest_path.name, line, (source_id,))
            )
        elif isinstance(query_id, str) and query_id in query_by_id and query_by_id[query_id].get("agent_id") != agent_id:
            findings.append(
                Finding("SOURCE_QUERY_AGENT_MISMATCH", "ERROR", f"Source event {source_id} and query {query_id} have different agents.", manifest_path.name, line, (source_id, query_id))
            )
        if isinstance(agent_id, str) and agent_id in agent_by_id:
            agent = agent_by_id[agent_id]
            if record.get("stage") != agent.get("stage") or record.get("arm") != agent.get("arm"):
                findings.append(
                    Finding("SOURCE_AGENT_CONTEXT_MISMATCH", "ERROR", f"Source event {source_id} stage/arm differs from its agent record.", manifest_path.name, line, (source_id, agent_id))
                )
        source_time = check_run_time(record.get("occurred_at"), code="SOURCE", label=f"Source event {source_id}", artifact=manifest_path.name, line=line, ids=(source_id,))
        if source_time is not None:
            source_times[source_id] = source_time
            agent_interval = agent_times.get(str(agent_id), (None, None))
            if (
                agent_interval[0] is None
                or agent_interval[1] is None
                or not (agent_interval[0] <= source_time <= agent_interval[1])
            ):
                findings.append(
                    Finding("SOURCE_OUTSIDE_AGENT_INTERVAL", "ERROR", f"Source event {source_id} occurred outside its owning agent's interval.", manifest_path.name, line, (source_id, str(agent_id)))
                )
            query_time = query_times.get(str(query_id))
            if query_time is not None and source_time < query_time:
                findings.append(
                    Finding("SOURCE_PRECEDES_QUERY", "ERROR", f"Source event {source_id} precedes its query {query_id}.", manifest_path.name, line, (source_id, str(query_id)))
                )
        entity_ids, entity_ids_valid = _valid_string_list(record.get("entity_ids"))
        if not entity_ids_valid:
            findings.append(
                Finding("SOURCE_ENTITY_LINK_MISSING", "UNKNOWN", f"Source event {source_id} must link to typed entity IDs.", manifest_path.name, line, (source_id,))
            )
            entity_ids = []
        unknown_entities = sorted(set(entity_ids) - entity_registry)
        if unknown_entities:
            findings.append(
                Finding("SOURCE_ENTITY_UNKNOWN", "ERROR", f"Source event {source_id} references unknown entities {unknown_entities}.", manifest_path.name, line, (source_id,))
            )
        source_entities[source_id] = set(entity_ids)
        if isinstance(query_id, str) and query_id in query_entities and not set(entity_ids).issubset(query_entities[query_id]):
            findings.append(
                Finding("SOURCE_QUERY_ENTITY_MISMATCH", "ERROR", f"Source event {source_id} has entities not assigned to query {query_id}.", manifest_path.name, line, (source_id, query_id))
            )
        linked_evidence = record.get("evidence_ids")
        linked_evidence, linked_evidence_valid = _valid_string_list(linked_evidence)
        if not linked_evidence_valid:
            findings.append(
                Finding("SOURCE_EVIDENCE_LINK_MISSING", "UNKNOWN", f"Source event {source_id} has no typed evidence link list.", manifest_path.name, line, (source_id,))
            )
        else:
            for evidence_id in linked_evidence:
                if evidence_id not in evidence_by_id:
                    findings.append(
                        Finding("SOURCE_EVIDENCE_UNKNOWN", "ERROR", f"Source event {source_id} references unknown evidence {evidence_id!r}.", manifest_path.name, line, (source_id, evidence_id))
                    )
                else:
                    evidence_sources, evidence_sources_valid = _valid_string_list(
                        evidence_by_id[evidence_id].get("source_event_ids")
                    )
                    if evidence_sources_valid and source_id not in evidence_sources:
                        findings.append(
                            Finding("SOURCE_EVIDENCE_LINK_ONE_WAY", "ERROR", f"Source {source_id} links evidence {evidence_id}, but the evidence does not link back.", manifest_path.name, line, (source_id, evidence_id))
                        )
    for evidence_id, evidence in evidence_by_id.items():
        linked_sources, linked_sources_valid = _valid_string_list(evidence.get("source_event_ids"))
        if not linked_sources_valid:
            findings.append(
                Finding(
                    "EVIDENCE_SOURCE_LINK_UNKNOWN",
                    "UNKNOWN",
                    f"Evidence {evidence_id} has no source-event ancestry.",
                    ledger_path.name,
                    evidence.get("_line"),
                    (evidence_id,),
                )
            )
        else:
            for source_id in linked_sources:
                if source_id not in source_by_id:
                    findings.append(
                        Finding(
                            "EVIDENCE_SOURCE_UNKNOWN",
                            "ERROR",
                            f"Evidence {evidence_id} references unknown source event {source_id!r}.",
                            ledger_path.name,
                            evidence.get("_line"),
                            (evidence_id,),
                        )
                    )
                    continue
                source_evidence_ids, source_links_valid = _valid_string_list(source_by_id[source_id].get("evidence_ids"))
                if source_links_valid and evidence_id not in source_evidence_ids:
                    findings.append(
                        Finding("EVIDENCE_SOURCE_LINK_ONE_WAY", "ERROR", f"Evidence {evidence_id} links source {source_id}, but the source does not link back.", ledger_path.name, evidence.get("_line"), (evidence_id, source_id))
                    )
                evidence_recorded_at = _parse_timestamp(evidence.get("recorded_at"))
                source_occurred_at = source_times.get(source_id)
                if (
                    evidence_recorded_at is not None
                    and source_occurred_at is not None
                    and evidence_recorded_at < source_occurred_at
                ):
                    findings.append(
                        Finding("EVIDENCE_PRECEDES_SOURCE", "ERROR", f"Evidence {evidence_id} was recorded before source event {source_id} occurred.", ledger_path.name, evidence.get("_line"), (evidence_id, source_id))
                    )
                direction_id = evidence.get("direction_id")
                relevant_entities = ({direction_id} if isinstance(direction_id, str) else set()) | {
                    raw_id
                    for raw_id, raw_mappings in mapping_by_raw.items()
                    if len(raw_mappings) == 1 and raw_mappings[0].get("direction_id") == direction_id
                }
                relevant_entities |= {
                    parent_id
                    for mapping in mappings
                    if mapping.get("direction_id") == direction_id
                    for parent_id in (_valid_string_list(mapping.get("parent_ids"), allow_empty=True)[0])
                    if parent_id in problem_set
                }
                if not source_entities.get(source_id, set()) & relevant_entities:
                    findings.append(
                        Finding("EVIDENCE_ENTITY_LINEAGE_MISMATCH", "ERROR", f"Evidence {evidence_id} has no source entity path to direction {direction_id}.", ledger_path.name, evidence.get("_line"), (evidence_id, source_id))
                    )

    sources_by_query: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in source_records:
        linked_query_id = source.get("query_id")
        if isinstance(linked_query_id, str):
            sources_by_query[linked_query_id].append(source)
    for query_id, query in query_by_id.items():
        if query.get("stage") not in RESEARCH_STAGES:
            continue
        chain_closed = False
        for source in sources_by_query.get(query_id, []):
            source_id = source.get("source_event_id")
            linked_evidence_ids, evidence_links_valid = _valid_string_list(
                source.get("evidence_ids")
            )
            if not evidence_links_valid or not isinstance(source_id, str):
                continue
            for evidence_id in linked_evidence_ids:
                evidence = evidence_by_id.get(evidence_id)
                if not isinstance(evidence, dict):
                    continue
                back_links, back_links_valid = _valid_string_list(
                    evidence.get("source_event_ids")
                )
                if back_links_valid and source_id in back_links:
                    chain_closed = True
                    break
            if chain_closed:
                break
        if not chain_closed:
            findings.append(
                Finding(
                    "QUERY_SOURCE_EVIDENCE_CHAIN_OPEN",
                    "UNKNOWN",
                    f"Research query {query_id} has no reciprocal query-to-source-to-evidence continuation.",
                    manifest_path.name,
                    query.get("_line"),
                    (query_id,),
                )
            )

    unique_queries = {
        _normalize_query(record.get("query"))
        for record in query_records
        if _normalize_query(record.get("query"))
    }
    agent_resource_values: dict[str, float | None] = {}
    agent_resource_keys = V2_AGENT_RESOURCE_KEYS if is_v2 else REQUIRED_AGENT_RESOURCE_KEYS
    for key in agent_resource_keys:
        values: list[float] = []
        valid = True
        for agent in agent_records:
            resource_record = agent.get("resources")
            value = resource_record.get(key) if isinstance(resource_record, dict) else None
            if not _is_nonnegative_number(value):
                valid = False
                break
            values.append(float(value))
        agent_resource_values[key] = sum(values) if valid else None
    v2_terminal_elapsed: Decimal | None = None
    if is_v2:
        v2_resource_boundary = (
            "frozen"
            if _is_v2_shadow_dispatch_prefix(run_record, checkpoint)
            else "complete"
        )
        terminal_checkpoints = [
            record
            for record in manifest_records
            if record.get("record_type") == "checkpoint"
            and record.get("state") == v2_resource_boundary
        ]
        if len(terminal_checkpoints) == 1 and isinstance(
            terminal_checkpoints[0].get("resource_totals"), dict
        ):
            v2_terminal_elapsed = _as_decimal(
                terminal_checkpoints[0]["resource_totals"].get("elapsed_microseconds")
            )
    calculated_resources = {
        "unique_queries": len(unique_queries),
        "uncached_input_tokens": (
            int(agent_resource_values["uncached_input_tokens"])
            if agent_resource_values["uncached_input_tokens"] is not None
            else None
        ),
        "output_tokens": (
            int(agent_resource_values["output_tokens"])
            if agent_resource_values["output_tokens"] is not None
            else None
        ),
        "elapsed_minutes": (
            float(v2_terminal_elapsed / Decimal(60_000_000))
            if is_v2 and v2_terminal_elapsed is not None
            else _wall_minutes(run_record)
        ),
        "elapsed_microseconds": (
            int(v2_terminal_elapsed)
            if is_v2 and v2_terminal_elapsed is not None
            else None
        ),
        "agent_elapsed_microseconds": (
            agent_resource_values.get("elapsed_microseconds") if is_v2 else None
        ),
        "agent_elapsed_minutes": (
            agent_resource_values.get("elapsed_minutes") if not is_v2 else None
        ),
    }
    resources["calculated"] = calculated_resources
    declared_totals = run_record.get("resource_totals")
    budgets = run_record.get("budgets")
    resources["declared"] = declared_totals if isinstance(declared_totals, dict) else {}
    resources["budgets"] = budgets if isinstance(budgets, dict) else {}
    if not isinstance(declared_totals, dict) or not isinstance(budgets, dict):
        findings.append(
            Finding(
                "RESOURCE_TELEMETRY_UNKNOWN",
                "UNKNOWN",
                "Run record lacks resource_totals or budgets.",
                manifest_path.name,
                run_record.get("_line"),
            )
        )
    else:
        missing_budget_keys = sorted(REQUIRED_BUDGET_KEYS - set(budgets))
        if missing_budget_keys:
            findings.append(
                Finding(
                    "RESOURCE_BUDGET_FIELDS_MISSING",
                    "UNKNOWN",
                    f"Budgets omit required fields: {missing_budget_keys}.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        if mode == "archipelago_lite_shadow" or matched_pilot:
            mismatched_caps = {
                key: {"declared": budgets.get(key), "required": required}
                for key, required in MATCHED_RESOURCE_CAPS.items()
                if budgets.get(key) != required
                or not isinstance(budgets.get(key), int)
                or isinstance(budgets.get(key), bool)
            }
            if mismatched_caps:
                findings.append(
                    Finding(
                        "MATCHED_RESOURCE_CAPS_INVALID",
                        "ERROR",
                        f"Matched and shadow arms must use the exact pre-registered caps: {mismatched_caps}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
        for key in REQUIRED_BUDGET_KEYS:
            if key in budgets and not _is_nonnegative_number(budgets[key]):
                findings.append(
                    Finding(
                        "RESOURCE_BUDGET_INVALID",
                        "ERROR",
                        f"Budget {key} must be finite and nonnegative.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
        if "max_concurrency" in budgets and (
            not isinstance(budgets["max_concurrency"], int)
            or isinstance(budgets["max_concurrency"], bool)
            or budgets["max_concurrency"] < 1
        ):
            findings.append(
                Finding(
                    "CONCURRENCY_BUDGET_INVALID",
                    "ERROR",
                    "max_concurrency must be a positive integer.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        total_keys = (
            ("unique_queries", "uncached_input_tokens", "output_tokens", "elapsed_microseconds")
            if is_v2
            else ("unique_queries", "uncached_input_tokens", "output_tokens", "elapsed_minutes")
        )
        for key in total_keys:
            calculated = calculated_resources[key]
            if calculated is None:
                findings.append(
                    Finding(
                        "RESOURCE_CALCULATION_UNKNOWN",
                        "UNKNOWN",
                        f"Resource {key} cannot be calculated from complete typed telemetry.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
                continue
            declared = declared_totals.get(key)
            if declared is None:
                findings.append(
                    Finding(
                        "RESOURCE_TOTAL_FIELD_MISSING",
                        "UNKNOWN",
                        f"Declared resource totals omit {key}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif not _is_nonnegative_number(declared):
                findings.append(
                    Finding(
                        "RESOURCE_TOTAL_INVALID",
                        "ERROR",
                        f"Declared resource {key} must be finite and nonnegative.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            elif float(declared) != float(calculated):
                findings.append(
                    Finding(
                        "RESOURCE_TOTAL_MISMATCH",
                        "ERROR",
                        f"Resource {key}: declared {declared!r}, calculated {calculated!r}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            budget_key = "elapsed_minutes" if key == "elapsed_microseconds" else key
            cap = budgets.get(budget_key)
            effective_cap = (
                float(cap) * 60_000_000
                if key == "elapsed_microseconds" and _is_nonnegative_number(cap)
                else float(cap) if _is_nonnegative_number(cap) else None
            )
            if effective_cap is not None and calculated > effective_cap:
                findings.append(
                    Finding(
                        "RESOURCE_BUDGET_EXCEEDED",
                        "ERROR",
                        f"Resource {key}: used {calculated}, cap {cap}.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )

    if agent_records:
        maximum = _max_concurrency(agent_records)
        resources["max_concurrency"] = maximum
        cap = budgets.get("max_concurrency") if isinstance(budgets, dict) else None
        if maximum is None:
            findings.append(
                Finding(
                    "CONCURRENCY_UNKNOWN",
                    "UNKNOWN",
                    "Agent start/end timestamps are incomplete or invalid.",
                    manifest_path.name,
                )
            )
        elif isinstance(cap, int) and not isinstance(cap, bool) and maximum > cap:
            findings.append(
                Finding(
                    "CONCURRENCY_EXCEEDED",
                    "ERROR",
                    f"Observed concurrency {maximum} exceeds cap {cap}.",
                    manifest_path.name,
                )
            )
        expected_model = run_record.get("model")
        expected_effort = run_record.get("reasoning_effort")
        if not isinstance(expected_model, str) or not expected_model.strip() or not isinstance(expected_effort, str) or not expected_effort.strip():
            findings.append(
                Finding(
                    "MODEL_OR_EFFORT_UNKNOWN",
                    "UNKNOWN",
                    "Run record must declare model and reasoning_effort.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        for agent in agent_records:
            if isinstance(expected_model, str) and expected_model and agent.get("model") != expected_model:
                findings.append(
                    Finding(
                        "MODEL_MISMATCH",
                        "ERROR",
                        f"Agent {agent.get('agent_id')} model differs from the run contract.",
                        manifest_path.name,
                        agent.get("_line"),
                    )
                )
            if isinstance(expected_effort, str) and expected_effort and agent.get("reasoning_effort") != expected_effort:
                findings.append(
                    Finding(
                        "REASONING_EFFORT_MISMATCH",
                        "ERROR",
                        f"Agent {agent.get('agent_id')} reasoning effort differs from the run contract.",
                        manifest_path.name,
                        agent.get("_line"),
                    )
                )

    sealed_fact_closure_ids: set[str] | None = None
    if mode == "archipelago_lite_shadow" and not is_v2:
        stage_counts = Counter(
            agent.get("stage") for agent in agent_records if isinstance(agent.get("stage"), str)
        )
        exact_stage_counts = {
            "problem_discovery": 6,
            "direct_concept": 3,
            "inversion": 2,
            "recombination": 2,
            "history_compressor": 1,
            "cartography": 1,
            "cluster_audit": 1,
            "provisional_selector": 1,
            "selector": 2,
            "tail_challenger": 1,
            "finalist_selector": 1,
        }
        for stage, required in exact_stage_counts.items():
            if stage_counts.get(stage, 0) != required:
                findings.append(
                    Finding(
                        "SHADOW_STAGE_ROLE_COUNT_INVALID",
                        "ERROR",
                        f"Stage {stage} requires {required} agents; found {stage_counts.get(stage, 0)}.",
                        manifest_path.name,
                    )
                )
        for stage in ("level1", "level2", "fact_closure"):
            if stage_counts.get(stage, 0) < 1:
                findings.append(
                    Finding(
                        "SHADOW_STAGE_ROLE_MISSING",
                        "ERROR",
                        f"Shadow run requires at least one {stage} agent.",
                        manifest_path.name,
                    )
                )
        for agent in agent_records:
            if agent.get("arm") != "shadow":
                findings.append(
                    Finding(
                        "SHADOW_AGENT_ARM_INVALID",
                        "ERROR",
                        f"Agent {agent.get('agent_id')} is not assigned to the shadow arm.",
                        manifest_path.name,
                        agent.get("_line"),
                    )
                )

        def require_stage_order(
            predecessor_stages: set[str], successor_stages: set[str], code: str
        ) -> None:
            predecessor_ends = [
                agent_times.get(str(agent.get("agent_id")), (None, None))[1]
                for agent in agent_records
                if agent.get("stage") in predecessor_stages
            ]
            successor_starts = [
                agent_times.get(str(agent.get("agent_id")), (None, None))[0]
                for agent in agent_records
                if agent.get("stage") in successor_stages
            ]
            if (
                not predecessor_ends
                or not successor_starts
                or any(value is None for value in predecessor_ends + successor_starts)
            ):
                findings.append(
                    Finding(
                        f"{code}_UNKNOWN",
                        "UNKNOWN",
                        f"Cannot prove stage order {sorted(predecessor_stages)} -> {sorted(successor_stages)}.",
                        manifest_path.name,
                    )
                )
                return
            latest_predecessor = max(
                value for value in predecessor_ends if value is not None
            )
            earliest_successor = min(
                value for value in successor_starts if value is not None
            )
            if latest_predecessor > earliest_successor:
                findings.append(
                    Finding(
                        code,
                        "ERROR",
                        f"Stage {sorted(successor_stages)} began before {sorted(predecessor_stages)} completed.",
                        manifest_path.name,
                    )
                )

        stage_dependencies = [
            ({"problem_discovery"}, {"direct_concept", "history_compressor"}, "SHADOW_PROBLEM_STAGE_ORDER_INVALID"),
            ({"direct_concept"}, {"inversion", "recombination"}, "SHADOW_TRANSFORM_STAGE_ORDER_INVALID"),
            ({"inversion", "recombination"}, {"cartography"}, "SHADOW_CARTOGRAPHY_STAGE_ORDER_INVALID"),
            ({"cartography"}, {"cluster_audit"}, "SHADOW_CLUSTER_AUDIT_STAGE_ORDER_INVALID"),
            ({"cluster_audit"}, {"level1"}, "SHADOW_LEVEL1_STAGE_ORDER_INVALID"),
            ({"level1"}, {"provisional_selector"}, "SHADOW_PROVISIONAL_STAGE_ORDER_INVALID"),
            ({"provisional_selector"}, {"selector", "tail_challenger"}, "SHADOW_RANKER_STAGE_ORDER_INVALID"),
            ({"selector", "tail_challenger"}, {"level2"}, "SHADOW_LEVEL2_STAGE_ORDER_INVALID"),
            ({"level2"}, {"finalist_selector"}, "SHADOW_FINALIST_SELECTOR_STAGE_ORDER_INVALID"),
            ({"finalist_selector"}, {"fact_closure"}, "SHADOW_FACT_CLOSURE_STAGE_ORDER_INVALID"),
        ]
        for predecessor_stages, successor_stages, code in stage_dependencies:
            require_stage_order(predecessor_stages, successor_stages, code)

        shadow_starts = [_parse_timestamp(agent.get("started_at")) for agent in agent_records]
        valid_shadow_starts = [value for value in shadow_starts if value is not None]
        live_reference_present = isinstance(live_arm_freeze_seal, dict) and isinstance(
            live_arm_freeze_seal_sha256, str
        )
        live_frozen_at: datetime | None = None
        if not live_reference_present:
            findings.append(
                Finding(
                    "LIVE_ARM_FREEZE_SEAL_MISSING",
                    "UNKNOWN",
                    "A shadow audit needs the independently pinned live-arm freeze seal to prove live-before-shadow separation and cross-arm parity.",
                    manifest_path.name,
                )
            )
        else:
            assert live_arm_freeze_seal is not None
            assert live_arm_freeze_seal_sha256 is not None
            if _json_payload_sha256(live_arm_freeze_seal) != live_arm_freeze_seal_sha256:
                findings.append(
                    Finding("LIVE_ARM_FREEZE_SEAL_PAYLOAD_HASH_MISMATCH", "ERROR", "The supplied live-arm freeze-seal payload does not match its SHA-256 pin.")
                )
            if run_record.get("live_arm_freeze_seal_sha256") != live_arm_freeze_seal_sha256:
                findings.append(
                    Finding("LIVE_ARM_FREEZE_SEAL_PIN_MISMATCH", "ERROR", "The shadow manifest is not bound to the supplied live-arm freeze-seal pin.", manifest_path.name, run_record.get("_line"))
                )
            live_root_value = live_arm_freeze_seal.get("run_dir")
            live_root = (
                Path(live_root_value).resolve(strict=False)
                if isinstance(live_root_value, str) and Path(live_root_value).is_absolute()
                else None
            )
            if (
                live_arm_freeze_seal.get("schema") != FREEZE_SEAL_SCHEMA
                or live_arm_freeze_seal.get("mode") != "audited_funnel"
                or live_root is None
                or not live_root.is_dir()
                or live_root == run_dir
                or live_arm_freeze_seal.get("run_id") != live_root.name
                or run_record.get("live_arm_run_dir") != str(live_root)
            ):
                findings.append(
                    Finding("LIVE_ARM_FREEZE_SEAL_IDENTITY_INVALID", "ERROR", "The live-arm seal must bind a distinct canonical audited_funnel run directory declared by the shadow manifest.", manifest_path.name, run_record.get("_line"))
                )
            if live_arm_freeze_seal.get("model") != run_record.get("model"):
                findings.append(
                    Finding("CROSS_ARM_MODEL_MISMATCH", "ERROR", "Live and shadow arms must use the exact same model identifier/version.", manifest_path.name, run_record.get("_line"))
                )
            if live_arm_freeze_seal.get("reasoning_effort") != run_record.get("reasoning_effort"):
                findings.append(
                    Finding("CROSS_ARM_REASONING_EFFORT_MISMATCH", "ERROR", "Live and shadow arms must use the exact same reasoning effort.", manifest_path.name, run_record.get("_line"))
                )
            if live_arm_freeze_seal.get("matched_pilot") is not True:
                findings.append(
                    Finding("LIVE_ARM_MATCHED_MODE_MISMATCH", "ERROR", "A shadow pilot must reference a matched live baseline seal.", manifest_path.name, run_record.get("_line"))
                )
            live_seal_entries = live_arm_freeze_seal.get("finalists")
            live_freeze_times: list[datetime] = []
            live_finalist_ids: set[str] = set()
            live_finalist_paths: set[str] = set()
            live_finalist_hashes: set[str] = set()
            expected_live_count = 6
            if (
                not isinstance(live_seal_entries, list)
                or len(live_seal_entries) != expected_live_count
            ):
                findings.append(
                    Finding("LIVE_ARM_FREEZE_SEAL_FINALIST_COUNT_INVALID", "ERROR", "The referenced live seal must contain the pre-registered live finalist count.")
                )
                live_seal_entries = []
            for live_item in live_seal_entries:
                live_finalist_id = (
                    live_item.get("finalist_id")
                    if isinstance(live_item, dict)
                    else None
                )
                if (
                    not isinstance(live_item, dict)
                    or live_item.get("arm") != "live"
                    or not isinstance(live_finalist_id, str)
                    or not live_finalist_id.strip()
                    or live_finalist_id in live_finalist_ids
                ):
                    findings.append(
                        Finding("LIVE_ARM_FREEZE_SEAL_FINALIST_INVALID", "ERROR", "Every referenced live-seal finalist must be a typed live-arm entry.")
                    )
                    continue
                live_finalist_ids.add(live_finalist_id)
                live_item_frozen_at = _parse_timestamp(live_item.get("frozen_at"))
                if live_item_frozen_at is None:
                    findings.append(
                        Finding("LIVE_ARM_FREEZE_TIME_INVALID", "ERROR", "Referenced live finalists need offset-aware freeze timestamps.")
                    )
                else:
                    live_freeze_times.append(live_item_frozen_at)
                if live_root is not None:
                    live_path, _live_relative = _canonical_run_path(
                        live_root, live_item.get("artifact_path")
                    )
                    declared_live_hash = live_item.get("sha256")
                    if (
                        live_path is None
                        or not live_path.is_file()
                        or (live_root / str(live_item.get("artifact_path"))).is_symlink()
                        or not isinstance(declared_live_hash, str)
                        or not re.fullmatch(r"[0-9a-f]{64}", declared_live_hash)
                        or _sha256(live_path) != declared_live_hash
                    ):
                        findings.append(
                            Finding("LIVE_ARM_FINALIST_ARTIFACT_MISMATCH", "ERROR", f"Referenced live finalist {live_item.get('finalist_id')!r} is missing, unsafe, or no longer matches its seal.")
                        )
                    else:
                        canonical_live_path = str(live_path.resolve())
                        if (
                            canonical_live_path in live_finalist_paths
                            or declared_live_hash in live_finalist_hashes
                        ):
                            findings.append(
                                Finding("LIVE_ARM_FINALIST_DUPLICATE", "ERROR", "Referenced live finalists must have unique paths and content hashes.")
                            )
                        live_finalist_paths.add(canonical_live_path)
                        live_finalist_hashes.add(declared_live_hash)
            if live_freeze_times:
                live_frozen_at = max(live_freeze_times)
                declared_live_frozen_at = _parse_timestamp(
                    run_record.get("live_finalists_frozen_at")
                )
                if declared_live_frozen_at != live_frozen_at:
                    findings.append(
                        Finding("LIVE_ARM_FREEZE_TIME_MISMATCH", "ERROR", "Shadow manifest live_finalists_frozen_at does not equal the externally sealed latest live freeze.", manifest_path.name, run_record.get("_line"))
                    )
            live_sealed_at = _parse_timestamp(live_arm_freeze_seal.get("sealed_at"))
            if (
                live_sealed_at is None
                or live_frozen_at is None
                or live_sealed_at < live_frozen_at
                or not valid_shadow_starts
                or any(value is None for value in shadow_starts)
                or live_sealed_at >= min(valid_shadow_starts)
                or any(live_frozen_at >= value for value in valid_shadow_starts)
            ):
                findings.append(
                    Finding("SHADOW_DISPATCH_ORDER_INVALID", "ERROR", "The externally sealed live cohort was not frozen and sealed before every shadow agent launched.", manifest_path.name)
                )
        frozen_at = _parse_timestamp(run_record.get("main_provisional_frozen_at"))
        selector_agents = [
            agent
            for agent in agent_records
            if agent.get("stage") in {"selector", "tail_challenger"}
        ]
        selector_starts = [_parse_timestamp(agent.get("started_at")) for agent in selector_agents]
        provisional_agents = [
            agent for agent in agent_records if agent.get("stage") == "provisional_selector"
        ]
        provisional_agent_id = (
            provisional_agents[0].get("agent_id") if len(provisional_agents) == 1 else None
        )
        provisional_agent_end = (
            agent_times.get(str(provisional_agent_id), (None, None))[1]
            if provisional_agent_id is not None
            else None
        )
        if (
            len(provisional_agents) != 1
            or provisional_agent_end is None
            or frozen_at is None
            or provisional_agent_end > frozen_at
        ):
            findings.append(
                Finding(
                    "SHADOW_PROVISIONAL_SELECTOR_ORDER_INVALID",
                    "ERROR",
                    "Exactly one isolated provisional selector must finish before the sealed order freezes.",
                    manifest_path.name,
                )
            )
        if len(selector_agents) != 3 or stage_counts.get("selector", 0) != 2 or stage_counts.get("tail_challenger", 0) != 1:
            findings.append(
                Finding(
                    "SHADOW_SELECTOR_COUNT_INVALID",
                    "ERROR",
                    f"Expected two rankers and one tail challenger; found {len(selector_agents)} agents.",
                    manifest_path.name,
                )
            )
        if frozen_at is None or not selector_starts or any(value is None for value in selector_starts):
            findings.append(
                Finding(
                    "SHADOW_SELECTION_FREEZE_ORDER_UNKNOWN",
                    "UNKNOWN",
                    "Cannot prove the main provisional list froze before selector launch.",
                    manifest_path.name,
                )
            )
        elif any(frozen_at >= value for value in selector_starts if value is not None):
            findings.append(
                Finding(
                    "SHADOW_SELECTION_FREEZE_ORDER_INVALID",
                    "ERROR",
                    "Main provisional choices did not freeze before selector launch.",
                    manifest_path.name,
                )
            )
        provisional_path = _safe_path(run_dir, run_record.get("main_provisional_file"))
        if provisional_path is None or not provisional_path.is_file():
            findings.append(
                Finding(
                    "SHADOW_PROVISIONAL_FILE_MISSING",
                    "ERROR",
                    "The sealed main provisional order file is missing.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        else:
            if run_record.get("main_provisional_sha256") != _sha256(provisional_path):
                findings.append(
                    Finding(
                        "SHADOW_PROVISIONAL_HASH_MISMATCH",
                        "ERROR",
                        "The sealed main provisional order hash does not match.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            try:
                provisional_text = provisional_path.read_text(encoding="utf-8-sig")
                provisional_payload = json.loads(provisional_text)
            except (OSError, UnicodeError, json.JSONDecodeError):
                provisional_text = ""
                provisional_payload = None
                findings.append(
                    Finding(
                        "SHADOW_PROVISIONAL_CONTENT_INVALID",
                        "ERROR",
                        "The sealed provisional file is not readable JSON.",
                        str(provisional_path.relative_to(run_dir)),
                    )
                )
            if any(
                pattern.search(provisional_text)
                for pattern in PROHIBITED_PACKET_PATTERNS
            ):
                findings.append(
                    Finding(
                        "SHADOW_PROVISIONAL_PROHIBITED_CONTENT",
                        "ERROR",
                        "The sealed provisional selector artifact contains prohibited validator, score, threshold, or evaluator material.",
                        str(provisional_path.relative_to(run_dir)),
                    )
                )
            if isinstance(provisional_payload, dict):
                main_ids, main_ids_valid = _valid_string_list(provisional_payload.get("main_provisional_ids"))
                reserve_ids, reserve_ids_valid = _valid_string_list(provisional_payload.get("ordered_reserve"))
                if (
                    not main_ids_valid
                    or not reserve_ids_valid
                    or len(main_ids) != 6
                    or len(reserve_ids) != 42
                    or len(set(main_ids + reserve_ids)) != 48
                    or set(main_ids + reserve_ids) != raw_set
                ):
                    findings.append(
                        Finding(
                            "SHADOW_PROVISIONAL_ORDER_INVALID",
                            "ERROR",
                            "Sealed provisional JSON must partition all 48 concepts into six main IDs plus an ordered reserve of 42.",
                            str(provisional_path.relative_to(run_dir)),
                        )
                    )
                provisional_frozen_at = _parse_timestamp(provisional_payload.get("frozen_at"))
                if provisional_frozen_at is None or frozen_at is None or provisional_frozen_at != frozen_at:
                    findings.append(
                        Finding(
                            "SHADOW_PROVISIONAL_TIMESTAMP_MISMATCH",
                            "ERROR",
                            "Sealed provisional frozen_at must equal the run record timestamp.",
                            str(provisional_path.relative_to(run_dir)),
                        )
                    )
                if provisional_payload.get("creator_agent_id") != provisional_agent_id:
                    findings.append(
                        Finding(
                            "SHADOW_PROVISIONAL_CREATOR_MISMATCH",
                            "ERROR",
                            "Sealed provisional JSON must name the isolated provisional selector that created it.",
                            str(provisional_path.relative_to(run_dir)),
                        )
                    )
                main_level2 = {
                    record.get("concept_id")
                    for record in level2_records
                    if record.get("selection_category") == "main_provisional"
                    and isinstance(record.get("concept_id"), str)
                }
                if main_ids_valid and main_level2 != set(main_ids):
                    findings.append(
                        Finding(
                            "SHADOW_MAIN_LEVEL2_MISMATCH",
                            "ERROR",
                            "The six main-provisional Level-2 records do not match the sealed main list.",
                            ledger_path.name,
                        )
                    )
        finalist_selector_agents = [
            agent for agent in agent_records if agent.get("stage") == "finalist_selector"
        ]
        finalist_selector_id = (
            finalist_selector_agents[0].get("agent_id")
            if len(finalist_selector_agents) == 1
            else None
        )
        finalist_selector_end = (
            agent_times.get(str(finalist_selector_id), (None, None))[1]
            if finalist_selector_id is not None
            else None
        )
        finalist_selector_start = (
            agent_times.get(str(finalist_selector_id), (None, None))[0]
            if finalist_selector_id is not None
            else None
        )
        if (
            finalist_selector_start is None
            or len(level2_completed_at_by_id) != len(level2_set)
            or any(
                completed_at > finalist_selector_start
                for completed_at in level2_completed_at_by_id.values()
            )
        ):
            findings.append(
                Finding(
                    "SHADOW_LEVEL2_COMPLETION_ORDER_INVALID",
                    "ERROR",
                    "All twelve Level-2 dossiers must complete before the isolated finalist selector starts.",
                    manifest_path.name,
                )
            )
        fact_closure_starts = [
            agent_times.get(str(agent.get("agent_id")), (None, None))[0]
            for agent in agent_records
            if agent.get("stage") == "fact_closure"
        ]
        valid_fact_closure_starts = [value for value in fact_closure_starts if value is not None]
        closure_selected_at = _parse_timestamp(run_record.get("fact_closure_selected_at"))
        if (
            len(finalist_selector_agents) != 1
            or finalist_selector_end is None
            or closure_selected_at is None
            or finalist_selector_end > closure_selected_at
            or (
                valid_fact_closure_starts
                and closure_selected_at >= min(valid_fact_closure_starts)
            )
        ):
            findings.append(
                Finding(
                    "SHADOW_FINALIST_SELECTOR_ORDER_INVALID",
                    "ERROR",
                    "Exactly one isolated finalist selector must finish and seal six IDs before fact closure starts.",
                    manifest_path.name,
                )
            )
        closure_path = _safe_path(run_dir, run_record.get("fact_closure_candidates_file"))
        if closure_path is None or not closure_path.is_file():
            findings.append(
                Finding(
                    "SHADOW_FACT_CLOSURE_FILE_MISSING",
                    "ERROR",
                    "The sealed fact-closure candidate file is missing.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        else:
            if run_record.get("fact_closure_candidates_sha256") != _sha256(closure_path):
                findings.append(
                    Finding(
                        "SHADOW_FACT_CLOSURE_HASH_MISMATCH",
                        "ERROR",
                        "The sealed fact-closure candidate hash does not match.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            try:
                closure_text = closure_path.read_text(encoding="utf-8-sig")
                closure_payload = json.loads(closure_text)
            except (OSError, UnicodeError, json.JSONDecodeError):
                closure_text = ""
                closure_payload = None
                findings.append(
                    Finding(
                        "SHADOW_FACT_CLOSURE_CONTENT_INVALID",
                        "ERROR",
                        "The sealed fact-closure file is not readable JSON.",
                        str(closure_path.relative_to(run_dir)),
                    )
                )
            if any(
                pattern.search(closure_text)
                for pattern in PROHIBITED_PACKET_PATTERNS
            ):
                findings.append(
                    Finding(
                        "SHADOW_FACT_CLOSURE_PROHIBITED_CONTENT",
                        "ERROR",
                        "The sealed finalist-selector artifact contains prohibited validator, score, threshold, or evaluator material.",
                        str(closure_path.relative_to(run_dir)),
                    )
                )
            if isinstance(closure_payload, dict):
                candidate_ids, candidate_ids_valid = _valid_string_list(
                    closure_payload.get("candidate_ids")
                )
                if (
                    not candidate_ids_valid
                    or len(candidate_ids) != 6
                    or len(set(candidate_ids)) != 6
                    or not set(candidate_ids).issubset(level2_set)
                ):
                    findings.append(
                        Finding(
                            "SHADOW_FACT_CLOSURE_COHORT_INVALID",
                            "ERROR",
                            "Fact-closure JSON must contain six unique Level-2 candidate IDs.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )
                else:
                    sealed_fact_closure_ids = set(candidate_ids)
                    incomplete_candidates = sorted(
                        concept_id
                        for concept_id in candidate_ids
                        if level2_status_by_id.get(concept_id) != "complete"
                    )
                    if incomplete_candidates:
                        findings.append(
                            Finding(
                                "SHADOW_FACT_CLOSURE_LEVEL2_INCOMPLETE",
                                "ERROR",
                                f"Fact-closure candidates must all have completed Level-2 dossiers: {incomplete_candidates}.",
                                str(closure_path.relative_to(run_dir)),
                                node_ids=tuple(incomplete_candidates),
                            )
                        )
                payload_selected_at = _parse_timestamp(closure_payload.get("selected_at"))
                if payload_selected_at is None or payload_selected_at != closure_selected_at:
                    findings.append(
                        Finding(
                            "SHADOW_FACT_CLOSURE_TIMESTAMP_MISMATCH",
                            "ERROR",
                            "Fact-closure selected_at must equal the run record timestamp.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )
                if closure_payload.get("creator_agent_id") != finalist_selector_id:
                    findings.append(
                        Finding(
                            "SHADOW_FACT_CLOSURE_CREATOR_MISMATCH",
                            "ERROR",
                            "Fact-closure JSON must name the isolated finalist selector that created it.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )

        fact_closure_ends = [
            agent_times.get(str(agent.get("agent_id")), (None, None))[1]
            for agent in agent_records
            if agent.get("stage") == "fact_closure"
        ]
        valid_fact_closure_ends = [value for value in fact_closure_ends if value is not None]
        if valid_fact_closure_ends:
            closure_finished_at = max(valid_fact_closure_ends)
            for finalist_id, finalist_frozen_at in finalist_times.items():
                if finalist_frozen_at < closure_finished_at:
                    findings.append(
                        Finding(
                            "SHADOW_FINALIST_FROZEN_BEFORE_FACT_CLOSURE",
                            "ERROR",
                            f"Finalist {finalist_id} froze before fact closure completed.",
                            ledger_path.name,
                            node_ids=(finalist_id,),
                        )
                    )
    if legacy_profile == "v2_matched_nonrouting" and mode == "audited_funnel":
        closure_selected_at = _parse_timestamp(run_record.get("fact_closure_selected_at"))
        fact_closure_agents = [
            agent for agent in agent_records if agent.get("stage") == "fact_closure"
        ]
        fact_closure_starts = [
            agent_times.get(str(agent.get("agent_id")), (None, None))[0]
            for agent in fact_closure_agents
        ]
        valid_fact_closure_starts = [value for value in fact_closure_starts if value is not None]
        if (
            closure_selected_at is None
            or not valid_fact_closure_starts
            or closure_selected_at >= min(valid_fact_closure_starts)
        ):
            findings.append(
                Finding(
                    "MATCHED_FACT_CLOSURE_SELECTION_ORDER_INVALID",
                    "ERROR",
                    "The matched baseline must seal six Level-2 directions before fact closure starts.",
                    manifest_path.name,
                )
            )
        closure_path = _safe_path(run_dir, run_record.get("fact_closure_candidates_file"))
        if closure_path is None or not closure_path.is_file():
            findings.append(
                Finding(
                    "MATCHED_FACT_CLOSURE_FILE_MISSING",
                    "ERROR",
                    "The matched baseline's sealed fact-closure candidate file is missing.",
                    manifest_path.name,
                    run_record.get("_line"),
                )
            )
        else:
            if run_record.get("fact_closure_candidates_sha256") != _sha256(closure_path):
                findings.append(
                    Finding(
                        "MATCHED_FACT_CLOSURE_HASH_MISMATCH",
                        "ERROR",
                        "The matched baseline's fact-closure candidate hash does not match.",
                        manifest_path.name,
                        run_record.get("_line"),
                    )
                )
            try:
                closure_payload = json.loads(closure_path.read_text(encoding="utf-8-sig"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                closure_payload = None
                findings.append(
                    Finding(
                        "MATCHED_FACT_CLOSURE_CONTENT_INVALID",
                        "ERROR",
                        "The matched baseline's fact-closure file is not readable JSON.",
                        str(closure_path.relative_to(run_dir)),
                    )
                )
            if isinstance(closure_payload, dict):
                candidate_ids, candidate_ids_valid = _valid_string_list(
                    closure_payload.get("candidate_ids")
                )
                if (
                    not candidate_ids_valid
                    or len(candidate_ids) != 6
                    or len(set(candidate_ids)) != 6
                    or not set(candidate_ids).issubset(level2_set)
                ):
                    findings.append(
                        Finding(
                            "MATCHED_FACT_CLOSURE_COHORT_INVALID",
                            "ERROR",
                            "Matched fact-closure JSON must contain six unique Level-2 direction IDs.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )
                else:
                    sealed_fact_closure_ids = set(candidate_ids)
                payload_selected_at = _parse_timestamp(closure_payload.get("selected_at"))
                if payload_selected_at is None or payload_selected_at != closure_selected_at:
                    findings.append(
                        Finding(
                            "MATCHED_FACT_CLOSURE_TIMESTAMP_MISMATCH",
                            "ERROR",
                            "Matched fact-closure selected_at must equal the run record timestamp.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )
                if closure_payload.get("creator_agent_id") != "root-orchestrator":
                    findings.append(
                        Finding(
                            "MATCHED_FACT_CLOSURE_CREATOR_INVALID",
                            "ERROR",
                            "Matched fact-closure JSON must identify the existing main-agent rule as root-orchestrator.",
                            str(closure_path.relative_to(run_dir)),
                        )
                    )
        fact_closure_ends = [
            agent_times.get(str(agent.get("agent_id")), (None, None))[1]
            for agent in fact_closure_agents
        ]
        valid_fact_closure_ends = [value for value in fact_closure_ends if value is not None]
        if not valid_fact_closure_ends:
            findings.append(
                Finding(
                    "MATCHED_FACT_CLOSURE_COMPLETION_UNKNOWN",
                    "UNKNOWN",
                    "Cannot prove that matched fact closure completed before finalist freeze.",
                    manifest_path.name,
                )
            )
        else:
            closure_finished_at = max(valid_fact_closure_ends)
            for finalist_id, finalist_frozen_at in finalist_times.items():
                if finalist_frozen_at < closure_finished_at:
                    findings.append(
                        Finding(
                            "MATCHED_FINALIST_FROZEN_BEFORE_FACT_CLOSURE",
                            "ERROR",
                            f"Finalist {finalist_id} froze before matched fact closure completed.",
                            ledger_path.name,
                            node_ids=(finalist_id,),
                        )
                    )
    if (mode == "archipelago_lite_shadow" or matched_pilot) and not is_v2:
        allocation_records = [
            record for record in manifest_records if record.get("record_type") == "allocation"
        ]
        allocation_by_id: dict[str, dict[str, Any]] = {}
        allocation_phase_counts = Counter()
        allocation_query_caps = {"level2": 12, "fact_closure": 8}
        for allocation in allocation_records:
            line = allocation.get("_line")
            allocation_id = allocation.get("allocation_id")
            if not isinstance(allocation_id, str) or not allocation_id.strip():
                findings.append(
                    Finding("ALLOCATION_ID_INVALID", "ERROR", "Allocation record has no valid allocation_id.", manifest_path.name, line)
                )
                continue
            allocation_id = allocation_id.strip()
            if allocation_id in allocation_by_id:
                findings.append(
                    Finding("ALLOCATION_ID_DUPLICATE", "ERROR", f"Allocation ID {allocation_id} is duplicated.", manifest_path.name, line, (allocation_id,))
                )
            allocation_by_id[allocation_id] = allocation
            stage = allocation.get("stage")
            phase = (
                "discovery"
                if isinstance(stage, str) and stage in {"problem_discovery", "generation"}
                else stage
            )
            supported_phases = {"discovery", *allocation_query_caps, *ZERO_QUERY_STAGES}
            if not isinstance(phase, str) or phase not in supported_phases:
                findings.append(
                    Finding("ALLOCATION_STAGE_INVALID", "ERROR", f"Allocation {allocation_id} has unsupported stage {stage!r}.", manifest_path.name, line, (allocation_id,))
                )
                continue
            if phase in {"discovery", *allocation_query_caps}:
                allocation_phase_counts[phase] += 1
            cap = allocation.get("query_cap")
            used = allocation.get("used_unique_queries")
            unused = allocation.get("unused_queries")
            expected_cap: int | None
            if phase in ZERO_QUERY_STAGES:
                expected_cap = 0
            elif phase == "discovery" and mode == "archipelago_lite_shadow":
                expected_cap = 18
            elif phase == "discovery" and matched_pilot and mode == "audited_funnel":
                expected_cap = cap if cap in {21, 22} else None
            else:
                expected_cap = allocation_query_caps.get(phase)
            if expected_cap is None or cap != expected_cap:
                requirement = (
                    "21 or 22 (five pre-registered allocations totaling 108)"
                    if phase == "discovery" and matched_pilot and mode == "audited_funnel"
                    else str(expected_cap)
                )
                findings.append(
                    Finding("ALLOCATION_CAP_INVALID", "ERROR", f"Allocation {allocation_id} must have query_cap {requirement}; found {cap!r}.", manifest_path.name, line, (allocation_id,))
                )
            if not _is_nonnegative_number(used) or not _is_nonnegative_number(unused):
                findings.append(
                    Finding("ALLOCATION_USAGE_INVALID", "ERROR", f"Allocation {allocation_id} used/unused counts must be finite and nonnegative.", manifest_path.name, line, (allocation_id,))
                )
            elif not isinstance(used, int) or isinstance(used, bool) or not isinstance(unused, int) or isinstance(unused, bool) or used + unused != cap:
                findings.append(
                    Finding("ALLOCATION_RECONCILIATION_INVALID", "ERROR", f"Allocation {allocation_id} must reconcile used + unused to its integer cap.", manifest_path.name, line, (allocation_id,))
                )
            elif unused > 0 and not isinstance(allocation.get("unused_reason"), str):
                findings.append(
                    Finding("ALLOCATION_UNUSED_REASON_MISSING", "UNKNOWN", f"Allocation {allocation_id} leaves budget unused without a reason.", manifest_path.name, line, (allocation_id,))
                )
            agent_id = allocation.get("agent_id")
            if not isinstance(agent_id, str) or agent_id not in agent_by_id:
                findings.append(
                    Finding("ALLOCATION_AGENT_UNKNOWN", "ERROR", f"Allocation {allocation_id} references unknown agent {agent_id!r}.", manifest_path.name, line, (allocation_id,))
                )
            else:
                agent_stage = agent_by_id[agent_id].get("stage")
                accepted_agent_stages = {stage}
                if stage in {"generation", "problem_discovery"}:
                    accepted_agent_stages |= {"generation", "problem_discovery"}
                if agent_stage not in accepted_agent_stages:
                    findings.append(
                        Finding(
                            "ALLOCATION_AGENT_STAGE_MISMATCH",
                            "ERROR",
                            f"Allocation {allocation_id} stage {stage!r} does not match agent {agent_id} stage {agent_stage!r}.",
                            manifest_path.name,
                            line,
                            (allocation_id, agent_id),
                        )
                    )
            entity_id = allocation.get("entity_id")
            if not isinstance(entity_id, str) or not entity_id:
                findings.append(
                    Finding("ALLOCATION_ENTITY_INVALID", "ERROR", f"Allocation {allocation_id} has no valid entity_id.", manifest_path.name, line, (allocation_id,))
                )
            elif phase == "discovery" and entity_id not in agent_by_id:
                findings.append(
                    Finding("ALLOCATION_ENTITY_UNKNOWN", "ERROR", f"Discovery allocation {allocation_id} must use a known scout/search-unit agent as entity_id.", manifest_path.name, line, (allocation_id,))
                )
            elif phase in {"level2", "fact_closure"} and entity_id not in level2_set:
                findings.append(
                    Finding("ALLOCATION_ENTITY_UNKNOWN", "ERROR", f"Allocation {allocation_id} references an entity outside the Level-2 cohort: {entity_id!r}.", manifest_path.name, line, (allocation_id,))
                )

        expected_allocation_counts = {
            "discovery": 6 if mode == "archipelago_lite_shadow" else 5,
            "level2": 12,
            "fact_closure": 6,
        }
        if any(
            allocation_phase_counts.get(phase, 0) != required
            for phase, required in expected_allocation_counts.items()
        ):
            findings.append(
                Finding(
                    "ALLOCATION_PHASE_COUNTS_INVALID",
                    "ERROR",
                    f"Expected allocation counts {expected_allocation_counts}; found {dict(allocation_phase_counts)}.",
                    manifest_path.name,
                )
            )
        discovery_caps = sorted(
            record.get("query_cap")
            for record in allocation_records
            if record.get("stage") in {"problem_discovery", "generation"}
            and isinstance(record.get("query_cap"), int)
            and not isinstance(record.get("query_cap"), bool)
        )
        expected_discovery_caps = (
            [18] * 6 if mode == "archipelago_lite_shadow" else [21, 21, 22, 22, 22]
        )
        if discovery_caps != expected_discovery_caps:
            findings.append(
                Finding(
                    "DISCOVERY_ALLOCATION_SPLIT_INVALID",
                    "ERROR",
                    f"Expected discovery caps {expected_discovery_caps}; found {discovery_caps}.",
                    manifest_path.name,
                )
            )
        discovery_entities = [
            record.get("entity_id")
            for record in allocation_records
            if record.get("stage") in {"problem_discovery", "generation"}
            and isinstance(record.get("entity_id"), str)
        ]
        expected_discovery_agents = {
            str(agent.get("agent_id"))
            for agent in agent_records
            if agent.get("stage")
            == ("problem_discovery" if mode == "archipelago_lite_shadow" else "generation")
        }
        if (
            len(discovery_entities) != expected_allocation_counts["discovery"]
            or len(set(discovery_entities)) != len(discovery_entities)
            or set(discovery_entities) != expected_discovery_agents
        ):
            findings.append(
                Finding(
                    "DISCOVERY_ALLOCATION_COVERAGE_INVALID",
                    "ERROR",
                    "Discovery allocations must cover each required scout or creative-role agent exactly once.",
                    manifest_path.name,
                )
            )
        level2_allocation_entities = {
            record.get("entity_id")
            for record in allocation_records
            if record.get("stage") == "level2" and isinstance(record.get("entity_id"), str)
        }
        if level2_allocation_entities != level2_set:
            findings.append(
                Finding("LEVEL2_ALLOCATION_COVERAGE_INVALID", "ERROR", "Level-2 allocations must cover each Level-2 concept exactly once.", manifest_path.name)
            )
        fact_allocation_entities = {
            record.get("entity_id")
            for record in allocation_records
            if record.get("stage") == "fact_closure" and isinstance(record.get("entity_id"), str)
        }
        finalist_cohort_ids = (
            {
                raw_id
                for finalist in finalist_records
                for raw_id in (_valid_string_list(finalist.get("raw_ids"))[0])
            }
            if mode == "archipelago_lite_shadow"
            else {
                finalist.get("direction_id")
                for finalist in finalist_records
                if isinstance(finalist.get("direction_id"), str)
            }
        )
        if len(fact_allocation_entities) != 6 or finalist_cohort_ids != fact_allocation_entities:
            findings.append(
                Finding("FACT_CLOSURE_ALLOCATION_COVERAGE_INVALID", "ERROR", "Six fact-closure allocations must exactly match the six frozen finalist cohort entities.", manifest_path.name)
            )
        if (
            sealed_fact_closure_ids is not None
            and fact_allocation_entities != sealed_fact_closure_ids
        ):
            findings.append(
                Finding(
                    "SHADOW_FACT_CLOSURE_COHORT_MISMATCH"
                    if mode == "archipelago_lite_shadow"
                    else "MATCHED_FACT_CLOSURE_COHORT_MISMATCH",
                    "ERROR",
                    "The sealed cohort, fact-closure allocations, and frozen finalist cohort must be identical.",
                    manifest_path.name,
                )
            )

        queries_by_allocation: dict[str, set[str]] = defaultdict(set)
        for query in query_records:
            query_id = query.get("query_id")
            allocation_id = query.get("allocation_id")
            if not isinstance(allocation_id, str) or allocation_id not in allocation_by_id:
                findings.append(
                    Finding("QUERY_ALLOCATION_UNKNOWN", "ERROR", f"Query {query_id!r} lacks a known allocation_id.", manifest_path.name, query.get("_line"))
                )
                continue
            normalized = _normalize_query(query.get("query"))
            if normalized:
                queries_by_allocation[allocation_id].add(normalized)
            allocation = allocation_by_id[allocation_id]
            accepted_stages = {allocation.get("stage")}
            if isinstance(allocation.get("stage"), str) and allocation.get("stage") in {"generation", "problem_discovery"}:
                accepted_stages |= {"generation", "problem_discovery"}
            if query.get("stage") not in accepted_stages or query.get("agent_id") != allocation.get("agent_id"):
                findings.append(
                    Finding("QUERY_ALLOCATION_CONTEXT_MISMATCH", "ERROR", f"Query {query_id!r} stage/agent differs from allocation {allocation_id}.", manifest_path.name, query.get("_line"))
                )
        for allocation_id, allocation in allocation_by_id.items():
            observed = len(queries_by_allocation.get(allocation_id, set()))
            if allocation.get("used_unique_queries") != observed:
                findings.append(
                    Finding("ALLOCATION_QUERY_COUNT_MISMATCH", "ERROR", f"Allocation {allocation_id} declares {allocation.get('used_unique_queries')!r} used queries; observed {observed}.", manifest_path.name, allocation.get("_line"), (allocation_id,))
                )

        for stage, cap in SHADOW_QUERY_CAPS.items():
            accepted_stages = {stage}
            if stage == "problem_discovery":
                accepted_stages.add("generation")
            observed = len(
                {
                    _normalize_query(r.get("query"))
                    for r in query_records
                    if r.get("stage") in accepted_stages and _normalize_query(r.get("query"))
                }
            )
            if observed > cap:
                findings.append(
                    Finding(
                        "SHADOW_STAGE_QUERY_CAP_EXCEEDED",
                        "ERROR",
                        f"Stage {stage} used {observed} unique queries; cap is {cap}.",
                        manifest_path.name,
                    )
                )

    if not is_v2 and not (mode == "archipelago_lite_shadow" or matched_pilot):
        legacy_allocations = [
            record
            for record in manifest_records
            if record.get("record_type") == "allocation"
        ]
        if legacy_allocations:
            legacy_allocation_by_id = {
                record.get("allocation_id"): record
                for record in legacy_allocations
                if isinstance(record.get("allocation_id"), str)
            }
            legacy_queries_by_allocation: dict[str, set[str]] = defaultdict(set)
            for query in query_records:
                if query.get("stage") not in RESEARCH_STAGES:
                    continue
                query_id = query.get("query_id")
                allocation_id = query.get("allocation_id")
                if (
                    not isinstance(allocation_id, str)
                    or allocation_id not in legacy_allocation_by_id
                ):
                    findings.append(
                        Finding(
                            "QUERY_ALLOCATION_UNKNOWN",
                            "ERROR",
                            f"Query {query_id!r} lacks a known allocation_id.",
                            manifest_path.name,
                            query.get("_line"),
                        )
                    )
                    continue
                normalized = _normalize_query(query.get("query"))
                if normalized:
                    legacy_queries_by_allocation[allocation_id].add(normalized)
                allocation = legacy_allocation_by_id[allocation_id]
                accepted_stages = {allocation.get("stage")}
                if allocation.get("stage") in {"generation", "problem_discovery"}:
                    accepted_stages |= {"generation", "problem_discovery"}
                if (
                    query.get("stage") not in accepted_stages
                    or query.get("agent_id") != allocation.get("agent_id")
                ):
                    findings.append(
                        Finding(
                            "QUERY_ALLOCATION_CONTEXT_MISMATCH",
                            "ERROR",
                            f"Query {query_id!r} stage/agent differs from allocation {allocation_id}.",
                            manifest_path.name,
                            query.get("_line"),
                        )
                    )
            for allocation_id, allocation in legacy_allocation_by_id.items():
                observed = len(legacy_queries_by_allocation.get(allocation_id, set()))
                if allocation.get("used_unique_queries") != observed:
                    findings.append(
                        Finding(
                            "ALLOCATION_QUERY_COUNT_MISMATCH",
                            "ERROR",
                            f"Allocation {allocation_id} declares {allocation.get('used_unique_queries')!r} used queries; observed {observed}.",
                            manifest_path.name,
                            allocation.get("_line"),
                            (allocation_id,),
                        )
                    )

    tool_events = [r for r in manifest_records if r.get("record_type") == "tool_event"]
    seen_call_ids: set[str] = set()
    tool_linked_query_ids: set[str] = set()
    tool_times_by_query: dict[str, list[datetime]] = defaultdict(list)
    for event in tool_events:
        line = event.get("_line")
        call_id = event.get("call_id")
        if not isinstance(call_id, str) or not call_id.strip():
            findings.append(
                Finding("TOOL_CALL_ID_INVALID", "ERROR", "Tool event has no valid call_id.", manifest_path.name, line)
            )
        elif call_id in seen_call_ids:
            findings.append(
                Finding("TOOL_CALL_ID_DUPLICATE", "ERROR", f"Tool call ID {call_id} is duplicated.", manifest_path.name, line, (call_id,))
            )
        else:
            seen_call_ids.add(call_id)
        agent_id = event.get("agent_id")
        if not isinstance(agent_id, str) or agent_id not in agent_by_id:
            findings.append(
                Finding("TOOL_AGENT_UNKNOWN", "ERROR", f"Tool event references unknown agent {agent_id!r}.", manifest_path.name, line)
            )
        else:
            agent = agent_by_id[agent_id]
            if event.get("stage") != agent.get("stage") or event.get("arm") != agent.get("arm"):
                findings.append(
                    Finding(
                        "TOOL_AGENT_CONTEXT_MISMATCH",
                        "ERROR",
                        f"Tool event {call_id!r} stage/arm differs from its agent record.",
                        manifest_path.name,
                        line,
                    )
                )
        occurred_at = _parse_timestamp(event.get("occurred_at"))
        if occurred_at is None:
            findings.append(
                Finding("TOOL_TIME_UNKNOWN", "UNKNOWN", "Tool event lacks an offset-aware occurred_at timestamp.", manifest_path.name, line)
            )
            # Missing timing cannot exonerate an explicitly forbidden call.
            in_window = True
        elif run_start is not None and run_end is not None and occurred_at > run_end:
            findings.append(
                Finding("TOOL_EVENT_AFTER_RUN", "INFO", "Post-run tool event was excluded from routing and resource checks.", manifest_path.name, line)
            )
            in_window = False
        elif run_start is not None and occurred_at < run_start:
            findings.append(
                Finding("TOOL_EVENT_BEFORE_RUN", "ERROR", "Tool event precedes the declared run window.", manifest_path.name, line)
            )
            in_window = False
        else:
            in_window = True
        if in_window and occurred_at is not None and isinstance(agent_id, str):
            agent_interval = agent_times.get(agent_id, (None, None))
            if (
                agent_interval[0] is None
                or agent_interval[1] is None
                or not (agent_interval[0] <= occurred_at <= agent_interval[1])
            ):
                findings.append(
                    Finding("TOOL_OUTSIDE_AGENT_INTERVAL", "ERROR", f"Tool event {call_id!r} occurred outside its owning agent's interval.", manifest_path.name, line, (str(call_id), agent_id))
                )
        tool = _canonical_tool_name(event.get("tool"))
        event_type = _canonical_tool_name(event.get("event_type"))
        if not tool or not event_type:
            findings.append(
                Finding(
                    "TOOL_EVENT_TYPE_INVALID",
                    "ERROR",
                    "Tool events must declare typed tool and event_type values.",
                    manifest_path.name,
                    line,
                )
            )
        query_id = event.get("query_id")
        is_query_tool = any(
            marker in tool for marker in ("search", "query", "browser", "web")
        )
        if in_window and (query_id is not None or is_query_tool):
            if not isinstance(query_id, str) or query_id not in query_by_id:
                findings.append(
                    Finding(
                        "TOOL_QUERY_UNKNOWN",
                        "ERROR",
                        f"Query-capable tool event {call_id!r} must reference a known query_id.",
                        manifest_path.name,
                        line,
                    )
                )
            else:
                query_record = query_by_id[query_id]
                tool_linked_query_ids.add(query_id)
                if occurred_at is not None:
                    tool_times_by_query[query_id].append(occurred_at)
                    query_time = query_times.get(query_id)
                    if query_time is not None and occurred_at < query_time:
                        findings.append(
                            Finding("TOOL_PRECEDES_QUERY", "ERROR", f"Tool event {call_id!r} precedes linked query {query_id}.", manifest_path.name, line, (str(call_id), query_id))
                        )
                if (
                    query_record.get("agent_id") != agent_id
                    or query_record.get("stage") != event.get("stage")
                    or query_record.get("arm") != event.get("arm")
                ):
                    findings.append(
                        Finding(
                            "TOOL_QUERY_CONTEXT_MISMATCH",
                            "ERROR",
                            f"Tool event {call_id!r} does not match query {query_id}'s agent/stage/arm.",
                            manifest_path.name,
                            line,
                        )
                    )
        event_arm = event.get("arm")
        if (
            mode == "archipelago_lite_shadow"
            or matched_pilot
            or (isinstance(event_arm, str) and event_arm in {"shadow", "matched_baseline"})
        ):
            forbidden = any(
                token == tool or token in tool or token == event_type or token in event_type
                for token in SHADOW_FORBIDDEN_TOOLS
            ) or any(
                marker in event_type
                for marker in ("validator", "evaluation", "advisory", "panel", "pivot")
            )
            if forbidden:
                findings.append(
                    Finding(
                        "SHADOW_VALIDATOR_CALL",
                        "ERROR",
                        f"Non-routing manifest invokes forbidden downstream tool {tool or event_type}; moving the timestamp outside the declared run does not create approval.",
                        manifest_path.name,
                        event.get("_line"),
                    )
                )

    for source_id, source_record in source_by_id.items():
        query_id = source_record.get("query_id")
        source_time = source_times.get(source_id)
        if not isinstance(query_id, str) or source_time is None:
            continue
        later_tool_times = [
            tool_time
            for tool_time in tool_times_by_query.get(query_id, [])
            if tool_time > source_time
        ]
        if later_tool_times:
            findings.append(
                Finding("SOURCE_PRECEDES_QUERY_TOOL", "ERROR", f"Source event {source_id} precedes a tool event for query {query_id}.", manifest_path.name, source_record.get("_line"), (source_id, query_id))
            )

    for finalist in finalist_records:
        finalist_id = finalist.get("finalist_id")
        frozen_at = finalist_times.get(str(finalist_id))
        evidence_ids, evidence_ids_valid = _valid_string_list(finalist.get("evidence_ids"))
        if frozen_at is None or not evidence_ids_valid:
            continue
        for evidence_id in evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            if not isinstance(evidence, dict):
                continue
            source_ids, source_ids_valid = _valid_string_list(evidence.get("source_event_ids"))
            if not source_ids_valid:
                continue
            for source_id in source_ids:
                source_time = source_times.get(source_id)
                if source_time is not None and source_time > frozen_at:
                    findings.append(
                        Finding("FINALIST_SOURCE_AFTER_FREEZE", "ERROR", f"Source event {source_id} supporting finalist {finalist_id} occurred after the finalist froze.", manifest_path.name, source_by_id.get(source_id, {}).get("_line"), (str(finalist_id), evidence_id, source_id))
                    )

    missing_tool_query_links = sorted(set(query_by_id) - tool_linked_query_ids)
    if missing_tool_query_links:
        findings.append(
            Finding(
                "QUERY_TOOL_EVENT_MISSING",
                "ERROR",
                f"Queries lack matching in-window tool events: {missing_tool_query_links}.",
                manifest_path.name,
                node_ids=tuple(missing_tool_query_links),
            )
        )

    shadow_dir = run_dir / "shadow_archipelago_lite"
    allowed_finalist_paths = {
        relative.casefold()
        for record in finalist_records
        for _path, relative in [_canonical_run_path(run_dir, record.get("artifact_path"))]
        if relative is not None
    }
    if shadow_dir.is_dir() and not _relative_is_excluded(
        shadow_dir.relative_to(run_dir), excluded_scope_roots
    ):
        for path in shadow_dir.rglob("finalist_*.md"):
            findings.append(
                Finding(
                    "SHADOW_LIVE_FILENAME_COLLISION",
                    "ERROR",
                    "Shadow artifact matches the live finalist filename pattern.",
                    str(path.relative_to(run_dir)),
                )
            )
    if mode == "archipelago_lite_shadow" or matched_pilot:
        for path in _owned_files(run_dir, excluded_scope_roots):
            if not path.match("finalist_*.md"):
                continue
            findings.append(
                Finding(
                    "NONROUTING_LIVE_FILENAME_COLLISION",
                    "ERROR",
                    "Non-routing diagnostic artifact matches the live finalist filename pattern.",
                    path.name,
                )
            )
        for path in _owned_files(run_dir, excluded_scope_roots):
            if not path.is_file():
                continue
            relative = path.relative_to(run_dir)
            if not _is_downstream_artifact(relative, allowed_finalist_paths=allowed_finalist_paths):
                continue
            findings.append(
                Finding(
                    "NONROUTING_DOWNSTREAM_ARTIFACT",
                    "ERROR",
                    "Non-routing diagnostic contains a forbidden evaluation, pivot, panel, chat, or confirmation artifact.",
                    str(relative),
                )
            )

    if mode == "audited_funnel" and not matched_pilot:
        nonrouting_ids: set[str] = set()
        for nonrouting_dir_name in ("shadow_archipelago_lite", "matched_audited_baseline"):
            nonrouting_dir = run_dir / nonrouting_dir_name
            if not nonrouting_dir.is_dir():
                continue
            nonrouting_ledger = nonrouting_dir / "02b_raw_to_direction_ledger.jsonl"
            if not nonrouting_ledger.is_file():
                findings.append(
                    Finding(
                        "NONROUTING_LEDGER_MISSING",
                        "UNKNOWN",
                        f"Cannot audit cross-arm routing because {nonrouting_dir_name} has no provenance ledger.",
                        str(nonrouting_ledger.relative_to(run_dir)),
                    )
                )
                continue
            nested_findings: list[Finding] = []
            for record in _read_jsonl(nonrouting_ledger, nested_findings):
                if record.get("record_type") == "finalist" and isinstance(record.get("finalist_id"), str):
                    nonrouting_ids.add(record["finalist_id"])
            findings.extend(nested_findings)

        live_generation_contexts: set[str] = set()
        for agent in agent_records:
            if agent.get("arm") != "live" or agent.get("stage") != "generation":
                continue
            context_files = agent.get("context_files")
            if not isinstance(context_files, list):
                continue
            for item in context_files:
                if not isinstance(item, dict):
                    continue
                _path, relative = _canonical_run_path(run_dir, item.get("path"))
                if relative is not None:
                    live_generation_contexts.add(relative)
        excluded_roots = excluded_scope_roots | {
            "shadow_archipelago_lite",
            "matched_audited_baseline",
        }
        for path in _owned_files(run_dir, excluded_roots):
            if not path.is_file() or path.suffix.casefold() not in {".md", ".json", ".jsonl"}:
                continue
            relative = path.relative_to(run_dir)
            if (
                not _is_downstream_artifact(relative, allowed_finalist_paths=allowed_finalist_paths)
                and "regeneration" not in relative.as_posix().casefold()
                and relative.as_posix() not in live_generation_contexts
            ):
                continue
            try:
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError):
                findings.append(
                    Finding(
                        "LIVE_ROUTING_ARTIFACT_UNREADABLE",
                        "UNKNOWN",
                        "Cannot inspect a live downstream artifact for shadow-ID leakage.",
                        str(relative),
                    )
                )
                continue
            leaked_ids = sorted(
                candidate_id
                for candidate_id in nonrouting_ids
                if re.search(
                    rf"(?<![A-Za-z0-9_-]){re.escape(candidate_id)}(?![A-Za-z0-9_-])",
                    text,
                )
            )
            if leaked_ids:
                findings.append(
                    Finding(
                        "NONROUTING_ID_IN_LIVE_ARTIFACT",
                        "ERROR",
                        f"Live downstream artifact contains non-routing finalist IDs: {leaked_ids}.",
                        str(relative),
                        node_ids=tuple(leaked_ids),
                    )
                )

    if checkpoint is not None and not is_v2:
        findings.append(
            Finding(
                "CHECKPOINT_SCHEMA_INVALID",
                "ERROR",
                "Named lifecycle checkpoints are available only for zt1-generation-run-v2.",
                manifest_path.name,
            )
        )
    if is_v2:
        _audit_v2_contract(
            run_dir,
            run_record,
            manifest_records,
            ledger_records,
            findings,
            counts,
            resources,
            strict=strict,
            protection_anchor=protection_anchor,
            protection_anchor_sha256=protection_anchor_sha256,
            child_protection_anchor=child_protection_anchor,
            child_protection_anchor_sha256=child_protection_anchor_sha256,
            freeze_seal=freeze_seal,
            freeze_seal_sha256=freeze_seal_sha256,
            live_arm_freeze_seal=live_arm_freeze_seal,
            live_arm_freeze_seal_sha256=live_arm_freeze_seal_sha256,
            initial_freeze_seal=initial_freeze_seal,
            initial_freeze_seal_sha256=initial_freeze_seal_sha256,
            child_trust_bundle=child_trust_bundle,
            child_trust_bundle_sha256=child_trust_bundle_sha256,
            checkpoint=checkpoint,
            fixed_contract_paths=required_protected_paths,
            scope_stack=_scope_stack,
        )
    elif legacy_profile in {"ordinary_audited_funnel", "operational_live_with_shadow"}:
        closure_file_value = run_record.get("fact_closure_candidates_file")
        if isinstance(closure_file_value, str):
            closure_file = _safe_path(run_dir, closure_file_value)
            if closure_file is not None and closure_file.is_file():
                try:
                    closure_payload = json.loads(closure_file.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, json.JSONDecodeError):
                    closure_payload = None
                if isinstance(closure_payload, dict) and closure_payload.get("creator_agent_id") != "root-orchestrator":
                    findings.append(
                        Finding(
                            "LIVE_SELECTOR_OWNERSHIP_MISMATCH",
                            "ERROR",
                            "Live fact-closure cohort must be owned by the root-orchestrator selection rule.",
                            closure_file.relative_to(run_dir).as_posix(),
                        )
                    )
        legacy_declarations: list[dict[str, Any]] = []
        for relative in sorted(excluded_scope_roots):
            name = Path(relative).name.casefold()
            relationship = (
                "regeneration"
                if "regeneration" in relative.casefold()
                else "shadow_child"
                if name in {"shadow_archipelago_lite", "matched_audited_baseline"}
                else None
            )
            if relationship is not None:
                legacy_declarations.append(
                    {"relative_path": relative, "relationship": relationship}
                )
        _audit_shadow_fingerprint_leaks(
            run_dir,
            ledger_records,
            manifest_records,
            legacy_declarations,
            excluded_scope_roots,
            findings,
            legacy_agent_overlap_is_ambiguous=True,
        )

    if is_v2 and checkpoint is not None:
        checkpoint_boundary = {
            "selection": "level2_complete",
            "freeze": "closure_complete",
            "shadow-dispatch": "frozen",
            "evaluation": "complete",
        }[checkpoint]
        boundary_reached = _v2_state_reached(run_record, checkpoint_boundary)
        has_blocking_finding = any(
            finding.severity in {"ERROR", "UNKNOWN"} for finding in findings
        )
        if boundary_reached and has_blocking_finding:
            findings.append(
                Finding(
                    "CHECKPOINT_BLOCKED",
                    "ERROR",
                    f"Checkpoint {checkpoint} is blocked by the causal findings above.",
                    manifest_path.name,
                )
            )

    findings.sort(key=_finding_sort_key)
    return AuditReport(
        run_id=run_dir.name,
        status=_status(findings, strict),
        findings=findings,
        counts=counts,
        resources=resources,
        adapter="native-v2" if is_v2 else "legacy-v1-conservative-profile",
    )


def _validate_v2_workflow_anchor(
    run_dir: Path,
    run_record: dict[str, Any],
    protection_anchor: dict[str, Any] | None,
    findings: list[Finding],
) -> None:
    if not isinstance(protection_anchor, dict):
        return
    _validate_v2_protection_anchor_fields(protection_anchor, findings)
    if protection_anchor.get("workflow_profile") != WORKFLOW_PROFILE_V2:
        findings.append(
            Finding(
                "WORKFLOW_PROFILE_INVALID",
                "ERROR",
                f"V2 protection anchor must bind workflow profile {WORKFLOW_PROFILE_V2}.",
            )
        )
    if (
        protection_anchor.get("run_id") != run_dir.name
        or protection_anchor.get("scope_id") != run_record.get("scope_id")
        or protection_anchor.get("development_contract_path")
        != "00b_development_contract.json"
        or protection_anchor.get("development_contract_sha256")
        != run_record.get("development_contract_sha256")
    ):
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_DEVELOPMENT_CONTRACT_MISMATCH",
                "ERROR",
                "The V2 pre-run anchor must bind this exact scope and raw development-contract bytes.",
            )
        )
    contract_path = run_dir / "00b_development_contract.json"
    if (
        contract_path.is_symlink()
        or not contract_path.is_file()
        or protection_anchor.get("development_contract_sha256")
        != _sha256(contract_path)
    ):
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_DEVELOPMENT_CONTRACT_HASH_MISMATCH",
                "ERROR",
                "The independently pinned development contract is missing, symlinked, or changed.",
                "00b_development_contract.json",
            )
        )
    entries = protection_anchor.get("workflow_files")
    if not isinstance(entries, list):
        findings.append(
            Finding(
                "WORKFLOW_PROFILE_FILES_INVALID",
                "ERROR",
                "V2 protection anchor must bind the protocol, auditor, matched manager, and isolated development runtime as workflow_files.",
            )
        )
        return
    observed: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            findings.append(Finding("WORKFLOW_PROFILE_FILE_INVALID", "ERROR", "Workflow-file entries must be objects."))
            continue
        workflow_id = item.get("id")
        expected_path = WORKFLOW_PROFILE_FILE_PATHS_V2.get(workflow_id)
        raw_path = item.get("path")
        digest = item.get("sha256")
        if (
            not isinstance(workflow_id, str)
            or expected_path is None
            or workflow_id in observed
            or not isinstance(raw_path, str)
            or raw_path != expected_path
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
        ):
            findings.append(Finding("WORKFLOW_PROFILE_FILE_INVALID", "ERROR", f"Malformed or aliased workflow-file entry {workflow_id!r}."))
            continue
        path = Path(raw_path)
        if _has_symlink_component(path) or _is_within(path, run_dir) or not path.is_file() or _sha256(path) != digest:
            findings.append(Finding("WORKFLOW_PROFILE_FILE_HASH_MISMATCH", "ERROR", f"Workflow file {workflow_id} is missing, symlinked, in-run, or changed from its pin.", raw_path))
        observed.add(workflow_id)
    if observed != set(WORKFLOW_PROFILE_FILE_PATHS_V2):
        findings.append(
            Finding(
                "WORKFLOW_PROFILE_FILE_SET_INCOMPLETE",
                "ERROR",
                f"Workflow profile must bind exactly {sorted(WORKFLOW_PROFILE_FILE_PATHS_V2)}.",
            )
        )


def _validate_v2_prefreeze_anchor(
    run_dir: Path,
    run_record: dict[str, Any],
    protection_anchor: dict[str, Any] | None,
    protection_anchor_sha256: str | None,
    fixed_contract_paths: dict[str, str],
    findings: list[Finding],
) -> None:
    if not isinstance(protection_anchor, dict) or not isinstance(protection_anchor_sha256, str):
        return
    if (
        not re.fullmatch(r"[0-9a-f]{64}", protection_anchor_sha256)
        or _json_payload_sha256(protection_anchor) != protection_anchor_sha256
        or protection_anchor.get("schema") != PROTECTION_ANCHOR_SCHEMA_V2
        or protection_anchor.get("contract_profile") != CONTRACT_PROFILE
        or protection_anchor.get("run_id") != run_dir.name
        or protection_anchor.get("run_dir") != str(run_dir)
    ):
        findings.append(Finding("PROTECTION_ANCHOR_PREFREEZE_INVALID", "ERROR", "Pre-freeze V2 protection anchor has an invalid pin, schema, profile, or run identity."))
        return
    anchor_time = _parse_timestamp(protection_anchor.get("created_at"))
    run_start = _parse_timestamp(run_record.get("started_at"))
    if anchor_time is None or run_start is None or anchor_time > run_start:
        findings.append(Finding("PROTECTION_ANCHOR_TIME_INVALID", "ERROR", "Pre-freeze V2 protection anchor must precede run start."))
    anchor_files = protection_anchor.get("files")
    observed_files: dict[str, dict[str, Any]] = {}
    if isinstance(anchor_files, list):
        observed_files = {
            item.get("id"): item
            for item in anchor_files
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
    if set(observed_files) != set(fixed_contract_paths):
        findings.append(Finding("PROTECTION_ANCHOR_FILE_SET_INCOMPLETE", "ERROR", "Pre-freeze anchor omits fixed-v1 contracts."))
    else:
        for contract_id, expected_path in fixed_contract_paths.items():
            item = observed_files[contract_id]
            path = Path(expected_path)
            if (
                item.get("path") != str(path.resolve(strict=False))
                or _has_symlink_component(path)
                or not path.is_file()
                or item.get("sha256") != _sha256(path)
            ):
                findings.append(Finding("PROTECTION_ANCHOR_FILE_INVALID", "ERROR", f"Pre-freeze anchor fixed contract {contract_id} is not canonical and hash-bound."))
    anchor_blocks = protection_anchor.get("blocks")
    expected_block_ids = set(REQUIRED_PROTECTED_BLOCK_IDS)
    observed_block_ids = {
        item.get("id")
        for item in anchor_blocks
        if isinstance(anchor_blocks, list) and isinstance(item, dict)
    } if isinstance(anchor_blocks, list) else set()
    if observed_block_ids != expected_block_ids:
        findings.append(Finding("PROTECTION_ANCHOR_BLOCK_SET_INCOMPLETE", "ERROR", "Pre-freeze anchor omits the fixed validation block."))
    elif isinstance(anchor_blocks, list):
        for item in anchor_blocks:
            block_id = item.get("id")
            expected_markers = REQUIRED_PROTECTED_BLOCK_IDS.get(block_id)
            block_path = Path(str(item.get("path")))
            if (
                expected_markers is None
                or (item.get("start_marker"), item.get("end_marker")) != expected_markers
                or _has_symlink_component(block_path)
                or block_path != Path(fixed_contract_paths["orchestration-prompt"]).resolve(strict=False)
                or item.get("sha256") != _marker_block_sha256(block_path, *expected_markers)
            ):
                findings.append(Finding("PROTECTION_ANCHOR_BLOCK_INVALID", "ERROR", f"Pre-freeze anchor block {block_id!r} is not the exact protected validation block."))


def _validate_v2_development_contract(
    run_dir: Path,
    run_record: dict[str, Any],
    excluded_roots: set[str],
    findings: list[Finding],
    manifest_name: str,
) -> dict[str, Any] | None:
    path_value = run_record.get("development_contract_path")
    if path_value != "00b_development_contract.json":
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_PATH_INVALID",
                "ERROR",
                "V2 runs must bind the exact run-local path 00b_development_contract.json.",
                manifest_name,
                run_record.get("_line"),
            )
        )
        return None
    parsed_path = _strict_run_file(run_dir, path_value, excluded_roots)
    if parsed_path is None:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_PATH_INVALID",
                "ERROR",
                "The development contract must be a regular non-symlink file owned by this scope.",
                str(path_value),
            )
        )
        return None
    path, relative = parsed_path
    expected_digest = run_record.get("development_contract_sha256")
    observed_digest = _sha256(path)
    if (
        not isinstance(expected_digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", expected_digest)
        or expected_digest != observed_digest
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_MISMATCH",
                "ERROR",
                "The raw-byte development-contract digest does not match the run record.",
                relative,
            )
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_INVALID",
                "ERROR",
                f"Development contract is not valid UTF-8 JSON: {exc}.",
                relative,
            )
        )
        return None
    if not isinstance(payload, dict) or payload.get("schema") != DEVELOPMENT_CONTRACT_SCHEMA_V2:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_INVALID",
                "ERROR",
                f"Development contract must use schema {DEVELOPMENT_CONTRACT_SCHEMA_V2}.",
                relative,
            )
        )
        return None
    if set(payload) != DEVELOPMENT_CONTRACT_FIELDS_V2:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "The V2 development contract must use the exact closed top-level field set; aliases and extra fields are invalid.",
                relative,
            )
        )

    matched_initial = (
        run_record.get("cohort_kind") == "initial"
        and run_record.get("run_profile")
        in {"operational_live_with_shadow", "v2_matched_nonrouting"}
    )
    discovery_complete = _v2_state_reached(
        run_record,
        "problem_cards_frozen"
        if run_record.get("mode") == "archipelago_lite_shadow"
        else "raw_frozen",
    )
    level2_complete = _v2_state_reached(run_record, "level2_complete")
    closure_cohort_sealed = _v2_state_reached(
        run_record, "fact_closure_cohort_sealed"
    )
    closure_complete = _v2_state_reached(run_record, "closure_complete")
    frozen_reached = _v2_state_reached(run_record, "frozen")
    if matched_initial and payload.get("contract_id") != "matched-development-v2":
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_ID_INVALID",
                "ERROR",
                "Matched initial arms must use contract_id matched-development-v2.",
                relative,
            )
        )
    elif not matched_initial and payload.get("contract_id") != "ordinary-development-v2":
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_ID_INVALID",
                "ERROR",
                "Ordinary initial and regeneration scopes must use contract_id ordinary-development-v2.",
                relative,
            )
        )
    aggregate = payload.get("aggregate_opportunity")
    if matched_initial and not _typed_value_equal(
        aggregate, MATCHED_AGGREGATE_OPPORTUNITY
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_OPPORTUNITY_INVALID",
                "ERROR",
                "Matched initial arms must bind the exact 48/12/6/6 and 108/144/48/300 opportunity.",
                relative,
            )
        )
    elif not matched_initial:
        aggregate_valid = (
            isinstance(aggregate, dict)
            and set(aggregate) == AGGREGATE_OPPORTUNITY_FIELDS_V2
            and all(
                isinstance(aggregate.get(key), int)
                and not isinstance(aggregate.get(key), bool)
                and aggregate[key] >= 0
                for key in AGGREGATE_OPPORTUNITY_FIELDS_V2
            )
        )
        if aggregate_valid:
            aggregate_valid = (
                40 <= aggregate["raw"] <= 60
                and 10 <= aggregate["level2"] <= 20
                and 3 <= aggregate["fact_closure"] <= 6
                and aggregate["frozen"] == aggregate["fact_closure"]
                and aggregate["level2_queries"] == aggregate["level2"] * 12
                and aggregate["fact_closure_queries"]
                == aggregate["fact_closure"] * 8
                and aggregate["total_queries"]
                == aggregate["discovery_queries"]
                + aggregate["level2_queries"]
                + aggregate["fact_closure_queries"]
            )
        if not aggregate_valid:
            findings.append(
                Finding(
                    "DEVELOPMENT_CONTRACT_OPPORTUNITY_INVALID",
                    "ERROR",
                    "Ordinary opportunity must use the exact eight integer fields, stay within 40-60/10-20/3-6 ranges, and reconcile stage query capacities.",
                    relative,
                )
            )

    stage_caps = payload.get("stage_query_caps")
    if not _typed_value_equal(stage_caps, {"level2": 12, "fact_closure": 8}):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_CAP_INVALID",
                "ERROR",
                "stage_query_caps must be exactly level2=12 and fact_closure=8.",
                relative,
            )
        )
    candidate_budgets = payload.get("candidate_budgets")
    budget_keys = {
        "uncached_input_tokens",
        "output_tokens",
        "elapsed_minutes",
    }
    budgets_valid = (
        isinstance(candidate_budgets, dict)
        and set(candidate_budgets) == {"level2", "fact_closure"}
    )
    if budgets_valid:
        for stage in ("level2", "fact_closure"):
            stage_budget = candidate_budgets.get(stage)
            if (
                not isinstance(stage_budget, dict)
                or set(stage_budget) != budget_keys
                or any(
                    not isinstance(stage_budget.get(key), int)
                    or isinstance(stage_budget.get(key), bool)
                    or stage_budget[key] < 0
                    for key in budget_keys
                )
            ):
                budgets_valid = False
                break
    if not budgets_valid:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_CAP_INVALID",
                "ERROR",
                "candidate_budgets must contain exact nonnegative uncached_input_tokens, output_tokens, and elapsed_minutes caps for level2 and fact_closure.",
                relative,
            )
        )
    elif matched_initial and not _typed_value_equal(
        candidate_budgets, MATCHED_CANDIDATE_BUDGETS
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_CAP_INVALID",
                "ERROR",
                "Matched candidate budgets must use the calibrated 112k/20k/15m Level-2 and 96k/20k/12m closure hard caps.",
                relative,
            )
        )
    live_thresholds = payload.get("candidate_live_stop_thresholds")
    monitor = payload.get("metering_monitor")
    if (
        matched_initial
        and (
            not _typed_value_equal(
                live_thresholds, MATCHED_CANDIDATE_LIVE_STOP_THRESHOLDS
            )
            or not _typed_value_equal(monitor, MATCHED_METERING_MONITOR)
        )
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_LIVE_METERING_CONTRACT_INVALID",
                "ERROR",
                "Matched development must bind the calibrated one-second live-stop thresholds and empirical provider-event reserves.",
                relative,
            )
        )
    elif not matched_initial and (
        not isinstance(live_thresholds, dict) or not isinstance(monitor, dict)
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_LIVE_METERING_CONTRACT_INVALID",
                "ERROR",
                "Development contract lacks typed live-stop thresholds or metering-monitor policy.",
                relative,
            )
        )

    for field in ("level2_sections", "frozen_sections"):
        values, valid = _valid_string_list(payload.get(field))
        if not valid or tuple(values) != REQUIRED_LEVEL2_SECTIONS:
            findings.append(
                Finding(
                    "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                    "ERROR",
                    f"{field} must use the exact neutral nine-section dossier inventory.",
                    relative,
                )
            )
    evidence_statuses, statuses_valid = _valid_string_list(
        payload.get("evidence_statuses")
    )
    if not statuses_valid or set(evidence_statuses) != ALLOWED_EVIDENCE_STATUSES:
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "evidence_statuses must be exactly the complete typed evidence taxonomy.",
                relative,
            )
        )
    prose_ranges = payload.get("dossier_prose_word_ranges")
    prose_ranges_valid = (
        isinstance(prose_ranges, dict)
        and set(prose_ranges) == {"level2", "frozen"}
    )
    if prose_ranges_valid:
        for stage in ("level2", "frozen"):
            value = prose_ranges.get(stage)
            minimum = value.get("minimum") if isinstance(value, dict) else None
            maximum = value.get("maximum") if isinstance(value, dict) else None
            minimum_per_section = (
                value.get("minimum_per_section")
                if isinstance(value, dict)
                else None
            )
            if (
                not isinstance(value, dict)
                or set(value)
                != {"minimum", "maximum", "minimum_per_section"}
                or not _is_nonnegative_int(minimum)
                or not _is_nonnegative_int(maximum)
                or not _is_nonnegative_int(minimum_per_section)
                or minimum_per_section <= 0
                or minimum > maximum
            ):
                prose_ranges_valid = False
                break
    if not prose_ranges_valid or (
        matched_initial
        and not _typed_value_equal(
            prose_ranges, MATCHED_DOSSIER_PROSE_WORD_RANGES
        )
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "dossier_prose_word_ranges must bind the calibrated stage totals and neutral per-section depth floors.",
                relative,
            )
        )
    if not _typed_value_equal(
        payload.get("dossier_measurement"), DOSSIER_MEASUREMENT_CONTRACT
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "dossier_measurement must exclude sources, trace material, telemetry, and machine metadata from persuasive prose.",
                relative,
            )
        )
    if not _typed_value_equal(
        payload.get("fact_closure_schema"),
        {
            "requires_decision_critical_evidence": True,
            "requires_pre_freeze_source_chain": True,
            "replacement_after_closure": False,
        },
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "fact_closure_schema must be explicitly bound.",
                relative,
            )
        )
    if not _typed_value_equal(
        payload.get("query_source_opportunity"),
        {
            "query_requires_tool_event": True,
            "query_requires_source_open": True,
            "source_requires_bidirectional_evidence": True,
        },
    ):
        findings.append(
            Finding(
                "DEVELOPMENT_CONTRACT_SCHEMA_INVALID",
                "ERROR",
                "query_source_opportunity must explicitly bind the matched research opportunity.",
                relative,
            )
        )
    return payload


def _audit_v2_state_chain(
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    run_dir: Path,
    excluded_roots: set[str],
    findings: list[Finding],
    checkpoint: str | None,
    *,
    allow_prefix: bool = False,
) -> None:
    manifest_name = "00a_context_and_resource_manifest.jsonl"
    mode = run_record.get("mode")
    chain = SHADOW_STATE_CHAIN_V2 if mode == "archipelago_lite_shadow" else LIVE_STATE_CHAIN_V2
    records = [
        record
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
    ]
    if not records:
        findings.append(
            Finding(
                "STAGE_BOUNDARY_LOG_MISSING",
                "UNKNOWN",
                "V2 lifecycle state cannot be certified without append-only checkpoint records.",
                manifest_name,
            )
        )
        return
    agent_by_id = {
        record.get("agent_id"): record
        for record in manifest_records
        if record.get("record_type") == "agent"
        and isinstance(record.get("agent_id"), str)
    }
    allocations_by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for allocation in manifest_records:
        if allocation.get("record_type") != "allocation":
            continue
        allocation_agent_id = allocation.get("agent_id")
        if isinstance(allocation_agent_id, str):
            allocations_by_agent[allocation_agent_id].append(allocation)
    seen_ids: set[str] = set()
    observed_states: list[str] = []
    previous_id: str | None = None
    previous_time: datetime | None = None
    previous_totals: dict[str, Decimal] | None = None
    checkpoint_times: dict[str, datetime] = {}
    for index, record in enumerate(records):
        checkpoint_id = record.get("checkpoint_id")
        state = record.get("state")
        line = record.get("_line")
        if set(record) - {"_line"} != V2_CHECKPOINT_FIELDS:
            findings.append(
                Finding(
                    "STAGE_BOUNDARY_FIELDS_INVALID",
                    "ERROR",
                    f"Checkpoint {checkpoint_id!r} must use the exact closed checkpoint schema.",
                    manifest_name,
                    line,
                )
            )
        if not isinstance(checkpoint_id, str) or not checkpoint_id.strip():
            findings.append(
                Finding("STAGE_BOUNDARY_ID_INVALID", "ERROR", "Checkpoint has no stable checkpoint_id.", manifest_name, line)
            )
            continue
        if checkpoint_id in seen_ids:
            findings.append(
                Finding("STAGE_BOUNDARY_ID_DUPLICATE", "ERROR", f"Checkpoint ID {checkpoint_id} is duplicated.", manifest_name, line, (checkpoint_id,))
            )
        seen_ids.add(checkpoint_id)
        if state not in chain:
            findings.append(
                Finding("STAGE_BOUNDARY_STATE_INVALID", "ERROR", f"Checkpoint {checkpoint_id} uses unsupported state {state!r}.", manifest_name, line, (checkpoint_id,))
            )
        else:
            observed_states.append(state)
        expected_predecessor = previous_id
        actual_predecessor = record.get("predecessor_id")
        if (index == 0 and actual_predecessor not in (None, "")) or (
            index > 0 and actual_predecessor != expected_predecessor
        ):
            findings.append(
                Finding("STAGE_BOUNDARY_PREDECESSOR_INVALID", "ERROR", f"Checkpoint {checkpoint_id} does not name the immediately preceding checkpoint.", manifest_name, line, (checkpoint_id,))
            )
        occurred_at = _parse_timestamp(record.get("occurred_at"))
        if occurred_at is None:
            findings.append(
                Finding("STAGE_BOUNDARY_TIME_UNKNOWN", "UNKNOWN", f"Checkpoint {checkpoint_id} lacks an offset-aware occurred_at timestamp.", manifest_name, line, (checkpoint_id,))
            )
        else:
            checkpoint_times[str(state)] = occurred_at
            if previous_time is not None and occurred_at <= previous_time:
                findings.append(
                    Finding("STAGE_BOUNDARY_ORDER_INVALID", "ERROR", f"Checkpoint {checkpoint_id} is not strictly later than its predecessor.", manifest_name, line, (checkpoint_id,))
                )
        completed_agent_ids, completed_valid = _valid_string_list(
            record.get("completed_agent_ids"), allow_empty=(state == "registered")
        )
        if not completed_valid:
            findings.append(
                Finding("STAGE_BOUNDARY_AGENT_SET_INVALID", "ERROR", f"Checkpoint {checkpoint_id} has no typed completed_agent_ids inventory.", manifest_name, line, (checkpoint_id,))
            )
            completed_agent_ids = []
        if len(completed_agent_ids) != len(set(completed_agent_ids)):
            findings.append(
                Finding(
                    "STAGE_BOUNDARY_AGENT_SET_INVALID",
                    "ERROR",
                    f"Checkpoint {checkpoint_id} repeats completed_agent_ids.",
                    manifest_name,
                    line,
                    (checkpoint_id,),
                )
            )
        if occurred_at is not None:
            expected_completed = {
                agent_id
                for agent_id, agent in agent_by_id.items()
                if (
                    (agent_end := _parse_timestamp(agent.get("ended_at")))
                    is not None
                    and agent_end < occurred_at
                )
            }
            if set(completed_agent_ids) != expected_completed:
                findings.append(
                    Finding(
                        "STAGE_BOUNDARY_AGENT_SET_MISMATCH",
                        "ERROR",
                        f"Checkpoint {checkpoint_id} must list every and only agent completed before the boundary.",
                        manifest_name,
                        line,
                        (checkpoint_id,),
                    )
                )
        for agent_id in completed_agent_ids:
            agent = agent_by_id.get(agent_id)
            agent_end = _parse_timestamp(agent.get("ended_at")) if isinstance(agent, dict) else None
            if agent is None or occurred_at is None or agent_end is None or agent_end >= occurred_at:
                findings.append(
                    Finding("STAGE_BOUNDARY_AGENT_TIMING_INVALID", "ERROR", f"Checkpoint {checkpoint_id} does not strictly follow completed agent {agent_id}.", manifest_name, line, (checkpoint_id, agent_id))
                )
        if (
            record.get("file_read_log_complete") is not True
            or record.get("tool_event_log_complete") is not True
        ):
            findings.append(
                Finding(
                    "STAGE_BOUNDARY_COMPLETENESS_UNKNOWN",
                    "UNKNOWN",
                    f"Checkpoint {checkpoint_id} must explicitly attest complete file-read and tool-event logs through the boundary.",
                    manifest_name,
                    line,
                    (checkpoint_id,),
                )
            )
        boundary_totals = record.get("resource_totals")
        if not isinstance(boundary_totals, dict) or set(boundary_totals) != V2_CHECKPOINT_RESOURCE_FIELDS:
            findings.append(
                Finding(
                    "STAGE_BOUNDARY_RESOURCE_FIELDS_INVALID",
                    "ERROR",
                    f"Checkpoint {checkpoint_id} resource_totals must use the exact closed key set.",
                    manifest_name,
                    line,
                    (checkpoint_id,),
                )
            )
        parsed_totals: dict[str, Decimal] = {}
        for key in (
            "unique_queries",
            "uncached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
        ):
            raw_total = boundary_totals.get(key) if isinstance(boundary_totals, dict) else None
            parsed = (
                _as_decimal(raw_total)
                if isinstance(raw_total, int) and not isinstance(raw_total, bool)
                else None
            )
            if parsed is None:
                findings.append(
                    Finding(
                        "STAGE_BOUNDARY_RESOURCE_TOTALS_INVALID",
                        "ERROR",
                        f"Checkpoint {checkpoint_id} lacks finite nonnegative incremental total {key}.",
                        manifest_name,
                        line,
                        (checkpoint_id,),
                    )
                )
            else:
                parsed_totals[key] = parsed
                if previous_totals is not None and parsed < previous_totals.get(key, Decimal("0")):
                    findings.append(
                        Finding(
                            "STAGE_BOUNDARY_RESOURCE_TOTALS_DECREASED",
                            "ERROR",
                            f"Checkpoint {checkpoint_id} decreases cumulative resource total {key}.",
                            manifest_name,
                            line,
                            (checkpoint_id,),
                        )
                    )
        if len(parsed_totals) == 4:
            previous_totals = parsed_totals
        if occurred_at is not None and len(parsed_totals) == 4:
            query_count = len(
                {
                    _normalize_query(item.get("query"))
                    for item in manifest_records
                    if item.get("record_type") == "query"
                    and _normalize_query(item.get("query"))
                    and (
                        (query_time := _parse_timestamp(item.get("occurred_at")))
                        is not None
                        and query_time <= occurred_at
                    )
                }
            )
            completed_agents = [
                item
                for item in agent_by_id.values()
                if (
                    (agent_end := _parse_timestamp(item.get("ended_at")))
                    is not None
                    and agent_end < occurred_at
                )
            ]
            token_totals: dict[str, int] = {
                "uncached_input_tokens": 0,
                "output_tokens": 0,
            }
            checkpoint_metering_certified = True
            for item in completed_agents:
                agent_id = item.get("agent_id")
                owned_allocations = allocations_by_agent.get(str(agent_id), [])
                if (
                    item.get("metering_basis") not in EXACT_METERING_BASES
                    or (
                        item.get("stage") in ALLOCATION_STAGES
                        and not owned_allocations
                    )
                ):
                    checkpoint_metering_certified = False
                for allocation in owned_allocations:
                    allocation_resources = allocation.get("resources")
                    if (
                        allocation.get("metering_basis") not in EXACT_METERING_BASES
                        or not isinstance(allocation_resources, dict)
                    ):
                        checkpoint_metering_certified = False
                        continue
                    for key in token_totals:
                        value = allocation_resources.get(key)
                        if (
                            not isinstance(value, int)
                            or isinstance(value, bool)
                            or value < 0
                        ):
                            checkpoint_metering_certified = False
                        else:
                            token_totals[key] += value
            for key in ("uncached_input_tokens", "output_tokens"):
                values = [
                    item.get("resources", {}).get(key)
                    if isinstance(item.get("resources"), dict)
                    else None
                    for item in completed_agents
                ]
                if not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in values):
                    checkpoint_metering_certified = False
                elif checkpoint_metering_certified and token_totals[key] != sum(values):
                    findings.append(
                        Finding(
                            "STAGE_BOUNDARY_RESOURCE_TOTALS_MISMATCH",
                            "ERROR",
                            f"Checkpoint {checkpoint_id} allocation {key} does not reconcile to completed agents.",
                            manifest_name,
                            line,
                            (checkpoint_id,),
                        )
                    )
            run_start = _parse_timestamp(run_record.get("started_at"))
            expected_elapsed = (
                _elapsed_microseconds(run_start, occurred_at)
                if run_start is not None and occurred_at >= run_start
                else None
            )
            base_reconciled = (
                parsed_totals["unique_queries"] == Decimal(query_count)
                and expected_elapsed is not None
                and parsed_totals["elapsed_microseconds"]
                == Decimal(expected_elapsed)
            )
            if not base_reconciled:
                findings.append(
                    Finding(
                        "STAGE_BOUNDARY_RESOURCE_TOTALS_MISMATCH",
                        "ERROR",
                        f"Checkpoint {checkpoint_id} query or elapsed totals do not reconcile through occurred_at.",
                        manifest_name,
                        line,
                        (checkpoint_id,),
                    )
                )
            if not checkpoint_metering_certified:
                findings.append(
                    Finding(
                        "STAGE_BOUNDARY_RESOURCE_TOTALS_UNCERTIFIED",
                        "UNKNOWN",
                        f"Checkpoint {checkpoint_id} token totals cannot be certified until every completed agent has an exact metering basis and resource record.",
                        manifest_name,
                        line,
                        (checkpoint_id,),
                    )
                )
            elif any(
                parsed_totals[key] != Decimal(value)
                for key, value in token_totals.items()
            ):
                findings.append(
                    Finding(
                        "STAGE_BOUNDARY_RESOURCE_TOTALS_MISMATCH",
                        "ERROR",
                        f"Checkpoint {checkpoint_id} token totals do not reconcile with complete certified telemetry through occurred_at.",
                        manifest_name,
                        line,
                        (checkpoint_id,),
                    )
                )

        artifacts = record.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            findings.append(
                Finding("STAGE_BOUNDARY_ARTIFACTS_MISSING", "ERROR", f"Checkpoint {checkpoint_id} must bind at least one owned artifact.", manifest_name, line, (checkpoint_id,))
            )
        elif isinstance(artifacts, list):
            for item in artifacts:
                if not isinstance(item, dict):
                    findings.append(Finding("STAGE_BOUNDARY_ARTIFACT_INVALID", "ERROR", f"Checkpoint {checkpoint_id} has a malformed artifact binding.", manifest_name, line, (checkpoint_id,)))
                    continue
                if set(item) != {"path", "sha256"}:
                    findings.append(Finding("STAGE_BOUNDARY_ARTIFACT_INVALID", "ERROR", f"Checkpoint {checkpoint_id} artifact bindings use exact path/sha256 keys.", manifest_name, line, (checkpoint_id,)))
                parsed = _strict_run_file(run_dir, item.get("path"), excluded_roots)
                if parsed is None or item.get("sha256") != _sha256(parsed[0]):
                    findings.append(
                        Finding("STAGE_BOUNDARY_ARTIFACT_INVALID", "ERROR", f"Checkpoint {checkpoint_id} has a missing, escaping, symlinked, child-owned, or hash-mismatched artifact.", manifest_name, line, (checkpoint_id,))
                    )
            if state == "registered":
                registered_paths = {
                    item.get("path")
                    for item in artifacts
                    if isinstance(item, dict) and isinstance(item.get("path"), str)
                }
                if not {"00_run_manifest.md", "00b_development_contract.json"}.issubset(registered_paths):
                    findings.append(
                        Finding(
                            "REGISTRATION_BINDINGS_INCOMPLETE",
                            "ERROR",
                            "Registration must bind both the run manifest and development contract.",
                            manifest_name,
                            line,
                            (checkpoint_id,),
                        )
                    )
        previous_id = checkpoint_id
        if occurred_at is not None:
            previous_time = occurred_at

    expected_prefix = list(chain[: len(observed_states)])
    if observed_states != expected_prefix:
        findings.append(
            Finding(
                "STAGE_BOUNDARY_SEQUENCE_INVALID",
                "ERROR",
                f"Checkpoint states must be the exact workflow prefix; expected {expected_prefix}, found {observed_states}.",
                manifest_name,
            )
        )
    lifecycle_state = run_record.get("lifecycle_state")
    if not observed_states or lifecycle_state != observed_states[-1]:
        findings.append(
            Finding(
                "LIFECYCLE_STATE_MISMATCH",
                "ERROR",
                "lifecycle_state must equal the final append-only checkpoint state.",
                manifest_name,
                run_record.get("_line"),
            )
        )

    stage_boundary_states = {
        "generation": "raw_frozen",
        "problem_discovery": "problem_cards_frozen",
        "direct_concept": "direct_concepts_frozen",
        "inversion": "transformations_frozen",
        "recombination": "transformations_frozen",
        "history_compressor": (
            "mapped"
            if mode == "archipelago_lite_shadow"
            else "history_frozen"
        ),
        "cartography": "mapped",
        "cluster_audit": (
            "level1_frozen"
            if mode == "archipelago_lite_shadow"
            else "cluster_audited"
        ),
        "level1": (
            "level1_frozen"
            if mode == "archipelago_lite_shadow"
            else "level2_cohort_sealed"
        ),
        "provisional_selector": "provisional_order_sealed",
        "selector": "ballots_sealed",
        "tail_challenger": "ballots_sealed",
        "level2": "level2_complete",
        "finalist_selector": "fact_closure_cohort_sealed",
        "fact_closure": "closure_complete",
    }
    for agent_id, agent in agent_by_id.items():
        boundary_state = stage_boundary_states.get(str(agent.get("stage")))
        boundary_time = checkpoint_times.get(str(boundary_state))
        end = _parse_timestamp(agent.get("ended_at"))
        if boundary_state in observed_states and (
            boundary_time is None or end is None or end >= boundary_time
        ):
            findings.append(
                Finding(
                    "STAGE_BOUNDARY_AGENT_TIMING_INVALID",
                    "ERROR",
                    f"Stage agent {agent_id} did not end strictly before {boundary_state}.",
                    manifest_name,
                    agent.get("_line"),
                    (str(agent_id),),
                )
            )

    dependency_groups = (
        (
            (
                ({"problem_discovery"}, {"direct_concept", "history_compressor"}),
                ({"direct_concept"}, {"inversion", "recombination"}),
                ({"inversion", "recombination"}, {"cartography"}),
                ({"history_compressor"}, {"cartography"}),
                ({"cartography"}, {"cluster_audit"}),
                ({"cluster_audit"}, {"level1"}),
                ({"level1"}, {"provisional_selector"}),
                ({"provisional_selector"}, {"selector", "tail_challenger"}),
                ({"selector", "tail_challenger"}, {"level2"}),
                ({"level2"}, {"finalist_selector"}),
                ({"finalist_selector"}, {"fact_closure"}),
            )
            if mode == "archipelago_lite_shadow"
            else (
                ({"generation"}, {"history_compressor"}),
                ({"history_compressor"}, {"cartography"}),
                ({"cartography"}, {"cluster_audit"}),
                ({"cluster_audit"}, {"level1"}),
                ({"level1"}, {"level2"}),
                ({"level2"}, {"fact_closure"}),
            )
        )
    )
    for predecessor_stages, successor_stages in dependency_groups:
        predecessor_ends = [
            _parse_timestamp(agent.get("ended_at"))
            for agent in agent_by_id.values()
            if agent.get("stage") in predecessor_stages
        ]
        successor_starts = [
            _parse_timestamp(agent.get("started_at"))
            for agent in agent_by_id.values()
            if agent.get("stage") in successor_stages
        ]
        if predecessor_ends and successor_starts and (
            any(value is None for value in predecessor_ends + successor_starts)
            or max(value for value in predecessor_ends if value is not None)
            >= min(value for value in successor_starts if value is not None)
        ):
            findings.append(
                Finding(
                    "V2_STAGE_DEPENDENCY_INVALID",
                    "ERROR",
                    f"Stages {sorted(successor_stages)} must start strictly after all {sorted(predecessor_stages)} agents finish.",
                    manifest_name,
                )
            )

    if checkpoint is None:
        if lifecycle_state != "complete" and not allow_prefix:
            findings.append(
                Finding("LIFECYCLE_INCOMPLETE", "UNKNOWN", "A final V2 audit requires lifecycle_state=complete.", manifest_name, run_record.get("_line"))
            )
        return
    required_state = {
        "selection": "level2_complete",
        "freeze": "closure_complete",
        "shadow-dispatch": "frozen",
        "evaluation": "complete",
    }[checkpoint]
    stopped_at_admission = (
        run_record.get("ended_at") is not None
        and isinstance(run_record.get("failure_receipt_path"), str)
        and isinstance(run_record.get("failure_receipt_sha256"), str)
    )
    if required_state not in observed_states and not stopped_at_admission:
        findings.append(
            Finding(
                "CHECKPOINT_STATE_NOT_REACHED",
                "ERROR",
                f"Checkpoint {checkpoint} requires lifecycle boundary {required_state}.",
                manifest_name,
            )
        )
    if checkpoint == "evaluation" and run_record.get("routing_state") != "enabled":
        findings.append(
            Finding("NONROUTING_EVALUATION_FORBIDDEN", "ERROR", "A frozen_nonrouting scope cannot cross the evaluation checkpoint.", manifest_name)
        )


def _audit_v2_development_failure_receipt(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    excluded_roots: set[str],
    findings: list[Finding],
) -> None:
    raw_path = run_record.get("failure_receipt_path")
    raw_digest = run_record.get("failure_receipt_sha256")
    if raw_path is None and raw_digest is None:
        return
    parsed = _strict_run_file(run_dir, raw_path, excluded_roots)
    if (
        parsed is None
        or not isinstance(raw_digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", raw_digest)
        or _sha256(parsed[0]) != raw_digest
    ):
        findings.append(Finding("DEVELOPMENT_FAILURE_RECEIPT_INVALID", "ERROR", "Development failure receipt is missing, unsafe, or differs from its manifest hash binding.", str(raw_path or "")))
        return
    try:
        receipt = json.loads(parsed[0].read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        receipt = None
    expected_fields = {
        "schema",
        "run_id",
        "scope_id",
        "stage",
        "primary_cause",
        "stopped_at",
        "last_reached_checkpoint",
        "pre_stage_manifest",
        "pre_stage_ledger",
        "preserved_evidence",
        "causal_traces",
        "materialized_stage_artifacts",
        "future_lifecycle_artifacts",
        "telemetry_reconstruction_performed",
    }
    if not isinstance(receipt, dict) or set(receipt) != expected_fields:
        findings.append(Finding("DEVELOPMENT_FAILURE_RECEIPT_INVALID", "ERROR", "Development failure receipt violates its exact closed schema.", parsed[1]))
        return
    stage = receipt.get("stage")
    expected_checkpoint = {
        "level2": "level2_cohort_sealed",
        "fact_closure": "fact_closure_cohort_sealed",
    }.get(stage)
    checkpoints = [record for record in manifest_records if record.get("record_type") == "checkpoint"]
    stopped_at = _parse_timestamp(receipt.get("stopped_at"))
    ended_at = _parse_timestamp(run_record.get("ended_at"))
    identity_invalid = (
        receipt.get("schema") != "zt1-development-admission-failure-v2"
        or receipt.get("run_id") != run_record.get("run_id")
        or receipt.get("scope_id") != run_record.get("scope_id")
        or expected_checkpoint is None
        or receipt.get("last_reached_checkpoint") != expected_checkpoint
        or run_record.get("lifecycle_state") != expected_checkpoint
        or not checkpoints
        or checkpoints[-1].get("state") != expected_checkpoint
        or stopped_at is None
        or ended_at is None
        or stopped_at != ended_at
        or receipt.get("telemetry_reconstruction_performed") is not False
    )
    primary = receipt.get("primary_cause")
    if (
        not isinstance(primary, dict)
        or set(primary) != {"code", "exception_type", "message"}
        or any(not isinstance(primary.get(key), str) or not primary[key].strip() for key in primary)
    ):
        identity_invalid = True
    if identity_invalid:
        findings.append(Finding("DEVELOPMENT_FAILURE_RECEIPT_INVALID", "ERROR", "Development failure receipt does not match the actual stopped lifecycle, timestamp, or typed primary cause.", parsed[1]))
        return

    def bound_file(item: Any) -> tuple[Path, str] | None:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            return None
        candidate = _strict_run_file(run_dir, item.get("path"), excluded_roots)
        digest = item.get("sha256")
        if candidate is None or not isinstance(digest, str) or digest != _sha256(candidate[0]):
            return None
        return candidate

    pre_manifest = bound_file(receipt.get("pre_stage_manifest"))
    pre_ledger = bound_file(receipt.get("pre_stage_ledger"))
    if pre_manifest is None or pre_ledger is None:
        findings.append(Finding("DEVELOPMENT_FAILURE_BASELINE_INVALID", "ERROR", "Failure receipt lacks hash-bound pre-stage manifest/ledger bytes.", parsed[1]))
    else:
        snapshot_findings: list[Finding] = []
        snapshot_records = _read_jsonl(pre_manifest[0], snapshot_findings)
        snapshot_runs = [item for item in snapshot_records if item.get("record_type") == "run"]
        if (
            snapshot_findings
            or len(snapshot_runs) != 1
            or _v2_immutable_run_view(snapshot_runs[0]) != _v2_immutable_run_view(run_record)
            or [item.get("state") for item in snapshot_records if item.get("record_type") == "checkpoint"][-1:] != [expected_checkpoint]
        ):
            findings.append(Finding("DEVELOPMENT_FAILURE_BASELINE_INVALID", "ERROR", "Pre-stage manifest snapshot does not prove the exact immutable checkpoint prefix.", pre_manifest[1]))

    for field in ("preserved_evidence", "materialized_stage_artifacts"):
        values = receipt.get(field)
        if (
            not isinstance(values, list)
            or any(bound_file(item) is None for item in values)
            or len({item.get("path") for item in values if isinstance(item, dict)}) != len(values)
        ):
            findings.append(Finding("DEVELOPMENT_FAILURE_EVIDENCE_INVALID", "ERROR", f"Failure receipt {field} is not a unique hash-bound run-owned inventory.", parsed[1]))

    agent_prefix = "baseline" if run_record.get("arm") == "matched_baseline" else "shadow"
    actual_materialized: set[str] = set()
    dossier_root = run_dir / f"{agent_prefix}_{stage}"
    if dossier_root.is_symlink():
        actual_materialized.add(dossier_root.relative_to(run_dir).as_posix())
    elif dossier_root.is_dir():
        actual_materialized.update(
            path.relative_to(run_dir).as_posix()
            for path in dossier_root.rglob("*")
            if path.is_file() or path.is_symlink()
        )
    trace_stage = "level2" if stage == "level2" else "fact-closure"
    for root_name in ("runtime_traces", "trace_attestations"):
        root = run_dir / root_name
        if root.is_dir() and not root.is_symlink():
            actual_materialized.update(
                path.relative_to(run_dir).as_posix()
                for path in root.glob(f"{agent_prefix}-{trace_stage}-*.json*")
                if path.is_file() or path.is_symlink()
            )
    report_path = run_dir / (
        "03a_level2_research.md" if stage == "level2" else "04_fact_closure.md"
    )
    if report_path.exists() or report_path.is_symlink():
        actual_materialized.add(report_path.relative_to(run_dir).as_posix())
    current_ledger = run_dir / "02b_raw_to_direction_ledger.jsonl"
    if (
        pre_ledger is not None
        and current_ledger.is_file()
        and not current_ledger.is_symlink()
        and _sha256(current_ledger) != receipt.get("pre_stage_ledger", {}).get("sha256")
    ):
        actual_materialized.add(current_ledger.relative_to(run_dir).as_posix())
    declared_materialized = receipt.get("materialized_stage_artifacts")
    declared_materialized_paths = (
        {item.get("path") for item in declared_materialized if isinstance(item, dict)}
        if isinstance(declared_materialized, list)
        else set()
    )
    if declared_materialized_paths != actual_materialized:
        findings.append(
            Finding(
                "DEVELOPMENT_FAILURE_EVIDENCE_INVALID",
                "ERROR",
                "Failure receipt materialized-stage inventory does not match the reachable filesystem prefix.",
                parsed[1],
            )
        )
    traces = receipt.get("causal_traces")
    if not isinstance(traces, list):
        findings.append(Finding("DEVELOPMENT_FAILURE_EVIDENCE_INVALID", "ERROR", "Failure receipt causal_traces must be a list.", parsed[1]))
    else:
        for item in traces:
            if not isinstance(item, dict) or set(item) != {"agent_id", "trace_task_name", "path", "sha256"} or bound_file({"path": item.get("path"), "sha256": item.get("sha256")}) is None:
                findings.append(Finding("DEVELOPMENT_FAILURE_EVIDENCE_INVALID", "ERROR", "Failure receipt contains an invalid causal raw-trace binding.", parsed[1]))
                break
    future = receipt.get("future_lifecycle_artifacts")
    actual_future: set[str] = set()
    future_names = (
        (
            "02d_fact_closure_candidates.json",
            "04_fact_closure.md",
            "00c_pre_freeze_manifest_snapshot.jsonl",
        )
        if stage == "level2"
        else ("00c_pre_freeze_manifest_snapshot.jsonl",)
    )
    for name in future_names:
        candidate = run_dir / name
        if candidate.exists() or candidate.is_symlink():
            actual_future.add(name)
    future_patterns = (
        (
            "baseline_fact_closure_launch.json",
            "shadow_fact_closure_launch.json",
            "baseline_fact_closure",
            "shadow_fact_closure",
            "baseline_shadow_finalist_*.md",
            "shadow_finalist_*.md",
            "finalist_*.md",
        )
        if stage == "level2"
        else (
            "baseline_shadow_finalist_*.md",
            "shadow_finalist_*.md",
            "finalist_*.md",
        )
    )
    for pattern in future_patterns:
        actual_future.update(
            path.relative_to(run_dir).as_posix()
            for path in run_dir.glob(pattern)
            if path.exists() or path.is_symlink()
        )
    if stage == "level2" and run_record.get("arm") == "matched_baseline":
        child_path = run_dir / "shadow_archipelago_lite"
        if child_path.exists() or child_path.is_symlink():
            actual_future.add("shadow_archipelago_lite")
    later_states = {
        "level2": {
            "level2_complete",
            "fact_closure_cohort_sealed",
            "closure_complete",
            "frozen",
            "complete",
        },
        "fact_closure": {"closure_complete", "frozen", "complete"},
    }[stage]
    actual_future.update(
        f"checkpoint:{record.get('state')}"
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
        and record.get("state") in later_states
    )
    if not isinstance(future, list) or any(not isinstance(item, str) for item in future):
        findings.append(Finding("DEVELOPMENT_FAILURE_EVIDENCE_INVALID", "ERROR", "Failure receipt future lifecycle inventory is malformed.", parsed[1]))
    elif future != sorted(set(future)) or set(future) != actual_future:
        findings.append(Finding("DEVELOPMENT_FAILURE_EVIDENCE_INVALID", "ERROR", "Failure receipt future lifecycle inventory does not match the reachable filesystem prefix.", parsed[1]))
    elif future:
        findings.append(Finding("DEVELOPMENT_FAILURE_FUTURE_ARTIFACTS_PRESENT", "ERROR", f"Stopped development run contains unreachable downstream lifecycle artifacts: {future}.", parsed[1]))
    findings.append(
        Finding(
            str(primary["code"]),
            "ERROR",
            f"{stage} admission stopped at {expected_checkpoint}: {primary['exception_type']}: {primary['message']}",
            parsed[1],
        )
    )


def _trace_output_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in _trace_output_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _trace_output_strings(item)]
    return []


def _trace_query_text(raw_input: str, opened_url: str) -> str | None:
    query_match = re.search(r'(?:(?:"q")|\bq)\s*:\s*"((?:\\.|[^"\\])*)"', raw_input)
    if query_match is not None:
        try:
            value = json.loads(f'"{query_match.group(1)}"')
        except json.JSONDecodeError:
            return None
        return _normalize_query(value)
    if re.search(r'(?:(?:"open")|\bopen)\s*:', raw_input):
        return _normalize_query(f"open {opened_url}")
    return None


def _parse_development_trace(
    run_dir: Path,
    agent: dict[str, Any],
    trace_path: Path,
    relative: str,
    findings: list[Finding],
) -> dict[str, Any] | None:
    """Independently reconcile a candidate-owned provider trace."""
    agent_id = str(agent.get("agent_id"))
    task_name = agent.get("trace_task_name")
    entity_id = agent.get("trace_entity_id")
    try:
        if trace_path.stat().st_size > 100_000_000:
            raise ValueError("candidate trace exceeds the 100 MB audit bound")
        trace_records = [
            json.loads(line)
            for line in trace_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        findings.append(
            Finding(
                "DEVELOPMENT_TRACE_CONTENT_INVALID",
                "ERROR",
                f"Development trace for {agent_id} cannot be completely parsed: {exc}.",
                relative,
                node_ids=(agent_id,),
            )
        )
        return None
    if not trace_records or any(not isinstance(record, dict) for record in trace_records):
        findings.append(Finding("DEVELOPMENT_TRACE_CONTENT_INVALID", "ERROR", f"Development trace for {agent_id} is empty or non-object JSON.", relative, node_ids=(agent_id,)))
        return None

    first = trace_records[0]
    if first.get("schema") == "zt1-hermetic-candidate-trace-v2":
        expected_fields = {
            "schema",
            "agent_id",
            "entity_id",
            "trace_task_name",
            "model",
            "reasoning_effort",
            "started_at",
            "ended_at",
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
            "meter_events",
            "web_calls",
        }
        valid = (
            len(trace_records) == 1
            and set(first) == expected_fields
            and agent.get("model") == "fixture-model-v1"
            and agent.get("reasoning_effort") == "fixture"
            and first.get("agent_id") == agent_id
            and first.get("entity_id") == entity_id
            and first.get("trace_task_name") == task_name
        )
        web_calls = first.get("web_calls")
        calls: dict[str, dict[str, Any]] = {}
        if isinstance(web_calls, list):
            for item in web_calls:
                if (
                    not isinstance(item, dict)
                    or set(item) != {"call_id", "query_text", "opened_url"}
                    or not all(isinstance(item.get(key), str) and item[key] for key in item)
                    or item["call_id"] in calls
                ):
                    valid = False
                    continue
                calls[item["call_id"]] = {
                    "query_text": _normalize_query(item["query_text"]),
                    "output_strings": [item["opened_url"]],
                }
        else:
            valid = False
        started = _parse_timestamp(first.get("started_at"))
        ended = _parse_timestamp(first.get("ended_at"))
        integer_fields = (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
        )
        integer_fields_valid = not any(
            not isinstance(first.get(key), int)
            or isinstance(first.get(key), bool)
            or first[key] < 0
            for key in integer_fields
        )
        if not integer_fields_valid:
            valid = False
        raw_meter_events = first.get("meter_events")
        meter_events: list[dict[str, Any]] = []
        if not isinstance(raw_meter_events, list) or not raw_meter_events:
            valid = False
        else:
            previous_time: datetime | None = None
            previous_resources = (-1, -1)
            for item in raw_meter_events:
                event_time = (
                    _parse_timestamp(item.get("occurred_at"))
                    if isinstance(item, dict)
                    else None
                )
                if (
                    not isinstance(item, dict)
                    or set(item)
                    != {
                        "occurred_at",
                        "input_tokens",
                        "cached_input_tokens",
                        "output_tokens",
                    }
                    or event_time is None
                    or any(
                        not isinstance(item.get(key), int)
                        or isinstance(item.get(key), bool)
                        or item[key] < 0
                        for key in (
                            "input_tokens",
                            "cached_input_tokens",
                            "output_tokens",
                        )
                    )
                    or item["cached_input_tokens"] > item["input_tokens"]
                ):
                    valid = False
                    continue
                event_resources = (
                    item["input_tokens"] - item["cached_input_tokens"],
                    item["output_tokens"],
                )
                if (
                    previous_time is not None
                    and event_time <= previous_time
                    or event_resources[0] < previous_resources[0]
                    or event_resources[1] < previous_resources[1]
                ):
                    valid = False
                meter_events.append(
                    {
                        "occurred_at": event_time,
                        "uncached_input_tokens": event_resources[0],
                        "output_tokens": event_resources[1],
                    }
                )
                previous_time = event_time
                previous_resources = event_resources
        if (
            started is None
            or ended is None
            or not meter_events
            or meter_events[0]["occurred_at"] < started
            or meter_events[-1]["occurred_at"] > ended
        ):
            valid = False
        elif integer_fields_valid and (
            meter_events[-1]["uncached_input_tokens"]
            != first["input_tokens"] - first["cached_input_tokens"]
            or meter_events[-1]["output_tokens"] != first["output_tokens"]
        ):
            valid = False
        if not valid or started is None or ended is None:
            findings.append(Finding("DEVELOPMENT_TRACE_CONTENT_INVALID", "ERROR", f"Hermetic development trace for {agent_id} violates its exact test-only schema.", relative, node_ids=(agent_id,)))
            return None
        facts = {
            "started_at": started,
            "ended_at": ended,
            "model": first["model"],
            "reasoning_effort": first["reasoning_effort"],
            "uncached_input_tokens": first["input_tokens"] - first["cached_input_tokens"],
            "output_tokens": first["output_tokens"],
            "elapsed_microseconds": first["elapsed_microseconds"],
            "calls": calls,
            "meter_events": meter_events,
            "hermetic": True,
        }
    else:
        source = first.get("payload", {}).get("source", {})
        subagent = source.get("subagent", {}) if isinstance(source, dict) else {}
        spawn = subagent.get("thread_spawn", {}) if isinstance(subagent, dict) else {}
        starts = [record for record in trace_records if record.get("type") == "event_msg" and record.get("payload", {}).get("type") == "task_started"]
        ends = [record for record in trace_records if record.get("type") == "event_msg" and record.get("payload", {}).get("type") == "task_complete"]
        contexts = [record.get("payload", {}) for record in trace_records if record.get("type") == "turn_context"]
        token_records = [record for record in trace_records if record.get("type") == "event_msg" and record.get("payload", {}).get("type") == "token_count"]
        if (
            first.get("type") != "session_meta"
            or not isinstance(task_name, str)
            or not isinstance(spawn, dict)
            or spawn.get("agent_path") != f"/root/{task_name}"
            or len(starts) != 1
            or len(ends) != 1
            or not contexts
            or not token_records
            or any(context.get("model") != agent.get("model") or context.get("effort") != agent.get("reasoning_effort") for context in contexts)
        ):
            findings.append(Finding("DEVELOPMENT_TRACE_IDENTITY_INVALID", "ERROR", f"Provider trace for {agent_id} does not bind its exact task/model/effort boundaries.", relative, node_ids=(agent_id,)))
            return None
        usage = token_records[-1].get("payload", {}).get("info", {}).get("total_token_usage", {})
        input_tokens = usage.get("input_tokens")
        cached_tokens = usage.get("cached_input_tokens")
        output_tokens = usage.get("output_tokens")
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in (input_tokens, cached_tokens, output_tokens)) or cached_tokens > input_tokens:
            findings.append(Finding("DEVELOPMENT_TRACE_RESOURCE_INVALID", "ERROR", f"Provider trace for {agent_id} has non-integral or impossible final token usage.", relative, node_ids=(agent_id,)))
            return None
        meter_events = []
        previous_event_time: datetime | None = None
        previous_event_resources = (-1, -1)
        for token_record in token_records:
            token_usage = (
                token_record.get("payload", {})
                .get("info", {})
                .get("total_token_usage", {})
            )
            event_input = token_usage.get("input_tokens")
            event_cached = token_usage.get("cached_input_tokens")
            event_output = token_usage.get("output_tokens")
            event_time = _parse_timestamp(token_record.get("timestamp"))
            if (
                event_time is None
                or any(
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value < 0
                    for value in (event_input, event_cached, event_output)
                )
                or event_cached > event_input
            ):
                findings.append(Finding("DEVELOPMENT_TRACE_RESOURCE_INVALID", "ERROR", f"Provider trace for {agent_id} has an invalid partial token meter event.", relative, node_ids=(agent_id,)))
                return None
            event_resources = (event_input - event_cached, event_output)
            if (
                previous_event_time is not None
                and event_time <= previous_event_time
                or event_resources[0] < previous_event_resources[0]
                or event_resources[1] < previous_event_resources[1]
            ):
                findings.append(Finding("DEVELOPMENT_TRACE_RESOURCE_INVALID", "ERROR", f"Provider trace for {agent_id} has non-monotonic partial meter events.", relative, node_ids=(agent_id,)))
                return None
            meter_events.append(
                {
                    "occurred_at": event_time,
                    "uncached_input_tokens": event_resources[0],
                    "output_tokens": event_resources[1],
                }
            )
            previous_event_time = event_time
            previous_event_resources = event_resources
        custom_calls = [record for record in trace_records if record.get("type") == "response_item" and record.get("payload", {}).get("type") == "custom_tool_call"]
        outputs = {
            record.get("payload", {}).get("call_id"): record.get("payload", {}).get("output")
            for record in trace_records
            if record.get("type") == "response_item"
            and record.get("payload", {}).get("type") == "custom_tool_call_output"
            and isinstance(record.get("payload", {}).get("call_id"), str)
        }
        calls: dict[str, dict[str, Any]] = {}
        for record in custom_calls:
            payload = record.get("payload", {})
            raw_input = str(payload.get("input", ""))
            if "tools.web__run" not in raw_input:
                continue
            call_id = payload.get("call_id")
            if not isinstance(call_id, str) or call_id in calls or call_id not in outputs:
                findings.append(Finding("DEVELOPMENT_TRACE_CALL_INVALID", "ERROR", f"Provider trace for {agent_id} has an unpaired or duplicate web call.", relative, node_ids=(agent_id,)))
                return None
            calls[call_id] = {
                "raw_input": raw_input,
                "output_strings": _trace_output_strings(outputs[call_id]),
            }
        started = _parse_timestamp(starts[0].get("timestamp"))
        ended = _parse_timestamp(ends[0].get("timestamp"))
        if started is None or ended is None:
            findings.append(Finding("DEVELOPMENT_TRACE_TIME_INVALID", "ERROR", f"Provider trace for {agent_id} lacks exact parseable task timestamps.", relative, node_ids=(agent_id,)))
            return None
        if (
            meter_events[0]["occurred_at"] < started
            or meter_events[-1]["occurred_at"] > ended
            or meter_events[-1]["uncached_input_tokens"] != input_tokens - cached_tokens
            or meter_events[-1]["output_tokens"] != output_tokens
        ):
            findings.append(Finding("DEVELOPMENT_TRACE_RESOURCE_INVALID", "ERROR", f"Provider trace for {agent_id} meter events do not reconcile to its task interval and final counters.", relative, node_ids=(agent_id,)))
            return None
        facts = {
            "started_at": started,
            "ended_at": ended,
            "model": contexts[-1].get("model"),
            "reasoning_effort": contexts[-1].get("effort"),
            "uncached_input_tokens": input_tokens - cached_tokens,
            "output_tokens": output_tokens,
            "elapsed_microseconds": _elapsed_microseconds(started, ended),
            "calls": calls,
            "meter_events": meter_events,
            "hermetic": False,
        }

    agent_start = _parse_timestamp(agent.get("started_at"))
    agent_end = _parse_timestamp(agent.get("ended_at"))
    resources = agent.get("resources")
    expected_resources = {
        "uncached_input_tokens": facts["uncached_input_tokens"],
        "output_tokens": facts["output_tokens"],
        "elapsed_microseconds": facts["elapsed_microseconds"],
    }
    if (
        agent_start != facts["started_at"]
        or agent_end != facts["ended_at"]
        or resources != expected_resources
        or facts["model"] != agent.get("model")
        or facts["reasoning_effort"] != agent.get("reasoning_effort")
    ):
        findings.append(Finding("DEVELOPMENT_TRACE_RECONCILIATION_MISMATCH", "ERROR", f"Development agent {agent_id} resources, timestamps, model, or effort differ from its raw trace.", relative, node_ids=(agent_id,)))
    return facts


def _audit_v2_live_metering(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    agent_by_id: dict[str, dict[str, Any]],
    trace_facts: dict[str, dict[str, Any]],
    contract: dict[str, Any] | None,
    excluded_roots: set[str],
    findings: list[Finding],
) -> None:
    """Replay live controller snapshots against exact partial raw-trace meters."""
    if run_record.get("run_profile") not in {
        "operational_live_with_shadow",
        "v2_matched_nonrouting",
    }:
        return
    thresholds = (
        contract.get("candidate_live_stop_thresholds")
        if isinstance(contract, dict)
        else None
    )
    monitor = contract.get("metering_monitor") if isinstance(contract, dict) else None
    if not isinstance(thresholds, dict) or monitor != MATCHED_METERING_MONITOR:
        return
    prefix = (
        "baseline"
        if run_record.get("arm") == "matched_baseline"
        else str(run_record.get("arm"))
    )
    scope_id = run_record.get("scope_id")
    meter_root = run_dir / "live_metering"
    maximum_gap = timedelta(
        milliseconds=monitor["poll_interval_milliseconds"] * 2
    )
    for stage, completion_state, expected_batches in (
        ("level2", "level2_complete", 4),
        ("fact_closure", "closure_complete", 2),
    ):
        if not _v2_state_reached(run_record, completion_state):
            continue
        stage_agents = {
            agent_id: agent
            for agent_id, agent in agent_by_id.items()
            if agent.get("stage") == stage
        }
        paths = sorted(
            meter_root.glob(f"{prefix}_{stage}_batch_*.jsonl")
            if meter_root.is_dir() and not meter_root.is_symlink()
            else []
        )
        checkpoint_records = [
            record
            for record in manifest_records
            if record.get("record_type") == "checkpoint"
            and record.get("state") == completion_state
        ]
        checkpoint_artifacts = {
            item.get("path"): item.get("sha256")
            for checkpoint_record in checkpoint_records
            for item in checkpoint_record.get("artifacts", [])
            if isinstance(item, dict)
        }
        if len(paths) != expected_batches or len(checkpoint_records) != 1:
            findings.append(
                Finding(
                    "DEVELOPMENT_LIVE_METERING_INVALID",
                    "ERROR",
                    f"Completed {stage} requires exactly {expected_batches} hash-bound live-controller batch logs.",
                    "live_metering",
                )
            )
            continue
        observed_agent_ids: set[str] = set()
        batch_intervals: list[tuple[datetime, datetime]] = []
        for batch_index, path in enumerate(paths, 1):
            parsed = _strict_run_file(
                run_dir, path.relative_to(run_dir).as_posix(), excluded_roots
            )
            relative = path.relative_to(run_dir).as_posix()
            if (
                parsed is None
                or checkpoint_artifacts.get(relative) != _sha256(path)
                or not re.fullmatch(
                    rf"{re.escape(prefix)}_{re.escape(stage)}_batch_{batch_index:02d}\.jsonl",
                    path.name,
                )
            ):
                findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller log {relative} is unsafe, misnumbered, or not checkpoint hash-bound.", relative))
                continue
            try:
                if path.stat().st_size > 100_000_000:
                    raise ValueError("live-controller log exceeds 100 MB")
                snapshots = [
                    json.loads(line)
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
                findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller log cannot be completely parsed: {exc}.", relative))
                continue
            if not snapshots or any(not isinstance(item, dict) for item in snapshots):
                findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller log is empty or malformed.", relative))
                continue
            poll_times: list[datetime] = []
            batch_agent_ids: set[str] | None = None
            log_invalid = False
            for snapshot in snapshots:
                expected_snapshot_fields = {
                    "schema",
                    "scope_id",
                    "arm",
                    "stage",
                    "batch_index",
                    "polled_at",
                    "poll_interval_milliseconds",
                    "agents",
                    "interrupt_task_names",
                    "stage_admission_must_fail",
                }
                polled_at = _parse_timestamp(snapshot.get("polled_at"))
                snapshot_agents = snapshot.get("agents")
                interrupt_names, interrupts_valid = _valid_string_list(
                    snapshot.get("interrupt_task_names"), allow_empty=True
                )
                if (
                    set(snapshot) != expected_snapshot_fields
                    or snapshot.get("schema")
                    != "zt1-development-live-meter-snapshot-v2"
                    or snapshot.get("scope_id") != scope_id
                    or snapshot.get("arm") != run_record.get("arm")
                    or snapshot.get("stage") != stage
                    or snapshot.get("batch_index") != batch_index
                    or snapshot.get("poll_interval_milliseconds")
                    != monitor["poll_interval_milliseconds"]
                    or polled_at is None
                    or not isinstance(snapshot_agents, list)
                    or not 1 <= len(snapshot_agents) <= 3
                    or not interrupts_valid
                    or len(interrupt_names) != len(set(interrupt_names))
                    or not isinstance(snapshot.get("stage_admission_must_fail"), bool)
                ):
                    log_invalid = True
                    continue
                poll_times.append(polled_at)
                current_agent_ids: set[str] = set()
                expected_interrupts: set[str] = set()
                for item in snapshot_agents:
                    expected_agent_fields = {
                        "agent_id",
                        "entity_id",
                        "task_name",
                        "status",
                        "measured_at",
                        "resources",
                        "live_stop_reasons",
                    }
                    if not isinstance(item, dict) or set(item) != expected_agent_fields:
                        log_invalid = True
                        continue
                    agent_id = item.get("agent_id")
                    agent = stage_agents.get(agent_id)
                    facts = trace_facts.get(agent_id) if isinstance(agent_id, str) else None
                    measured_at = _parse_timestamp(item.get("measured_at"))
                    resources = item.get("resources")
                    reasons, reasons_valid = _valid_string_list(
                        item.get("live_stop_reasons"), allow_empty=True
                    )
                    if (
                        agent is None
                        or facts is None
                        or measured_at is None
                        or measured_at > polled_at
                        or item.get("entity_id") != agent.get("trace_entity_id")
                        or item.get("task_name") != agent.get("trace_task_name")
                        or not isinstance(resources, dict)
                        or set(resources) != V2_AGENT_RESOURCE_KEYS
                        or any(not _is_nonnegative_int(resources.get(key)) for key in V2_AGENT_RESOURCE_KEYS)
                        or not reasons_valid
                    ):
                        log_invalid = True
                        continue
                    current_agent_ids.add(agent_id)
                    started = facts["started_at"]
                    ended = facts["ended_at"]
                    if measured_at < started:
                        expected_status = "not_started"
                        expected_elapsed = 0
                    elif measured_at >= ended:
                        expected_status = "complete"
                        expected_elapsed = facts["elapsed_microseconds"]
                    else:
                        expected_status = "running"
                        expected_elapsed = _elapsed_microseconds(started, measured_at)
                    prior_events = [
                        event
                        for event in facts["meter_events"]
                        if event["occurred_at"] <= measured_at
                    ]
                    expected_uncached = (
                        prior_events[-1]["uncached_input_tokens"]
                        if prior_events
                        else 0
                    )
                    expected_output = (
                        prior_events[-1]["output_tokens"] if prior_events else 0
                    )
                    expected_resources = {
                        "uncached_input_tokens": expected_uncached,
                        "output_tokens": expected_output,
                        "elapsed_microseconds": expected_elapsed,
                    }
                    stage_thresholds = thresholds[stage]
                    expected_reasons = {
                        key
                        for key in (
                            "uncached_input_tokens",
                            "output_tokens",
                            "elapsed_microseconds",
                        )
                        if resources[key]
                        >= (
                            stage_thresholds["elapsed_minutes"] * 60_000_000
                            if key == "elapsed_microseconds"
                            else stage_thresholds[key]
                        )
                    }
                    if (
                        item.get("status") != expected_status
                        or resources != expected_resources
                        or set(reasons) != expected_reasons
                    ):
                        log_invalid = True
                    if expected_reasons and expected_status == "running":
                        expected_interrupts.add(str(agent.get("trace_task_name")))
                if batch_agent_ids is None:
                    batch_agent_ids = current_agent_ids
                elif current_agent_ids != batch_agent_ids:
                    log_invalid = True
                if (
                    set(interrupt_names) != expected_interrupts
                    or snapshot["stage_admission_must_fail"]
                    != bool(expected_interrupts)
                    or expected_interrupts
                ):
                    log_invalid = True
            if (
                log_invalid
                or not poll_times
                or poll_times != sorted(poll_times)
                or any(
                    later - earlier > maximum_gap
                    for earlier, later in zip(poll_times, poll_times[1:])
                )
                or batch_agent_ids is None
            ):
                findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller log {relative} does not reconcile to its raw partial meter events and one-second schedule.", relative))
                continue
            batch_agents = [stage_agents[agent_id] for agent_id in batch_agent_ids]
            starts = [_parse_timestamp(agent.get("started_at")) for agent in batch_agents]
            ends = [_parse_timestamp(agent.get("ended_at")) for agent in batch_agents]
            if (
                any(value is None for value in starts + ends)
                or poll_times[0] - min(starts) > maximum_gap
                or max(ends) - poll_times[-1] > maximum_gap
            ):
                findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller log {relative} does not cover its batch boundaries.", relative))
                continue
            observed_agent_ids.update(batch_agent_ids)
            batch_intervals.append((min(starts), max(ends)))
        if observed_agent_ids != set(stage_agents) or any(
            current_start <= previous_end
            for (_previous_start, previous_end), (current_start, _current_end)
            in zip(batch_intervals, batch_intervals[1:])
        ):
            findings.append(Finding("DEVELOPMENT_LIVE_METERING_INVALID", "ERROR", f"{stage} live-controller batches do not partition the exact independently metered agents in sequential groups of at most three.", "live_metering"))


def _audit_v2_research_chains(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
    contract: dict[str, Any] | None,
    excluded_roots: set[str],
    findings: list[Finding],
    resources: dict[str, Any],
    checkpoint: str | None,
) -> None:
    manifest_name = "00a_context_and_resource_manifest.jsonl"
    ledger_name = "02b_raw_to_direction_ledger.jsonl"
    scope_id = run_record.get("scope_id")
    expected_arm = run_record.get("arm")
    expected_model = run_record.get("model")
    expected_effort = run_record.get("reasoning_effort")
    agent_records = [record for record in manifest_records if record.get("record_type") == "agent"]
    allocation_records = [record for record in manifest_records if record.get("record_type") == "allocation"]
    query_records = [record for record in manifest_records if record.get("record_type") == "query"]
    tool_records = [record for record in manifest_records if record.get("record_type") == "tool_event"]
    source_records = [record for record in manifest_records if record.get("record_type") == "source_open"]
    evidence_records = [record for record in ledger_records if record.get("record_type") == "evidence"]
    ledger_ids = _typed_ledger_id_registry(ledger_records)
    known_entity_ids = _scope_entity_ids(ledger_records)
    matched_initial = (
        run_record.get("cohort_kind") == "initial"
        and run_record.get("run_profile")
        in {"operational_live_with_shadow", "v2_matched_nonrouting"}
    )
    discovery_complete = _v2_state_reached(
        run_record,
        "problem_cards_frozen"
        if run_record.get("mode") == "archipelago_lite_shadow"
        else "raw_frozen",
    )
    level2_complete = _v2_state_reached(run_record, "level2_complete")
    closure_cohort_sealed = _v2_state_reached(
        run_record, "fact_closure_cohort_sealed"
    )
    closure_complete = _v2_state_reached(run_record, "closure_complete")
    frozen_reached = _v2_state_reached(run_record, "frozen")
    primary_ledger_id_fields = {
        "problem": "problem_id",
        "mapping": "raw_id",
        "level2": "concept_id",
        "finalist": "finalist_id",
        "evidence": "evidence_id",
    }
    for record_type, id_field in primary_ledger_id_fields.items():
        observed = [
            record.get(id_field)
            for record in ledger_records
            if record.get("record_type") == record_type
            and isinstance(record.get(id_field), str)
            and record.get(id_field).strip()
        ]
        duplicates = sorted(
            value for value, count in Counter(observed).items() if count > 1
        )
        if duplicates:
            findings.append(
                Finding(
                    "V2_TYPED_ID_DUPLICATE",
                    "ERROR",
                    f"V2 {record_type} records duplicate their owning {id_field} values: {duplicates}.",
                    ledger_name,
                    node_ids=tuple(duplicates),
                )
            )

    agent_by_id: dict[str, dict[str, Any]] = {}
    agent_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    agent_metering_exact: dict[str, bool] = {}
    agent_assignments: dict[str, set[str]] = {}
    agent_outputs: dict[str, set[str]] = {}
    development_trace_hashes: dict[str, str] = {}
    development_trace_tasks: dict[str, str] = {}
    development_trace_facts: dict[str, dict[str, Any]] = {}
    for agent in agent_records:
        agent_id = agent.get("agent_id")
        line = agent.get("_line")
        if not isinstance(agent_id, str) or not agent_id.strip():
            findings.append(
                Finding(
                    "AGENT_ID_INVALID",
                    "ERROR",
                    "V2 agent has no stable non-empty agent_id.",
                    manifest_name,
                    line,
                )
            )
            continue
        if agent_id in agent_by_id:
            findings.append(
                Finding(
                    "AGENT_ID_DUPLICATE",
                    "ERROR",
                    f"V2 agent ID {agent_id} is duplicated.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
        agent_by_id[agent_id] = agent
        expected_agent_fields = set(V2_AGENT_FIELDS)
        if agent.get("stage") == "problem_discovery":
            expected_agent_fields.add("island_id")
        if agent.get("stage") in {"level2", "fact_closure"}:
            expected_agent_fields.update(V2_DEVELOPMENT_TRACE_FIELDS)
        if set(agent) - {"_line"} != expected_agent_fields:
            findings.append(
                Finding(
                    "V2_AGENT_FIELDS_INVALID",
                    "ERROR",
                    f"Agent {agent_id} must use the exact closed V2 agent schema.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
        assigned_ids, assigned_valid = _valid_string_list(agent.get("assigned_ids"))
        output_ids, output_valid = _valid_string_list(agent.get("output_ids"))
        if (
            not assigned_valid
            or not output_valid
            or len(assigned_ids) != len(set(assigned_ids))
            or len(output_ids) != len(set(output_ids))
        ):
            findings.append(
                Finding(
                    "AGENT_ASSIGNMENT_IDS_INVALID",
                    "ERROR",
                    f"V2 agent {agent_id} requires non-empty unique assigned_ids and output_ids.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
            assigned_ids = []
            output_ids = []
        agent_assignments[agent_id] = set(assigned_ids)
        agent_outputs[agent_id] = set(output_ids)
        if agent.get("stage") in {"level2", "fact_closure"}:
            trace_entity_id = agent.get("trace_entity_id")
            trace_task_name = agent.get("trace_task_name")
            trace_path = _strict_run_file(
                run_dir, agent.get("trace_path"), excluded_roots
            )
            trace_digest = agent.get("trace_sha256")
            if (
                len(assigned_ids) != 1
                or assigned_ids != output_ids
                or trace_entity_id != assigned_ids[0]
                or not isinstance(trace_task_name, str)
                or not trace_task_name.strip()
                or trace_path is None
                or not isinstance(trace_digest, str)
                or not re.fullmatch(r"[0-9a-f]{64}", trace_digest)
                or trace_digest != _sha256(trace_path[0])
            ):
                findings.append(
                    Finding(
                        "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                        "ERROR",
                        f"Development agent {agent_id} must own exactly one candidate, one output, and one exact candidate-bound trace.",
                        manifest_name,
                        line,
                        (agent_id,),
                    )
                )
            elif trace_digest in development_trace_hashes:
                findings.append(
                    Finding(
                        "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                        "ERROR",
                        f"Development agents {development_trace_hashes[trace_digest]} and {agent_id} reuse one trace; post-hoc multi-entity partitioning is not candidate proof.",
                        manifest_name,
                        line,
                        (development_trace_hashes[trace_digest], agent_id),
                    )
                )
            elif trace_task_name in development_trace_tasks:
                findings.append(
                    Finding(
                        "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                        "ERROR",
                        f"Development agents {development_trace_tasks[trace_task_name]} and {agent_id} reuse one global trace-task identity.",
                        manifest_name,
                        line,
                        (development_trace_tasks[trace_task_name], agent_id),
                    )
                )
            else:
                development_trace_hashes[trace_digest] = agent_id
                development_trace_tasks[trace_task_name] = agent_id
                trace_facts = _parse_development_trace(
                    run_dir,
                    agent,
                    trace_path[0],
                    trace_path[1],
                    findings,
                )
                if trace_facts is not None:
                    development_trace_facts[agent_id] = trace_facts
        unknown_agent_ids = sorted((set(assigned_ids) | set(output_ids)) - known_entity_ids)
        if unknown_agent_ids:
            findings.append(
                Finding(
                    "AGENT_ENTITY_IDS_UNKNOWN",
                    "ERROR",
                    f"Agent {agent_id} assignment/output contains IDs not structurally registered by their owning ledger record types: {unknown_agent_ids}.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
        if agent.get("fork_turns") != "none":
            findings.append(Finding("FORBIDDEN_CONTEXT_FORK", "ERROR", f"V2 agent {agent_id} must use fork_turns=none.", manifest_name, line, (agent_id,)))
        context_classes, context_valid = _valid_string_list(agent.get("context_classes"))
        expected_context_classes = (
            {"history"}
            if agent.get("stage") == "history_compressor"
            else {"founder_constraints", "safety_legal", "neutral_evidence"}
        )
        if (
            not context_valid
            or len(context_classes) != len(set(context_classes))
            or set(context_classes) != expected_context_classes
            or not set(context_classes).issubset(V2_CONTEXT_CLASSES)
        ):
            findings.append(
                Finding(
                    "V2_CONTEXT_CLASSES_INVALID",
                    "ERROR",
                    f"Agent {agent_id} must declare the exact closed context class set for stage {agent.get('stage')!r}.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
        allowlisted, allowlisted_valid = _valid_string_list(agent.get("allowlisted_files"))
        files_read, files_read_valid = _valid_string_list(agent.get("files_read"))
        context_files = agent.get("context_files")
        context_paths: list[str] = []
        if not isinstance(context_files, list) or not context_files:
            findings.append(Finding("V2_CONTEXT_PACKET_INVALID", "ERROR", f"Agent {agent_id} requires a non-empty hashed context_files inventory.", manifest_name, line, (agent_id,)))
        else:
            for item in context_files:
                if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
                    findings.append(Finding("V2_CONTEXT_PACKET_INVALID", "ERROR", f"Agent {agent_id} context_files entries use exactly path and sha256.", manifest_name, line, (agent_id,)))
                    continue
                parsed_context = _strict_run_file(run_dir, item.get("path"), excluded_roots)
                if parsed_context is None or item.get("sha256") != _sha256(parsed_context[0]):
                    findings.append(Finding("V2_CONTEXT_PACKET_INVALID", "ERROR", f"Agent {agent_id} context packet is missing, unsafe, child-owned, or hash-mismatched.", manifest_name, line, (agent_id,)))
                    continue
                context_paths.append(parsed_context[1])
                try:
                    if parsed_context[0].stat().st_size > 5_000_000:
                        raise ValueError("context packet exceeds the bounded scanner limit")
                    packet_text = parsed_context[0].read_text(encoding="utf-8-sig")
                except (OSError, UnicodeError, ValueError) as exc:
                    findings.append(Finding("V2_CONTEXT_PACKET_SCAN_INCOMPLETE", "ERROR", f"Agent {agent_id} context packet cannot be completely scanned: {exc}.", parsed_context[1], node_ids=(agent_id,)))
                else:
                    if any(pattern.search(packet_text) for pattern in PROHIBITED_PACKET_PATTERNS):
                        findings.append(Finding("FORBIDDEN_CONTEXT_CONTENT", "ERROR", f"Agent {agent_id} context contains prohibited downstream, validator, score, objection, or rejection content.", parsed_context[1], node_ids=(agent_id,)))
        if (
            not allowlisted_valid
            or not files_read_valid
            or len(allowlisted) != len(set(allowlisted))
            or len(files_read) != len(set(files_read))
            or set(allowlisted) != set(context_paths)
            or set(files_read) != set(context_paths)
        ):
            findings.append(
                Finding(
                    "V2_CONTEXT_INVENTORY_MISMATCH",
                    "ERROR",
                    f"Agent {agent_id} allowlisted_files, files_read, and hashed context_files must be exact reciprocal inventories.",
                    manifest_name,
                    line,
                    (agent_id,),
                )
            )
        resource_fields = set(agent.get("resources", {})) if isinstance(agent.get("resources"), dict) else set()
        if resource_fields != V2_AGENT_RESOURCE_KEYS:
            findings.append(Finding("AGENT_RESOURCE_FIELDS_INVALID", "ERROR", f"Agent {agent_id} resources must use the exact closed resource keys.", manifest_name, line, (agent_id,)))
        agent_metering_exact[agent_id] = agent.get("metering_basis") in EXACT_METERING_BASES
        if not agent_metering_exact[agent_id]:
            findings.append(
                Finding(
                    "METERING_BASIS_INCOMPLETE",
                    "UNKNOWN",
                    f"Agent {agent_id} must use metering_basis tool_reported or trace_derived_exact; estimates and missing bases are not certifiable.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )

    expected_stage_counts = (
        SHADOW_V2_STAGE_COUNTS
        if run_record.get("mode") == "archipelago_lite_shadow"
        else LIVE_V2_STAGE_COUNTS
    )
    expected_stage_roles = (
        SHADOW_V2_STAGE_ROLES
        if run_record.get("mode") == "archipelago_lite_shadow"
        else LIVE_V2_STAGE_ROLES
    )
    stage_boundaries = {
        "generation": "raw_frozen",
        "problem_discovery": "problem_cards_frozen",
        "direct_concept": "direct_concepts_frozen",
        "inversion": "transformations_frozen",
        "recombination": "transformations_frozen",
        "history_compressor": (
            "mapped"
            if run_record.get("mode") == "archipelago_lite_shadow"
            else "history_frozen"
        ),
        "cartography": "mapped",
        "cluster_audit": (
            "level1_frozen"
            if run_record.get("mode") == "archipelago_lite_shadow"
            else "cluster_audited"
        ),
        "level1": (
            "level1_frozen"
            if run_record.get("mode") == "archipelago_lite_shadow"
            else "level2_cohort_sealed"
        ),
        "provisional_selector": "provisional_order_sealed",
        "selector": "ballots_sealed",
        "tail_challenger": "ballots_sealed",
        "level2": "level2_complete",
        "finalist_selector": "fact_closure_cohort_sealed",
        "fact_closure": "closure_complete",
    }
    reachable_stage_counts = {
        stage: count
        for stage, count in expected_stage_counts.items()
        if _v2_state_reached(run_record, stage_boundaries[stage])
    }
    observed_stage_counts = Counter(str(agent.get("stage")) for agent in agent_records)
    if observed_stage_counts != Counter(reachable_stage_counts):
        findings.append(
            Finding(
                "V2_STAGE_ROLE_CARDINALITY_INVALID",
                "ERROR",
                f"V2 lifecycle prefix has an extra, missing, or cross-mode stage; expected {reachable_stage_counts}, found {dict(observed_stage_counts)}.",
                manifest_name,
            )
        )
    for stage, expected_roles in expected_stage_roles.items():
        if stage not in reachable_stage_counts:
            continue
        observed_roles = [
            str(agent.get("role"))
            for agent in agent_records
            if agent.get("stage") == stage
        ]
        expected_count = reachable_stage_counts[stage]
        expected_role_counter = (
            Counter({role: 1 for role in expected_roles})
            if len(expected_roles) == expected_count
            else Counter({next(iter(expected_roles)): expected_count})
        )
        if Counter(observed_roles) != expected_role_counter:
            findings.append(
                Finding(
                    "V2_STAGE_ROLE_CARDINALITY_INVALID",
                    "ERROR",
                    f"V2 stage {stage} must use exact role cardinality {dict(expected_role_counter)}; found {dict(Counter(observed_roles))}.",
                    manifest_name,
                )
                )

    _audit_v2_live_metering(
        run_dir,
        run_record,
        manifest_records,
        agent_by_id,
        development_trace_facts,
        contract,
        excluded_roots,
        findings,
    )

    problem_outputs_by_creator: dict[str, set[str]] = defaultdict(set)
    mapping_outputs_by_creator: dict[str, set[str]] = defaultdict(set)
    for record in ledger_records:
        creator = record.get("creator_agent_id")
        if not isinstance(creator, str):
            continue
        if record.get("record_type") == "problem" and isinstance(record.get("problem_id"), str):
            problem_outputs_by_creator[creator].add(record["problem_id"])
        elif record.get("record_type") == "mapping" and isinstance(record.get("raw_id"), str):
            mapping_outputs_by_creator[creator].add(record["raw_id"])
    for agent_id, agent in agent_by_id.items():
        stage = agent.get("stage")
        expected_outputs: set[str] | None = None
        if stage == "problem_discovery":
            expected_outputs = problem_outputs_by_creator.get(agent_id, set())
        elif stage in {"generation", "direct_concept", "inversion", "recombination"}:
            expected_outputs = mapping_outputs_by_creator.get(agent_id, set())
        elif stage == "level2" and level2_complete:
            expected_outputs = agent_outputs.get(agent_id, set())
        if expected_outputs is not None and agent_outputs.get(agent_id, set()) != expected_outputs:
            findings.append(
                Finding(
                    "AGENT_OUTPUT_LEDGER_MISMATCH",
                    "ERROR",
                    f"Agent {agent_id} output_ids do not exactly equal the entities created for its V2 stage.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )
        agent_times[agent_id] = (
            _parse_timestamp(agent.get("started_at")),
            _parse_timestamp(agent.get("ended_at")),
        )
        if (
            agent.get("scope_id") != scope_id
            or agent.get("arm") != expected_arm
            or agent.get("model") != expected_model
            or agent.get("reasoning_effort") != expected_effort
        ):
            findings.append(
                Finding(
                    "AGENT_SCOPE_PROFILE_MISMATCH",
                    "ERROR",
                    f"Agent {agent_id} differs from the exact V2 scope, arm, model, or reasoning effort.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )

    stage_caps = (
        contract.get("stage_query_caps") if isinstance(contract, dict) else {}
    )
    allocation_by_id: dict[str, dict[str, Any]] = {}
    allocation_entities: dict[str, set[str]] = {}
    allocation_times: dict[str, datetime] = {}
    allocation_resources: dict[str, dict[str, Decimal]] = {}
    allocation_metering_exact: dict[str, bool] = {}
    for allocation in allocation_records:
        allocation_id = allocation.get("allocation_id")
        line = allocation.get("_line")
        if not isinstance(allocation_id, str) or not allocation_id.strip():
            findings.append(Finding("ALLOCATION_ID_INVALID", "ERROR", "V2 allocation has no stable allocation_id.", manifest_name, line))
            continue
        if allocation_id in allocation_by_id:
            findings.append(Finding("ALLOCATION_ID_DUPLICATE", "ERROR", f"Allocation {allocation_id} is duplicated.", manifest_name, line, (allocation_id,)))
        allocation_by_id[allocation_id] = allocation
        if set(allocation) - {"_line"} != V2_ALLOCATION_FIELDS:
            findings.append(Finding("V2_ALLOCATION_FIELDS_INVALID", "ERROR", f"Allocation {allocation_id} must use the exact closed V2 allocation schema.", manifest_name, line, (allocation_id,)))
        allocation_metering_exact[allocation_id] = allocation.get("metering_basis") in EXACT_METERING_BASES
        if not allocation_metering_exact[allocation_id]:
            findings.append(
                Finding(
                    "METERING_BASIS_INCOMPLETE",
                    "UNKNOWN",
                    f"Allocation {allocation_id} must use metering_basis tool_reported or trace_derived_exact.",
                    manifest_name,
                    line,
                    (allocation_id,),
                )
            )
        stage = allocation.get("stage")
        if stage not in ALLOCATION_STAGES:
            findings.append(Finding("ALLOCATION_STAGE_INVALID", "ERROR", f"Allocation {allocation_id} has unsupported stage {stage!r}.", manifest_name, line, (allocation_id,)))
        agent_id = allocation.get("agent_id")
        agent = agent_by_id.get(agent_id) if isinstance(agent_id, str) else None
        if agent is None:
            findings.append(Finding("ALLOCATION_AGENT_UNKNOWN", "ERROR", f"Allocation {allocation_id} references unknown agent {agent_id!r}.", manifest_name, line, (allocation_id,)))
        elif (
            allocation.get("scope_id") != scope_id
            or allocation.get("arm") != expected_arm
            or agent.get("stage") != stage
            or agent.get("scope_id") != scope_id
            or agent.get("arm") != expected_arm
        ):
            findings.append(Finding("ALLOCATION_AGENT_CONTEXT_MISMATCH", "ERROR", f"Allocation {allocation_id} does not match its agent's scope, arm, and stage.", manifest_name, line, (allocation_id, str(agent_id))))
        entity_ids, entities_valid = _valid_string_list(allocation.get("entity_ids"))
        if not entities_valid or len(entity_ids) != len(set(entity_ids)):
            findings.append(Finding("ALLOCATION_ENTITY_IDS_INVALID", "ERROR", f"Allocation {allocation_id} needs unique typed entity_ids.", manifest_name, line, (allocation_id,)))
            entity_ids = []
        unknown_allocation_entities = sorted(set(entity_ids) - known_entity_ids)
        if unknown_allocation_entities:
            findings.append(Finding("ALLOCATION_ENTITY_UNKNOWN", "ERROR", f"Allocation {allocation_id} references unregistered entities {unknown_allocation_entities}.", manifest_name, line, (allocation_id,)))
        if isinstance(agent_id, str) and agent is not None and not set(entity_ids).issubset(
            agent_assignments.get(agent_id, set()) | agent_outputs.get(agent_id, set())
        ):
            findings.append(
                Finding(
                    "ALLOCATION_AGENT_ENTITY_MISMATCH",
                    "ERROR",
                    f"Allocation {allocation_id} contains entities outside owning agent {agent_id}'s assigned_ids/output_ids.",
                    manifest_name,
                    line,
                    (allocation_id, agent_id),
                )
            )
        allocation_entities[allocation_id] = set(entity_ids)
        created_at = _parse_timestamp(allocation.get("created_at"))
        if created_at is None:
            findings.append(Finding("ALLOCATION_TIME_UNKNOWN", "UNKNOWN", f"Allocation {allocation_id} lacks an offset-aware created_at.", manifest_name, line, (allocation_id,)))
        else:
            allocation_times[allocation_id] = created_at
            agent_start = agent_times.get(str(agent_id), (None, None))[0]
            if agent_start is None or created_at >= agent_start:
                findings.append(Finding("ALLOCATION_NOT_PREREGISTERED", "ERROR", f"Allocation {allocation_id} was not created strictly before its agent started.", manifest_name, line, (allocation_id, str(agent_id))))
        cap = allocation.get("query_cap")
        used = allocation.get("used_unique_queries")
        unused = allocation.get("unused_queries")
        expected_cap = (
            0
            if stage in ZERO_QUERY_STAGES
            else stage_caps.get(stage) if stage in {"level2", "fact_closure"} else cap
        )
        if (
            not isinstance(cap, int)
            or isinstance(cap, bool)
            or cap < 0
            or cap != expected_cap
            or not isinstance(used, int)
            or isinstance(used, bool)
            or not isinstance(unused, int)
            or isinstance(unused, bool)
            or used < 0
            or unused < 0
            or used + unused != cap
        ):
            findings.append(Finding("ALLOCATION_RECONCILIATION_INVALID", "ERROR", f"Allocation {allocation_id} does not reconcile to the exact stage cap.", manifest_name, line, (allocation_id,)))
        if stage in ZERO_QUERY_STAGES and (cap != 0 or used != 0 or unused != 0):
            findings.append(Finding("ZERO_QUERY_STAGE_ALLOCATION_INVALID", "ERROR", f"Allocation {allocation_id} is a supported zero-query stage and must declare zero cap and usage.", manifest_name, line, (allocation_id,)))
        resource_record = allocation.get("resources")
        if not isinstance(resource_record, dict) or set(resource_record) != V2_AGENT_RESOURCE_KEYS:
            findings.append(Finding("ALLOCATION_RESOURCE_FIELDS_INVALID", "ERROR", f"Allocation {allocation_id} resources must use the exact closed resource keys.", manifest_name, line, (allocation_id,)))
        parsed_resources: dict[str, Decimal] = {}
        for key in (
            "uncached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
        ):
            raw_resource = resource_record.get(key) if isinstance(resource_record, dict) else None
            parsed = _as_decimal(raw_resource)
            if key in {
                "uncached_input_tokens",
                "output_tokens",
                "elapsed_microseconds",
            } and (
                not isinstance(raw_resource, int) or isinstance(raw_resource, bool)
            ):
                parsed = None
            if parsed is None:
                findings.append(
                    Finding(
                        "ALLOCATION_RESOURCE_TELEMETRY_INCOMPLETE",
                        "UNKNOWN",
                        f"Allocation {allocation_id} lacks exact nonnegative resource {key}.",
                        manifest_name,
                        line,
                        (allocation_id,),
                    )
                )
            else:
                parsed_resources[key] = parsed
        if len(parsed_resources) == 3:
            allocation_resources[allocation_id] = parsed_resources
            if stage in {"level2", "fact_closure"} and isinstance(contract, dict):
                stage_budget = contract.get("candidate_budgets", {}).get(stage)
                budget_map = {
                    "uncached_input_tokens": "uncached_input_tokens",
                    "output_tokens": "output_tokens",
                    "elapsed_microseconds": "elapsed_minutes",
                }
                if isinstance(stage_budget, dict):
                    exceeded = [
                        key
                        for key, contract_key in budget_map.items()
                        if (
                            _as_decimal(stage_budget.get(contract_key)) is not None
                            and parsed_resources[key]
                            > (
                                _as_decimal(stage_budget.get(contract_key))
                                * Decimal(60_000_000)
                                if key == "elapsed_microseconds"
                                else _as_decimal(stage_budget.get(contract_key))
                            )
                        )
                    ]
                    if exceeded:
                        findings.append(Finding("DEVELOPMENT_CONTRACT_CAP_EXCEEDED", "ERROR", f"Allocation {allocation_id} exceeds candidate budgets for {exceeded}.", manifest_name, line, (allocation_id,)))

    allocations_by_agent: dict[str, list[str]] = defaultdict(list)
    for allocation_id, allocation in allocation_by_id.items():
        agent_id = allocation.get("agent_id")
        if isinstance(agent_id, str):
            allocations_by_agent[agent_id].append(allocation_id)
    for agent_id, agent in agent_by_id.items():
        stage = agent.get("stage")
        owned_ids = allocations_by_agent.get(agent_id, [])
        owned_entity_union = set().union(
            *(allocation_entities.get(allocation_id, set()) for allocation_id in owned_ids)
        ) if owned_ids else set()
        expected_allocation_count = 1
        if len(owned_ids) != expected_allocation_count:
            findings.append(
                Finding(
                    "AGENT_ALLOCATION_OWNERSHIP_MISMATCH",
                    "ERROR",
                    f"Agent {agent_id} stage {stage!r} requires exactly {expected_allocation_count} owned allocation(s); found {len(owned_ids)}.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )
        if stage in {"generation", "problem_discovery", "level2", "fact_closure"}:
            expected_entities = agent_assignments.get(agent_id, set())
            if owned_entity_union != expected_entities:
                findings.append(
                    Finding(
                        "AGENT_ALLOCATION_ENTITY_RECIPROCITY_INVALID",
                        "ERROR",
                        f"Research agent {agent_id}'s allocation entities must exactly cover its assigned_ids.",
                        manifest_name,
                        agent.get("_line"),
                        (agent_id,),
                    )
                )
        if stage in {"level2", "fact_closure"} and any(
            len(allocation_entities.get(allocation_id, set())) != 1
            for allocation_id in owned_ids
        ):
            findings.append(
                Finding(
                    "DEVELOPMENT_ALLOCATION_ENTITY_INVALID",
                    "ERROR",
                    f"Every {stage} allocation owned by {agent_id} must cover exactly one candidate.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )
        if stage in {"level2", "fact_closure"} and (
            len(agent_assignments.get(agent_id, set())) != 1
            or len(agent_outputs.get(agent_id, set())) != 1
            or agent_assignments.get(agent_id, set())
            != agent_outputs.get(agent_id, set())
        ):
            findings.append(
                Finding(
                    "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                    "ERROR",
                    f"Development agent {agent_id} cannot aggregate or partition multiple candidate assignments.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )

    if level2_complete:
        level2_agent_entities = [
            next(iter(agent_assignments[agent_id]))
            for agent_id, agent in agent_by_id.items()
            if agent.get("stage") == "level2"
            and len(agent_assignments.get(agent_id, set())) == 1
        ]
        if Counter(level2_agent_entities) != Counter(ledger_ids["level2"]):
            findings.append(
                Finding(
                    "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                    "ERROR",
                    "The twelve Level-2 agents must map one-to-one to the twelve completed Level-2 ledger entities.",
                    manifest_name,
                )
            )

    aggregate = contract.get("aggregate_opportunity") if isinstance(contract, dict) else None
    if isinstance(aggregate, dict) and frozen_reached:
        actual_opportunity = {
            "raw": len(_typed_record_field_ids(ledger_records, "mapping", "raw_id")),
            "level2": len(
                [record for record in ledger_records if record.get("record_type") == "level2"]
            ),
            "fact_closure": len(
                [record for record in ledger_records if record.get("record_type") == "finalist"]
            ),
            "frozen": len(
                [record for record in ledger_records if record.get("record_type") == "finalist"]
            ),
            "discovery_queries": sum(
                int(allocation.get("query_cap", 0))
                for allocation in allocation_records
                if allocation.get("stage") in {"generation", "problem_discovery"}
                and isinstance(allocation.get("query_cap"), int)
                and not isinstance(allocation.get("query_cap"), bool)
            ),
            "level2_queries": sum(
                int(allocation.get("query_cap", 0))
                for allocation in allocation_records
                if allocation.get("stage") == "level2"
                and isinstance(allocation.get("query_cap"), int)
                and not isinstance(allocation.get("query_cap"), bool)
            ),
            "fact_closure_queries": sum(
                int(allocation.get("query_cap", 0))
                for allocation in allocation_records
                if allocation.get("stage") == "fact_closure"
                and isinstance(allocation.get("query_cap"), int)
                and not isinstance(allocation.get("query_cap"), bool)
            ),
        }
        actual_opportunity["total_queries"] = (
            actual_opportunity["discovery_queries"]
            + actual_opportunity["level2_queries"]
            + actual_opportunity["fact_closure_queries"]
        )
        if aggregate != actual_opportunity:
            findings.append(
                Finding(
                    "DEVELOPMENT_CONTRACT_OPPORTUNITY_MISMATCH",
                    "ERROR",
                    f"Contract aggregate_opportunity does not exactly reconcile to typed cohorts and allocation capacities; declared={aggregate}, observed={actual_opportunity}.",
                    manifest_name,
                )
            )
    if matched_initial and discovery_complete:
        discovery_allocations = [
            allocation
            for allocation in allocation_records
            if allocation.get("stage") in {"generation", "problem_discovery"}
        ]
        if run_record.get("mode") == "archipelago_lite_shadow":
            cap_split_valid = (
                len(discovery_allocations) == 6
                and all(allocation.get("query_cap") == 18 for allocation in discovery_allocations)
            )
        else:
            seed = run_record.get("seed")
            ordered_roles = (
                sorted(
                    LIVE_CREATIVE_ROLES,
                    key=lambda role: hashlib.sha256(
                        f"{seed}|baseline-discovery-role|{role}".encode("utf-8")
                    ).hexdigest(),
                )
                if isinstance(seed, (str, int))
                else []
            )
            expected_caps_by_role = dict(
                zip(ordered_roles, (22, 22, 22, 21, 21))
            )
            cap_split_valid = len(discovery_allocations) == 5 and all(
                isinstance(allocation.get("agent_id"), str)
                and agent_by_id.get(allocation["agent_id"], {}).get("role")
                in expected_caps_by_role
                and allocation.get("query_cap")
                == expected_caps_by_role[
                    agent_by_id[allocation["agent_id"]]["role"]
                ]
                for allocation in discovery_allocations
            )
        if not cap_split_valid:
            findings.append(
                Finding(
                    "MATCHED_DISCOVERY_ALLOCATION_SPLIT_INVALID",
                    "ERROR",
                    "Matched initial discovery must use the exact role-bound 22/22/22/21/21 audited split or six 18-query shadow allocations.",
                    manifest_name,
                )
            )
    certified_allocation_ids = {
        allocation_id
        for allocation_id in allocation_resources
        if allocation_metering_exact.get(allocation_id) is True
    }
    resource_contributors_complete = True
    for agent_id, agent in agent_by_id.items():
        owned_allocations = allocations_by_agent.get(agent_id, [])
        if agent.get("stage") in ALLOCATION_STAGES and not owned_allocations:
            findings.append(Finding("AGENT_ALLOCATION_MISSING", "UNKNOWN", f"V2 agent {agent_id} has no preregistered allocation record.", manifest_name, agent.get("_line"), (agent_id,)))
            resource_contributors_complete = False
            continue
        agent_resource_record = agent.get("resources")
        parsed_agent_resources = {
            key: (
                _as_decimal(agent_resource_record.get(key))
                if isinstance(agent_resource_record, dict)
                and isinstance(agent_resource_record.get(key), int)
                and not isinstance(agent_resource_record.get(key), bool)
                else None
            )
            for key in (
                "uncached_input_tokens",
                "output_tokens",
                "elapsed_microseconds",
            )
        }
        if any(value is None for value in parsed_agent_resources.values()):
            findings.append(Finding("AGENT_RESOURCE_TELEMETRY_INCOMPLETE", "UNKNOWN", f"V2 agent {agent_id} lacks exact resources for allocation reconciliation.", manifest_name, agent.get("_line"), (agent_id,)))
            certified_allocation_ids.difference_update(owned_allocations)
            resource_contributors_complete = False
            continue
        start, end = agent_times.get(agent_id, (None, None))
        actual_elapsed = (
            _elapsed_microseconds(start, end)
            if start is not None and end is not None and end >= start
            else None
        )
        if (
            actual_elapsed is None
            or parsed_agent_resources["elapsed_microseconds"]
            != Decimal(actual_elapsed)
        ):
            findings.append(Finding("AGENT_ELAPSED_MISMATCH", "ERROR", f"V2 agent {agent_id} elapsed_microseconds must exactly equal timestamp-derived active time.", manifest_name, agent.get("_line"), (agent_id,)))
            certified_allocation_ids.difference_update(owned_allocations)
            resource_contributors_complete = False
        allocation_telemetry_exact = all(
            allocation_id in allocation_resources
            and allocation_metering_exact.get(allocation_id) is True
            for allocation_id in owned_allocations
        )
        if (
            not agent_metering_exact.get(agent_id, False)
            or not allocation_telemetry_exact
        ):
            findings.append(
                Finding(
                    "RESOURCE_TOTAL_UNCERTIFIED",
                    "UNKNOWN",
                    f"Agent {agent_id}'s allocation totals cannot be certified until every metering basis and exact resource record is available.",
                    manifest_name,
                    agent.get("_line"),
                    (agent_id,),
                )
            )
            certified_allocation_ids.difference_update(owned_allocations)
            resource_contributors_complete = False
            continue
        for key, agent_value in parsed_agent_resources.items():
            allocation_values = [
                allocation_resources[allocation_id][key]
                for allocation_id in owned_allocations
            ]
            if sum(allocation_values, Decimal("0")) != agent_value:
                findings.append(Finding("ALLOCATION_AGENT_RESOURCE_MISMATCH", "ERROR", f"Allocation {key} sums do not exactly reconcile to owning agent {agent_id}.", manifest_name, agent.get("_line"), (agent_id,)))
                certified_allocation_ids.difference_update(owned_allocations)
                resource_contributors_complete = False

    orphaned_allocation_ids = {
        allocation_id
        for allocation_id, allocation in allocation_by_id.items()
        if allocation.get("agent_id") not in agent_by_id
    }
    if orphaned_allocation_ids:
        certified_allocation_ids.difference_update(orphaned_allocation_ids)
        resource_contributors_complete = False
    resource_telemetry_complete = (
        resource_contributors_complete
        and bool(allocation_by_id)
        and certified_allocation_ids == set(allocation_by_id)
    )

    allocation_resource_totals = {
        key: sum(
            (allocation_resources[allocation_id][key] for allocation_id in certified_allocation_ids),
            Decimal("0"),
        )
        for key in (
            "uncached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
        )
    }
    resources["certified_allocation_totals"] = {
        key: int(value)
        for key, value in allocation_resource_totals.items()
    }
    resources["resource_totals_certified"] = resource_telemetry_complete

    query_by_id: dict[str, dict[str, Any]] = {}
    query_times: dict[str, datetime] = {}
    query_entities: dict[str, set[str]] = {}
    queries_by_allocation: dict[str, set[str]] = defaultdict(set)
    invalid_queries: set[str] = set()
    normalized_query_owners: dict[str, str] = {}
    for query in query_records:
        query_id = query.get("query_id")
        line = query.get("_line")
        if not isinstance(query_id, str) or not query_id.strip():
            findings.append(Finding("QUERY_ID_MISSING", "ERROR", "V2 query has no stable query_id.", manifest_name, line))
            continue
        if query_id in query_by_id:
            findings.append(Finding("QUERY_ID_DUPLICATE", "ERROR", f"V2 query ID {query_id} is duplicated.", manifest_name, line, (query_id,)))
        query_by_id[query_id] = query
        if set(query) - {"_line"} != V2_QUERY_FIELDS:
            findings.append(Finding("V2_QUERY_FIELDS_INVALID", "ERROR", f"Query {query_id} must use the exact closed V2 query schema.", manifest_name, line, (query_id,)))
            invalid_queries.add(query_id)
        if not _normalize_query(query.get("query")):
            findings.append(Finding("QUERY_TEXT_INVALID", "ERROR", f"Query {query_id} has empty or invalid query text.", manifest_name, line, (query_id,)))
            invalid_queries.add(query_id)
        stage = query.get("stage")
        if stage not in RESEARCH_STAGES:
            findings.append(Finding("QUERY_STAGE_INVALID", "ERROR", f"Query {query_id} is attached to non-research stage {stage!r}.", manifest_name, line, (query_id,)))
            invalid_queries.add(query_id)
        allocation_id = query.get("allocation_id")
        allocation = allocation_by_id.get(allocation_id) if isinstance(allocation_id, str) else None
        if allocation is None:
            findings.append(Finding("QUERY_ALLOCATION_UNKNOWN", "ERROR", f"Query {query_id} lacks a known allocation_id.", manifest_name, line, (query_id,)))
            invalid_queries.add(query_id)
        else:
            if (
                query.get("scope_id") != scope_id
                or query.get("arm") != expected_arm
                or query.get("agent_id") != allocation.get("agent_id")
                or query.get("stage") != allocation.get("stage")
            ):
                findings.append(Finding("QUERY_ALLOCATION_CONTEXT_MISMATCH", "ERROR", f"Query {query_id} differs from allocation {allocation_id}'s scope, arm, agent, or stage.", manifest_name, line, (query_id, allocation_id)))
                invalid_queries.add(query_id)
        entities, entities_valid = _valid_string_list(query.get("entity_ids"))
        if not entities_valid:
            findings.append(Finding("QUERY_ENTITY_LINK_MISSING", "ERROR", f"Query {query_id} has no typed entity_ids.", manifest_name, line, (query_id,)))
            entities = []
            invalid_queries.add(query_id)
        query_entities[query_id] = set(entities)
        if isinstance(allocation_id, str) and allocation is not None:
            if not set(entities).issubset(allocation_entities.get(allocation_id, set())):
                findings.append(Finding("QUERY_ALLOCATION_ENTITY_MISMATCH", "ERROR", f"Query {query_id} references entities outside allocation {allocation_id}.", manifest_name, line, (query_id, allocation_id)))
                invalid_queries.add(query_id)
            normalized = _normalize_query(query.get("query"))
            if normalized:
                queries_by_allocation[allocation_id].add(normalized)
                prior_owner = normalized_query_owners.get(normalized)
                if prior_owner is not None and prior_owner != allocation_id:
                    findings.append(Finding("QUERY_DUPLICATED_ACROSS_ALLOCATIONS", "ERROR", f"Normalized query {query_id} is reused across allocations {prior_owner} and {allocation_id}.", manifest_name, line, (query_id, prior_owner, allocation_id)))
                    invalid_queries.add(query_id)
                normalized_query_owners[normalized] = allocation_id
        occurred_at = _parse_timestamp(query.get("occurred_at"))
        if occurred_at is not None:
            query_times[query_id] = occurred_at
            agent_id = query.get("agent_id")
            agent_start, agent_end = agent_times.get(str(agent_id), (None, None))
            allocation_created = allocation_times.get(str(allocation_id))
            if (
                agent_start is None
                or agent_end is None
                or not (agent_start <= occurred_at <= agent_end)
                or allocation_created is None
                or allocation_created >= occurred_at
            ):
                findings.append(Finding("QUERY_CHAIN_TIME_INVALID", "ERROR", f"Query {query_id} must occur at/after agent start, at/before agent end, and strictly after allocation registration.", manifest_name, line, (query_id,)))
                invalid_queries.add(query_id)
        else:
            invalid_queries.add(query_id)
    for allocation_id, allocation in allocation_by_id.items():
        observed = len(queries_by_allocation.get(allocation_id, set()))
        if allocation.get("used_unique_queries") != observed:
            findings.append(Finding("ALLOCATION_QUERY_COUNT_MISMATCH", "ERROR", f"Allocation {allocation_id} declares {allocation.get('used_unique_queries')!r} used queries; observed {observed}.", manifest_name, allocation.get("_line"), (allocation_id,)))
    calls_by_id: dict[str, dict[str, Any]] = {}
    calls_by_query: dict[str, list[dict[str, Any]]] = defaultdict(list)
    call_times: dict[str, datetime] = {}
    for event in tool_records:
        call_id = event.get("call_id")
        query_id = event.get("query_id")
        line = event.get("_line")
        contract_invalid = False
        if not isinstance(call_id, str) or not call_id.strip():
            findings.append(Finding("V2_TOOL_EVENT_CONTRACT_INVALID", "ERROR", "V2 tool event has no stable call_id.", manifest_name, line))
            continue
        if call_id in calls_by_id:
            findings.append(Finding("TOOL_CALL_ID_DUPLICATE", "ERROR", f"Tool call ID {call_id} is duplicated.", manifest_name, line, (call_id,)))
            contract_invalid = True
        if set(event) - {"_line"} != V2_TOOL_EVENT_FIELDS:
            findings.append(Finding("V2_TOOL_EVENT_CONTRACT_INVALID", "ERROR", f"Tool event {call_id} must use the exact closed V2 tool-event schema.", manifest_name, line, (call_id,)))
            contract_invalid = True
        if (
            event.get("tool") not in V2_RESEARCH_TOOLS
            or event.get("event_type") not in V2_RESEARCH_TOOL_EVENT_TYPES
        ):
            findings.append(Finding("V2_TOOL_EVENT_CONTRACT_INVALID", "ERROR", f"Tool event {call_id} must be an exact allowed research tool/event pair; aliases and external-call events are forbidden.", manifest_name, line, (call_id,)))
            contract_invalid = True
        if not isinstance(query_id, str) or query_id not in query_by_id:
            findings.append(Finding("V2_TOOL_EVENT_CONTRACT_INVALID", "ERROR", f"Tool event {call_id} must reciprocally reference one known query_id.", manifest_name, line, (call_id, str(query_id))))
            continue
        calls_by_id[call_id] = event
        calls_by_query[query_id].append(event)
        occurred_at = _parse_timestamp(event.get("occurred_at"))
        if occurred_at is not None:
            call_times[call_id] = occurred_at
        query = query_by_id[query_id]
        agent_start, agent_end = agent_times.get(str(event.get("agent_id")), (None, None))
        if (
            event.get("scope_id") != scope_id
            or event.get("arm") != expected_arm
            or event.get("allocation_id") != query.get("allocation_id")
            or event.get("agent_id") != query.get("agent_id")
            or event.get("stage") != query.get("stage")
            or occurred_at is None
            or query_times.get(query_id) is None
            or occurred_at <= query_times[query_id]
            or agent_start is None
            or agent_end is None
            or not (agent_start < occurred_at <= agent_end)
        ):
            findings.append(Finding("TOOL_QUERY_CHAIN_MISMATCH", "ERROR", f"Tool call {call_id} breaks query {query_id}'s scope, context, or chronology.", manifest_name, event.get("_line"), (call_id, query_id)))
            invalid_queries.add(query_id)
        if contract_invalid:
            invalid_queries.add(query_id)

    sources_by_query: dict[str, list[dict[str, Any]]] = defaultdict(list)
    sources_by_call: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_by_id: dict[str, dict[str, Any]] = {}
    source_times: dict[str, datetime] = {}
    source_query_id: dict[str, str] = {}
    for source in source_records:
        source_id = source.get("source_event_id")
        query_id = source.get("query_id")
        call_id = source.get("call_id")
        line = source.get("_line")
        if not isinstance(source_id, str) or not source_id.strip():
            findings.append(Finding("SOURCE_EVENT_ID_INVALID", "ERROR", "V2 source_open has no stable source_event_id.", manifest_name, line))
            continue
        if source_id in source_by_id:
            findings.append(Finding("SOURCE_EVENT_ID_DUPLICATE", "ERROR", f"Source event ID {source_id} is duplicated.", manifest_name, line, (source_id,)))
        source_by_id[source_id] = source
        if set(source) - {"_line"} != V2_SOURCE_OPEN_FIELDS:
            findings.append(Finding("V2_SOURCE_FIELDS_INVALID", "ERROR", f"Source {source_id} must use the exact closed V2 source-open schema.", manifest_name, line, (source_id,)))
        if not _normalize_source_url(source.get("url")):
            findings.append(Finding("SOURCE_URL_INVALID", "ERROR", f"Source {source_id} must carry a non-empty exact URL.", manifest_name, line, (source_id,)))
        if isinstance(query_id, str):
            sources_by_query[query_id].append(source)
            source_query_id[source_id] = query_id
        if isinstance(call_id, str):
            sources_by_call[call_id].append(source)
        source_time = _parse_timestamp(source.get("occurred_at"))
        if source_time is not None:
            source_times[source_id] = source_time
        query = query_by_id.get(query_id) if isinstance(query_id, str) else None
        call = calls_by_id.get(call_id) if isinstance(call_id, str) else None
        source_entities, entities_valid = _valid_string_list(source.get("entity_ids"))
        agent_start, agent_end = agent_times.get(str(source.get("agent_id")), (None, None))
        broken = query is None or call is None
        if query is not None and call is not None:
            broken = broken or (
                call.get("query_id") != query_id
                or source.get("scope_id") != scope_id
                or source.get("arm") != expected_arm
                or source.get("allocation_id") != query.get("allocation_id")
                or source.get("agent_id") != query.get("agent_id")
                or source.get("stage") != query.get("stage")
            )
        if (
            not entities_valid
            or (isinstance(query_id, str) and not set(source_entities).issubset(query_entities.get(query_id, set())))
            or source_time is None
            or not isinstance(call_id, str)
            or call_times.get(call_id) is None
            or source_time <= call_times[call_id]
            or agent_start is None
            or agent_end is None
            or not (agent_start < source_time <= agent_end)
        ):
            broken = True
        if broken:
            findings.append(Finding("SOURCE_TOOL_CHAIN_MISMATCH", "ERROR", f"Source {source_id} lacks a direct matching call_id or breaks scope, entity, or chronology rules.", manifest_name, source.get("_line"), (source_id, str(query_id), str(call_id))))
            if isinstance(query_id, str):
                invalid_queries.add(query_id)

    evidence_by_id = {
        record.get("evidence_id"): record
        for record in evidence_records
        if isinstance(record.get("evidence_id"), str)
    }
    evidence_sources_by_id: dict[str, set[str]] = {}
    for evidence_id, evidence in evidence_by_id.items():
        source_ids, links_valid = _valid_string_list(evidence.get("source_event_ids"))
        evidence_sources_by_id[str(evidence_id)] = set(source_ids)
        evidence_entities, entities_valid = _valid_string_list(evidence.get("entity_ids"))
        evidence_time = _parse_timestamp(evidence.get("recorded_at"))
        evidence_required_fields = {
            "record_type",
            "scope_id",
            "allocation_id",
            "agent_id",
            "arm",
            "stage",
            "evidence_id",
            "direction_id",
            "entity_ids",
            "source_event_ids",
            "recorded_at",
            "decision_critical",
            "status",
            "proposition",
            "source",
            "cheapest_resolving_test",
        }
        evidence_context_invalid = (
            evidence.get("scope_id") != scope_id
            or evidence.get("arm") != expected_arm
            or not links_valid
            or not entities_valid
            or evidence_time is None
            or not evidence_required_fields.issubset(set(evidence) - {"_line"})
            or not set(evidence_entities).issubset(known_entity_ids)
            or evidence.get("status") not in ALLOWED_EVIDENCE_STATUSES
            or not isinstance(evidence.get("decision_critical"), bool)
        )
        if evidence_context_invalid:
            findings.append(Finding("EVIDENCE_CHAIN_CONTEXT_MISMATCH", "ERROR", f"Evidence {evidence_id} lacks exact V2 scope, arm, source, entity, or timing telemetry.", ledger_name, evidence.get("_line"), (str(evidence_id),)))
        for source_id in source_ids:
            source = source_by_id.get(source_id)
            query_id = source_query_id.get(source_id)
            source_evidence, source_links_valid = _valid_string_list(source.get("evidence_ids")) if isinstance(source, dict) else ([], False)
            source_entities, source_entities_valid = _valid_string_list(source.get("entity_ids")) if isinstance(source, dict) else ([], False)
            query = query_by_id.get(query_id) if isinstance(query_id, str) else None
            expected_agent_id = source.get("agent_id") if isinstance(source, dict) else None
            agent_start, agent_end = agent_times.get(str(expected_agent_id), (None, None))
            if (
                evidence_context_invalid
                or
                source is None
                or query is None
                or not source_links_valid
                or evidence_id not in source_evidence
                or not source_entities_valid
                or not set(evidence_entities).issubset(set(source_entities))
                or evidence.get("allocation_id") != source.get("allocation_id")
                or evidence.get("agent_id") != expected_agent_id
                or evidence.get("arm") != source.get("arm")
                or evidence.get("stage") != source.get("stage")
                or evidence_time is None
                or source_times.get(source_id) is None
                or evidence_time <= source_times[source_id]
                or agent_start is None
                or agent_end is None
                or not (agent_start < evidence_time <= agent_end)
            ):
                findings.append(Finding("EVIDENCE_SOURCE_CHAIN_MISMATCH", "ERROR", f"Evidence {evidence_id} and source {source_id} are not reciprocal or chronological on the same entities.", ledger_name, evidence.get("_line"), (str(evidence_id), source_id)))
                if isinstance(query_id, str):
                    invalid_queries.add(query_id)

    for call_id, call in calls_by_id.items():
        if not sources_by_call.get(call_id):
            query_id = call.get("query_id")
            findings.append(
                Finding(
                    "TOOL_SOURCE_CHAIN_INCOMPLETE",
                    "ERROR",
                    f"Tool call {call_id} has no directly linked source-open record.",
                    manifest_name,
                    call.get("_line"),
                    (call_id, str(query_id)),
                )
            )
            if isinstance(query_id, str):
                invalid_queries.add(query_id)
    for source_id, source in source_by_id.items():
        linked_evidence, links_valid = _valid_string_list(source.get("evidence_ids"))
        query_id = source_query_id.get(source_id)
        if (
            not links_valid
            or any(
                evidence_id not in evidence_by_id
                or source_id not in evidence_sources_by_id.get(evidence_id, set())
                for evidence_id in linked_evidence
            )
        ):
            findings.append(
                Finding(
                    "SOURCE_EVIDENCE_CHAIN_INCOMPLETE",
                    "ERROR",
                    f"Source {source_id} does not have complete reciprocal evidence links.",
                    manifest_name,
                    source.get("_line"),
                    (source_id, str(query_id)),
                )
            )
            if isinstance(query_id, str):
                invalid_queries.add(query_id)

    for agent_id, facts in development_trace_facts.items():
        manifest_call_ids = {
            call_id
            for call_id, call in calls_by_id.items()
            if call.get("agent_id") == agent_id
        }
        trace_calls = facts.get("calls", {})
        trace_call_ids = set(trace_calls) if isinstance(trace_calls, dict) else set()
        if manifest_call_ids != trace_call_ids:
            findings.append(
                Finding(
                    "DEVELOPMENT_TRACE_CALL_SET_MISMATCH",
                    "ERROR",
                    f"Development agent {agent_id} raw web-call IDs differ from its complete manifest tool-event set.",
                    manifest_name,
                    agent_by_id[agent_id].get("_line"),
                    (agent_id,),
                )
            )
        for call_id in sorted(manifest_call_ids & trace_call_ids):
            call = calls_by_id[call_id]
            query_id = call.get("query_id")
            query = query_by_id.get(query_id) if isinstance(query_id, str) else None
            linked_sources = sources_by_call.get(call_id, [])
            trace_call = trace_calls[call_id]
            if query is None or len(linked_sources) != 1:
                findings.append(Finding("DEVELOPMENT_TRACE_SOURCE_MISMATCH", "ERROR", f"Development call {call_id} must map to exactly one query and one source event.", manifest_name, call.get("_line"), (agent_id, call_id)))
                continue
            source = linked_sources[0]
            opened_url = source.get("url")
            raw_input = trace_call.get("raw_input")
            expected_query = (
                _trace_query_text(raw_input, str(opened_url))
                if isinstance(raw_input, str)
                else trace_call.get("query_text")
            )
            output_strings = trace_call.get("output_strings")
            url_proven = (
                isinstance(opened_url, str)
                and isinstance(output_strings, list)
                and any(
                    isinstance(value, str) and opened_url in value
                    for value in output_strings
                )
            )
            if expected_query != _normalize_query(query.get("query")) or not url_proven:
                findings.append(
                    Finding(
                        "DEVELOPMENT_TRACE_SOURCE_MISMATCH",
                        "ERROR",
                        f"Development call {call_id} query text or source URL is not present in that exact raw tool call/result.",
                        manifest_name,
                        call.get("_line"),
                        (agent_id, call_id),
                    )
                )
                if isinstance(query_id, str):
                    invalid_queries.add(query_id)

    certified_query_ids: set[str] = set()
    certified_source_ids: set[str] = set()
    for query_id, query in query_by_id.items():
        if query.get("stage") not in RESEARCH_STAGES:
            continue
        linked_calls = calls_by_query.get(query_id, [])
        linked_sources = sources_by_query.get(query_id, [])
        has_closed_source = False
        for source in linked_sources:
            source_id = source.get("source_event_id")
            linked_evidence, valid_links = _valid_string_list(source.get("evidence_ids"))
            if (
                isinstance(source_id, str)
                and valid_links
                and any(
                    evidence_id in evidence_by_id
                    and source_id in evidence_sources_by_id.get(evidence_id, set())
                    for evidence_id in linked_evidence
                )
            ):
                has_closed_source = True
                certified_source_ids.add(source_id)
        if not linked_calls or not has_closed_source:
            findings.append(Finding("QUERY_CHAIN_INCOMPLETE", "ERROR", f"Query {query_id} does not complete allocation→agent→tool→source→evidence ancestry.", manifest_name, query.get("_line"), (query_id,)))
            invalid_queries.add(query_id)
        if query_id not in invalid_queries:
            certified_query_ids.add(query_id)

    for evidence_id, evidence in evidence_by_id.items():
        entity_ids, valid = _valid_string_list(evidence.get("entity_ids"))
        if not valid or not set(entity_ids).issubset(known_entity_ids):
            findings.append(Finding("EVIDENCE_ENTITY_ANCESTRY_INVALID", "ERROR", f"Evidence {evidence_id} does not terminate in registered entities.", ledger_name, evidence.get("_line"), (str(evidence_id),)))

    checkpoint_times = {
        str(record.get("state")): parsed
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
        and (parsed := _parse_timestamp(record.get("occurred_at"))) is not None
    }
    level2_records = [
        record for record in ledger_records if record.get("record_type") == "level2"
    ]
    level2_by_concept = {
        str(record.get("concept_id")): record
        for record in level2_records
        if isinstance(record.get("concept_id"), str)
    }
    level2_allocations_by_entity: dict[str, list[str]] = defaultdict(list)
    closure_allocations_by_entity: dict[str, list[str]] = defaultdict(list)
    for allocation_id, allocation in allocation_by_id.items():
        entities = allocation_entities.get(allocation_id, set())
        if allocation.get("stage") == "level2":
            for entity_id in entities:
                level2_allocations_by_entity[entity_id].append(allocation_id)
        elif allocation.get("stage") == "fact_closure":
            for entity_id in entities:
                closure_allocations_by_entity[entity_id].append(allocation_id)

    for concept_id, level2_record in level2_by_concept.items():
        selected_at = _parse_timestamp(level2_record.get("selected_at"))
        completed_at = _parse_timestamp(level2_record.get("completed_at"))
        linked_evidence_ids, evidence_ids_valid = _valid_string_list(
            level2_record.get("evidence_ids")
        )
        owned_allocations = level2_allocations_by_entity.get(concept_id, [])
        if len(owned_allocations) != 1:
            findings.append(
                Finding(
                    "LEVEL2_ALLOCATION_ANCESTRY_INVALID",
                    "ERROR",
                    f"Level-2 concept {concept_id} must have exactly one single-candidate allocation.",
                    ledger_name,
                    level2_record.get("_line"),
                    (concept_id,),
                )
            )
        allocation_id = owned_allocations[0] if len(owned_allocations) == 1 else None
        allocation_query_times = [
            query_times[query_id]
            for query_id, query in query_by_id.items()
            if query.get("allocation_id") == allocation_id and query_id in query_times
        ]
        if (
            selected_at is None
            or completed_at is None
            or selected_at >= completed_at
            or (
                allocation_query_times
                and selected_at > min(allocation_query_times)
            )
            or (
                checkpoint_times.get("level2_complete") is not None
                and completed_at >= checkpoint_times["level2_complete"]
            )
        ):
            findings.append(
                Finding(
                    "LEVEL2_LIFECYCLE_ORDER_INVALID",
                    "ERROR",
                    f"Level-2 concept {concept_id} must be selected before research, completed later, and finish strictly before level2_complete.",
                    ledger_name,
                    level2_record.get("_line"),
                    (concept_id,),
                )
            )
        if matched_initial and level2_record.get("development_status") != "complete":
            findings.append(Finding("MATCHED_LEVEL2_INCOMPLETE", "ERROR", f"Matched initial Level-2 concept {concept_id} must be complete.", ledger_name, level2_record.get("_line"), (concept_id,)))
        if not evidence_ids_valid:
            findings.append(Finding("LEVEL2_EVIDENCE_ANCESTRY_INVALID", "ERROR", f"Level-2 concept {concept_id} requires non-empty evidence_ids.", ledger_name, level2_record.get("_line"), (concept_id,)))
            linked_evidence_ids = []
        for evidence_id in linked_evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            evidence_entities, entities_valid = _valid_string_list(
                evidence.get("entity_ids") if isinstance(evidence, dict) else None
            )
            evidence_time = _parse_timestamp(evidence.get("recorded_at")) if isinstance(evidence, dict) else None
            if (
                not isinstance(evidence, dict)
                or evidence.get("stage") != "level2"
                or evidence.get("allocation_id") != allocation_id
                or not entities_valid
                or set(evidence_entities) != {concept_id}
                or selected_at is None
                or completed_at is None
                or evidence_time is None
                or not (selected_at <= evidence_time <= completed_at)
            ):
                findings.append(
                    Finding(
                        "LEVEL2_EVIDENCE_ANCESTRY_INVALID",
                        "ERROR",
                        f"Level-2 concept {concept_id} evidence {evidence_id} must be same-concept, same-allocation, stage=level2, and inside its selected/completed interval.",
                        ledger_name,
                        level2_record.get("_line"),
                        (concept_id, str(evidence_id)),
                    )
                )

    if not closure_cohort_sealed:
        return

    closure_path_value = run_record.get("fact_closure_candidates_file")
    closure_digest = run_record.get("fact_closure_candidates_sha256")
    closure_path = _strict_run_file(run_dir, closure_path_value, excluded_roots)
    closure_payload: dict[str, Any] | None = None
    if (
        closure_path_value != "02d_fact_closure_candidates.json"
        or closure_path is None
        or not isinstance(closure_digest, str)
        or closure_digest != _sha256(closure_path[0])
    ):
        findings.append(
            Finding(
                "FACT_CLOSURE_COHORT_BINDING_INVALID",
                "ERROR",
                "V2 run must bind the exact run-local 02d_fact_closure_candidates.json bytes and SHA-256.",
                str(closure_path_value or ""),
            )
        )
    else:
        try:
            parsed_payload = json.loads(closure_path[0].read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            parsed_payload = None
        if isinstance(parsed_payload, dict):
            closure_payload = parsed_payload
    candidate_ids: list[str] = []
    closure_selected_at: datetime | None = None
    if closure_payload is None or set(closure_payload) != {
        "candidate_ids",
        "creator_agent_id",
        "selected_at",
        "seed",
    }:
        findings.append(Finding("FACT_CLOSURE_COHORT_SCHEMA_INVALID", "ERROR", "The fact-closure cohort must use the exact closed candidate_ids/creator_agent_id/selected_at/seed payload.", str(closure_path_value or "")))
    else:
        candidate_ids, candidates_valid = _valid_string_list(
            closure_payload.get("candidate_ids")
        )
        closure_selected_at = _parse_timestamp(closure_payload.get("selected_at"))
        expected_creator = "root-orchestrator"
        if run_record.get("mode") == "archipelago_lite_shadow":
            selector_ids = [
                agent_id
                for agent_id, agent in agent_by_id.items()
                if agent.get("stage") == "finalist_selector"
            ]
            expected_creator = selector_ids[0] if len(selector_ids) == 1 else ""
        if (
            not candidates_valid
            or len(candidate_ids) != len(set(candidate_ids))
            or closure_payload.get("creator_agent_id") != expected_creator
            or closure_payload.get("selected_at")
            != run_record.get("fact_closure_selected_at")
            or closure_payload.get("seed") != run_record.get("candidate_order_seed")
            or closure_selected_at is None
        ):
            findings.append(Finding("FACT_CLOSURE_COHORT_SCHEMA_INVALID", "ERROR", "Fact-closure candidates, exact owner, selection time, and candidate_order_seed do not reconcile.", str(closure_path_value or "")))
        if run_record.get("mode") == "archipelago_lite_shadow" and expected_creator:
            selector_end = agent_times.get(expected_creator, (None, None))[1]
            if selector_end is None or closure_selected_at is None or selector_end >= closure_selected_at:
                findings.append(Finding("FACT_CLOSURE_SELECTION_ORDER_INVALID", "ERROR", "The isolated finalist selector must finish strictly before its cohort is sealed.", str(closure_path_value or ""), node_ids=(expected_creator,)))

    if isinstance(aggregate, dict) and len(candidate_ids) != aggregate.get("fact_closure"):
        findings.append(Finding("FACT_CLOSURE_COHORT_COUNT_INVALID", "ERROR", "The sealed closure cohort does not match aggregate_opportunity fact_closure.", str(closure_path_value or "")))
    completed_level2_ids = {
        concept_id
        for concept_id, record in level2_by_concept.items()
        if record.get("development_status") == "complete"
    }
    if not set(candidate_ids).issubset(completed_level2_ids):
        findings.append(Finding("FACT_CLOSURE_COHORT_ANCESTRY_INVALID", "ERROR", "Every closure candidate must be an exact completed Level-2 concept ID.", str(closure_path_value or ""), node_ids=tuple(sorted(set(candidate_ids) - completed_level2_ids))))
    if not closure_complete:
        return
    if set(closure_allocations_by_entity) != set(candidate_ids) or any(
        len(closure_allocations_by_entity.get(candidate_id, [])) != 1
        for candidate_id in candidate_ids
    ):
        findings.append(Finding("FACT_CLOSURE_ALLOCATION_SET_INVALID", "ERROR", "The sealed closure cohort must map one-to-one to single-candidate fact-closure allocations.", manifest_name))
    first_closure_query = min(
        (
            occurred
            for query_id, occurred in query_times.items()
            if query_by_id.get(query_id, {}).get("stage") == "fact_closure"
        ),
        default=None,
    )
    if closure_selected_at is None or first_closure_query is None or closure_selected_at >= first_closure_query:
        findings.append(Finding("FACT_CLOSURE_SELECTION_ORDER_INVALID", "ERROR", "The exact closure cohort must be selected strictly before the first closure query.", str(closure_path_value or "")))

    closure_agent_entities = [
        next(iter(agent_assignments[agent_id]))
        for agent_id, agent in agent_by_id.items()
        if agent.get("stage") == "fact_closure"
        and len(agent_assignments.get(agent_id, set())) == 1
    ]
    if Counter(closure_agent_entities) != Counter(candidate_ids):
        findings.append(
            Finding(
                "DEVELOPMENT_RESOURCE_PARTITION_INVALID",
                "ERROR",
                "The six fact-closure agents must map one-to-one to the sealed six-candidate cohort.",
                manifest_name,
            )
        )

    if not frozen_reached:
        return

    finalist_candidate_ids: list[str] = []
    for finalist in [record for record in ledger_records if record.get("record_type") == "finalist"]:
        finalist_id = str(finalist.get("finalist_id"))
        direction_id = finalist.get("direction_id")
        raw_ancestors, raw_valid = _valid_string_list(finalist.get("raw_ids"))
        candidate_matches = (
            ([direction_id] if isinstance(direction_id, str) and direction_id in candidate_ids else [])
            + ([value for value in raw_ancestors if value in candidate_ids] if raw_valid else [])
        )
        candidate_matches = list(dict.fromkeys(candidate_matches))
        candidate_id = candidate_matches[0] if len(candidate_matches) == 1 else None
        if candidate_id is None:
            findings.append(Finding("FINALIST_STAGE_ENTITY_CHAIN_INVALID", "ERROR", f"Finalist {finalist_id} must identify exactly one sealed closure candidate through direction_id or raw_ids.", ledger_name, finalist.get("_line"), (finalist_id,)))
            continue
        finalist_candidate_ids.append(candidate_id)
        frozen_at = _parse_timestamp(finalist.get("frozen_at"))
        finalist_evidence_ids, finalist_evidence_valid = _valid_string_list(
            finalist.get("evidence_ids")
        )
        has_valid_closure_evidence = False
        for evidence_id in finalist_evidence_ids:
            evidence = evidence_by_id.get(evidence_id)
            evidence_entities, entity_valid = _valid_string_list(
                evidence.get("entity_ids") if isinstance(evidence, dict) else None
            )
            evidence_time = _parse_timestamp(evidence.get("recorded_at")) if isinstance(evidence, dict) else None
            if (
                isinstance(evidence, dict)
                and evidence.get("stage") == "fact_closure"
                and evidence.get("decision_critical") is True
                and entity_valid
                and set(evidence_entities) == {candidate_id}
                and evidence.get("allocation_id")
                in closure_allocations_by_entity.get(candidate_id, [])
                and closure_selected_at is not None
                and evidence_time is not None
                and frozen_at is not None
                and closure_selected_at < evidence_time <= frozen_at
            ):
                has_valid_closure_evidence = True
        if not finalist_evidence_valid or not has_valid_closure_evidence:
            findings.append(Finding("FINALIST_STAGE_ENTITY_CHAIN_INVALID", "ERROR", f"Finalist {finalist_id} lacks exact decision-critical fact-closure evidence for sealed candidate {candidate_id} before freeze.", ledger_name, finalist.get("_line"), (finalist_id, candidate_id)))
    if Counter(finalist_candidate_ids) != Counter(candidate_ids):
        findings.append(Finding("FINALIST_CLOSURE_COHORT_MISMATCH", "ERROR", "Frozen finalists must be exactly the sealed closure cohort with one finalist per candidate and no substitution.", ledger_name))

    frozen_checkpoint = checkpoint_times.get("frozen")
    finalist_freeze_times = [
        parsed
        for record in ledger_records
        if record.get("record_type") == "finalist"
        and (parsed := _parse_timestamp(record.get("frozen_at"))) is not None
    ]
    if finalist_freeze_times and (
        frozen_checkpoint is None or max(finalist_freeze_times) >= frozen_checkpoint
    ):
        findings.append(Finding("FINALIST_FREEZE_CHECKPOINT_ORDER_INVALID", "ERROR", "Every finalist frozen_at must be strictly earlier than the frozen checkpoint.", ledger_name))

    development_allocation_ids = {
        allocation_id
        for allocation_id, allocation in allocation_by_id.items()
        if allocation.get("stage") in {"level2", "fact_closure"}
    }
    telemetry_complete = bool(development_allocation_ids) and development_allocation_ids.issubset(certified_allocation_ids)
    input_tokens = sum(
        (allocation_resources[allocation_id]["uncached_input_tokens"] for allocation_id in development_allocation_ids if allocation_id in certified_allocation_ids),
        Decimal("0"),
    )
    output_tokens = sum(
        (allocation_resources[allocation_id]["output_tokens"] for allocation_id in development_allocation_ids if allocation_id in certified_allocation_ids),
        Decimal("0"),
    )
    elapsed_microseconds = sum(
        (allocation_resources[allocation_id]["elapsed_microseconds"] for allocation_id in development_allocation_ids if allocation_id in certified_allocation_ids),
        Decimal("0"),
    )
    if not telemetry_complete:
        findings.append(Finding("DEVELOPMENT_RESOURCE_TELEMETRY_INCOMPLETE", "UNKNOWN", "Certified Level-2/fact-closure token or timing telemetry is incomplete.", manifest_name))

    level2_word_counts: list[int] = []
    frozen_word_counts: list[int] = []
    measurement = contract.get("dossier_measurement") if isinstance(contract, dict) else None
    counted_sections = (
        measurement.get("counted_sections")
        if isinstance(measurement, dict)
        else None
    )
    if run_record.get("cohort_kind") == "initial":
        for record in ledger_records:
            if record.get("record_type") == "level2" and record.get("development_status") == "complete":
                parsed = _strict_run_file(run_dir, record.get("artifact_path"), excluded_roots)
                words = (
                    _dossier_prose_word_count(parsed[0], counted_sections)
                    if parsed is not None and isinstance(counted_sections, list)
                    else None
                )
                if words is not None:
                    level2_word_counts.append(words)
            elif record.get("record_type") == "finalist":
                parsed = _strict_run_file(run_dir, record.get("artifact_path"), excluded_roots)
                words = (
                    _dossier_prose_word_count(parsed[0], counted_sections)
                    if parsed is not None and isinstance(counted_sections, list)
                    else None
                )
                if words is not None:
                    frozen_word_counts.append(words)
    depth_required = (
        run_record.get("cohort_kind") == "initial"
        and checkpoint not in {"selection", "freeze"}
    )
    if depth_required and (not level2_word_counts or not frozen_word_counts):
        findings.append(Finding("DEVELOPMENT_DEPTH_METRICS_INCOMPLETE", "UNKNOWN", "Initial complete Level-2 and frozen dossier byte metrics are incomplete.", ledger_name))

    def mean_or_none(values: list[int]) -> str | None:
        if not values:
            return None
        return str(Decimal(sum(values)) / Decimal(len(values)))

    development_metrics: dict[str, int | str | None] = {
        "level2_queries": sum(1 for query_id in certified_query_ids if query_by_id[query_id].get("stage") == "level2"),
        "level2_sources": len({
            normalized_url
            for source_id in certified_source_ids
            if source_query_id.get(source_id) in certified_query_ids
            and source_by_id[source_id].get("stage") == "level2"
            and (normalized_url := _normalize_source_url(source_by_id[source_id].get("url")))
        }),
        "fact_closure_queries": sum(1 for query_id in certified_query_ids if query_by_id[query_id].get("stage") == "fact_closure"),
        "fact_closure_sources": len({
            normalized_url
            for source_id in certified_source_ids
            if source_query_id.get(source_id) in certified_query_ids
            and source_by_id[source_id].get("stage") == "fact_closure"
            and (normalized_url := _normalize_source_url(source_by_id[source_id].get("url")))
        }),
        "development_input_tokens": int(input_tokens) if telemetry_complete else None,
        "development_output_tokens": int(output_tokens) if telemetry_complete else None,
        "development_elapsed_minutes": (
            str(elapsed_microseconds / Decimal(60_000_000))
            if telemetry_complete
            else None
        ),
        "level2_mean_words": mean_or_none(level2_word_counts),
        "frozen_mean_words": mean_or_none(frozen_word_counts),
    }
    resources["development_metrics"] = development_metrics

    declared_totals = run_record.get("resource_totals")
    if run_record.get("lifecycle_state") == "complete" and isinstance(declared_totals, dict):
        if set(declared_totals) != V2_CHECKPOINT_RESOURCE_FIELDS:
            findings.append(
                Finding(
                    "RESOURCE_TOTAL_FIELDS_INVALID",
                    "ERROR",
                    "Completed V2 resource_totals must use exactly unique_queries, uncached_input_tokens, output_tokens, and elapsed_microseconds.",
                    manifest_name,
                    run_record.get("_line"),
                )
            )
        for key in (
            "unique_queries",
            "uncached_input_tokens",
            "output_tokens",
            "elapsed_microseconds",
        ):
            raw_total = declared_totals.get(key)
            value = (
                _as_decimal(raw_total)
                if isinstance(raw_total, int) and not isinstance(raw_total, bool)
                else None
            )
            if value is None or value <= 0:
                findings.append(Finding("RESOURCE_TOTAL_ZERO_INVALID", "ERROR", f"Completed V2 run has missing or zero exact total {key}.", manifest_name, run_record.get("_line")))
        expected_run_values = {
            "unique_queries": Decimal(len({_normalize_query(item.get("query")) for item in query_records if _normalize_query(item.get("query"))})),
        }
        complete_checkpoints = [
            item
            for item in manifest_records
            if item.get("record_type") == "checkpoint"
            and item.get("state") == "complete"
        ]
        if len(complete_checkpoints) == 1:
            final_checkpoint_totals = complete_checkpoints[0].get("resource_totals")
            final_elapsed = (
                _as_decimal(final_checkpoint_totals.get("elapsed_microseconds"))
                if isinstance(final_checkpoint_totals, dict)
                else None
            )
            if final_elapsed is not None:
                expected_run_values["elapsed_microseconds"] = final_elapsed
            if isinstance(final_checkpoint_totals, dict):
                for key in V2_CHECKPOINT_RESOURCE_FIELDS:
                    declared_value = _as_decimal(declared_totals.get(key))
                    checkpoint_value = _as_decimal(final_checkpoint_totals.get(key))
                    if (
                        declared_value is None
                        or checkpoint_value is None
                        or declared_value != checkpoint_value
                    ):
                        findings.append(
                            Finding(
                                "RESOURCE_TOTAL_FINAL_CHECKPOINT_MISMATCH",
                                "ERROR",
                                f"Run resource_totals {key} must exactly mirror the terminal complete checkpoint.",
                                manifest_name,
                                run_record.get("_line"),
                            )
                        )
        else:
            findings.append(Finding("RESOURCE_TOTAL_FINAL_CHECKPOINT_MISSING", "ERROR", "Completed V2 run totals require exactly one terminal complete checkpoint.", manifest_name))
        if resource_telemetry_complete:
            expected_run_values.update(
                {
                    "uncached_input_tokens": allocation_resource_totals["uncached_input_tokens"],
                    "output_tokens": allocation_resource_totals["output_tokens"],
                }
            )
        else:
            findings.append(
                Finding(
                    "RESOURCE_TOTAL_UNCERTIFIED",
                    "UNKNOWN",
                    "Allocation/agent metering is incomplete, so partial certified sums are not compared with full declared run totals.",
                    manifest_name,
                    run_record.get("_line"),
                )
            )
        for key, expected_value in expected_run_values.items():
            declared_value = _as_decimal(declared_totals.get(key))
            if declared_value is None:
                findings.append(Finding("RESOURCE_TOTAL_FIELD_MISSING", "UNKNOWN", f"V2 resource_totals omit exact allocation-reconciled {key}.", manifest_name, run_record.get("_line")))
            elif declared_value != expected_value:
                findings.append(Finding("RESOURCE_TOTAL_MISMATCH", "ERROR", f"V2 resource {key}: declared {declared_value}, allocation-certified {expected_value}.", manifest_name, run_record.get("_line")))


def _scope_text_fingerprints(scope_dir: Path) -> tuple[set[str], set[str]]:
    titles: set[str] = set()
    paragraphs: set[str] = set()
    for path in _owned_files(scope_dir, set()):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            if path.stat().st_size > 5_000_000:
                continue
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        for line in text.splitlines():
            match = re.match(r"^#\s+(.+?)\s*$", line)
            if match:
                normalized = " ".join(match.group(1).casefold().split())
                if len(normalized) >= 3:
                    titles.add(normalized)
        paragraphs.update(_meaningful_paragraphs(text))
    return titles, paragraphs


def _audit_shadow_fingerprint_leaks(
    run_dir: Path,
    parent_ledger_records: list[dict[str, Any]],
    parent_manifest_records: list[dict[str, Any]],
    child_declarations: list[dict[str, Any]],
    excluded_roots: set[str],
    findings: list[Finding],
    *,
    legacy_agent_overlap_is_ambiguous: bool = False,
) -> None:
    run_dir = run_dir.resolve(strict=False)
    parent_ids = _scope_ledger_machine_ids(parent_ledger_records)
    parent_agent_entity_ids: set[str] = set()
    for record in parent_manifest_records:
        if record.get("record_type") != "agent":
            continue
        for key in ("assigned_ids", "output_ids"):
            values = record.get(key)
            if isinstance(values, list):
                parent_agent_entity_ids.update(
                    value.strip()
                    for value in values
                    if isinstance(value, str) and value.strip()
                )
    legacy_agent_ids = (
        parent_agent_entity_ids if legacy_agent_overlap_is_ambiguous else set()
    )
    scan_paths = list(_owned_files(run_dir, excluded_roots))
    for declaration in child_declarations:
        if declaration.get("relationship") != "regeneration":
            continue
        parsed = _strict_relative_directory(run_dir, declaration.get("relative_path"))
        if parsed is not None:
            scan_paths.extend(_owned_files(parsed[0], set()))

    for declaration in child_declarations:
        if declaration.get("relationship") != "shadow_child":
            continue
        parsed = _strict_relative_directory(run_dir, declaration.get("relative_path"))
        if parsed is None:
            continue
        child_dir = parsed[0]
        for child_path in _owned_files(child_dir, set()):
            child_relative = _relative_display(child_path, run_dir)
            if child_path.is_symlink():
                findings.append(Finding("CHILD_FINGERPRINT_SCAN_UNSAFE", "ERROR", "Shadow fingerprint source is a symlink and was not read.", child_relative))
            else:
                try:
                    if child_path.stat().st_size > 5_000_000:
                        findings.append(Finding("CHILD_FINGERPRINT_SCAN_INCOMPLETE", "ERROR", "Shadow fingerprint source exceeds the bounded scanner limit; the audit fails closed.", child_relative))
                except OSError:
                    findings.append(Finding("CHILD_FINGERPRINT_SCAN_INCOMPLETE", "UNKNOWN", "Shadow fingerprint source metadata is unreadable.", child_relative))
        child_ledger = child_dir / "02b_raw_to_direction_ledger.jsonl"
        child_records = _read_jsonl(child_ledger, []) if child_ledger.is_file() else []
        child_ids = _scope_ledger_machine_ids(child_records) - parent_ids
        child_titles, child_paragraphs = _scope_text_fingerprints(child_dir)
        for path in scan_paths:
            if not path.is_file():
                continue
            try:
                if path.is_symlink():
                    findings.append(Finding("CHILD_FINGERPRINT_SCAN_UNSAFE", "ERROR", "Parent leak-scan input is a symlink and was not read.", _relative_display(path, run_dir)))
                    continue
                if path.stat().st_size > 5_000_000:
                    findings.append(Finding("CHILD_FINGERPRINT_SCAN_INCOMPLETE", "ERROR", "Parent leak-scan input exceeds the bounded scanner limit; the audit fails closed.", _relative_display(path, run_dir)))
                    continue
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as exc:
                findings.append(
                    Finding(
                        "CHILD_FINGERPRINT_SCAN_INCOMPLETE",
                        "ERROR",
                        f"Leak-scan input cannot be read completely: {exc}.",
                        _relative_display(path, run_dir),
                    )
                )
                continue
            relative = _relative_display(path, run_dir)
            observed_child_ids = {
                candidate_id
                for candidate_id in child_ids
                if re.search(
                    rf"(?<![A-Za-z0-9_-]){re.escape(candidate_id)}(?![A-Za-z0-9_-])",
                    text,
                )
            }
            ambiguous_ids = sorted(observed_child_ids & legacy_agent_ids)
            leaked_ids = sorted(observed_child_ids - legacy_agent_ids)
            normalized_titles = {
                " ".join(match.group(1).casefold().split())
                for line in text.splitlines()
                for match in [re.match(r"^#\s+(.+?)\s*$", line)]
                if match
            }
            normalized_parent_text = " ".join(text.casefold().split())
            leaked_titles = sorted(
                title
                for title in child_titles
                if title in normalized_titles
                or re.search(
                    rf"(?<![\w]){re.escape(title)}(?![\w])",
                    normalized_parent_text,
                )
            )
            leaked_paragraphs = _meaningful_paragraphs(text) & child_paragraphs
            if leaked_ids:
                findings.append(
                    Finding(
                        "CHILD_FINGERPRINT_ID_LEAK",
                        "ERROR",
                        f"Parent-owned or regeneration text contains shadow-only entity IDs: {leaked_ids}.",
                        relative,
                        node_ids=tuple(leaked_ids),
                    )
                )
            if ambiguous_ids:
                findings.append(
                    Finding(
                        "LEGACY_CHILD_ID_OWNERSHIP_AMBIGUOUS",
                        "UNKNOWN",
                        f"Legacy parent evidence and child scope reuse IDs {ambiguous_ids}; ownership cannot be reconstructed with certainty.",
                        relative,
                        node_ids=tuple(ambiguous_ids),
                    )
                )
            if leaked_titles:
                findings.append(
                    Finding(
                        "CHILD_FINGERPRINT_TITLE_LEAK",
                        "ERROR",
                        f"Parent-owned or regeneration text contains {len(leaked_titles)} unique normalized shadow H1 title(s).",
                        relative,
                    )
                )
            if leaked_paragraphs:
                findings.append(
                    Finding(
                        "CHILD_FINGERPRINT_PARAGRAPH_LEAK",
                        "ERROR",
                        f"Parent-owned or regeneration text contains {len(leaked_paragraphs)} meaningful shadow paragraph fingerprint(s).",
                        relative,
                    )
                )


def _compare_development_parity(
    parent_metrics: dict[str, Any],
    child_metrics: dict[str, Any],
    child_scope_id: str,
    findings: list[Finding],
) -> None:
    for key in DEVELOPMENT_METRIC_KEYS:
        parent_value = _as_decimal(parent_metrics.get(key))
        child_value = _as_decimal(child_metrics.get(key))
        if parent_value is None or child_value is None:
            findings.append(
                Finding(
                    "PARITY_METRIC_INCOMPLETE",
                    "UNKNOWN",
                    f"Cannot compare derived metric {key} with child scope {child_scope_id}.",
                    node_ids=(child_scope_id,),
                )
            )
            continue
        denominator = max(abs(parent_value), abs(child_value))
        if denominator == 0:
            findings.append(
                Finding(
                    "PARITY_METRIC_INCOMPLETE",
                    "UNKNOWN",
                    f"Derived metric {key} is zero in both arms and cannot demonstrate matched opportunity for child scope {child_scope_id}.",
                    node_ids=(child_scope_id,),
                )
            )
            continue
        gap = abs(parent_value - child_value) / denominator
        if gap > Decimal("0.10"):
            findings.append(
                Finding(
                    "PARITY_METRIC_GAP",
                    "UNKNOWN",
                    f"Derived metric {key} differs by {(gap * Decimal('100'))}% from child scope {child_scope_id}; exactly 10% passes, greater than 10% is incomplete.",
                    node_ids=(child_scope_id,),
                )
            )


def _discover_nested_machine_runs(run_dir: Path) -> set[str]:
    discovered: set[str] = set()
    for current, directory_names, file_names in os.walk(run_dir, followlinks=False):
        current_path = Path(current)
        if current_path != run_dir and "00a_context_and_resource_manifest.jsonl" in file_names:
            discovered.add(current_path.relative_to(run_dir).as_posix())
        for name in tuple(directory_names):
            candidate = current_path / name
            if candidate.is_symlink() and (candidate / "00a_context_and_resource_manifest.jsonl").is_file():
                discovered.add(candidate.relative_to(run_dir).as_posix())
    return discovered


def _typed_downstream_content(path: Path, text: str) -> bool:
    structured_suffixes = {".json", ".jsonl"}
    typed_keys = {
        "record-type",
        "artifact-type",
        "event-type",
        "tool",
        "action",
        "command",
        "operation",
        "operation-name",
        "intent",
        "destination",
        "route",
        "call",
        "next-step",
        "stage",
        "routing-target",
        "result-type",
    }
    typed_key_forms = {
        form
        for key in typed_keys
        for form in (key, key.replace("-", ""))
    }
    routing_boolean_keys = {
        "validation-eligible",
        "can-route-to-validation",
    }
    routing_boolean_key_forms = {
        form
        for key in routing_boolean_keys
        for form in (key, key.replace("-", ""))
    }
    forbidden_values = {
        "evaluation",
        "evaluator",
        "validation",
        "validator",
        "advisory",
        "panel",
        "pivot",
        "scorecard",
        "adjudication",
        "confirmed_idea",
        "working_chat",
        "fresh_chat",
    }

    def forbidden_typed_value(value: Any) -> bool:
        if isinstance(value, str):
            canonical = _canonical_tool_name(value)
            return any(
                (normalized_token := _canonical_tool_name(token))
                and (
                    normalized_token == canonical
                    or normalized_token in canonical
                )
                for token in forbidden_values
            )
        if isinstance(value, dict):
            return any(forbidden_typed_value(child) for child in value.values())
        if isinstance(value, list):
            return any(forbidden_typed_value(child) for child in value)
        return False

    def contains(value: Any) -> bool:
        if isinstance(value, dict):
            for key, child in value.items():
                normalized_key = _canonical_tool_name(key)
                normalized_key_forms = {
                    normalized_key,
                    normalized_key.replace("-", ""),
                }
                if (
                    child is True
                    and normalized_key_forms & routing_boolean_key_forms
                ):
                    return True
                if (
                    normalized_key_forms & typed_key_forms
                    and forbidden_typed_value(child)
                ):
                    return True
                if contains(child):
                    return True
        elif isinstance(value, list):
            return any(contains(child) for child in value)
        return False

    stripped = text.strip()
    if path.suffix.casefold() in structured_suffixes or stripped.startswith(
        ("{", "[")
    ):
        values: list[Any] = []
        try:
            if path.suffix.casefold() == ".jsonl":
                values = [json.loads(line) for line in text.splitlines() if line.strip()]
            else:
                values = [json.loads(stripped)]
        except (json.JSONDecodeError, RecursionError):
            values = []
        if any(contains(value) for value in values):
            return True
    return bool(
        re.search(
            r"(?im)^#{1,6}\s+.*\b(?:evaluation|validator|validation|advisory|scorecard|adjudication|confirmed idea|panel result)\b",
            text,
        )
    )


def _audit_v2_nonrouting_owned_content(
    run_dir: Path,
    run_record: dict[str, Any],
    ledger_records: list[dict[str, Any]],
    excluded_roots: set[str],
    findings: list[Finding],
) -> None:
    if run_record.get("routing_state") != "frozen_nonrouting":
        return
    allowed_finalist_paths = {
        relative.casefold()
        for record in ledger_records
        if record.get("record_type") == "finalist"
        for _path, relative in [
            _canonical_run_path(run_dir, record.get("artifact_path"))
        ]
        if relative is not None
    }
    for path in _owned_files(run_dir, excluded_roots):
        if not path.is_file():
            continue
        relative = path.relative_to(run_dir)
        if path.is_symlink():
            findings.append(
                Finding(
                    "V2_NONROUTING_SCAN_UNSAFE",
                    "ERROR",
                    "Non-routing scope contains a symlinked scan target; escaped content was not read.",
                    relative.as_posix(),
                )
            )
            continue
        filename_match = _is_downstream_artifact(
            relative, allowed_finalist_paths=allowed_finalist_paths
        )
        try:
            if path.stat().st_size > 5_000_000:
                findings.append(
                    Finding(
                        "V2_NONROUTING_SCAN_INCOMPLETE",
                        "ERROR",
                        "Non-routing text exceeds the bounded content scanner; the audit fails closed.",
                        relative.as_posix(),
                    )
                )
                continue
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError):
            findings.append(
                Finding(
                    "V2_NONROUTING_SCAN_INCOMPLETE",
                    "ERROR",
                    "Non-routing content is unreadable.",
                    relative.as_posix(),
                )
            )
            continue
        if filename_match or _typed_downstream_content(path, text):
            findings.append(
                Finding(
                    "V2_NONROUTING_DOWNSTREAM_ARTIFACT",
                    "ERROR",
                    "A frozen_nonrouting V2 scope contains a filename- or content-typed downstream artifact.",
                    relative.as_posix(),
                )
            )


def _regeneration_contamination_content(path: Path, text: str) -> bool:
    if any(pattern.search(text) for pattern in PROHIBITED_PACKET_PATTERNS):
        return True
    if any(pattern.search(text) for pattern in REGENERATION_CONTAMINATION_PATTERNS):
        return True

    typed_keys = {
        "record-type",
        "artifact-type",
        "event-type",
        "tool",
        "action",
        "command",
        "operation",
        "operation-name",
        "intent",
        "destination",
        "route",
        "call",
        "next-step",
        "stage",
        "routing-target",
        "result-type",
        "role",
        "agent-role",
        "source-role",
    }
    typed_key_forms = {
        form
        for key in typed_keys
        for form in (key, key.replace("-", ""))
    }
    evaluator_signals = {
        "feedback",
        "output",
        "outputs",
        "result",
        "results",
        "assessment",
        "objection",
        "objections",
        "recommendation",
        "recommendations",
        "score",
        "scores",
        "ranking",
        "rankings",
        "verdict",
        "decision",
        "notes",
    }
    validator_signals = {
        "feedback",
        "output",
        "outputs",
        "result",
        "results",
        "objection",
        "objections",
        "recommendation",
        "recommendations",
        "score",
        "scores",
        "verdict",
        "decision",
    }
    ranking_signals = {
        "ranking",
        "rankings",
        "ranked",
        "score",
        "scores",
        "scored",
        "verdict",
        "selection",
        "recommendation",
        "result",
        "results",
    }
    output_signals = {
        "output",
        "outputs",
        "result",
        "results",
        "finding",
        "findings",
        "ranking",
        "rankings",
        "score",
        "scores",
        "selection",
        "selections",
        "shortlist",
        "finalist",
        "finalists",
        "candidate",
        "candidates",
        "cohort",
    }

    def canonical_structured_name(value: Any) -> str:
        if not isinstance(value, str):
            return ""
        camel_separated = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", value)
        return _canonical_tool_name(camel_separated)

    def substantive(value: Any) -> bool:
        if value is None or value is False:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (dict, list)):
            return bool(value)
        return True

    def forbidden_typed_value(value: Any) -> bool:
        if isinstance(value, str):
            parts = set(canonical_structured_name(value).split("-")) - {""}
            if parts & {
                "evaluation",
                "evaluator",
                "validation",
                "validator",
                "advisory",
                "judge",
                "panel",
            }:
                return True
            return bool(parts & {"shadow", "matched"} and parts & output_signals)
        if isinstance(value, dict):
            return any(forbidden_typed_value(child) for child in value.values())
        if isinstance(value, list):
            return any(forbidden_typed_value(child) for child in value)
        return False

    def contains(value: Any, ancestor_parts: frozenset[str] = frozenset()) -> bool:
        if isinstance(value, dict):
            for key, child in value.items():
                canonical_key = canonical_structured_name(key)
                key_parts = set(canonical_key.split("-")) - {""}
                path_parts = set(ancestor_parts) | key_parts
                key_forms = {canonical_key, canonical_key.replace("-", "")}
                if substantive(child):
                    if (
                        "evaluator" in path_parts
                        and (
                            canonical_key in {"evaluator", "advisory-evaluator"}
                            or bool(path_parts & evaluator_signals)
                        )
                    ):
                        return True
                    if (
                        {"advisory", "evaluation"}.issubset(path_parts)
                        and bool(path_parts & evaluator_signals)
                    ):
                        return True
                    if (
                        "validator" in path_parts
                        and bool(path_parts & validator_signals)
                    ):
                        return True
                    if (
                        path_parts & {"judge", "panel"}
                        and path_parts & ranking_signals
                    ):
                        return True
                    if (
                        path_parts & {"shadow", "matched"}
                        and path_parts & output_signals
                    ):
                        return True
                    if (
                        child is True
                        and canonical_key in {"shadow-only", "matched-pilot"}
                    ):
                        return True
                if key_forms & typed_key_forms and forbidden_typed_value(child):
                    return True
                if contains(child, frozenset(path_parts)):
                    return True
        elif isinstance(value, list):
            return any(contains(child, ancestor_parts) for child in value)
        return False

    stripped = text.strip()
    if path.suffix.casefold() not in {".json", ".jsonl"} and not stripped.startswith(
        ("{", "[")
    ):
        return False
    try:
        values = (
            [json.loads(line) for line in text.splitlines() if line.strip()]
            if path.suffix.casefold() == ".jsonl"
            else [json.loads(stripped)]
        )
    except (json.JSONDecodeError, RecursionError):
        return False
    return any(contains(value) for value in values)


def _audit_regeneration_owned_content(
    run_record: dict[str, Any],
    path: Path,
    relative: str,
    text: str,
    findings: list[Finding],
) -> None:
    if (
        run_record.get("cohort_kind") == "regeneration"
        and run_record.get("routing_state") == "enabled"
        and _regeneration_contamination_content(path, text)
    ):
        findings.append(
            Finding(
                "REGENERATION_CONTEXT_CONTAMINATION",
                "ERROR",
                "An enabled regeneration scope contains evaluator/advisory, validator-feedback, judge/panel-ranking, or shadow/matched-output material.",
                relative,
            )
        )


def _parse_closed_v2_manifest_text(text: str) -> list[dict[str, Any]] | None:
    try:
        records = [
            json.loads(line)
            for line in text.splitlines()
            if line.strip()
        ]
    except (json.JSONDecodeError, RecursionError):
        return None
    if not records or any(not isinstance(record, dict) for record in records):
        return None
    for record in records:
        record_type = record.get("record_type")
        observed_fields = set(record)
        if record_type == "run":
            if not observed_fields.issubset(V2_RUN_FIELDS):
                return None
        elif record_type == "agent":
            expected_fields = set(V2_AGENT_FIELDS)
            if record.get("stage") == "problem_discovery":
                expected_fields.add("island_id")
            if record.get("stage") in {"level2", "fact_closure"}:
                expected_fields.update(V2_DEVELOPMENT_TRACE_FIELDS)
            if observed_fields != expected_fields:
                return None
        elif record_type == "allocation":
            if observed_fields != V2_ALLOCATION_FIELDS:
                return None
        elif record_type == "query":
            if observed_fields != V2_QUERY_FIELDS:
                return None
        elif record_type == "tool_event":
            if observed_fields != V2_TOOL_EVENT_FIELDS:
                return None
        elif record_type == "source_open":
            if observed_fields != V2_SOURCE_OPEN_FIELDS:
                return None
        elif record_type == "checkpoint":
            if observed_fields != V2_CHECKPOINT_FIELDS:
                return None
        else:
            return None
    run_records = [record for record in records if record.get("record_type") == "run"]
    if len(run_records) != 1 or records[0] is not run_records[0]:
        return None
    return records


def _regeneration_control_records_contaminated(
    records: list[dict[str, Any]],
) -> bool:
    """Scan semantic V2 control-record fields without treating routing enums as input."""
    semantic_fields_by_type = {
        "run": {
            "fact_closure_candidates_file",
            "main_provisional_file",
        },
        "agent": {
            "context_files",
            "allowlisted_files",
            "files_read",
        },
        "query": {"query"},
        "tool_event": {"tool", "event_type"},
        "source_open": {"url"},
        "checkpoint": {"artifacts"},
    }
    payload_field_forms = {
        "query",
        "query-text",
        "search-query",
        "text",
        "prompt",
        "payload",
        "content",
        "message",
        "body",
        "notes",
        "description",
        "feedback",
        "output",
        "result",
        "results",
        "ranking",
        "rankings",
        "tool",
        "tool-name",
        "event-type",
        "action",
        "command",
        "operation",
        "operation-name",
        "intent",
        "destination",
        "route",
        "call",
        "next-step",
        "routing-target",
        "url",
        "source",
        "source-url",
        "proposition",
        "cheapest-resolving-test",
    }

    for record in records:
        record_type = record.get("record_type")
        explicit_fields = semantic_fields_by_type.get(str(record_type), set())
        for key, value in record.items():
            canonical_key = _canonical_tool_name(str(key))
            camel_separated_key = re.sub(
                r"(?<=[a-z0-9])(?=[A-Z])", "-", str(key)
            )
            canonical_camel_key = _canonical_tool_name(camel_separated_key)
            if (
                key not in explicit_fields
                and canonical_key not in payload_field_forms
                and canonical_camel_key not in payload_field_forms
            ):
                continue
            try:
                semantic_text = json.dumps(
                    {str(key): value}, ensure_ascii=False, sort_keys=True
                )
            except (TypeError, ValueError, RecursionError):
                return True
            if _regeneration_contamination_content(
                Path("regeneration-control-field.json"), semantic_text
            ):
                return True
    return False


def _is_canonical_native_v2_audit_report(
    text: str, run_record: dict[str, Any]
) -> bool:
    try:
        payload = json.loads(text)
    except (json.JSONDecodeError, RecursionError):
        return False
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version",
        "run_id",
        "adapter",
        "status",
        "counts",
        "resources",
        "findings",
    }:
        return False
    if (
        payload.get("schema_version") != SCHEMA_VERSION
        or payload.get("run_id") != run_record.get("run_id")
        or payload.get("adapter") != "native-v2"
        or not isinstance(payload.get("counts"), dict)
        or not isinstance(payload.get("resources"), dict)
        or not isinstance(payload.get("findings"), list)
        or text.encode("utf-8") != _json_bytes(payload)
    ):
        return False
    parsed_findings: list[Finding] = []
    for item in payload["findings"]:
        if not isinstance(item, dict) or set(item) != {
            "code",
            "severity",
            "message",
            "artifact",
            "line",
            "node_ids",
        }:
            return False
        if (
            not isinstance(item.get("code"), str)
            or item.get("severity") not in {"ERROR", "UNKNOWN", "WARNING", "INFO"}
            or not isinstance(item.get("message"), str)
            or not isinstance(item.get("artifact"), str)
            or (
                item.get("line") is not None
                and (
                    not isinstance(item.get("line"), int)
                    or isinstance(item.get("line"), bool)
                    or item.get("line") < 1
                )
            )
            or not isinstance(item.get("node_ids"), list)
            or any(not isinstance(node_id, str) for node_id in item["node_ids"])
        ):
            return False
        parsed_findings.append(
            Finding(
                item["code"],
                item["severity"],
                item["message"],
                item["artifact"],
                item["line"],
                tuple(item["node_ids"]),
            )
        )
    return payload.get("status") == _status(parsed_findings)


def _is_regeneration_control_artifact(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    freeze_seal: dict[str, Any] | None,
    path: Path,
    relative: str,
    text: str,
) -> bool:
    owned = _strict_run_file(run_dir, relative)
    if owned is None or owned[0] != path.resolve(strict=True):
        return False
    records = _parse_closed_v2_manifest_text(text)
    if relative == "00a_context_and_resource_manifest.jsonl":
        expected_records = [
            {key: value for key, value in record.items() if key != "_line"}
            for record in manifest_records
        ]
        return records is not None and records == expected_records
    if relative == PREFREEZE_MANIFEST_SNAPSHOT_V2:
        if records is None:
            return False
        snapshot_run = records[0]
        if (
            snapshot_run.get("schema") != RUN_SCHEMA_V2
            or snapshot_run.get("run_id") != run_record.get("run_id")
            or snapshot_run.get("scope_id") != run_record.get("scope_id")
            or _v2_immutable_run_view(snapshot_run)
            != _v2_immutable_run_view(run_record)
        ):
            return False
        if isinstance(freeze_seal, dict):
            if (
                freeze_seal.get("manifest_snapshot_path")
                != PREFREEZE_MANIFEST_SNAPSHOT_V2
                or freeze_seal.get("manifest_snapshot_sha256") != _sha256(path)
            ):
                return False
        return True
    return _is_canonical_native_v2_audit_report(text, run_record)


def _audit_v2_manifest_snapshot(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    freeze_seal: dict[str, Any],
    excluded_roots: set[str],
    findings: list[Finding],
    *,
    allow_frozen_final: bool = False,
) -> None:
    """Verify the immutable, run-owned manifest snapshot bound by a V2 seal."""
    raw_path = freeze_seal.get("manifest_snapshot_path")
    if raw_path != PREFREEZE_MANIFEST_SNAPSHOT_V2:
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_PATH_INVALID",
                "ERROR",
                f"V2 freeze seal must bind exactly {PREFREEZE_MANIFEST_SNAPSHOT_V2}.",
                str(raw_path or ""),
            )
        )
        return
    parsed = _strict_run_file(run_dir, raw_path, excluded_roots)
    if parsed is None:
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_INVALID",
                "ERROR",
                "The pre-freeze manifest snapshot must be a regular, non-symlink, parent-owned run-local file.",
                raw_path,
            )
        )
        return
    snapshot_path, relative = parsed
    try:
        snapshot_stat = snapshot_path.stat()
        manifest_stat = (run_dir / "00a_context_and_resource_manifest.jsonl").stat()
        if (
            snapshot_stat.st_dev == manifest_stat.st_dev
            and snapshot_stat.st_ino == manifest_stat.st_ino
        ):
            findings.append(
                Finding(
                    "FREEZE_MANIFEST_SNAPSHOT_INODE_ALIAS",
                    "ERROR",
                    "The pre-freeze snapshot must be an independent regular file, not a hard link to the mutable final manifest.",
                    relative,
                )
            )
    except OSError:
        findings.append(Finding("FREEZE_MANIFEST_SNAPSHOT_INVALID", "ERROR", "Snapshot/manifest inode ownership cannot be verified.", relative))
    expected_digest = freeze_seal.get("manifest_snapshot_sha256")
    observed_digest = _sha256(snapshot_path)
    if (
        not isinstance(expected_digest, str)
        or not re.fullmatch(r"[0-9a-f]{64}", expected_digest)
        or expected_digest != observed_digest
    ):
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_HASH_MISMATCH",
                "ERROR",
                "The V2 freeze seal does not match the exact raw bytes of its pre-freeze manifest snapshot.",
                relative,
            )
        )

    parse_findings: list[Finding] = []
    snapshot_records = _read_jsonl(snapshot_path, parse_findings)
    if parse_findings:
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_INVALID",
                "ERROR",
                "The pre-freeze manifest snapshot is not valid typed JSONL.",
                relative,
            )
        )
        return
    snapshot_run_records = [
        record
        for record in snapshot_records
        if record.get("record_type") == "run"
    ]
    if len(snapshot_run_records) != 1:
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_RUN_INVALID",
                "ERROR",
                "The pre-freeze manifest snapshot must contain exactly one run record.",
                relative,
            )
        )
        return
    snapshot_run = snapshot_run_records[0]
    if snapshot_run.get("_line") != 1:
        findings.append(Finding("FREEZE_MANIFEST_SNAPSHOT_RUN_INVALID", "ERROR", "The V2 snapshot run record must be its first line.", relative, snapshot_run.get("_line")))
    if _v2_immutable_run_view(snapshot_run) != _v2_immutable_run_view(run_record):
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_IDENTITY_MISMATCH",
                "ERROR",
                "The pre-freeze snapshot differs from the final immutable run identity, selection, wave, lineage, seed, budget, or live-seal pin.",
                relative,
                snapshot_run.get("_line"),
            )
        )
    invalid_types = sorted(
        {
            str(record.get("record_type"))
            for record in snapshot_records
            if record.get("record_type") not in MANIFEST_RECORD_TYPES
        }
    )
    if invalid_types:
        findings.append(Finding("FREEZE_MANIFEST_SNAPSHOT_RECORD_TYPE_INVALID", "ERROR", f"Snapshot contains unsupported record types {invalid_types}.", relative))

    try:
        snapshot_lines = snapshot_path.read_bytes().splitlines(keepends=True)
        final_lines = (run_dir / "00a_context_and_resource_manifest.jsonl").read_bytes().splitlines(keepends=True)
    except OSError:
        snapshot_lines = []
        final_lines = []
    snapshot_run_index = int(snapshot_run.get("_line", 0)) - 1
    final_run_index = int(run_record.get("_line", 0)) - 1
    snapshot_nonrun = [line for index, line in enumerate(snapshot_lines) if index != snapshot_run_index]
    final_nonrun = [line for index, line in enumerate(final_lines) if index != final_run_index]
    if (
        not snapshot_lines
        or not final_lines
        or any(not line.strip() for line in snapshot_lines + final_lines)
        or len(final_nonrun) < len(snapshot_nonrun)
        or snapshot_nonrun != final_nonrun[: len(snapshot_nonrun)]
        or (allow_frozen_final and snapshot_lines != final_lines)
    ):
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_CONTENT_MISMATCH",
                "ERROR",
                "Every pre-seal non-run JSONL line must remain a byte-identical ordered prefix of the final manifest; research telemetry cannot be dropped, reordered, rewritten, or reconstructed after sealing.",
                relative,
            )
        )

    snapshot_checkpoints = [
        record
        for record in snapshot_records
        if record.get("record_type") == "checkpoint"
    ]
    appended_records = [
        record
        for record in manifest_records
        if isinstance(record.get("_line"), int)
        and record.get("_line") > len(snapshot_nonrun) + 1
    ]
    last_snapshot_checkpoint = snapshot_checkpoints[-1] if snapshot_checkpoints else None
    sealed_at = _parse_timestamp(freeze_seal.get("sealed_at"))
    last_snapshot_time = (
        _parse_timestamp(last_snapshot_checkpoint.get("occurred_at"))
        if isinstance(last_snapshot_checkpoint, dict)
        else None
    )
    if (
        last_snapshot_time is None
        or sealed_at is None
        or last_snapshot_time >= sealed_at
    ):
        findings.append(
            Finding(
                "FREEZE_MANIFEST_SNAPSHOT_SEAL_ORDER_INVALID",
                "ERROR",
                "The pinned frozen checkpoint must occur strictly before the external freeze seal.",
                relative,
            )
        )
    expected_predecessor = (
        last_snapshot_checkpoint.get("checkpoint_id")
        if isinstance(last_snapshot_checkpoint, dict)
        else None
    )
    for appended in appended_records:
        appended_time = _parse_timestamp(appended.get("occurred_at"))
        if (
            appended.get("record_type") != "checkpoint"
            or set(appended) - {"_line"} != V2_CHECKPOINT_FIELDS
            or appended.get("state") != "complete"
            or appended.get("predecessor_id") != expected_predecessor
            or sealed_at is None
            or appended_time is None
            or appended_time <= sealed_at
        ):
            findings.append(
                Finding(
                    "FREEZE_MANIFEST_TERMINAL_APPEND_INVALID",
                    "ERROR",
                    "After a V2 seal, only the exact terminal complete checkpoint may append, strictly after the seal and naming the frozen checkpoint predecessor.",
                    "00a_context_and_resource_manifest.jsonl",
                    appended.get("_line"),
                )
            )
        expected_predecessor = appended.get("checkpoint_id")
    if allow_frozen_final:
        if appended_records or run_record.get("lifecycle_state") != "frozen":
            findings.append(
                Finding(
                    "FREEZE_MANIFEST_TERMINAL_APPEND_INVALID",
                    "ERROR",
                    "A shadow-dispatch audit requires the exact sealed frozen prefix with no post-seal manifest record.",
                    "00a_context_and_resource_manifest.jsonl",
                )
            )
    elif len(appended_records) != 1:
        findings.append(
            Finding(
                "FREEZE_MANIFEST_TERMINAL_APPEND_INVALID",
                "ERROR",
                "A completed V2 final manifest must append exactly one terminal complete checkpoint after its frozen snapshot.",
                "00a_context_and_resource_manifest.jsonl",
            )
        )

    snapshot_state_findings: list[Finding] = []
    _audit_v2_state_chain(
        snapshot_run,
        snapshot_records,
        run_dir,
        excluded_roots,
        snapshot_state_findings,
        None,
        allow_prefix=True,
    )
    for item in snapshot_state_findings:
        findings.append(
            Finding(
                "FREEZE_SNAPSHOT_" + item.code,
                item.severity,
                item.message,
                relative,
                item.line,
                item.node_ids,
            )
        )
    if (
        snapshot_run.get("lifecycle_state") != "frozen"
        or snapshot_run.get("status") != "frozen"
        or not snapshot_checkpoints
        or snapshot_checkpoints[-1].get("state") != "frozen"
    ):
        findings.append(Finding("FREEZE_MANIFEST_SNAPSHOT_LIFECYCLE_INVALID", "ERROR", "A V2 freeze seal requires a valid pre-seal checkpoint prefix through the exact frozen boundary, with all research telemetry already present.", relative, snapshot_run.get("_line")))
    _audit_v2_terminal_lifecycle_times(
        snapshot_run,
        snapshot_records,
        findings,
        artifact=relative,
    )

    snapshot_declarations = snapshot_run.get("declared_child_scopes")
    final_declarations = run_record.get("declared_child_scopes")
    if not isinstance(snapshot_declarations, list) or not isinstance(final_declarations, list):
        findings.append(Finding("CHILD_REGISTRATION_SNAPSHOT_INVALID", "ERROR", "Snapshot and final run must both contain typed child declaration lists.", relative))
    else:
        prereg_by_scope = {
            item.get("scope_id"): item
            for item in snapshot_declarations
            if isinstance(item, dict) and isinstance(item.get("scope_id"), str)
        }
        final_by_scope = {
            item.get("scope_id"): item
            for item in final_declarations
            if isinstance(item, dict) and isinstance(item.get("scope_id"), str)
        }
        if len(prereg_by_scope) != len(snapshot_declarations) or set(prereg_by_scope) != set(final_by_scope):
            findings.append(Finding("CHILD_PREREGISTRATION_MISMATCH", "ERROR", "Every final child must have one exact pre-dispatch declaration in the pinned live snapshot.", relative))
        for child_scope_id, final_declaration in final_by_scope.items():
            preregistration = prereg_by_scope.get(child_scope_id)
            if not isinstance(preregistration, dict):
                continue
            immutable_prereg = {
                key: value
                for key, value in preregistration.items()
                if key not in CHILD_FINALIZATION_FIELDS_V2
            }
            immutable_final = {
                key: value
                for key, value in final_declaration.items()
                if key not in CHILD_FINALIZATION_FIELDS_V2
            }
            if (
                set(preregistration) != CHILD_DECLARATION_FIELDS_V2
                or set(final_declaration) != CHILD_DECLARATION_FIELDS_V2
                or any(preregistration.get(key) is not None for key in CHILD_FINALIZATION_FIELDS_V2)
                or not isinstance(preregistration.get("development_contract_sha256"), str)
                or not isinstance(preregistration.get("protection_anchor_sha256"), str)
                or immutable_prereg != immutable_final
            ):
                findings.append(Finding("CHILD_PREREGISTRATION_MISMATCH", "ERROR", f"Child {child_scope_id} was not fill-once materialized from its pinned pre-dispatch declaration.", relative, node_ids=(str(child_scope_id),)))


def _audit_v2_compatibility_mirrors(
    run_record: dict[str, Any],
    profile_name: Any,
    manifest_name: str,
    findings: list[Finding],
) -> None:
    compatibility_mirrors = {
        "status": run_record.get("lifecycle_state"),
        "matched_pilot": profile_name
        in {"operational_live_with_shadow", "v2_matched_nonrouting"},
        "shadow_only": run_record.get("routing_state") == "frozen_nonrouting",
        "validation_eligible": run_record.get("routing_state") == "enabled",
        "shadow_can_route_to_validation": False,
    }
    for mirror, expected in compatibility_mirrors.items():
        if mirror in run_record and run_record.get(mirror) != expected:
            findings.append(
                Finding(
                    "V2_COMPATIBILITY_MIRROR_MISMATCH",
                    "ERROR",
                    f"Compatibility mirror {mirror} must exactly reconcile to the authoritative V2 profile/routing/lifecycle state.",
                    manifest_name,
                    run_record.get("_line"),
                )
            )


def _audit_v2_predispatch_child_protection_anchor(
    declaration: dict[str, Any],
    reserved_dir: Path,
    child_protection_anchor: dict[str, Any] | None,
    child_protection_anchor_sha256: str | None,
    fixed_contract_paths: dict[str, str],
    findings: list[Finding],
) -> None:
    if not isinstance(child_protection_anchor, dict) or not isinstance(
        child_protection_anchor_sha256, str
    ):
        return

    _validate_v2_protection_anchor_fields(child_protection_anchor, findings)
    try:
        observed_payload_digest = _json_payload_sha256(child_protection_anchor)
    except (RecursionError, TypeError, ValueError):
        observed_payload_digest = None
    if (
        not re.fullmatch(r"[0-9a-f]{64}", child_protection_anchor_sha256)
        or observed_payload_digest != child_protection_anchor_sha256
        or declaration.get("protection_anchor_sha256")
        != child_protection_anchor_sha256
    ):
        findings.append(
            Finding(
                "SHADOW_DISPATCH_CHILD_PROTECTION_PIN_MISMATCH",
                "ERROR",
                "The child protection-anchor payload, independent pin, and sealed preregistration digest must be identical.",
                "00a_context_and_resource_manifest.jsonl",
                node_ids=(str(declaration.get("scope_id")),),
            )
        )

    if child_protection_anchor.get("schema") != PROTECTION_ANCHOR_SCHEMA_V2:
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_SCHEMA_INVALID",
                "ERROR",
                "The pre-dispatch child protection anchor must use zt1-protection-anchor-v2.",
            )
        )
    if child_protection_anchor.get("contract_profile") != CONTRACT_PROFILE:
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_PROFILE_INVALID",
                "ERROR",
                "The pre-dispatch child protection anchor must retain the exact fixed-v1 contract profile.",
            )
        )
    if child_protection_anchor.get("workflow_profile") != WORKFLOW_PROFILE_V2:
        findings.append(
            Finding(
                "WORKFLOW_PROFILE_INVALID",
                "ERROR",
                f"The child protection anchor must bind workflow profile {WORKFLOW_PROFILE_V2}.",
            )
        )
    if (
        child_protection_anchor.get("block_semantics")
        != "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1"
    ):
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_BLOCK_SEMANTICS_INVALID",
                "ERROR",
                "The child protection anchor uses unsupported validation-block byte semantics.",
            )
        )

    registered_at = _parse_timestamp(declaration.get("registered_at"))
    created_at = _parse_timestamp(child_protection_anchor.get("created_at"))
    expected_child_dir = reserved_dir.resolve(strict=False)
    identity_invalid = (
        child_protection_anchor.get("run_id") != expected_child_dir.name
        or child_protection_anchor.get("run_dir") != str(expected_child_dir)
        or child_protection_anchor.get("scope_id") != declaration.get("scope_id")
        or child_protection_anchor.get("development_contract_path")
        != "00b_development_contract.json"
        or child_protection_anchor.get("development_contract_sha256")
        != declaration.get("development_contract_sha256")
        or created_at is None
        or registered_at is None
        or created_at >= registered_at
    )
    if identity_invalid:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_CHILD_PROTECTION_IDENTITY_INVALID",
                "ERROR",
                "The child anchor must bind the exact reserved run/scope/development identity and be created strictly before preregistration.",
                "00a_context_and_resource_manifest.jsonl",
                node_ids=(str(declaration.get("scope_id")),),
            )
        )

    workflow_entries = child_protection_anchor.get("workflow_files")
    workflow_by_id: dict[str, dict[str, Any]] = {}
    workflow_duplicates = False
    if isinstance(workflow_entries, list):
        for entry in workflow_entries:
            workflow_id = entry.get("id") if isinstance(entry, dict) else None
            if (
                not isinstance(entry, dict)
                or not isinstance(workflow_id, str)
                or workflow_id in workflow_by_id
            ):
                workflow_duplicates = True
                continue
            workflow_by_id[workflow_id] = entry
    if (
        not isinstance(workflow_entries, list)
        or workflow_duplicates
        or len(workflow_entries) != len(WORKFLOW_PROFILE_FILE_PATHS_V2)
        or set(workflow_by_id) != set(WORKFLOW_PROFILE_FILE_PATHS_V2)
    ):
        findings.append(
            Finding(
                "WORKFLOW_PROFILE_FILE_SET_INCOMPLETE",
                "ERROR",
                "The child anchor must bind every and only the protocol/auditor/executor workflow file once.",
            )
        )
    for workflow_id, expected_path_value in WORKFLOW_PROFILE_FILE_PATHS_V2.items():
        entry = workflow_by_id.get(workflow_id)
        if not isinstance(entry, dict):
            continue
        expected_path = Path(expected_path_value)
        if (
            entry.get("path") != expected_path_value
            or _has_symlink_component(expected_path)
            or not expected_path.is_file()
            or _is_within(expected_path, expected_child_dir)
        ):
            findings.append(
                Finding(
                    "WORKFLOW_PROFILE_FILE_INVALID",
                    "ERROR",
                    f"Child workflow file {workflow_id!r} is not its exact canonical external path.",
                    str(entry.get("path") or ""),
                )
            )
        elif entry.get("sha256") != _sha256(expected_path):
            findings.append(
                Finding(
                    "WORKFLOW_PROFILE_FILE_HASH_MISMATCH",
                    "ERROR",
                    f"Child workflow file {workflow_id!r} differs from its exact current bytes.",
                    expected_path_value,
                )
            )

    fixed_entries = child_protection_anchor.get("files")
    fixed_by_id: dict[str, dict[str, Any]] = {}
    fixed_duplicates = False
    if isinstance(fixed_entries, list):
        for entry in fixed_entries:
            contract_id = entry.get("id") if isinstance(entry, dict) else None
            if (
                not isinstance(entry, dict)
                or not isinstance(contract_id, str)
                or contract_id in fixed_by_id
            ):
                fixed_duplicates = True
                continue
            fixed_by_id[contract_id] = entry
    if (
        not isinstance(fixed_entries, list)
        or fixed_duplicates
        or len(fixed_entries) != len(fixed_contract_paths)
        or set(fixed_by_id) != set(fixed_contract_paths)
    ):
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_FILE_SET_INCOMPLETE",
                "ERROR",
                "The child anchor must bind every and only the fixed-v1 contract once.",
            )
        )
    for contract_id, expected_path_value in fixed_contract_paths.items():
        entry = fixed_by_id.get(contract_id)
        if not isinstance(entry, dict):
            continue
        expected_path = Path(expected_path_value).resolve(strict=False)
        if (
            entry.get("path") != str(expected_path)
            or _has_symlink_component(Path(expected_path_value))
            or not expected_path.is_file()
            or _is_within(expected_path, expected_child_dir)
            or entry.get("sha256") != _sha256(expected_path)
        ):
            findings.append(
                Finding(
                    "PROTECTION_ANCHOR_FILE_INVALID",
                    "ERROR",
                    f"Child anchor fixed contract {contract_id!r} is not canonical and hash-bound.",
                    str(entry.get("path") or ""),
                )
            )

    block_entries = child_protection_anchor.get("blocks")
    block_by_id: dict[str, dict[str, Any]] = {}
    block_duplicates = False
    if isinstance(block_entries, list):
        for entry in block_entries:
            block_id = entry.get("id") if isinstance(entry, dict) else None
            if (
                not isinstance(entry, dict)
                or not isinstance(block_id, str)
                or block_id in block_by_id
            ):
                block_duplicates = True
                continue
            block_by_id[block_id] = entry
    if (
        not isinstance(block_entries, list)
        or block_duplicates
        or len(block_entries) != len(REQUIRED_PROTECTED_BLOCK_IDS)
        or set(block_by_id) != set(REQUIRED_PROTECTED_BLOCK_IDS)
    ):
        findings.append(
            Finding(
                "PROTECTION_ANCHOR_BLOCK_SET_INCOMPLETE",
                "ERROR",
                "The child anchor must bind every and only the fixed validation block once.",
            )
        )
    expected_block_path = Path(
        fixed_contract_paths["orchestration-prompt"]
    ).resolve(strict=False)
    for block_id, expected_markers in REQUIRED_PROTECTED_BLOCK_IDS.items():
        entry = block_by_id.get(block_id)
        if not isinstance(entry, dict):
            continue
        if (
            entry.get("path") != str(expected_block_path)
            or (entry.get("start_marker"), entry.get("end_marker"))
            != expected_markers
            or _has_symlink_component(expected_block_path)
            or not expected_block_path.is_file()
            or _is_within(expected_block_path, expected_child_dir)
            or entry.get("sha256")
            != _marker_block_sha256(expected_block_path, *expected_markers)
        ):
            findings.append(
                Finding(
                    "PROTECTION_ANCHOR_BLOCK_INVALID",
                    "ERROR",
                    f"Child anchor block {block_id!r} is not the exact fixed validation block.",
                    str(entry.get("path") or ""),
                )
            )


def _audit_v2_shadow_dispatch_preregistration(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    findings: list[Finding],
    *,
    protection_anchor: dict[str, Any] | None,
    protection_anchor_sha256: str | None,
    child_protection_anchor: dict[str, Any] | None,
    child_protection_anchor_sha256: str | None,
    freeze_seal: dict[str, Any] | None,
    freeze_seal_sha256: str | None,
    child_trust_bundle: dict[str, Any] | None,
    child_trust_bundle_sha256: str | None,
    fixed_contract_paths: dict[str, str],
) -> None:
    """Audit the sealed parent prefix immediately before a shadow is started."""
    manifest_name = "00a_context_and_resource_manifest.jsonl"
    if not all(
        (
            isinstance(protection_anchor, dict),
            isinstance(protection_anchor_sha256, str),
            isinstance(freeze_seal, dict),
            isinstance(freeze_seal_sha256, str),
            isinstance(protection_anchor_sha256, str)
            and re.fullmatch(r"[0-9a-f]{64}", protection_anchor_sha256),
            isinstance(freeze_seal_sha256, str)
            and re.fullmatch(r"[0-9a-f]{64}", freeze_seal_sha256),
        )
    ):
        findings.append(
            Finding(
                "SHADOW_DISPATCH_PARENT_TRUST_MISSING",
                "ERROR",
                "Shadow dispatch requires independently pinned parent protection and V2 freeze-seal payloads.",
                manifest_name,
            )
        )

    checkpoints = [
        record
        for record in manifest_records
        if record.get("record_type") == "checkpoint"
    ]
    frozen_checkpoints = [
        record for record in checkpoints if record.get("state") == "frozen"
    ]
    frozen_checkpoint = (
        frozen_checkpoints[0] if len(frozen_checkpoints) == 1 else None
    )
    frozen_at = (
        _parse_timestamp(frozen_checkpoint.get("occurred_at"))
        if isinstance(frozen_checkpoint, dict)
        else None
    )
    if (
        run_record.get("lifecycle_state") != "frozen"
        or run_record.get("status") != "frozen"
        or not checkpoints
        or checkpoints[-1].get("state") != "frozen"
        or len(frozen_checkpoints) != 1
        or frozen_at is None
    ):
        findings.append(
            Finding(
                "SHADOW_DISPATCH_FROZEN_PREFIX_INVALID",
                "ERROR",
                "Shadow dispatch requires one exact lifecycle prefix ending at the frozen boundary.",
                manifest_name,
                run_record.get("_line"),
            )
        )

    if child_trust_bundle is not None or child_trust_bundle_sha256 is not None:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_CHILD_ALREADY_PRESENT",
                "ERROR",
                "A child trust bundle cannot exist before shadow dispatch.",
                manifest_name,
            )
        )
    if run_record.get("shadow_results_released_at") is not None:
        findings.append(
            Finding(
                "SHADOW_RESULTS_RELEASE_PREMATURE",
                "ERROR",
                "Shadow results cannot be released before the preregistered child is dispatched, completed, recursively audited, and trusted.",
                manifest_name,
                run_record.get("_line"),
            )
        )

    declarations_value = run_record.get("declared_child_scopes")
    declaration = (
        declarations_value[0]
        if isinstance(declarations_value, list)
        and len(declarations_value) == 1
        and isinstance(declarations_value[0], dict)
        else None
    )
    declaration_invalid = declaration is None
    parsed_reservation: tuple[Path, str] | None = None
    child_scope_id: Any = None
    if isinstance(declaration, dict):
        child_scope_id = declaration.get("scope_id")
        parsed_reservation = _strict_reserved_child_directory(
            run_dir, declaration.get("relative_path")
        )
        parent_start = _parse_timestamp(run_record.get("started_at"))
        registered_at = _parse_timestamp(declaration.get("registered_at"))
        digest_fields_valid = all(
            isinstance(declaration.get(field), str)
            and re.fullmatch(r"[0-9a-f]{64}", declaration[field])
            for field in (
                "development_contract_sha256",
                "protection_anchor_sha256",
            )
        )
        declaration_invalid = any(
            (
                set(declaration) != CHILD_DECLARATION_FIELDS_V2,
                not isinstance(child_scope_id, str),
                not isinstance(child_scope_id, str)
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]*", child_scope_id),
                child_scope_id == run_record.get("scope_id"),
                parsed_reservation is None,
                declaration.get("relationship") != "shadow_child",
                declaration.get("run_profile") != run_record.get("run_profile"),
                declaration.get("mode") != "archipelago_lite_shadow",
                declaration.get("arm") != "shadow",
                declaration.get("routing_state") != "frozen_nonrouting",
                declaration.get("cohort_kind") != "initial",
                declaration.get("model") != run_record.get("model"),
                declaration.get("reasoning_effort")
                != run_record.get("reasoning_effort"),
                declaration.get("results_visibility") != "withheld",
                not digest_fields_valid,
                declaration.get("development_contract_sha256")
                != run_record.get("development_contract_sha256"),
                any(
                    declaration.get(field) is not None
                    for field in CHILD_FINALIZATION_FIELDS_V2
                ),
                parent_start is None,
                registered_at is None,
                frozen_at is None,
                parent_start is not None
                and registered_at is not None
                and registered_at < parent_start,
                frozen_at is not None
                and registered_at is not None
                and registered_at >= frozen_at,
            )
        )
    if declaration_invalid:
        findings.append(
            Finding(
                "CHILD_PREREGISTRATION_MISMATCH",
                "ERROR",
                "Shadow dispatch requires exactly one closed, safe, null-finalized child preregistration with matching immutable profile, development, protection, model, effort, visibility, and timing pins.",
                manifest_name,
                run_record.get("_line"),
                (str(child_scope_id),) if child_scope_id is not None else (),
            )
        )
    if isinstance(declaration, dict) and parsed_reservation is not None:
        _audit_v2_predispatch_child_protection_anchor(
            declaration,
            parsed_reservation[0],
            child_protection_anchor,
            child_protection_anchor_sha256,
            fixed_contract_paths,
            findings,
        )

    active_agents = sorted(
        str(record.get("agent_id"))
        for record in manifest_records
        if record.get("record_type") == "agent"
        and (
            frozen_at is None
            or (ended_at := _parse_timestamp(record.get("ended_at"))) is None
            or ended_at >= frozen_at
        )
    )
    if active_agents:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_ACTIVE_AGENT",
                "ERROR",
                f"Every parent agent must finish strictly before the frozen dispatch boundary; active or unresolved agents: {active_agents}.",
                manifest_name,
                node_ids=tuple(active_agents),
            )
        )

    run_totals = run_record.get("resource_totals")
    frozen_totals = (
        frozen_checkpoint.get("resource_totals")
        if isinstance(frozen_checkpoint, dict)
        else None
    )
    totals_match = (
        isinstance(run_totals, dict)
        and set(run_totals) == V2_CHECKPOINT_RESOURCE_FIELDS
        and isinstance(frozen_totals, dict)
        and set(frozen_totals) == V2_CHECKPOINT_RESOURCE_FIELDS
        and all(
            isinstance(run_totals.get(field), int)
            and not isinstance(run_totals.get(field), bool)
            and isinstance(frozen_totals.get(field), int)
            and not isinstance(frozen_totals.get(field), bool)
            and (run_value := _as_decimal(run_totals.get(field))) is not None
            and (frozen_value := _as_decimal(frozen_totals.get(field))) is not None
            and run_value > 0
            and run_value == frozen_value
            for field in V2_CHECKPOINT_RESOURCE_FIELDS
        )
    )
    if not totals_match:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_RESOURCE_TOTAL_MISMATCH",
                "ERROR",
                "The frozen parent run totals must use the exact four-key schema, be positive, and equal the frozen checkpoint totals.",
                manifest_name,
                run_record.get("_line"),
            )
        )

    child_event_records = [
        record
        for record in manifest_records
        if record.get("record_type") not in {"run", "checkpoint"}
        and (
            record.get("scope_id") == child_scope_id
            or record.get("arm") == "shadow"
        )
    ]
    discovered_runs = _discover_nested_machine_runs(run_dir)
    declared_reservation_paths = (
        {parsed_reservation[1]} if parsed_reservation is not None else set()
    )
    for undeclared in sorted(discovered_runs - declared_reservation_paths):
        findings.append(
            Finding(
                "CHILD_RUN_UNDECLARED",
                "ERROR",
                "Nested machine-run manifest is not registered as the exact pre-dispatch child reservation.",
                f"{undeclared}/00a_context_and_resource_manifest.jsonl",
            )
        )
    if child_event_records or discovered_runs:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_CHILD_ALREADY_PRESENT",
                "ERROR",
                "No child manifest or shadow execution event may exist before the dispatch gate.",
                manifest_name,
                node_ids=tuple(sorted(discovered_runs)),
            )
        )

    if parsed_reservation is not None:
        reserved_dir, reserved_relative = parsed_reservation
        unexpected_entries: list[str] = []
        reservation_symlink = False
        if reserved_dir.exists():
            for current, directory_names, file_names in os.walk(
                reserved_dir, followlinks=False
            ):
                current_path = Path(current)
                for name in directory_names:
                    entry = current_path / name
                    if entry.is_symlink():
                        reservation_symlink = True
                    unexpected_entries.append(
                        entry.relative_to(reserved_dir).as_posix() + "/"
                    )
                for name in file_names:
                    entry = current_path / name
                    entry_relative = entry.relative_to(reserved_dir).as_posix()
                    if entry.is_symlink():
                        reservation_symlink = True
                    if entry_relative != "00b_development_contract.json":
                        unexpected_entries.append(entry_relative)
            child_contract = reserved_dir / "00b_development_contract.json"
            if child_contract.exists() and (
                child_contract.is_symlink()
                or not child_contract.is_file()
                or not isinstance(declaration, dict)
                or _sha256(child_contract)
                != declaration.get("development_contract_sha256")
            ):
                declaration_invalid = True
                findings.append(
                    Finding(
                        "CHILD_PREREGISTRATION_MISMATCH",
                        "ERROR",
                        "The reserved child development-contract bytes do not match the preregistered digest.",
                        f"{reserved_relative}/00b_development_contract.json",
                    )
                )
        if reservation_symlink:
            findings.append(
                Finding(
                    "CHILD_PREREGISTRATION_MISMATCH",
                    "ERROR",
                    "The reserved child path contains a symlink component or entry.",
                    reserved_relative,
                )
            )
        if unexpected_entries:
            findings.append(
                Finding(
                    "SHADOW_DISPATCH_CHILD_ALREADY_PRESENT",
                    "ERROR",
                    f"The reserved child scope contains premature execution material: {sorted(unexpected_entries)}.",
                    reserved_relative,
                )
            )


def _audit_v2_contract(
    run_dir: Path,
    run_record: dict[str, Any],
    manifest_records: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
    findings: list[Finding],
    counts: dict[str, Any],
    resources: dict[str, Any],
    *,
    strict: bool,
    protection_anchor: dict[str, Any] | None,
    protection_anchor_sha256: str | None,
    child_protection_anchor: dict[str, Any] | None,
    child_protection_anchor_sha256: str | None,
    freeze_seal: dict[str, Any] | None,
    freeze_seal_sha256: str | None,
    live_arm_freeze_seal: dict[str, Any] | None,
    live_arm_freeze_seal_sha256: str | None,
    initial_freeze_seal: dict[str, Any] | None,
    initial_freeze_seal_sha256: str | None,
    child_trust_bundle: dict[str, Any] | None,
    child_trust_bundle_sha256: str | None,
    checkpoint: str | None,
    fixed_contract_paths: dict[str, str],
    scope_stack: tuple[str, ...],
) -> None:
    manifest_name = "00a_context_and_resource_manifest.jsonl"
    shadow_dispatch_prefix = _is_v2_shadow_dispatch_prefix(
        run_record, checkpoint
    )
    if isinstance(freeze_seal, dict):
        _validate_v2_freeze_seal_fields(
            freeze_seal,
            findings,
            expected_arm=run_record.get("arm"),
            expected_cohort_kind=run_record.get("cohort_kind"),
        )
    required_fields = (
        "record_type",
        "schema",
        "run_id",
        "run_profile",
        "scope_id",
        "mode",
        "arm",
        "routing_state",
        "cohort_kind",
        "wave_index",
        "selection_policy",
        "lifecycle_state",
        "started_at",
        "ended_at",
        "model",
        "reasoning_effort",
        "results_visibility",
        "seed",
        "candidate_order_seed",
        "development_contract_path",
        "development_contract_sha256",
        "parent_scope_id",
        "declared_child_scopes",
        "file_read_log_complete",
        "tool_event_log_complete",
        "protected_files",
        "protected_blocks",
        "budgets",
        "resource_totals",
    )
    missing_fields = [field for field in required_fields if field not in run_record]
    if missing_fields:
        findings.append(Finding("V2_RUN_FIELDS_MISSING", "ERROR", f"V2 run omits required exact fields: {missing_fields}.", manifest_name, run_record.get("_line")))
    extra_run_fields = (set(run_record) - {"_line"}) - V2_RUN_FIELDS
    if extra_run_fields:
        findings.append(
            Finding(
                "V2_RUN_FIELDS_INVALID",
                "ERROR",
                f"V2 run contains unknown authoritative or routing fields: {sorted(extra_run_fields)}.",
                manifest_name,
                run_record.get("_line"),
            )
        )
    for ledger_record in ledger_records:
        record_type = ledger_record.get("record_type")
        allowed_fields = V2_LEDGER_FIELDS_BY_TYPE.get(str(record_type))
        if allowed_fields is None:
            continue
        extra_fields = (set(ledger_record) - {"_line"}) - allowed_fields
        if extra_fields:
            stable_id = next(
                (
                    ledger_record.get(field)
                    for field in (
                        "problem_id",
                        "raw_id",
                        "concept_id",
                        "finalist_id",
                        "evidence_id",
                    )
                    if isinstance(ledger_record.get(field), str)
                ),
                str(record_type),
            )
            findings.append(
                Finding(
                    "V2_LEDGER_FIELDS_INVALID",
                    "ERROR",
                    f"V2 {record_type} record {stable_id!r} contains unknown authoritative fields: {sorted(extra_fields)}.",
                    "02b_raw_to_direction_ledger.jsonl",
                    ledger_record.get("_line"),
                    (str(stable_id),),
                )
            )
        if record_type == "mapping" and isinstance(
            ledger_record.get("operation"), dict
        ):
            operation_fields = set(ledger_record["operation"])
            expected_operation_fields = (
                {"dimension", "assumption", "causal_benefit", "new_risk"}
                if ledger_record.get("concept_type") == "inversion"
                else {"transferred_mechanism", "analogy_break"}
                if ledger_record.get("concept_type") == "recombination"
                else set()
            )
            if operation_fields != expected_operation_fields:
                findings.append(
                    Finding(
                        "V2_LEDGER_FIELDS_INVALID",
                        "ERROR",
                        f"V2 mapping operation must use the exact closed fields for concept_type {ledger_record.get('concept_type')!r}.",
                        "02b_raw_to_direction_ledger.jsonl",
                        ledger_record.get("_line"),
                        (str(ledger_record.get("raw_id")),),
                    )
                )
    profile_name = run_record.get("run_profile")
    profile = PROFILE_SPECS_V2.get(profile_name)
    if profile is None:
        findings.append(Finding("RUN_PROFILE_INVALID", "ERROR", f"Unsupported V2 run_profile {profile_name!r}; aliases are not normalized.", manifest_name, run_record.get("_line")))
    scope_id = run_record.get("scope_id")
    if not isinstance(scope_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]*", scope_id):
        findings.append(Finding("SCOPE_ID_INVALID", "ERROR", "V2 scope_id must be a stable non-empty typed identifier.", manifest_name, run_record.get("_line")))
        scope_id = ""
    if run_record.get("_line") != 1:
        findings.append(Finding("V2_RUN_RECORD_NOT_FIRST", "ERROR", "The sole V2 run record must be the first JSONL line.", manifest_name, run_record.get("_line")))
    if run_record.get("run_id") != run_dir.name:
        findings.append(Finding("V2_RUN_ID_MISMATCH", "ERROR", "run_id must equal the canonical scope directory name and external trust identity.", manifest_name, run_record.get("_line")))
    canonical_scope = str(run_dir.resolve())
    if canonical_scope in scope_stack:
        findings.append(Finding("CHILD_SCOPE_CYCLE", "ERROR", "Recursive child audit re-entered an ancestor scope.", manifest_name))
        return
    if run_record.get("routing_state") not in ROUTING_STATES_V2:
        findings.append(Finding("ROUTING_STATE_INVALID", "ERROR", "routing_state must be exactly enabled or frozen_nonrouting.", manifest_name, run_record.get("_line")))
    if run_record.get("cohort_kind") not in COHORT_KINDS_V2:
        findings.append(Finding("COHORT_KIND_INVALID", "ERROR", "cohort_kind must be exactly initial or regeneration.", manifest_name, run_record.get("_line")))
    if run_record.get("arm") not in KNOWN_ARMS:
        findings.append(Finding("RUN_ARM_INVALID", "ERROR", "arm must be exactly live, shadow, or matched_baseline.", manifest_name, run_record.get("_line")))
    expected_visibility = "available" if run_record.get("routing_state") == "enabled" else "withheld"
    if run_record.get("results_visibility") != expected_visibility:
        findings.append(Finding("RESULTS_VISIBILITY_INVALID", "ERROR", f"V2 results_visibility must be exactly {expected_visibility!r} for routing_state {run_record.get('routing_state')!r}.", manifest_name, run_record.get("_line")))
    wave_index = run_record.get("wave_index")
    if (
        not isinstance(wave_index, int)
        or isinstance(wave_index, bool)
        or wave_index < 1
        or (run_record.get("cohort_kind") == "initial" and wave_index != 1)
        or (run_record.get("cohort_kind") == "regeneration" and wave_index < 2)
    ):
        findings.append(Finding("WAVE_INDEX_INVALID", "ERROR", "Initial V2 scopes use wave_index=1 and regeneration scopes use an integer >=2.", manifest_name, run_record.get("_line")))
    expected_selection_policy = "isolated_two_stage" if run_record.get("arm") == "shadow" else "root_orchestrator"
    if run_record.get("selection_policy") != expected_selection_policy:
        findings.append(Finding("SELECTION_POLICY_INVALID", "ERROR", f"This scope requires selection_policy={expected_selection_policy!r}.", manifest_name, run_record.get("_line")))
    for seed_field in ("seed", "candidate_order_seed"):
        if not isinstance(run_record.get(seed_field), str) or not run_record.get(seed_field).strip():
            findings.append(Finding("RUN_SEED_INVALID", "ERROR", f"V2 run field {seed_field} must be a pre-registered non-empty string.", manifest_name, run_record.get("_line")))
    _audit_v2_compatibility_mirrors(
        run_record, profile_name, manifest_name, findings
    )
    if run_record.get("cohort_kind") == "initial" and run_record.get("parent_scope_id") is not None:
        findings.append(Finding("PARENT_SCOPE_ID_INVALID", "ERROR", "An initial V2 scope must use parent_scope_id=null.", manifest_name, run_record.get("_line")))
    if profile is not None:
        observed_contract = (
            run_record.get("mode"),
            run_record.get("arm"),
            run_record.get("routing_state"),
            run_record.get("cohort_kind"),
        )
        if observed_contract not in profile.allowed_contracts:
            findings.append(Finding("RUN_PROFILE_SEMANTICS_MISMATCH", "ERROR", f"run_profile does not permit exact (mode, arm, routing_state, cohort_kind) contract {observed_contract!r}.", manifest_name, run_record.get("_line")))
    if checkpoint == "shadow-dispatch" and not shadow_dispatch_prefix:
        findings.append(
            Finding(
                "SHADOW_DISPATCH_PROFILE_INVALID",
                "ERROR",
                "shadow-dispatch is valid only for an initial operational live or matched-baseline composite root.",
                manifest_name,
                run_record.get("_line"),
            )
        )

    if run_record.get("arm") == "shadow":
        supplied_live_pin = live_arm_freeze_seal_sha256
        run_live_pin = run_record.get("live_arm_freeze_seal_sha256")
        if (
            not isinstance(live_arm_freeze_seal, dict)
            or not isinstance(supplied_live_pin, str)
            or not re.fullmatch(r"[0-9a-f]{64}", supplied_live_pin)
        ):
            findings.append(Finding("LIVE_ARM_FREEZE_SEAL_MISSING", "UNKNOWN", "A V2 shadow scope requires the independently pinned live-arm V2 freeze seal.", manifest_name))
        else:
            expected_parent_arm = "live" if profile_name == "operational_live_with_shadow" else "matched_baseline"
            expected_parent_routing = "enabled" if profile_name == "operational_live_with_shadow" else "frozen_nonrouting"
            _validate_v2_freeze_seal_fields(
                live_arm_freeze_seal,
                findings,
                expected_arm=expected_parent_arm,
                expected_cohort_kind="initial",
            )
            if _json_payload_sha256(live_arm_freeze_seal) != supplied_live_pin:
                findings.append(Finding("LIVE_ARM_FREEZE_SEAL_PAYLOAD_HASH_MISMATCH", "ERROR", "The supplied V2 live-arm seal payload differs from its digest pin."))
            if (
                run_live_pin != supplied_live_pin
                or not isinstance(freeze_seal, dict)
                or freeze_seal.get("live_arm_freeze_seal_sha256") != supplied_live_pin
            ):
                findings.append(Finding("LIVE_ARM_FREEZE_SEAL_PIN_MISMATCH", "ERROR", "Shadow run, snapshot, external shadow seal, and supplied live-arm seal must bind one exact digest.", manifest_name, run_record.get("_line")))
            if (
                live_arm_freeze_seal.get("schema") != FREEZE_SEAL_SCHEMA_V2
                or live_arm_freeze_seal.get("arm") != expected_parent_arm
                or live_arm_freeze_seal.get("mode") != "audited_funnel"
                or live_arm_freeze_seal.get("routing_state") != expected_parent_routing
                or live_arm_freeze_seal.get("run_profile") != profile_name
                or live_arm_freeze_seal.get("model") != run_record.get("model")
                or live_arm_freeze_seal.get("reasoning_effort") != run_record.get("reasoning_effort")
            ):
                findings.append(Finding("LIVE_ARM_FREEZE_SEAL_IDENTITY_INVALID", "ERROR", "The supplied V2 parent-arm seal is not the exact profile, routing, model, and effort identity.", manifest_name))
            live_sealed_at = _parse_timestamp(live_arm_freeze_seal.get("sealed_at"))
            shadow_started_at = _parse_timestamp(run_record.get("started_at"))
            if live_sealed_at is None or shadow_started_at is None or live_sealed_at >= shadow_started_at:
                findings.append(Finding("SHADOW_DISPATCH_ORDER_INVALID", "ERROR", "The live V2 seal must be strictly earlier than the shadow run start.", manifest_name))

    excluded_roots = _declared_child_relative_paths(run_dir, run_record)
    _audit_owned_symlinks(run_dir, excluded_roots, findings)
    if isinstance(freeze_seal, dict):
        _audit_v2_manifest_snapshot(
            run_dir,
            run_record,
            manifest_records,
            freeze_seal,
            excluded_roots,
            findings,
            allow_frozen_final=shadow_dispatch_prefix,
        )
    if checkpoint in {"selection", "freeze"} and freeze_seal is None:
        _validate_v2_prefreeze_anchor(
            run_dir,
            run_record,
            protection_anchor,
            protection_anchor_sha256,
            fixed_contract_paths,
            findings,
        )
    _validate_v2_workflow_anchor(run_dir, run_record, protection_anchor, findings)
    contract = _validate_v2_development_contract(run_dir, run_record, excluded_roots, findings, manifest_name)
    if run_record.get("cohort_kind") == "regeneration":
        parent_scope_id = run_record.get("parent_scope_id")
        initial_seal_pin = run_record.get("initial_freeze_seal_sha256")
        prefreeze_without_seal = (
            checkpoint in {"selection", "freeze"} and freeze_seal is None
        )
        if (
            not isinstance(parent_scope_id, str)
            or not parent_scope_id
            or not isinstance(initial_seal_pin, str)
            or not re.fullmatch(r"[0-9a-f]{64}", initial_seal_pin)
            or (
                not prefreeze_without_seal
                and (
                    not isinstance(freeze_seal, dict)
                    or freeze_seal.get("parent_scope_id") != parent_scope_id
                    or freeze_seal.get("initial_freeze_seal_sha256")
                    != initial_seal_pin
                )
            )
        ):
            findings.append(Finding("REGENERATION_LINEAGE_INVALID", "ERROR", "A regeneration run and V2 freeze seal must bind parent_scope_id and initial_freeze_seal_sha256.", manifest_name, run_record.get("_line")))
        _audit_v2_regeneration_initial_seal(
            run_record,
            freeze_seal,
            initial_freeze_seal,
            initial_freeze_seal_sha256,
            findings,
            artifact=manifest_name,
        )
    _audit_v2_state_chain(run_record, manifest_records, run_dir, excluded_roots, findings, checkpoint)
    _audit_v2_terminal_lifecycle_times(
        run_record, manifest_records, findings, artifact=manifest_name
    )

    for agent in (record for record in manifest_records if record.get("record_type") == "agent"):
        for field in ("allowlisted_files", "files_read"):
            values, valid = _valid_string_list(agent.get(field), allow_empty=True)
            if not valid:
                continue
            for value in values:
                if _strict_run_file(run_dir, value, excluded_roots) is None:
                    findings.append(Finding("V2_CONTEXT_PATH_INVALID", "ERROR", f"Agent {agent.get('agent_id')} has a non-relative, missing, symlinked, out-of-scope, or child-owned {field} path {value!r}.", manifest_name, agent.get("_line"), (str(agent.get("agent_id")),)))
        context_files = agent.get("context_files")
        if isinstance(context_files, list):
            for item in context_files:
                if not isinstance(item, dict):
                    continue
                parsed = _strict_run_file(run_dir, item.get("path"), excluded_roots)
                if parsed is None or item.get("sha256") != _sha256(parsed[0]):
                    findings.append(Finding("V2_CONTEXT_PACKET_INVALID", "ERROR", f"Agent {agent.get('agent_id')} has an escaping, symlinked, child-owned, missing, or hash-mismatched context packet.", manifest_name, agent.get("_line"), (str(agent.get("agent_id")),)))

    for record in ledger_records:
        if record.get("record_type") not in {"level2", "finalist"}:
            continue
        artifact_value = record.get("artifact_path")
        if artifact_value is None and record.get("development_status") == "early_stop":
            continue
        stable_id = record.get("concept_id") or record.get("finalist_id")
        parsed = _strict_run_file(run_dir, artifact_value, excluded_roots)
        if parsed is None or record.get("sha256") != _sha256(parsed[0]):
            findings.append(
                Finding(
                    "V2_ARTIFACT_PATH_INVALID",
                    "ERROR",
                    f"Artifact {stable_id!r} must be a hash-bound, regular, non-symlink file owned by this scope.",
                    str(artifact_value or ""),
                    record.get("_line"),
                    (str(stable_id),),
                )
            )
            continue
        if isinstance(contract, dict):
            section_field = (
                "level2_sections"
                if record.get("record_type") == "level2"
                else "frozen_sections"
            )
            required_sections, sections_valid = _valid_string_list(
                contract.get(section_field)
            )
            try:
                artifact_text = parsed[0].read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError):
                artifact_text = ""
            if sections_valid and any(
                sum(1 for line in artifact_text.splitlines() if line.strip() == section)
                != 1
                for section in required_sections
            ):
                findings.append(Finding("DEVELOPMENT_CONTRACT_SECTION_MISMATCH", "ERROR", f"Artifact {stable_id!r} does not contain every contract-bound {section_field} heading exactly once.", parsed[1], record.get("_line"), (str(stable_id),)))
            measurement = contract.get("dossier_measurement")
            counted_sections = (
                measurement.get("counted_sections")
                if isinstance(measurement, dict)
                else None
            )
            ranges = contract.get("dossier_prose_word_ranges")
            range_key = "level2" if record.get("record_type") == "level2" else "frozen"
            word_range = ranges.get(range_key) if isinstance(ranges, dict) else None
            section_word_counts = (
                _dossier_prose_section_word_counts(parsed[0], counted_sections)
                if isinstance(counted_sections, list)
                else None
            )
            word_count = (
                sum(section_word_counts.values())
                if section_word_counts is not None
                else None
            )
            minimum = _as_decimal(word_range.get("minimum")) if isinstance(word_range, dict) else None
            maximum = _as_decimal(word_range.get("maximum")) if isinstance(word_range, dict) else None
            minimum_per_section = _as_decimal(word_range.get("minimum_per_section")) if isinstance(word_range, dict) else None
            if (
                word_count is None
                or minimum is None
                or maximum is None
                or minimum_per_section is None
                or not (minimum <= Decimal(word_count) <= maximum)
                or any(
                    Decimal(words) < minimum_per_section
                    for words in (section_word_counts or {}).values()
                )
            ):
                findings.append(Finding("DEVELOPMENT_CONTRACT_WORD_RANGE_MISMATCH", "ERROR", f"Artifact {stable_id!r} is outside the contract-bound persuasive-prose range; sources, trace material, telemetry, and machine metadata are excluded.", parsed[1], record.get("_line"), (str(stable_id),)))
        if record.get("record_type") == "finalist":
            if (
                record.get("arm") != run_record.get("arm")
                or record.get("shadow_only")
                is not (run_record.get("routing_state") == "frozen_nonrouting")
                or record.get("validation_eligible")
                is not (run_record.get("routing_state") == "enabled")
            ):
                findings.append(
                    Finding(
                        "FINALIST_COMPATIBILITY_MIRROR_MISMATCH",
                        "ERROR",
                        f"Finalist {stable_id!r} arm/shadow_only/validation_eligible must exactly mirror authoritative V2 routing.",
                        parsed[1],
                        record.get("_line"),
                        (str(stable_id),),
                    )
                )

    registered_candidate_artifacts = {
        parsed[1]
        for record in ledger_records
        if record.get("record_type") in {"level2", "finalist"}
        and (parsed := _strict_run_file(run_dir, record.get("artifact_path"), excluded_roots))
        is not None
    }
    registered_agent_input_artifacts: set[str] = set()
    for agent in (
        record
        for record in manifest_records
        if record.get("record_type") == "agent"
    ):
        context_files = agent.get("context_files")
        if isinstance(context_files, list):
            for item in context_files:
                if not isinstance(item, dict):
                    continue
                parsed = _strict_run_file(
                    run_dir, item.get("path"), excluded_roots
                )
                if parsed is not None:
                    registered_agent_input_artifacts.add(parsed[1])
        files_read, files_read_valid = _valid_string_list(
            agent.get("files_read"), allow_empty=True
        )
        if files_read_valid:
            for value in files_read:
                parsed = _strict_run_file(run_dir, value, excluded_roots)
                if parsed is not None:
                    registered_agent_input_artifacts.add(parsed[1])
    candidate_owned_roots = {
        "level2",
        "live_level2",
        "shadow_level2",
        "shadow_candidates",
        "frozen_candidates",
    }
    dossier_headings = set(REQUIRED_LEVEL2_SECTIONS)
    for owned_path in _owned_files(run_dir, excluded_roots):
        if not owned_path.is_file() or owned_path.is_symlink():
            continue
        relative = owned_path.relative_to(run_dir).as_posix()
        relative_parts = Path(relative).parts
        if (
            relative_parts
            and relative_parts[0] in candidate_owned_roots
            and relative not in registered_candidate_artifacts
        ):
            findings.append(
                Finding(
                    "UNREGISTERED_CANDIDATE_ARTIFACT",
                    "ERROR",
                    "Every regular file in a candidate-owned namespace must be the exact artifact_path of one typed Level-2/finalist record.",
                    relative,
                )
            )
        try:
            if owned_path.stat().st_size > 5_000_000:
                raise ValueError("owned file exceeds the bounded scanner limit")
            owned_text = owned_path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError, ValueError) as exc:
            findings.append(
                Finding(
                    "OWNED_ARTIFACT_SCAN_INCOMPLETE",
                    "ERROR",
                    f"Owned artifact cannot be completely scanned: {exc}.",
                    relative,
                )
            )
            continue
        regeneration_control_artifact = _is_regeneration_control_artifact(
            run_dir,
            run_record,
            manifest_records,
            freeze_seal,
            owned_path,
            relative,
            owned_text,
        )
        control_records = (
            _parse_closed_v2_manifest_text(owned_text)
            if regeneration_control_artifact
            else None
        )
        if (
            run_record.get("cohort_kind") == "regeneration"
            and run_record.get("routing_state") == "enabled"
            and control_records is not None
            and _regeneration_control_records_contaminated(control_records)
        ):
            findings.append(
                Finding(
                    "REGENERATION_CONTEXT_CONTAMINATION",
                    "ERROR",
                    "An enabled regeneration machine manifest/snapshot contains evaluator/advisory, validator-feedback, judge/panel-ranking, or shadow/matched-output material in a semantic field.",
                    relative,
                )
            )
        elif (
            control_records is None
            and (
                not regeneration_control_artifact
                or relative in registered_agent_input_artifacts
                or relative in registered_candidate_artifacts
            )
        ):
            _audit_regeneration_owned_content(
                run_record,
                owned_path,
                relative,
                owned_text,
                findings,
            )
        observed_headings = {
            line.strip() for line in owned_text.splitlines() if line.startswith("## ")
        }
        if (
            dossier_headings.issubset(observed_headings)
            and relative not in registered_candidate_artifacts
        ):
            findings.append(
                Finding(
                    "UNREGISTERED_CANDIDATE_ARTIFACT",
                    "ERROR",
                    "A dossier-shaped owned artifact is absent from the exact Level-2/finalist ledger inventory.",
                    relative,
                )
            )

    if run_record.get("cohort_kind") == "regeneration":
        expected_wave = run_record.get("wave_index")
        wave_namespace = re.compile(
            rf"^wave{expected_wave}_candidate_[A-Za-z0-9_.-]+\.md$"
        )
        for finalist in (
            record
            for record in ledger_records
            if record.get("record_type") == "finalist"
        ):
            raw_artifact = finalist.get("artifact_path")
            artifact_name = (
                Path(raw_artifact).name if isinstance(raw_artifact, str) else ""
            )
            if not wave_namespace.fullmatch(artifact_name):
                findings.append(
                    Finding(
                        "REGENERATION_CANDIDATE_NAMESPACE_INVALID",
                        "ERROR",
                        f"Regeneration finalist {finalist.get('finalist_id')!r} must use the exact wave{expected_wave}_candidate_*.md namespace.",
                        str(raw_artifact or ""),
                        finalist.get("_line"),
                        (str(finalist.get("finalist_id")),),
                    )
                )

    if isinstance(contract, dict):
        allowed_contract_statuses, statuses_valid = _valid_string_list(
            contract.get("evidence_statuses")
        )
        if statuses_valid:
            for record in ledger_records:
                if record.get("record_type") == "evidence" and record.get("status") not in set(allowed_contract_statuses):
                    findings.append(Finding("DEVELOPMENT_CONTRACT_EVIDENCE_STATUS_MISMATCH", "ERROR", f"Evidence {record.get('evidence_id')!r} uses a status outside the development contract.", "02b_raw_to_direction_ledger.jsonl", record.get("_line"), (str(record.get("evidence_id")),)))

    _audit_v2_development_failure_receipt(
        run_dir, run_record, manifest_records, excluded_roots, findings
    )
    _audit_v2_research_chains(run_dir, run_record, manifest_records, ledger_records, contract, excluded_roots, findings, resources, checkpoint)

    if shadow_dispatch_prefix:
        _audit_v2_shadow_dispatch_preregistration(
            run_dir,
            run_record,
            manifest_records,
            findings,
            protection_anchor=protection_anchor,
            protection_anchor_sha256=protection_anchor_sha256,
            child_protection_anchor=child_protection_anchor,
            child_protection_anchor_sha256=child_protection_anchor_sha256,
            freeze_seal=freeze_seal,
            freeze_seal_sha256=freeze_seal_sha256,
            child_trust_bundle=child_trust_bundle,
            child_trust_bundle_sha256=child_trust_bundle_sha256,
            fixed_contract_paths=fixed_contract_paths,
        )
        _audit_v2_nonrouting_owned_content(
            run_dir, run_record, ledger_records, excluded_roots, findings
        )
        return

    if run_record.get("lifecycle_state") != "complete":
        declarations_value = run_record.get("declared_child_scopes")
        declarations = (
            [item for item in declarations_value if isinstance(item, dict)]
            if isinstance(declarations_value, list)
            else []
        )
        if (
            not isinstance(declarations_value, list)
            or len(declarations) != len(declarations_value)
        ):
            findings.append(
                Finding(
                    "CHILD_SCOPE_DECLARATIONS_INVALID",
                    "ERROR",
                    "A lifecycle prefix must preserve its typed preregistered child declarations.",
                    manifest_name,
                    run_record.get("_line"),
                )
            )
        for declaration in declarations:
            child_scope_id = declaration.get("scope_id")
            reserved = _strict_reserved_child_directory(
                run_dir, declaration.get("relative_path")
            )
            final_fields_are_null = all(
                declaration.get(field) is None
                for field in CHILD_FINALIZATION_FIELDS_V2
            )
            if (
                set(declaration) != CHILD_DECLARATION_FIELDS_V2
                or not isinstance(child_scope_id, str)
                or not child_scope_id
                or reserved is None
                or not final_fields_are_null
                or not isinstance(
                    declaration.get("development_contract_sha256"), str
                )
                or not isinstance(
                    declaration.get("protection_anchor_sha256"), str
                )
            ):
                findings.append(
                    Finding(
                        "CHILD_SCOPE_DECLARATION_INVALID",
                        "ERROR",
                        f"Child scope {child_scope_id!r} is not a safe null-finalization preregistration.",
                        manifest_name,
                        run_record.get("_line"),
                    )
                )
        premature_runs = _discover_nested_machine_runs(run_dir)
        if premature_runs:
            findings.append(
                Finding(
                    "PREMATURE_CHILD_DISPATCH",
                    "ERROR",
                    f"A non-complete parent prefix already contains child execution manifests: {sorted(premature_runs)}.",
                    manifest_name,
                )
            )
        if child_trust_bundle is not None or child_trust_bundle_sha256 is not None:
            findings.append(
                Finding(
                    "PREMATURE_CHILD_TRUST",
                    "ERROR",
                    "A child trust bundle cannot exist before the parent reaches the lifecycle that can dispatch and complete the child.",
                    manifest_name,
                )
            )
        _audit_v2_nonrouting_owned_content(
            run_dir, run_record, ledger_records, excluded_roots, findings
        )
        return

    declarations_value = run_record.get("declared_child_scopes")
    declarations = [item for item in declarations_value if isinstance(item, dict)] if isinstance(declarations_value, list) else []
    if not isinstance(declarations_value, list) or len(declarations) != len(declarations_value):
        findings.append(Finding("CHILD_SCOPE_DECLARATIONS_INVALID", "ERROR", "declared_child_scopes must be a list of typed child declarations.", manifest_name, run_record.get("_line")))
    child_by_scope: dict[str, dict[str, Any]] = {}
    child_paths: list[Path] = []
    required_child_fields = {
        "scope_id",
        "relative_path",
        "relationship",
        "run_profile",
        "mode",
        "arm",
        "routing_state",
        "cohort_kind",
        "manifest_sha256",
        "protection_anchor_sha256",
        "freeze_seal_sha256",
        "audit_report_path",
        "audit_report_sha256",
        "audit_status",
        "model",
        "reasoning_effort",
        "results_visibility",
        "development_contract_sha256",
        "registered_at",
    }
    for declaration in declarations:
        child_scope_id = declaration.get("scope_id")
        if set(declaration) != required_child_fields:
            findings.append(Finding("CHILD_SCOPE_DECLARATION_FIELDS_INVALID", "ERROR", f"Child {child_scope_id!r} must use the exact closed declaration keys; missing={sorted(required_child_fields - set(declaration))}, extra={sorted(set(declaration) - required_child_fields)}.", manifest_name, run_record.get("_line")))
        parsed = _strict_relative_directory(run_dir, declaration.get("relative_path"))
        if not isinstance(child_scope_id, str) or not child_scope_id or child_scope_id in child_by_scope or parsed is None:
            findings.append(Finding("CHILD_SCOPE_DECLARATION_INVALID", "ERROR", f"Child scope {child_scope_id!r} has a duplicate ID or unsafe relative_path.", manifest_name, run_record.get("_line")))
            continue
        child_by_scope[child_scope_id] = declaration
        child_paths.append(Path(parsed[1]))
        if declaration.get("relationship") not in CHILD_RELATIONSHIPS_V2:
            findings.append(Finding("CHILD_SCOPE_RELATIONSHIP_INVALID", "ERROR", f"Child {child_scope_id} has unsupported relationship {declaration.get('relationship')!r}.", manifest_name))
        if declaration.get("model") != run_record.get("model") or declaration.get("reasoning_effort") != run_record.get("reasoning_effort"):
            findings.append(Finding("CHILD_MODEL_EFFORT_MISMATCH", "ERROR", f"Child {child_scope_id} does not preserve exact model and reasoning effort.", manifest_name, node_ids=(child_scope_id,)))
        if declaration.get("relationship") == "shadow_child" and (
            profile_name not in {"operational_live_with_shadow", "v2_matched_nonrouting"}
            or declaration.get("run_profile") != profile_name
            or declaration.get("mode") != "archipelago_lite_shadow"
            or declaration.get("arm") != "shadow"
            or declaration.get("routing_state") != "frozen_nonrouting"
            or declaration.get("cohort_kind") != "initial"
        ):
            findings.append(Finding("CHILD_SCOPE_SEMANTICS_MISMATCH", "ERROR", f"Shadow child {child_scope_id} must be initial, shadow, and frozen_nonrouting.", manifest_name, node_ids=(child_scope_id,)))
        if declaration.get("relationship") == "regeneration" and (
            declaration.get("run_profile") != "ordinary_audited_funnel"
            or declaration.get("mode") != "audited_funnel"
            or declaration.get("arm") != "live"
            or declaration.get("routing_state") != "enabled"
            or declaration.get("cohort_kind") != "regeneration"
        ):
            findings.append(Finding("CHILD_SCOPE_SEMANTICS_MISMATCH", "ERROR", f"Regeneration child {child_scope_id} must use the exact ordinary live regeneration profile.", manifest_name, node_ids=(child_scope_id,)))
    for left_index, left in enumerate(child_paths):
        for right in child_paths[left_index + 1 :]:
            if _relative_is_excluded(left, {right.as_posix()}) or _relative_is_excluded(right, {left.as_posix()}):
                findings.append(Finding("CHILD_SCOPE_OVERLAP", "ERROR", f"Declared child paths {left} and {right} overlap."))

    declared_run_paths = {
        Path(str(item.get("relative_path"))).as_posix()
        for item in declarations
        if _strict_relative_directory(run_dir, item.get("relative_path")) is not None
    }
    discovered_run_paths = _discover_nested_machine_runs(run_dir)
    for undeclared in sorted(discovered_run_paths - declared_run_paths):
        findings.append(
            Finding(
                "CHILD_RUN_UNDECLARED",
                "ERROR",
                "Nested machine-run manifest is not registered as an exact child scope.",
                f"{undeclared}/00a_context_and_resource_manifest.jsonl",
            )
        )
    for missing in sorted(declared_run_paths - discovered_run_paths):
        findings.append(
            Finding(
                "CHILD_RUN_MANIFEST_MISSING",
                "ERROR",
                "Declared child scope has no exact nested machine manifest.",
                f"{missing}/00a_context_and_resource_manifest.jsonl",
            )
        )

    shadow_declarations = [item for item in declarations if item.get("relationship") == "shadow_child"]
    regeneration_declarations = [item for item in declarations if item.get("relationship") == "regeneration"]
    if profile_name == "ordinary_audited_funnel" and shadow_declarations:
        findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "ordinary_audited_funnel may declare regeneration children but no shadow child.", manifest_name))
    if profile_name == "ordinary_audited_funnel" and regeneration_declarations and (
        run_record.get("cohort_kind") != "initial"
        or run_record.get("arm") != "live"
        or run_record.get("routing_state") != "enabled"
    ):
        findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "Only an initial routing-enabled ordinary live root may declare direct regeneration children; regeneration rebasing/nesting is forbidden.", manifest_name))
    if profile_name == "operational_live_with_shadow":
        if run_record.get("arm") == "live" and len(shadow_declarations) != 1:
            findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "A live operational_live_with_shadow root requires exactly one declared shadow child.", manifest_name))
        if run_record.get("arm") == "shadow" and declarations:
            findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "An operational shadow child cannot itself declare child scopes.", manifest_name))
    if profile_name == "v2_matched_nonrouting":
        if run_record.get("arm") == "matched_baseline" and len(shadow_declarations) != 1:
            findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "A v2_matched_nonrouting matched-baseline root requires exactly one declared shadow child.", manifest_name))
        if run_record.get("arm") == "shadow" and declarations:
            findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "A shadow child scope cannot itself declare child scopes.", manifest_name))
        if regeneration_declarations:
            findings.append(Finding("CHILD_SCOPE_PROFILE_INVALID", "ERROR", "A frozen nonrouting matched scope cannot declare regeneration children.", manifest_name))

    child_reports: dict[str, AuditReport] = {}
    bundle_entries_by_scope: dict[str, dict[str, Any]] = {}
    if declarations:
        if not isinstance(child_trust_bundle, dict) or not isinstance(child_trust_bundle_sha256, str):
            findings.append(Finding("CHILD_TRUST_BUNDLE_MISSING", "UNKNOWN", "Declared child scopes require an independently pinned child trust bundle.", manifest_name))
        else:
            if _json_payload_sha256(child_trust_bundle) != child_trust_bundle_sha256:
                findings.append(Finding("CHILD_TRUST_BUNDLE_HASH_MISMATCH", "ERROR", "Child trust bundle payload differs from its independent SHA-256 pin."))
            if set(child_trust_bundle) != {"schema", "parent_scope_id", "children"}:
                findings.append(Finding("CHILD_TRUST_BUNDLE_FIELDS_INVALID", "ERROR", "Child trust bundle must use exactly schema, parent_scope_id, and children; aliases and extra top-level keys are invalid."))
            if child_trust_bundle.get("schema") != CHILD_TRUST_BUNDLE_SCHEMA_V2 or child_trust_bundle.get("parent_scope_id") != scope_id:
                findings.append(Finding("CHILD_TRUST_BUNDLE_IDENTITY_INVALID", "ERROR", "Child trust bundle schema or parent_scope_id is invalid."))
            bundle_entries = child_trust_bundle.get("children")
            if not isinstance(bundle_entries, list):
                findings.append(Finding("CHILD_TRUST_BUNDLE_CHILDREN_INVALID", "ERROR", "Child trust bundle children must be a list."))
            else:
                for entry in bundle_entries:
                    entry_scope_id = entry.get("scope_id") if isinstance(entry, dict) else None
                    if not isinstance(entry, dict) or not isinstance(entry_scope_id, str) or entry_scope_id in bundle_entries_by_scope:
                        findings.append(Finding("CHILD_TRUST_BUNDLE_ENTRY_INVALID", "ERROR", f"Malformed or duplicate trust entry {entry_scope_id!r}."))
                        continue
                    trust_keys = {
                        "scope_id",
                        "protection_anchor_path",
                        "protection_anchor_sha256",
                        "freeze_seal_path",
                        "freeze_seal_sha256",
                        "manifest_sha256",
                        "development_contract_sha256",
                        "audit_report_sha256",
                        "audit_status",
                        "model",
                        "reasoning_effort",
                        "results_visibility",
                    }
                    declaration = child_by_scope.get(entry_scope_id)
                    if isinstance(declaration, dict) and declaration.get("relationship") == "shadow_child":
                        trust_keys |= {
                            "live_arm_freeze_seal_path",
                            "live_arm_freeze_seal_sha256",
                        }
                    if set(entry) != trust_keys:
                        findings.append(
                            Finding(
                                "CHILD_TRUST_BUNDLE_ENTRY_FIELDS_INVALID",
                                "ERROR",
                                f"Trust entry {entry_scope_id} must use exact closed keys; missing={sorted(trust_keys - set(entry))}, extra={sorted(set(entry) - trust_keys)}.",
                                node_ids=(entry_scope_id,),
                            )
                        )
                    bundle_entries_by_scope[entry_scope_id] = entry
                if set(bundle_entries_by_scope) != set(child_by_scope):
                    findings.append(Finding("CHILD_TRUST_BUNDLE_SET_MISMATCH", "ERROR", "Child trust bundle scope IDs differ from declared_child_scopes."))

    parent_machine_ids = _scope_cross_scope_machine_ids(manifest_records, ledger_records)
    observed_child_machine_ids: set[str] = set()
    observed_regeneration_waves: set[int] = set()
    child_completion_times: dict[str, datetime] = {}
    parent_inode_owners: dict[tuple[int, int], str] = {}
    for parent_path in _owned_files(run_dir, excluded_roots):
        try:
            if parent_path.is_file() and not parent_path.is_symlink():
                stat = parent_path.stat()
                parent_inode_owners[(stat.st_dev, stat.st_ino)] = parent_path.relative_to(run_dir).as_posix()
        except OSError:
            continue

    for child_scope_id, declaration in child_by_scope.items():
        entry = bundle_entries_by_scope.get(child_scope_id)
        if entry is None:
            continue
        child_dir_parsed = _strict_relative_directory(run_dir, declaration.get("relative_path"))
        if child_dir_parsed is None:
            continue
        child_dir = child_dir_parsed[0]
        child_manifest_path = child_dir / manifest_name
        child_manifest_digest = _sha256(child_manifest_path) if child_manifest_path.is_file() and not child_manifest_path.is_symlink() else None
        child_manifest_findings: list[Finding] = []
        child_manifest_records = (
            _read_jsonl(child_manifest_path, child_manifest_findings)
            if child_manifest_digest is not None
            else []
        )
        child_ledger_path = child_dir / "02b_raw_to_direction_ledger.jsonl"
        child_ledger_findings: list[Finding] = []
        child_ledger_records = (
            _read_jsonl(child_ledger_path, child_ledger_findings)
            if child_ledger_path.is_file() and not child_ledger_path.is_symlink()
            else []
        )
        child_machine_ids = _scope_cross_scope_machine_ids(
            child_manifest_records, child_ledger_records
        )
        collided_machine_ids = sorted(
            child_machine_ids
            & (parent_machine_ids | observed_child_machine_ids)
        )
        if collided_machine_ids:
            findings.append(
                Finding(
                    "CROSS_SCOPE_MACHINE_ID_COLLISION",
                    "ERROR",
                    f"Child {child_scope_id} reuses typed machine IDs owned by its parent or another child: {collided_machine_ids}.",
                    declaration.get("relative_path", ""),
                    node_ids=tuple(collided_machine_ids),
                )
            )
        observed_child_machine_ids.update(child_machine_ids)
        for child_path in _owned_files(child_dir, set()):
            try:
                if not child_path.is_file() or child_path.is_symlink():
                    continue
                stat = child_path.stat()
                inode = (stat.st_dev, stat.st_ino)
            except OSError:
                continue
            prior_owner = parent_inode_owners.get(inode)
            if prior_owner is not None:
                findings.append(
                    Finding(
                        "CROSS_SCOPE_INODE_ALIAS",
                        "ERROR",
                        f"Child {child_scope_id} file is a hard-link/inode alias of another scope file {prior_owner!r}.",
                        child_path.relative_to(run_dir).as_posix(),
                        node_ids=(child_scope_id,),
                    )
                )
            else:
                parent_inode_owners[inode] = child_path.relative_to(run_dir).as_posix()
        findings.extend(
            Finding(
                "CHILD_MANIFEST_INVALID",
                item.severity,
                item.message,
                child_manifest_path.relative_to(run_dir).as_posix(),
                item.line,
                (child_scope_id,),
            )
            for item in child_manifest_findings
        )
        child_run_records = [
            item for item in child_manifest_records if item.get("record_type") == "run"
        ]
        child_run_record = child_run_records[0] if len(child_run_records) == 1 else None
        child_complete_times = [
            parsed
            for item in child_manifest_records
            if item.get("record_type") == "checkpoint"
            and item.get("state") == "complete"
            and (parsed := _parse_timestamp(item.get("occurred_at"))) is not None
        ]
        if len(child_complete_times) == 1:
            child_completion_times[child_scope_id] = child_complete_times[0]
        repeated_fields = (
            "manifest_sha256",
            "development_contract_sha256",
            "audit_report_sha256",
            "audit_status",
            "model",
            "reasoning_effort",
            "results_visibility",
        )
        if any(entry.get(field) != declaration.get(field) for field in repeated_fields):
            findings.append(Finding("CHILD_TRUST_DECLARATION_MISMATCH", "ERROR", f"Child {child_scope_id} trust entry and declaration disagree on identity, report, telemetry, or visibility fields.", node_ids=(child_scope_id,)))
        if child_manifest_digest is None or child_manifest_digest != declaration.get("manifest_sha256"):
            findings.append(Finding("CHILD_MANIFEST_HASH_MISMATCH", "ERROR", f"Child {child_scope_id}'s raw machine manifest does not match its independent pin.", child_manifest_path.relative_to(run_dir).as_posix(), node_ids=(child_scope_id,)))
        if child_run_record is None:
            findings.append(Finding("CHILD_RUN_RECORD_INVALID", "ERROR", f"Child {child_scope_id} must have exactly one typed run record.", child_manifest_path.relative_to(run_dir).as_posix(), node_ids=(child_scope_id,)))
        else:
            identity_fields = (
                "scope_id",
                "run_profile",
                "mode",
                "arm",
                "routing_state",
                "cohort_kind",
                "model",
                "reasoning_effort",
                "results_visibility",
                "development_contract_sha256",
            )
            mismatches = [
                field
                for field in identity_fields
                if child_run_record.get(field) != declaration.get(field)
            ]
            if mismatches:
                findings.append(Finding("CHILD_RUN_IDENTITY_MISMATCH", "ERROR", f"Child {child_scope_id}'s manifest differs from its declaration for fields {mismatches}.", child_manifest_path.relative_to(run_dir).as_posix(), child_run_record.get("_line"), (child_scope_id,)))
            registered_at = _parse_timestamp(declaration.get("registered_at"))
            event_times = [
                parsed
                for item in child_manifest_records
                if item.get("record_type") != "run"
                for key in ("created_at", "started_at", "occurred_at")
                for parsed in [_parse_timestamp(item.get(key))]
                if parsed is not None
            ]
            child_run_start = _parse_timestamp(child_run_record.get("started_at"))
            if child_run_start is not None:
                event_times.append(child_run_start)
            parent_start = _parse_timestamp(run_record.get("started_at"))
            parent_end = _parse_timestamp(run_record.get("ended_at"))
            if (
                registered_at is None
                or parent_start is None
                or parent_end is None
                or registered_at < parent_start
                or registered_at > parent_end
                or not event_times
                or registered_at >= min(event_times)
            ):
                findings.append(Finding("CHILD_REGISTRATION_TIME_INVALID", "ERROR", f"Child {child_scope_id} must be registered inside the exact parent start/end window and strictly before its first event.", manifest_name, node_ids=(child_scope_id,)))
            child_contract_path = child_dir / "00b_development_contract.json"
            child_contract_digest = _sha256(child_contract_path) if child_contract_path.is_file() and not child_contract_path.is_symlink() else None
            if child_contract_digest != declaration.get("development_contract_sha256"):
                findings.append(Finding("DEVELOPMENT_CONTRACT_MISMATCH", "ERROR", f"Child {child_scope_id}'s actual development-contract bytes differ from the declared and trusted hash.", child_contract_path.relative_to(run_dir).as_posix(), node_ids=(child_scope_id,)))
            if declaration.get("relationship") == "shadow_child" and declaration.get("results_visibility") != "withheld":
                findings.append(Finding("SHADOW_RESULTS_VISIBILITY_INVALID", "ERROR", f"Shadow child {child_scope_id} must keep results_visibility=withheld through irreversible live close.", manifest_name, node_ids=(child_scope_id,)))
            if declaration.get("relationship") == "regeneration":
                child_wave = child_run_record.get("wave_index")
                if (
                    not isinstance(child_wave, int)
                    or isinstance(child_wave, bool)
                    or child_wave < 2
                    or child_wave in observed_regeneration_waves
                ):
                    findings.append(Finding("REGENERATION_WAVE_DUPLICATE", "ERROR", f"Regeneration child {child_scope_id} must use one unique wave_index >=2 among its initial root's children.", child_manifest_path.relative_to(run_dir).as_posix(), child_run_record.get("_line"), (child_scope_id,)))
                else:
                    observed_regeneration_waves.add(child_wave)
        pin_pairs = (
            ("protection_anchor_path", "protection_anchor_sha256"),
            ("freeze_seal_path", "freeze_seal_sha256"),
        )
        loaded: dict[str, dict[str, Any]] = {}
        pins_valid = True
        for path_key, digest_key in pin_pairs:
            raw_path = entry.get(path_key)
            digest = entry.get(digest_key)
            if declaration.get(digest_key) != digest or not isinstance(raw_path, str) or not Path(raw_path).is_absolute() or not isinstance(digest, str):
                findings.append(Finding("CHILD_TRUST_PIN_MISMATCH", "ERROR", f"Child {child_scope_id} has an absent, aliased, or declaration-mismatched {digest_key}.", node_ids=(child_scope_id,)))
                pins_valid = False
                continue
            try:
                loaded[path_key], _observed = _read_pinned_external_json(Path(raw_path), digest, run_dir)
            except (OSError, ValueError) as exc:
                findings.append(Finding("CHILD_TRUST_PIN_INVALID", "ERROR", f"Child {child_scope_id} {path_key} cannot be independently verified: {exc}.", node_ids=(child_scope_id,)))
                pins_valid = False
        live_seal_payload: dict[str, Any] | None = None
        live_seal_digest: str | None = None
        if declaration.get("relationship") == "shadow_child":
            raw_path = entry.get("live_arm_freeze_seal_path")
            live_seal_digest = entry.get("live_arm_freeze_seal_sha256")
            if not isinstance(raw_path, str) or not Path(raw_path).is_absolute() or not isinstance(live_seal_digest, str):
                findings.append(Finding("CHILD_LIVE_SEAL_PIN_MISSING", "ERROR", f"Shadow child {child_scope_id} lacks an external live-arm seal path and pin.", node_ids=(child_scope_id,)))
                pins_valid = False
            else:
                try:
                    live_seal_payload, _observed = _read_pinned_external_json(Path(raw_path), live_seal_digest, run_dir)
                except (OSError, ValueError) as exc:
                    findings.append(Finding("CHILD_LIVE_SEAL_PIN_INVALID", "ERROR", f"Shadow child {child_scope_id} live-arm seal cannot be verified: {exc}.", node_ids=(child_scope_id,)))
                    pins_valid = False
        if entry.get("development_contract_sha256") != declaration.get("development_contract_sha256"):
            findings.append(Finding("DEVELOPMENT_CONTRACT_MISMATCH", "ERROR", f"Child trust entry and declaration disagree on {child_scope_id}'s development contract hash.", node_ids=(child_scope_id,)))
        if declaration.get("cohort_kind") == "initial" and declaration.get("relationship") == "shadow_child" and declaration.get("development_contract_sha256") != run_record.get("development_contract_sha256"):
            findings.append(Finding("DEVELOPMENT_CONTRACT_MISMATCH", "ERROR", f"Matched initial child {child_scope_id} does not share the parent's exact raw-byte development contract.", node_ids=(child_scope_id,)))
        if not pins_valid:
            continue
        if declaration.get("relationship") == "shadow_child":
            expected_parent_arm = (
                "live"
                if profile_name == "operational_live_with_shadow"
                else "matched_baseline"
            )
            expected_parent_routing = (
                "enabled"
                if profile_name == "operational_live_with_shadow"
                else "frozen_nonrouting"
            )
            if (
                live_seal_digest != freeze_seal_sha256
                or not isinstance(live_seal_payload, dict)
                or live_seal_payload.get("schema") != FREEZE_SEAL_SCHEMA_V2
                or live_seal_payload.get("scope_id") != scope_id
                or live_seal_payload.get("run_profile") != profile_name
                or live_seal_payload.get("arm") != expected_parent_arm
                or live_seal_payload.get("routing_state") != expected_parent_routing
                or live_seal_payload.get("model") != run_record.get("model")
                or live_seal_payload.get("reasoning_effort") != run_record.get("reasoning_effort")
            ):
                findings.append(Finding("CHILD_LIVE_SEAL_IDENTITY_INVALID", "ERROR", f"Shadow child {child_scope_id} is not bound to this parent's independently pinned V2 live freeze seal.", node_ids=(child_scope_id,)))
            live_sealed_at = _parse_timestamp(live_seal_payload.get("sealed_at")) if isinstance(live_seal_payload, dict) else None
            child_event_times = [
                parsed
                for item in child_manifest_records
                if item.get("record_type") != "run"
                for key in ("created_at", "started_at", "occurred_at")
                for parsed in [_parse_timestamp(item.get(key))]
                if parsed is not None
            ]
            if isinstance(child_run_record, dict):
                child_run_start = _parse_timestamp(child_run_record.get("started_at"))
                if child_run_start is not None:
                    child_event_times.append(child_run_start)
            if live_sealed_at is None or not child_event_times or min(child_event_times) <= live_sealed_at:
                findings.append(Finding("SHADOW_DISPATCH_ORDER_INVALID", "ERROR", f"Shadow child {child_scope_id} began before the live V2 freeze seal was irreversible.", node_ids=(child_scope_id,)))
        if declaration.get("relationship") == "regeneration":
            child_freeze = loaded.get("freeze_seal_path")
            if (
                run_record.get("cohort_kind") != "initial"
                or
                not isinstance(child_run_record, dict)
                or child_run_record.get("parent_scope_id") != scope_id
                or child_run_record.get("initial_freeze_seal_sha256") != freeze_seal_sha256
                or not isinstance(child_freeze, dict)
                or child_freeze.get("parent_scope_id") != scope_id
                or child_freeze.get("initial_freeze_seal_sha256") != freeze_seal_sha256
            ):
                findings.append(Finding("REGENERATION_LINEAGE_INVALID", "ERROR", f"Regeneration child {child_scope_id} and its seal must bind parent_scope_id and the initial freeze-seal pin.", node_ids=(child_scope_id,)))
            release_at = _parse_timestamp(run_record.get("shadow_results_released_at"))
            regeneration_start = _parse_timestamp(child_run_record.get("started_at")) if isinstance(child_run_record, dict) else None
            if release_at is not None and (regeneration_start is None or regeneration_start >= release_at):
                findings.append(Finding("REGENERATION_AFTER_SHADOW_RELEASE", "ERROR", f"Regeneration child {child_scope_id} started at or after typed shadow-result release.", node_ids=(child_scope_id,)))
        child_report = audit_run(
            child_dir,
            strict,
            protection_anchor=loaded.get("protection_anchor_path"),
            protection_anchor_sha256=entry.get("protection_anchor_sha256"),
            freeze_seal=loaded.get("freeze_seal_path"),
            freeze_seal_sha256=entry.get("freeze_seal_sha256"),
            live_arm_freeze_seal=live_seal_payload,
            live_arm_freeze_seal_sha256=live_seal_digest,
            initial_freeze_seal=(
                freeze_seal
                if declaration.get("relationship") == "regeneration"
                else None
            ),
            initial_freeze_seal_sha256=(
                freeze_seal_sha256
                if declaration.get("relationship") == "regeneration"
                else None
            ),
            checkpoint=None,
            _fixed_contract_paths=fixed_contract_paths,
            _scope_stack=scope_stack + (canonical_scope,),
        )
        child_reports[child_scope_id] = child_report
        severity = "ERROR" if child_report.status == "FAIL" else "UNKNOWN" if child_report.status == "INCOMPLETE" else "WARNING" if child_report.status == "PASS_WITH_WARNINGS" else "INFO"
        if child_report.status != "PASS":
            findings.append(Finding("CHILD_SCOPE_AUDIT_NOT_PASS", severity, f"Recursive audit of child {child_scope_id} returned {child_report.status} with {len(child_report.findings)} findings.", declaration.get("relative_path", ""), node_ids=(child_scope_id,)))
        raw_report_path = declaration.get("audit_report_path")
        child_relative = Path(str(declaration.get("relative_path")))
        report_relative = Path(str(raw_report_path)) if isinstance(raw_report_path, str) else Path()
        try:
            report_inside_child = report_relative.relative_to(child_relative)
        except ValueError:
            report_inside_child = Path()
        report_path = (
            _strict_run_file(child_dir, report_inside_child.as_posix())
            if report_inside_child.parts
            else None
        )
        if report_path is None:
            findings.append(Finding("CHILD_AUDIT_REPORT_SCOPE_INVALID", "ERROR", f"Child {child_scope_id}'s audit_report_path must begin with its exact relative_path and resolve inside that child only.", str(raw_report_path), node_ids=(child_scope_id,)))
        elif declaration.get("audit_report_sha256") != _sha256(report_path[0]):
            findings.append(Finding("CHILD_AUDIT_REPORT_PIN_INVALID", "ERROR", f"Child {child_scope_id}'s saved audit report is hash-mismatched.", str(raw_report_path), node_ids=(child_scope_id,)))
        else:
            try:
                saved_report_bytes = report_path[0].read_bytes()
                saved_report = json.loads(saved_report_bytes.decode("utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                saved_report_bytes = b""
                saved_report = None
            saved_status = saved_report.get("status") if isinstance(saved_report, dict) else None
            if saved_status != declaration.get("audit_status") or saved_status != child_report.status:
                findings.append(Finding("CHILD_AUDIT_STATUS_MISMATCH", "ERROR", f"Child {child_scope_id}'s declared, saved, and recomputed audit statuses differ.", raw_report_path, node_ids=(child_scope_id,)))
            expected_report_payload = json.loads(child_report.to_json())
            if (
                saved_report != expected_report_payload
                or saved_report_bytes != _json_bytes(expected_report_payload)
            ):
                findings.append(
                    Finding(
                        "CHILD_AUDIT_REPORT_CONTENT_MISMATCH",
                        "ERROR",
                        f"Child {child_scope_id}'s saved report is not the complete canonical recomputed native report bytes.",
                        str(raw_report_path),
                        node_ids=(child_scope_id,),
                    )
                )
        parent_metrics = resources.get("development_metrics")
        child_metrics = child_report.resources.get("development_metrics")
        if declaration.get("relationship") == "shadow_child" and isinstance(parent_metrics, dict) and isinstance(child_metrics, dict):
            _compare_development_parity(parent_metrics, child_metrics, child_scope_id, findings)
        elif declaration.get("relationship") == "shadow_child":
            findings.append(Finding("PARITY_METRIC_INCOMPLETE", "UNKNOWN", f"Derived matched metrics are unavailable for child {child_scope_id}.", node_ids=(child_scope_id,)))

    raw_release_at = run_record.get("shadow_results_released_at")
    if raw_release_at is not None:
        release_at = _parse_timestamp(raw_release_at)
        root_complete_times = [
            parsed
            for item in manifest_records
            if item.get("record_type") == "checkpoint"
            and item.get("state") == "complete"
            and (parsed := _parse_timestamp(item.get("occurred_at"))) is not None
        ]
        seal_time = _parse_timestamp(freeze_seal.get("sealed_at")) if isinstance(freeze_seal, dict) else None
        trust_ready = (
            isinstance(child_trust_bundle, dict)
            and isinstance(child_trust_bundle_sha256, str)
            and _json_payload_sha256(child_trust_bundle) == child_trust_bundle_sha256
            and set(bundle_entries_by_scope) == set(child_by_scope)
            and all(
                declaration.get("audit_status") == "PASS"
                and child_reports.get(child_scope_id) is not None
                and child_reports[child_scope_id].status == "PASS"
                and child_scope_id in child_completion_times
                for child_scope_id, declaration in child_by_scope.items()
            )
        )
        latest_required_time = max(
            [
                value
                for value in (
                    seal_time,
                    root_complete_times[0] if len(root_complete_times) == 1 else None,
                    *child_completion_times.values(),
                )
                if value is not None
            ],
            default=None,
        )
        if (
            profile_name not in {"operational_live_with_shadow", "v2_matched_nonrouting"}
            or release_at is None
            or len(root_complete_times) != 1
            or latest_required_time is None
            or release_at <= latest_required_time
            or not trust_ready
        ):
            findings.append(
                Finding(
                    "SHADOW_RESULTS_RELEASE_PREMATURE",
                    "ERROR",
                    "shadow_results_released_at is valid only strictly after the parent seal, parent complete checkpoint, every child complete checkpoint, PASS child audits, and the exact trusted child bundle.",
                    manifest_name,
                    run_record.get("_line"),
                )
            )
        later_live_events: list[str] = []
        if release_at is not None:
            for item in manifest_records:
                if item.get("record_type") == "run":
                    continue
                event_times = [
                    parsed
                    for key in ("created_at", "started_at", "occurred_at")
                    if (parsed := _parse_timestamp(item.get(key))) is not None
                ]
                if event_times and min(event_times) >= release_at:
                    later_live_events.append(
                        str(
                            item.get("checkpoint_id")
                            or item.get("agent_id")
                            or item.get("allocation_id")
                            or item.get("query_id")
                            or item.get("call_id")
                            or item.get("source_event_id")
                            or item.get("record_type")
                        )
                    )
            if later_live_events:
                findings.append(
                    Finding(
                        "LIVE_EVENT_AFTER_SHADOW_RELEASE",
                        "ERROR",
                        f"Live selection, research, promotion, validation, or checkpoint events occur at/after shadow release: {later_live_events}.",
                        manifest_name,
                        node_ids=tuple(later_live_events),
                    )
                )

    _audit_v2_nonrouting_owned_content(
        run_dir, run_record, ledger_records, excluded_roots, findings
    )

    _audit_shadow_fingerprint_leaks(
        run_dir,
        ledger_records,
        manifest_records,
        declarations,
        excluded_roots,
        findings,
    )


def audit_legacy_august(run_dir: Path, strict: bool = False) -> AuditReport:
    """Conservative August initial snapshot; prose mentions never count as dispositions."""
    run_dir = run_dir.resolve()
    findings: list[Finding] = []
    raw_path = run_dir / "02a_adversarial_raw_pool.md"
    raw_ids = _extract_raw_ids(raw_path, findings) if raw_path.is_file() else []
    raw_set = set(raw_ids)
    if len(raw_ids) != 55:
        findings.append(
            Finding(
                "LEGACY_RAW_COUNT_MISMATCH",
                "ERROR",
                f"Expected 55 initial August raw IDs; found {len(raw_ids)}.",
                raw_path.name,
            )
        )
    if "R08" not in raw_set:
        findings.append(
            Finding(
                "LEGACY_R08_MISSING",
                "ERROR",
                "The required R08 audit case is absent.",
                raw_path.name,
                node_ids=("R08",),
            )
        )
    funnel_path = run_dir / "02_candidate_funnel.md"
    funnel_lines = (
        funnel_path.read_text(encoding="utf-8-sig").splitlines()
        if funnel_path.is_file()
        else []
    )
    explicit_set: set[str] = set()
    raw_code_column: int | None = None
    disposition_column: int | None = None
    for line in funnel_lines:
        if not line.lstrip().startswith("|"):
            raw_code_column = None
            disposition_column = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        normalized = [re.sub(r"\s+", " ", cell.casefold()) for cell in cells]
        if "raw codes" in normalized:
            raw_code_column = normalized.index("raw codes")
            disposition_columns = [
                index
                for index, heading in enumerate(normalized)
                if heading in {"disposition", "status"}
            ]
            disposition_column = (
                disposition_columns[0] if len(disposition_columns) == 1 else None
            )
            continue
        if (
            raw_code_column is None
            or disposition_column is None
            or raw_code_column >= len(cells)
            or disposition_column >= len(cells)
        ):
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        disposition = re.sub(
            r"\s+", " ", cells[disposition_column].casefold()
        ).strip()
        if disposition not in ALLOWED_DISPOSITIONS:
            continue
        for token in re.findall(r"\b[A-Z][A-Z0-9_-]*\d+\b", cells[raw_code_column]):
            if token in raw_set:
                explicit_set.add(token)
    explicit = sorted(explicit_set)
    missing = sorted(raw_set - set(explicit))
    if missing:
        findings.append(
            Finding(
                "LEGACY_ANCESTRY_UNKNOWN",
                "UNKNOWN",
                f"Initial funnel has no explicit disposition for {len(missing)}/{len(raw_ids)} raw IDs.",
                funnel_path.name,
                node_ids=tuple(missing),
            )
        )
    if "R08" in missing:
        findings.append(
            Finding(
                "LEGACY_R08_DISPOSITION_UNKNOWN",
                "UNKNOWN",
                "R08 has no explicit initial-funnel disposition; no semantic lineage was guessed.",
                funnel_path.name,
                node_ids=("R08",),
            )
        )
    findings.append(
        Finding(
            "LEGACY_EVIDENCE_TIMING_UNKNOWN",
            "UNKNOWN",
            "The legacy artifacts do not link decision-critical evidence IDs and freeze timestamps.",
            "03_research_and_sources.md",
        )
    )
    findings.sort(key=_finding_sort_key)
    return AuditReport(
        run_id=run_dir.name,
        adapter="august-initial-snapshot",
        status=_status(findings, strict),
        findings=findings,
        counts={
            "raw": len(raw_ids),
            "explicit_initial_dispositions": len(explicit),
            "unknown_initial_dispositions": len(missing),
        },
        resources={},
    )


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def _fixture_fixed_contract_paths(root: Path) -> dict[str, str]:
    fixed_root = root.parent / "fixed_contracts"
    return {
        "founder-profile": str((fixed_root / "PERSONALITY_SITUATION.md").resolve()),
        "success-safety-contract": str((fixed_root / "COMMUNICATION_AND_GENERAL_RULES.md").resolve()),
        "goal": str((fixed_root / "prompts/NEW_IDEA_GOAL.md").resolve()),
        "validator": str((fixed_root / "Personalities/ZeroToOne.txt").resolve()),
        "orchestration-prompt": str((fixed_root / "prompts/NEW_IDEA_AGENT_PROMPT.md").resolve()),
        "generator-skill": str((fixed_root / "skills/generate-zero-to-one-candidates/SKILL.md").resolve()),
        "evaluator-skill": str((fixed_root / "skills/evaluate-zero-to-one/SKILL.md").resolve()),
        "pivot-skill": str((fixed_root / "skills/pivot-zero-to-one/SKILL.md").resolve()),
    }


def _build_protected_contract_fixture(
    root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    relative_files = {
        "PERSONALITY_SITUATION.md": "Fixed founder profile.\n",
        "COMMUNICATION_AND_GENERAL_RULES.md": "Fixed success and safety contract.\n",
        "prompts/NEW_IDEA_GOAL.md": "Fixed goal.\n",
        "Personalities/ZeroToOne.txt": "Fixed validator framework.\n",
        "prompts/NEW_IDEA_AGENT_PROMPT.md": (
            "# Discovery\n\n## Validation Gates\nFixed validation block.\n\n"
            "## Workflow\nFixed downstream route.\n"
        ),
        "skills/generate-zero-to-one-candidates/SKILL.md": "Fixed generator protocol.\n",
        "skills/evaluate-zero-to-one/SKILL.md": "Fixed evaluator protocol.\n",
        "skills/pivot-zero-to-one/SKILL.md": "Fixed pivot protocol.\n",
    }
    fixed_root = root.parent / "fixed_contracts"
    protected_files: list[dict[str, Any]] = []
    captured_at = "2026-08-21T09:59:00+02:00"
    for relative, content in relative_files.items():
        path = fixed_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        digest = _sha256(path)
        protected_files.append(
            {
                "path": str(path.resolve()),
                "pre_run_sha256": digest,
                "sha256": digest,
                "captured_at": captured_at,
            }
        )
    prompt = fixed_root / "prompts/NEW_IDEA_AGENT_PROMPT.md"
    block_hash = _marker_block_sha256(prompt, "## Validation Gates", "## Workflow")
    protected_blocks = [
        {
            "path": str(prompt.resolve()),
            "start_marker": "## Validation Gates",
            "end_marker": "## Workflow",
            "pre_run_sha256": block_hash,
            "sha256": block_hash,
            "captured_at": captured_at,
        }
    ]
    return protected_files, protected_blocks


def _fixture_trust_payloads(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Create deterministic externally-trusted payloads for hermetic self-tests."""
    manifest_records = _read_jsonl(root / "00a_context_and_resource_manifest.jsonl", [])
    run_record = next(record for record in manifest_records if record.get("record_type") == "run")
    protected_files: list[dict[str, Any]] = []
    fixture_contract_paths = _fixture_fixed_contract_paths(root)
    for item in run_record.get("protected_files", []):
        contract_id = _required_file_id(item.get("path"), fixture_contract_paths)
        if contract_id is None:
            continue
        path = Path(str(item["path"]))
        if not path.is_absolute():
            path = root / path
        protected_files.append(
            {
                "id": contract_id,
                "path": str(path.resolve()),
                "sha256": item["pre_run_sha256"],
            }
        )
    protected_blocks: list[dict[str, Any]] = []
    for item in run_record.get("protected_blocks", []):
        path = Path(str(item["path"]))
        if not path.is_absolute():
            path = root / path
        protected_blocks.append(
            {
                "id": "validation-gates",
                "path": str(path.resolve()),
                "start_marker": item["start_marker"],
                "end_marker": item["end_marker"],
                "sha256": item["pre_run_sha256"],
            }
        )
    protection_anchor: dict[str, Any] = {
        "schema": PROTECTION_ANCHOR_SCHEMA,
        "contract_profile": CONTRACT_PROFILE,
        "run_id": root.name,
        "run_dir": str(root.resolve()),
        "created_at": min(
            str(item["captured_at"])
            for item in run_record.get("protected_files", [])
        ),
        "block_semantics": "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1",
        "files": sorted(protected_files, key=lambda item: item["id"]),
        "blocks": sorted(protected_blocks, key=lambda item: item["id"]),
    }
    protection_digest = _json_payload_sha256(protection_anchor)

    ledger = _read_jsonl(root / "02b_raw_to_direction_ledger.jsonl", [])
    finalists: list[dict[str, Any]] = []
    frozen_times: list[datetime] = []
    for record in ledger:
        if record.get("record_type") != "finalist":
            continue
        _path, relative = _canonical_run_path(root, record.get("artifact_path"))
        finalists.append(
            {
                "finalist_id": record["finalist_id"],
                "arm": record["arm"],
                "artifact_path": relative,
                "frozen_at": record["frozen_at"],
                "sha256": record["sha256"],
            }
        )
        frozen = _parse_timestamp(record.get("frozen_at"))
        if frozen is not None:
            frozen_times.append(frozen)
    sealed_at = max(frozen_times) + timedelta(seconds=1)
    freeze_seal: dict[str, Any] = {
        "schema": FREEZE_SEAL_SCHEMA,
        "run_id": root.name,
        "run_dir": str(root.resolve()),
        "protection_anchor_sha256": protection_digest,
        "mode": run_record.get("mode"),
        "matched_pilot": run_record.get("matched_pilot") is True,
        "model": run_record.get("model"),
        "reasoning_effort": run_record.get("reasoning_effort"),
        "sealed_at": sealed_at.isoformat(),
        "finalists": sorted(finalists, key=lambda item: item["finalist_id"]),
    }
    return protection_anchor, freeze_seal


def _capture_fixture_trust(root: Path) -> None:
    protection_anchor, freeze_seal = _fixture_trust_payloads(root)
    (root / ".fixture_protection_anchor.json").write_bytes(_json_bytes(protection_anchor))
    (root / ".fixture_freeze_seal.json").write_bytes(_json_bytes(freeze_seal))


def _build_valid_fixture(root: Path) -> None:
    (root / "00_run_manifest.md").write_text("# Test run manifest\n", encoding="utf-8")
    raw_lines = ["# Raw pool", ""]
    for index in range(1, 41):
        raw_lines.extend([f"### RAW-{index:03d} — Concept {index}", ""])
    (root / "02a_raw_pool.md").write_text("\n".join(raw_lines), encoding="utf-8")
    context_dir = root / "context"
    context_dir.mkdir()
    packet = context_dir / "generator.md"
    packet.write_text("Neutral founder and safety packet.\n", encoding="utf-8")
    context_hash = _sha256(packet)
    protected_files, protected_blocks = _build_protected_contract_fixture(root)
    manifest = [
        {
            "record_type": "run",
            "mode": "audited_funnel",
            "status": "complete",
            "matched_pilot": False,
            "shadow_only": False,
            "validation_eligible": True,
            "file_read_log_complete": True,
            "tool_event_log_complete": True,
            "started_at": "2026-08-21T10:00:00+02:00",
            "ended_at": "2026-08-21T10:08:00+02:00",
            "model": "test-model",
            "reasoning_effort": "test",
            "budgets": {
                "unique_queries": 10,
                "uncached_input_tokens": 100,
                "output_tokens": 100,
                "elapsed_minutes": 10,
                "max_concurrency": 3,
            },
            "resource_totals": {
                "unique_queries": 1,
                "uncached_input_tokens": 10,
                "output_tokens": 5,
                "elapsed_minutes": 8.0,
            },
            "shadow_can_route_to_validation": False,
            "protected_files": protected_files,
            "protected_blocks": protected_blocks,
        },
        {
            "record_type": "agent",
            "agent_id": "generator-1",
            "arm": "live",
            "stage": "generation",
            "role": "taboo_space_explorer",
            "assigned_ids": ["search-cell-1"],
            "output_ids": [f"RAW-{index:03d}" for index in range(1, 9)],
            "fork_turns": "none",
            "context_classes": ["founder_constraints", "safety_legal", "neutral_evidence"],
            "context_files": [{"path": "context/generator.md", "sha256": context_hash}],
            "allowlisted_files": ["context/generator.md"],
            "files_read": ["context/generator.md"],
            "model": "test-model",
            "reasoning_effort": "test",
            "started_at": "2026-08-21T10:00:00+02:00",
            "ended_at": "2026-08-21T10:01:00+02:00",
            "resources": {
                "uncached_input_tokens": 10,
                "output_tokens": 5,
                "elapsed_minutes": 1.0,
            },
        },
        {
            "record_type": "query",
            "agent_id": "generator-1",
            "arm": "live",
            "stage": "generation",
            "query_id": "Q-0001",
            "query": "customer workaround evidence",
            "entity_ids": ["RAW-001", "RAW-002", "RAW-003"],
            "occurred_at": "2026-08-21T10:00:20+02:00",
        },
        {
            "record_type": "source_open",
            "source_event_id": "SRC-0001",
            "query_id": "Q-0001",
            "agent_id": "generator-1",
            "arm": "live",
            "stage": "generation",
            "url": "https://example.test/source",
            "entity_ids": ["RAW-001", "RAW-002", "RAW-003"],
            "evidence_ids": ["EV-0001", "EV-0002", "EV-0003"],
            "occurred_at": "2026-08-21T10:00:30+02:00",
        },
        {
            "record_type": "tool_event",
            "call_id": "CALL-0001",
            "agent_id": "generator-1",
            "arm": "live",
            "stage": "generation",
            "tool": "web_search",
            "event_type": "tool_call",
            "query_id": "Q-0001",
            "occurred_at": "2026-08-21T10:00:20+02:00",
        },
    ]
    for index, role in enumerate(
        (
            "incentive_hacker",
            "incumbent_attacker",
            "rule_structure_analyst",
            "first_principles_extremist",
        ),
        2,
    ):
        manifest.append(
            {
                "record_type": "agent",
                "agent_id": f"generator-{index}",
                "arm": "live",
                "stage": "generation",
                "role": role,
                "assigned_ids": [f"search-cell-{index}"],
                "output_ids": [
                    f"RAW-{raw_index:03d}"
                    for raw_index in range((index - 1) * 8 + 1, index * 8 + 1)
                ],
                "fork_turns": "none",
                "context_classes": ["founder_constraints", "safety_legal", "neutral_evidence"],
                "context_files": [{"path": "context/generator.md", "sha256": context_hash}],
                "allowlisted_files": ["context/generator.md"],
                "files_read": ["context/generator.md"],
                "model": "test-model",
                "reasoning_effort": "test",
                "started_at": f"2026-08-21T10:0{index - 1}:00+02:00",
                "ended_at": f"2026-08-21T10:0{index}:00+02:00",
                "resources": {
                    "uncached_input_tokens": 0,
                    "output_tokens": 0,
                    "elapsed_minutes": 1.0,
                },
            }
        )
    _write_jsonl(root / "00a_context_and_resource_manifest.jsonl", manifest)
    ledger: list[dict[str, Any]] = []
    for index in range(1, 41):
        ledger.append(
            {
                "record_type": "mapping",
                "raw_id": f"RAW-{index:03d}",
                "direction_id": f"DIR-{((index - 1) % 10) + 1:03d}",
                "cluster_id": f"CL-{((index - 1) % 10) + 1:03d}",
                "disposition": "retained" if index <= 10 else "merged",
                "reason": "Hermetic field-level mapping rationale.",
            }
        )
    for index in range(1, 4):
        evidence_id = f"EV-{index:04d}"
        dossier = root / f"finalist_candidate_{index:02d}.md"
        dossier.write_text(f"# Frozen candidate {index}\n\nDistinct content {index}.\n", encoding="utf-8")
        ledger.append(
            {
                "record_type": "evidence",
                "evidence_id": evidence_id,
                "direction_id": f"DIR-{index:03d}",
                "recorded_at": "2026-08-21T10:06:00+02:00",
                "decision_critical": True,
                "status": "unknown",
                "source_event_ids": ["SRC-0001"],
                "entity_ids": [f"RAW-{index:03d}"],
                "proposition": f"Decision-critical proposition {index}.",
                "source": "https://example.test/source",
                "cheapest_resolving_test": "Verify with one bounded buyer interview.",
            }
        )
        ledger.append(
            {
                "record_type": "finalist",
                "finalist_id": f"FIN-{index:02d}",
                "direction_id": f"DIR-{index:03d}",
                "raw_ids": [f"RAW-{index:03d}"],
                "evidence_ids": [evidence_id],
                "frozen_at": "2026-08-21T10:07:00+02:00",
                "arm": "live",
                "validation_eligible": True,
                "artifact_path": dossier.name,
                "sha256": _sha256(dossier),
            }
        )
    _write_jsonl(root / "02b_raw_to_direction_ledger.jsonl", ledger)
    _capture_fixture_trust(root)


def _build_live_arm_reference_fixture(root: Path) -> tuple[Path, str]:
    """Create a sealed matched live cohort beside a hermetic shadow fixture."""
    live_root = root.parent / "live_arm"
    live_root.mkdir(parents=True, exist_ok=True)
    finalists: list[dict[str, Any]] = []
    for index in range(1, 7):
        artifact = live_root / f"finalist_{index:02d}.md"
        artifact.write_text(
            f"# Live finalist LIVE-FIN-{index:02d}\n\nFrozen live baseline {index}.\n",
            encoding="utf-8",
        )
        finalists.append(
            {
                "finalist_id": f"LIVE-FIN-{index:02d}",
                "arm": "live",
                "artifact_path": artifact.name,
                "frozen_at": "2026-08-21T11:55:00+02:00",
                "sha256": _sha256(artifact),
            }
        )
    payload = {
        "schema": FREEZE_SEAL_SCHEMA,
        "run_id": live_root.name,
        "run_dir": str(live_root.resolve()),
        "protection_anchor_sha256": "a" * 64,
        "mode": "audited_funnel",
        "matched_pilot": True,
        "model": "test-model",
        "reasoning_effort": "test",
        "sealed_at": "2026-08-21T11:56:00+02:00",
        "finalists": finalists,
    }
    seal_path = root.parent / ".fixture_live_arm_freeze_seal.json"
    seal_path.write_bytes(_json_bytes(payload))
    return live_root, _sha256(seal_path)


def _build_shadow_fixture(root: Path) -> None:
    (root / "00_run_manifest.md").write_text("# Shadow test manifest\n", encoding="utf-8")
    direct_ids = [f"D-{index:03d}" for index in range(1, 37)]
    inversion_ids = [f"I-{index:03d}" for index in range(1, 7)]
    recombination_ids = [f"X-{index:03d}" for index in range(1, 7)]
    raw_ids = direct_ids + inversion_ids + recombination_ids
    islands = list(SHADOW_ISLAND_ROLES)
    problem_ids = [
        f"P-{island}-{index:02d}"
        for island in islands
        for index in range(1, 7)
    ]
    (root / "02a_raw_pool.md").write_text(
        "# Raw pool\n\n"
        + "\n\n".join(f"### {raw_id} — Concept {raw_id}" for raw_id in raw_ids)
        + "\n",
        encoding="utf-8",
    )
    context_dir = root / "context"
    context_dir.mkdir()
    packet = context_dir / "neutral.md"
    packet.write_text("Neutral founder constraints, safety, and assigned evidence only.\n", encoding="utf-8")
    packet_hash = _sha256(packet)
    protected_files, protected_blocks = _build_protected_contract_fixture(root)
    live_root, live_seal_digest = _build_live_arm_reference_fixture(root)

    provisional_payload = {
        "main_provisional_ids": direct_ids[:6],
        "ordered_reserve": raw_ids[6:],
        "creator_agent_id": "provisional-1",
        "frozen_at": "2026-08-21T13:00:00+02:00",
        "seed": "fixture-seed",
    }
    provisional = root / "02c_main_provisional_order.json"
    provisional.write_text(json.dumps(provisional_payload, sort_keys=True) + "\n", encoding="utf-8")

    closure_payload = {
        "candidate_ids": direct_ids[:6],
        "creator_agent_id": "finalist-selector-1",
        "selected_at": "2026-08-21T13:43:00+02:00",
        "seed": "fixture-seed",
    }
    closure_cohort = root / "02d_fact_closure_candidates.json"
    closure_cohort.write_text(
        json.dumps(closure_payload, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest: list[dict[str, Any]] = [
        {
            "record_type": "run",
            "mode": "archipelago_lite_shadow",
            "status": "complete",
            "matched_pilot": True,
            "file_read_log_complete": True,
            "tool_event_log_complete": True,
            "validation_eligible": False,
            "shadow_only": True,
            "shadow_can_route_to_validation": False,
            "started_at": "2026-08-21T12:00:00+02:00",
            "ended_at": "2026-08-21T14:30:00+02:00",
            "live_finalists_frozen_at": "2026-08-21T11:55:00+02:00",
            "live_arm_run_dir": str(live_root.resolve()),
            "live_arm_freeze_seal_sha256": live_seal_digest,
            "main_provisional_frozen_at": "2026-08-21T13:00:00+02:00",
            "main_provisional_file": provisional.name,
            "main_provisional_sha256": _sha256(provisional),
            "fact_closure_selected_at": "2026-08-21T13:43:00+02:00",
            "fact_closure_candidates_file": closure_cohort.name,
            "fact_closure_candidates_sha256": _sha256(closure_cohort),
            "model": "test-model",
            "reasoning_effort": "test",
            "budgets": {
                "unique_queries": 300,
                "uncached_input_tokens": 10_000_000,
                "output_tokens": 700_000,
                "elapsed_minutes": 180,
                "max_concurrency": 3,
            },
            "resource_totals": {
                "unique_queries": 12,
                "uncached_input_tokens": 0,
                "output_tokens": 0,
                "elapsed_minutes": 150.0,
            },
            "protected_files": protected_files,
            "protected_blocks": protected_blocks,
        }
    ]

    agent_specs: list[tuple[str, str, str, str, str]] = []
    for index, island in enumerate(islands, 1):
        agent_specs.append((f"scout-{index}", "problem_discovery", SHADOW_ISLAND_ROLES[island], f"12:{index:02d}:00", f"12:{index:02d}:30"))
    for index in range(1, 4):
        agent_specs.append((f"builder-{index}", "direct_concept", f"direct_builder_{index}", f"12:{10 + index:02d}:00", f"12:{10 + index:02d}:30"))
    agent_specs.extend(
        [
            ("inverter-1", "inversion", "assumption_inverter", "12:20:00", "12:20:30"),
            ("inverter-2", "inversion", "assumption_inverter", "12:21:00", "12:21:30"),
            ("recombiner-1", "recombination", "cross_domain_recombiner", "12:22:00", "12:22:30"),
            ("recombiner-2", "recombination", "cross_domain_recombiner", "12:23:00", "12:23:30"),
            ("history-1", "history_compressor", "neutral_history_compressor", "12:24:00", "12:24:30"),
            ("cartographer-1", "cartography", "semantic_cartographer", "12:25:00", "12:25:30"),
            ("cluster-auditor-1", "cluster_audit", "anti_overmerge_auditor", "12:26:00", "12:26:30"),
            ("level1-1", "level1", "canonicalizer", "12:27:00", "12:27:30"),
            ("provisional-1", "provisional_selector", "isolated_provisional_selector", "12:58:00", "12:59:00"),
            ("ranker-1", "selector", "commercial_ranker", "13:01:00", "13:01:30"),
            ("ranker-2", "selector", "economics_ranker", "13:02:00", "13:02:30"),
            ("challenger-1", "tail_challenger", "tail_recall_challenger", "13:03:00", "13:03:30"),
            ("level2-1", "level2", "level2_researcher", "13:10:00", "13:40:00"),
            ("finalist-selector-1", "finalist_selector", "isolated_finalist_selector", "13:41:00", "13:42:00"),
            ("closure-1", "fact_closure", "fact_closure_researcher", "13:45:00", "14:00:00"),
        ]
    )
    for agent_id, stage, role, start_clock, end_clock in agent_specs:
        context_classes = ["history"] if stage == "history_compressor" else ["founder_constraints", "safety_legal", "neutral_evidence"]
        started_at = f"2026-08-21T{start_clock}+02:00"
        ended_at = f"2026-08-21T{end_clock}+02:00"
        parsed_start = _parse_timestamp(started_at)
        parsed_end = _parse_timestamp(ended_at)
        elapsed_minutes = (
            (parsed_end - parsed_start).total_seconds() / 60.0
            if parsed_start is not None and parsed_end is not None
            else 0.0
        )
        agent_record: dict[str, Any] = {
                "record_type": "agent",
                "agent_id": agent_id,
                "arm": "shadow",
                "stage": stage,
                "role": role,
                "fork_turns": "none",
                "context_classes": context_classes,
                "context_files": [{"path": "context/neutral.md", "sha256": packet_hash}],
                "allowlisted_files": ["context/neutral.md"],
                "files_read": ["context/neutral.md"],
                "model": "test-model",
                "reasoning_effort": "test",
                "started_at": started_at,
                "ended_at": ended_at,
                "resources": {"uncached_input_tokens": 0, "output_tokens": 0, "elapsed_minutes": elapsed_minutes},
            }
        if stage == "problem_discovery":
            scout_index = int(agent_id.rsplit("-", 1)[-1]) - 1
            island = islands[scout_index]
            scoped_problem_ids = problem_ids[scout_index * 6 : (scout_index + 1) * 6]
            agent_record.update(
                {
                    "island_id": island,
                    "assigned_ids": scoped_problem_ids,
                    "output_ids": scoped_problem_ids,
                }
            )
        elif stage == "direct_concept":
            builder_index = int(agent_id.rsplit("-", 1)[-1]) - 1
            agent_record.update(
                {
                    "assigned_ids": problem_ids[builder_index * 12 : (builder_index + 1) * 12],
                    "output_ids": direct_ids[builder_index * 12 : (builder_index + 1) * 12],
                }
            )
        elif stage == "inversion":
            transformer_index = int(agent_id.rsplit("-", 1)[-1]) - 1
            start = transformer_index * 3
            agent_record.update(
                {
                    "assigned_ids": direct_ids[start : start + 3],
                    "output_ids": inversion_ids[start : start + 3],
                }
            )
        elif stage == "recombination":
            transformer_index = int(agent_id.rsplit("-", 1)[-1]) - 1
            start = transformer_index * 3
            assigned = direct_ids[start : start + 3] + direct_ids[start + 6 : start + 9]
            agent_record.update(
                {
                    "assigned_ids": assigned,
                    "output_ids": recombination_ids[start : start + 3],
                }
            )
        manifest.append(agent_record)

    for index in range(1, 7):
        manifest.append(
            {
                "record_type": "allocation",
                "allocation_id": f"ALLOC-DISC-{index}",
                "agent_id": f"scout-{index}",
                "stage": "problem_discovery",
                "entity_id": f"scout-{index}",
                "query_cap": 18,
                "used_unique_queries": 1,
                "unused_queries": 17,
                "unused_reason": "One hermetic discovery source covers the assigned six cards.",
            }
        )
        problem_ids_for_scout = problem_ids[(index - 1) * 6 : index * 6]
        evidence_ids_for_scout = [
            f"EV-P-{problem_index:03d}"
            for problem_index in range((index - 1) * 6 + 1, index * 6 + 1)
        ]
        manifest.extend(
            [
                {
                    "record_type": "query",
                    "query_id": f"Q-DISC-{index}",
                    "allocation_id": f"ALLOC-DISC-{index}",
                    "agent_id": f"scout-{index}",
                    "arm": "shadow",
                    "stage": "problem_discovery",
                    "query": f"discovery evidence island {index}",
                    "entity_ids": problem_ids_for_scout,
                    "occurred_at": f"2026-08-21T12:0{index}:05+02:00",
                },
                {
                    "record_type": "source_open",
                    "source_event_id": f"SRC-DISC-{index}",
                    "query_id": f"Q-DISC-{index}",
                    "agent_id": f"scout-{index}",
                    "arm": "shadow",
                    "stage": "problem_discovery",
                    "url": f"https://example.test/discovery-{index}",
                    "entity_ids": problem_ids_for_scout,
                    "evidence_ids": evidence_ids_for_scout,
                    "occurred_at": f"2026-08-21T12:0{index}:10+02:00",
                },
                {
                    "record_type": "tool_event",
                    "call_id": f"CALL-DISC-{index}",
                    "agent_id": f"scout-{index}",
                    "arm": "shadow",
                    "stage": "problem_discovery",
                    "tool": "web_search",
                    "event_type": "tool_call",
                    "query_id": f"Q-DISC-{index}",
                    "occurred_at": f"2026-08-21T12:0{index}:05+02:00",
                },
            ]
        )
    level2_dir = root / "shadow_level2"
    level2_dir.mkdir()
    level2_artifacts: dict[str, Path] = {}
    for index, concept_id in enumerate(direct_ids[:12], 1):
        dossier = level2_dir / f"level2_{concept_id.casefold()}.md"
        dossier.write_text(
            f"# Level-2 {concept_id}\n\n"
            "## Problem And Payer Evidence\n"
            f"Evidence-backed problem dossier {index}.\n\n"
            "## Proposed Transaction\n"
            f"Transaction structure for {concept_id}.\n\n"
            "## Acquisition Route\n"
            "Bounded first-customer route.\n\n"
            "## Decision-Critical Unknowns\n"
            "Unknowns remain explicitly testable.\n\n"
            "## Evidence And Sources\n"
            f"Hermetic source record for {concept_id}.\n",
            encoding="utf-8",
        )
        level2_artifacts[concept_id] = dossier
        manifest.append(
            {
                "record_type": "allocation",
                "allocation_id": f"ALLOC-L2-{index}",
                "agent_id": "level2-1",
                "stage": "level2",
                "entity_id": concept_id,
                "query_cap": 12,
                "used_unique_queries": 0,
                "unused_queries": 12,
                "unused_reason": "Hermetic fixture does not browse.",
            }
        )
    for index, concept_id in enumerate(direct_ids[:6], 1):
        allocation_id = f"ALLOC-FC-{index}"
        manifest.append(
            {
                "record_type": "allocation",
                "allocation_id": allocation_id,
                "agent_id": "closure-1",
                "stage": "fact_closure",
                "entity_id": concept_id,
                "query_cap": 8,
                "used_unique_queries": 1,
                "unused_queries": 7,
                "unused_reason": "One hermetic source is sufficient for the fixture.",
            }
        )
        manifest.append(
            {
                "record_type": "query",
                "query_id": f"Q-FC-{index}",
                "allocation_id": allocation_id,
                "agent_id": "closure-1",
                "arm": "shadow",
                "stage": "fact_closure",
                "query": f"fact closure evidence {index}",
                "entity_ids": [concept_id],
                "occurred_at": f"2026-08-21T13:5{index}:00+02:00",
            }
        )
        manifest.append(
            {
                "record_type": "source_open",
                "source_event_id": f"SRC-FC-{index}",
                "query_id": f"Q-FC-{index}",
                "agent_id": "closure-1",
                "arm": "shadow",
                "stage": "fact_closure",
                "url": f"https://example.test/fact-{index}",
                "entity_ids": [concept_id],
                "evidence_ids": [f"EV-FC-{index}"],
                "occurred_at": f"2026-08-21T13:5{index}:10+02:00",
            }
        )
        manifest.append(
            {
                "record_type": "tool_event",
                "call_id": f"CALL-FC-{index}",
                "agent_id": "closure-1",
                "arm": "shadow",
                "stage": "fact_closure",
                "tool": "web_search",
                "event_type": "tool_call",
                "query_id": f"Q-FC-{index}",
                "occurred_at": f"2026-08-21T13:5{index}:00+02:00",
            }
        )
    _write_jsonl(root / "00a_context_and_resource_manifest.jsonl", manifest)

    ledger: list[dict[str, Any]] = []
    for index, problem_id in enumerate(problem_ids, 1):
        island_index = (index - 1) // 6
        ledger.append(
            {
                "record_type": "problem",
                "problem_id": problem_id,
                "source_island": islands[island_index],
                "creator_agent_id": f"scout-{island_index + 1}",
                "evidence_ids": [f"EV-P-{index:03d}"],
            }
        )
    for index, raw_id in enumerate(direct_ids, 1):
        ledger.append(
            {
                "record_type": "mapping",
                "raw_id": raw_id,
                "concept_type": "direct",
                "parent_ids": [problem_ids[index - 1]],
                "creator_agent_id": f"builder-{((index - 1) // 12) + 1}",
                "direction_id": f"DIR-{((index - 1) % 12) + 1:03d}",
                "cluster_id": f"CL-{index:03d}",
                "disposition": "retained" if index <= 12 else "merged",
                "reason": "Hermetic direct-concept mapping rationale.",
            }
        )
    for index, raw_id in enumerate(inversion_ids, 1):
        ledger.append(
            {
                "record_type": "mapping",
                "raw_id": raw_id,
                "concept_type": "inversion",
                "parent_ids": [direct_ids[index - 1]],
                "creator_agent_id": f"inverter-{((index - 1) // 3) + 1}",
                "operation": {
                    "dimension": "payer",
                    "assumption": "The original payer must remain the buyer.",
                    "causal_benefit": "A different payer internalizes more of the loss.",
                    "new_risk": "The alternate payer may have a longer procurement cycle.",
                },
                "direction_id": f"DIR-{index:03d}",
                "cluster_id": f"CL-I-{index:03d}",
                "disposition": "merged",
                "reason": "Hermetic assumption-inversion sibling rationale.",
            }
        )
    for index, raw_id in enumerate(recombination_ids, 1):
        ledger.append(
            {
                "record_type": "mapping",
                "raw_id": raw_id,
                "concept_type": "recombination",
                "parent_ids": [direct_ids[index - 1], direct_ids[index + 5]],
                "creator_agent_id": f"recombiner-{((index - 1) // 3) + 1}",
                "operation": {
                    "transferred_mechanism": "Transfer a verified workflow mechanism across evidence islands.",
                    "analogy_break": "Buyer authority and operating cadence differ across the two islands.",
                },
                "direction_id": f"DIR-{index + 6:03d}",
                "cluster_id": f"CL-X-{index:03d}",
                "disposition": "merged",
                "reason": "Hermetic cross-domain recombination rationale.",
            }
        )
    for index, problem_id in enumerate(problem_ids, 1):
        ledger.append(
            {
                "record_type": "evidence",
                "evidence_id": f"EV-P-{index:03d}",
                "direction_id": f"DIR-{((index - 1) % 12) + 1:03d}",
                "source_event_ids": [f"SRC-DISC-{((index - 1) // 6) + 1}"],
                "entity_ids": [problem_id],
                "recorded_at": "2026-08-21T12:07:00+02:00",
                "decision_critical": False,
                "status": "interpreted",
                "proposition": f"Problem evidence proposition {index}.",
                "source": f"https://example.test/discovery-{((index - 1) // 6) + 1}",
                "cheapest_resolving_test": "Check the next primary customer source.",
            }
        )
    categories = ["main_provisional"] * 6 + ["selector_or_challenger"] * 3 + ["rejected", "near_cutoff", "singleton"]
    for index, (concept_id, category) in enumerate(zip(direct_ids[:12], categories), 1):
        level2_artifact = level2_artifacts[concept_id]
        ledger.append(
            {
                "record_type": "level2",
                "concept_id": concept_id,
                "selection_category": category,
                "selected_at": "2026-08-21T13:05:00+02:00",
                "completed_at": "2026-08-21T13:39:00+02:00",
                "development_status": "complete",
                "artifact_path": str(level2_artifact.relative_to(root)),
                "sha256": _sha256(level2_artifact),
            }
        )
    shadow_candidates = root / "shadow_candidates"
    shadow_candidates.mkdir()
    for index, concept_id in enumerate(direct_ids[:6], 1):
        evidence_id = f"EV-FC-{index}"
        ledger.append(
            {
                "record_type": "evidence",
                "evidence_id": evidence_id,
                "direction_id": f"DIR-{index:03d}",
                "source_event_ids": [f"SRC-FC-{index}"],
                "entity_ids": [concept_id],
                "recorded_at": f"2026-08-21T13:5{index}:20+02:00",
                "decision_critical": True,
                "status": "interpreted",
                "proposition": f"Fact-closure proposition {index}.",
                "source": f"https://example.test/fact-{index}",
                "cheapest_resolving_test": "Run the bounded fact-closure test.",
            }
        )
        dossier = shadow_candidates / f"shadow_finalist_candidate_{index:02d}.md"
        dossier.write_text(f"# Shadow candidate {index}\n\nDistinct frozen content {index}.\n", encoding="utf-8")
        ledger.append(
            {
                "record_type": "finalist",
                "finalist_id": f"SFIN-{index:02d}",
                "direction_id": f"DIR-{index:03d}",
                "raw_ids": [concept_id],
                "evidence_ids": [evidence_id],
                "frozen_at": "2026-08-21T14:05:00+02:00",
                "arm": "shadow",
                "shadow_only": True,
                "validation_eligible": False,
                "artifact_path": str(dossier.relative_to(root)),
                "sha256": _sha256(dossier),
            }
        )
    _write_jsonl(root / "02b_raw_to_direction_ledger.jsonl", ledger)
    _capture_fixture_trust(root)


def _convert_shadow_fixture_to_matched_baseline(root: Path) -> None:
    """Convert the hermetic shadow fixture to the five-role audited baseline."""
    shadow_problem_ids = [
        f"P-{island}-{index:02d}"
        for island in SHADOW_ISLAND_ROLES
        for index in range(1, 7)
    ]
    problem_to_direct = {
        problem_id: f"D-{index:03d}"
        for index, problem_id in enumerate(shadow_problem_ids, 1)
    }
    matched_raw_ids = [f"D-{index:03d}" for index in range(1, 37)] + [
        f"I-{index:03d}" for index in range(1, 7)
    ] + [f"X-{index:03d}" for index in range(1, 7)]
    closure_path = root / "02d_fact_closure_candidates.json"
    closure_payload = json.loads(closure_path.read_text(encoding="utf-8"))
    closure_payload["candidate_ids"] = [f"DIR-{index:03d}" for index in range(1, 7)]
    closure_payload["creator_agent_id"] = "root-orchestrator"
    closure_path.write_text(json.dumps(closure_payload, sort_keys=True) + "\n", encoding="utf-8")

    manifest_path = root / "00a_context_and_resource_manifest.jsonl"
    manifest: list[dict[str, Any]] = []
    discovery_caps = [22, 22, 22, 21, 21]
    for record in _read_jsonl(manifest_path, []):
        record.pop("_line", None)
        if record.get("record_type") == "agent" and record.get("agent_id") == "scout-6":
            continue
        if record.get("record_type") == "allocation" and record.get("allocation_id") == "ALLOC-DISC-6":
            continue
        if record.get("record_type") in {"query", "source_open", "tool_event"} and record.get("agent_id") == "scout-6":
            continue
        if record.get("record_type") == "run":
            record["mode"] = "audited_funnel"
            record["fact_closure_candidates_sha256"] = _sha256(closure_path)
            record["resource_totals"]["unique_queries"] = 11
        elif record.get("record_type") == "agent":
            record["arm"] = "matched_baseline"
            agent_id = record.get("agent_id")
            if isinstance(agent_id, str) and agent_id.startswith("scout-"):
                record["stage"] = "generation"
                role_index = int(agent_id.rsplit("-", 1)[-1]) - 1
                record["role"] = (
                    "taboo_space_explorer",
                    "incentive_hacker",
                    "incumbent_attacker",
                    "rule_structure_analyst",
                    "first_principles_extremist",
                )[role_index]
                starts = [0, 10, 20, 30, 39]
                ends = [10, 20, 30, 39, 48]
                record["assigned_ids"] = [f"matched-search-cell-{role_index + 1}"]
                record["output_ids"] = matched_raw_ids[starts[role_index] : ends[role_index]]
                record.pop("island_id", None)
        elif record.get("record_type") in {"query", "source_open", "tool_event"}:
            record["arm"] = "matched_baseline"
            if record.get("stage") == "problem_discovery":
                record["stage"] = "generation"
            entity_ids, entity_ids_valid = _valid_string_list(
                record.get("entity_ids"), allow_empty=True
            )
            if entity_ids_valid:
                record["entity_ids"] = [
                    f"DIR-{int(entity_id.rsplit('-', 1)[-1]):03d}"
                    if entity_id.startswith("D-")
                    else problem_to_direct.get(entity_id, entity_id)
                    for entity_id in entity_ids
                ]
        elif record.get("record_type") == "allocation" and str(record.get("allocation_id", "")).startswith("ALLOC-DISC-"):
            index = int(str(record["allocation_id"]).rsplit("-", 1)[-1]) - 1
            cap = discovery_caps[index]
            record["stage"] = "generation"
            record["query_cap"] = cap
            record["used_unique_queries"] = 1
            record["unused_queries"] = cap - 1
        elif record.get("record_type") == "allocation" and record.get("stage") in {"level2", "fact_closure"}:
            entity_id = record.get("entity_id")
            if isinstance(entity_id, str) and entity_id.startswith("D-"):
                record["entity_id"] = f"DIR-{int(entity_id.rsplit('-', 1)[-1]):03d}"
        manifest.append(record)
    _write_jsonl(manifest_path, manifest)

    ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
    ledger = []
    for record in _read_jsonl(ledger_path, []):
        record.pop("_line", None)
        if record.get("record_type") == "problem":
            continue
        if record.get("record_type") == "evidence" and str(record.get("evidence_id", "")).startswith("EV-P-"):
            evidence_index = int(str(record["evidence_id"]).rsplit("-", 1)[-1])
            if evidence_index > 30:
                continue
        if record.get("record_type") == "evidence":
            entity_ids, entity_ids_valid = _valid_string_list(
                record.get("entity_ids"), allow_empty=True
            )
            if entity_ids_valid:
                record["entity_ids"] = [
                    f"DIR-{int(entity_id.rsplit('-', 1)[-1]):03d}"
                    if entity_id.startswith("D-")
                    else problem_to_direct.get(entity_id, entity_id)
                    for entity_id in entity_ids
                ]
        if record.get("record_type") == "level2":
            concept_id = record.get("concept_id")
            if isinstance(concept_id, str) and concept_id.startswith("D-"):
                matched_concept_id = f"DIR-{int(concept_id.rsplit('-', 1)[-1]):03d}"
                record["concept_id"] = matched_concept_id
                level2_path = root / str(record.get("artifact_path"))
                if level2_path.is_file():
                    level2_text = level2_path.read_text(encoding="utf-8")
                    level2_path.write_text(
                        level2_text.replace(concept_id, matched_concept_id),
                        encoding="utf-8",
                    )
                    record["sha256"] = _sha256(level2_path)
        if record.get("record_type") == "finalist":
            record["arm"] = "matched_baseline"
            old_path = root / str(record.get("artifact_path"))
            new_path = old_path.with_name(
                old_path.name.replace("shadow_finalist_", "baseline_shadow_finalist_", 1)
            )
            old_path.rename(new_path)
            record["artifact_path"] = str(new_path.relative_to(root))
            record["sha256"] = _sha256(new_path)
        ledger.append(record)
    _write_jsonl(ledger_path, ledger)
    _capture_fixture_trust(root)


class SelfTest(unittest.TestCase):
    def _audit(self, root: Path, *, strict: bool = False) -> AuditReport:
        protection_path = root / ".fixture_protection_anchor.json"
        seal_path = root / ".fixture_freeze_seal.json"
        protection_anchor = json.loads(protection_path.read_text(encoding="utf-8"))
        freeze_seal = json.loads(seal_path.read_text(encoding="utf-8"))
        live_seal_path = root.parent / ".fixture_live_arm_freeze_seal.json"
        live_seal = (
            json.loads(live_seal_path.read_text(encoding="utf-8"))
            if live_seal_path.is_file()
            else None
        )
        return audit_run(
            root,
            strict,
            protection_anchor=protection_anchor,
            protection_anchor_sha256=_sha256(protection_path),
            freeze_seal=freeze_seal,
            freeze_seal_sha256=_sha256(seal_path),
            live_arm_freeze_seal=live_seal,
            live_arm_freeze_seal_sha256=(
                _sha256(live_seal_path) if live_seal is not None else None
            ),
            _fixed_contract_paths=_fixture_fixed_contract_paths(root),
        )

    def _fixed_file(self, root: Path, suffix: str) -> Path:
        records = _read_jsonl(root / "00a_context_and_resource_manifest.jsonl", [])
        run_record = next(record for record in records if record.get("record_type") == "run")
        item = next(
            item
            for item in run_record["protected_files"]
            if str(item.get("path", "")).casefold().endswith(suffix.casefold())
        )
        return Path(item["path"])

    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name).resolve() / "run"
        root.mkdir()
        _build_valid_fixture(root)
        return temporary, root

    def _shadow_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name).resolve() / "run"
        root.mkdir()
        _build_shadow_fixture(root)
        return temporary, root

    def _v2_state_chain_probe(
        self,
        mode: str,
        agent_specs: list[tuple[str, str, int, int]],
        states: tuple[str, ...],
    ) -> list[Finding]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve() / "run"
        root.mkdir()
        (root / "00_run_manifest.md").write_text("fixture\n", encoding="utf-8")
        (root / "00b_development_contract.json").write_text(
            "{}\n", encoding="utf-8"
        )
        artifacts = [
            {"path": path.name, "sha256": _sha256(path)}
            for path in (
                root / "00_run_manifest.md",
                root / "00b_development_contract.json",
            )
        ]
        run_started = datetime.fromisoformat("2026-08-23T00:00:00+00:00")
        agents = [
            {
                "record_type": "agent",
                "agent_id": agent_id,
                "stage": stage,
                "started_at": (run_started + timedelta(seconds=start)).isoformat(),
                "ended_at": (run_started + timedelta(seconds=end)).isoformat(),
            }
            for agent_id, stage, start, end in agent_specs
        ]
        checkpoints: list[dict[str, Any]] = []
        predecessor_id: str | None = None
        for index, state in enumerate(states):
            occurred_at = run_started + timedelta(minutes=index)
            checkpoint_id = f"checkpoint-{index}"
            checkpoints.append(
                {
                    "record_type": "checkpoint",
                    "checkpoint_id": checkpoint_id,
                    "state": state,
                    "predecessor_id": predecessor_id,
                    "occurred_at": occurred_at.isoformat(),
                    "completed_agent_ids": [
                        str(agent["agent_id"])
                        for agent in agents
                        if _parse_timestamp(agent.get("ended_at")) < occurred_at
                    ],
                    "file_read_log_complete": True,
                    "tool_event_log_complete": True,
                    "resource_totals": {
                        "unique_queries": 0,
                        "uncached_input_tokens": 0,
                        "output_tokens": 0,
                        "elapsed_minutes": index,
                    },
                    "artifacts": artifacts,
                }
            )
            predecessor_id = checkpoint_id
        run_record = {
            "record_type": "run",
            "mode": mode,
            "started_at": run_started.isoformat(),
            "lifecycle_state": states[-1],
        }
        findings: list[Finding] = []
        _audit_v2_state_chain(
            run_record,
            [*agents, *checkpoints],
            root,
            set(),
            findings,
            None,
            allow_prefix=True,
        )
        return findings

    def test_valid(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        report = self._audit(root)
        self.assertEqual(report.status, "PASS", report.to_json())

    def test_valid_shadow_protocol(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        report = self._audit(root)
        self.assertEqual(report.status, "PASS", report.to_json())

    def test_shadow_missing_scout_fails(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = [
            record
            for record in _read_jsonl(manifest_path, [])
            if not (record.get("record_type") == "agent" and record.get("agent_id") == "scout-6")
        ]
        for record in records:
            record.pop("_line", None)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_STAGE_ROLE_COUNT_INVALID", {item.code for item in report.findings})

    def test_shadow_level2_category_quota_fails(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "level2" and record.get("selection_category") == "near_cutoff":
                record["selection_category"] = "main_provisional"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_LEVEL2_CATEGORY_COUNTS", {item.code for item in report.findings})

    def test_shadow_allocation_gap_fails(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = [
            record
            for record in _read_jsonl(manifest_path, [])
            if not (record.get("record_type") == "allocation" and record.get("allocation_id") == "ALLOC-L2-12")
        ]
        for record in records:
            record.pop("_line", None)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("ALLOCATION_PHASE_COUNTS_INVALID", {item.code for item in report.findings})

    def test_shadow_provisional_payload_is_verified(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        provisional = root / "02c_main_provisional_order.json"
        payload = json.loads(provisional.read_text(encoding="utf-8"))
        payload["ordered_reserve"] = payload["ordered_reserve"][:-1]
        provisional.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["main_provisional_sha256"] = _sha256(provisional)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_PROVISIONAL_ORDER_INVALID", {item.code for item in report.findings})

    def test_shadow_provisional_creator_is_isolated(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        provisional = root / "02c_main_provisional_order.json"
        payload = json.loads(provisional.read_text(encoding="utf-8"))
        payload["creator_agent_id"] = "root-orchestrator"
        provisional.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["main_provisional_sha256"] = _sha256(provisional)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_PROVISIONAL_CREATOR_MISMATCH", {item.code for item in report.findings})

    def test_shadow_fact_closure_cohort_is_sealed(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        closure = root / "02d_fact_closure_candidates.json"
        payload = json.loads(closure.read_text(encoding="utf-8"))
        payload["candidate_ids"][-1] = "D-012"
        closure.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["fact_closure_candidates_sha256"] = _sha256(closure)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_FACT_CLOSURE_COHORT_MISMATCH", {item.code for item in report.findings})

    def test_shadow_fact_closure_creator_is_isolated(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        closure = root / "02d_fact_closure_candidates.json"
        payload = json.loads(closure.read_text(encoding="utf-8"))
        payload["creator_agent_id"] = "root-orchestrator"
        closure.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["fact_closure_candidates_sha256"] = _sha256(closure)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_FACT_CLOSURE_CREATOR_MISMATCH", {item.code for item in report.findings})

    def test_shadow_finalist_requires_completed_fact_closure(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "finalist":
                record["frozen_at"] = "2026-08-21T13:59:00+02:00"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_FINALIST_FROZEN_BEFORE_FACT_CLOSURE", {item.code for item in report.findings})

    def test_valid_matched_baseline_protocol(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        _convert_shadow_fixture_to_matched_baseline(root)
        report = self._audit(root)
        self.assertEqual(report.status, "PASS", report.to_json())

    def test_matched_baseline_needs_twelve_directions(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        _convert_shadow_fixture_to_matched_baseline(root)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        ledger = _read_jsonl(ledger_path, [])
        for record in ledger:
            record.pop("_line", None)
            if record.get("record_type") == "mapping" and record.get("direction_id") == "DIR-011":
                record["direction_id"] = "DIR-009"
            if record.get("record_type") == "mapping" and record.get("direction_id") == "DIR-012":
                record["direction_id"] = "DIR-010"
        _write_jsonl(ledger_path, ledger)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("MATCHED_BASELINE_DIRECTION_COUNT", {item.code for item in report.findings})

    def test_orphan_raw(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = [
            record
            for record in _read_jsonl(ledger_path, [])
            if not (record.get("record_type") == "mapping" and record.get("raw_id") == "RAW-040")
        ]
        for record in records:
            record.pop("_line", None)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("RAW_UNACCOUNTED", {item.code for item in report.findings})

    def test_duplicate_mapping(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        duplicate = dict(next(record for record in records if record.get("record_type") == "mapping"))
        duplicate.pop("_line", None)
        records.append(duplicate)
        for record in records:
            record.pop("_line", None)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("RAW_MAPPING_DUPLICATE", {item.code for item in report.findings})

    def test_late_evidence(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("evidence_id") == "EV-0001":
                record["recorded_at"] = "2026-08-21T10:08:00+02:00"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("EVIDENCE_RECORDED_AFTER_FREEZE", {item.code for item in report.findings})

    def test_forbidden_context(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        forbidden = root / "Personalities" / "ZeroToOne.txt"
        forbidden.parent.mkdir(exist_ok=True)
        forbidden.write_text("validator framework\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["allowlisted_files"].append("Personalities/ZeroToOne.txt")
                record["files_read"].append("Personalities/ZeroToOne.txt")
                record["context_files"].append(
                    {
                        "path": "Personalities/ZeroToOne.txt",
                        "sha256": _sha256(forbidden),
                    }
                )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FORBIDDEN_CONTEXT_FILE", {item.code for item in report.findings})

    def test_forbidden_context_content(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        packet = root / "context" / "generator.md"
        packet.write_text("Use holistic-11-v1 to shape the idea.\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["context_files"][0]["sha256"] = _sha256(packet)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FORBIDDEN_CONTEXT_CONTENT", {item.code for item in report.findings})

    def test_protected_contract_hash(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        self._fixed_file(root, "PERSONALITY_SITUATION.md").write_text("Changed.\n", encoding="utf-8")
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROTECTED_FILE_HASH_MISMATCH", {item.code for item in report.findings})

    def test_shadow_validator_call(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
        records.append(
            {
                "record_type": "tool_event",
                "agent_id": "shadow-1",
                "arm": "shadow",
                "stage": "selector",
                "tool": "simulated_panel",
            }
        )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_VALIDATOR_CALL", {item.code for item in report.findings})

    def test_invalid_status_cannot_bypass_completion(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        manifest = _read_jsonl(manifest_path, [])
        for record in manifest:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["status"] = "complte"
        _write_jsonl(manifest_path, manifest)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        ledger = [record for record in _read_jsonl(ledger_path, []) if record.get("record_type") != "finalist"]
        for record in ledger:
            record.pop("_line", None)
        _write_jsonl(ledger_path, ledger)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("RUN_STATUS_INVALID", {item.code for item in report.findings})

    def test_nonterminal_run_is_incomplete(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["status"] = "generating"
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertIn("RUN_NOT_COMPLETE", {item.code for item in report.findings})

    def test_malformed_finalist_ids_do_not_crash(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("finalist_id") == "FIN-01":
                record["raw_ids"] = [{}]
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FINALIST_NO_RAW_ANCESTOR", {item.code for item in report.findings})

    def test_malformed_typed_fields_are_contained(self) -> None:
        cases = [
            ("manifest", "run", None, "mode", {}),
            ("manifest", "run", None, "status", []),
            ("manifest", "agent", "generator-1", "stage", {}),
            ("manifest", "agent", "generator-1", "context_classes", [{}]),
            ("manifest", "query", "Q-0001", "entity_ids", [None]),
            ("manifest", "source_open", "SRC-0001", "evidence_ids", [{}]),
            ("ledger", "finalist", "FIN-01", "evidence_ids", [False]),
            ("ledger", "evidence", "EV-0001", "source_event_ids", [False]),
        ]
        for artifact, record_type, record_id, field, value in cases:
            with self.subTest(artifact=artifact, record_type=record_type, field=field):
                temporary, root = self._fixture()
                try:
                    path = root / (
                        "00a_context_and_resource_manifest.jsonl"
                        if artifact == "manifest"
                        else "02b_raw_to_direction_ledger.jsonl"
                    )
                    records = _read_jsonl(path, [])
                    id_fields = ("agent_id", "query_id", "source_event_id", "finalist_id", "evidence_id")
                    for record in records:
                        record.pop("_line", None)
                        matches_id = record_id is None or any(record.get(key) == record_id for key in id_fields)
                        if record.get("record_type") == record_type and matches_id:
                            record[field] = value
                            break
                    _write_jsonl(path, records)
                    report = self._audit(root)
                    self.assertIn(report.status, {"FAIL", "INCOMPLETE"})
                finally:
                    temporary.cleanup()

    def test_zero_agent_provenance_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = [record for record in _read_jsonl(manifest_path, []) if record.get("record_type") != "agent"]
        for record in records:
            record.pop("_line", None)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_PROVENANCE_MISSING", {item.code for item in report.findings})

    def test_unknown_agent_stage_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["stage"] = "generaton"
                record["fork_turns"] = "all"
            elif record.get("record_type") in {"query", "source_open"}:
                record["stage"] = "generaton"
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_STAGE_INVALID", {item.code for item in report.findings})

    def test_negative_resource_value_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["resources"]["output_tokens"] = -5
            if record.get("record_type") == "run":
                record["resource_totals"]["output_tokens"] = -5
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_RESOURCE_INVALID", {item.code for item in report.findings})

    def test_empty_budget_is_not_a_pass(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["budgets"] = {}
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertIn("RESOURCE_BUDGET_FIELDS_MISSING", {item.code for item in report.findings})

    def test_score_and_objection_packet_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        packet = root / "context" / "generator.md"
        packet.write_text(
            "Prior validator score 86. Evaluator objections follow. Historical rejection rhetoric.",
            encoding="utf-8",
        )
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["context_files"][0]["sha256"] = _sha256(packet)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FORBIDDEN_CONTEXT_CONTENT", {item.code for item in report.findings})

    def test_read_without_hash_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        untracked = root / "context" / "extra.md"
        untracked.write_text("Neutral but untracked input.\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["allowlisted_files"].append("context/extra.md")
                record["files_read"].append("context/extra.md")
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("CONTEXT_READ_NOT_HASHED", {item.code for item in report.findings})

    def test_duplicate_finalist_content_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        source = root / "finalist_candidate_01.md"
        for record in records:
            record.pop("_line", None)
            if record.get("finalist_id") == "FIN-02":
                record["artifact_path"] = source.name
                record["sha256"] = _sha256(source)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FINALIST_CONTENT_DUPLICATE", {item.code for item in report.findings})

    def test_rejected_raw_cannot_support_finalist(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "RAW-001":
                record["disposition"] = "rejected"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FINALIST_ANCESTRY_INELIGIBLE", {item.code for item in report.findings})

    def test_event_outside_run_window_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("evidence_id") == "EV-0001":
                record["recorded_at"] = "2026-08-21T10:09:00+02:00"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("EVIDENCE_OUTSIDE_RUN_WINDOW", {item.code for item in report.findings})

    def test_ghost_entity_lineage_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") in {"query", "source_open"}:
                record["entity_ids"] = ["GHOST-999"]
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("QUERY_ENTITY_UNKNOWN", {item.code for item in report.findings})
        self.assertIn("EVIDENCE_ENTITY_LINEAGE_MISMATCH", {item.code for item in report.findings})

    def test_one_way_evidence_link_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "source_open":
                record["evidence_ids"].remove("EV-0001")
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("EVIDENCE_SOURCE_LINK_ONE_WAY", {item.code for item in report.findings})

    def test_dollar_prefixed_evaluator_is_blocked(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
        records.append(
            {
                "record_type": "tool_event",
                "call_id": "CALL-001",
                "agent_id": "generator-1",
                "arm": "shadow",
                "stage": "generation",
                "tool": "$evaluate-zero-to-one",
                "event_type": "tool_call",
                "occurred_at": "2026-08-21T10:01:00+02:00",
            }
        )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_VALIDATOR_CALL", {item.code for item in report.findings})

    def test_post_run_evaluator_event_cannot_bypass_approval(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
        records.append(
            {
                "record_type": "tool_event",
                "call_id": "CALL-POST",
                "agent_id": "generator-1",
                "arm": "shadow",
                "stage": "generation",
                "tool": "$evaluate-zero-to-one",
                "event_type": "tool_call",
                "occurred_at": "2026-08-21T10:09:00+02:00",
            }
        )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        codes = {item.code for item in report.findings}
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_VALIDATOR_CALL", codes)
        self.assertIn("TOOL_EVENT_AFTER_RUN", codes)

    def test_live_finalist_cannot_disable_routing(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "finalist":
                record["validation_eligible"] = False
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("LIVE_FINALIST_ELIGIBILITY_INVALID", {item.code for item in report.findings})

    def test_live_finalist_filename_is_enforced(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        old_path = root / "finalist_candidate_01.md"
        new_path = root / "candidate_01.md"
        old_path.rename(new_path)
        for record in records:
            record.pop("_line", None)
            if record.get("finalist_id") == "FIN-01":
                record["artifact_path"] = new_path.name
                record["sha256"] = _sha256(new_path)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("LIVE_FINALIST_FILENAME_INVALID", {item.code for item in report.findings})

    def test_nonrouting_id_cannot_enter_live_evaluator_packet(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        shadow = root / "shadow_archipelago_lite"
        shadow.mkdir()
        _write_jsonl(
            shadow / "02b_raw_to_direction_ledger.jsonl",
            [{"record_type": "finalist", "finalist_id": "SFIN-01"}],
        )
        (root / "evaluation_candidate.md").write_text(
            "Evaluate shadow candidate SFIN-01.\n", encoding="utf-8"
        )
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("NONROUTING_ID_IN_LIVE_ARTIFACT", {item.code for item in report.findings})

    def test_unread_prohibited_packet_is_still_rejected(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        packet = root / "context" / "generator.md"
        packet.write_text("Prior validator score 86 and evaluator objections.\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["context_files"][0]["sha256"] = _sha256(packet)
                record["files_read"] = []
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FORBIDDEN_CONTEXT_CONTENT", {item.code for item in report.findings})

    def test_unknown_manifest_record_type_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
        records.append(
            {
                "record_type": "tool_evnt",
                "call_id": "CALL-TYPO",
                "tool": "$evaluate-zero-to-one",
            }
        )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("MANIFEST_RECORD_TYPE_INVALID", {item.code for item in report.findings})

    def test_query_tool_event_must_link_known_query(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
        records.append(
            {
                "record_type": "tool_event",
                "call_id": "CALL-GHOST",
                "agent_id": "generator-1",
                "arm": "live",
                "stage": "generation",
                "tool": "web_search",
                "event_type": "tool_call",
                "query_id": "Q-GHOST",
                "occurred_at": "2026-08-21T10:00:40+02:00",
            }
        )
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("TOOL_QUERY_UNKNOWN", {item.code for item in report.findings})

    def test_protected_contract_set_cannot_be_empty(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["protected_files"] = []
                record["protected_blocks"] = []
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROTECTED_CONTRACT_SET_EMPTY", {item.code for item in report.findings})

    def test_protected_post_hash_cannot_replace_prerun_anchor(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        protected = self._fixed_file(root, "PERSONALITY_SITUATION.md")
        protected.write_text("Changed after registration.\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                for item in record["protected_files"]:
                    if str(item.get("path", "")).endswith("PERSONALITY_SITUATION.md"):
                        item["sha256"] = _sha256(protected)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROTECTED_FILE_CHANGED_DURING_RUN", {item.code for item in report.findings})

    def test_shadow_provisional_selector_cannot_run_before_level1(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("agent_id") == "provisional-1":
                record["started_at"] = "2026-08-21T12:26:00+02:00"
                record["ended_at"] = "2026-08-21T12:26:30+02:00"
                record["resources"]["elapsed_minutes"] = 0.5
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_PROVISIONAL_STAGE_ORDER_INVALID", {item.code for item in report.findings})

    def test_shadow_finalist_selector_cannot_run_before_level2(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("agent_id") == "finalist-selector-1":
                record["started_at"] = "2026-08-21T13:09:00+02:00"
                record["ended_at"] = "2026-08-21T13:09:30+02:00"
                record["resources"]["elapsed_minutes"] = 0.5
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_FINALIST_SELECTOR_STAGE_ORDER_INVALID", {item.code for item in report.findings})

    def test_shadow_problem_card_requires_evidence(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("problem_id") == "P-customer_workarounds-01":
                record["evidence_ids"] = []
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROBLEM_EVIDENCE_MISSING", {item.code for item in report.findings})

    def test_query_text_and_source_url_are_required(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "query":
                record["query"] = ""
            if record.get("record_type") == "source_open":
                record["url"] = ""
            if record.get("record_type") == "run":
                record["resource_totals"]["unique_queries"] = 0
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        codes = {item.code for item in report.findings}
        self.assertIn("QUERY_TEXT_INVALID", codes)
        self.assertIn("SOURCE_URL_INVALID", codes)

    def test_agent_elapsed_must_match_timestamps(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent":
                record["resources"]["elapsed_minutes"] = 1_000_000
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_ELAPSED_MISMATCH", {item.code for item in report.findings})

    def test_elapsed_normalizes_the_dst_fallback_fold(self) -> None:
        start = datetime.fromisoformat("2026-10-25T02:30:00+02:00")
        end = datetime.fromisoformat("2026-10-25T02:15:00+01:00")
        self.assertEqual(_elapsed_microseconds(start, end), 2_700_000_000)

    def test_malformed_evidence_source_list_is_contained(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("evidence_id") == "EV-0001":
                record["source_event_ids"] = None
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertIn("EVIDENCE_SOURCE_LINK_UNKNOWN", {item.code for item in report.findings})

    def test_live_requires_all_five_creative_roles(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("agent_id") == "generator-5":
                record["role"] = "incumbent_attacker"
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("LIVE_CREATIVE_ROLE_SET_INVALID", {item.code for item in report.findings})

    def test_mapping_requires_reversible_cluster_rationale(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "RAW-001":
                record.pop("reason", None)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("MAPPING_REASON_MISSING", {item.code for item in report.findings})

    def test_evidence_schema_is_required(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("evidence_id") == "EV-0001":
                record.pop("proposition", None)
                record["status"] = "maybe"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        codes = {item.code for item in report.findings}
        self.assertIn("EVIDENCE_FIELD_MISSING", codes)
        self.assertIn("EVIDENCE_STATUS_INVALID", codes)

    def test_shadow_cannot_contain_evaluation_artifact(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        (root / "evaluation_shadow.md").write_text("No evaluator is allowed here.\n", encoding="utf-8")
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("NONROUTING_DOWNSTREAM_ARTIFACT", {item.code for item in report.findings})

    def test_missing_external_trust_pins_is_incomplete(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        report = audit_run(
            root, _fixed_contract_paths=_fixture_fixed_contract_paths(root)
        )
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertIn("EXTERNAL_TRUST_PINS_MISSING", {item.code for item in report.findings})

    def test_manifest_local_protection_forgery_fails_external_anchor(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        protected = self._fixed_file(root, "Personalities/ZeroToOne.txt")
        protected.write_text("Forged validator framework.\n", encoding="utf-8")
        forged_hash = _sha256(protected)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                for item in record["protected_files"]:
                    if str(item.get("path", "")).endswith("Personalities/ZeroToOne.txt"):
                        item["pre_run_sha256"] = forged_hash
                        item["sha256"] = forged_hash
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROTECTED_FILE_EXTERNAL_ANCHOR_MISMATCH", {item.code for item in report.findings})

    def test_ledger_local_finalist_forgery_fails_external_seal(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        dossier = root / "finalist_candidate_01.md"
        dossier.write_text("# Rewritten after freeze\n", encoding="utf-8")
        forged_hash = _sha256(dossier)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("finalist_id") == "FIN-01":
                record["sha256"] = forged_hash
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FINALIST_EXTERNAL_SEAL_MISMATCH", {item.code for item in report.findings})

    def test_extra_candidate_artifact_fails_sealed_set(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        (root / "finalist_unsealed.md").write_text("# Unsealed candidate\n", encoding="utf-8")
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("FREEZE_SEAL_ARTIFACT_SET_MISMATCH", {item.code for item in report.findings})

    def test_external_snapshot_inside_run_is_rejected(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        anchor = root / ".fixture_protection_anchor.json"
        with self.assertRaises(ValueError):
            _read_pinned_external_json(anchor, _sha256(anchor), root)

    def test_external_snapshot_pin_mismatch_is_rejected(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        external = root.parent / "external-anchor.json"
        external.write_bytes((root / ".fixture_protection_anchor.json").read_bytes())
        with self.assertRaises(ValueError):
            _read_pinned_external_json(external, "0" * 64, root)

    def test_live_arm_seal_must_be_external_to_live_run(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        protection = root.parent / "external-protection-anchor.json"
        protection.write_bytes(
            (root / ".fixture_protection_anchor.json").read_bytes()
        )
        freeze_seal = root.parent / "external-shadow-freeze-seal.json"
        freeze_seal.write_bytes((root / ".fixture_freeze_seal.json").read_bytes())
        original_live_seal = root.parent / ".fixture_live_arm_freeze_seal.json"
        live_payload = json.loads(original_live_seal.read_text(encoding="utf-8"))
        live_root = Path(str(live_payload["run_dir"]))
        inside_live_seal = live_root / "live_freeze_seal.json"
        inside_live_seal.write_bytes(original_live_seal.read_bytes())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(
                [
                    str(root),
                    "--protection-anchor",
                    str(protection),
                    "--protection-anchor-sha256",
                    _sha256(protection),
                    "--freeze-seal",
                    str(freeze_seal),
                    "--freeze-seal-sha256",
                    _sha256(freeze_seal),
                    "--live-arm-freeze-seal",
                    str(inside_live_seal),
                    "--live-arm-freeze-seal-sha256",
                    _sha256(inside_live_seal),
                ]
            )
        self.assertEqual(exit_code, 3)
        self.assertIn("outside the live run directory", stderr.getvalue())

    def test_matched_resource_caps_are_exact(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["budgets"] = {
                    "unique_queries": 600,
                    "uncached_input_tokens": 20_000_000,
                    "output_tokens": 1_400_000,
                    "elapsed_minutes": 360,
                    "max_concurrency": 6,
                }
        _write_jsonl(manifest_path, records)
        report = self._audit(root, strict=True)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("MATCHED_RESOURCE_CAPS_INVALID", {item.code for item in report.findings})

    def test_shadow_mode_cannot_disable_matched_pilot(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        live_seal_path = root.parent / ".fixture_live_arm_freeze_seal.json"
        live_seal = json.loads(live_seal_path.read_text(encoding="utf-8"))
        live_seal["matched_pilot"] = False
        live_seal_path.write_bytes(_json_bytes(live_seal))

        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["matched_pilot"] = False
                record["live_arm_freeze_seal_sha256"] = _sha256(live_seal_path)
        _write_jsonl(manifest_path, records)

        freeze_seal_path = root / ".fixture_freeze_seal.json"
        freeze_seal = json.loads(freeze_seal_path.read_text(encoding="utf-8"))
        freeze_seal["matched_pilot"] = False
        freeze_seal_path.write_bytes(_json_bytes(freeze_seal))

        report = self._audit(root, strict=True)
        self.assertEqual(report.status, "FAIL")
        codes = {item.code for item in report.findings}
        self.assertIn("SHADOW_MATCHED_PILOT_REQUIRED", codes)
        self.assertIn("LIVE_ARM_MATCHED_MODE_MISMATCH", codes)

    def test_shadow_requires_pinned_live_arm_seal(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        protection_path = root / ".fixture_protection_anchor.json"
        seal_path = root / ".fixture_freeze_seal.json"
        report = audit_run(
            root,
            protection_anchor=json.loads(protection_path.read_text(encoding="utf-8")),
            protection_anchor_sha256=_sha256(protection_path),
            freeze_seal=json.loads(seal_path.read_text(encoding="utf-8")),
            freeze_seal_sha256=_sha256(seal_path),
            _fixed_contract_paths=_fixture_fixed_contract_paths(root),
        )
        self.assertEqual(report.status, "INCOMPLETE", report.to_json())
        self.assertIn("LIVE_ARM_FREEZE_SEAL_MISSING", {item.code for item in report.findings})

    def test_live_arm_model_and_dispatch_are_externally_bound(self) -> None:
        mutations = (
            ("model", "other-model", "CROSS_ARM_MODEL_MISMATCH"),
            ("sealed_at", "2026-08-21T12:02:00+02:00", "SHADOW_DISPATCH_ORDER_INVALID"),
        )
        for field, value, expected_code in mutations:
            with self.subTest(field=field):
                temporary, root = self._shadow_fixture()
                try:
                    live_path = root.parent / ".fixture_live_arm_freeze_seal.json"
                    live_payload = json.loads(live_path.read_text(encoding="utf-8"))
                    live_payload[field] = value
                    live_path.write_bytes(_json_bytes(live_payload))
                    manifest_path = root / "00a_context_and_resource_manifest.jsonl"
                    records = _read_jsonl(manifest_path, [])
                    for record in records:
                        record.pop("_line", None)
                        if record.get("record_type") == "run":
                            record["live_arm_freeze_seal_sha256"] = _sha256(live_path)
                    _write_jsonl(manifest_path, records)
                    report = self._audit(root)
                    self.assertEqual(report.status, "FAIL")
                    self.assertIn(expected_code, {item.code for item in report.findings})
                finally:
                    temporary.cleanup()

    def test_same_suffix_fixed_contract_forgery_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        attacker = root.parent / "attacker" / "Personalities" / "ZeroToOne.txt"
        attacker.parent.mkdir(parents=True)
        attacker.write_text("Forged validator criteria.\n", encoding="utf-8")
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                for item in record["protected_files"]:
                    if str(item.get("path", "")).endswith("Personalities/ZeroToOne.txt"):
                        item["path"] = str(attacker.resolve())
                        item["pre_run_sha256"] = _sha256(attacker)
                        item["sha256"] = _sha256(attacker)
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROTECTED_FILE_CANONICAL_PATH_INVALID", {item.code for item in report.findings})

    def test_direct_audit_rejects_fake_digest_strings(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        protection = json.loads((root / ".fixture_protection_anchor.json").read_text(encoding="utf-8"))
        seal = json.loads((root / ".fixture_freeze_seal.json").read_text(encoding="utf-8"))
        seal["protection_anchor_sha256"] = "0" * 64
        report = audit_run(
            root,
            protection_anchor=protection,
            protection_anchor_sha256="0" * 64,
            freeze_seal=seal,
            freeze_seal_sha256="0" * 64,
            _fixed_contract_paths=_fixture_fixed_contract_paths(root),
        )
        self.assertEqual(report.status, "FAIL")
        codes = {item.code for item in report.findings}
        self.assertIn("PROTECTION_ANCHOR_PAYLOAD_HASH_MISMATCH", codes)
        self.assertIn("FREEZE_SEAL_PAYLOAD_HASH_MISMATCH", codes)

    def test_deep_external_json_is_contained(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        external = root.parent / "deep-anchor.json"
        external.write_bytes(
            b'{"x":' + (b"[" * 2_000) + b"0" + (b"]" * 2_000) + b"}\n"
        )
        with self.assertRaises(ValueError):
            _read_pinned_external_json(external, _sha256(external), root)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            exit_code = main(
                [
                    str(root),
                    "--protection-anchor",
                    str(external),
                    "--protection-anchor-sha256",
                    _sha256(external),
                ]
            )
        self.assertEqual(exit_code, 3)
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_nonrouting_downstream_filename_variants_are_recursive(self) -> None:
        filenames = (
            "reevaluation_candidate.md",
            "04_evaluator_packet.md",
            "08_simulated_panel_request.md",
            "06_advisory_outcomes.md",
            "nested/finalist_leak.md",
            "nested/validation_request.md",
            "nested/04_judge_packet.md",
            "nested/06_scorecard.md",
            "nested/real_chat_request.md",
            "nested/confirmed-idea.md",
            "nested/adjudication_result.json",
        )
        for filename in filenames:
            with self.subTest(filename=filename):
                temporary, root = self._shadow_fixture()
                try:
                    artifact = root / filename
                    artifact.parent.mkdir(parents=True, exist_ok=True)
                    artifact.write_text("Forbidden downstream artifact.\n", encoding="utf-8")
                    report = self._audit(root)
                    self.assertEqual(report.status, "FAIL")
                    self.assertIn("NONROUTING_DOWNSTREAM_ARTIFACT", {item.code for item in report.findings})
                finally:
                    temporary.cleanup()

    def test_level2_dossier_is_hash_bound(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        (root / "shadow_level2" / "level2_d-001.md").unlink()
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("LEVEL2_ARTIFACT_MISSING", {item.code for item in report.findings})

    def test_level2_chronology_completion_and_uniqueness(self) -> None:
        mutations = (
            "reversed",
            "early_stop",
            "duplicate",
            "symlink",
            "empty",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                temporary, root = self._shadow_fixture()
                try:
                    ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
                    records = _read_jsonl(ledger_path, [])
                    level2_records = [
                        record for record in records if record.get("record_type") == "level2"
                    ]
                    first = level2_records[0]
                    if mutation == "reversed":
                        first["completed_at"] = "2026-08-21T13:04:00+02:00"
                    elif mutation == "early_stop":
                        first["development_status"] = "early_stop"
                        first["early_stop_code"] = "directly_falsified_premise"
                        first_path = root / str(first["artifact_path"])
                        first_path.unlink()
                        first.pop("artifact_path", None)
                        first.pop("sha256", None)
                    elif mutation == "duplicate":
                        second = level2_records[1]
                        second["artifact_path"] = first["artifact_path"]
                        second["sha256"] = first["sha256"]
                    elif mutation == "symlink":
                        first_path = root / str(first["artifact_path"])
                        target = root / str(level2_records[1]["artifact_path"])
                        first_path.unlink()
                        first_path.symlink_to(target)
                        first["sha256"] = _sha256(target)
                    elif mutation == "empty":
                        first_path = root / str(first["artifact_path"])
                        first_path.write_bytes(b"")
                        first["sha256"] = _sha256(first_path)
                    for record in records:
                        record.pop("_line", None)
                    _write_jsonl(ledger_path, records)
                    report = self._audit(root)
                    self.assertEqual(report.status, "FAIL")
                    expected = {
                        "reversed": "LEVEL2_COMPLETION_PRECEDES_SELECTION",
                        "early_stop": "SHADOW_FACT_CLOSURE_LEVEL2_INCOMPLETE",
                        "duplicate": "LEVEL2_ARTIFACT_PATH_DUPLICATE",
                        "symlink": "LEVEL2_ARTIFACT_SYMLINK",
                        "empty": "LEVEL2_DOSSIER_SCHEMA_INVALID",
                    }[mutation]
                    self.assertIn(expected, {item.code for item in report.findings})
                finally:
                    temporary.cleanup()

    def test_evidence_query_source_tool_chronology(self) -> None:
        mutations = ("after_freeze", "source_before_query", "source_context", "tool_before_query")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                temporary, root = self._shadow_fixture()
                try:
                    manifest_path = root / "00a_context_and_resource_manifest.jsonl"
                    records = _read_jsonl(manifest_path, [])
                    for record in records:
                        record.pop("_line", None)
                        if mutation == "after_freeze" and record.get("agent_id") == "closure-1":
                            if record.get("record_type") == "agent":
                                record["ended_at"] = "2026-08-21T14:25:00+02:00"
                                record["resources"]["elapsed_minutes"] = 40.0
                            elif record.get("record_type") in {"query", "source_open", "tool_event"}:
                                record["occurred_at"] = "2026-08-21T14:20:00+02:00"
                        if mutation == "source_before_query" and record.get("source_event_id") == "SRC-FC-1":
                            record["occurred_at"] = "2026-08-21T13:50:00+02:00"
                        if mutation == "source_context" and record.get("source_event_id") == "SRC-FC-1":
                            record["arm"] = "live"
                            record["stage"] = "generation"
                        if mutation == "tool_before_query" and record.get("call_id") == "CALL-FC-1":
                            record["occurred_at"] = "2026-08-21T13:50:00+02:00"
                    _write_jsonl(manifest_path, records)
                    report = self._audit(root)
                    self.assertEqual(report.status, "FAIL")
                    expected = {
                        "after_freeze": "FINALIST_SOURCE_AFTER_FREEZE",
                        "source_before_query": "SOURCE_PRECEDES_QUERY",
                        "source_context": "SOURCE_AGENT_CONTEXT_MISMATCH",
                        "tool_before_query": "TOOL_PRECEDES_QUERY",
                    }[mutation]
                    self.assertIn(expected, {item.code for item in report.findings})
                finally:
                    temporary.cleanup()

    def test_shadow_downstream_tool_aliases_are_blocked(self) -> None:
        for tool_name in ("judge", "evaluator", "scorecard", "adjudicator", "fresh-chat", "real-chat"):
            with self.subTest(tool=tool_name):
                temporary, root = self._shadow_fixture()
                try:
                    manifest_path = root / "00a_context_and_resource_manifest.jsonl"
                    records = _read_jsonl(manifest_path, [])
                    for record in records:
                        record.pop("_line", None)
                    records.append(
                        {
                            "record_type": "tool_event",
                            "call_id": f"CALL-{tool_name}",
                            "agent_id": "closure-1",
                            "arm": "shadow",
                            "stage": "fact_closure",
                            "tool": tool_name,
                            "event_type": "tool_call",
                            "occurred_at": "2026-08-21T14:31:00+02:00",
                        }
                    )
                    _write_jsonl(manifest_path, records)
                    report = self._audit(root)
                    self.assertEqual(report.status, "FAIL")
                    self.assertIn("SHADOW_VALIDATOR_CALL", {item.code for item in report.findings})
                finally:
                    temporary.cleanup()

    def test_sealed_shadow_finalist_cannot_smuggle_validator_content(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        finalist = next(record for record in records if record.get("finalist_id") == "SFIN-01")
        artifact = root / str(finalist["artifact_path"])
        artifact.write_text("# Shadow candidate\n\nholistic-11-v1 validator score: 9.7\n", encoding="utf-8")
        finalist["sha256"] = _sha256(artifact)
        for record in records:
            record.pop("_line", None)
        _write_jsonl(ledger_path, records)
        _capture_fixture_trust(root)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("NONROUTING_FINALIST_PROHIBITED_CONTENT", {item.code for item in report.findings})

    def test_shadow_island_enum_is_exact(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("problem_id") == "P-customer_workarounds-01":
                record["source_island"] = "regulation_variant"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_SOURCE_ISLAND_INVALID", {item.code for item in report.findings})

    def test_shadow_scout_output_must_match_ledger(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "agent" and record.get("agent_id") == "scout-1":
                record["output_ids"][-1] = "P-spend_procurement-01"
        _write_jsonl(manifest_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_OUTPUT_LEDGER_MISMATCH", {item.code for item in report.findings})

    def test_problem_evidence_needs_entity_lineage(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("evidence_id") == "EV-P-001":
                record["entity_ids"] = ["P-customer_workarounds-02"]
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("PROBLEM_EVIDENCE_ENTITY_MISMATCH", {item.code for item in report.findings})

    def test_direct_problem_partition_cannot_duplicate_parent(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "D-002":
                record["parent_ids"] = ["P-customer_workarounds-01"]
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_DIRECT_PROBLEM_PARTITION_INVALID", {item.code for item in report.findings})

    def test_inversion_operation_is_required(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "I-001":
                record.pop("operation", None)
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_INVERSION_OPERATION_INVALID", {item.code for item in report.findings})

    def test_recombination_requires_distinct_islands(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "X-001":
                record["parent_ids"] = ["D-001", "D-002"]
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("SHADOW_RECOMBINATION_ISLANDS_INVALID", {item.code for item in report.findings})

    def test_concept_creator_must_match_agent_outputs(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        ledger_path = root / "02b_raw_to_direction_ledger.jsonl"
        records = _read_jsonl(ledger_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("raw_id") == "D-001":
                record["creator_agent_id"] = "builder-2"
        _write_jsonl(ledger_path, records)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL")
        self.assertIn("AGENT_OUTPUT_LEDGER_MISMATCH", {item.code for item in report.findings})

    def test_legacy_prose_mentions_are_not_dispositions(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        raw_ids = ["R08"] + [f"T{index:02d}" for index in range(1, 55)]
        (root / "02a_adversarial_raw_pool.md").write_text(
            "# Raw\n\n" + "\n\n".join(f"### {raw_id} — Idea" for raw_id in raw_ids) + "\n",
            encoding="utf-8",
        )
        (root / "02_candidate_funnel.md").write_text(
            "No dispositions were recorded. Mentioned IDs: "
            + ", ".join(raw_ids)
            + ".\n\n| Raw codes | Notes |\n|---|---|\n| "
            + ", ".join(raw_ids)
            + " | ancestry references only |\n",
            encoding="utf-8",
        )
        report = audit_legacy_august(root)
        self.assertEqual(report.status, "INCOMPLETE")
        self.assertEqual(report.counts["explicit_initial_dispositions"], 0)
        self.assertEqual(report.counts["unknown_initial_dispositions"], 55)

    def test_v2_profile_contracts_are_exact(self) -> None:
        self.assertIn(
            ("audited_funnel", "live", "enabled", "initial"),
            PROFILE_SPECS_V2["operational_live_with_shadow"].allowed_contracts,
        )
        self.assertIn(
            (
                "archipelago_lite_shadow",
                "shadow",
                "frozen_nonrouting",
                "initial",
            ),
            PROFILE_SPECS_V2["operational_live_with_shadow"].allowed_contracts,
        )
        self.assertIn(
            (
                "archipelago_lite_shadow",
                "shadow",
                "frozen_nonrouting",
                "initial",
            ),
            PROFILE_SPECS_V2["v2_matched_nonrouting"].allowed_contracts,
        )
        self.assertIn(
            ("audited_funnel", "live", "enabled", "initial"),
            PROFILE_SPECS_V2["ordinary_audited_funnel"].allowed_contracts,
        )
        self.assertIn(
            ("audited_funnel", "live", "enabled", "regeneration"),
            PROFILE_SPECS_V2["ordinary_audited_funnel"].allowed_contracts,
        )
        for profile_name in (
            "operational_live_with_shadow",
            "v2_matched_nonrouting",
        ):
            self.assertFalse(
                any(
                    contract[-1] == "regeneration"
                    for contract in PROFILE_SPECS_V2[profile_name].allowed_contracts
                )
            )
        self.assertNotIn("operational-live-with-shadow", PROFILE_SPECS_V2)

    def test_v2_shadow_routing_compatibility_mirror_is_fail_closed(self) -> None:
        shadow_profiles = (
            (
                "operational_live_with_shadow",
                "audited_funnel",
                "live",
                "enabled",
            ),
            (
                "v2_matched_nonrouting",
                "audited_funnel",
                "matched_baseline",
                "frozen_nonrouting",
            ),
            (
                "operational_live_with_shadow",
                "archipelago_lite_shadow",
                "shadow",
                "frozen_nonrouting",
            ),
        )
        for profile_name, mode, arm, routing_state in shadow_profiles:
            with self.subTest(profile_name=profile_name, arm=arm):
                run_record = {
                    "run_profile": profile_name,
                    "mode": mode,
                    "arm": arm,
                    "routing_state": routing_state,
                    "lifecycle_state": "complete",
                    "declared_child_scopes": [],
                    "shadow_can_route_to_validation": True,
                }
                findings: list[Finding] = []
                _audit_v2_compatibility_mirrors(
                    run_record,
                    profile_name,
                    "00a_context_and_resource_manifest.jsonl",
                    findings,
                )
                self.assertEqual(
                    [item.code for item in findings],
                    ["V2_COMPATIBILITY_MIRROR_MISMATCH"],
                )
                run_record["shadow_can_route_to_validation"] = False
                findings = []
                _audit_v2_compatibility_mirrors(
                    run_record,
                    profile_name,
                    "00a_context_and_resource_manifest.jsonl",
                    findings,
                )
                self.assertEqual(findings, [])

        ordinary_no_shadow = {
            "run_profile": "ordinary_audited_funnel",
            "mode": "audited_funnel",
            "arm": "live",
            "routing_state": "enabled",
            "lifecycle_state": "complete",
            "declared_child_scopes": [],
        }
        findings = []
        _audit_v2_compatibility_mirrors(
            ordinary_no_shadow,
            "ordinary_audited_funnel",
            "00a_context_and_resource_manifest.jsonl",
            findings,
        )
        self.assertEqual(findings, [])
        ordinary_no_shadow["shadow_can_route_to_validation"] = True
        findings = []
        _audit_v2_compatibility_mirrors(
            ordinary_no_shadow,
            "ordinary_audited_funnel",
            "00a_context_and_resource_manifest.jsonl",
            findings,
        )
        self.assertEqual(
            [item.code for item in findings],
            ["V2_COMPATIBILITY_MIRROR_MISMATCH"],
        )
        ordinary_no_shadow["shadow_can_route_to_validation"] = False
        findings = []
        _audit_v2_compatibility_mirrors(
            ordinary_no_shadow,
            "ordinary_audited_funnel",
            "00a_context_and_resource_manifest.jsonl",
            findings,
        )
        self.assertEqual(findings, [])

    def test_v2_stage_predecessors_and_reachable_boundaries_are_strict(self) -> None:
        live_boundary = self._v2_state_chain_probe(
            "audited_funnel",
            [("level1-boundary", "level1", 270, 300)],
            LIVE_STATE_CHAIN_V2[:6],
        )
        self.assertTrue(
            any(
                item.code == "STAGE_BOUNDARY_AGENT_TIMING_INVALID"
                and item.node_ids == ("level1-boundary",)
                for item in live_boundary
            )
        )
        shadow_boundary = self._v2_state_chain_probe(
            "archipelago_lite_shadow",
            [("history-boundary", "history_compressor", 210, 240)],
            SHADOW_STATE_CHAIN_V2[:5],
        )
        self.assertTrue(
            any(
                item.code == "STAGE_BOUNDARY_AGENT_TIMING_INVALID"
                and item.node_ids == ("history-boundary",)
                for item in shadow_boundary
            )
        )

        live_dependencies = self._v2_state_chain_probe(
            "audited_funnel",
            [
                ("cluster-order", "cluster_audit", 60, 120),
                ("level1-order", "level1", 120, 180),
                ("level2-order", "level2", 180, 240),
            ],
            LIVE_STATE_CHAIN_V2[:1],
        )
        live_messages = {
            item.message
            for item in live_dependencies
            if item.code == "V2_STAGE_DEPENDENCY_INVALID"
        }
        self.assertTrue(
            any("['cluster_audit']" in message and "['level1']" in message for message in live_messages)
        )
        self.assertTrue(
            any("['level1']" in message and "['level2']" in message for message in live_messages)
        )

        shadow_dependencies = self._v2_state_chain_probe(
            "archipelago_lite_shadow",
            [
                ("history-order", "history_compressor", 60, 120),
                ("cartography-order", "cartography", 120, 180),
            ],
            SHADOW_STATE_CHAIN_V2[:1],
        )
        self.assertTrue(
            any(
                item.code == "V2_STAGE_DEPENDENCY_INVALID"
                and "['history_compressor']" in item.message
                and "['cartography']" in item.message
                for item in shadow_dependencies
            )
        )

    def test_parity_exact_ten_percent_passes_and_zero_is_incomplete(self) -> None:
        parent = {key: 100 for key in DEVELOPMENT_METRIC_KEYS}
        child = {key: 90 for key in DEVELOPMENT_METRIC_KEYS}
        findings: list[Finding] = []
        _compare_development_parity(parent, child, "child", findings)
        self.assertEqual(findings, [])
        parent["level2_queries"] = 0
        child["level2_queries"] = 0
        _compare_development_parity(parent, child, "child", findings)
        self.assertEqual(
            [item.code for item in findings], ["PARITY_METRIC_INCOMPLETE"]
        )

    def test_v2_prefreeze_manifest_snapshot_is_raw_and_never_overwritten(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        run_record = {
            "record_type": "run",
            "run_id": root.name,
            "schema": RUN_SCHEMA_V2,
            "scope_id": "scope-live",
            "run_profile": "ordinary_audited_funnel",
            "mode": "audited_funnel",
            "arm": "live",
            "routing_state": "enabled",
            "cohort_kind": "initial",
            "model": "test-model",
            "reasoning_effort": "high",
            "development_contract_sha256": "0" * 64,
        }
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        _write_jsonl(manifest_path, [run_record])
        original_bytes = manifest_path.read_bytes()
        records, digest = _load_or_create_v2_manifest_snapshot(root)
        snapshot_path = root / PREFREEZE_MANIFEST_SNAPSHOT_V2
        self.assertEqual(snapshot_path.read_bytes(), original_bytes)
        self.assertEqual(digest, hashlib.sha256(original_bytes).hexdigest())
        self.assertEqual(len(records), 1)

        changed_record = dict(run_record)
        changed_record["declared_child_scopes"] = []
        _write_jsonl(manifest_path, [changed_record])
        reused_records, reused_digest = _load_or_create_v2_manifest_snapshot(root)
        self.assertEqual(snapshot_path.read_bytes(), original_bytes)
        self.assertEqual(reused_digest, digest)
        self.assertNotEqual(snapshot_path.read_bytes(), manifest_path.read_bytes())
        self.assertEqual(reused_records[0].get("scope_id"), "scope-live")

        seal = {
            "manifest_snapshot_path": PREFREEZE_MANIFEST_SNAPSHOT_V2,
            "manifest_snapshot_sha256": digest,
            "sealed_at": datetime.now().astimezone().isoformat(),
        }
        findings: list[Finding] = []
        changed_records = _read_jsonl(manifest_path, [])
        _audit_v2_manifest_snapshot(
            root,
            changed_records[0],
            changed_records,
            seal,
            set(),
            findings,
        )
        self.assertNotIn(
            "FREEZE_MANIFEST_SNAPSHOT_CONTENT_MISMATCH",
            {item.code for item in findings},
        )

    def test_nested_machine_run_discovery_is_recursive(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        nested = root / "neutral" / "deep"
        nested.mkdir(parents=True)
        (nested / "00a_context_and_resource_manifest.jsonl").write_text(
            "{}\n", encoding="utf-8"
        )
        self.assertEqual(_discover_nested_machine_runs(root), {"neutral/deep"})

    def test_typed_downstream_content_ignores_neutral_filename(self) -> None:
        path = Path("neutral.json")
        self.assertTrue(
            _typed_downstream_content(
                path,
                json.dumps({"record_type": "evaluation", "validation_eligible": True}),
            )
        )
        for key in ("route", "call", "next_step", "next-step"):
            with self.subTest(key=key):
                self.assertTrue(
                    _typed_downstream_content(
                        Path("neutral_notes.md"),
                        json.dumps(
                            {
                                key: {
                                    "targets": [
                                        "send_to_fresh_chat_validator"
                                    ]
                                }
                            }
                        ),
                    )
                )
        for payload in (
            {"NextStep": "validator"},
            {"validation-eligible": True},
            {"CAN_ROUTE_TO_VALIDATION": True},
        ):
            with self.subTest(payload=payload):
                self.assertTrue(
                    _typed_downstream_content(
                        Path("neutral_notes.md"),
                        json.dumps(payload),
                    )
                )
        self.assertFalse(
            _typed_downstream_content(
                Path("neutral_notes.md"),
                json.dumps({"ValidationEligible": False}),
            )
        )
        self.assertFalse(
            _typed_downstream_content(
                Path("neutral_notes.md"),
                "A route to a fresh chat validator is discussed as ordinary prose.",
            )
        )

    def test_regeneration_contamination_is_owned_scope_and_content_typed(self) -> None:
        path = Path("neutral_notes.md")
        contaminated_texts = (
            "Live evaluator output: this should advance and was accepted.",
            "Live advisory evaluation result: retain this for the next downstream gate.",
            "Validator feedback from the live initial cohort: it passed validation.",
            "Judge panel ranking from the live initial cohort: it ranked first.",
            json.dumps({"prior_evaluator_output": {"decision": "advance"}}),
            json.dumps({"priorEvaluatorOutput": {"decision": "advance"}}),
            json.dumps({"validator": {"feedback": "retain"}}),
            json.dumps({"panel": {"ranking": ["candidate-a"]}}),
            json.dumps({"shadow": {"outputs": ["candidate-a"]}}),
            json.dumps({"matched_baseline": {"finalists": ["candidate-a"]}}),
        )
        for text in contaminated_texts:
            with self.subTest(text=text):
                self.assertTrue(_regeneration_contamination_content(path, text))

        allowed_history = (
            "Evaluate customer demand before launch. Customers judge vendors on uptime; "
            "the matching output is a neutral economic fingerprint."
        )
        self.assertFalse(_regeneration_contamination_content(path, allowed_history))
        self.assertFalse(
            _regeneration_contamination_content(
                path,
                json.dumps(
                    {
                        "history": allowed_history,
                        "validation_eligible": True,
                    }
                ),
            )
        )

        regeneration = {
            "cohort_kind": "regeneration",
            "routing_state": "enabled",
        }
        findings: list[Finding] = []
        _audit_regeneration_owned_content(
            regeneration,
            path,
            path.as_posix(),
            contaminated_texts[0],
            findings,
        )
        self.assertEqual(
            [item.code for item in findings],
            ["REGENERATION_CONTEXT_CONTAMINATION"],
        )

        for run_record in (
            {"cohort_kind": "initial", "routing_state": "enabled"},
            {"cohort_kind": "regeneration", "routing_state": "frozen_nonrouting"},
        ):
            findings = []
            _audit_regeneration_owned_content(
                run_record,
                path,
                path.as_posix(),
                contaminated_texts[0],
                findings,
            )
            self.assertEqual(findings, [])

    def test_regeneration_closed_control_artifacts_do_not_self_contaminate(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve() / "run"
        root.mkdir()
        run_payload = {
            "record_type": "run",
            "schema": RUN_SCHEMA_V2,
            "run_id": root.name,
            "scope_id": "scope-regeneration",
            "cohort_kind": "regeneration",
            "routing_state": "enabled",
            "protected_files": [
                {
                    "id": "evaluator-skill",
                    "path": "Live evaluator output: fixed-contract identity only",
                    "sha256": "0" * 64,
                }
            ],
        }
        manifest_text = json.dumps(run_payload, sort_keys=True) + "\n"
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        manifest_path.write_text(manifest_text, encoding="utf-8")
        manifest_records = [{**run_payload, "_line": 1}]
        self.assertTrue(
            _is_regeneration_control_artifact(
                root,
                run_payload,
                manifest_records,
                None,
                manifest_path,
                manifest_path.name,
                manifest_text,
            )
        )

        snapshot_path = root / PREFREEZE_MANIFEST_SNAPSHOT_V2
        snapshot_path.write_text(manifest_text, encoding="utf-8")
        freeze_seal = {
            "manifest_snapshot_path": PREFREEZE_MANIFEST_SNAPSHOT_V2,
            "manifest_snapshot_sha256": _sha256(snapshot_path),
        }
        self.assertTrue(
            _is_regeneration_control_artifact(
                root,
                run_payload,
                manifest_records,
                freeze_seal,
                snapshot_path,
                snapshot_path.name,
                manifest_text,
            )
        )

        report_payload = {
            "schema_version": SCHEMA_VERSION,
            "run_id": root.name,
            "adapter": "native-v2",
            "status": "FAIL",
            "counts": {},
            "resources": {},
            "findings": [
                asdict(
                    Finding(
                        "EXAMPLE",
                        "ERROR",
                        "Live evaluator output is quoted in this generated audit finding.",
                    )
                )
            ],
        }
        report_text = _json_bytes(report_payload).decode("utf-8")
        report_path = root / "neutral_control.json"
        report_path.write_text(report_text, encoding="utf-8")
        self.assertTrue(
            _regeneration_contamination_content(report_path, report_text)
        )
        self.assertTrue(
            _is_regeneration_control_artifact(
                root,
                run_payload,
                manifest_records,
                freeze_seal,
                report_path,
                report_path.name,
                report_text,
            )
        )

        neutral_path = root / "neutral_context.md"
        neutral_text = "Live evaluator output: advance this candidate."
        neutral_path.write_text(neutral_text, encoding="utf-8")
        self.assertFalse(
            _is_regeneration_control_artifact(
                root,
                run_payload,
                manifest_records,
                freeze_seal,
                neutral_path,
                neutral_path.name,
                neutral_text,
            )
        )

    def test_regeneration_control_records_scan_semantic_fields_only(self) -> None:
        structural_record = {
            "record_type": "run",
            "run_profile": "v2_matched_nonrouting",
            "arm": "matched_baseline",
            "routing_state": "frozen_nonrouting",
            "matched_pilot": True,
            "shadow_only": True,
            "validation_eligible": False,
            "protected_files": [
                {
                    "id": "evaluator-skill",
                    "path": "/fixed/evaluate-zero-to-one/SKILL.md",
                    "sha256": "0" * 64,
                },
                {
                    "id": "validator-personality",
                    "path": "/fixed/Personalities/ZeroToOne.txt",
                    "sha256": "1" * 64,
                },
            ],
        }
        safe_query = {
            "record_type": "query",
            "query": "retrieve neutral customer-workaround evidence",
        }
        safe_tool = {
            "record_type": "tool_event",
            "tool": "web_search",
            "event_type": "tool_call",
        }
        safe_source = {
            "record_type": "source_open",
            "url": "https://example.test/neutral-source",
        }
        self.assertFalse(
            _regeneration_control_records_contaminated(
                [structural_record, safe_query, safe_tool, safe_source]
            )
        )

        contaminated_query = {
            **safe_query,
            "query": "retrieve advisory evaluator output candidate rankings for regeneration",
        }
        self.assertTrue(
            _regeneration_control_records_contaminated(
                [structural_record, contaminated_query, safe_tool, safe_source]
            )
        )
        self.assertTrue(
            _regeneration_control_records_contaminated(
                [
                    structural_record,
                    safe_query,
                    {**safe_tool, "tool": "advisory_evaluator"},
                    safe_source,
                ]
            )
        )
        self.assertTrue(
            _regeneration_control_records_contaminated(
                [
                    structural_record,
                    safe_query,
                    safe_tool,
                    {
                        **safe_source,
                        "url": "https://example.test/advisory-evaluator-output/rankings",
                    },
                ]
            )
        )
        self.assertTrue(
            _regeneration_control_records_contaminated(
                [
                    {
                        "record_type": "tool_event",
                        "payload": {"destination": "validator"},
                    }
                ]
            )
        )

    def test_parent_typed_id_preexisting_child_is_not_a_leak(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        child = root / "shadow"
        child.mkdir()
        _write_jsonl(
            child / "02b_raw_to_direction_ledger.jsonl",
            [
                {
                    "record_type": "mapping",
                    "raw_id": "D-001",
                    "direction_id": "DIR-021",
                    "cluster_id": "CL-001",
                }
            ],
        )
        (root / "typed_live_packet.md").write_text(
            "The live cartography agent emitted DIR-021 before shadow dispatch.\n",
            encoding="utf-8",
        )
        findings: list[Finding] = []
        _audit_shadow_fingerprint_leaks(
            root,
            [
                {
                    "record_type": "mapping",
                    "raw_id": "R-001",
                    "direction_id": "DIR-021",
                    "cluster_id": "CL-PARENT",
                }
            ],
            [{"record_type": "agent", "output_ids": ["DIR-021"]}],
            [{"relationship": "shadow_child", "relative_path": "shadow"}],
            {"shadow"},
            findings,
        )
        self.assertNotIn(
            "CHILD_FINGERPRINT_ID_LEAK",
            {item.code for item in findings},
        )

    def test_legacy_live_routing_mirror_contradiction_fails(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["matched_pilot"] = False
                record["shadow_only"] = True
                record["validation_eligible"] = False
        _write_jsonl(manifest_path, records)
        _capture_fixture_trust(root)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL", report.to_json())
        self.assertIn(
            "LEGACY_ROUTING_CONTRADICTION",
            {item.code for item in report.findings},
        )

    def test_legacy_missing_routing_proof_is_incomplete(self) -> None:
        temporary, root = self._fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record.pop("shadow_only", None)
        _write_jsonl(manifest_path, records)
        _capture_fixture_trust(root)
        report = self._audit(root)
        self.assertEqual(report.status, "INCOMPLETE", report.to_json())
        self.assertIn(
            "LEGACY_PROFILE_INCOMPLETE",
            {item.code for item in report.findings},
        )

    def test_legacy_shadow_reverse_seal_link_contradiction_fails(self) -> None:
        temporary, root = self._shadow_fixture()
        self.addCleanup(temporary.cleanup)
        manifest_path = root / "00a_context_and_resource_manifest.jsonl"
        records = _read_jsonl(manifest_path, [])
        for record in records:
            record.pop("_line", None)
            if record.get("record_type") == "run":
                record["live_arm_freeze_seal_sha256"] = "f" * 64
        _write_jsonl(manifest_path, records)
        _capture_fixture_trust(root)
        report = self._audit(root)
        self.assertEqual(report.status, "FAIL", report.to_json())
        self.assertIn(
            "LEGACY_SHADOW_LINK_CONTRADICTION",
            {item.code for item in report.findings},
        )


def _read_pinned_external_json(
    path: Path,
    expected_sha256: str,
    run_dir: Path,
) -> tuple[dict[str, Any], str]:
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("external snapshot pin must be a lowercase SHA-256 digest")
    if path.is_symlink() or not path.is_file():
        raise ValueError("external snapshot must be an existing regular non-symlink file")
    resolved = path.resolve()
    if _is_within(resolved, run_dir.resolve()):
        raise ValueError("external snapshot must live outside the run directory")
    data = resolved.read_bytes()
    if len(data) > 1_000_000:
        raise ValueError("external snapshot exceeds the 1 MB trust-input limit")
    observed = hashlib.sha256(data).hexdigest()
    if observed != expected_sha256:
        raise ValueError("external snapshot does not match the independently supplied SHA-256 pin")
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ValueError(f"external snapshot is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("external snapshot JSON must be an object")
    try:
        canonical_data = _json_bytes(payload)
    except (RecursionError, ValueError) as exc:
        raise ValueError(f"external snapshot nesting is unsupported: {exc}") from exc
    if data != canonical_data:
        raise ValueError("external snapshot must use the canonical sorted JSON encoding emitted by this auditor")
    return payload, observed


def _write_external_snapshot(path: Path, payload: dict[str, Any], run_dir: Path) -> str:
    if path.exists() or path.is_symlink():
        raise ValueError("refusing to overwrite an existing external snapshot")
    resolved_parent = path.parent.resolve()
    if _is_within(resolved_parent, run_dir.resolve()):
        raise ValueError("external snapshot must be created outside the run directory")
    data = _json_bytes(payload)
    with path.open("xb") as handle:
        handle.write(data)
    return hashlib.sha256(data).hexdigest()


def _load_or_create_v2_manifest_snapshot(
    run_dir: Path,
) -> tuple[list[dict[str, Any]], str]:
    """Create the canonical raw-byte manifest snapshot once, or verify and reuse it."""
    manifest_parsed = _strict_run_file(
        run_dir,
        "00a_context_and_resource_manifest.jsonl",
        set(),
    )
    if manifest_parsed is None:
        raise ValueError("V2 manifest must be a regular non-symlink run-local file")
    manifest_path = manifest_parsed[0]
    snapshot_path = run_dir / PREFREEZE_MANIFEST_SNAPSHOT_V2
    if snapshot_path.is_symlink():
        raise ValueError("pre-freeze manifest snapshot must not be a symlink")
    if snapshot_path.exists():
        if not snapshot_path.is_file():
            raise ValueError("pre-freeze manifest snapshot must be a regular file")
        try:
            if snapshot_path.stat().st_dev == manifest_path.stat().st_dev and snapshot_path.stat().st_ino == manifest_path.stat().st_ino:
                raise ValueError("pre-freeze manifest snapshot must be an independent raw-byte copy, not a hard link")
        except OSError as exc:
            raise ValueError(f"cannot verify existing pre-freeze manifest snapshot: {exc}") from exc
        data = snapshot_path.read_bytes()
    else:
        data = manifest_path.read_bytes()
        with snapshot_path.open("xb") as handle:
            handle.write(data)
    parsed = _strict_run_file(run_dir, PREFREEZE_MANIFEST_SNAPSHOT_V2, set())
    if parsed is None:
        raise ValueError("pre-freeze manifest snapshot escaped its run or became non-regular")
    observed_data = parsed[0].read_bytes()
    if observed_data != data:
        raise ValueError("pre-freeze manifest snapshot changed while it was being certified")
    findings: list[Finding] = []
    records = _read_jsonl(parsed[0], findings)
    if findings:
        raise ValueError("pre-freeze manifest snapshot is not valid typed JSONL")
    return records, hashlib.sha256(observed_data).hexdigest()


def _create_protection_anchor_payload(run_dir: Path) -> dict[str, Any]:
    findings: list[Finding] = []
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = _read_jsonl(manifest_path, findings)
    if findings:
        raise ValueError("cannot create protection anchor from an invalid manifest")
    run_records = [record for record in records if record.get("record_type") == "run"]
    if len(run_records) != 1:
        raise ValueError("protection anchor creation needs exactly one run record")
    run_record = run_records[0]
    anchor_files: list[dict[str, Any]] = []
    observed_ids: set[str] = set()
    for item in run_record.get("protected_files", []):
        if not isinstance(item, dict):
            raise ValueError("protected_files entries must be objects")
        contract_id = _required_file_id(item.get("path"))
        if contract_id is None or contract_id in observed_ids:
            raise ValueError("protected file inventory has an unknown or duplicate contract")
        unresolved_path = Path(str(item.get("path")))
        if not unresolved_path.is_absolute():
            unresolved_path = run_dir / unresolved_path
        if _has_symlink_component(unresolved_path):
            raise ValueError("fixed contracts must not be symlinks")
        path = unresolved_path.resolve()
        if _is_within(path, run_dir) or not path.is_file():
            raise ValueError("fixed contracts must be regular canonical files outside the run directory")
        observed_ids.add(contract_id)
        anchor_files.append({"id": contract_id, "path": str(path), "sha256": _sha256(path)})
    if observed_ids != set(DEFAULT_PROTECTED_FILE_PATHS):
        raise ValueError("protected file inventory does not contain the complete fixed-contract profile")

    anchor_blocks: list[dict[str, Any]] = []
    observed_block_ids: set[str] = set()
    for item in run_record.get("protected_blocks", []):
        if not isinstance(item, dict):
            raise ValueError("protected_blocks entries must be objects")
        marker_pair = (item.get("start_marker"), item.get("end_marker"))
        block_ids = [
            block_id
            for block_id, expected in REQUIRED_PROTECTED_BLOCK_IDS.items()
            if marker_pair == expected
        ]
        if len(block_ids) != 1 or block_ids[0] in observed_block_ids:
            raise ValueError("protected block inventory has an unknown or duplicate marker pair")
        block_id = block_ids[0]
        unresolved_path = Path(str(item.get("path")))
        if not unresolved_path.is_absolute():
            unresolved_path = run_dir / unresolved_path
        if _has_symlink_component(unresolved_path):
            raise ValueError("protected block files must not be symlinks")
        path = unresolved_path.resolve()
        if _is_within(path, run_dir) or not path.is_file():
            raise ValueError("protected blocks must bind canonical files outside the run directory")
        if path != Path(
            DEFAULT_PROTECTED_FILE_PATHS["orchestration-prompt"]
        ).resolve(strict=False):
            raise ValueError("protected validation block must bind the exact canonical orchestration prompt")
        block_hash = _marker_block_sha256(path, marker_pair[0], marker_pair[1])
        if block_hash is None:
            raise ValueError("protected block markers are absent, repeated, or reversed")
        observed_block_ids.add(block_id)
        anchor_blocks.append(
            {
                "id": block_id,
                "path": str(path),
                "start_marker": marker_pair[0],
                "end_marker": marker_pair[1],
                "sha256": block_hash,
            }
        )
    if observed_block_ids != set(REQUIRED_PROTECTED_BLOCK_IDS):
        raise ValueError("protected block inventory does not contain the complete fixed-contract profile")
    is_v2 = run_record.get("schema") == RUN_SCHEMA_V2
    if is_v2:
        contract_path_value = run_record.get("development_contract_path")
        contract_digest = run_record.get("development_contract_sha256")
        parsed_contract = _strict_run_file(run_dir, contract_path_value, set())
        if (
            contract_path_value != "00b_development_contract.json"
            or parsed_contract is None
            or not isinstance(contract_digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", contract_digest)
            or _sha256(parsed_contract[0]) != contract_digest
        ):
            raise ValueError(
                "V2 protection anchor creation requires the exact regular run-local development contract path and matching raw-byte SHA-256"
            )
    payload: dict[str, Any] = {
        "schema": PROTECTION_ANCHOR_SCHEMA_V2 if is_v2 else PROTECTION_ANCHOR_SCHEMA,
        "contract_profile": CONTRACT_PROFILE,
        "run_id": run_dir.name,
        "run_dir": str(run_dir.resolve()),
        "created_at": datetime.now().astimezone().isoformat(),
        "block_semantics": "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1",
        "files": sorted(anchor_files, key=lambda item: item["id"]),
        "blocks": sorted(anchor_blocks, key=lambda item: item["id"]),
    }
    if is_v2:
        workflow_files: list[dict[str, str]] = []
        for workflow_id, raw_path in WORKFLOW_PROFILE_FILE_PATHS_V2.items():
            path = Path(raw_path)
            if _has_symlink_component(path) or not path.is_file() or _is_within(path, run_dir):
                raise ValueError(f"workflow profile file {workflow_id} is not a canonical external regular file")
            workflow_files.append(
                {"id": workflow_id, "path": raw_path, "sha256": _sha256(path)}
            )
        payload.update(
            {
                "scope_id": run_record.get("scope_id"),
                "development_contract_path": "00b_development_contract.json",
                "development_contract_sha256": contract_digest,
                "workflow_profile": WORKFLOW_PROFILE_V2,
                "workflow_files": sorted(workflow_files, key=lambda item: item["id"]),
            }
        )
    return payload


def _create_freeze_seal_payload(
    run_dir: Path,
    protection_anchor: dict[str, Any],
    protection_anchor_sha256: str,
) -> dict[str, Any]:
    if protection_anchor.get("run_id") != run_dir.name or protection_anchor.get("run_dir") != str(run_dir.resolve()):
        raise ValueError("protection anchor belongs to another run")
    findings: list[Finding] = []
    manifest_records = _read_jsonl(
        run_dir / "00a_context_and_resource_manifest.jsonl", findings
    )
    records = _read_jsonl(run_dir / "02b_raw_to_direction_ledger.jsonl", findings)
    if findings:
        raise ValueError("cannot create freeze seal from an invalid provenance ledger")
    run_records = [
        record for record in manifest_records if record.get("record_type") == "run"
    ]
    if len(run_records) != 1:
        raise ValueError("freeze seal creation needs exactly one run record")
    run_record = run_records[0]
    is_v2 = run_record.get("schema") == RUN_SCHEMA_V2
    seal_run_record = run_record
    manifest_snapshot_sha256: str | None = None
    snapshot_frozen_at: datetime | None = None
    terminal_complete_at: datetime | None = None
    if is_v2:
        snapshot_records, manifest_snapshot_sha256 = (
            _load_or_create_v2_manifest_snapshot(run_dir)
        )
        snapshot_run_records = [
            record
            for record in snapshot_records
            if record.get("record_type") == "run"
        ]
        if len(snapshot_run_records) != 1:
            raise ValueError(
                "pre-freeze manifest snapshot needs exactly one run record"
            )
        seal_run_record = snapshot_run_records[0]
        if seal_run_record.get("_line") != 1 or run_record.get("_line") != 1:
            raise ValueError("V2 run records must be the first line of their manifests")
        if _v2_immutable_run_view(seal_run_record) != _v2_immutable_run_view(run_record):
            raise ValueError(
                "final manifest changed immutable pre-freeze run identity, selection, wave, lineage, seed, budget, or live-seal pin"
            )
        snapshot_lines = (run_dir / PREFREEZE_MANIFEST_SNAPSHOT_V2).read_bytes().splitlines(keepends=True)
        final_lines = (run_dir / "00a_context_and_resource_manifest.jsonl").read_bytes().splitlines(keepends=True)
        snapshot_run_index = int(seal_run_record.get("_line", 0)) - 1
        final_run_index = int(run_record.get("_line", 0)) - 1
        snapshot_nonrun = [line for index, line in enumerate(snapshot_lines) if index != snapshot_run_index]
        final_nonrun = [line for index, line in enumerate(final_lines) if index != final_run_index]
        if (
            not snapshot_lines
            or not final_lines
            or any(not line.strip() for line in snapshot_lines + final_lines)
            or len(final_nonrun) < len(snapshot_nonrun)
            or snapshot_nonrun != final_nonrun[: len(snapshot_nonrun)]
        ):
            raise ValueError(
                "pre-freeze manifest research/checkpoint lines must remain a byte-identical ordered prefix"
            )
        if (
            seal_run_record.get("lifecycle_state") != "frozen"
            or seal_run_record.get("status") != "frozen"
        ):
            raise ValueError(
                "V2 freeze sealing requires lifecycle_state=status=frozen in the immutable snapshot"
            )

        snapshot_checkpoints = [
            record
            for record in snapshot_records
            if record.get("record_type") == "checkpoint"
        ]
        expected_chain = (
            SHADOW_STATE_CHAIN_V2
            if seal_run_record.get("mode") == "archipelago_lite_shadow"
            else LIVE_STATE_CHAIN_V2
        )
        if [record.get("state") for record in snapshot_checkpoints] != list(
            expected_chain[:-1]
        ):
            raise ValueError(
                "V2 pre-freeze snapshot must contain the exact checkpoint prefix through frozen"
            )
        previous_checkpoint_id: str | None = None
        previous_checkpoint_time: datetime | None = None
        for checkpoint_record in snapshot_checkpoints:
            checkpoint_time = _parse_timestamp(checkpoint_record.get("occurred_at"))
            if (
                set(checkpoint_record) - {"_line"} != V2_CHECKPOINT_FIELDS
                or checkpoint_record.get("predecessor_id")
                not in ((None, "") if previous_checkpoint_id is None else (previous_checkpoint_id,))
                or checkpoint_time is None
                or (
                    previous_checkpoint_time is not None
                    and checkpoint_time <= previous_checkpoint_time
                )
            ):
                raise ValueError(
                    "V2 pre-freeze checkpoint prefix has invalid fields, predecessor, or chronology"
                )
            previous_checkpoint_id = checkpoint_record.get("checkpoint_id")
            if not isinstance(previous_checkpoint_id, str) or not previous_checkpoint_id:
                raise ValueError("V2 pre-freeze checkpoints need stable checkpoint IDs")
            previous_checkpoint_time = checkpoint_time
        snapshot_frozen_at = previous_checkpoint_time
        if snapshot_frozen_at is None:
            raise ValueError("V2 pre-freeze snapshot has no frozen checkpoint time")

        snapshot_declarations = seal_run_record.get("declared_child_scopes")
        final_declarations = run_record.get("declared_child_scopes")
        if not isinstance(snapshot_declarations, list) or not isinstance(
            final_declarations, list
        ):
            raise ValueError(
                "V2 snapshot and final manifests need typed child declaration lists"
            )
        preregistered_by_scope: dict[str, dict[str, Any]] = {}
        for declaration in snapshot_declarations:
            if (
                not isinstance(declaration, dict)
                or set(declaration) != CHILD_DECLARATION_FIELDS_V2
                or any(
                    declaration.get(key) is not None
                    for key in CHILD_FINALIZATION_FIELDS_V2
                )
            ):
                raise ValueError(
                    "V2 pre-freeze child declarations must use the exact schema with null fill-once finalization fields"
                )
            child_scope_id = declaration.get("scope_id")
            if (
                not isinstance(child_scope_id, str)
                or not child_scope_id
                or child_scope_id in preregistered_by_scope
            ):
                raise ValueError("V2 child preregistrations need unique stable scope IDs")
            preregistered_by_scope[child_scope_id] = declaration
        finalized_by_scope = {
            declaration.get("scope_id"): declaration
            for declaration in final_declarations
            if isinstance(declaration, dict)
            and isinstance(declaration.get("scope_id"), str)
        }
        if (
            len(finalized_by_scope) != len(final_declarations)
            or set(finalized_by_scope) != set(preregistered_by_scope)
        ):
            raise ValueError(
                "final child declarations must materialize only the pre-freeze registrations"
            )
        for child_scope_id, preregistration in preregistered_by_scope.items():
            final_declaration = finalized_by_scope[child_scope_id]
            immutable_preregistration = {
                key: value
                for key, value in preregistration.items()
                if key not in CHILD_FINALIZATION_FIELDS_V2
            }
            immutable_final = {
                key: value
                for key, value in final_declaration.items()
                if key not in CHILD_FINALIZATION_FIELDS_V2
            }
            if (
                set(final_declaration) != CHILD_DECLARATION_FIELDS_V2
                or immutable_preregistration != immutable_final
            ):
                raise ValueError(
                    "final child declarations may fill only the locked post-audit fields"
                )

        appended_records = [
            record
            for record in manifest_records
            if isinstance(record.get("_line"), int)
            and record.get("_line") > len(snapshot_nonrun) + 1
        ]
        if run_record.get("lifecycle_state") == "frozen" and run_record.get("status") == "frozen":
            if appended_records:
                raise ValueError("a frozen final manifest cannot append post-seal records")
        elif run_record.get("lifecycle_state") == "complete" and run_record.get("status") == "complete":
            if len(appended_records) != 1:
                raise ValueError(
                    "a completed final manifest must append exactly one terminal complete checkpoint"
                )
            terminal = appended_records[0]
            terminal_complete_at = _parse_timestamp(terminal.get("occurred_at"))
            if (
                terminal.get("record_type") != "checkpoint"
                or set(terminal) - {"_line"} != V2_CHECKPOINT_FIELDS
                or terminal.get("state") != "complete"
                or terminal.get("predecessor_id") != previous_checkpoint_id
                or terminal_complete_at is None
                or terminal_complete_at <= snapshot_frozen_at
            ):
                raise ValueError(
                    "the only post-snapshot record must be the exact later terminal complete checkpoint"
                )
        else:
            raise ValueError(
                "the final V2 manifest must be frozen or have only the allowed terminal complete materialization"
            )
    excluded_roots = _declared_child_relative_paths(run_dir, run_record) if is_v2 else set()
    finalists: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    frozen_times: list[datetime] = []
    for record in records:
        if record.get("record_type") != "finalist":
            continue
        finalist_id = record.get("finalist_id")
        if not isinstance(finalist_id, str) or finalist_id in seen_ids:
            raise ValueError("freeze seal needs unique stable finalist IDs")
        if is_v2:
            strict_artifact = _strict_run_file(
                run_dir, record.get("artifact_path"), excluded_roots
            )
            path, relative = strict_artifact if strict_artifact is not None else (None, None)
        else:
            path, relative = _canonical_run_path(run_dir, record.get("artifact_path"))
        unresolved = run_dir / str(record.get("artifact_path"))
        if path is None or relative is None or unresolved.is_symlink() or not path.is_file():
            raise ValueError("freeze seal finalist paths must be regular files inside the run directory")
        digest = _sha256(path)
        if record.get("sha256") != digest:
            raise ValueError("freeze seal refuses a finalist whose ledger hash does not match")
        frozen_at = _parse_timestamp(record.get("frozen_at"))
        if frozen_at is None:
            raise ValueError("freeze seal finalists need offset-aware frozen_at timestamps")
        seen_ids.add(finalist_id)
        frozen_times.append(frozen_at)
        finalists.append(
            {
                "finalist_id": finalist_id,
                "arm": record.get("arm"),
                "artifact_path": relative,
                "frozen_at": record.get("frozen_at"),
                "sha256": digest,
            }
        )
    if not finalists:
        raise ValueError("freeze seal needs at least one frozen finalist")
    now = datetime.now().astimezone()
    seal_predecessors = list(frozen_times)
    if snapshot_frozen_at is not None:
        seal_predecessors.append(snapshot_frozen_at)
    sealed_at = max(now, max(seal_predecessors) + timedelta(microseconds=1))
    if terminal_complete_at is not None and sealed_at >= terminal_complete_at:
        raise ValueError(
            "freeze seal creation must occur strictly before an already appended terminal complete checkpoint"
        )
    payload: dict[str, Any] = {
        "schema": FREEZE_SEAL_SCHEMA_V2 if is_v2 else FREEZE_SEAL_SCHEMA,
        "run_id": run_dir.name,
        "run_dir": str(run_dir.resolve()),
        "protection_anchor_sha256": protection_anchor_sha256,
        "mode": seal_run_record.get("mode"),
        "matched_pilot": seal_run_record.get("matched_pilot") is True,
        "model": seal_run_record.get("model"),
        "reasoning_effort": seal_run_record.get("reasoning_effort"),
        "sealed_at": sealed_at.isoformat(),
        "finalists": sorted(finalists, key=lambda item: item["finalist_id"]),
    }
    if is_v2:
        if protection_anchor.get("schema") != PROTECTION_ANCHOR_SCHEMA_V2:
            raise ValueError("a V2 freeze seal requires a V2 protection anchor")
        anchor_schema_findings: list[Finding] = []
        _validate_v2_protection_anchor_fields(
            protection_anchor, anchor_schema_findings
        )
        if anchor_schema_findings:
            raise ValueError(
                "a V2 freeze seal requires the exact closed V2 protection-anchor schema"
            )
        payload.update(
            {
                "run_profile": seal_run_record.get("run_profile"),
                "scope_id": seal_run_record.get("scope_id"),
                "arm": seal_run_record.get("arm"),
                "routing_state": seal_run_record.get("routing_state"),
                "cohort_kind": seal_run_record.get("cohort_kind"),
                "wave_index": seal_run_record.get("wave_index"),
                "selection_policy": seal_run_record.get("selection_policy"),
                "seed": seal_run_record.get("seed"),
                "candidate_order_seed": seal_run_record.get(
                    "candidate_order_seed"
                ),
                "parent_scope_id": seal_run_record.get("parent_scope_id"),
                "matched_pilot": seal_run_record.get("run_profile")
                in {
                    "operational_live_with_shadow",
                    "v2_matched_nonrouting",
                },
                "results_visibility": seal_run_record.get("results_visibility"),
                "manifest_snapshot_path": PREFREEZE_MANIFEST_SNAPSHOT_V2,
                "manifest_snapshot_sha256": manifest_snapshot_sha256,
                "development_contract_sha256": seal_run_record.get(
                    "development_contract_sha256"
                ),
            }
        )
        if seal_run_record.get("cohort_kind") == "regeneration":
            payload.update(
                {
                    "parent_scope_id": seal_run_record.get("parent_scope_id"),
                    "initial_freeze_seal_sha256": seal_run_record.get(
                        "initial_freeze_seal_sha256"
                    ),
                }
            )
        if seal_run_record.get("arm") == "shadow":
            payload["live_arm_freeze_seal_sha256"] = seal_run_record.get(
                "live_arm_freeze_seal_sha256"
            )
        seal_schema_findings: list[Finding] = []
        _validate_v2_freeze_seal_fields(
            payload,
            seal_schema_findings,
            expected_arm=seal_run_record.get("arm"),
            expected_cohort_kind=seal_run_record.get("cohort_kind"),
        )
        if seal_schema_findings:
            raise ValueError(
                "created V2 freeze seal does not satisfy the exact closed schema"
            )
    return payload
def run_self_test() -> int:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(SelfTest))
    integration_dir = Path(__file__).resolve().parent.parent / "tests"
    integration_file = integration_dir / "test_live_shadow_integration.py"
    if integration_file.is_file():
        integration_path = str(integration_dir)
        inserted = integration_path not in sys.path
        if inserted:
            sys.path.insert(0, integration_path)
        try:
            suite.addTests(
                loader.discover(
                    integration_path,
                    pattern=integration_file.name,
                    top_level_dir=integration_path,
                )
            )
        finally:
            if inserted:
                sys.path.remove(integration_path)
    stream = io.StringIO()
    with contextlib.redirect_stderr(stream):
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(stream.getvalue(), end="")
    return 0 if result.wasSuccessful() else 1


def _print_report(report: AuditReport, as_json: bool) -> None:
    if as_json:
        print(report.to_json())
        return
    print(f"{report.status}: {report.run_id} ({report.adapter})")
    print(
        f"Counts: raw={report.counts.get('raw', 0)}, "
        f"directions={report.counts.get('directions', 'unknown')}, "
        f"finalists={report.counts.get('finalists', 'unknown')}"
    )
    for item in report.findings:
        location = item.artifact
        if item.line:
            location = f"{location}:{item.line}"
        prefix = f"[{item.severity}] {item.code}"
        if location:
            prefix += f" ({location})"
        print(f"{prefix}: {item.message}")


def _exit_code(report: AuditReport) -> int:
    if report.status == "FAIL":
        return 1
    if report.status == "INCOMPLETE":
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--august-initial-snapshot",
        "--legacy-august",
        dest="legacy_august",
        action="store_true",
        help="Conservatively inspect the August initial pool without treating prose mentions as ancestry.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true")
    creation_group = parser.add_mutually_exclusive_group()
    creation_group.add_argument("--create-protection-anchor", type=Path)
    creation_group.add_argument("--create-freeze-seal", type=Path)
    parser.add_argument("--protection-anchor", type=Path)
    parser.add_argument("--protection-anchor-sha256")
    parser.add_argument("--child-protection-anchor", type=Path)
    parser.add_argument("--child-protection-anchor-sha256")
    parser.add_argument("--freeze-seal", type=Path)
    parser.add_argument("--freeze-seal-sha256")
    parser.add_argument("--live-arm-freeze-seal", type=Path)
    parser.add_argument("--live-arm-freeze-seal-sha256")
    parser.add_argument("--initial-freeze-seal", type=Path)
    parser.add_argument("--initial-freeze-seal-sha256")
    parser.add_argument("--child-trust-bundle", type=Path)
    parser.add_argument("--child-trust-bundle-sha256")
    parser.add_argument("--checkpoint", choices=sorted(AUDIT_CHECKPOINTS))
    args = parser.parse_args(argv)

    child_protection_requested = (
        args.child_protection_anchor is not None
        or args.child_protection_anchor_sha256 is not None
    )
    child_protection_pair_complete = (
        args.child_protection_anchor is not None
        and args.child_protection_anchor_sha256 is not None
    )
    if args.self_test:
        if child_protection_requested:
            print(
                "TRUST_INPUT_ERROR: child protection-anchor inputs are not valid with --self-test",
                file=sys.stderr,
            )
            return 3
        return run_self_test()
    if args.run_dir is None:
        parser.error("run_dir is required unless --self-test is used")
    if not args.run_dir.is_dir():
        parser.error(f"run_dir is not a directory: {args.run_dir}")

    run_dir = args.run_dir.resolve()
    creation_requested = (
        args.create_protection_anchor is not None
        or args.create_freeze_seal is not None
    )
    if child_protection_requested and not child_protection_pair_complete:
        print(
            "TRUST_INPUT_ERROR: --child-protection-anchor and --child-protection-anchor-sha256 must be supplied together",
            file=sys.stderr,
        )
        return 3
    if child_protection_requested and (
        args.checkpoint != "shadow-dispatch"
        or args.legacy_august
        or creation_requested
    ):
        print(
            "TRUST_INPUT_ERROR: --child-protection-anchor is valid only for a shadow-dispatch audit",
            file=sys.stderr,
        )
        return 3
    if (
        args.checkpoint == "shadow-dispatch"
        and not args.legacy_august
        and not creation_requested
        and not child_protection_pair_complete
    ):
        print(
            "TRUST_INPUT_ERROR: shadow-dispatch requires --child-protection-anchor and --child-protection-anchor-sha256",
            file=sys.stderr,
        )
        return 3

    if args.create_protection_anchor is not None:
        try:
            payload = _create_protection_anchor_payload(run_dir)
            digest = _write_external_snapshot(
                args.create_protection_anchor,
                payload,
                run_dir,
            )
        except (OSError, ValueError) as exc:
            print(f"ANCHOR_CREATION_ERROR: {exc}", file=sys.stderr)
            return 3
        print(f"PROTECTION_ANCHOR_SHA256={digest}")
        return 0

    protection_anchor: dict[str, Any] | None = None
    protection_digest: str | None = None
    if args.protection_anchor is not None or args.protection_anchor_sha256 is not None:
        if args.protection_anchor is None or args.protection_anchor_sha256 is None:
            print("TRUST_INPUT_ERROR: --protection-anchor and --protection-anchor-sha256 must be supplied together", file=sys.stderr)
            return 3
        try:
            protection_anchor, protection_digest = _read_pinned_external_json(
                args.protection_anchor,
                args.protection_anchor_sha256,
                run_dir,
            )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    child_protection_anchor: dict[str, Any] | None = None
    child_protection_digest: str | None = None
    if child_protection_pair_complete:
        assert args.child_protection_anchor is not None
        assert args.child_protection_anchor_sha256 is not None
        try:
            if _has_symlink_component(args.child_protection_anchor):
                raise ValueError(
                    "child protection-anchor path must not contain any symlink component"
                )
            child_protection_anchor, child_protection_digest = (
                _read_pinned_external_json(
                    args.child_protection_anchor,
                    args.child_protection_anchor_sha256,
                    run_dir,
                )
            )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    if args.create_freeze_seal is not None:
        if protection_anchor is None or protection_digest is None:
            print("SEAL_CREATION_ERROR: a pinned external protection anchor is required", file=sys.stderr)
            return 3
        try:
            payload = _create_freeze_seal_payload(
                run_dir,
                protection_anchor,
                protection_digest,
            )
            digest = _write_external_snapshot(
                args.create_freeze_seal,
                payload,
                run_dir,
            )
        except (OSError, ValueError) as exc:
            print(f"SEAL_CREATION_ERROR: {exc}", file=sys.stderr)
            return 3
        print(f"FREEZE_SEAL_SHA256={digest}")
        return 0

    freeze_seal: dict[str, Any] | None = None
    freeze_digest: str | None = None
    if args.freeze_seal is not None or args.freeze_seal_sha256 is not None:
        if args.freeze_seal is None or args.freeze_seal_sha256 is None:
            print("TRUST_INPUT_ERROR: --freeze-seal and --freeze-seal-sha256 must be supplied together", file=sys.stderr)
            return 3
        try:
            freeze_seal, freeze_digest = _read_pinned_external_json(
                args.freeze_seal,
                args.freeze_seal_sha256,
                run_dir,
            )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    live_arm_freeze_seal: dict[str, Any] | None = None
    live_arm_freeze_digest: str | None = None
    if (
        args.live_arm_freeze_seal is not None
        or args.live_arm_freeze_seal_sha256 is not None
    ):
        if (
            args.live_arm_freeze_seal is None
            or args.live_arm_freeze_seal_sha256 is None
        ):
            print("TRUST_INPUT_ERROR: --live-arm-freeze-seal and --live-arm-freeze-seal-sha256 must be supplied together", file=sys.stderr)
            return 3
        try:
            live_arm_freeze_seal, live_arm_freeze_digest = _read_pinned_external_json(
                args.live_arm_freeze_seal,
                args.live_arm_freeze_seal_sha256,
                run_dir,
            )
            live_run_dir_value = live_arm_freeze_seal.get("run_dir")
            if (
                isinstance(live_run_dir_value, str)
                and Path(live_run_dir_value).is_absolute()
                and _is_within(
                    args.live_arm_freeze_seal.resolve(),
                    Path(live_run_dir_value).resolve(strict=False),
                )
            ):
                raise ValueError(
                    "live-arm freeze seal must live outside the live run directory it attests"
                )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    initial_freeze_seal: dict[str, Any] | None = None
    initial_freeze_digest: str | None = None
    if (
        args.initial_freeze_seal is not None
        or args.initial_freeze_seal_sha256 is not None
    ):
        if (
            args.initial_freeze_seal is None
            or args.initial_freeze_seal_sha256 is None
        ):
            print(
                "TRUST_INPUT_ERROR: --initial-freeze-seal and --initial-freeze-seal-sha256 must be supplied together",
                file=sys.stderr,
            )
            return 3
        try:
            initial_freeze_seal, initial_freeze_digest = _read_pinned_external_json(
                args.initial_freeze_seal,
                args.initial_freeze_seal_sha256,
                run_dir,
            )
            initial_run_dir_value = initial_freeze_seal.get("run_dir")
            if (
                isinstance(initial_run_dir_value, str)
                and Path(initial_run_dir_value).is_absolute()
                and _is_within(
                    args.initial_freeze_seal.resolve(),
                    Path(initial_run_dir_value).resolve(strict=False),
                )
            ):
                raise ValueError(
                    "initial freeze seal must live outside the initial run directory it attests"
                )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    child_trust_bundle: dict[str, Any] | None = None
    child_trust_digest: str | None = None
    if (
        args.child_trust_bundle is not None
        or args.child_trust_bundle_sha256 is not None
    ):
        if (
            args.child_trust_bundle is None
            or args.child_trust_bundle_sha256 is None
        ):
            print("TRUST_INPUT_ERROR: --child-trust-bundle and --child-trust-bundle-sha256 must be supplied together", file=sys.stderr)
            return 3
        try:
            child_trust_bundle, child_trust_digest = _read_pinned_external_json(
                args.child_trust_bundle,
                args.child_trust_bundle_sha256,
                run_dir,
            )
        except (OSError, ValueError) as exc:
            print(f"TRUST_INPUT_ERROR: {exc}", file=sys.stderr)
            return 3

    try:
        report = (
            audit_legacy_august(args.run_dir, args.strict)
            if args.legacy_august
            else audit_run(
                args.run_dir,
                args.strict,
                protection_anchor=protection_anchor,
                protection_anchor_sha256=protection_digest,
                child_protection_anchor=child_protection_anchor,
                child_protection_anchor_sha256=child_protection_digest,
                freeze_seal=freeze_seal,
                freeze_seal_sha256=freeze_digest,
                live_arm_freeze_seal=live_arm_freeze_seal,
                live_arm_freeze_seal_sha256=live_arm_freeze_digest,
                initial_freeze_seal=initial_freeze_seal,
                initial_freeze_seal_sha256=initial_freeze_digest,
                child_trust_bundle=child_trust_bundle,
                child_trust_bundle_sha256=child_trust_digest,
                checkpoint=args.checkpoint,
            )
        )
    except Exception as exc:  # pragma: no cover - last-resort CLI containment
        print(f"INTERNAL_ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 4
    _print_report(report, args.as_json)
    return _exit_code(report)


if __name__ == "__main__":
    sys.exit(main())
