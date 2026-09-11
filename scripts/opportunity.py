#!/usr/bin/env python3
"""Deterministic state and artifact utility for the opportunity workflow.

This program deliberately does not orchestrate agents.  Codex owns creative and
research work; this utility owns the small deterministic boundary around it:
validation, scoring, immutable artifacts, retries, state transitions, external
handoffs, and publication.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
import tempfile
import unicodedata
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Iterator, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "opportunity-workflow.json"
DEFAULT_RUNS_DIR = REPO_ROOT / "runs"
ACTIVE_SCHEMA_VERSION = 3
LEGACY_PUBLISHED_SCHEMA_VERSION = 2

STAGES = (
    "initialized",
    "discovery",
    "calibration",
    "research",
    "development",
    "frozen",
    "holdout",
    "complete",
)
CANDIDATE_STAGES = ("discovery", "development")
RUN_STATUSES = {"active", "qualified", "no_finalist", "no_qualifier", "contested", "failed"}
CAMPAIGN_STATUSES = {"active", "qualified", "plateau", "max_cohorts"}
JOB_STATUSES = {"pending", "running", "completed", "failed", "interrupted", "skipped"}
RETRYABLE_JOB_STATUSES = {"pending", "failed", "interrupted"}
TERMINAL_JOB_STATUSES = {"completed", "skipped"}
ARTIFACT_KINDS = {
    "candidate",
    "research",
    "evaluation",
    "secondary-evaluation",
    "generic",
    "portfolio-selection",
    "portfolio-amendment",
    "portfolio-decision",
    "development-result",
}
PREFLIGHT_ARTIFACT_KINDS = ARTIFACT_KINDS - {"generic"}
LEGACY_CONFIG_KEYS_V2 = {
    "schema_version",
    "rubric_id",
    "threshold",
    "comparison",
    "scouts",
    "seeds_per_scout",
    "unique_min",
    "gap_scout_max",
    "dominant_structure_ratio",
    "similarity_flag_threshold",
    "shortlist_max",
    "develop_max",
    "finalists_max",
    "native_holdout_judges",
    "mechanical_attempts",
    "sources_min",
    "sources_max",
    "working_evaluators_per_candidate",
    "semantic_shortlist_min_archetypes",
    "semantic_shortlist_max_per_archetype",
    "campaign_min_cohorts",
    "campaign_max_cohorts",
    "campaign_plateau_patience",
    "campaign_official_improvement",
    "campaign_working_median_improvement",
    "campaign_novelty_score_gap",
}
LEGACY_CONFIG_KEYS_V3 = LEGACY_CONFIG_KEYS_V2 - {
    "dominant_structure_ratio",
    "semantic_shortlist_min_archetypes",
    "semantic_shortlist_max_per_archetype",
    "campaign_novelty_score_gap",
} | {
    "discovery_lanes",
    "core_shortlist_slots",
    "wildcard_shortlist_slots",
}
CONFIG_KEYS_V3 = LEGACY_CONFIG_KEYS_V3 - {
    "core_shortlist_slots",
    "wildcard_shortlist_slots",
} | {
    "screening_batches",
}
CONTROL_CONTRACT_CONFIG_KEYS = {
    "mechanism_first_founder_access_reserve",
    "secondary_screening_enabled",
    "secondary_screening_close_margin",
    "secondary_screening_candidates_per_side",
    "secondary_screening_aggregation",
    "development_evaluators_per_lineage",
    "development_score_aggregation",
}
CONFIG_KEYS_V3_CONTROL = CONFIG_KEYS_V3 | CONTROL_CONTRACT_CONFIG_KEYS
PREFLIGHT_ATTESTATION_VERSION = 1
PREFLIGHT_ATTESTATION_CONFIG_KEYS = {"preflight_attestation_version"}
CONFIG_KEYS_V3_ATTESTED = CONFIG_KEYS_V3_CONTROL | PREFLIGHT_ATTESTATION_CONFIG_KEYS
PREFLIGHT_RECEIPT_DOMAIN = "discussion-panel-preflight-v1"
PREFLIGHT_RECEIPT_KEYS = {
    "schema_version",
    "domain",
    "run_id",
    "manifest_sha256",
    "stage",
    "job_id",
    "kind",
    "input_sha256",
    "canonical_artifact_sha256",
    "receipt_sha256",
}
CONTROL_DISCOVERY_LANES = {
    "mechanism-first",
    "weak-signal",
    "future-backcast",
}
SOURCE_PATHS = (
    "PERSONALITY_SITUATION.md",
    "Personalities/ZeroToOne.txt",
    "config/opportunity-workflow.json",
)
INPUT_SNAPSHOTS = {
    "PERSONALITY_SITUATION.md": "inputs/founder.md",
    "Personalities/ZeroToOne.txt": "inputs/evaluator.txt",
    "config/opportunity-workflow.json": "inputs/config.json",
}
FACTOR_BASE_KEYS = {"name", "status", "score", "rationale"}
FACTOR_DERIVED_KEYS = {"original_weight", "effective_weight"}
CANDIDATE_KEYS = {
    "schema_version",
    "candidate_id",
    "version",
    "parent",
    "stage",
    "discovery_lane",
    "title",
    "thesis",
    "fingerprint",
    "founder_fit",
    "source_refs",
    "economics",
    "claims",
    "contrary_evidence",
    "uncertainties",
    "risks",
}
CANDIDATE_OPTIONAL_KEYS = {"redesign", "structure"}
STRUCTURE_KEYS = {"commercial_archetype", "control_point", "critical_dependency"}
REDESIGN_KEYS = {"changed_fingerprint_fields", "economic_effect"}
CANDIDATE_CONTROL_KEYS = {
    "critical_control_point",
    "commercial_mechanics",
    "structural_signature",
}
REDESIGN_CONTROL_KEYS = REDESIGN_KEYS | {"changed_structural_fields"}
STRUCTURAL_CHANGE_FIELDS = {
    "critical_control_point",
    "commercial_mechanics",
    "structural_signature",
}
CRITICAL_CONTROL_POINT_KEYS = {
    "subject_type",
    "subject",
    "current_owner",
    "launch_controller",
    "acquisition_instrument_type",
    "acquisition_instrument",
    "exclusivity",
    "duration",
    "revocability",
    "transferability",
    "renewal",
    "counterparty_refusal_fallback",
    "replaceability",
    "customer_relationship_owner",
    "customer_relationship_control",
    "mechanism_control",
    "status",
    "founder_access_basis",
    "founder_access_description",
    "confidential_employer_resource_dependency",
}
CONTROL_POINT_SUBJECT_TYPES = {
    "asset",
    "right",
    "workflow_position",
    "relationship",
    "capacity",
    "transaction",
    "dataset",
    "other",
}
CONTROL_POINT_STATUSES = {
    "owned",
    "exclusively_contracted",
    "durably_contracted",
    "replaceable_access",
    "externally_controlled",
    "unknown",
}
ACQUISITION_INSTRUMENT_TYPES = {
    "ownership",
    "exclusive_contract",
    "long_term_contract",
    "license",
    "purchase",
    "lease",
    "workflow_integration_agreement",
    "data_rights_agreement",
    "capacity_reservation",
    "distribution_agreement",
    "other",
    "unknown",
}
EXCLUSIVITY_STATUSES = {"exclusive", "nonexclusive", "not_applicable", "unknown"}
REVOCABILITY_STATUSES = {"irrevocable", "for_cause", "at_will", "not_applicable", "unknown"}
TRANSFERABILITY_STATUSES = {"transferable", "consent_required", "nontransferable", "not_applicable", "unknown"}
REPLACEABILITY_STATUSES = {"replaceable", "not_replaceable", "unknown"}
CUSTOMER_RELATIONSHIP_CONTROLS = {"owned", "contracted", "externally_owned", "unknown"}
MECHANISM_CONTROLS = {"owned", "dependent", "unknown"}
FOUNDER_ACCESS_BASES = {
    "owned_or_controlled_asset",
    "operating_relationship",
    "other_legally_usable_access",
    "none",
    "unknown",
}
FOUNDER_ACCESS_RESERVE_BASES = {
    "owned_or_controlled_asset",
    "operating_relationship",
    "other_legally_usable_access",
}
EMPLOYER_RESOURCE_DEPENDENCIES = {"none", "unknown", "present"}
COMMERCIAL_MECHANICS_KEYS = {
    "paid_event_or_measurable_loss",
    "payer",
    "budget_owner",
    "purchase_trigger",
    "renewal_event",
    "distribution_origin",
    "customer_relationship_owner",
    "fully_loaded_economics",
    "likely_incumbent_response",
    "bundling_resistance",
}
FULLY_LOADED_ECONOMICS_KEYS = {
    "revenue_basis",
    "variable_costs",
    "delivery_and_support_costs",
    "acquisition_cost",
    "overhead_and_compliance",
    "contribution_margin",
    "cash_conversion",
}
STRUCTURAL_SIGNATURE_KEYS = {
    "commercial_model_category",
    "commercial_model_descriptor",
    "control_point_category",
    "control_point_descriptor",
    "critical_dependency_category",
    "critical_dependency_descriptor",
}
COMMERCIAL_MODEL_CATEGORIES = {
    "software_subscription",
    "usage_based_service",
    "managed_service",
    "productized_service",
    "transaction_intermediation",
    "marketplace",
    "data_or_intelligence",
    "licensing_or_royalty",
    "capacity_or_asset_operator",
    "risk_transfer_or_financing",
    "other",
}
SIGNATURE_CONTROL_POINT_CATEGORIES = {
    "owned_asset",
    "exclusive_right",
    "contracted_capacity",
    "workflow_integration",
    "customer_relationship",
    "proprietary_dataset",
    "transaction_rail",
    "regulatory_authorization",
    "distribution_access",
    "operating_relationship",
    "other",
}
CRITICAL_DEPENDENCY_CATEGORIES = {
    "rights_holder",
    "data_provider",
    "distribution_channel",
    "capacity_provider",
    "regulatory_approval",
    "integration_platform",
    "specialist_labor",
    "capital_provider",
    "customer_adoption",
    "supply_partner",
    "none",
    "other",
}
PORTFOLIO_REF_KEYS = {"candidate_id", "version", "candidate_sha256"}
PORTFOLIO_SELECTION_KEYS = {
    "schema_version",
    "selection_version",
    "calibration",
    "candidate_refs",
    "wildcard_candidate_refs",
    "missing_archetypes",
    "rationale",
}
CALIBRATION_ROW_KEYS = {
    "candidate_ref",
    "commercial_archetype",
    "control_point",
    "critical_dependency",
    "control_point_acquisition_evidence",
}
CONTROL_POINT_ACQUISITION_EVIDENCE_KEYS = {
    "assessment",
    "acquisition_mode",
    "counterparty_or_source",
    "instrument_or_transaction",
    "founder_access_path",
    "claim_ids",
    "evidence_refs",
    "unresolved_preconditions",
    "credibility_rationale",
}
CONTROL_POINT_ACQUISITION_ASSESSMENTS = {
    "credible_preliminary",
    "under_evidenced",
}
CONTROL_POINT_ACQUISITION_MODES = {
    "owned_or_buildable_asset",
    "direct_purchase",
    "license",
    "commercial_contract",
    "delegated_authority",
    "embedded_workflow_agreement",
    "other_bounded_path",
}
PORTFOLIO_AMENDMENT_KEYS = {
    "schema_version",
    "amendment_version",
    "base_selection_sha256",
    "remove_candidate_ref",
    "add_candidate_ref",
    "reason",
}
PORTFOLIO_DECISION_KEYS = {"schema_version", "candidate_decisions"}
PORTFOLIO_CANDIDATE_DECISION_KEYS = {
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "disposition",
    "fatal_reason",
    "fatal_claim_ids",
    "rationale",
}
FATAL_RESEARCH_REASONS = {
    "illegality",
    "unobtainable_essential_rights",
    "impossible_conservative_economics",
    "nondelegable_founder_incompatibility",
}
DEVELOPMENT_RESULT_KEYS = {
    "schema_version",
    "candidate_id",
    "base_candidate_version",
    "base_candidate_sha256",
    "outcome",
    "final_candidate_version",
    "final_candidate_sha256",
    "constructor_id",
    "rationale",
    "falsification",
}
DEVELOPMENT_RESPONSE_KEYS = {
    "schema_version",
    "candidate_id",
    "outcome",
    "constructor_id",
    "rationale",
    "falsification",
}
DEVELOPMENT_CONTROL_KEY = "structural_change"
FINALIST_SELECTION_KEYS = {"schema_version", "candidate_refs"}
FINGERPRINT_KEYS = {
    "customer",
    "problem_trigger",
    "payer_and_paid_event",
    "offer_and_business_model",
    "distribution_mechanism",
    "compounding_advantage",
}
ECONOMICS_KEYS = {
    "pricing",
    "gross_margin_basis",
    "acquisition_route",
    "payback",
    "retention_or_repeat",
    "capital_required_pln",
    "founder_time",
    "founder_net_worth_path",
}
CLAIM_KEYS = {"claim_id", "claim_type", "statement", "evidence_refs", "confidence"}
CLAIM_TYPES = {
    "paid_event_or_measurable_loss",
    "payer_and_budget",
    "founder_control_point_path",
    "other",
}
CORE_READINESS_CLAIM_TYPES = CLAIM_TYPES - {"other"}
RESEARCH_KEYS = {
    "schema_version",
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "sources",
    "claims",
    "contrary_evidence",
    "unknowns",
    "falsification",
}
RESEARCH_SOURCE_KEYS = {
    "source_id",
    "url",
    "title",
    "publisher",
    "published_at",
    "accessed_at",
    "source_type",
    "evidence_class",
    "stance",
}
LEGACY_RESEARCH_SOURCE_KEYS = RESEARCH_SOURCE_KEYS - {"evidence_class"}
RESEARCH_CLAIM_KEYS = {"claim_id", "statement", "assessment", "evidence_refs"}
RESEARCH_CONTROL_KEYS = {"commercial_evidence", "critical_control_point_assessment"}
COMMERCIAL_EVIDENCE_SOURCE_CLASSES = {
    "buyer_or_paid_event": {"direct_buyer", "paid_event", "other"},
    "distribution_and_acquisition": {"distribution", "acquisition", "other"},
    "fully_loaded_unit_economics": {"unit_economics", "other"},
    "rights_control_access_contractibility": {
        "rights_control_access",
        "contracting",
        "other",
    },
}
COMMERCIAL_EVIDENCE_KEYS = set(COMMERCIAL_EVIDENCE_SOURCE_CLASSES)
COMMERCIAL_EVIDENCE_ITEM_KEYS = {"status", "claim_ids", "source_ids"}
COMMERCIAL_EVIDENCE_STATUSES = {"evidence", "inference", "unknown"}
EVIDENCE_CLASSES = {
    "direct_buyer",
    "paid_event",
    "distribution",
    "acquisition",
    "unit_economics",
    "rights_control_access",
    "contracting",
    "regulatory",
    "incumbent",
    "market_context",
    "other",
}
RESEARCH_CONTROL_ASSESSMENT_KEYS = {"status", "assessment", "claim_ids", "source_ids"}
FALSIFICATION_KEYS = {
    "control_point_obtainability",
    "substitutes_and_incumbent_response",
    "external_dependencies",
    "willingness_urgency_and_repeat_economics",
    "cold_start_and_data_moat",
    "critical_mechanism_ownership",
}
EVALUATOR_RESPONSE_KEYS = {
    "candidate_id",
    "candidate_version",
    "judge_id",
    "factors",
    "interaction_adjustment",
    "assumptions",
    "main_structural_strength",
    "primary_score_limiter",
    "strongest_disconfirming_evidence",
    "highest_value_structural_change",
    "evidence_needed_for_higher_score",
}
EVALUATION_IDENTITY_KEYS = {
    "schema_version",
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "rubric_id",
    "rubric_sha256",
    "judge_id",
    "evaluation_type",
}
EVALUATION_INPUT_KEYS = EVALUATOR_RESPONSE_KEYS | EVALUATION_IDENTITY_KEYS
EVALUATION_DERIVED_KEYS = {
    "base_score",
    "unrounded_score",
    "constrained_score",
    "final_score",
    "qualified",
}
EVALUATION_TYPES = {
    "working_screening",
    "working_screening_secondary",
    "working_research",
    "working_development",
    "holdout_native",
    "holdout_external",
}
SCREENING_BATCHES_KEYS = {"schema_version", "dedup_report_sha256", "batches"}
SCREENING_BATCH_KEYS = {"batch_id", "candidate_refs"}
SECONDARY_SCREENING_KEYS = {
    "schema_version",
    "screening_batches_sha256",
    "batches",
}
SECONDARY_SCREENING_BATCH_KEYS = {
    "secondary_batch_id",
    "primary_batch_id",
    "candidate_refs",
    "primary_inputs",
    "cutoff_margin",
}
SECONDARY_SCREENING_INPUT_KEYS = {
    "candidate_ref",
    "evaluation_path",
    "evaluation_sha256",
    "final_score",
}
SCREENING_AGGREGATION_KEYS = {
    "schema_version",
    "secondary_screening_sha256",
    "rule",
    "candidates",
}
SCREENING_AGGREGATION_ROW_KEYS = {
    "candidate_ref",
    "primary_evaluation_path",
    "primary_evaluation_sha256",
    "primary_score",
    "secondary_evaluation_path",
    "secondary_evaluation_sha256",
    "secondary_score",
    "canonical_score",
}
VERSION_SELECTION_KEYS = {"schema_version", "lineages"}
VERSION_SELECTION_ROW_KEYS = {
    "candidate_id",
    "base_candidate_ref",
    "redesign_candidate_ref",
    "base_evaluation_sha256",
    "redesign_evaluation_sha256",
    "selected_candidate_ref",
    "selected_evaluation_sha256",
    "selection_reason",
}
VERSION_SELECTION_CONTROL_ROW_KEYS = {
    "candidate_id",
    "base_candidate_ref",
    "redesign_candidate_ref",
    "base_evaluations",
    "redesign_evaluations",
    "base_conservative_score",
    "redesign_conservative_score",
    "selected_candidate_ref",
    "selected_conservative_score",
    "selection_reason",
}
DEVELOPMENT_AGGREGATION_INPUT_KEYS = {
    "path",
    "sha256",
    "judge_id",
    "final_score",
}
CONSTRUCTION_CHANGE_KEYS = {
    "dependency_change",
    "resulting_control_point_status",
    "control_instrument",
    "distribution_instrument",
    "customer_relationship_owner",
    "customer_relationship_control",
    "fully_loaded_economic_effects",
    "incumbent_response_defensibility",
    "supporting_research_claim_ids",
}
IMPORT_RECEIPT_COMMON_KEYS = {
    "schema_version",
    "run_id",
    "candidate_id",
    "raw_response_path",
    "raw_response_sha256",
    "status",
}
OUTCOME_HISTORY_KEYS = {
    "record_type",
    "run_id",
    "run_status",
    "qualification_label",
    "rubric_id",
    "rubric_sha256",
    "score_scale",
    "official_score",
    "binding_score_floor",
    "selected_candidate_id",
    "selected_candidate_version",
    "selected_title",
    "selected_fingerprint",
    "source_candidate_path",
    "source_candidate_sha256",
    "report_sha256",
    "outcome_path",
    "terminal_objection",
    "reopen_condition",
}
OUTCOME_HISTORY_V2_KEYS = OUTCOME_HISTORY_KEYS | {
    "learning_digest_path",
    "learning_digest_sha256",
    "learning_row_count",
}
OUTCOME_QUARANTINE_KEYS = {
    "schema_version",
    "record_type",
    "run_id",
    "outcome_path",
    "report_sha256",
    "quarantined_at",
    "reason_code",
    "reason",
    "business_decision_eligible",
    "permitted_use",
}
OUTCOME_QUARANTINE_HISTORY_KEYS = OUTCOME_QUARANTINE_KEYS | {
    "quarantine_path",
    "quarantine_sha256",
}
OUTCOME_QUARANTINE_REASON_CODES = {
    "acceptance_test_only",
    "procedural_context_violation",
    "other",
}
LEARNING_ROW_KEYS = {
    "schema_version",
    "run_id",
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "structure",
    "working_limiter",
    "disconfirming_evidence",
    "disposition",
    "constructor_outcome",
    "fresh_evaluation",
    "holdout_objection",
    "reopen_condition",
}
LEARNING_FRESH_EVALUATION_KEYS = {
    "path",
    "sha256",
    "evaluation_type",
    "candidate_version",
    "candidate_sha256",
    "final_score",
}
IMPORT_RECEIPT_ACCEPTED_KEYS = IMPORT_RECEIPT_COMMON_KEYS | {
    "evaluation",
    "evaluation_sha256",
    "final_score",
    "qualified",
}
IMPORT_RECEIPT_REJECTED_KEYS = IMPORT_RECEIPT_COMMON_KEYS | {"error"}
FINAL_EVENT_DETAIL_KEYS_V1 = {
    "previous_stage",
    "run_status",
    "selected_candidate_id",
    "official_score",
    "no_qualifier_reason",
    "report_sha256",
}
FINAL_EVENT_DETAIL_KEYS_V2 = (
    FINAL_EVENT_DETAIL_KEYS_V1 - {"no_qualifier_reason"}
) | {"no_finalist_reason"}
JOB_KEYS = {
    "status",
    "attempts",
    "max_attempts",
    "artifact",
    "artifact_sha256",
    "error",
    "updated_at",
}
JOB_EVENT_CORE_KEYS = {
    "status",
    "attempts",
    "max_attempts",
    "artifact",
    "artifact_sha256",
    "error",
}
STATE_KEYS = {"schema_version", "run_id", "stage", "run_status", "updated_at", "jobs"}
MANIFEST_KEYS = {
    "schema_version",
    "run_id",
    "created_at",
    "config",
    "source_hashes",
    "rubric",
    "campaign",
}
CAMPAIGN_BINDING_KEYS = {
    "campaign_id",
    "cohort_number",
    "gap_brief_path",
    "gap_brief_sha256",
}
CAMPAIGN_MANIFEST_KEYS = {
    "schema_version",
    "campaign_id",
    "created_at",
    "config",
    "config_sha256",
    "founder_sha256",
    "rubric",
}
CAMPAIGN_STATE_KEYS = {
    "schema_version",
    "campaign_id",
    "status",
    "created_at",
    "updated_at",
    "active_run_id",
    "active_cohort_number",
    "cohorts",
    "no_progress_streak",
    "best_official_score",
    "best_working_median",
    "terminal_reason",
}
CAMPAIGN_COHORT_KEYS = {
    "cohort_number",
    "run_id",
    "run_status",
    "report_path",
    "report_sha256",
    "metrics_path",
    "metrics_sha256",
    "gap_brief_path",
    "gap_brief_sha256",
    "official_score",
    "top_four_working_median",
    "deficient_factors",
    "missing_archetypes",
    "progress_signals",
    "made_progress",
    "no_progress_streak",
}
CAMPAIGN_PROGRESS_KEYS = {
    "official_score",
    "working_median",
}
CAMPAIGN_METRIC_KEYS = {
    "official_score",
    "top_four_working_median",
    "deficient_factors",
    "missing_archetypes",
}
CAMPAIGN_EVENT_KEYS = {"sequence", "at", "event", "campaign_id", "details"}
CAMPAIGN_RECEIPT_KEYS = {
    "schema_version",
    "campaign_id",
    "status",
    "terminal_reason",
    "cohort_count",
    "best_official_score",
    "best_working_median",
    "quality_objective_achieved",
    "campaign_manifest_sha256",
    "cohorts",
}
LEGACY_CAMPAIGN_STATE_KEYS_V2 = CAMPAIGN_STATE_KEYS | {
    "best_working_score",
    "seen_archetypes",
}
LEGACY_CAMPAIGN_COHORT_KEYS_V2 = CAMPAIGN_COHORT_KEYS | {
    "best_working_score",
    "archetype_scores",
    "dominant_patterns",
}
LEGACY_CAMPAIGN_PROGRESS_KEYS_V2 = CAMPAIGN_PROGRESS_KEYS | {"novel_archetype"}
LEGACY_CAMPAIGN_METRIC_KEYS_V2 = CAMPAIGN_METRIC_KEYS | {
    "best_working_score",
    "archetype_scores",
    "dominant_patterns",
}
LEGACY_CAMPAIGN_DOMINANT_KEYS_V2 = {
    "commercial_archetype",
    "control_point",
    "critical_dependency",
}
LEGACY_CAMPAIGN_RECEIPT_KEYS_V2 = CAMPAIGN_RECEIPT_KEYS | {"best_working_score"}
CAMPAIGN_GAP_BRIEF_KEYS = {
    "schema_version",
    "campaign_id",
    "cohort_number",
    "deficient_factors",
    "missing_archetypes",
}
CAMPAIGN_METRIC_RECEIPT_KEYS = {
    "schema_version",
    "campaign_id",
    "cohort_number",
    "run_id",
    "report_sha256",
    "metrics",
    "evidence_artifacts",
}
PUBLISHED_CAMPAIGN_REPAIR_KEYS = {
    "schema_version",
    "repair_id",
    "campaign_id",
    "repair_type",
    "reason",
    "prior_commit",
    "prior_receipt_sha256",
    "repaired_receipt_sha256",
    "prior_events_sha256",
    "cohorts",
}
PUBLISHED_CAMPAIGN_REPAIR_COHORT_KEYS = {
    "cohort_number",
    "run_id",
    "prior_metrics_sha256",
    "repaired_metrics_sha256",
    "metrics",
    "added_artifacts",
}
PUBLISHED_CAMPAIGN_REPAIR_ARTIFACT_KEYS = {"path", "sha256"}
EVENT_KEYS = {"sequence", "at", "event", "run_id", "stage", "job_id", "details"}
SAFE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SAFE_JOB_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SAFE_JUDGE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
RUN_ID_RE = re.compile(r"^\d{8}T\d{6}Z-[0-9a-f]{6}$")
CAMPAIGN_ID_RE = re.compile(r"^campaign-\d{8}T\d{6}Z-[0-9a-f]{6}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DERIVED_QUANTUM = Decimal("0.000001")
FINAL_QUANTUM = Decimal("0.1")
QUALIFICATION_LABEL = "score-qualified under holistic-11; not empirically market-validated"


class WorkflowError(Exception):
    exit_code = 1


class InputError(WorkflowError):
    exit_code = 2


class ConflictError(WorkflowError):
    exit_code = 3


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise InputError(f"non-finite JSON number is not allowed: {value}")


def parse_json(text: str, *, source: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_invalid_constant,
        )
    except WorkflowError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise InputError(f"invalid JSON in {source}: {exc}") from exc


def load_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read {path}: {exc}") from exc
    return parse_json(text, source=str(path))


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InputError(f"value is not canonical JSON: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise InputError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def build_preflight_receipt(
    manifest: Mapping[str, Any],
    stage: str,
    job_id: str,
    kind: str,
    input_sha256: str,
    canonical_artifact_sha256: str,
) -> dict[str, Any]:
    """Build the deterministic receipt bound to one structured completion context."""
    payload = {
        "schema_version": PREFLIGHT_ATTESTATION_VERSION,
        "domain": PREFLIGHT_RECEIPT_DOMAIN,
        "run_id": manifest["run_id"],
        "manifest_sha256": sha256_bytes(canonical_json_bytes(manifest)),
        "stage": stage,
        "job_id": job_id,
        "kind": kind,
        "input_sha256": input_sha256,
        "canonical_artifact_sha256": canonical_artifact_sha256,
    }
    return {
        **payload,
        "receipt_sha256": sha256_bytes(canonical_json_bytes(payload)),
    }


def _assert_safe_write_path(root: Path, path: Path, label: str = "output path") -> None:
    """Reject lexical escapes and symlinked path components below a trusted root."""
    root_absolute = Path(os.path.abspath(root))
    path_absolute = Path(os.path.abspath(path))
    try:
        relative = path_absolute.relative_to(root_absolute)
    except ValueError as exc:
        raise InputError(f"{label} escapes its storage root") from exc
    current = root_absolute
    if current.is_symlink():
        raise InputError(f"{label} storage root must not be a symlink: {current}")
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise InputError(f"{label} contains a symlink component: {current}")
        if current.exists() and current != path_absolute and not current.is_dir():
            raise InputError(f"{label} parent is not a directory: {current}")


def atomic_write(path: Path, data: bytes, *, root: Path | None = None) -> None:
    if root is not None:
        _assert_safe_write_path(root, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if root is not None:
        _assert_safe_write_path(root, path)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            temp_path.unlink()
        raise


def write_immutable(path: Path, data: bytes, *, root: Path | None = None) -> str:
    if root is not None:
        _assert_safe_write_path(root, path, "immutable artifact path")
    digest = sha256_bytes(data)
    if path.exists():
        existing = path.read_bytes()
        if existing != data:
            raise ConflictError(f"immutable artifact already exists with different content: {path}")
        return digest
    atomic_write(path, data, root=root)
    return digest


def load_history_entries(history_path: Path) -> list[dict[str, Any]]:
    if not history_path.exists():
        return []
    try:
        lines = history_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read history index {history_path}: {exc}") from exc
    entries: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise InputError(f"blank line in history index at {line_number}")
        entries.append(
            expect_object(
                parse_json(line, source=f"{history_path}:{line_number}"),
                f"history entry {line_number}",
            )
        )
    return entries


def update_history_verification(entries: Sequence[Mapping[str, Any]]) -> None:
    meta_entries = [
        entry for entry in entries if entry.get("record_type") == "index_meta"
    ]
    if len(meta_entries) > 1:
        raise InputError("knowledge history contains multiple index_meta records")
    if not meta_entries:
        return
    verification = expect_object(
        meta_entries[0].get("verification"),
        "knowledge history index_meta.verification",
    )
    required_counts = {
        "total_rows_including_meta",
        "non_meta_rows",
        "opportunity_outcomes",
        "opportunity_outcome_corrections",
    }
    missing_counts = sorted(required_counts - set(verification))
    if missing_counts:
        raise InputError(
            "knowledge history index_meta.verification is missing "
            f"{missing_counts}"
        )
    verification["total_rows_including_meta"] = len(entries)
    verification["non_meta_rows"] = len(entries) - 1
    verification["opportunity_outcomes"] = sum(
        entry.get("record_type")
        in {"opportunity_outcome_v1", "opportunity_outcome_v2"}
        for entry in entries
    )
    verification["opportunity_outcome_corrections"] = sum(
        entry.get("record_type") == "opportunity_outcome_correction_v2"
        for entry in entries
    )
    verification["opportunity_outcome_quarantines"] = sum(
        entry.get("record_type") == "opportunity_outcome_quarantine_v1"
        for entry in entries
    )


def history_jsonl_bytes(entries: Sequence[Mapping[str, Any]]) -> bytes:
    return "".join(
        json.dumps(
            dict(entry),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
        for entry in entries
    ).encode("utf-8")


@contextlib.contextmanager
def file_lock(path: Path, *, root: Path | None = None) -> Iterator[None]:
    """Open a lock without following a substituted symlink."""
    if root is not None:
        _assert_safe_write_path(root, path, "lock path")
    path.parent.mkdir(parents=True, exist_ok=True)
    if root is not None:
        _assert_safe_write_path(root, path, "lock path")
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags, 0o600)
    except OSError as exc:
        raise InputError(f"cannot open lock without following symlinks: {path}: {exc}") from exc
    with os.fdopen(descriptor, "a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def load_events(path: Path, run_id: str | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read event log {path}: {exc}") from exc
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise InputError(f"blank line in event log at {line_number}")
        event = expect_object(
            parse_json(line, source=f"{path}:{line_number}"),
            f"event {line_number}",
            exact_keys=EVENT_KEYS,
        )
        sequence = expect_int(event["sequence"], f"event {line_number}.sequence", minimum=1)
        if sequence != line_number:
            raise InputError(f"event sequence is not contiguous at line {line_number}")
        expect_nonempty_string(event["at"], f"event {line_number}.at")
        expect_nonempty_string(event["event"], f"event {line_number}.event")
        event_run_id = expect_nonempty_string(event["run_id"], f"event {line_number}.run_id")
        if run_id is not None and event_run_id != run_id:
            raise InputError(f"event {line_number} belongs to a different run")
        if event["stage"] not in STAGES:
            raise InputError(f"event {line_number}.stage is invalid")
        if event["job_id"] is not None:
            job_id = expect_nonempty_string(event["job_id"], f"event {line_number}.job_id")
            if not SAFE_JOB_RE.fullmatch(job_id):
                raise InputError(f"event {line_number}.job_id is invalid")
        expect_object(event["details"], f"event {line_number}.details")
        events.append(event)
    return events


def append_event(
    run_dir: Path,
    state: Mapping[str, Any],
    event_name: str,
    *,
    job_id: str | None = None,
    details: Mapping[str, Any] | None = None,
    stage: str | None = None,
) -> dict[str, Any]:
    events_path = run_dir / "events.jsonl"
    events = load_events(events_path, state["run_id"])
    record = {
        "sequence": len(events) + 1,
        "at": utc_now(),
        "event": expect_nonempty_string(event_name, "event name"),
        "run_id": state["run_id"],
        "stage": stage or state["stage"],
        "job_id": job_id,
        "details": dict(details or {}),
    }
    expect_object(record, "event", exact_keys=EVENT_KEYS)
    data = "".join(
        json.dumps(item, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        for item in [*events, record]
    ).encode("utf-8")
    atomic_write(events_path, data, root=run_dir)
    return record


def project_transition_state(events: Sequence[Mapping[str, Any]]) -> tuple[str, str, Mapping[str, Any] | None]:
    """Derive the durable lifecycle state from the ordered event log."""
    if not events or events[0]["event"] != "run_created" or events[0]["stage"] != "initialized":
        raise InputError("event log must begin with run_created at initialized stage")
    stage = "initialized"
    run_status = "active"
    finalized: Mapping[str, Any] | None = None
    for event in events[1:]:
        name = event["event"]
        if name == "stage_advanced":
            if stage == "complete" or run_status != "active":
                raise InputError("stage_advanced appears after run finalization")
            details = expect_object(event["details"], "stage_advanced details")
            previous = details.get("previous_stage")
            advanced = details.get("stage")
            if previous != stage:
                raise InputError("stage_advanced previous_stage disagrees with event history")
            expected = STAGES[STAGES.index(stage) + 1]
            if advanced != expected or event["stage"] != expected:
                raise InputError("stage_advanced does not follow the configured stage order")
            stage = expected
            continue
        if name == "run_finalized":
            if finalized is not None or stage == "complete" or run_status != "active":
                raise InputError("event log contains duplicate or misplaced run_finalized")
            details = expect_object(event["details"], "run_finalized details")
            if details.get("previous_stage") != stage or event["stage"] != "complete":
                raise InputError("run_finalized stage disagrees with event history")
            terminal = details.get("run_status")
            if terminal not in RUN_STATUSES - {"active"}:
                raise InputError("run_finalized has an invalid terminal status")
            stage = "complete"
            run_status = terminal
            finalized = event
            continue
        if event["stage"] != stage:
            raise InputError(
                f"event {event['sequence']} ({name}) stage disagrees with lifecycle history"
            )
    return stage, run_status, finalized


def _projected_job_record(
    *,
    status: str,
    attempts: int,
    max_attempts: int,
    at: str,
    artifact: str | None = None,
    artifact_sha256: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "attempts": attempts,
        "max_attempts": max_attempts,
        "artifact": artifact,
        "artifact_sha256": artifact_sha256,
        "error": error,
        "updated_at": at,
    }


def project_job_lifecycle(
    events: Sequence[Mapping[str, Any]],
    manifest: Mapping[str, Any],
) -> dict[str, dict[str, dict[str, Any]]]:
    """Project auditable job state from lifecycle events."""
    projected: dict[str, dict[str, dict[str, Any]]] = {stage: {} for stage in STAGES}
    configured_maximum = manifest["config"]["mechanical_attempts"]
    for event in events:
        name = event["event"]
        stage = event["stage"]
        job_id = event["job_id"]
        details = expect_object(event["details"], f"{name} details")
        if name == "job_started":
            if job_id is None:
                raise InputError("job_started event requires a job_id")
            expect_object(details, "job_started details", exact_keys={"attempt", "max_attempts"})
            attempt = expect_int(details["attempt"], "job_started attempt", minimum=1)
            maximum = expect_int(details["max_attempts"], "job_started max_attempts", minimum=1)
            if maximum != configured_maximum:
                raise InputError("job_started max_attempts differs from immutable config")
            previous = projected[stage].get(job_id)
            expected_attempt = 1 if previous is None else previous["attempts"] + 1
            if attempt != expected_attempt:
                raise InputError(f"job_started attempt is not consecutive for {stage}/{job_id}")
            if previous is not None and (
                previous["status"] not in RETRYABLE_JOB_STATUSES
                or previous["attempts"] >= previous["max_attempts"]
            ):
                raise InputError(f"job_started follows a non-retryable job state for {stage}/{job_id}")
            projected[stage][job_id] = _projected_job_record(
                status="running",
                attempts=attempt,
                max_attempts=maximum,
                at=event["at"],
            )
            continue
        if name == "job_failed":
            if job_id is None:
                raise InputError("job_failed event requires a job_id")
            expect_object(
                details,
                "job_failed details",
                exact_keys={"attempt", "error", "retryable"},
            )
            previous = projected[stage].get(job_id)
            if previous is None or previous["status"] != "running":
                raise InputError(f"job_failed has no matching running job for {stage}/{job_id}")
            attempt = expect_int(details["attempt"], "job_failed attempt", minimum=1)
            if attempt != previous["attempts"]:
                raise InputError(f"job_failed attempt differs from job_started for {stage}/{job_id}")
            error = expect_nonempty_string(details["error"], "job_failed error")
            retryable = details["retryable"]
            expected_retryable = attempt < previous["max_attempts"]
            if not isinstance(retryable, bool) or retryable is not expected_retryable:
                raise InputError(f"job_failed retryable flag is invalid for {stage}/{job_id}")
            projected[stage][job_id] = _projected_job_record(
                status="failed",
                attempts=attempt,
                max_attempts=previous["max_attempts"],
                at=event["at"],
                error=error,
            )
            continue
        if name == "job_completed":
            if job_id is None:
                raise InputError("job_completed event requires a job_id")
            kind = details.get("kind")
            if kind not in ARTIFACT_KINDS:
                raise InputError("job_completed kind is invalid")
            attestation_required = (
                preflight_attestation_enabled(manifest["config"])
                and kind in PREFLIGHT_ARTIFACT_KINDS
            )
            allowed = {
                "artifact",
                "artifact_sha256",
                "kind",
                "recovered_after_state_commit",
            }
            required = {"artifact", "artifact_sha256", "kind"}
            if attestation_required:
                allowed.add("preflight_receipt")
                required.add("preflight_receipt")
            if not required.issubset(details) or not set(details).issubset(allowed):
                raise InputError("job_completed details keys are invalid")
            if "recovered_after_state_commit" in details and details["recovered_after_state_commit"] is not True:
                raise InputError("job_completed recovered_after_state_commit must be true when present")
            previous = projected[stage].get(job_id)
            if previous is None or previous["status"] != "running":
                raise InputError(f"job_completed has no matching running job for {stage}/{job_id}")
            artifact = expect_nonempty_string(details["artifact"], "job_completed artifact")
            digest = expect_nonempty_string(details["artifact_sha256"], "job_completed artifact_sha256")
            if not SHA256_RE.fullmatch(digest):
                raise InputError("job_completed artifact_sha256 is invalid")
            if attestation_required:
                receipt = expect_object(
                    details["preflight_receipt"],
                    "job_completed preflight_receipt",
                    exact_keys=PREFLIGHT_RECEIPT_KEYS,
                )
                if (
                    expect_int(
                        receipt["schema_version"],
                        "job_completed preflight_receipt.schema_version",
                        minimum=1,
                    )
                    != PREFLIGHT_ATTESTATION_VERSION
                ):
                    raise InputError(
                        "job_completed preflight_receipt.schema_version is unsupported"
                    )
                input_digest = expect_nonempty_string(
                    receipt["input_sha256"],
                    "job_completed preflight_receipt.input_sha256",
                )
                if not SHA256_RE.fullmatch(input_digest):
                    raise InputError(
                        "job_completed preflight_receipt.input_sha256 is invalid"
                    )
                if receipt != build_preflight_receipt(
                    manifest,
                    stage,
                    job_id,
                    kind,
                    input_digest,
                    digest,
                ):
                    raise InputError(
                        "job_completed preflight receipt differs from its immutable context"
                    )
            projected[stage][job_id] = _projected_job_record(
                status="completed",
                attempts=previous["attempts"],
                max_attempts=previous["max_attempts"],
                at=event["at"],
                artifact=artifact,
                artifact_sha256=digest,
            )
            continue
        if name == "run_resumed":
            expect_object(details, "run_resumed details", exact_keys={"interrupted_jobs"})
            interrupted_value = details["interrupted_jobs"]
            if not isinstance(interrupted_value, list):
                raise InputError("run_resumed interrupted_jobs must be a list")
            interrupted: set[tuple[str, str]] = set()
            for index, raw_item in enumerate(interrupted_value):
                item = expect_object(
                    raw_item,
                    f"run_resumed interrupted_jobs[{index}]",
                    exact_keys={"stage", "job_id"},
                )
                interrupted_stage = item["stage"]
                interrupted_job = expect_nonempty_string(
                    item["job_id"], f"run_resumed interrupted_jobs[{index}].job_id"
                )
                if interrupted_stage not in STAGES or not SAFE_JOB_RE.fullmatch(interrupted_job):
                    raise InputError("run_resumed contains an invalid interrupted job identity")
                reference = (interrupted_stage, interrupted_job)
                if reference in interrupted:
                    raise InputError("run_resumed interrupted_jobs contains a duplicate")
                interrupted.add(reference)
            running = {
                (candidate_stage, candidate_job)
                for candidate_stage, jobs in projected.items()
                for candidate_job, record in jobs.items()
                if record["status"] == "running"
            }
            if interrupted != running:
                raise InputError("run_resumed interrupted_jobs differs from projected running jobs")
            for interrupted_stage, interrupted_job in interrupted:
                previous = projected[interrupted_stage][interrupted_job]
                projected[interrupted_stage][interrupted_job] = _projected_job_record(
                    status="interrupted",
                    attempts=previous["attempts"],
                    max_attempts=previous["max_attempts"],
                    at=event["at"],
                    error="interrupted during previous process lifetime",
                )
            continue
        if name == "dedup_completed":
            gap = details.get("gap_scout_job")
            if gap is None:
                continue
            gap_record = expect_object(gap, "dedup gap_scout_job")
            if gap_record.get("job_id") != "gap-scout":
                raise InputError("dedup gap_scout_job identity is invalid")
            status = gap_record.get("status")
            attempts = expect_int(gap_record.get("attempts"), "dedup gap_scout_job attempts", minimum=0)
            maximum = expect_int(
                gap_record.get("max_attempts"), "dedup gap_scout_job max_attempts", minimum=1
            )
            if maximum != configured_maximum:
                raise InputError("dedup gap_scout_job max_attempts differs from immutable config")
            existing = projected["discovery"].get("gap-scout")
            if existing is None:
                if status != "pending" or attempts != 0:
                    raise InputError("dedup may introduce gap-scout only as a pending job")
                projected["discovery"]["gap-scout"] = _projected_job_record(
                    status="pending",
                    attempts=0,
                    max_attempts=maximum,
                    at=event["at"],
                )
            elif status == "skipped":
                if existing["status"] not in RETRYABLE_JOB_STATUSES:
                    raise InputError("dedup cannot skip a terminal gap-scout job")
                projected["discovery"]["gap-scout"] = _projected_job_record(
                    status="skipped",
                    attempts=existing["attempts"],
                    max_attempts=existing["max_attempts"],
                    at=event["at"],
                )
            elif status != existing["status"] or attempts != existing["attempts"]:
                raise InputError("dedup gap_scout_job summary differs from job lifecycle events")
    return projected


def _job_core(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: record[key] for key in JOB_EVENT_CORE_KEYS}


def job_state_matches_projection(
    state: Mapping[str, Any],
    projected: Mapping[str, Mapping[str, Mapping[str, Any]]],
) -> bool:
    for stage in STAGES:
        state_jobs = state["jobs"][stage]
        projected_jobs = projected[stage]
        if set(state_jobs) != set(projected_jobs):
            return False
        for job_id in state_jobs:
            if _job_core(state_jobs[job_id]) != _job_core(projected_jobs[job_id]):
                return False
    return True


def require_job_event_state_match(
    events: Sequence[Mapping[str, Any]],
    state: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> None:
    if not job_state_matches_projection(state, project_job_lifecycle(events, manifest)):
        raise InputError(
            "state job lifecycle disagrees with events.jsonl; rerun the interrupted job command"
        )


def _recover_trailing_job_event(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: dict[str, Any],
    *,
    event_name: str,
    job_id: str | None = None,
) -> Mapping[str, Any] | None:
    """Reconcile exactly one event-first transition whose state write failed."""
    events = load_events(run_dir / "events.jsonl", state["run_id"])
    projected = project_job_lifecycle(events, manifest)
    if job_state_matches_projection(state, projected):
        return None
    if not events:
        raise InputError("state job lifecycle disagrees with an empty event log")
    trailing = events[-1]
    if trailing["event"] != event_name or (job_id is not None and trailing["job_id"] != job_id):
        raise InputError(
            "state job lifecycle disagrees with events.jsonl outside the requested recovery"
        )
    previous_projection = project_job_lifecycle(events[:-1], manifest)
    if not job_state_matches_projection(state, previous_projection):
        raise InputError("state job lifecycle mismatch is not a single recoverable transition")
    state["jobs"] = {
        stage: {candidate_job: dict(record) for candidate_job, record in projected[stage].items()}
        for stage in STAGES
    }
    save_state(run_dir, state, manifest)
    return trailing


def require_event_state_match(
    run_dir: Path,
    state: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], Mapping[str, Any] | None]:
    events = load_events(run_dir / "events.jsonl", state["run_id"])
    projected_stage, projected_status, finalized = project_transition_state(events)
    if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
        raise InputError(
            "state lifecycle disagrees with events.jsonl; rerun the interrupted transition command"
        )
    require_job_event_state_match(events, state, manifest)
    return events, finalized


def expect_object(value: Any, label: str, *, exact_keys: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{label} must be an object")
    if exact_keys is not None and set(value) != exact_keys:
        missing = sorted(exact_keys - set(value))
        extra = sorted(set(value) - exact_keys)
        raise InputError(f"{label} keys differ; missing={missing}, extra={extra}")
    return value


def expect_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} must be a nonempty string")
    if value != value.strip():
        raise InputError(f"{label} must not contain surrounding whitespace")
    return value


def expect_string_list(value: Any, label: str, *, unique: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise InputError(f"{label} must be a list")
    result = [expect_nonempty_string(item, f"{label}[{index}]") for index, item in enumerate(value)]
    if unique and len(set(result)) != len(result):
        raise InputError(f"{label} must not contain duplicates")
    return result


def expect_int(value: Any, label: str, *, minimum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise InputError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise InputError(f"{label} must be >= {minimum}")
    return value


def expect_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise InputError(f"{label} must be boolean")
    return value


def as_decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise InputError(f"{label} must be numeric")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise InputError(f"{label} must be numeric") from exc
    if not result.is_finite():
        raise InputError(f"{label} must be finite")
    return result


def as_json_number(value: Any, label: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise InputError(f"{label} must be a JSON number")
    return as_decimal(value, label)


def decimal_json(value: Decimal, *, quantum: Decimal | None = None) -> int | float:
    if quantum is not None:
        value = value.quantize(quantum, rounding=ROUND_HALF_UP)
    if value == value.to_integral_value():
        return int(value)
    return float(format(value, "f"))


def validate_config(value: Any, *, allow_legacy_published: bool = False) -> dict[str, Any]:
    config = expect_object(value, "config")
    schema_version = expect_int(config.get("schema_version"), "config.schema_version", minimum=1)
    if schema_version == ACTIVE_SCHEMA_VERSION:
        supplied_keys = set(config)
        if supplied_keys == CONFIG_KEYS_V3_ATTESTED:
            expected_keys = CONFIG_KEYS_V3_ATTESTED
        elif supplied_keys == CONFIG_KEYS_V3_CONTROL:
            expected_keys = CONFIG_KEYS_V3_CONTROL
        elif supplied_keys == CONFIG_KEYS_V3:
            expected_keys = CONFIG_KEYS_V3
        elif supplied_keys == LEGACY_CONFIG_KEYS_V3:
            # Preserve already-created schema-v3 runs while new runs use the
            # score-driven screening bracket.
            expected_keys = LEGACY_CONFIG_KEYS_V3
        else:
            expected_keys = CONFIG_KEYS_V3
    elif schema_version == LEGACY_PUBLISHED_SCHEMA_VERSION and allow_legacy_published:
        expected_keys = LEGACY_CONFIG_KEYS_V2
    else:
        raise InputError(
            f"config.schema_version must be {ACTIVE_SCHEMA_VERSION} for active workflow state"
        )
    expect_object(config, "config", exact_keys=expected_keys)
    if expect_nonempty_string(config["rubric_id"], "config.rubric_id") != "holistic-11-v1":
        raise InputError("config.rubric_id must be holistic-11-v1")
    if config["comparison"] != "strictly_greater_than":
        raise InputError("config.comparison must be strictly_greater_than")
    threshold = as_json_number(config["threshold"], "config.threshold")
    if threshold < 1 or threshold > 10:
        raise InputError("config.threshold must be between 1 and 10")
    for key in (
        "scouts",
        "seeds_per_scout",
        "unique_min",
        "gap_scout_max",
        "shortlist_max",
        "develop_max",
        "finalists_max",
        "native_holdout_judges",
        "mechanical_attempts",
        "sources_min",
        "sources_max",
    ):
        expect_int(config[key], f"config.{key}", minimum=1)
    if schema_version == ACTIVE_SCHEMA_VERSION:
        discovery_lanes = expect_string_list(
            config["discovery_lanes"], "config.discovery_lanes", unique=True
        )
        if len(discovery_lanes) != config["scouts"]:
            raise InputError("config.discovery_lanes must define exactly one lane per scout")
        for lane in discovery_lanes:
            if not SAFE_ID_RE.fullmatch(lane):
                raise InputError("config.discovery_lanes entries must be lowercase path-safe slugs")
    similarity = as_json_number(config["similarity_flag_threshold"], "config.similarity_flag_threshold")
    if similarity <= 0 or similarity > 1:
        raise InputError("config.similarity_flag_threshold must be in (0, 1]")
    if config["sources_min"] > config["sources_max"]:
        raise InputError("config.sources_min must not exceed sources_max")
    if config["finalists_max"] > config["develop_max"] or config["develop_max"] > config["shortlist_max"]:
        raise InputError("config limits must satisfy finalists_max <= develop_max <= shortlist_max")
    if schema_version == ACTIVE_SCHEMA_VERSION and expected_keys == LEGACY_CONFIG_KEYS_V3:
        for key in ("core_shortlist_slots", "wildcard_shortlist_slots"):
            expect_int(config[key], f"config.{key}", minimum=1)
        if (
            config["core_shortlist_slots"] + config["wildcard_shortlist_slots"]
            != config["shortlist_max"]
        ):
            raise InputError(
                "config core_shortlist_slots plus wildcard_shortlist_slots must equal shortlist_max"
            )
    if schema_version == ACTIVE_SCHEMA_VERSION and expected_keys == CONFIG_KEYS_V3:
        expect_int(config["screening_batches"], "config.screening_batches", minimum=1)
        discovery_total = config["scouts"] * config["seeds_per_scout"]
        if discovery_total % config["screening_batches"] != 0:
            raise InputError(
                "config.screening_batches must divide the discovery seed total"
            )
        if config["shortlist_max"] % config["screening_batches"] != 0:
            raise InputError(
                "config.screening_batches must divide shortlist_max"
            )
        batch_size = discovery_total // config["screening_batches"]
        advances_per_batch = config["shortlist_max"] // config["screening_batches"]
        if advances_per_batch > batch_size:
            raise InputError(
                "the derived screening advances per batch cannot exceed batch size"
            )
        if batch_size % len(discovery_lanes) != 0:
            raise InputError(
                "the derived screening batch size must be divisible by the discovery lane count"
            )
        if config["unique_min"] != discovery_total:
            raise InputError(
                "score-bracket config.unique_min must equal the discovery seed total"
            )
    if schema_version == ACTIVE_SCHEMA_VERSION and (
        expected_keys == CONFIG_KEYS_V3_CONTROL
        or expected_keys == CONFIG_KEYS_V3_ATTESTED
    ):
        if set(discovery_lanes) != CONTROL_DISCOVERY_LANES:
            raise InputError(
                "control-contract config.discovery_lanes must define the three permanent discovery lanes"
            )
        expect_int(config["screening_batches"], "config.screening_batches", minimum=1)
        discovery_total = config["scouts"] * config["seeds_per_scout"]
        if discovery_total % config["screening_batches"] != 0:
            raise InputError(
                "config.screening_batches must divide the discovery seed total"
            )
        if config["shortlist_max"] % config["screening_batches"] != 0:
            raise InputError("config.screening_batches must divide shortlist_max")
        batch_size = discovery_total // config["screening_batches"]
        advances_per_batch = config["shortlist_max"] // config["screening_batches"]
        if advances_per_batch > batch_size:
            raise InputError(
                "the derived screening advances per batch cannot exceed batch size"
            )
        if batch_size % len(discovery_lanes) != 0:
            raise InputError(
                "the derived screening batch size must be divisible by the discovery lane count"
            )
        if config["unique_min"] != discovery_total:
            raise InputError(
                "score-bracket config.unique_min must equal the discovery seed total"
            )
        reserve = expect_int(
            config["mechanism_first_founder_access_reserve"],
            "config.mechanism_first_founder_access_reserve",
            minimum=0,
        )
        if reserve > config["seeds_per_scout"]:
            raise InputError(
                "mechanism_first_founder_access_reserve cannot exceed seeds_per_scout"
            )
        expect_bool(
            config["secondary_screening_enabled"],
            "config.secondary_screening_enabled",
        )
        margin = as_json_number(
            config["secondary_screening_close_margin"],
            "config.secondary_screening_close_margin",
        )
        if margin <= 0 or margin > 9:
            raise InputError(
                "config.secondary_screening_close_margin must be in (0, 9]"
            )
        expect_int(
            config["secondary_screening_candidates_per_side"],
            "config.secondary_screening_candidates_per_side",
            minimum=1,
        )
        if config["secondary_screening_aggregation"] != "mean":
            raise InputError(
                "config.secondary_screening_aggregation must be mean"
            )
        expect_int(
            config["development_evaluators_per_lineage"],
            "config.development_evaluators_per_lineage",
            minimum=1,
        )
        if config["development_score_aggregation"] != "minimum":
            raise InputError(
                "config.development_score_aggregation must be minimum"
            )
    if (
        schema_version == ACTIVE_SCHEMA_VERSION
        and expected_keys == CONFIG_KEYS_V3_ATTESTED
        and expect_int(
            config["preflight_attestation_version"],
            "config.preflight_attestation_version",
            minimum=1,
        )
        != PREFLIGHT_ATTESTATION_VERSION
    ):
        raise InputError(
            "config.preflight_attestation_version is not supported"
        )
    for key in (
        "working_evaluators_per_candidate",
        "campaign_min_cohorts",
        "campaign_max_cohorts",
        "campaign_plateau_patience",
    ):
        expect_int(config[key], f"config.{key}", minimum=1)
    if config["working_evaluators_per_candidate"] != 1:
        raise InputError("config.working_evaluators_per_candidate must be 1")
    if config["campaign_min_cohorts"] > config["campaign_max_cohorts"]:
        raise InputError("campaign_min_cohorts must not exceed campaign_max_cohorts")
    for key in (
        "campaign_official_improvement",
        "campaign_working_median_improvement",
    ):
        configured = as_json_number(config[key], f"config.{key}")
        if configured <= 0:
            raise InputError(f"config.{key} must be greater than zero")
    if schema_version == LEGACY_PUBLISHED_SCHEMA_VERSION:
        ratio = as_json_number(
            config["dominant_structure_ratio"], "config.dominant_structure_ratio"
        )
        if ratio <= 0 or ratio > 1:
            raise InputError("config.dominant_structure_ratio must be in (0, 1]")
        for key in (
            "semantic_shortlist_min_archetypes",
            "semantic_shortlist_max_per_archetype",
        ):
            expect_int(config[key], f"config.{key}", minimum=1)
            if config[key] > config["shortlist_max"]:
                raise InputError(f"config.{key} cannot exceed shortlist_max")
        novelty_gap = as_json_number(
            config["campaign_novelty_score_gap"], "config.campaign_novelty_score_gap"
        )
        if novelty_gap <= 0:
            raise InputError("config.campaign_novelty_score_gap must be greater than zero")
    return dict(config)


def control_contract_enabled(config: Mapping[str, Any]) -> bool:
    """Return whether an immutable config uses the focused control contracts."""
    return set(CONTROL_CONTRACT_CONFIG_KEYS).issubset(config)


def preflight_attestation_enabled(config: Mapping[str, Any]) -> bool:
    """Return whether structured completions require a preflight receipt."""
    return (
        config.get("preflight_attestation_version")
        == PREFLIGHT_ATTESTATION_VERSION
    )


def score_bracket_enabled(config: Mapping[str, Any]) -> bool:
    """Return whether this immutable config uses the score-driven bracket."""
    return "screening_batches" in config


def parse_rubric(path: Path) -> tuple[list[tuple[str, Decimal]], str]:
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read rubric {path}: {exc}") from exc
    start_marker = "Score each factor from 1 to 10 using these weights:"
    end_marker = "Base Score ="
    start = text.find(start_marker)
    end = text.find(end_marker, start + len(start_marker)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise InputError("rubric scoring weight section was not found")
    section = text[start + len(start_marker) : end]
    factors: list[tuple[str, Decimal]] = []
    line_re = re.compile(r"^([^:\n]+):\s*([0-9]+(?:\.[0-9]+)?)%$")
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = line_re.fullmatch(line)
        if not match:
            raise InputError(f"unrecognized rubric weight line: {line}")
        name = match.group(1).strip()
        weight = Decimal(match.group(2))
        if any(existing == name for existing, _ in factors):
            raise InputError(f"duplicate rubric factor: {name}")
        factors.append((name, weight))
    if len(factors) != 11:
        raise InputError(f"rubric must define exactly 11 factors, found {len(factors)}")
    if sum((weight for _, weight in factors), Decimal(0)) != Decimal(100):
        raise InputError("rubric weights must sum to 100%")
    return factors, sha256_bytes(data)


def validate_manifest(value: Any) -> dict[str, Any]:
    manifest = expect_object(value, "manifest", exact_keys=MANIFEST_KEYS)
    schema_version = expect_int(manifest["schema_version"], "manifest.schema_version")
    if schema_version != ACTIVE_SCHEMA_VERSION:
        raise InputError(
            f"active manifest.schema_version must be {ACTIVE_SCHEMA_VERSION}; "
            "legacy recovery is available from the documented Git checkpoint"
        )
    run_id = expect_nonempty_string(manifest["run_id"], "manifest.run_id")
    if not RUN_ID_RE.fullmatch(run_id):
        raise InputError("manifest.run_id is not canonical")
    expect_nonempty_string(manifest["created_at"], "manifest.created_at")
    validate_config(manifest["config"])
    if schema_version != manifest["config"]["schema_version"]:
        raise InputError("manifest.schema_version differs from workflow schema")
    hashes = expect_object(manifest["source_hashes"], "manifest.source_hashes")
    if set(hashes) != set(SOURCE_PATHS):
        raise InputError("manifest.source_hashes does not cover the canonical source set")
    for path, digest in hashes.items():
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise InputError(f"manifest source hash is invalid for {path}")
    rubric = expect_object(manifest["rubric"], "manifest.rubric", exact_keys={"rubric_id", "sha256", "factors"})
    if rubric["rubric_id"] != manifest["config"]["rubric_id"]:
        raise InputError("manifest rubric id differs from config")
    if not isinstance(rubric["sha256"], str) or not SHA256_RE.fullmatch(rubric["sha256"]):
        raise InputError("manifest rubric hash is invalid")
    factor_rows = rubric["factors"]
    if not isinstance(factor_rows, list) or len(factor_rows) != 11:
        raise InputError("manifest rubric factors must contain 11 rows")
    names: set[str] = set()
    total = Decimal(0)
    for index, row in enumerate(factor_rows):
        item = expect_object(row, f"manifest.rubric.factors[{index}]", exact_keys={"name", "weight"})
        name = expect_nonempty_string(item["name"], f"manifest.rubric.factors[{index}].name")
        if name in names:
            raise InputError(f"duplicate manifest rubric factor: {name}")
        names.add(name)
        total += as_json_number(item["weight"], f"manifest.rubric.factors[{index}].weight")
    if total != 100:
        raise InputError("manifest rubric weights must sum to 100")
    if manifest["campaign"] is not None:
        binding = expect_object(
            manifest["campaign"], "manifest.campaign", exact_keys=CAMPAIGN_BINDING_KEYS
        )
        campaign_id = expect_nonempty_string(
            binding["campaign_id"], "manifest.campaign.campaign_id"
        )
        if not CAMPAIGN_ID_RE.fullmatch(campaign_id):
            raise InputError("manifest.campaign.campaign_id is not canonical")
        cohort_number = expect_int(
            binding["cohort_number"], "manifest.campaign.cohort_number", minimum=1
        )
        gap_path = binding["gap_brief_path"]
        gap_digest = binding["gap_brief_sha256"]
        if cohort_number == 1:
            if gap_path is not None or gap_digest is not None:
                raise InputError("the first campaign cohort must not bind a gap brief")
        else:
            expected_path = f"briefs/cohort-{cohort_number}.json"
            if gap_path != expected_path:
                raise InputError("manifest campaign gap brief path is not canonical")
            if not isinstance(gap_digest, str) or not SHA256_RE.fullmatch(gap_digest):
                raise InputError("manifest campaign gap brief hash is invalid")
    return manifest


def validate_job_record(value: Any, label: str) -> dict[str, Any]:
    job = expect_object(value, label, exact_keys=JOB_KEYS)
    if job["status"] not in JOB_STATUSES:
        raise InputError(f"{label}.status is invalid")
    attempts = expect_int(job["attempts"], f"{label}.attempts", minimum=0)
    maximum = expect_int(job["max_attempts"], f"{label}.max_attempts", minimum=1)
    if attempts > maximum:
        raise InputError(f"{label}.attempts exceeds max_attempts")
    if job["artifact"] is not None:
        expect_nonempty_string(job["artifact"], f"{label}.artifact")
    if job["artifact_sha256"] is not None and (
        not isinstance(job["artifact_sha256"], str) or not SHA256_RE.fullmatch(job["artifact_sha256"])
    ):
        raise InputError(f"{label}.artifact_sha256 is invalid")
    if (job["artifact"] is None) != (job["artifact_sha256"] is None):
        raise InputError(f"{label} artifact and hash must both be null or both be set")
    if job["error"] is not None:
        expect_nonempty_string(job["error"], f"{label}.error")
    expect_nonempty_string(job["updated_at"], f"{label}.updated_at")
    if job["status"] == "completed" and job["artifact"] is None:
        raise InputError(f"{label} completed without an artifact")
    return job


def validate_state(value: Any, manifest: Mapping[str, Any]) -> dict[str, Any]:
    state = expect_object(value, "state", exact_keys=STATE_KEYS)
    if expect_int(state["schema_version"], "state.schema_version") != manifest["schema_version"]:
        raise InputError("state.schema_version differs from manifest")
    if state["run_id"] != manifest["run_id"]:
        raise InputError("state identity differs from manifest")
    if state["stage"] not in STAGES:
        raise InputError("state.stage is invalid")
    if state["run_status"] not in RUN_STATUSES:
        raise InputError("state.run_status is invalid")
    if state["stage"] == "complete" and state["run_status"] == "active":
        raise InputError("complete run cannot have active status")
    if state["stage"] != "complete" and state["run_status"] != "active":
        raise InputError("non-complete run must have active status")
    expect_nonempty_string(state["updated_at"], "state.updated_at")
    jobs = expect_object(state["jobs"], "state.jobs")
    if set(jobs) != set(STAGES):
        raise InputError("state.jobs must contain every stage")
    for stage, stage_jobs in jobs.items():
        mapping = expect_object(stage_jobs, f"state.jobs.{stage}")
        for job_id, record in mapping.items():
            if not SAFE_JOB_RE.fullmatch(job_id):
                raise InputError(f"invalid job id in state: {job_id}")
            validate_job_record(record, f"state.jobs.{stage}.{job_id}")
    return state


def rubric_from_manifest(manifest: Mapping[str, Any]) -> list[tuple[str, Decimal]]:
    return [
        (row["name"], as_json_number(row["weight"], f"weight for {row['name']}"))
        for row in manifest["rubric"]["factors"]
    ]


def resolve_run(runs_dir: Path, run: str) -> Path:
    if not isinstance(run, str) or not RUN_ID_RE.fullmatch(run):
        raise InputError("run must be a canonical run id, not a path")
    root = Path(os.path.abspath(runs_dir))
    path = root / run
    _assert_safe_write_path(root, path, "run path")
    if not path.is_dir() or not (path / "manifest.json").is_file() or not (path / "state.json").is_file():
        raise InputError(f"run not found: {run}")
    return path


def validate_input_snapshots(run_dir: Path, manifest: Mapping[str, Any]) -> None:
    for source, snapshot in INPUT_SNAPSHOTS.items():
        path = run_dir / snapshot
        if not path.is_file():
            raise InputError(f"run is missing immutable input snapshot: {snapshot}")
        digest = sha256_file(path)
        if digest != manifest["source_hashes"][source]:
            raise InputError(f"input snapshot hash mismatch: {snapshot}")
    snapshot_config = validate_config(load_json(run_dir / "inputs" / "config.json"))
    if snapshot_config != manifest["config"]:
        raise InputError("inputs/config.json differs from the immutable manifest config")
    snapshot_factors, snapshot_rubric_hash = parse_rubric(run_dir / "inputs" / "evaluator.txt")
    if snapshot_rubric_hash != manifest["rubric"]["sha256"]:
        raise InputError("inputs/evaluator.txt hash differs from the immutable manifest rubric")
    manifest_factors = rubric_from_manifest(manifest)
    if snapshot_factors != manifest_factors:
        raise InputError("inputs/evaluator.txt factors differ from the immutable manifest rubric")


def load_run(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = validate_manifest(load_json(run_dir / "manifest.json"))
    validate_input_snapshots(run_dir, manifest)
    state = validate_state(load_json(run_dir / "state.json"), manifest)
    return manifest, state


def save_state(run_dir: Path, state: dict[str, Any], manifest: Mapping[str, Any]) -> None:
    state["updated_at"] = utc_now()
    validate_state(state, manifest)
    atomic_write(run_dir / "state.json", canonical_json_bytes(state), root=run_dir)


def run_relative_path(run_dir: Path, value: Any, label: str, *, must_exist: bool = True) -> tuple[str, Path]:
    text = expect_nonempty_string(value, label)
    relative = Path(text)
    if relative.is_absolute() or ".." in relative.parts:
        raise InputError(f"{label} must be a safe run-relative path")
    lexical = run_dir / relative
    _assert_safe_write_path(run_dir, lexical, label)
    resolved = lexical.resolve()
    try:
        resolved.relative_to(run_dir.resolve())
    except ValueError as exc:
        raise InputError(f"{label} escapes the run directory") from exc
    if must_exist and not resolved.is_file():
        raise InputError(f"{label} does not exist: {text}")
    return relative.as_posix(), resolved


def candidate_relpath(candidate_id: str, version: int) -> str:
    return f"candidates/{candidate_id}/v{version}.json"


def evaluation_relpath(candidate_id: str, version: int, evaluation_type: str, judge_id: str) -> str:
    if evaluation_type == "working_screening":
        return f"evaluations/{candidate_id}/v{version}/screening-{judge_id}.json"
    if evaluation_type == "working_screening_secondary":
        return f"evaluations/{candidate_id}/v{version}/screening-secondary-{judge_id}.json"
    if evaluation_type == "working_research":
        return f"evaluations/{candidate_id}/v{version}/research-{judge_id}.json"
    if evaluation_type == "working_development":
        return f"evaluations/{candidate_id}/v{version}/development-{judge_id}.json"
    if evaluation_type == "holdout_native":
        return f"holdout/{candidate_id}/v{version}/native-{judge_id}.json"
    if evaluation_type == "holdout_external":
        return f"holdout/{candidate_id}/v{version}/external-{judge_id}.json"
    # Read-only schema-v2 publication compatibility. Active artifacts never use
    # this unqualified evaluation type.
    if evaluation_type == "working":
        return f"evaluations/{candidate_id}/v{version}/working-{judge_id}.json"
    raise InputError(f"unsupported evaluation type: {evaluation_type}")


def _validated_enum(value: Any, label: str, allowed: set[str]) -> str:
    item = expect_nonempty_string(value, label)
    if item not in allowed:
        raise InputError(f"{label} is invalid")
    return item


def validate_critical_control_point(value: Any, label: str) -> dict[str, Any]:
    control = expect_object(value, label, exact_keys=CRITICAL_CONTROL_POINT_KEYS)
    canonical = dict(control)
    canonical["subject_type"] = _validated_enum(
        control["subject_type"], f"{label}.subject_type", CONTROL_POINT_SUBJECT_TYPES
    )
    canonical["acquisition_instrument_type"] = _validated_enum(
        control["acquisition_instrument_type"],
        f"{label}.acquisition_instrument_type",
        ACQUISITION_INSTRUMENT_TYPES,
    )
    canonical["exclusivity"] = _validated_enum(
        control["exclusivity"], f"{label}.exclusivity", EXCLUSIVITY_STATUSES
    )
    canonical["revocability"] = _validated_enum(
        control["revocability"], f"{label}.revocability", REVOCABILITY_STATUSES
    )
    canonical["transferability"] = _validated_enum(
        control["transferability"],
        f"{label}.transferability",
        TRANSFERABILITY_STATUSES,
    )
    canonical["replaceability"] = _validated_enum(
        control["replaceability"],
        f"{label}.replaceability",
        REPLACEABILITY_STATUSES,
    )
    canonical["customer_relationship_control"] = _validated_enum(
        control["customer_relationship_control"],
        f"{label}.customer_relationship_control",
        CUSTOMER_RELATIONSHIP_CONTROLS,
    )
    canonical["mechanism_control"] = _validated_enum(
        control["mechanism_control"],
        f"{label}.mechanism_control",
        MECHANISM_CONTROLS,
    )
    canonical["status"] = _validated_enum(
        control["status"], f"{label}.status", CONTROL_POINT_STATUSES
    )
    canonical["founder_access_basis"] = _validated_enum(
        control["founder_access_basis"],
        f"{label}.founder_access_basis",
        FOUNDER_ACCESS_BASES,
    )
    canonical["confidential_employer_resource_dependency"] = _validated_enum(
        control["confidential_employer_resource_dependency"],
        f"{label}.confidential_employer_resource_dependency",
        EMPLOYER_RESOURCE_DEPENDENCIES,
    )
    enum_fields = {
        "subject_type",
        "acquisition_instrument_type",
        "exclusivity",
        "revocability",
        "transferability",
        "replaceability",
        "customer_relationship_control",
        "mechanism_control",
        "status",
        "founder_access_basis",
        "confidential_employer_resource_dependency",
    }
    for key in sorted(CRITICAL_CONTROL_POINT_KEYS - enum_fields):
        canonical[key] = expect_nonempty_string(control[key], f"{label}.{key}")
    if canonical["status"] == "owned" and canonical["mechanism_control"] != "owned":
        raise InputError(f"{label}.mechanism_control must be owned when status is owned")
    if canonical["status"] in {
        "exclusively_contracted",
        "durably_contracted",
        "replaceable_access",
        "externally_controlled",
    } and canonical["mechanism_control"] != "dependent":
        raise InputError(
            f"{label}.mechanism_control must be dependent when the mechanism is not owned"
        )
    if canonical["status"] == "owned" and canonical[
        "acquisition_instrument_type"
    ] not in {"ownership", "purchase"}:
        raise InputError(
            f"{label}.acquisition_instrument_type: owned status requires ownership or purchase"
        )
    if canonical["status"] in {"exclusively_contracted", "durably_contracted"} and canonical[
        "acquisition_instrument_type"
    ] in {"ownership", "purchase", "unknown"}:
        raise InputError(
            f"{label}.acquisition_instrument_type must name a concrete contract instrument "
            f"when status is {canonical['status']}"
        )
    if (
        canonical["status"] == "exclusively_contracted"
        and canonical["exclusivity"] != "exclusive"
    ):
        raise InputError(
            f"{label}.exclusivity: exclusively_contracted status requires exclusive terms"
        )
    if (
        canonical["status"] == "replaceable_access"
        and canonical["replaceability"] != "replaceable"
    ):
        raise InputError(
            f"{label}.replaceability: replaceable_access status requires replaceable terms"
        )
    if (
        canonical["status"] == "replaceable_access"
        and canonical["acquisition_instrument_type"] == "unknown"
    ):
        raise InputError(
            f"{label}.acquisition_instrument_type: replaceable_access status requires "
            "a concrete acquisition instrument"
        )
    if canonical["status"] in {
        "owned",
        "exclusively_contracted",
        "durably_contracted",
        "replaceable_access",
    } and normalize_fingerprint(canonical["acquisition_instrument"]) == "unknown":
        raise InputError(
            f"{label}.acquisition_instrument: affirmative control status requires "
            "a stated acquisition instrument"
        )
    if canonical["status"] == "durably_contracted":
        if normalize_fingerprint(canonical["duration"]) == "unknown":
            raise InputError(
                f"{label}.duration: durably_contracted status requires a known duration"
            )
        if canonical["revocability"] in {"at_will", "unknown"}:
            raise InputError(
                f"{label}.revocability: durably_contracted status cannot be at_will or unknown"
            )
    if (
        canonical["status"] == "replaceable_access"
        and canonical["acquisition_instrument_type"] == "ownership"
    ):
        raise InputError(
            f"{label}.acquisition_instrument_type: replaceable_access status cannot use ownership"
        )
    return canonical


def validate_commercial_mechanics(value: Any, label: str) -> dict[str, Any]:
    mechanics = expect_object(value, label, exact_keys=COMMERCIAL_MECHANICS_KEYS)
    canonical = dict(mechanics)
    loaded = expect_object(
        mechanics["fully_loaded_economics"],
        f"{label}.fully_loaded_economics",
        exact_keys=FULLY_LOADED_ECONOMICS_KEYS,
    )
    canonical["fully_loaded_economics"] = {
        key: expect_nonempty_string(
            loaded[key], f"{label}.fully_loaded_economics.{key}"
        )
        for key in sorted(FULLY_LOADED_ECONOMICS_KEYS)
    }
    for key in sorted(COMMERCIAL_MECHANICS_KEYS - {"fully_loaded_economics"}):
        canonical[key] = expect_nonempty_string(mechanics[key], f"{label}.{key}")
    return canonical


def validate_structural_signature(value: Any, label: str) -> dict[str, Any]:
    signature = expect_object(value, label, exact_keys=STRUCTURAL_SIGNATURE_KEYS)
    categories = {
        "commercial_model_category": COMMERCIAL_MODEL_CATEGORIES,
        "control_point_category": SIGNATURE_CONTROL_POINT_CATEGORIES,
        "critical_dependency_category": CRITICAL_DEPENDENCY_CATEGORIES,
    }
    canonical: dict[str, Any] = {}
    for key, allowed in categories.items():
        canonical[key] = _validated_enum(signature[key], f"{label}.{key}", allowed)
        descriptor_key = key.replace("_category", "_descriptor")
        descriptor = normalize_fingerprint(
            expect_nonempty_string(signature[descriptor_key], f"{label}.{descriptor_key}")
        )
        if not descriptor:
            raise InputError(f"{label}.{descriptor_key} must normalize to nonempty text")
        canonical[descriptor_key] = descriptor
    return canonical


def structural_signature_key(candidate: Mapping[str, Any]) -> tuple[str, ...]:
    signature = candidate["structural_signature"]
    parts: list[str] = []
    for prefix in ("commercial_model", "control_point", "critical_dependency"):
        category = signature[f"{prefix}_category"]
        parts.extend(
            (category, signature[f"{prefix}_descriptor"] if category == "other" else "")
        )
    return tuple(parts)


def validate_candidate(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    *,
    verify_parent: bool = True,
) -> dict[str, Any]:
    candidate = expect_object(value, "candidate")
    uses_control_contract = control_contract_enabled(manifest["config"])
    required_keys = CANDIDATE_KEYS | (
        CANDIDATE_CONTROL_KEYS if uses_control_contract else set()
    )
    missing = sorted(required_keys - set(candidate))
    extra = sorted(set(candidate) - CANDIDATE_KEYS - CANDIDATE_OPTIONAL_KEYS)
    if uses_control_contract:
        extra = sorted(
            set(candidate)
            - CANDIDATE_KEYS
            - CANDIDATE_OPTIONAL_KEYS
            - CANDIDATE_CONTROL_KEYS
        )
    if missing or extra:
        raise InputError(f"candidate keys differ; missing={missing}, extra={extra}")
    if expect_int(candidate["schema_version"], "candidate.schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError("candidate.schema_version differs from workflow schema")
    if "structure" not in candidate:
        raise InputError("candidate requires structure")
    structure = expect_object(candidate["structure"], "candidate.structure", exact_keys=STRUCTURE_KEYS)
    for key in STRUCTURE_KEYS:
        expect_nonempty_string(structure[key], f"candidate.structure.{key}")
    canonical = dict(candidate)
    if uses_control_contract:
        critical_control_point = validate_critical_control_point(
            candidate["critical_control_point"], "candidate.critical_control_point"
        )
        commercial_mechanics = validate_commercial_mechanics(
            candidate["commercial_mechanics"], "candidate.commercial_mechanics"
        )
        structural_signature = validate_structural_signature(
            candidate["structural_signature"], "candidate.structural_signature"
        )
        if normalize_fingerprint(
            commercial_mechanics["customer_relationship_owner"]
        ) != normalize_fingerprint(
            critical_control_point["customer_relationship_owner"]
        ):
            raise InputError(
                "candidate customer_relationship_owner must agree across control and commercial mechanics"
            )
        canonical["critical_control_point"] = critical_control_point
        canonical["commercial_mechanics"] = commercial_mechanics
        canonical["structural_signature"] = structural_signature
    candidate_id = expect_nonempty_string(candidate["candidate_id"], "candidate.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("candidate.candidate_id must be a lowercase slug")
    version = expect_int(candidate["version"], "candidate.version", minimum=1)
    stage = candidate["stage"]
    if stage not in CANDIDATE_STAGES:
        raise InputError("candidate.stage is invalid")
    discovery_lane = expect_nonempty_string(
        candidate["discovery_lane"], "candidate.discovery_lane"
    )
    if discovery_lane not in manifest["config"]["discovery_lanes"]:
        raise InputError("candidate.discovery_lane is not configured for this run")
    parent = candidate["parent"]
    redesign_parent: dict[str, Any] | None = None
    if version == 1:
        if parent is not None or stage != "discovery":
            raise InputError("candidate v1 must be an unparented discovery candidate")
    else:
        if version != 2 or stage != "development" or parent is None:
            raise InputError(
                "only one admitted development redesign may create candidate v2"
            )
        parent_obj = expect_object(parent, "candidate.parent", exact_keys={"candidate_id", "version"})
        parent_id = expect_nonempty_string(parent_obj["candidate_id"], "candidate.parent.candidate_id")
        if not SAFE_ID_RE.fullmatch(parent_id):
            raise InputError("candidate.parent.candidate_id must be a lowercase slug")
        parent_version = expect_int(parent_obj["version"], "candidate.parent.version", minimum=1)
        if parent_id != candidate_id or parent_version != 1:
            raise InputError("development redesign parent must be the same candidate v1")
        if verify_parent:
            parent_path = run_dir / candidate_relpath(parent_id, parent_version)
            _assert_safe_write_path(run_dir, parent_path, "candidate parent artifact path")
            if not parent_path.is_file():
                raise InputError(f"candidate parent artifact does not exist: {parent_path.relative_to(run_dir)}")
            parent_candidate = validate_candidate(
                load_json(parent_path),
                manifest,
                run_dir,
                verify_parent=True,
            )
            if (
                parent_candidate["candidate_id"] != parent_id
                or parent_candidate["version"] != parent_version
            ):
                raise InputError("candidate parent artifact identity differs from its canonical path")
            if parent_candidate["stage"] != "discovery":
                raise InputError("development redesign must descend directly from discovery v1")
            redesign_parent = parent_candidate
            if discovery_lane != parent_candidate["discovery_lane"]:
                raise InputError(
                    "development redesign must preserve its discovery lane provenance"
                )
    expect_nonempty_string(candidate["title"], "candidate.title")
    expect_nonempty_string(candidate["thesis"], "candidate.thesis")
    fingerprint = expect_object(candidate["fingerprint"], "candidate.fingerprint", exact_keys=FINGERPRINT_KEYS)
    for key in FINGERPRINT_KEYS:
        expect_nonempty_string(fingerprint[key], f"candidate.fingerprint.{key}")
    founder_fit = expect_string_list(
        candidate["founder_fit"], "candidate.founder_fit", unique=True
    )
    if not founder_fit:
        raise InputError(
            "candidate.founder_fit must be a nonempty JSON array of distinct strings"
        )
    source_refs = expect_string_list(candidate["source_refs"], "candidate.source_refs", unique=True)
    maximum = manifest["config"]["sources_max"]
    if len(source_refs) > maximum:
        raise InputError(f"candidate.source_refs exceeds sources_max={maximum}")
    economics = expect_object(candidate["economics"], "candidate.economics", exact_keys=ECONOMICS_KEYS)
    for key, item in economics.items():
        if item is None:
            continue
        if isinstance(item, bool) or not isinstance(item, (str, int, float)):
            raise InputError(f"candidate.economics.{key} must be a string, number, or null")
        if isinstance(item, str) and not item.strip():
            raise InputError(f"candidate.economics.{key} must not be an empty string")
        if isinstance(item, float) and not Decimal(str(item)).is_finite():
            raise InputError(f"candidate.economics.{key} must be finite")
    redesign: dict[str, Any] | None = None
    declared_fields: list[str] = []
    if "redesign" in candidate:
        if candidate["stage"] != "development" or candidate["version"] != 2:
            raise InputError("candidate.redesign is valid only for admitted development v2")
        redesign = expect_object(
            candidate["redesign"],
            "candidate.redesign",
            exact_keys=REDESIGN_CONTROL_KEYS if uses_control_contract else REDESIGN_KEYS,
        )
        declared_fields = expect_string_list(
            redesign["changed_fingerprint_fields"],
            "candidate.redesign.changed_fingerprint_fields",
            unique=True,
        )
        if not declared_fields or any(field not in FINGERPRINT_KEYS for field in declared_fields):
            raise InputError("candidate.redesign.changed_fingerprint_fields must name fingerprint fields")
        expect_nonempty_string(redesign["economic_effect"], "candidate.redesign.economic_effect")
        if uses_control_contract:
            changed_structural_fields = expect_string_list(
                redesign["changed_structural_fields"],
                "candidate.redesign.changed_structural_fields",
                unique=True,
            )
            if not changed_structural_fields or any(
                field not in STRUCTURAL_CHANGE_FIELDS
                for field in changed_structural_fields
            ):
                raise InputError(
                    "candidate.redesign.changed_structural_fields must name commercial structure fields"
                )
    if redesign_parent is None:
        if redesign is not None:
            raise InputError("candidate.redesign is valid only for admitted development v2")
    else:
        if redesign is None:
            raise InputError("development v2 requires candidate.redesign")
        actual_fields = {
            key
            for key in FINGERPRINT_KEYS
            if normalize_fingerprint(candidate["fingerprint"][key])
            != normalize_fingerprint(redesign_parent["fingerprint"][key])
        }
        if set(declared_fields) != actual_fields:
            raise InputError(
                "candidate.redesign.changed_fingerprint_fields must exactly match normalized fingerprint changes"
            )
        if all(candidate["economics"][key] == redesign_parent["economics"][key] for key in ECONOMICS_KEYS):
            raise InputError("development redesign must update at least one economics field")
        if uses_control_contract:
            actual_structural_fields = {
                key
                for key in STRUCTURAL_CHANGE_FIELDS
                if canonical[key] != redesign_parent[key]
            }
            if set(redesign["changed_structural_fields"]) != actual_structural_fields:
                raise InputError(
                    "candidate.redesign.changed_structural_fields must exactly match changed commercial structures"
                )
    capital = economics["capital_required_pln"]
    if isinstance(capital, bool) or not isinstance(capital, (int, float)):
        raise InputError("candidate.economics.capital_required_pln must be a JSON number")
    if as_json_number(capital, "candidate.economics.capital_required_pln") < 0:
        raise InputError("candidate.economics.capital_required_pln must be nonnegative")
    claims = candidate["claims"]
    if not isinstance(claims, list):
        raise InputError("candidate.claims must be a list")
    claim_source_refs = set(source_refs)
    if redesign_parent is not None:
        parent_research_relative = research_relpath(candidate_id, 1)
        parent_research_source = f"runs/{manifest['run_id']}/{parent_research_relative}"
        if parent_research_source in claim_source_refs:
            parent_research_path = run_dir / parent_research_relative
            _assert_safe_write_path(
                run_dir, parent_research_path, "candidate parent research artifact path"
            )
            if parent_research_path.is_file():
                parent_research = validate_research(
                    load_json(parent_research_path), manifest, run_dir
                )
                if (
                    parent_research["candidate_id"] != candidate_id
                    or parent_research["candidate_version"] != 1
                    or parent_research_path.read_bytes() != canonical_json_bytes(parent_research)
                ):
                    raise InputError("candidate parent research differs from its canonical binding")
                claim_source_refs.update(
                    f"{parent_research_source}#{claim['claim_id']}"
                    for claim in parent_research["claims"]
                )
    claim_ids: set[str] = set()
    for index, raw_claim in enumerate(claims):
        claim = expect_object(raw_claim, f"candidate.claims[{index}]", exact_keys=CLAIM_KEYS)
        claim_id = expect_nonempty_string(claim["claim_id"], f"candidate.claims[{index}].claim_id")
        if claim_id in claim_ids:
            raise InputError(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        expect_nonempty_string(claim["statement"], f"candidate.claims[{index}].statement")
        if not isinstance(claim["claim_type"], str) or claim["claim_type"] not in CLAIM_TYPES:
            raise InputError(f"candidate.claims[{index}].claim_type is invalid")
        evidence_refs = expect_string_list(
            claim["evidence_refs"], f"candidate.claims[{index}].evidence_refs", unique=True
        )
        missing_evidence = sorted(set(evidence_refs) - claim_source_refs)
        if missing_evidence:
            raise InputError(f"candidate claim {claim_id} references unknown source_refs: {missing_evidence}")
        confidence = claim["confidence"]
        if isinstance(confidence, str):
            expect_nonempty_string(confidence, f"candidate.claims[{index}].confidence")
        elif isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise InputError(f"candidate.claims[{index}].confidence must be a string or number")
        elif as_decimal(confidence, f"candidate.claims[{index}].confidence") < 0 or as_decimal(
            confidence, f"candidate.claims[{index}].confidence"
        ) > 1:
            raise InputError(f"candidate.claims[{index}].confidence numeric value must be in [0, 1]")
    for key in ("contrary_evidence", "uncertainties", "risks"):
        expect_string_list(candidate[key], f"candidate.{key}", unique=True)
    if uses_control_contract and stage == "discovery" and discovery_lane == "mechanism-first":
        control = canonical["critical_control_point"]
        mechanics = canonical["commercial_mechanics"]
        if control["status"] == "externally_controlled":
            raise InputError(
                "mechanism-first discovery must begin from an obtainable control point, not an externally controlled mechanism"
            )
        if normalize_fingerprint(mechanics["paid_event_or_measurable_loss"]) == "unknown":
            raise InputError(
                "mechanism-first discovery requires an existing paid event or measurable loss"
            )
        if control["confidential_employer_resource_dependency"] == "present":
            raise InputError(
                "mechanism-first discovery cannot depend on confidential employer resources"
            )
    return canonical


def research_relpath(candidate_id: str, version: int) -> str:
    return f"research/{candidate_id}/v{version}.json"


def validate_falsification_map(
    value: Any,
    label: str,
    claim_ids: set[str],
) -> dict[str, list[str]]:
    mapping = expect_object(value, label, exact_keys=FALSIFICATION_KEYS)
    canonical: dict[str, list[str]] = {}
    for key in sorted(FALSIFICATION_KEYS):
        refs = expect_string_list(mapping[key], f"{label}.{key}", unique=True)
        if not refs:
            raise InputError(f"{label}.{key} must reference at least one claim")
        missing = sorted(set(refs) - claim_ids)
        if missing:
            raise InputError(f"{label}.{key} references unknown claims: {missing}")
        canonical[key] = refs
    return canonical


def _validate_claim_source_coverage(
    value: Any,
    label: str,
    claims_by_id: Mapping[str, Mapping[str, Any]],
    source_ids: set[str],
) -> dict[str, Any]:
    item = expect_object(value, label, exact_keys=COMMERCIAL_EVIDENCE_ITEM_KEYS)
    status = _validated_enum(
        item["status"], f"{label}.status", COMMERCIAL_EVIDENCE_STATUSES
    )
    claim_ids = expect_string_list(item["claim_ids"], f"{label}.claim_ids", unique=True)
    if not claim_ids:
        raise InputError(f"{label}.claim_ids must not be empty")
    missing_claims = sorted(set(claim_ids) - set(claims_by_id))
    if missing_claims:
        raise InputError(f"{label}.claim_ids reference unknown claims: {missing_claims}")
    cited_sources = expect_string_list(
        item["source_ids"], f"{label}.source_ids", unique=True
    )
    missing_sources = sorted(set(cited_sources) - source_ids)
    if missing_sources:
        raise InputError(f"{label}.source_ids reference unknown sources: {missing_sources}")
    claim_sources = {
        source_id
        for claim_id in claim_ids
        for source_id in claims_by_id[claim_id]["evidence_refs"]
    }
    uncited_sources = sorted(set(cited_sources) - claim_sources)
    if uncited_sources:
        raise InputError(
            f"{label}.source_ids must be cited by its claim_ids: {uncited_sources}"
        )
    assessments = {claims_by_id[claim_id]["assessment"] for claim_id in claim_ids}
    if status == "unknown":
        if cited_sources or assessments != {"unknown"}:
            raise InputError(
                f"{label} explicit unknown coverage requires only unknown claims and no source_ids"
            )
    else:
        if not cited_sources or status not in assessments:
            raise InputError(
                f"{label} {status} coverage requires a matching assessed claim and cited source"
            )
    return {"status": status, "claim_ids": claim_ids, "source_ids": cited_sources}


def validate_commercial_evidence(
    value: Any,
    claims_by_id: Mapping[str, Mapping[str, Any]],
    sources_by_id: Mapping[str, Mapping[str, Any]],
    label: str = "research.commercial_evidence",
) -> dict[str, Any]:
    evidence = expect_object(value, label, exact_keys=COMMERCIAL_EVIDENCE_KEYS)
    canonical: dict[str, Any] = {}
    for key in sorted(COMMERCIAL_EVIDENCE_KEYS):
        item = _validate_claim_source_coverage(
            evidence[key],
            f"{label}.{key}",
            claims_by_id,
            set(sources_by_id),
        )
        if item["status"] != "unknown" and not any(
            sources_by_id[source_id]["evidence_class"] in COMMERCIAL_EVIDENCE_SOURCE_CLASSES[key]
            for source_id in item["source_ids"]
        ):
            raise InputError(
                f"{label}.{key} lacks a source with a matching bounded evidence_class"
            )
        canonical[key] = item
    return canonical


def validate_research(value: Any, manifest: Mapping[str, Any], run_dir: Path) -> dict[str, Any]:
    uses_control_contract = control_contract_enabled(manifest["config"])
    research = expect_object(
        value,
        "research",
        exact_keys=RESEARCH_KEYS
        | (RESEARCH_CONTROL_KEYS if uses_control_contract else set()),
    )
    if expect_int(research["schema_version"], "research.schema_version") != manifest["config"]["schema_version"]:
        raise InputError("research.schema_version differs from workflow schema")
    candidate_id = expect_nonempty_string(research["candidate_id"], "research.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("research.candidate_id must be a lowercase slug")
    version = expect_int(research["candidate_version"], "research.candidate_version", minimum=1)
    candidate_path = run_dir / candidate_relpath(candidate_id, version)
    if not candidate_path.is_file():
        raise InputError("research candidate artifact does not exist")
    candidate_digest = sha256_file(candidate_path)
    if research["candidate_sha256"] != candidate_digest:
        raise InputError("research.candidate_sha256 does not match the immutable candidate")
    candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
    if candidate["stage"] != "discovery" or candidate["version"] != 1:
        raise InputError("research must bind the immutable discovery candidate directly")
    sources = research["sources"]
    if not isinstance(sources, list):
        raise InputError("research.sources must be a list")
    minimum = manifest["config"]["sources_min"]
    maximum = manifest["config"]["sources_max"]
    if not minimum <= len(sources) <= maximum:
        raise InputError(f"research.sources count must be between {minimum} and {maximum}")
    source_ids: set[str] = set()
    canonical_sources: list[dict[str, Any]] = []
    for index, raw_source in enumerate(sources):
        source_keys = (
            RESEARCH_SOURCE_KEYS if uses_control_contract else LEGACY_RESEARCH_SOURCE_KEYS
        )
        source = expect_object(
            raw_source, f"research.sources[{index}]", exact_keys=source_keys
        )
        for key in source_keys - {"stance", "evidence_class"}:
            expect_nonempty_string(source[key], f"research.sources[{index}].{key}")
        source_id = source["source_id"].strip()
        if source_id in source_ids:
            raise InputError(f"duplicate research source id: {source_id}")
        source_ids.add(source_id)
        if not isinstance(source["stance"], str) or source["stance"] not in {"supporting", "contradicting", "context"}:
            raise InputError(f"research.sources[{index}].stance is invalid")
        if uses_control_contract:
            _validated_enum(
                source["evidence_class"],
                f"research.sources[{index}].evidence_class",
                EVIDENCE_CLASSES,
            )
        canonical_sources.append(dict(source))
    claims = research["claims"]
    if not isinstance(claims, list):
        raise InputError("research.claims must be a list")
    claim_ids: set[str] = set()
    canonical_claims: list[dict[str, Any]] = []
    for index, raw_claim in enumerate(claims):
        claim = expect_object(raw_claim, f"research.claims[{index}]", exact_keys=RESEARCH_CLAIM_KEYS)
        claim_id = expect_nonempty_string(claim["claim_id"], f"research.claims[{index}].claim_id")
        if claim_id in claim_ids:
            raise InputError(f"duplicate research claim id: {claim_id}")
        claim_ids.add(claim_id)
        expect_nonempty_string(claim["statement"], f"research.claims[{index}].statement")
        if not isinstance(claim["assessment"], str) or claim["assessment"] not in {"evidence", "inference", "unknown"}:
            raise InputError(f"research.claims[{index}].assessment is invalid")
        refs = expect_string_list(
            claim["evidence_refs"], f"research.claims[{index}].evidence_refs", unique=True
        )
        missing_refs = sorted(set(refs) - source_ids)
        if missing_refs:
            raise InputError(f"research claim {claim_id} references unknown sources: {missing_refs}")
        canonical_claims.append(dict(claim))
    contrary = expect_string_list(
        research["contrary_evidence"], "research.contrary_evidence", unique=True
    )
    if not contrary:
        raise InputError("research.contrary_evidence must not be empty")
    if not any(source["stance"] == "contradicting" for source in canonical_sources):
        raise InputError("research requires at least one contradicting source")
    expect_string_list(research["unknowns"], "research.unknowns", unique=True)
    canonical = dict(research)
    canonical["sources"] = canonical_sources
    canonical["claims"] = canonical_claims
    canonical["falsification"] = validate_falsification_map(
        research["falsification"], "research.falsification", claim_ids
    )
    if uses_control_contract:
        claims_by_id = {claim["claim_id"]: claim for claim in canonical_claims}
        sources_by_id = {source["source_id"]: source for source in canonical_sources}
        canonical["commercial_evidence"] = validate_commercial_evidence(
            research["commercial_evidence"], claims_by_id, sources_by_id
        )
        control_assessment = expect_object(
            research["critical_control_point_assessment"],
            "research.critical_control_point_assessment",
            exact_keys=RESEARCH_CONTROL_ASSESSMENT_KEYS,
        )
        assessed = _validate_claim_source_coverage(
            {
                "status": control_assessment["assessment"],
                "claim_ids": control_assessment["claim_ids"],
                "source_ids": control_assessment["source_ids"],
            },
            "research.critical_control_point_assessment",
            claims_by_id,
            set(sources_by_id),
        )
        status = _validated_enum(
            control_assessment["status"],
            "research.critical_control_point_assessment.status",
            CONTROL_POINT_STATUSES,
        )
        if status == "unknown" and assessed["status"] != "unknown":
            raise InputError(
                "research critical-control-point status unknown requires an explicit unknown assessment"
            )
        if assessed["status"] == "unknown" and status != "unknown":
            raise InputError(
                "research critical-control-point explicit unknown assessment requires status unknown"
            )
        canonical["critical_control_point_assessment"] = {
            "status": status,
            "assessment": assessed["status"],
            "claim_ids": assessed["claim_ids"],
            "source_ids": assessed["source_ids"],
        }
    return canonical


def validate_development_control_resolution(
    candidate: Mapping[str, Any],
    research: Mapping[str, Any],
    *,
    label: str = "candidate",
) -> None:
    """Keep an externally controlled v1 from producing an unusable immutable v2."""
    if research["critical_control_point_assessment"]["status"] != "externally_controlled":
        return
    if "critical_control_point" not in candidate["redesign"][
        "changed_structural_fields"
    ]:
        raise InputError(
            f"{label}.redesign.changed_structural_fields must include critical_control_point "
            "when research establishes external control"
        )
    control = candidate["critical_control_point"]
    if control["status"] == "externally_controlled":
        raise InputError(
            f"{label}.critical_control_point.status must change from externally_controlled "
            "when research establishes external control"
        )
    if control["acquisition_instrument_type"] == "unknown":
        raise InputError(
            f"{label}.critical_control_point.acquisition_instrument_type must state a "
            "concrete control or contract path when research establishes external control"
        )
    for key in (
        "acquisition_instrument",
        "launch_controller",
        "counterparty_refusal_fallback",
    ):
        if normalize_fingerprint(control[key]) == "unknown":
            raise InputError(
                f"{label}.critical_control_point.{key} must state a concrete control or "
                "contract path when research establishes external control"
            )


def parse_evaluator_response(value: Any, label: str = "evaluator response") -> dict[str, Any]:
    response = expect_object(value, label, exact_keys=EVALUATOR_RESPONSE_KEYS)
    candidate_id = expect_nonempty_string(response["candidate_id"], f"{label}.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError(f"{label}.candidate_id must be a lowercase slug")
    expect_int(response["candidate_version"], f"{label}.candidate_version", minimum=1)
    judge_id = expect_nonempty_string(response["judge_id"], f"{label}.judge_id")
    if not SAFE_JUDGE_RE.fullmatch(judge_id):
        raise InputError(f"{label}.judge_id is not path-safe")
    expect_string_list(response["assumptions"], f"{label}.assumptions", unique=True)
    for key in (
        "main_structural_strength",
        "primary_score_limiter",
        "strongest_disconfirming_evidence",
        "highest_value_structural_change",
        "evidence_needed_for_higher_score",
    ):
        expect_nonempty_string(response[key], f"{label}.{key}")
    return dict(response)


def canonicalize_evaluator_response(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    evaluation_type: str,
) -> dict[str, Any]:
    if evaluation_type not in EVALUATION_TYPES:
        raise InputError("evaluation_type is invalid")
    response = parse_evaluator_response(value)
    candidate_id = response["candidate_id"]
    version = response["candidate_version"]
    candidate_path = run_dir / candidate_relpath(candidate_id, version)
    if not candidate_path.is_file():
        raise InputError("evaluation candidate artifact does not exist")
    candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
    required_candidate_stages = {
        "working_screening": {"discovery"},
        "working_screening_secondary": {"discovery"},
        "working_research": {"discovery"},
        "working_development": {"discovery", "development"},
        "holdout_native": {"discovery", "development"},
        "holdout_external": {"discovery", "development"},
    }[evaluation_type]
    if candidate["stage"] not in required_candidate_stages:
        raise InputError(
            f"{evaluation_type} evaluation cannot bind candidate stage {candidate['stage']}"
        )
    adjustment = as_json_number(
        response["interaction_adjustment"], "evaluator response.interaction_adjustment"
    )
    if adjustment < Decimal("-0.5") or adjustment > Decimal("0.5"):
        raise InputError("evaluator response.interaction_adjustment must be in [-0.5, 0.5]")

    rubric = rubric_from_manifest(manifest)
    expected_names = [name for name, _ in rubric]
    factors_value = response["factors"]
    if not isinstance(factors_value, list):
        raise InputError("evaluator response.factors must be a list")
    supplied_by_name: dict[str, dict[str, Any]] = {}
    supplied_index_by_name: dict[str, int] = {}
    for index, raw_factor in enumerate(factors_value):
        factor = expect_object(
            raw_factor,
            f"evaluator response.factors[{index}]",
            exact_keys=FACTOR_BASE_KEYS,
        )
        name = expect_nonempty_string(
            factor["name"], f"evaluator response.factors[{index}].name"
        )
        if name in supplied_by_name:
            raise InputError(
                f"evaluator response.factors[{index}].name duplicates factor {name}"
            )
        supplied_by_name[name] = factor
        supplied_index_by_name[name] = index
    if set(supplied_by_name) != set(expected_names):
        missing = sorted(set(expected_names) - set(supplied_by_name))
        extra = sorted(set(supplied_by_name) - set(expected_names))
        raise InputError(f"evaluation factors differ from rubric; missing={missing}, extra={extra}")

    scored_weight = Decimal(0)
    scored_values: dict[str, Decimal] = {}
    for name, weight in rubric:
        factor = supplied_by_name[name]
        factor_index = supplied_index_by_name[name]
        status = factor["status"]
        rationale = expect_nonempty_string(
            factor["rationale"],
            f"evaluator response.factors[{factor_index}].rationale",
        )
        if status == "scored":
            score = as_json_number(
                factor["score"],
                f"evaluator response.factors[{factor_index}].score",
            )
            if score < 1 or score > 10:
                raise InputError(
                    f"evaluator response.factors[{factor_index}].score must be in [1, 10]"
                )
            scored_values[name] = score
            scored_weight += weight
        elif status == "excluded":
            if factor["score"] is not None:
                raise InputError(
                    f"evaluator response.factors[{factor_index}].score must be null when excluded"
                )
            if not rationale:
                raise InputError(f"excluded evaluation factor {name} requires a rationale")
        else:
            raise InputError(
                f"evaluator response.factors[{factor_index}].status must be scored or excluded"
            )
    if scored_weight <= 0:
        raise InputError("evaluation must score at least one factor")

    weighted_sum = sum(
        (scored_values[name] * weight for name, weight in rubric if name in scored_values),
        Decimal(0),
    )
    base_exact = weighted_sum / scored_weight
    unrounded_exact = base_exact + adjustment
    constrained_exact = min(Decimal(10), max(Decimal(1), unrounded_exact))
    final_exact = constrained_exact.quantize(FINAL_QUANTUM, rounding=ROUND_HALF_UP)
    qualified = final_exact > as_decimal(manifest["config"]["threshold"], "config.threshold")

    canonical_factors: list[dict[str, Any]] = []
    for name, weight in rubric:
        supplied = supplied_by_name[name]
        effective = weight * Decimal(100) / scored_weight if supplied["status"] == "scored" else Decimal(0)
        canonical_factors.append(
            {
                "name": name,
                "status": supplied["status"],
                "score": None if supplied["status"] == "excluded" else decimal_json(scored_values[name]),
                "rationale": supplied["rationale"].strip(),
                "original_weight": decimal_json(weight, quantum=DERIVED_QUANTUM),
                "effective_weight": decimal_json(effective, quantum=DERIVED_QUANTUM),
            }
        )

    expected_derived: dict[str, Any] = {
        "base_score": decimal_json(base_exact, quantum=DERIVED_QUANTUM),
        "unrounded_score": decimal_json(unrounded_exact, quantum=DERIVED_QUANTUM),
        "constrained_score": decimal_json(constrained_exact, quantum=DERIVED_QUANTUM),
        "final_score": decimal_json(final_exact, quantum=FINAL_QUANTUM),
        "qualified": qualified,
    }
    canonical = {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "candidate_version": version,
        "candidate_sha256": sha256_file(candidate_path),
        "rubric_id": manifest["rubric"]["rubric_id"],
        "rubric_sha256": manifest["rubric"]["sha256"],
        "judge_id": response["judge_id"],
        "evaluation_type": evaluation_type,
        **{key: response[key] for key in EVALUATOR_RESPONSE_KEYS - {"candidate_id", "candidate_version", "judge_id", "factors", "interaction_adjustment"}},
    }
    canonical["interaction_adjustment"] = decimal_json(adjustment)
    canonical["factors"] = canonical_factors
    canonical.update(expected_derived)
    return canonical


def validate_canonical_evaluation(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
) -> dict[str, Any]:
    evaluation = expect_object(
        value,
        "evaluation",
        exact_keys=EVALUATION_INPUT_KEYS | EVALUATION_DERIVED_KEYS,
    )
    if expect_int(
        evaluation["schema_version"], "evaluation.schema_version"
    ) != ACTIVE_SCHEMA_VERSION:
        raise InputError("evaluation.schema_version differs from workflow schema")
    evaluation_type = evaluation["evaluation_type"]
    if evaluation_type not in EVALUATION_TYPES:
        raise InputError("evaluation.evaluation_type is invalid")
    raw_factors = evaluation["factors"]
    if not isinstance(raw_factors, list):
        raise InputError("evaluation.factors must be a list")
    projected_factors: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_factors):
        factor = expect_object(
            raw,
            f"evaluation.factors[{index}]",
            exact_keys=FACTOR_BASE_KEYS | FACTOR_DERIVED_KEYS,
        )
        projected_factors.append({key: factor[key] for key in FACTOR_BASE_KEYS})
    response = {
        key: evaluation[key]
        for key in EVALUATOR_RESPONSE_KEYS - {"factors"}
    }
    response["factors"] = projected_factors
    expected = canonicalize_evaluator_response(
        response, manifest, run_dir, evaluation_type
    )
    if evaluation != expected:
        raise InputError(
            "canonical evaluation differs from its single response or deterministic score"
        )
    return expected


def compute_evaluation(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
) -> dict[str, Any]:
    """Backward-compatible internal name for canonical evaluation validation."""
    return validate_canonical_evaluation(value, manifest, run_dir)


def validate_generic_input(path: Path, kind: str) -> bytes:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read input artifact {path}: {exc}") from exc
    if not data:
        raise InputError(f"{kind} artifact must not be empty")
    return data


def campaign_storage_for_runs(runs_dir: Path) -> Path:
    return runs_dir.parent / "campaigns"


def resolve_campaign(campaigns_dir: Path, campaign: str) -> Path:
    if not isinstance(campaign, str) or not CAMPAIGN_ID_RE.fullmatch(campaign):
        raise InputError("campaign must be a canonical campaign id, not a path")
    root = Path(os.path.abspath(campaigns_dir))
    path = root / campaign
    _assert_safe_write_path(root, path, "campaign path")
    if not path.is_dir() or not (path / "manifest.json").is_file() or not (path / "state.json").is_file():
        raise InputError(f"campaign not found: {campaign}")
    return path


def validate_campaign_manifest(
    value: Any, *, legacy_published: bool = False
) -> dict[str, Any]:
    manifest = expect_object(
        value, "campaign manifest", exact_keys=CAMPAIGN_MANIFEST_KEYS
    )
    expected_schema = (
        LEGACY_PUBLISHED_SCHEMA_VERSION if legacy_published else ACTIVE_SCHEMA_VERSION
    )
    if expect_int(
        manifest["schema_version"], "campaign manifest.schema_version"
    ) != expected_schema:
        raise InputError(
            f"campaign manifest.schema_version must be {expected_schema}"
        )
    campaign_id = expect_nonempty_string(
        manifest["campaign_id"], "campaign manifest.campaign_id"
    )
    if not CAMPAIGN_ID_RE.fullmatch(campaign_id):
        raise InputError("campaign manifest.campaign_id is not canonical")
    expect_nonempty_string(manifest["created_at"], "campaign manifest.created_at")
    config = validate_config(
        manifest["config"], allow_legacy_published=legacy_published
    )
    if config["schema_version"] != expected_schema:
        raise InputError("campaign manifest and config schema versions differ")
    digest = manifest["config_sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise InputError("campaign manifest.config_sha256 is invalid")
    if digest != sha256_bytes(canonical_json_bytes(config)):
        raise InputError("campaign manifest.config_sha256 differs from its config snapshot")
    founder_digest = manifest["founder_sha256"]
    if not isinstance(founder_digest, str) or not SHA256_RE.fullmatch(founder_digest):
        raise InputError("campaign manifest.founder_sha256 is invalid")
    rubric = expect_object(
        manifest["rubric"],
        "campaign manifest.rubric",
        exact_keys={"rubric_id", "sha256", "factors"},
    )
    if rubric["rubric_id"] != config["rubric_id"]:
        raise InputError("campaign rubric id differs from campaign config")
    if not isinstance(rubric["sha256"], str) or not SHA256_RE.fullmatch(rubric["sha256"]):
        raise InputError("campaign rubric hash is invalid")
    factors = rubric["factors"]
    if not isinstance(factors, list) or len(factors) != 11:
        raise InputError("campaign rubric must contain exactly 11 factors")
    names: set[str] = set()
    total = Decimal(0)
    for index, raw in enumerate(factors):
        factor = expect_object(
            raw,
            f"campaign manifest.rubric.factors[{index}]",
            exact_keys={"name", "weight"},
        )
        name = expect_nonempty_string(
            factor["name"], f"campaign manifest.rubric.factors[{index}].name"
        )
        if name in names:
            raise InputError("campaign rubric contains a duplicate factor")
        names.add(name)
        total += as_json_number(
            factor["weight"], f"campaign manifest.rubric.factors[{index}].weight"
        )
    if total != Decimal(100):
        raise InputError("campaign rubric weights must sum to 100")
    return manifest


def _optional_campaign_score(value: Any, label: str) -> Decimal | None:
    if value is None:
        return None
    score = as_json_number(value, label)
    if score < 1 or score > 10:
        raise InputError(f"{label} must be in [1, 10]")
    return score


def campaign_terminal_reason(status: str) -> str | None:
    reasons = {
        "qualified": "A cohort produced a binding strict qualifier.",
        "max_cohorts": "The configured maximum number of fully scored cohorts was reached.",
        "plateau": "The configured no-progress patience was exhausted after the minimum cohort count.",
    }
    return reasons.get(status)


def _campaign_factor_names(manifest: Mapping[str, Any]) -> list[str]:
    return [factor["name"] for factor in manifest["rubric"]["factors"]]


def _gap_archetype_label_is_safe(item: str) -> bool:
    forbidden = re.compile(
        r"\b(candidate|opportunity|score|ranking|threshold|holdout|finalist|winner)\b",
        re.IGNORECASE,
    )
    return (
        0 < len(item) <= 64
        and item == normalize_fingerprint(item)
        and not any(character.isdigit() for character in item)
        and forbidden.search(item) is None
    )


def _validate_gap_archetype_labels(value: Any, label: str) -> list[str]:
    labels = expect_string_list(value, label, unique=True)
    for item in labels:
        if not _gap_archetype_label_is_safe(item):
            raise InputError(f"{label} contains a candidate-like or score-like label")
    return labels


def validate_campaign_cohort(
    value: Any,
    label: str,
    manifest: Mapping[str, Any] | None = None,
    *,
    legacy_published: bool = False,
) -> dict[str, Any]:
    cohort = expect_object(
        value,
        label,
        exact_keys=(
            LEGACY_CAMPAIGN_COHORT_KEYS_V2
            if legacy_published
            else CAMPAIGN_COHORT_KEYS
        ),
    )
    expect_int(cohort["cohort_number"], f"{label}.cohort_number", minimum=1)
    run_id = expect_nonempty_string(cohort["run_id"], f"{label}.run_id")
    if not RUN_ID_RE.fullmatch(run_id):
        raise InputError(f"{label}.run_id is not canonical")
    if cohort["run_status"] not in RUN_STATUSES - {"active", "failed"}:
        raise InputError(f"{label}.run_status is not a published terminal status")
    expected_report_path = f"outcomes/{run_id}/report.json"
    if cohort["report_path"] != expected_report_path:
        raise InputError(f"{label}.report_path is not canonical")
    digest = cohort["report_sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise InputError(f"{label}.report_sha256 is invalid")
    if cohort["metrics_path"] != f"outcomes/{run_id}/campaign-metrics.json":
        raise InputError(f"{label}.metrics_path is not canonical")
    metrics_digest = cohort["metrics_sha256"]
    if not isinstance(metrics_digest, str) or not SHA256_RE.fullmatch(metrics_digest):
        raise InputError(f"{label}.metrics_sha256 is invalid")
    gap_path = cohort["gap_brief_path"]
    gap_digest = cohort["gap_brief_sha256"]
    if cohort["cohort_number"] == 1:
        if gap_path is not None or gap_digest is not None:
            raise InputError(f"{label} first cohort cannot have a gap brief")
    else:
        if gap_path != f"briefs/cohort-{cohort['cohort_number']}.json":
            raise InputError(f"{label}.gap_brief_path is not canonical")
        if not isinstance(gap_digest, str) or not SHA256_RE.fullmatch(gap_digest):
            raise InputError(f"{label}.gap_brief_sha256 is invalid")
    official = _optional_campaign_score(
        cohort["official_score"], f"{label}.official_score"
    )
    if manifest is not None:
        threshold = as_decimal(manifest["config"]["threshold"], "campaign threshold")
        if cohort["run_status"] == "qualified" and (
            official is None or official <= threshold
        ):
            raise InputError(f"{label} qualified status does not strictly exceed threshold")
        if cohort["run_status"] == "no_finalist" and official is not None:
            raise InputError(f"{label} no_finalist status must have an N/A official score")
        if cohort["run_status"] in {"no_qualifier", "contested"} and official is None:
            raise InputError(f"{label} held-out terminal status requires an official score")
    _optional_campaign_score(
        cohort["top_four_working_median"], f"{label}.top_four_working_median"
    )
    if legacy_published:
        _optional_campaign_score(
            cohort["best_working_score"], f"{label}.best_working_score"
        )
        archetype_scores = expect_object(
            cohort["archetype_scores"], f"{label}.archetype_scores"
        )
        for archetype, raw_score in archetype_scores.items():
            normalized = expect_nonempty_string(
                archetype, f"{label}.archetype_scores key"
            )
            if normalized != normalize_fingerprint(normalized):
                raise InputError(f"{label}.archetype_scores keys must be normalized")
            _optional_campaign_score(
                raw_score, f"{label}.archetype_scores.{archetype}"
            )
    deficient = expect_string_list(
        cohort["deficient_factors"], f"{label}.deficient_factors", unique=True
    )
    if len(deficient) > 3:
        raise InputError(f"{label}.deficient_factors may contain at most three factors")
    if manifest is not None and not set(deficient).issubset(_campaign_factor_names(manifest)):
        raise InputError(f"{label}.deficient_factors contains a non-rubric factor")
    _validate_gap_archetype_labels(
        cohort["missing_archetypes"], f"{label}.missing_archetypes"
    )
    if legacy_published:
        dominant = expect_object(
            cohort["dominant_patterns"],
            f"{label}.dominant_patterns",
            exact_keys=LEGACY_CAMPAIGN_DOMINANT_KEYS_V2,
        )
        for key, raw in dominant.items():
            if raw is not None:
                expect_nonempty_string(raw, f"{label}.dominant_patterns.{key}")
    signals = expect_object(
        cohort["progress_signals"],
        f"{label}.progress_signals",
        exact_keys=(
            LEGACY_CAMPAIGN_PROGRESS_KEYS_V2
            if legacy_published
            else CAMPAIGN_PROGRESS_KEYS
        ),
    )
    for key, raw in signals.items():
        if not isinstance(raw, bool):
            raise InputError(f"{label}.progress_signals.{key} must be boolean")
    if not isinstance(cohort["made_progress"], bool):
        raise InputError(f"{label}.made_progress must be boolean")
    if cohort["made_progress"] != any(signals.values()):
        raise InputError(f"{label}.made_progress differs from progress signals")
    expect_int(cohort["no_progress_streak"], f"{label}.no_progress_streak", minimum=0)
    return cohort


def validate_campaign_state(
    value: Any,
    manifest: Mapping[str, Any],
    *,
    legacy_published: bool = False,
) -> dict[str, Any]:
    state = expect_object(
        value,
        "campaign state",
        exact_keys=(
            LEGACY_CAMPAIGN_STATE_KEYS_V2
            if legacy_published
            else CAMPAIGN_STATE_KEYS
        ),
    )
    expected_schema = (
        LEGACY_PUBLISHED_SCHEMA_VERSION if legacy_published else ACTIVE_SCHEMA_VERSION
    )
    if expect_int(state["schema_version"], "campaign state.schema_version") != expected_schema:
        raise InputError(f"campaign state.schema_version must be {expected_schema}")
    if state["campaign_id"] != manifest["campaign_id"]:
        raise InputError("campaign state identity differs from manifest")
    if state["status"] not in CAMPAIGN_STATUSES:
        raise InputError("campaign state.status is invalid")
    expect_nonempty_string(state["created_at"], "campaign state.created_at")
    expect_nonempty_string(state["updated_at"], "campaign state.updated_at")
    if state["created_at"] != manifest["created_at"]:
        raise InputError("campaign state creation time differs from manifest")
    raw_cohorts = state["cohorts"]
    if not isinstance(raw_cohorts, list):
        raise InputError("campaign state.cohorts must be a list")
    cohorts: list[dict[str, Any]] = []
    run_ids: set[str] = set()
    projected: dict[str, Any] = {
        "cohorts": [],
        "best_official_score": None,
        "best_working_median": None,
    }
    if legacy_published:
        projected.update({"best_working_score": None, "seen_archetypes": []})
    for index, raw in enumerate(raw_cohorts, start=1):
        cohort = validate_campaign_cohort(
            raw,
            f"campaign state.cohorts[{index - 1}]",
            manifest,
            legacy_published=legacy_published,
        )
        if cohort["cohort_number"] != index or cohort["run_id"] in run_ids:
            raise InputError("campaign cohorts must be contiguous with unique run ids")
        expected_streak = (
            0
            if index == 1 or cohort["made_progress"]
            else cohorts[-1]["no_progress_streak"] + 1
        )
        if cohort["no_progress_streak"] != expected_streak:
            raise InputError("campaign cohort no-progress streak is inconsistent")
        expected_signals = campaign_progress_signals(
            projected,
            cohort,
            manifest["config"],
            legacy_published=legacy_published,
        )
        if cohort["progress_signals"] != expected_signals:
            raise InputError("campaign cohort progress signals differ from deterministic policy")
        prefix_terminal = (
            cohort["run_status"] == "qualified"
            or index >= manifest["config"]["campaign_max_cohorts"]
            or (
                index >= manifest["config"]["campaign_min_cohorts"]
                and expected_streak >= manifest["config"]["campaign_plateau_patience"]
            )
        )
        if prefix_terminal and index != len(raw_cohorts):
            raise InputError("campaign contains a cohort after an earlier terminal stop")
        run_ids.add(cohort["run_id"])
        cohorts.append(cohort)
        projected["cohorts"].append(cohort)
        pairs = [
            ("best_official_score", "official_score"),
            ("best_working_median", "top_four_working_median"),
        ]
        if legacy_published:
            pairs.append(("best_working_score", "best_working_score"))
        for state_key, metric_key in pairs:
            current = _optional_campaign_score(
                projected[state_key], f"projected campaign {state_key}"
            )
            observed = _optional_campaign_score(
                cohort[metric_key], f"projected campaign {metric_key}"
            )
            if observed is not None and (current is None or observed > current):
                projected[state_key] = decimal_json(observed, quantum=FINAL_QUANTUM)
        if legacy_published:
            projected["seen_archetypes"] = sorted(
                set(projected["seen_archetypes"]) | set(cohort["archetype_scores"])
            )
    if len(cohorts) > manifest["config"]["campaign_max_cohorts"]:
        raise InputError("campaign state exceeds campaign_max_cohorts")
    expected_streak = cohorts[-1]["no_progress_streak"] if cohorts else 0
    if expect_int(state["no_progress_streak"], "campaign state.no_progress_streak", minimum=0) != expected_streak:
        raise InputError("campaign state no-progress streak differs from its latest cohort")
    active_run = state["active_run_id"]
    active_number = state["active_cohort_number"]
    if (active_run is None) != (active_number is None):
        raise InputError("campaign active run id and cohort number must both be null or set")
    if active_run is not None:
        if not isinstance(active_run, str) or not RUN_ID_RE.fullmatch(active_run):
            raise InputError("campaign state.active_run_id is invalid")
        if expect_int(active_number, "campaign state.active_cohort_number", minimum=1) != len(cohorts) + 1:
            raise InputError("campaign active cohort number is not next in sequence")
        if state["status"] != "active":
            raise InputError("terminal campaign cannot have an active run")
    metric_pairs = [
        ("best_official_score", "official_score"),
        ("best_working_median", "top_four_working_median"),
    ]
    if legacy_published:
        metric_pairs.append(("best_working_score", "best_working_score"))
    for state_key, cohort_key in metric_pairs:
        observed = [
            _optional_campaign_score(item[cohort_key], f"campaign cohort {cohort_key}")
            for item in cohorts
            if item[cohort_key] is not None
        ]
        expected = max(observed, default=None)
        actual = _optional_campaign_score(state[state_key], f"campaign state.{state_key}")
        if actual != expected:
            raise InputError(f"campaign state.{state_key} differs from cohort receipts")
    if legacy_published:
        seen = expect_string_list(
            state["seen_archetypes"], "campaign state.seen_archetypes", unique=True
        )
        expected_seen = sorted(
            {label for cohort in cohorts for label in cohort["archetype_scores"]}
        )
        if seen != expected_seen:
            raise InputError("campaign state.seen_archetypes differs from cohort receipts")
    config = manifest["config"]
    if any(item["run_status"] == "qualified" for item in cohorts):
        expected_status = "qualified"
    elif len(cohorts) >= config["campaign_max_cohorts"]:
        expected_status = "max_cohorts"
    elif len(cohorts) >= config["campaign_min_cohorts"] and expected_streak >= config["campaign_plateau_patience"]:
        expected_status = "plateau"
    else:
        expected_status = "active"
    if state["status"] != expected_status:
        raise InputError("campaign state.status differs from deterministic cohort policy")
    if state["status"] == "active":
        if state["terminal_reason"] is not None:
            raise InputError("active campaign must have a null terminal reason")
    else:
        if state["terminal_reason"] != campaign_terminal_reason(state["status"]):
            raise InputError("campaign terminal reason differs from deterministic policy")
        if active_run is not None:
            raise InputError("terminal campaign cannot retain an active run")
    return state


def load_campaign(campaign_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = validate_campaign_manifest(load_json(campaign_dir / "manifest.json"))
    founder_path = campaign_dir / "inputs" / "founder.md"
    evaluator_path = campaign_dir / "inputs" / "evaluator.txt"
    if not founder_path.is_file() or not evaluator_path.is_file():
        raise InputError("campaign is missing its immutable founder or evaluator snapshot")
    if sha256_file(founder_path) != manifest["founder_sha256"]:
        raise InputError("campaign founder snapshot hash differs from its manifest")
    factors, evaluator_digest = parse_rubric(evaluator_path)
    expected_factors = [
        {"name": name, "weight": decimal_json(weight)}
        for name, weight in factors
    ]
    if (
        evaluator_digest != manifest["rubric"]["sha256"]
        or expected_factors != manifest["rubric"]["factors"]
    ):
        raise InputError("campaign evaluator snapshot differs from its manifest")
    state = validate_campaign_state(load_json(campaign_dir / "state.json"), manifest)
    return manifest, state


def _campaign_metric_evidence(outcome_dir: Path) -> list[dict[str, str]]:
    evidence: list[dict[str, str]] = []
    for path in sorted(outcome_dir.rglob("*")):
        if not path.is_file() or path.name == "campaign-metrics.json":
            continue
        _assert_safe_write_path(outcome_dir, path, "campaign metric evidence")
        evidence.append(
            {
                "path": path.relative_to(outcome_dir).as_posix(),
                "sha256": sha256_file(path),
            }
        )
    return evidence


def build_campaign_metric_receipt(
    outcome_dir: Path,
    binding: Mapping[str, Any],
    run_id: str,
    report_sha256: str,
    metrics: Mapping[str, Any],
) -> dict[str, Any]:
    canonical_metrics = expect_object(
        dict(metrics), "campaign metrics", exact_keys=CAMPAIGN_METRIC_KEYS
    )
    return {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "campaign_id": binding["campaign_id"],
        "cohort_number": binding["cohort_number"],
        "run_id": run_id,
        "report_sha256": report_sha256,
        "metrics": canonical_metrics,
        "evidence_artifacts": _campaign_metric_evidence(outcome_dir),
    }


def validate_campaign_metric_receipt(
    outcome_dir: Path,
    cohort: Mapping[str, Any],
    campaign_id: str,
    *,
    legacy_published: bool = False,
) -> dict[str, Any]:
    path = outcome_dir / "campaign-metrics.json"
    if not path.is_file() or sha256_file(path) != cohort["metrics_sha256"]:
        raise InputError("campaign metric receipt is missing or differs from the campaign ledger")
    receipt = expect_object(
        load_json(path),
        "campaign metric receipt",
        exact_keys=CAMPAIGN_METRIC_RECEIPT_KEYS,
    )
    if path.read_bytes() != canonical_json_bytes(receipt):
        raise InputError("campaign metric receipt is not canonical JSON")
    if (
        receipt["schema_version"]
        != (LEGACY_PUBLISHED_SCHEMA_VERSION if legacy_published else ACTIVE_SCHEMA_VERSION)
        or receipt["campaign_id"] != campaign_id
        or receipt["cohort_number"] != cohort["cohort_number"]
        or receipt["run_id"] != cohort["run_id"]
        or receipt["report_sha256"] != cohort["report_sha256"]
    ):
        raise InputError("campaign metric receipt identity differs from its cohort")
    metrics = expect_object(
        receipt["metrics"],
        "campaign metric receipt.metrics",
        exact_keys=(
            LEGACY_CAMPAIGN_METRIC_KEYS_V2
            if legacy_published
            else CAMPAIGN_METRIC_KEYS
        ),
    )
    metric_keys = (
        LEGACY_CAMPAIGN_METRIC_KEYS_V2
        if legacy_published
        else CAMPAIGN_METRIC_KEYS
    )
    expected_metrics = {key: cohort[key] for key in metric_keys}
    if metrics != expected_metrics:
        raise InputError("campaign ledger metrics differ from the immutable metric receipt")
    evidence = receipt["evidence_artifacts"]
    if not isinstance(evidence, list):
        raise InputError("campaign metric evidence_artifacts must be a list")
    canonical_evidence: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(evidence):
        item = expect_object(
            raw,
            f"campaign metric evidence_artifacts[{index}]",
            exact_keys={"path", "sha256"},
        )
        relative, evidence_path = run_relative_path(
            outcome_dir,
            item["path"],
            f"campaign metric evidence_artifacts[{index}].path",
        )
        if relative in seen:
            raise InputError("campaign metric receipt contains duplicate evidence paths")
        seen.add(relative)
        if not isinstance(item["sha256"], str) or not SHA256_RE.fullmatch(item["sha256"]):
            raise InputError("campaign metric receipt contains an invalid evidence hash")
        if not evidence_path.is_file() or sha256_file(evidence_path) != item["sha256"]:
            raise InputError("campaign metric evidence artifact is missing or has changed")
        canonical_evidence.append({"path": relative, "sha256": item["sha256"]})
    if canonical_evidence != _campaign_metric_evidence(outcome_dir):
        raise InputError("campaign metric receipt does not bind the complete outcome evidence set")
    return receipt


def validate_campaign_publication_receipts(
    campaign_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    *,
    outcomes_dir: Path | None = None,
    legacy_published: bool = False,
) -> None:
    outcomes_dir = outcomes_dir or campaign_dir.parent.parent / "outcomes"
    threshold = as_decimal(manifest["config"]["threshold"], "campaign threshold")
    for cohort in state["cohorts"]:
        report_path = outcomes_dir / cohort["run_id"] / "report.json"
        _assert_safe_write_path(outcomes_dir, report_path, "campaign cohort report")
        if not report_path.is_file():
            raise InputError(
                f"campaign cohort {cohort['cohort_number']} report is missing; restore its published outcome before continuing"
            )
        if sha256_file(report_path) != cohort["report_sha256"]:
            raise InputError(
                f"campaign cohort {cohort['cohort_number']} report hash differs from its receipt"
            )
        report = expect_object(
            load_json(report_path),
            f"campaign cohort {cohort['cohort_number']} report",
        )
        validate_campaign_metric_receipt(
            outcomes_dir / cohort["run_id"],
            cohort,
            manifest["campaign_id"],
            legacy_published=legacy_published,
        )
        if report_path.read_bytes() != canonical_json_bytes(report):
            raise InputError("campaign cohort report is not canonical JSON")
        expected_schema = (
            LEGACY_PUBLISHED_SCHEMA_VERSION if legacy_published else ACTIVE_SCHEMA_VERSION
        )
        if report.get("schema_version") != expected_schema:
            raise InputError(
                f"campaign cohort report must use workflow schema v{expected_schema}"
            )
        if (
            report.get("run_id") != cohort["run_id"]
            or report.get("run_status") != cohort["run_status"]
        ):
            raise InputError("campaign cohort report identity differs from its receipt")
        binding = expect_object(
            report.get("campaign"),
            "campaign cohort report.campaign",
            exact_keys=CAMPAIGN_BINDING_KEYS,
        )
        expected_binding = {
            "campaign_id": manifest["campaign_id"],
            "cohort_number": cohort["cohort_number"],
            "gap_brief_path": cohort["gap_brief_path"],
            "gap_brief_sha256": cohort["gap_brief_sha256"],
        }
        if binding != expected_binding:
            raise InputError("campaign cohort report binding differs from its receipt")
        if (
            report.get("rubric_id") != manifest["rubric"]["rubric_id"]
            or report.get("rubric_sha256") != manifest["rubric"]["sha256"]
            or report.get("founder_sha256") != manifest["founder_sha256"]
            or as_json_number(report.get("threshold"), "campaign report threshold")
            != threshold
            or report.get("comparison") != "strictly_greater_than"
        ):
            raise InputError("campaign cohort report canonical inputs differ from the campaign")
        report_score = _optional_campaign_score(
            report.get("official_score"), "campaign report official_score"
        )
        receipt_score = _optional_campaign_score(
            cohort["official_score"], "campaign receipt official_score"
        )
        if report_score != receipt_score:
            raise InputError("campaign cohort official score differs from its report")
        binding_floor = _optional_campaign_score(
            report.get("binding_score_floor"), "campaign report binding_score_floor"
        )
        if cohort["run_status"] == "qualified":
            if report_score is None or binding_floor is None or not (
                report_score > threshold and binding_floor > threshold
            ):
                raise InputError("qualified campaign cohort does not strictly exceed the threshold")
        elif cohort["run_status"] == "no_finalist":
            if report_score is not None or binding_floor is not None:
                raise InputError("no_finalist campaign cohort must have N/A official scores")
        elif cohort["run_status"] == "no_qualifier":
            if report_score is None or binding_floor is None or binding_floor > threshold:
                raise InputError("no_qualifier campaign cohort has invalid held-out score semantics")
        elif cohort["run_status"] == "contested" and binding_floor is None:
            raise InputError("contested campaign cohort must preserve its binding score floor")
        if cohort["cohort_number"] > 1:
            brief_path = campaign_dir / cohort["gap_brief_path"]
            _assert_safe_write_path(campaign_dir, brief_path, "campaign cohort gap brief")
            if not brief_path.is_file() or sha256_file(brief_path) != cohort["gap_brief_sha256"]:
                raise InputError("campaign cohort gap brief is missing or differs from its receipt")
            validate_campaign_gap_brief(
                load_json(brief_path),
                manifest,
                cohort["cohort_number"],
                legacy_published=legacy_published,
            )


def _validate_legacy_published_run_outcome(outcome_dir: Path) -> dict[str, Any]:
    _assert_safe_write_path(
        outcome_dir.parent, outcome_dir, "published run outcome directory"
    )
    report_path = outcome_dir / "report.json"
    markdown_path = outcome_dir / "report.md"
    report = expect_object(load_json(report_path), "published run report")
    if report_path.read_bytes() != canonical_json_bytes(report):
        raise InputError("published run report is not canonical JSON")
    run_id = expect_nonempty_string(report.get("run_id"), "published run report.run_id")
    if run_id != outcome_dir.name or not RUN_ID_RE.fullmatch(run_id):
        raise InputError("published run report identity differs from its outcome directory")
    if report.get("schema_version") != 2:
        raise InputError("published run report must use workflow schema v2")
    if not markdown_path.is_file() or not markdown_path.read_bytes():
        raise InputError("published report.md is missing or empty")
    correction = report.get("correction")
    if correction is None:
        if not report_markdown_matches(report, markdown_path.read_bytes()):
            raise InputError("published report.md differs from its structured report")
    else:
        correction = expect_object(correction, "published outcome correction")
        markdown_hash = correction.get("report_markdown_sha256")
        if (
            not isinstance(markdown_hash, str)
            or not SHA256_RE.fullmatch(markdown_hash)
            or sha256_file(markdown_path) != markdown_hash
        ):
            raise InputError("published correction report.md is not hash-bound")

    checked: set[str] = {"report.json", "report.md"}
    for finalist in report.get("candidates", []):
        candidate_rel, candidate_path = run_relative_path(
            outcome_dir,
            finalist["candidate_artifact"],
            "published finalist candidate",
        )
        if sha256_file(candidate_path) != finalist["candidate_sha256"]:
            raise InputError("published finalist candidate hash differs from report")
        candidate = expect_object(load_json(candidate_path), "published finalist candidate")
        if (
            candidate.get("candidate_id") != finalist["candidate_id"]
            or candidate.get("version") != finalist["candidate_version"]
        ):
            raise InputError("published finalist candidate identity differs from report")
        checked.add(candidate_rel)
        export_root = outcome_dir / "exports" / finalist["candidate_id"]
        for name in ("holdout_packet.md", "response_schema.json"):
            path = export_root / name
            _assert_safe_write_path(outcome_dir, path, "published finalist packet")
            if not path.is_file():
                raise InputError(
                    f"published finalist is missing exports/{finalist['candidate_id']}/{name}"
                )
            checked.add(path.relative_to(outcome_dir).as_posix())
        for artifact in finalist["evaluation_artifacts"]:
            evaluation_rel, evaluation_path = run_relative_path(
                outcome_dir,
                artifact["path"],
                "published finalist evaluation",
            )
            if sha256_file(evaluation_path) != artifact["sha256"]:
                raise InputError("published finalist evaluation hash differs from report")
            evaluation = expect_object(
                load_json(evaluation_path), "published finalist evaluation"
            )
            if (
                evaluation.get("candidate_id") != finalist["candidate_id"]
                or evaluation.get("candidate_version") != finalist["candidate_version"]
                or evaluation.get("evaluation_type") != artifact["evaluation_type"]
                or evaluation.get("judge_id") != artifact["judge_id"]
            ):
                raise InputError("published finalist evaluation identity differs from report")
            raw_rel, raw_path = run_relative_path(
                outcome_dir,
                evaluation.get("raw_response_path"),
                "published finalist raw response",
            )
            if sha256_file(raw_path) != evaluation.get("raw_response_sha256"):
                raise InputError("published finalist raw response hash differs from evaluation")
            checked.update((evaluation_rel, raw_rel))

    coverage = report.get("working_evaluation_coverage")
    if coverage is not None:
        coverage = expect_object(coverage, "published working evaluation coverage")
        for stage in ("research", "development"):
            stage_coverage = expect_object(
                coverage.get(stage), f"published working evaluation coverage.{stage}"
            )
            records = stage_coverage.get("records")
            if not isinstance(records, list):
                raise InputError("published working evaluation coverage records are invalid")
            for record in records:
                record = expect_object(record, "published working evaluation coverage record")
                candidate_relative = candidate_relpath(
                    record["candidate_id"], record["candidate_version"]
                )
                _, candidate_path = run_relative_path(
                    outcome_dir,
                    candidate_relative,
                    "published working-evaluation candidate",
                )
                if sha256_file(candidate_path) != record["candidate_sha256"]:
                    raise InputError(
                        "published working-evaluation candidate hash differs from coverage"
                    )
                candidate = expect_object(
                    load_json(candidate_path), "published working-evaluation candidate"
                )
                if (
                    candidate.get("candidate_id") != record["candidate_id"]
                    or candidate.get("version") != record["candidate_version"]
                    or candidate.get("stage") != record["candidate_stage"]
                    or candidate.get("stage") != stage
                ):
                    raise InputError(
                        "published working-evaluation candidate identity differs from coverage"
                    )
                expected_evaluation = evaluation_relpath(
                    record["candidate_id"],
                    record["candidate_version"],
                    "working",
                    record["judge_id"],
                )
                if record["evaluation_path"] != expected_evaluation:
                    raise InputError(
                        "published working evaluation path differs from coverage identity"
                    )
                evaluation_rel, evaluation_path = run_relative_path(
                    outcome_dir,
                    record["evaluation_path"],
                    "published working evaluation",
                )
                if sha256_file(evaluation_path) != record["evaluation_sha256"]:
                    raise InputError(
                        "published working evaluation hash differs from coverage"
                    )
                evaluation = expect_object(
                    load_json(evaluation_path), "published working evaluation"
                )
                if (
                    evaluation.get("candidate_id") != record["candidate_id"]
                    or evaluation.get("candidate_version") != record["candidate_version"]
                    or evaluation.get("candidate_sha256") != record["candidate_sha256"]
                    or evaluation.get("evaluation_type") != "working"
                    or evaluation.get("judge_id") != record["judge_id"]
                    or evaluation.get("final_score") != record["final_score"]
                ):
                    raise InputError(
                        "published working evaluation identity differs from coverage"
                    )
                raw_rel, raw_path = run_relative_path(
                    outcome_dir,
                    evaluation.get("raw_response_path"),
                    "published working evaluation raw response",
                )
                if sha256_file(raw_path) != evaluation.get("raw_response_sha256"):
                    raise InputError(
                        "published working evaluation raw response hash differs from evaluation"
                    )
                checked.update(
                    (candidate_relative, evaluation_rel, raw_rel)
                )

    for strongest in report.get("strongest_candidates", []):
        if "artifact" not in strongest:
            continue
        artifact_rel, artifact_path = run_relative_path(
            outcome_dir,
            strongest["artifact"],
            "published strongest candidate",
        )
        if sha256_file(artifact_path) != strongest.get("artifact_sha256"):
            raise InputError("published strongest candidate hash differs from report")
        checked.add(artifact_rel)

    raw_portfolio = report.get("portfolio_decision") or {}
    portfolio = raw_portfolio if isinstance(raw_portfolio, Mapping) else {}
    for artifact in (
        portfolio.get("selection_artifact"),
        *portfolio.get("amendment_artifacts", []),
        portfolio.get("development_decision_artifact"),
    ):
        if not artifact:
            continue
        artifact_rel, artifact_path = run_relative_path(
            outcome_dir, artifact["path"], "published portfolio artifact"
        )
        if sha256_file(artifact_path) != artifact["sha256"]:
            raise InputError("published portfolio artifact hash differs from report")
        checked.add(artifact_rel)
    return {"run_id": run_id, "checked_artifacts": sorted(checked)}


def validate_published_run_outcome(outcome_dir: Path) -> dict[str, Any]:
    report_path = outcome_dir / "report.json"
    report = expect_object(load_json(report_path), "published run report")
    if report.get("schema_version") == LEGACY_PUBLISHED_SCHEMA_VERSION:
        return _validate_legacy_published_run_outcome(outcome_dir)
    if report.get("schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError("published run report uses an unsupported workflow schema")
    _assert_safe_write_path(
        outcome_dir.parent, outcome_dir, "published run outcome directory"
    )
    if report_path.read_bytes() != canonical_json_bytes(report):
        raise InputError("published run report is not canonical JSON")
    run_id = expect_nonempty_string(report.get("run_id"), "published run report.run_id")
    if run_id != outcome_dir.name or not RUN_ID_RE.fullmatch(run_id):
        raise InputError("published run report identity differs from its outcome directory")
    markdown_path = outcome_dir / "report.md"
    if (
        not markdown_path.is_file()
        or not report_markdown_matches(report, markdown_path.read_bytes())
    ):
        raise InputError("published report.md differs from its structured report")
    manifest_path = outcome_dir / "manifest.json"
    manifest = validate_manifest(load_json(manifest_path))
    if manifest_path.read_bytes() != canonical_json_bytes(manifest):
        raise InputError("published manifest is not canonical JSON")
    if manifest["run_id"] != run_id:
        raise InputError("published manifest identity differs from its report")
    validate_input_snapshots(outcome_dir, manifest)
    if (
        report.get("rubric_id") != manifest["rubric"]["rubric_id"]
        or report.get("rubric_sha256") != manifest["rubric"]["sha256"]
        or report.get("founder_sha256")
        != manifest["source_hashes"]["PERSONALITY_SITUATION.md"]
        or report.get("comparison") != "strictly_greater_than"
        or as_json_number(report.get("threshold"), "published report threshold")
        != as_json_number(manifest["config"]["threshold"], "published config threshold")
    ):
        raise InputError("published report canonical inputs differ from its manifest")
    events = load_events(outcome_dir / "events.jsonl", run_id)
    projected_stage, projected_status, finalized_event = project_transition_state(events)
    if (
        projected_stage != "complete"
        or finalized_event is None
        or events[-1] is not finalized_event
    ):
        raise InputError(
            "published event log must end at exactly one complete run_finalized boundary"
        )
    final_details = expect_object(
        finalized_event["details"],
        "published run_finalized details",
        exact_keys=FINAL_EVENT_DETAIL_KEYS_V2,
    )
    previous_stage = final_details["previous_stage"]
    if previous_stage not in STAGES[:-1]:
        raise InputError("published run_finalized previous_stage is invalid")
    projected_jobs = project_job_lifecycle(events, manifest)
    prior_state = {
        "run_id": run_id,
        "stage": previous_stage,
        "run_status": "active",
        "jobs": projected_jobs,
    }
    blockers = sorted(
        f"{stage}/{job_id}"
        for stage, jobs in projected_jobs.items()
        for job_id, job in jobs.items()
        if job["status"] == "running" or job_is_retryable(job)
    )
    if blockers:
        raise InputError(
            "published run finalized with running or retryable jobs: "
            + ", ".join(blockers)
        )
    closure_reason = final_details["no_finalist_reason"]
    if closure_reason is None:
        if previous_stage != "holdout":
            raise InputError(
                "only a holdout-derived published report may omit a closure reason"
            )
        expected_report = build_final_report(outcome_dir, manifest, prior_state)
    else:
        if previous_stage != "research":
            raise InputError(
                "published no_finalist closure must derive from the research stage"
            )
        _validate_stage_gate(outcome_dir, manifest, prior_state)
        decision = _load_portfolio_decision(outcome_dir, manifest)
        if any(
            item["disposition"] != "fatal"
            for item in decision["candidate_decisions"]
        ):
            raise InputError(
                "published research closure requires direct-evidence fatal dispositions"
            )
        reason = expect_nonempty_string(
            closure_reason, "published run_finalized closure reason"
        )
        expected_report = build_early_no_qualifier_report(
            outcome_dir,
            manifest,
            prior_state,
            reason,
            final_details["selected_candidate_id"],
        )
    if report != expected_report:
        raise InputError(
            "published report differs from the deterministically rederived outcome"
        )
    if (
        projected_status != expected_report["run_status"]
        or final_details["run_status"] != expected_report["run_status"]
        or final_details["selected_candidate_id"]
        != expected_report["selected_candidate_id"]
        or final_details["official_score"] != expected_report["official_score"]
        or final_details["report_sha256"] != sha256_file(report_path)
    ):
        raise InputError(
            "published run_finalized identity differs from the rederived report"
        )
    checked: set[str] = {
        "report.json",
        "report.md",
        "manifest.json",
        "inputs/founder.md",
        "inputs/evaluator.txt",
        "inputs/config.json",
        "events.jsonl",
    }
    for path, _ in iter_candidates(outcome_dir, manifest):
        checked.add(path.relative_to(outcome_dir).as_posix())
    for path, _ in iter_research(outcome_dir, manifest):
        checked.add(path.relative_to(outcome_dir).as_posix())
    for path, _ in iter_evaluations(outcome_dir, manifest):
        checked.add(path.relative_to(outcome_dir).as_posix())
    if (outcome_dir / "portfolio" / "selection.json").is_file():
        if score_bracket_enabled(manifest["config"]):
            load_screening_batches(outcome_dir, manifest)
            checked.add("dedup/report.json")
            checked.add("portfolio/screening-batches.json")
            if control_contract_enabled(manifest["config"]):
                load_secondary_screening_plan(outcome_dir, manifest)
                load_screening_aggregation(outcome_dir, manifest)
                checked.add("portfolio/secondary-screening.json")
                checked.add("portfolio/screening-aggregation.json")
        effective_portfolio_selection(outcome_dir, manifest)
        checked.add("portfolio/selection.json")
        for path in sorted((outcome_dir / "portfolio" / "amendments").glob("v*.json")):
            checked.add(path.relative_to(outcome_dir).as_posix())
    if (outcome_dir / "portfolio" / "development-decision.json").is_file():
        _load_portfolio_decision(outcome_dir, manifest)
        checked.add("portfolio/development-decision.json")
    if (outcome_dir / "portfolio" / "version-selection.json").is_file():
        load_version_selection(outcome_dir, manifest)
        checked.add("portfolio/version-selection.json")
    for path in sorted((outcome_dir / "development").glob("*/constructor-result.json")):
        validate_development_result(load_json(path), manifest, outcome_dir)
        checked.add(path.relative_to(outcome_dir).as_posix())
    if (outcome_dir / "portfolio" / "finalists.json").is_file():
        if load_finalist_selection(outcome_dir, manifest) != build_finalist_selection(
            outcome_dir, manifest
        ):
            raise InputError("published finalist selection differs from deterministic ranking")
        checked.add("portfolio/finalists.json")
        for _, candidate in finalist_candidates(outcome_dir, manifest):
            validate_finalist_lineage(outcome_dir, manifest, candidate)
            _external_identity(outcome_dir, manifest, candidate["candidate_id"])
            checked.update(
                {
                    f"exports/{candidate['candidate_id']}/holdout_packet.md",
                    f"exports/{candidate['candidate_id']}/response_schema.json",
                }
            )
    for finalist in report.get("candidates", []):
        candidate_rel, candidate_path = run_relative_path(
            outcome_dir,
            finalist["candidate_artifact"],
            "published finalist candidate",
        )
        if sha256_file(candidate_path) != finalist["candidate_sha256"]:
            raise InputError("published finalist candidate hash differs from report")
        checked.add(candidate_rel)
        for artifact in finalist["evaluation_artifacts"]:
            evaluation_rel, evaluation_path = run_relative_path(
                outcome_dir, artifact["path"], "published finalist evaluation"
            )
            if sha256_file(evaluation_path) != artifact["sha256"]:
                raise InputError("published finalist evaluation hash differs from report")
            checked.add(evaluation_rel)
    receipts = validate_external_imports(outcome_dir, manifest)
    for receipt_path, receipt, _ in receipts:
        checked.add(receipt_path.relative_to(outcome_dir).as_posix())
        checked.add(receipt["raw_response_path"])
    learning_rows = validate_learning_digest(outcome_dir, manifest, report)
    checked.add("learning-digest.jsonl")
    if len(learning_rows) != len(list(iter_research(outcome_dir, manifest))):
        raise InputError("published learning digest does not cover every researched candidate")
    return {"run_id": run_id, "checked_artifacts": sorted(checked)}


def _validate_published_campaign_events(
    campaign_dir: Path,
    outcomes_dir: Path,
    receipt: Mapping[str, Any],
) -> int:
    events_path = campaign_dir / "events.jsonl"
    events = load_campaign_events(events_path, receipt["campaign_id"])
    created = [event for event in events if event["event"] == "campaign_created"]
    if len(created) != 1 or created[0] is not events[0] or created[0]["details"] != {}:
        raise InputError("published campaign must begin with campaign_created")
    repair_events = [
        event for event in events if event["event"] == "campaign_publication_repaired"
    ]
    repair_files = sorted((campaign_dir / "repairs").glob("*.json"))
    if len(repair_events) != len(repair_files) or len(repair_events) > 1:
        raise InputError("published campaign repair events and plans do not reconcile")
    allowed = {
        "campaign_created",
        "gap_brief_created",
        "cohort_attached",
        "cohort_published",
        "campaign_finalized",
        "campaign_publication_repaired",
    }
    if any(event["event"] not in allowed for event in events):
        raise InputError("published campaign contains an unknown event")
    for event in events:
        if event["event"] in {
            "gap_brief_created",
            "cohort_attached",
            "cohort_published",
        }:
            expect_int(
                event["details"].get("cohort_number"),
                f"published {event['event']} cohort_number",
                minimum=1,
            )
    expected_counts = {
        "campaign_created": 1,
        "gap_brief_created": max(0, len(receipt["cohorts"]) - 1),
        "cohort_attached": len(receipt["cohorts"]),
        "cohort_published": len(receipt["cohorts"]),
        "campaign_finalized": 1,
        "campaign_publication_repaired": len(repair_events),
    }
    if any(
        sum(event["event"] == name for event in events) != count
        for name, count in expected_counts.items()
    ):
        raise InputError("published campaign lifecycle event counts are invalid")
    expected_lifecycle: list[tuple[str, int | None]] = [
        ("campaign_created", None)
    ]
    for cohort in receipt["cohorts"]:
        number = cohort["cohort_number"]
        if number > 1:
            expected_lifecycle.append(("gap_brief_created", number))
        expected_lifecycle.extend(
            (("cohort_attached", number), ("cohort_published", number))
        )
    expected_lifecycle.append(("campaign_finalized", None))
    if repair_events:
        expected_lifecycle.append(("campaign_publication_repaired", None))
    actual_lifecycle = [
        (
            event["event"],
            event["details"].get("cohort_number")
            if isinstance(event["details"], Mapping)
            else None,
        )
        for event in events
    ]
    if actual_lifecycle != expected_lifecycle:
        raise InputError("published campaign lifecycle events are out of cohort order")

    prior_receipt_sha = sha256_file(campaign_dir / "receipt.json")
    prior_metrics: dict[int, str] = {}
    if repair_events:
        if repair_events[0] is not events[-1]:
            raise InputError("campaign publication repair must be the final event")
        details = expect_object(
            repair_events[0]["details"],
            "campaign publication repair event",
            exact_keys={"repair_id", "repair_path", "repair_sha256"},
        )
        _, repair_path = run_relative_path(
            campaign_dir, details["repair_path"], "campaign publication repair plan"
        )
        if repair_path != repair_files[0].resolve():
            raise InputError("campaign publication repair event names the wrong plan")
        if sha256_file(repair_path) != details["repair_sha256"]:
            raise InputError("campaign publication repair plan hash differs from its event")
        repair = expect_object(
            load_json(repair_path),
            "campaign publication repair plan",
            exact_keys=PUBLISHED_CAMPAIGN_REPAIR_KEYS,
        )
        if repair_path.read_bytes() != canonical_json_bytes(repair):
            raise InputError("campaign publication repair plan is not canonical JSON")
        if (
            expect_int(
                repair["schema_version"],
                "campaign publication repair schema_version",
                minimum=1,
            )
            != 1
            or repair["campaign_id"] != receipt["campaign_id"]
            or repair["repair_type"] != "publication_evidence_completion"
            or repair["repair_id"] != details["repair_id"]
        ):
            raise InputError("campaign publication repair identity is invalid")
        expect_nonempty_string(repair["reason"], "campaign publication repair.reason")
        if not re.fullmatch(r"[0-9a-f]{40}", repair["prior_commit"]):
            raise InputError("campaign publication repair prior_commit is invalid")
        for key in (
            "prior_receipt_sha256",
            "repaired_receipt_sha256",
            "prior_events_sha256",
        ):
            if not isinstance(repair[key], str) or not SHA256_RE.fullmatch(repair[key]):
                raise InputError(f"campaign publication repair {key} is invalid")
        payload = {key: value for key, value in repair.items() if key != "repair_id"}
        if repair["repair_id"] != sha256_bytes(canonical_json_bytes(payload)):
            raise InputError("campaign publication repair id differs from its payload")
        if repair["repaired_receipt_sha256"] != prior_receipt_sha:
            raise InputError("campaign publication repair does not bind the current receipt")
        if repair["prior_receipt_sha256"] == repair["repaired_receipt_sha256"]:
            raise InputError("campaign publication repair must change the receipt hash")
        event_lines = events_path.read_bytes().splitlines(keepends=True)
        if sha256_bytes(b"".join(event_lines[:-1])) != repair["prior_events_sha256"]:
            raise InputError("campaign publication repair does not bind the prior event log")
        prior_receipt_sha = repair["prior_receipt_sha256"]
        repair_cohorts = repair["cohorts"]
        if not isinstance(repair_cohorts, list) or len(repair_cohorts) != len(
            receipt["cohorts"]
        ):
            raise InputError("campaign publication repair cohort coverage is incomplete")
        for expected_number, (cohort, repair_cohort) in enumerate(
            zip(receipt["cohorts"], repair_cohorts, strict=True), start=1
        ):
            repair_cohort = expect_object(
                repair_cohort,
                f"campaign publication repair cohort {expected_number}",
                exact_keys=PUBLISHED_CAMPAIGN_REPAIR_COHORT_KEYS,
            )
            if (
                expect_int(
                    repair_cohort["cohort_number"],
                    f"campaign publication repair cohort {expected_number}.cohort_number",
                    minimum=1,
                )
                != expected_number
                or repair_cohort["run_id"] != cohort["run_id"]
                or repair_cohort["repaired_metrics_sha256"]
                != cohort["metrics_sha256"]
            ):
                raise InputError("campaign publication repair cohort identity is invalid")
            prior = repair_cohort["prior_metrics_sha256"]
            if not isinstance(prior, str) or not SHA256_RE.fullmatch(prior):
                raise InputError("campaign publication repair prior metric hash is invalid")
            if prior == repair_cohort["repaired_metrics_sha256"]:
                raise InputError("campaign publication repair must change each metric hash")
            prior_metrics[expected_number] = prior
            repaired_metric_receipt = expect_object(
                load_json(
                    outcomes_dir / cohort["run_id"] / "campaign-metrics.json"
                ),
                "repaired campaign metric receipt",
            )
            preserved_metrics = expect_object(
                repair_cohort["metrics"],
                "campaign publication repair preserved metrics",
                exact_keys=(
                    LEGACY_CAMPAIGN_METRIC_KEYS_V2
                    if receipt["schema_version"] == LEGACY_PUBLISHED_SCHEMA_VERSION
                    else CAMPAIGN_METRIC_KEYS
                ),
            )
            if repaired_metric_receipt.get("metrics") != preserved_metrics:
                raise InputError(
                    "campaign publication repair changed semantic campaign metrics"
                )
            additions = repair_cohort["added_artifacts"]
            if not isinstance(additions, list) or len(additions) != 6:
                raise InputError(
                    "publication evidence repair must name exactly six recovered finalist artifacts"
                )
            metric_evidence = {
                item["path"]: item["sha256"]
                for item in repaired_metric_receipt["evidence_artifacts"]
            }
            seen_additions: set[str] = set()
            for index, addition in enumerate(additions):
                addition = expect_object(
                    addition,
                    f"campaign publication repair added artifact {index}",
                    exact_keys=PUBLISHED_CAMPAIGN_REPAIR_ARTIFACT_KEYS,
                )
                relative, path = run_relative_path(
                    outcomes_dir / cohort["run_id"],
                    addition["path"],
                    "campaign publication repaired artifact",
                )
                if relative in seen_additions:
                    raise InputError("campaign publication repair repeats an added artifact")
                seen_additions.add(relative)
                if (
                    not isinstance(addition["sha256"], str)
                    or not SHA256_RE.fullmatch(addition["sha256"])
                    or not path.is_file()
                    or sha256_file(path) != addition["sha256"]
                    or metric_evidence.get(relative) != addition["sha256"]
                ):
                    raise InputError("campaign publication repaired artifact is not bound")
            prior_metric_receipt = {
                **repaired_metric_receipt,
                "evidence_artifacts": [
                    artifact
                    for artifact in repaired_metric_receipt["evidence_artifacts"]
                    if artifact["path"] not in seen_additions
                ],
            }
            if (
                len(prior_metric_receipt["evidence_artifacts"])
                != len(repaired_metric_receipt["evidence_artifacts"])
                - len(seen_additions)
                or sha256_bytes(canonical_json_bytes(prior_metric_receipt)) != prior
            ):
                raise InputError(
                    "campaign publication repair does not reconstruct its prior metric receipt"
                )

    finalized = [event for event in events if event["event"] == "campaign_finalized"]
    if len(finalized) != 1 or finalized[0] is not events[-1 - bool(repair_events)]:
        raise InputError("published campaign has an invalid finalization boundary")
    if finalized[0]["details"] != {
        "status": receipt["status"],
        "receipt_sha256": prior_receipt_sha,
    }:
        raise InputError("published campaign finalization event differs from its receipt chain")

    for cohort in receipt["cohorts"]:
        number = cohort["cohort_number"]
        attached = [
            event
            for event in events
            if event["event"] == "cohort_attached"
            and event["details"].get("cohort_number") == number
        ]
        published = [
            event
            for event in events
            if event["event"] == "cohort_published"
            and event["details"].get("cohort_number") == number
        ]
        if len(attached) != 1 or len(published) != 1:
            raise InputError("published campaign cohort lifecycle events are incomplete")
        if attached[0]["details"] != {
            "cohort_number": number,
            "run_id": cohort["run_id"],
            "gap_brief_sha256": cohort["gap_brief_sha256"],
        }:
            raise InputError("published campaign attachment differs from its receipt")
        if number > 1:
            gap_events = [
                event
                for event in events
                if event["event"] == "gap_brief_created"
                and event["details"].get("cohort_number") == number
            ]
            if len(gap_events) != 1 or gap_events[0]["details"] != {
                "cohort_number": number,
                "gap_brief_sha256": cohort["gap_brief_sha256"],
            }:
                raise InputError("published campaign gap-brief event differs from its receipt")
            if gap_events[0]["sequence"] >= attached[0]["sequence"]:
                raise InputError("published campaign gap brief must precede attachment")
        expected_published = {
            "cohort_number": number,
            "run_id": cohort["run_id"],
            "run_status": cohort["run_status"],
            "report_sha256": cohort["report_sha256"],
            "metrics_sha256": prior_metrics.get(number, cohort["metrics_sha256"]),
            "made_progress": cohort["made_progress"],
            "no_progress_streak": cohort["no_progress_streak"],
            "campaign_status": (
                receipt["status"] if number == len(receipt["cohorts"]) else "active"
            ),
        }
        if published[0]["details"] != expected_published:
            raise InputError("published campaign cohort event differs from its receipt chain")
        if attached[0]["sequence"] >= published[0]["sequence"]:
            raise InputError("published campaign cohort event order is invalid")
    return len(repair_events)


def validate_published_campaign(
    campaign_dir: Path, outcomes_dir: Path
) -> dict[str, Any]:
    _assert_safe_write_path(
        outcomes_dir, campaign_dir, "published campaign outcome directory"
    )
    manifest_path = campaign_dir / "manifest.json"
    receipt_path = campaign_dir / "receipt.json"
    raw_manifest = expect_object(load_json(manifest_path), "published campaign manifest")
    legacy_published = (
        raw_manifest.get("schema_version") == LEGACY_PUBLISHED_SCHEMA_VERSION
    )
    manifest = validate_campaign_manifest(
        raw_manifest, legacy_published=legacy_published
    )
    receipt = expect_object(
        load_json(receipt_path),
        "published campaign receipt",
        exact_keys=(
            LEGACY_CAMPAIGN_RECEIPT_KEYS_V2
            if legacy_published
            else CAMPAIGN_RECEIPT_KEYS
        ),
    )
    if (
        manifest_path.read_bytes() != canonical_json_bytes(manifest)
        or receipt_path.read_bytes() != canonical_json_bytes(receipt)
    ):
        raise InputError("published campaign manifest or receipt is not canonical JSON")
    if (
        receipt["schema_version"]
        != (
            LEGACY_PUBLISHED_SCHEMA_VERSION
            if legacy_published
            else ACTIVE_SCHEMA_VERSION
        )
        or receipt["campaign_id"] != manifest["campaign_id"]
        or receipt["campaign_id"] != campaign_dir.name
        or receipt["campaign_manifest_sha256"] != sha256_file(manifest_path)
        or receipt["cohort_count"] != len(receipt["cohorts"])
        or receipt["quality_objective_achieved"] != (receipt["status"] == "qualified")
    ):
        raise InputError("published campaign receipt identity is invalid")
    founder_path = campaign_dir / "inputs" / "founder.md"
    evaluator_path = campaign_dir / "inputs" / "evaluator.txt"
    if (
        not founder_path.is_file()
        or sha256_file(founder_path) != manifest["founder_sha256"]
        or not evaluator_path.is_file()
    ):
        raise InputError("published campaign canonical inputs are missing or changed")
    factors, evaluator_hash = parse_rubric(evaluator_path)
    if (
        evaluator_hash != manifest["rubric"]["sha256"]
        or [
            {"name": name, "weight": decimal_json(weight)} for name, weight in factors
        ]
        != manifest["rubric"]["factors"]
    ):
        raise InputError("published campaign evaluator differs from its manifest")
    state: dict[str, Any] = {
        "schema_version": receipt["schema_version"],
        "campaign_id": receipt["campaign_id"],
        "status": receipt["status"],
        "created_at": manifest["created_at"],
        "updated_at": manifest["created_at"],
        "active_run_id": None,
        "active_cohort_number": None,
        "cohorts": receipt["cohorts"],
        "no_progress_streak": (
            receipt["cohorts"][-1]["no_progress_streak"] if receipt["cohorts"] else 0
        ),
        "best_official_score": receipt["best_official_score"],
        "best_working_median": receipt["best_working_median"],
        "terminal_reason": receipt["terminal_reason"],
    }
    if legacy_published:
        state["best_working_score"] = receipt["best_working_score"]
        state["seen_archetypes"] = sorted(
            {
                archetype
                for cohort in receipt["cohorts"]
                for archetype in cohort["archetype_scores"]
            }
        )
    validate_campaign_state(
        state, manifest, legacy_published=legacy_published
    )
    validate_campaign_publication_receipts(
        campaign_dir,
        manifest,
        state,
        outcomes_dir=outcomes_dir,
        legacy_published=legacy_published,
    )
    report_path = campaign_dir / "report.md"
    if not report_path.is_file() or report_path.read_bytes() != render_campaign_report(
        receipt
    ).encode("utf-8"):
        raise InputError("published campaign report differs from its receipt")
    repair_count = _validate_published_campaign_events(
        campaign_dir, outcomes_dir, receipt
    )
    return {
        "campaign_id": receipt["campaign_id"],
        "cohort_count": len(receipt["cohorts"]),
        "repair_count": repair_count,
    }


def validate_outcome_quarantine(
    value: Any, label: str, *, history_record: bool = False
) -> dict[str, Any]:
    quarantine = expect_object(
        value,
        label,
        exact_keys=(
            OUTCOME_QUARANTINE_HISTORY_KEYS
            if history_record
            else OUTCOME_QUARANTINE_KEYS
        ),
    )
    if expect_int(quarantine["schema_version"], f"{label}.schema_version") != 1:
        raise InputError(f"{label}.schema_version must be 1")
    if quarantine["record_type"] != "opportunity_outcome_quarantine_v1":
        raise InputError(f"{label}.record_type is invalid")
    run_id = expect_nonempty_string(quarantine["run_id"], f"{label}.run_id")
    if not RUN_ID_RE.fullmatch(run_id):
        raise InputError(f"{label}.run_id is invalid")
    if quarantine["outcome_path"] != f"outcomes/{run_id}":
        raise InputError(f"{label}.outcome_path is invalid")
    report_sha256 = quarantine["report_sha256"]
    if not isinstance(report_sha256, str) or not SHA256_RE.fullmatch(report_sha256):
        raise InputError(f"{label}.report_sha256 is invalid")
    timestamp = expect_nonempty_string(
        quarantine["quarantined_at"], f"{label}.quarantined_at"
    )
    try:
        parsed_timestamp = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InputError(f"{label}.quarantined_at is invalid") from exc
    if not timestamp.endswith("Z") or parsed_timestamp.utcoffset() != dt.timedelta(0):
        raise InputError(f"{label}.quarantined_at must be a UTC timestamp ending in Z")
    reason_code = expect_nonempty_string(
        quarantine["reason_code"], f"{label}.reason_code"
    )
    if reason_code not in OUTCOME_QUARANTINE_REASON_CODES:
        raise InputError(f"{label}.reason_code is unsupported")
    expect_nonempty_string(quarantine["reason"], f"{label}.reason")
    if quarantine["business_decision_eligible"] is not False:
        raise InputError(f"{label}.business_decision_eligible must be false")
    if quarantine["permitted_use"] != "workflow_test_evidence_only":
        raise InputError(f"{label}.permitted_use is invalid")
    if history_record:
        if quarantine["quarantine_path"] != f"outcomes/{run_id}/quarantine.json":
            raise InputError(f"{label}.quarantine_path is invalid")
        quarantine_sha256 = quarantine["quarantine_sha256"]
        if not isinstance(quarantine_sha256, str) or not SHA256_RE.fullmatch(
            quarantine_sha256
        ):
            raise InputError(f"{label}.quarantine_sha256 is invalid")
    return quarantine


def validate_outcome_quarantines(
    outcomes_dir: Path, history_path: Path | None = None
) -> dict[str, Any]:
    history_path = history_path or outcomes_dir.parent / "knowledge" / "history_index.jsonl"
    entries = load_history_entries(history_path)
    history_rows = [
        validate_outcome_quarantine(
            entry, "opportunity outcome quarantine history row", history_record=True
        )
        for entry in entries
        if entry.get("record_type") == "opportunity_outcome_quarantine_v1"
    ]
    by_run: dict[str, dict[str, Any]] = {}
    for row in history_rows:
        if row["run_id"] in by_run:
            raise InputError("knowledge history contains duplicate outcome quarantines")
        by_run[row["run_id"]] = row

    sidecars = [
        path / "quarantine.json"
        for path in sorted(outcomes_dir.iterdir())
        if path.is_dir()
        and RUN_ID_RE.fullmatch(path.name)
        and (path / "quarantine.json").is_file()
    ]
    if sidecars and not history_path.is_file():
        raise InputError("published outcome quarantine is missing its history index")
    if len(sidecars) != len(history_rows):
        raise InputError(
            "published outcome quarantine sidecars and history rows do not reconcile"
        )

    outcome_rows = [
        entry
        for entry in entries
        if entry.get("record_type")
        in {"opportunity_outcome_v1", "opportunity_outcome_v2"}
    ]
    for sidecar_path in sidecars:
        outcome_dir = sidecar_path.parent
        run_id = outcome_dir.name
        if (outcome_dir / "campaign-metrics.json").exists():
            raise InputError("a quarantined outcome cannot remain a campaign cohort")
        sidecar = validate_outcome_quarantine(
            load_json(sidecar_path), f"published outcome quarantine {run_id}"
        )
        if sidecar_path.read_bytes() != canonical_json_bytes(sidecar):
            raise InputError("published outcome quarantine is not canonical JSON")
        if sidecar["run_id"] != run_id:
            raise InputError("published outcome quarantine identity differs from its directory")
        report_path = outcome_dir / "report.json"
        if not report_path.is_file() or sha256_file(report_path) != sidecar["report_sha256"]:
            raise InputError("published outcome quarantine report hash is invalid")
        original_rows = [row for row in outcome_rows if row.get("run_id") == run_id]
        if len(original_rows) != 1:
            raise InputError(
                "published outcome quarantine requires exactly one original history outcome"
            )
        if (
            original_rows[0].get("outcome_path") != sidecar["outcome_path"]
            or original_rows[0].get("report_sha256") != sidecar["report_sha256"]
        ):
            raise InputError(
                "published outcome quarantine differs from its original history outcome"
            )
        history_row = by_run.get(run_id)
        expected_history_row = {
            **sidecar,
            "quarantine_path": f"outcomes/{run_id}/quarantine.json",
            "quarantine_sha256": sha256_file(sidecar_path),
        }
        if history_row != expected_history_row:
            raise InputError(
                "published outcome quarantine differs from its history record"
            )

    meta_entries = [
        entry for entry in entries if entry.get("record_type") == "index_meta"
    ]
    if history_rows:
        if len(meta_entries) != 1:
            raise InputError("outcome quarantines require exactly one history index_meta")
        verification = expect_object(
            meta_entries[0].get("verification"),
            "knowledge history index_meta.verification",
        )
        if verification.get("opportunity_outcome_quarantines") != len(history_rows):
            raise InputError("history quarantine verification count is invalid")
    elif meta_entries:
        verification = expect_object(
            meta_entries[0].get("verification"),
            "knowledge history index_meta.verification",
        )
        if verification.get("opportunity_outcome_quarantines", 0) != 0:
            raise InputError("history quarantine verification count is invalid")
    return {"quarantined_run_count": len(history_rows)}


def quarantine_published_outcome(
    run_id: str,
    outcomes_dir: Path,
    knowledge_dir: Path,
    reason_code: str,
    reason: str,
) -> dict[str, Any]:
    if not RUN_ID_RE.fullmatch(run_id):
        raise InputError("published outcome run id is invalid")
    if reason_code not in OUTCOME_QUARANTINE_REASON_CODES:
        raise InputError(
            "quarantine reason code must be one of: "
            + ", ".join(sorted(OUTCOME_QUARANTINE_REASON_CODES))
        )
    reason = expect_nonempty_string(reason, "quarantine reason")
    outcome_dir = outcomes_dir / run_id
    if not outcome_dir.is_dir():
        raise InputError(f"published outcome does not exist: {run_id}")
    validate_published_run_outcome(outcome_dir)
    if (outcome_dir / "campaign-metrics.json").exists():
        raise ConflictError("campaign cohorts cannot be quarantined independently")

    history_path = knowledge_dir / "history_index.jsonl"
    sidecar_path = outcome_dir / "quarantine.json"
    with file_lock(outcomes_dir / ".publish.lock", root=outcomes_dir):
        entries = load_history_entries(history_path)
        originals = [
            entry
            for entry in entries
            if entry.get("record_type")
            in {"opportunity_outcome_v1", "opportunity_outcome_v2"}
            and entry.get("run_id") == run_id
        ]
        if len(originals) != 1:
            raise InputError(
                "quarantine requires exactly one original published outcome history row"
            )
        report_sha256 = sha256_file(outcome_dir / "report.json")
        if (
            originals[0].get("outcome_path") != f"outcomes/{run_id}"
            or originals[0].get("report_sha256") != report_sha256
        ):
            raise InputError("original history outcome does not bind the published report")

        existing_history = [
            entry
            for entry in entries
            if entry.get("record_type") == "opportunity_outcome_quarantine_v1"
            and entry.get("run_id") == run_id
        ]
        if len(existing_history) > 1:
            raise InputError("knowledge history contains duplicate outcome quarantines")
        if sidecar_path.exists():
            sidecar = validate_outcome_quarantine(
                load_json(sidecar_path), "existing published outcome quarantine"
            )
            if sidecar_path.read_bytes() != canonical_json_bytes(sidecar):
                raise InputError("existing published outcome quarantine is not canonical JSON")
            if sidecar["reason_code"] != reason_code or sidecar["reason"] != reason:
                raise ConflictError(
                    "published outcome is already quarantined with a different reason"
                )
        else:
            if existing_history:
                raise InputError(
                    "outcome quarantine history exists without its immutable sidecar"
                )
            sidecar = validate_outcome_quarantine(
                {
                    "schema_version": 1,
                    "record_type": "opportunity_outcome_quarantine_v1",
                    "run_id": run_id,
                    "outcome_path": f"outcomes/{run_id}",
                    "report_sha256": report_sha256,
                    "quarantined_at": utc_now(),
                    "reason_code": reason_code,
                    "reason": reason,
                    "business_decision_eligible": False,
                    "permitted_use": "workflow_test_evidence_only",
                },
                "published outcome quarantine",
            )
            write_immutable(
                sidecar_path, canonical_json_bytes(sidecar), root=outcome_dir
            )

        expected_history = validate_outcome_quarantine(
            {
                **sidecar,
                "quarantine_path": f"outcomes/{run_id}/quarantine.json",
                "quarantine_sha256": sha256_file(sidecar_path),
            },
            "published outcome quarantine history row",
            history_record=True,
        )
        if existing_history and existing_history[0] != expected_history:
            raise InputError(
                "existing outcome quarantine history differs from its sidecar"
            )
        if not existing_history:
            entries.append(expected_history)
        update_history_verification(entries)
        atomic_write(
            history_path, history_jsonl_bytes(entries), root=knowledge_dir
        )

    validate_outcome_quarantines(outcomes_dir, history_path)
    return {
        "run_id": run_id,
        "outcome_path": f"outcomes/{run_id}",
        "quarantine_path": f"outcomes/{run_id}/quarantine.json",
        "quarantine_sha256": sha256_file(sidecar_path),
        "reason_code": reason_code,
        "business_decision_eligible": False,
        "permitted_use": "workflow_test_evidence_only",
        "idempotent": bool(existing_history),
    }


def validate_published_outcomes(
    outcomes_dir: Path, history_path: Path | None = None
) -> dict[str, Any]:
    run_results = [
        validate_published_run_outcome(path)
        for path in sorted(outcomes_dir.iterdir())
        if path.is_dir() and RUN_ID_RE.fullmatch(path.name)
    ]
    campaigns_root = outcomes_dir / "campaigns"
    campaign_results = (
        [
            validate_published_campaign(path, outcomes_dir)
            for path in sorted(campaigns_root.iterdir())
            if path.is_dir()
        ]
        if campaigns_root.is_dir()
        else []
    )
    quarantines = validate_outcome_quarantines(outcomes_dir, history_path)
    return {
        "run_count": len(run_results),
        "campaign_count": len(campaign_results),
        "campaign_repairs": sum(item["repair_count"] for item in campaign_results),
        **quarantines,
    }


def save_campaign_state(
    campaign_dir: Path, state: dict[str, Any], manifest: Mapping[str, Any]
) -> None:
    state["updated_at"] = utc_now()
    validate_campaign_state(state, manifest)
    atomic_write(
        campaign_dir / "state.json", canonical_json_bytes(state), root=campaign_dir
    )


def load_campaign_events(path: Path, campaign_id: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read campaign event log {path}: {exc}") from exc
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise InputError(f"blank line in campaign event log at {line_number}")
        event = expect_object(
            parse_json(line, source=f"{path}:{line_number}"),
            f"campaign event {line_number}",
            exact_keys=CAMPAIGN_EVENT_KEYS,
        )
        sequence = expect_int(
            event["sequence"], f"campaign event {line_number}.sequence", minimum=1
        )
        if sequence != line_number:
            raise InputError("campaign event sequence is not contiguous")
        expect_nonempty_string(event["at"], f"campaign event {line_number}.at")
        expect_nonempty_string(event["event"], f"campaign event {line_number}.event")
        if event["campaign_id"] != campaign_id:
            raise InputError("campaign event belongs to a different campaign")
        expect_object(event["details"], f"campaign event {line_number}.details")
        events.append(event)
    return events


def append_campaign_event(
    campaign_dir: Path,
    campaign_id: str,
    event_name: str,
    details: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    path = campaign_dir / "events.jsonl"
    events = load_campaign_events(path, campaign_id)
    record = {
        "sequence": len(events) + 1,
        "at": utc_now(),
        "event": expect_nonempty_string(event_name, "campaign event name"),
        "campaign_id": campaign_id,
        "details": dict(details or {}),
    }
    data = "".join(
        json.dumps(item, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        for item in [*events, record]
    ).encode("utf-8")
    atomic_write(path, data, root=campaign_dir)
    return record


def _ensure_campaign_event(
    campaign_dir: Path,
    campaign_id: str,
    event_name: str,
    details: Mapping[str, Any] | None = None,
    *,
    identity: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    expected_details = dict(details or {})
    identity_fields = dict(identity or {})

    def matches_identity(event: Mapping[str, Any]) -> bool:
        return event["event"] == event_name and all(
            event["details"].get(key) == value
            for key, value in identity_fields.items()
        )

    def existing_event() -> dict[str, Any] | None:
        matches = [
            event
            for event in load_campaign_events(
                campaign_dir / "events.jsonl", campaign_id
            )
            if matches_identity(event)
        ]
        if len(matches) > 1:
            raise InputError(f"campaign contains duplicate {event_name} events")
        if matches and matches[0]["details"] != expected_details:
            raise InputError(f"campaign {event_name} event conflicts with canonical state")
        return matches[0] if matches else None

    current = existing_event()
    if current is not None:
        return current
    try:
        append_campaign_event(campaign_dir, campaign_id, event_name, expected_details)
    except BaseException:
        recovered = existing_event()
        if recovered is None:
            raise
        return recovered
    recovered = existing_event()
    if recovered is None:
        raise InputError(f"campaign {event_name} event was not durably recorded")
    return recovered


def reconcile_campaign_events(
    campaign_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
) -> None:
    campaign_id = manifest["campaign_id"]
    _ensure_campaign_event(
        campaign_dir, campaign_id, "campaign_created", identity={}
    )
    allowed_brief_numbers = set(range(2, len(state["cohorts"]) + 1))
    if state["status"] == "active":
        next_number = len(state["cohorts"]) + 1
        if next_number > 1:
            allowed_brief_numbers.add(next_number)
    observed_brief_numbers: set[int] = set()
    for brief_path in sorted((campaign_dir / "briefs").glob("cohort-*.json")):
        match = re.fullmatch(r"cohort-(\d+)\.json", brief_path.name)
        if match is None:
            raise InputError("campaign contains a noncanonical gap brief filename")
        cohort_number = int(match.group(1))
        if cohort_number not in allowed_brief_numbers:
            raise InputError("campaign contains a gap brief for an unexpected cohort")
        observed_brief_numbers.add(cohort_number)
        brief = validate_campaign_gap_brief(
            load_json(brief_path), manifest, cohort_number
        )
        if brief_path.read_bytes() != canonical_json_bytes(brief):
            raise InputError("campaign gap brief is not canonical JSON")
        _ensure_campaign_event(
            campaign_dir,
            campaign_id,
            "gap_brief_created",
            {
                "cohort_number": cohort_number,
                "gap_brief_sha256": sha256_file(brief_path),
            },
            identity={"cohort_number": cohort_number},
        )
    required_brief_numbers = set(range(2, len(state["cohorts"]) + 1))
    if state["active_cohort_number"] is not None and state["active_cohort_number"] > 1:
        required_brief_numbers.add(state["active_cohort_number"])
    if not required_brief_numbers.issubset(observed_brief_numbers):
        raise InputError("campaign is missing a gap brief bound to a cohort")
    for cohort in state["cohorts"]:
        _ensure_campaign_event(
            campaign_dir,
            campaign_id,
            "cohort_attached",
            {
                "cohort_number": cohort["cohort_number"],
                "run_id": cohort["run_id"],
                "gap_brief_sha256": cohort["gap_brief_sha256"],
            },
            identity={"cohort_number": cohort["cohort_number"]},
        )
        _ensure_campaign_event(
            campaign_dir,
            campaign_id,
            "cohort_published",
            {
                "cohort_number": cohort["cohort_number"],
                "run_id": cohort["run_id"],
                "run_status": cohort["run_status"],
                "report_sha256": cohort["report_sha256"],
                "metrics_sha256": cohort["metrics_sha256"],
                "made_progress": cohort["made_progress"],
                "no_progress_streak": cohort["no_progress_streak"],
                "campaign_status": (
                    state["status"]
                    if cohort["cohort_number"] == len(state["cohorts"])
                    else "active"
                ),
            },
            identity={"cohort_number": cohort["cohort_number"]},
        )
    if state["active_run_id"] is not None:
        run_manifest_path = (
            campaign_dir.parent.parent
            / "runs"
            / state["active_run_id"]
            / "manifest.json"
        )
        if not run_manifest_path.is_file():
            raise InputError("campaign active run manifest is missing; restore the run before resuming")
        run_manifest = expect_object(load_json(run_manifest_path), "campaign active run manifest")
        binding = expect_object(
            run_manifest.get("campaign"),
            "campaign active run manifest.campaign",
            exact_keys=CAMPAIGN_BINDING_KEYS,
        )
        if (
            binding["campaign_id"] != campaign_id
            or binding["cohort_number"] != state["active_cohort_number"]
        ):
            raise InputError("campaign active run binding differs from campaign state")
        _ensure_campaign_event(
            campaign_dir,
            campaign_id,
            "cohort_attached",
            {
                "cohort_number": binding["cohort_number"],
                "run_id": state["active_run_id"],
                "gap_brief_sha256": binding["gap_brief_sha256"],
            },
            identity={"cohort_number": binding["cohort_number"]},
        )
    receipt_path = campaign_dir / "receipt.json"
    if receipt_path.exists():
        if state["status"] == "active":
            raise InputError("active campaign contains a terminal receipt")
        _ensure_campaign_event(
            campaign_dir,
            campaign_id,
            "campaign_finalized",
            {
                "status": state["status"],
                "receipt_sha256": sha256_file(receipt_path),
            },
            identity={},
        )
    events = load_campaign_events(campaign_dir / "events.jsonl", campaign_id)
    allowed_names = {
        "campaign_created",
        "gap_brief_created",
        "cohort_attached",
        "cohort_published",
        "campaign_finalized",
    }
    if any(event["event"] not in allowed_names for event in events):
        raise InputError("campaign event log contains an unknown lifecycle event")
    created_events = [event for event in events if event["event"] == "campaign_created"]
    if len(created_events) != 1 or created_events[0]["sequence"] != 1:
        raise InputError("campaign_created must be the first and only creation event")
    published_numbers = {cohort["cohort_number"] for cohort in state["cohorts"]}
    attached_numbers = set(published_numbers)
    if state["active_cohort_number"] is not None:
        attached_numbers.add(state["active_cohort_number"])
    brief_numbers = {
        int(re.fullmatch(r"cohort-(\d+)\.json", path.name).group(1))
        for path in (campaign_dir / "briefs").glob("cohort-*.json")
    }
    expected_numbers = {
        "gap_brief_created": brief_numbers,
        "cohort_attached": attached_numbers,
        "cohort_published": published_numbers,
    }
    sequences: dict[tuple[str, int], int] = {}
    for event in events:
        if event["event"] in expected_numbers:
            number = expect_int(
                event["details"].get("cohort_number"),
                f"campaign {event['event']} cohort_number",
                minimum=1,
            )
            if number not in expected_numbers[event["event"]]:
                raise InputError("campaign event log contains a state-inconsistent cohort event")
            sequences[(event["event"], number)] = event["sequence"]
    for number in attached_numbers:
        attached_sequence = sequences[("cohort_attached", number)]
        if number > 1 and sequences[("gap_brief_created", number)] >= attached_sequence:
            raise InputError("campaign gap brief event must precede cohort attachment")
        if number in published_numbers and attached_sequence >= sequences[("cohort_published", number)]:
            raise InputError("campaign attachment event must precede publication")
    finalized_events = [event for event in events if event["event"] == "campaign_finalized"]
    if bool(finalized_events) != receipt_path.exists() or len(finalized_events) > 1:
        raise InputError("campaign finalization event differs from terminal receipt state")
    if finalized_events and finalized_events[0]["sequence"] != len(events):
        raise InputError("campaign_finalized must be the final lifecycle event")


def new_campaign(config_path: Path, campaigns_dir: Path) -> dict[str, Any]:
    config = validate_config(load_json(config_path))
    founder_source = REPO_ROOT / "PERSONALITY_SITUATION.md"
    evaluator_source = REPO_ROOT / "Personalities" / "ZeroToOne.txt"
    founder_bytes = founder_source.read_bytes()
    evaluator_bytes = evaluator_source.read_bytes()
    factors, rubric_digest = parse_rubric(evaluator_source)
    created_at = utc_now()
    for _ in range(32):
        timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        campaign_id = f"campaign-{timestamp}-{secrets.token_hex(3)}"
        campaign_dir = campaigns_dir / campaign_id
        try:
            campaign_dir.mkdir(parents=True, exist_ok=False)
            break
        except FileExistsError:
            continue
    else:
        raise ConflictError("could not allocate a unique campaign id")
    manifest = {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "campaign_id": campaign_id,
        "created_at": created_at,
        "config": config,
        "config_sha256": sha256_bytes(canonical_json_bytes(config)),
        "founder_sha256": sha256_bytes(founder_bytes),
        "rubric": {
            "rubric_id": config["rubric_id"],
            "sha256": rubric_digest,
            "factors": [
                {"name": name, "weight": decimal_json(weight)}
                for name, weight in factors
            ],
        },
    }
    state = {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "campaign_id": campaign_id,
        "status": "active",
        "created_at": created_at,
        "updated_at": created_at,
        "active_run_id": None,
        "active_cohort_number": None,
        "cohorts": [],
        "no_progress_streak": 0,
        "best_official_score": None,
        "best_working_median": None,
        "terminal_reason": None,
    }
    validate_campaign_manifest(manifest)
    validate_campaign_state(state, manifest)
    write_immutable(
        campaign_dir / "inputs" / "founder.md", founder_bytes, root=campaign_dir
    )
    write_immutable(
        campaign_dir / "inputs" / "evaluator.txt", evaluator_bytes, root=campaign_dir
    )
    write_immutable(
        campaign_dir / "manifest.json", canonical_json_bytes(manifest), root=campaign_dir
    )
    write_immutable(
        campaign_dir / "state.json", canonical_json_bytes(state), root=campaign_dir
    )
    _ensure_campaign_event(campaign_dir, campaign_id, "campaign_created")
    return {
        "campaign_id": campaign_id,
        "campaign_dir": str(campaign_dir),
        "status": "active",
        "next_action": "create_cohort",
    }


def campaign_status(campaign_dir: Path, full_json: bool = False) -> dict[str, Any]:
    with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
        manifest, state = load_campaign(campaign_dir)
        reconcile_campaign_events(campaign_dir, manifest, state)
        validate_campaign_publication_receipts(campaign_dir, manifest, state)
        result = {
            "campaign_id": state["campaign_id"],
            "status": state["status"],
            "cohort_count": len(state["cohorts"]),
            "active_run_id": state["active_run_id"],
            "no_progress_streak": state["no_progress_streak"],
            "best_official_score": state["best_official_score"],
            "best_working_median": state["best_working_median"],
            "terminal_reason": state["terminal_reason"],
        }
        if full_json:
            result["manifest"] = manifest
            result["state"] = state
        return result


def validate_campaign_gap_brief(
    value: Any,
    manifest: Mapping[str, Any],
    cohort_number: int,
    *,
    legacy_published: bool = False,
) -> dict[str, Any]:
    brief = expect_object(
        value, "campaign gap brief", exact_keys=CAMPAIGN_GAP_BRIEF_KEYS
    )
    expected_schema = (
        LEGACY_PUBLISHED_SCHEMA_VERSION if legacy_published else ACTIVE_SCHEMA_VERSION
    )
    if expect_int(
        brief["schema_version"], "campaign gap brief.schema_version"
    ) != expected_schema:
        raise InputError(
            f"campaign gap brief.schema_version must be {expected_schema}"
        )
    if brief["campaign_id"] != manifest["campaign_id"]:
        raise InputError("campaign gap brief identity differs from campaign")
    if expect_int(brief["cohort_number"], "campaign gap brief.cohort_number", minimum=2) != cohort_number:
        raise InputError("campaign gap brief cohort number is not next in sequence")
    deficient = expect_string_list(
        brief["deficient_factors"], "campaign gap brief.deficient_factors", unique=True
    )
    if len(deficient) > 3 or not set(deficient).issubset(
        _campaign_factor_names(manifest)
    ):
        raise InputError("campaign gap brief deficient_factors must name up to three rubric factors")
    _validate_gap_archetype_labels(
        brief["missing_archetypes"], "campaign gap brief.missing_archetypes"
    )
    return brief


def _prepare_campaign_binding(
    campaign_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest, state = load_campaign(campaign_dir)
    reconcile_campaign_events(campaign_dir, manifest, state)
    validate_campaign_publication_receipts(campaign_dir, manifest, state)
    if state["status"] != "active":
        raise ConflictError(f"campaign is terminal: {state['status']}")
    if state["active_run_id"] is not None:
        raise ConflictError(
            f"campaign already has active run {state['active_run_id']}"
        )
    cohort_number = len(state["cohorts"]) + 1
    if cohort_number > manifest["config"]["campaign_max_cohorts"]:
        raise ConflictError("campaign has reached campaign_max_cohorts")
    gap_path: str | None = None
    gap_digest: str | None = None
    if cohort_number > 1:
        gap_path = f"briefs/cohort-{cohort_number}.json"
        path = campaign_dir / gap_path
        if not path.is_file():
            raise ConflictError(
                "run campaign next before attaching the next cohort"
            )
        brief = validate_campaign_gap_brief(
            load_json(path), manifest, cohort_number
        )
        if path.read_bytes() != canonical_json_bytes(brief):
            raise InputError("campaign gap brief is not canonical")
        gap_digest = sha256_file(path)
    binding = {
        "campaign_id": state["campaign_id"],
        "cohort_number": cohort_number,
        "gap_brief_path": gap_path,
        "gap_brief_sha256": gap_digest,
    }
    return manifest, state, binding


def make_run(
    config_path: Path,
    runs_dir: Path,
    campaign_id: str | None = None,
    campaigns_dir: Path | None = None,
) -> dict[str, Any]:
    config = validate_config(load_json(config_path))
    campaign_dir: Path | None = None
    campaign_binding: dict[str, Any] | None = None
    if campaign_id is not None:
        storage = (campaigns_dir or campaign_storage_for_runs(runs_dir)).resolve()
        campaign_dir = resolve_campaign(storage, campaign_id)
        with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
            campaign_manifest, _, campaign_binding = _prepare_campaign_binding(campaign_dir)
            config = campaign_manifest["config"]
    rubric_path = (
        campaign_dir / "inputs" / "evaluator.txt"
        if campaign_dir is not None
        else REPO_ROOT / "Personalities" / "ZeroToOne.txt"
    )
    factors, rubric_digest = parse_rubric(rubric_path)
    if campaign_dir is not None:
        campaign_rubric = campaign_manifest["rubric"]
        expected_factors = [
            {"name": name, "weight": decimal_json(weight)}
            for name, weight in factors
        ]
        if (
            campaign_rubric["rubric_id"] != config["rubric_id"]
            or campaign_rubric["sha256"] != rubric_digest
            or campaign_rubric["factors"] != expected_factors
        ):
            raise InputError("run rubric differs from the immutable campaign rubric")
    # Configuration identity is semantic.  Key order and insignificant JSON
    # formatting must not change a run's immutable source binding.
    config_source_bytes = canonical_json_bytes(config)
    config_source_digest = sha256_bytes(config_source_bytes)
    source_hashes: dict[str, str] = {}
    source_bytes: dict[str, bytes] = {}
    for relative in SOURCE_PATHS:
        path = REPO_ROOT / relative
        if relative == "config/opportunity-workflow.json":
            source_hashes[relative] = config_source_digest
            source_bytes[relative] = config_source_bytes
        elif campaign_dir is not None and relative == "PERSONALITY_SITUATION.md":
            source_bytes[relative] = (campaign_dir / "inputs" / "founder.md").read_bytes()
            source_hashes[relative] = sha256_bytes(source_bytes[relative])
        elif campaign_dir is not None and relative == "Personalities/ZeroToOne.txt":
            source_bytes[relative] = (campaign_dir / "inputs" / "evaluator.txt").read_bytes()
            source_hashes[relative] = sha256_bytes(source_bytes[relative])
        else:
            if not path.is_file():
                raise InputError(f"required source file is missing: {relative}")
            source_hashes[relative] = sha256_file(path)
            source_bytes[relative] = path.read_bytes()
    created_at = utc_now()
    for _ in range(32):
        timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_id = f"{timestamp}-{secrets.token_hex(3)}"
        run_dir = runs_dir / run_id
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
            break
        except FileExistsError:
            continue
    else:
        raise ConflictError("could not allocate a unique run id")
    manifest = {
        "schema_version": config["schema_version"],
        "run_id": run_id,
        "created_at": created_at,
        "config": config,
        "source_hashes": source_hashes,
        "rubric": {
            "rubric_id": config["rubric_id"],
            "sha256": rubric_digest,
            "factors": [{"name": name, "weight": decimal_json(weight)} for name, weight in factors],
        },
    }
    manifest["campaign"] = campaign_binding
    state = {
        "schema_version": config["schema_version"],
        "run_id": run_id,
        "stage": "initialized",
        "run_status": "active",
        "updated_at": created_at,
        "jobs": {stage: {} for stage in STAGES},
    }
    validate_manifest(manifest)
    validate_state(state, manifest)
    try:
        for source, snapshot in INPUT_SNAPSHOTS.items():
            write_immutable(run_dir / snapshot, source_bytes[source], root=run_dir)
        write_immutable(run_dir / "manifest.json", canonical_json_bytes(manifest), root=run_dir)
        write_immutable(run_dir / "state.json", canonical_json_bytes(state), root=run_dir)
        append_event(run_dir, state, "run_created", details={"source_hashes": source_hashes})
        if campaign_dir is not None and campaign_binding is not None:
            with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
                campaign_manifest, campaign_state, current_binding = _prepare_campaign_binding(
                    campaign_dir
                )
                if current_binding != campaign_binding:
                    raise ConflictError("campaign attachment changed while the run was created")
                campaign_state["active_run_id"] = run_id
                campaign_state["active_cohort_number"] = campaign_binding["cohort_number"]
                save_campaign_state(campaign_dir, campaign_state, campaign_manifest)
                _ensure_campaign_event(
                    campaign_dir,
                    campaign_state["campaign_id"],
                    "cohort_attached",
                    {
                        "cohort_number": campaign_binding["cohort_number"],
                        "run_id": run_id,
                        "gap_brief_sha256": campaign_binding["gap_brief_sha256"],
                    },
                    identity={"cohort_number": campaign_binding["cohort_number"]},
                )
    except BaseException:
        # A just-created empty run directory has no historical value.  Keep any
        # partially written files visible rather than attempting broad cleanup.
        raise
    result = {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "stage": "initialized",
        "run_status": "active",
    }
    if campaign_binding is not None:
        result["campaign"] = campaign_binding
    return result


def assert_active(state: Mapping[str, Any]) -> None:
    if state["stage"] == "complete" or state["run_status"] != "active":
        raise ConflictError(f"run is terminal: {state['run_status']}")


def job_is_retryable(job: Mapping[str, Any]) -> bool:
    return job["status"] in RETRYABLE_JOB_STATUSES and job["attempts"] < job["max_attempts"]


def job_is_exhausted(job: Mapping[str, Any]) -> bool:
    return (
        job["status"] in {"failed", "interrupted"}
        and job["attempts"] >= job["max_attempts"]
    )


def current_stage_blockers(state: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    for job_id, job in state["jobs"][state["stage"]].items():
        if job["status"] == "running" or job_is_retryable(job):
            blockers.append(job_id)
    return sorted(blockers)


def start_job(run_dir: Path, job_id: str, requested_stage: str | None) -> dict[str, Any]:
    if not SAFE_JOB_RE.fullmatch(job_id):
        raise InputError("JOB_ID is not path-safe")
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        stage = state["stage"]
        if requested_stage is not None and requested_stage != stage:
            raise ConflictError(f"requested stage {requested_stage} differs from current stage {stage}")
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, _ = project_transition_state(events)
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before job start")
        recovered = _recover_trailing_job_event(
            run_dir,
            manifest,
            state,
            event_name="job_started",
            job_id=job_id,
        )
        if recovered is not None:
            recovered_job = state["jobs"][stage][job_id]
            return {
                "run_id": state["run_id"],
                "stage": stage,
                "job_id": job_id,
                **recovered_job,
                "idempotent": True,
            }
        jobs = state["jobs"][stage]
        if job_id not in jobs:
            attempt = 1
            maximum = manifest["config"]["mechanical_attempts"]
        else:
            job = jobs[job_id]
            if job["status"] == "running":
                raise ConflictError(f"job is already running: {job_id}")
            if job["status"] in TERMINAL_JOB_STATUSES:
                raise ConflictError(f"job is terminal: {job_id} ({job['status']})")
            if not job_is_retryable(job):
                raise ConflictError(f"job exhausted {job['max_attempts']} attempts: {job_id}")
            attempt = job["attempts"] + 1
            maximum = job["max_attempts"]
        event = append_event(
            run_dir,
            state,
            "job_started",
            job_id=job_id,
            details={"attempt": attempt, "max_attempts": maximum},
        )
        jobs[job_id] = _projected_job_record(
            status="running",
            attempts=attempt,
            max_attempts=maximum,
            at=event["at"],
        )
        save_state(run_dir, state, manifest)
        return {
            "run_id": state["run_id"],
            "stage": stage,
            "job_id": job_id,
            **jobs[job_id],
            "idempotent": False,
        }


def fail_job(run_dir: Path, job_id: str, error: str) -> dict[str, Any]:
    if not SAFE_JOB_RE.fullmatch(job_id):
        raise InputError("JOB_ID is not path-safe")
    message = expect_nonempty_string(error, "--error")
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, _ = project_transition_state(events)
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before job failure")
        recovered = _recover_trailing_job_event(
            run_dir,
            manifest,
            state,
            event_name="job_failed",
            job_id=job_id,
        )
        if recovered is not None:
            recovered_job = state["jobs"][state["stage"]][job_id]
            return {
                "run_id": state["run_id"],
                "stage": state["stage"],
                "job_id": job_id,
                **recovered_job,
                "retryable": job_is_retryable(recovered_job),
                "idempotent": True,
            }
        jobs = state["jobs"][state["stage"]]
        if job_id not in jobs:
            raise InputError(f"unknown job in current stage: {job_id}")
        job = jobs[job_id]
        if job["status"] != "running":
            raise ConflictError(f"only a running job can fail: {job_id} is {job['status']}")
        _fail_running_job_locked(run_dir, manifest, state, job_id, message)
        return {
            "run_id": state["run_id"],
            "stage": state["stage"],
            "job_id": job_id,
            **job,
            "retryable": job_is_retryable(job),
            "idempotent": False,
        }


def _fail_running_job_locked(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: dict[str, Any],
    job_id: str,
    message: str,
) -> None:
    job = state["jobs"][state["stage"]][job_id]
    if job["status"] != "running":
        raise ConflictError(f"only a running job can fail: {job_id} is {job['status']}")
    retryable = job["attempts"] < job["max_attempts"]
    event = append_event(
        run_dir,
        state,
        "job_failed",
        job_id=job_id,
        details={"attempt": job["attempts"], "error": message, "retryable": retryable},
    )
    job.update({"status": "failed", "error": message, "updated_at": event["at"]})
    save_state(run_dir, state, manifest)


def _artifact_for_input(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    job_id: str,
    input_path: Path,
    kind: str,
) -> tuple[str, bytes, dict[str, Any] | None]:
    if not input_path.is_file():
        raise InputError(f"input artifact not found: {input_path}")
    if kind == "candidate":
        canonical = validate_candidate(load_json(input_path), manifest, run_dir)
        if canonical["stage"] != state["stage"]:
            raise ConflictError(
                f"candidate stage {canonical['stage']} differs from current run stage {state['stage']}"
            )
        if state["stage"] not in {"discovery", "development"}:
            raise ConflictError(f"candidate artifacts are not accepted during {state['stage']}")
        relative = candidate_relpath(canonical["candidate_id"], canonical["version"])
        existing_candidate_paths = [
            path
            for path, item in iter_candidates(run_dir, manifest)
            if item["stage"] == state["stage"]
        ]
        if state["stage"] == "discovery":
            discovery_maximum = (
                manifest["config"]["scouts"] * manifest["config"]["seeds_per_scout"]
                + manifest["config"]["gap_scout_max"]
            )
            if not (run_dir / relative).exists() and len(existing_candidate_paths) >= discovery_maximum:
                raise ConflictError(f"discovery candidate artifact limit is {discovery_maximum}")
        if state["stage"] == "development":
            parent = canonical["parent"]
            if parent is None:
                raise ConflictError("development candidate requires a researched parent")
            parent_path = run_dir / candidate_relpath(parent["candidate_id"], parent["version"])
            parent_candidate = validate_candidate(load_json(parent_path), manifest, run_dir)
            decision = _load_portfolio_decision(run_dir, manifest)
            selected = {
                (item["candidate_id"], item["candidate_version"], item["candidate_sha256"])
                for item in decision["candidate_decisions"]
                if item["disposition"] == "develop"
            }
            binding = (
                parent_candidate["candidate_id"],
                parent_candidate["version"],
                sha256_file(parent_path),
            )
            if binding not in selected:
                raise ConflictError("development redesign parent is not selected by the canonical portfolio decision")
            if (
                run_dir
                / "development"
                / canonical["candidate_id"]
                / "constructor-result.json"
            ).is_file():
                raise ConflictError(
                    "a development redesign cannot be added after its constructor result"
                )
            research_path = run_dir / research_relpath(
                parent_candidate["candidate_id"], parent_candidate["version"]
            )
            if not research_path.is_file():
                raise ConflictError("development redesign requires canonical research for its exact parent")
            research = validate_research(load_json(research_path), manifest, run_dir)
            if control_contract_enabled(manifest["config"]):
                validate_development_control_resolution(canonical, research)
            if len(
                _working_evaluations_for_candidate(
                    run_dir,
                    manifest,
                    parent_path,
                    parent_candidate,
                    "working_research",
                )
            ) != 1:
                raise ConflictError("development redesign requires the research working evaluation")
        return relative, canonical_json_bytes(canonical), canonical
    if kind in {"evaluation", "secondary-evaluation"}:
        expected_type = (
            "working_screening_secondary"
            if kind == "secondary-evaluation" and state["stage"] == "calibration"
            else {
                "calibration": "working_screening",
                "research": "working_research",
                "development": "working_development",
                "holdout": "holdout_native",
            }.get(state["stage"])
            if kind == "evaluation"
            else None
        )
        if expected_type is None:
            raise ConflictError(f"evaluation artifacts are not accepted during {state['stage']}")
        canonical = canonicalize_evaluator_response(
            load_json(input_path), manifest, run_dir, expected_type
        )
        relative = evaluation_relpath(
            canonical["candidate_id"], canonical["candidate_version"], canonical["evaluation_type"], canonical["judge_id"]
        )
        candidate_path = run_dir / candidate_relpath(
            canonical["candidate_id"], canonical["candidate_version"]
        )
        candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
        if expected_type == "working_screening":
            batches = load_screening_batches(run_dir, manifest)
            batch_by_candidate = {
                ref["candidate_id"]: batch["batch_id"]
                for batch in batches["batches"]
                for ref in batch["candidate_refs"]
            }
            batch_id = batch_by_candidate.get(canonical["candidate_id"])
            if batch_id is None:
                raise ConflictError(
                    "screening evaluation candidate is not in a canonical screening batch"
                )
            for _, evaluation in iter_evaluations(run_dir, manifest):
                if evaluation["evaluation_type"] != "working_screening":
                    continue
                other_batch = batch_by_candidate.get(evaluation["candidate_id"])
                if other_batch == batch_id and evaluation["judge_id"] != canonical["judge_id"]:
                    raise ConflictError(
                        "every candidate in one screening batch must use the same fresh evaluator"
                    )
                if other_batch != batch_id and evaluation["judge_id"] == canonical["judge_id"]:
                    raise ConflictError(
                        "a screening evaluator identity cannot be reused across batches"
                    )
        elif expected_type == "working_screening_secondary":
            plan = load_secondary_screening_plan(run_dir, manifest)
            batch_by_candidate = {
                ref["candidate_id"]: batch["secondary_batch_id"]
                for batch in plan["batches"]
                for ref in batch["candidate_refs"]
            }
            batch_id = batch_by_candidate.get(canonical["candidate_id"])
            if batch_id is None:
                raise ConflictError(
                    "secondary screening candidate is not in the deterministic close-cutoff set"
                )
            primary_judges = {
                evaluation["judge_id"]
                for _, evaluation in iter_evaluations(run_dir, manifest)
                if evaluation["evaluation_type"] == "working_screening"
            }
            if canonical["judge_id"] in primary_judges:
                raise ConflictError(
                    "secondary screening evaluator must be fresh from primary screening"
                )
            for _, evaluation in iter_evaluations(run_dir, manifest):
                if evaluation["evaluation_type"] != "working_screening_secondary":
                    continue
                other_batch = batch_by_candidate.get(evaluation["candidate_id"])
                if other_batch == batch_id and evaluation["judge_id"] != canonical["judge_id"]:
                    raise ConflictError(
                        "every candidate in one secondary set must use the same fresh evaluator"
                    )
                if other_batch != batch_id and evaluation["judge_id"] == canonical["judge_id"]:
                    raise ConflictError(
                        "a secondary screening evaluator identity cannot be reused across sets"
                    )
        elif expected_type == "working_research":
            selected = {
                (item["candidate_id"], item["version"], item["candidate_sha256"])
                for item in effective_portfolio_selection(run_dir, manifest)["candidate_refs"]
            }
            identity = (
                canonical["candidate_id"],
                canonical["candidate_version"],
                canonical["candidate_sha256"],
            )
            if identity not in selected:
                raise ConflictError("research evaluation candidate is not in the effective shortlist")
            if not (run_dir / research_relpath(*identity[:2])).is_file():
                raise ConflictError("research evaluation requires canonical research for the exact candidate")
            if score_bracket_enabled(manifest["config"]):
                screening_judges = {
                    evaluation["judge_id"]
                    for _, evaluation in iter_evaluations(run_dir, manifest)
                    if evaluation["evaluation_type"]
                    in {"working_screening", "working_screening_secondary"}
                }
                if canonical["judge_id"] in screening_judges:
                    raise ConflictError(
                        "research evaluator must be fresh from screening roles"
                    )
        elif expected_type == "working_development":
            _, result = _development_result_for_candidate(
                run_dir, manifest, canonical["candidate_id"]
            )
            allowed = {
                (
                    result["base_candidate_version"],
                    result["base_candidate_sha256"],
                )
            }
            if result["outcome"] == "redesigned":
                allowed.add(
                    (
                        result["final_candidate_version"],
                        result["final_candidate_sha256"],
                    )
                )
            identity = (
                canonical["candidate_version"],
                canonical["candidate_sha256"],
            )
            if score_bracket_enabled(manifest["config"]):
                if identity not in allowed:
                    raise ConflictError(
                        "development evaluation must bind the immutable base or its authorized redesign"
                    )
                paired_judges = {
                    evaluation["judge_id"]
                    for _, evaluation in iter_evaluations(run_dir, manifest)
                    if evaluation["evaluation_type"] == "working_development"
                    and evaluation["candidate_id"] == canonical["candidate_id"]
                }
                evaluator_limit = (
                    manifest["config"]["development_evaluators_per_lineage"]
                    if control_contract_enabled(manifest["config"])
                    else 1
                )
                if len(paired_judges | {canonical["judge_id"]}) > evaluator_limit:
                    raise ConflictError(
                        "development evaluator set exceeds the configured lineage limit"
                    )
                if control_contract_enabled(manifest["config"]):
                    other_lineage_judges = {
                        evaluation["judge_id"]
                        for _, evaluation in iter_evaluations(run_dir, manifest)
                        if evaluation["evaluation_type"] == "working_development"
                        and evaluation["candidate_id"] != canonical["candidate_id"]
                    }
                    if canonical["judge_id"] in other_lineage_judges:
                        raise ConflictError(
                            "development evaluator identity cannot be reused across lineages"
                        )
                earlier_judges = {
                    evaluation["judge_id"]
                    for _, evaluation in iter_evaluations(run_dir, manifest)
                    if evaluation["evaluation_type"]
                    in {
                        "working_screening",
                        "working_screening_secondary",
                        "working_research",
                    }
                }
                if canonical["judge_id"] in earlier_judges:
                    raise ConflictError(
                        "development evaluator must be fresh from screening and research roles"
                    )
            elif identity != (
                result["final_candidate_version"],
                result["final_candidate_sha256"],
            ):
                raise ConflictError(
                    "development evaluation must bind the exact constructor final candidate"
                )
        else:
            finalist_identities = {
                (item["candidate_id"], item["version"], item["candidate_sha256"])
                for item in load_finalist_selection(run_dir, manifest)["candidate_refs"]
            }
            identity = (
                canonical["candidate_id"],
                canonical["candidate_version"],
                canonical["candidate_sha256"],
            )
            if identity not in finalist_identities:
                raise ConflictError("native holdout response must bind an exact frozen finalist ref")
        if canonical["evaluation_type"].startswith("working_"):
            root = run_dir / "evaluations" / canonical["candidate_id"] / f"v{canonical['candidate_version']}"
            prefix = {
                "working_screening": "screening-",
                "working_screening_secondary": "screening-secondary-",
                "working_research": "research-",
                "working_development": "development-",
            }[canonical["evaluation_type"]]
            existing = [
                path
                for path in root.glob(f"{prefix}*.json")
                if path.relative_to(run_dir).as_posix() != relative
            ]
            phase_limit = (
                manifest["config"]["development_evaluators_per_lineage"]
                if canonical["evaluation_type"] == "working_development"
                and control_contract_enabled(manifest["config"])
                else 1
            )
            if len(existing) >= phase_limit:
                raise ConflictError(
                    "the active workflow already has the configured evaluations for this candidate and phase"
                )
        if canonical["evaluation_type"] == "holdout_native":
            existing_evaluations = list(iter_evaluations(run_dir, manifest))
            working_ids = {
                evaluation["judge_id"]
                for _, evaluation in existing_evaluations
                if evaluation["evaluation_type"].startswith("working_")
            }
            native_ids = {
                evaluation["judge_id"]
                for path, evaluation in existing_evaluations
                if evaluation["evaluation_type"] == "holdout_native"
                and path.relative_to(run_dir).as_posix() != relative
            }
            constructor_ids = {
                result["constructor_id"]
                for result_path in sorted((run_dir / "development").glob("*/constructor-result.json"))
                for result in [validate_development_result(load_json(result_path), manifest, run_dir)]
            }
            if canonical["judge_id"] in working_ids | constructor_ids:
                raise ConflictError("native holdout judge must be fresh and independent of development roles")
            if canonical["judge_id"] in native_ids:
                raise ConflictError("native holdout judge identity cannot be reused")
        return relative, canonical_json_bytes(canonical), canonical
    if kind == "research":
        if state["stage"] != "research":
            raise ConflictError("research artifacts are accepted only during research stage")
        canonical = validate_research(load_json(input_path), manifest, run_dir)
        selected = {
            (item["candidate_id"], item["version"], item["candidate_sha256"])
            for item in effective_portfolio_selection(run_dir, manifest)["candidate_refs"]
        }
        identity = (
            canonical["candidate_id"],
            canonical["candidate_version"],
            canonical["candidate_sha256"],
        )
        if identity not in selected:
            raise ConflictError(
                "research candidate is not bound to the effective selection; use a versioned portfolio amendment"
            )
        relative = research_relpath(canonical["candidate_id"], canonical["candidate_version"])
        return relative, canonical_json_bytes(canonical), canonical
    if kind == "portfolio-selection":
        if state["stage"] != "calibration":
            raise ConflictError("portfolio-selection artifacts are accepted only during calibration")
        if score_bracket_enabled(manifest["config"]):
            raise ConflictError(
                "score-bracket portfolio selection is generated deterministically by advance"
            )
        canonical = validate_portfolio_selection(load_json(input_path), manifest, run_dir)
        return "portfolio/selection.json", canonical_json_bytes(canonical), canonical
    if kind == "portfolio-amendment":
        if state["stage"] != "research":
            raise ConflictError("portfolio-amendment artifacts are accepted only during research")
        if score_bracket_enabled(manifest["config"]):
            raise ConflictError(
                "score-bracket shortlists are immutable and do not accept manual amendments"
            )
        if (run_dir / "portfolio" / "development-decision.json").exists():
            raise ConflictError("portfolio amendments cannot follow the development decision")
        effective = effective_portfolio_selection(run_dir, manifest)
        expected_version = len(effective["amendments"]) + 1
        canonical, _, _ = _validate_portfolio_amendment_record(
            load_json(input_path), manifest, run_dir,
            expected_version=expected_version,
            expected_base_digest=effective["latest_binding_sha256"],
            current_refs=effective["candidate_refs"],
            current_wildcard_refs=effective["wildcard_candidate_refs"],
            calibrated_refs=effective["calibrated_refs"],
            calibration_rows=effective["calibration"],
        )
        return f"portfolio/amendments/v{expected_version}.json", canonical_json_bytes(canonical), canonical
    if kind == "portfolio-decision":
        if state["stage"] != "research":
            raise ConflictError("portfolio-decision artifacts are accepted only during research")
        canonical = validate_portfolio_decision(load_json(input_path), manifest, run_dir)
        return "portfolio/development-decision.json", canonical_json_bytes(canonical), canonical
    if kind == "development-result":
        if state["stage"] != "development":
            raise ConflictError("development-result artifacts are accepted only during development")
        canonical = canonicalize_development_response(
            load_json(input_path), manifest, run_dir
        )
        working_ids = {
            evaluation["judge_id"]
            for _, evaluation in iter_evaluations(run_dir, manifest)
            if evaluation["evaluation_type"].startswith("working_")
        }
        if canonical["constructor_id"] in working_ids:
            raise ConflictError(
                "development constructor and working evaluator roles must be independent"
            )
        relative = f"development/{canonical['candidate_id']}/constructor-result.json"
        return relative, canonical_json_bytes(canonical), canonical
    if kind != "generic":
        raise InputError(f"unsupported artifact kind: {kind}")
    data = validate_generic_input(input_path, kind)
    suffix = input_path.suffix.lower() if re.fullmatch(r"\.[A-Za-z0-9]{1,10}", input_path.suffix) else ".bin"
    if state["stage"] == "discovery":
        relative = f"discovery/{job_id}{suffix}"
    elif state["stage"] == "holdout":
        relative = f"holdout/jobs/{job_id}{suffix}"
    else:
        relative = f"artifacts/{state['stage']}/{job_id}{suffix}"
    return relative, data, None


def complete_job(
    run_dir: Path,
    job_id: str,
    input_path: Path,
    kind: str,
    preflight_sha256: str | None = None,
    preflight_receipt_sha256: str | None = None,
) -> dict[str, Any]:
    if not SAFE_JOB_RE.fullmatch(job_id):
        raise InputError("JOB_ID is not path-safe")
    if preflight_sha256 is not None:
        if not SHA256_RE.fullmatch(preflight_sha256):
            raise InputError("--preflight-sha256 must be a lowercase SHA-256 digest")
        if not input_path.is_file():
            raise InputError(f"input artifact not found: {input_path}")
        if sha256_file(input_path) != preflight_sha256:
            raise ConflictError(
                "job input bytes differ from the successful preflight artifact"
            )
    if preflight_receipt_sha256 is not None and not SHA256_RE.fullmatch(
        preflight_receipt_sha256
    ):
        raise InputError(
            "--preflight-receipt-sha256 must be a lowercase SHA-256 digest"
        )
    if preflight_receipt_sha256 is not None and preflight_sha256 is None:
        raise InputError(
            "--preflight-receipt-sha256 requires --preflight-sha256"
        )
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        attestation_required = (
            preflight_attestation_enabled(manifest["config"])
            and kind in PREFLIGHT_ARTIFACT_KINDS
        )
        if attestation_required and (
            preflight_sha256 is None or preflight_receipt_sha256 is None
        ):
            raise InputError(
                "structured job completion requires --preflight-sha256 and "
                "--preflight-receipt-sha256"
            )
        if not attestation_required and preflight_receipt_sha256 is not None:
            raise InputError(
                "--preflight-receipt-sha256 is not enabled for this job"
            )
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, _ = project_transition_state(events)
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before job completion")
        state_job = state["jobs"][state["stage"]].get(job_id)
        trailing_event = events[-1] if events else None
        if (
            state_job is not None
            and state_job["status"] == "running"
            and trailing_event is not None
            and trailing_event["event"] == "job_failed"
            and trailing_event["job_id"] == job_id
            and trailing_event["stage"] == state["stage"]
        ):
            _recover_trailing_job_event(
                run_dir,
                manifest,
                state,
                event_name="job_failed",
                job_id=job_id,
            )
        jobs = state["jobs"][state["stage"]]
        if job_id not in jobs:
            raise InputError(f"unknown job in current stage: {job_id}")
        job = jobs[job_id]
        if job["status"] not in {"running", "completed"}:
            raise ConflictError(f"only a running job can complete: {job_id} is {job['status']}")
        try:
            relative, data, _ = _artifact_for_input(
                run_dir, manifest, state, job_id, input_path, kind
            )
        except WorkflowError as exc:
            output_roles = {
                "candidate": "candidate",
                "development-result": "constructor",
                "evaluation": "evaluator",
                "secondary-evaluation": "evaluator",
            }
            if kind == "research" and isinstance(exc, InputError):
                output_roles[kind] = "researcher"
            if kind in output_roles and job["status"] == "running":
                _fail_running_job_locked(
                    run_dir,
                    manifest,
                    state,
                    job_id,
                    f"mechanical {output_roles[kind]} output failure: {exc}",
                )
            raise
        digest = sha256_bytes(data)
        preflight_receipt: dict[str, Any] | None = None
        if attestation_required:
            assert preflight_sha256 is not None
            assert preflight_receipt_sha256 is not None
            preflight_receipt = build_preflight_receipt(
                manifest,
                state["stage"],
                job_id,
                kind,
                preflight_sha256,
                digest,
            )
            if preflight_receipt["receipt_sha256"] != preflight_receipt_sha256:
                raise ConflictError(
                    "preflight receipt differs from the structured completion context"
                )
        completion_details: dict[str, Any] = {
            "artifact": relative,
            "artifact_sha256": digest,
            "kind": kind,
        }
        if preflight_receipt is not None:
            completion_details["preflight_receipt"] = preflight_receipt
        if job["status"] == "completed":
            if job["artifact_sha256"] == digest and job["artifact"] == relative:
                completion_logged = any(
                    event["event"] == "job_completed"
                    and event["job_id"] == job_id
                    and event["details"].get("artifact_sha256") == digest
                    for event in load_events(run_dir / "events.jsonl", state["run_id"])
                )
                if not completion_logged:
                    projected = project_job_lifecycle(events, manifest)
                    projected_job = projected[state["stage"]].get(job_id)
                    if (
                        projected_job is None
                        or projected_job["status"] != "running"
                        or projected_job["attempts"] != job["attempts"]
                        or projected_job["max_attempts"] != job["max_attempts"]
                    ):
                        raise InputError(
                            "completed job state is not recoverable from its preceding lifecycle events"
                        )
                    append_event(
                        run_dir,
                        state,
                        "job_completed",
                        job_id=job_id,
                        details={
                            **completion_details,
                            "recovered_after_state_commit": True,
                        },
                    )
                else:
                    require_job_event_state_match(events, state, manifest)
                return {
                    "run_id": state["run_id"],
                    "stage": state["stage"],
                    "job_id": job_id,
                    **job,
                    "idempotent": True,
                }
            raise ConflictError(f"completed job artifact differs: {job_id}")
        require_job_event_state_match(events, state, manifest)
        write_immutable(run_dir / relative, data, root=run_dir)
        job.update(
            {
                "status": "completed",
                "artifact": relative,
                "artifact_sha256": digest,
                "error": None,
                "updated_at": utc_now(),
            }
        )
        save_state(run_dir, state, manifest)
        append_event(
            run_dir,
            state,
            "job_completed",
            job_id=job_id,
            details=completion_details,
        )
        return {
            "run_id": state["run_id"],
            "stage": state["stage"],
            "job_id": job_id,
            **job,
            "idempotent": False,
        }


def resume_run(run_dir: Path) -> dict[str, Any]:
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, _ = project_transition_state(events)
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before resume")
        recovered = _recover_trailing_job_event(
            run_dir,
            manifest,
            state,
            event_name="run_resumed",
        )
        if recovered is not None:
            interrupted = list(recovered["details"]["interrupted_jobs"])
            eligible = [
                {
                    "stage": stage,
                    "job_id": job_id,
                    "status": job["status"],
                    "attempts": job["attempts"],
                    "max_attempts": job["max_attempts"],
                }
                for stage in STAGES
                for job_id, job in state["jobs"][stage].items()
                if job_is_retryable(job)
            ]
            exhausted = [
                {
                    "stage": stage,
                    "job_id": job_id,
                    "status": job["status"],
                    "attempts": job["attempts"],
                    "max_attempts": job["max_attempts"],
                    "error": job["error"],
                }
                for stage in STAGES
                for job_id, job in state["jobs"][stage].items()
                if job_is_exhausted(job)
            ]
            return {
                "run_id": state["run_id"],
                "stage": state["stage"],
                "interrupted": interrupted,
                "eligible_jobs": sorted(eligible, key=lambda item: (item["stage"], item["job_id"])),
                "exhausted_jobs": sorted(exhausted, key=lambda item: (item["stage"], item["job_id"])),
                "idempotent": True,
            }
        interrupted: list[dict[str, str]] = [
            {"stage": stage, "job_id": job_id}
            for stage in STAGES
            for job_id, job in state["jobs"][stage].items()
            if job["status"] == "running"
        ]
        event = append_event(
            run_dir,
            state,
            "run_resumed",
            details={"interrupted_jobs": interrupted},
        )
        for item in interrupted:
            job = state["jobs"][item["stage"]][item["job_id"]]
            job["status"] = "interrupted"
            job["error"] = "interrupted during previous process lifetime"
            job["updated_at"] = event["at"]
        if interrupted:
            save_state(run_dir, state, manifest)
        eligible: list[dict[str, Any]] = []
        for stage in STAGES:
            for job_id, job in state["jobs"][stage].items():
                if job_is_retryable(job):
                    eligible.append(
                        {
                            "stage": stage,
                            "job_id": job_id,
                            "status": job["status"],
                            "attempts": job["attempts"],
                            "max_attempts": job["max_attempts"],
                        }
                    )
        exhausted = [
            {
                "stage": stage,
                "job_id": job_id,
                "status": job["status"],
                "attempts": job["attempts"],
                "max_attempts": job["max_attempts"],
                "error": job["error"],
            }
            for stage in STAGES
            for job_id, job in state["jobs"][stage].items()
            if job_is_exhausted(job)
        ]
        return {
            "run_id": state["run_id"],
            "stage": state["stage"],
            "interrupted": interrupted,
            "eligible_jobs": sorted(eligible, key=lambda item: (item["stage"], item["job_id"])),
            "exhausted_jobs": sorted(exhausted, key=lambda item: (item["stage"], item["job_id"])),
            "idempotent": False,
        }


def iter_candidates(
    run_dir: Path,
    manifest: Mapping[str, Any],
    *,
    verify_parents: bool = True,
) -> Iterator[tuple[Path, dict[str, Any]]]:
    root = run_dir / "candidates"
    if not root.exists():
        return
    for path in sorted(root.glob("*/v*.json")):
        _assert_safe_write_path(run_dir, path, "candidate artifact path")
        candidate = validate_candidate(load_json(path), manifest, run_dir, verify_parent=verify_parents)
        expected = (run_dir / candidate_relpath(candidate["candidate_id"], candidate["version"])).resolve()
        if path.resolve() != expected:
            raise InputError(f"candidate stored at noncanonical path: {path.relative_to(run_dir)}")
        yield path, candidate


def normalize_fingerprint(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE).split())


def latest_candidates_for_stage(
    run_dir: Path, manifest: Mapping[str, Any], stage: str
) -> list[tuple[Path, dict[str, Any]]]:
    latest: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path, candidate in iter_candidates(run_dir, manifest):
        if candidate["stage"] != stage:
            continue
        current = latest.get(candidate["candidate_id"])
        if current is None or candidate["version"] > current[1]["version"]:
            latest[candidate["candidate_id"]] = (path, candidate)
    return sorted(latest.values(), key=lambda item: item[1]["candidate_id"])


def candidate_input_hashes(run_dir: Path, manifest: Mapping[str, Any], stage: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for path, _ in latest_candidates_for_stage(run_dir, manifest, stage):
        result[path.relative_to(run_dir).as_posix()] = sha256_file(path)
    return dict(sorted(result.items()))


def build_dedup_report(run_dir: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    rows = latest_candidates_for_stage(run_dir, manifest, "discovery")
    if not rows:
        raise InputError("dedup requires discovery candidate artifacts")
    fingerprint_groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    lexical_rows: list[tuple[dict[str, Any], tuple[str, ...], set[str]]] = []
    ordered_keys = sorted(FINGERPRINT_KEYS)
    for _, candidate in rows:
        reference = {"candidate_id": candidate["candidate_id"], "version": candidate["version"]}
        fingerprint = tuple(normalize_fingerprint(candidate["fingerprint"][key]) for key in ordered_keys)
        fingerprint_groups.setdefault(fingerprint, []).append(reference)
        tokens = set(" ".join(fingerprint).split())
        lexical_rows.append((reference, fingerprint, tokens))
    sorted_groups = sorted(
        (sorted(group, key=lambda item: (item["candidate_id"], item["version"])) for group in fingerprint_groups.values()),
        key=lambda group: (group[0]["candidate_id"], group[0]["version"]),
    )
    unique_refs = [group[0] for group in sorted_groups]
    duplicate_groups = [group for group in sorted_groups if len(group) > 1]
    similarity_threshold = as_decimal(
        manifest["config"]["similarity_flag_threshold"], "config.similarity_flag_threshold"
    )
    similarity_flags: list[dict[str, Any]] = []
    for left_index, (left_ref, left_fingerprint, left_tokens) in enumerate(lexical_rows):
        for right_ref, right_fingerprint, right_tokens in lexical_rows[left_index + 1 :]:
            if left_fingerprint == right_fingerprint:
                continue
            union = left_tokens | right_tokens
            similarity = Decimal(len(left_tokens & right_tokens)) / Decimal(len(union)) if union else Decimal(1)
            if similarity >= similarity_threshold:
                similarity_flags.append(
                    {
                        "left": left_ref,
                        "right": right_ref,
                        "jaccard": decimal_json(similarity, quantum=DERIVED_QUANTUM),
                    }
                )
    candidate_count = len(rows)
    candidates_by_ref = {
        (candidate["candidate_id"], candidate["version"]): candidate
        for _, candidate in rows
    }
    lane_counts = {
        lane: sum(1 for _, candidate in rows if candidate["discovery_lane"] == lane)
        for lane in manifest["config"]["discovery_lanes"]
    }
    unique_lane_counts = {
        lane: sum(
            1
            for ref in unique_refs
            if candidates_by_ref[(ref["candidate_id"], ref["version"])]["discovery_lane"]
            == lane
        )
        for lane in manifest["config"]["discovery_lanes"]
    }
    lane_shortfalls = {
        lane: max(0, manifest["config"]["seeds_per_scout"] - count)
        for lane, count in unique_lane_counts.items()
    }
    unique_count = len(sorted_groups)
    unique_shortfall = max(0, manifest["config"]["unique_min"] - unique_count)
    mechanism_access_count = 0
    mechanism_access_shortfall = 0
    if control_contract_enabled(manifest["config"]):
        mechanism_access_count = sum(
            1
            for reference in unique_refs
            for candidate in [
                candidates_by_ref[
                    (reference["candidate_id"], reference["version"])
                ]
            ]
            if candidate["discovery_lane"] == "mechanism-first"
            and candidate["critical_control_point"]["founder_access_basis"]
            in FOUNDER_ACCESS_RESERVE_BASES
            and candidate["critical_control_point"][
                "confidential_employer_resource_dependency"
            ]
            == "none"
        )
        mechanism_access_shortfall = max(
            0,
            manifest["config"]["mechanism_first_founder_access_reserve"]
            - mechanism_access_count,
        )
    needs_gap = unique_shortfall > 0 or (
        score_bracket_enabled(manifest["config"]) and any(lane_shortfalls.values())
    ) or mechanism_access_shortfall > 0
    gap_slots = 0
    if needs_gap:
        gap_slots = min(
            manifest["config"]["gap_scout_max"],
            max(
                unique_shortfall,
                sum(lane_shortfalls.values()),
                mechanism_access_shortfall,
            ),
        )
    report = {
        "schema_version": manifest["config"]["schema_version"],
        "candidate_artifacts": candidate_input_hashes(run_dir, manifest, "discovery"),
        "candidate_count": candidate_count,
        "lane_counts": lane_counts,
        "unique_lane_counts": unique_lane_counts,
        "lane_shortfalls": lane_shortfalls,
        "unique_candidate_refs": unique_refs,
        "duplicate_groups": duplicate_groups,
        "similarity_flags": similarity_flags,
        "limits": {
            "unique_min": manifest["config"]["unique_min"],
            "similarity_flag_threshold": manifest["config"]["similarity_flag_threshold"],
            "gap_scout_max": manifest["config"]["gap_scout_max"],
            "unique_per_lane_target": manifest["config"]["seeds_per_scout"],
        },
        "needs_gap_scout": needs_gap,
        "gap_scout_slots": gap_slots,
    }
    report["exact_fingerprint_unique_count"] = unique_count
    if control_contract_enabled(manifest["config"]):
        semantic_groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
        for reference in unique_refs:
            candidate = candidates_by_ref[
                (reference["candidate_id"], reference["version"])
            ]
            semantic_groups.setdefault(
                structural_signature_key(candidate), []
            ).append(reference)
        ordered_semantic_groups = sorted(
            (
                sorted(
                    group,
                    key=lambda item: (item["candidate_id"], item["version"]),
                )
                for group in semantic_groups.values()
            ),
            key=lambda group: (group[0]["candidate_id"], group[0]["version"]),
        )
        report["semantic_signature_unique_count"] = len(semantic_groups)
        report["semantic_collision_groups"] = [
            group for group in ordered_semantic_groups if len(group) > 1
        ]
        report["mechanism_first_founder_access_count"] = mechanism_access_count
        report["mechanism_first_founder_access_shortfall"] = (
            mechanism_access_shortfall
        )
        report["limits"]["mechanism_first_founder_access_reserve"] = manifest[
            "config"
        ]["mechanism_first_founder_access_reserve"]
    return report


def _screening_pool_rows(
    run_dir: Path,
    manifest: Mapping[str, Any],
    report: Mapping[str, Any],
) -> list[tuple[Path, dict[str, Any]]]:
    """Return the deterministic lane-balanced pool used by score screening."""
    if not score_bracket_enabled(manifest["config"]):
        raise ConflictError("this run does not use score-bracket screening")
    by_lane: dict[str, list[tuple[Path, dict[str, Any]]]] = {
        lane: [] for lane in manifest["config"]["discovery_lanes"]
    }
    for raw_ref in report.get("unique_candidate_refs", []):
        ref = expect_object(raw_ref, "dedup unique candidate ref")
        candidate_id = expect_nonempty_string(
            ref.get("candidate_id"), "dedup unique candidate ref.candidate_id"
        )
        version = expect_int(
            ref.get("version"), "dedup unique candidate ref.version", minimum=1
        )
        path = run_dir / candidate_relpath(candidate_id, version)
        if not path.is_file():
            raise InputError("dedup unique candidate ref artifact is missing")
        candidate = validate_candidate(load_json(path), manifest, run_dir)
        by_lane[candidate["discovery_lane"]].append((path, candidate))
    lane_target = manifest["config"]["seeds_per_scout"]
    selected: list[tuple[Path, dict[str, Any]]] = []
    for lane in manifest["config"]["discovery_lanes"]:
        rows = sorted(by_lane[lane], key=lambda item: item[1]["candidate_id"])
        if len(rows) < lane_target:
            raise ConflictError(
                f"screening requires {lane_target} unique candidates in lane {lane}"
            )
        selected.extend(rows[:lane_target])
    return selected


def build_screening_batches(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    report_path = run_dir / "dedup" / "report.json"
    if not report_path.is_file():
        raise ConflictError("screening batches require a current dedup report")
    report = expect_object(load_json(report_path), "dedup report")
    if report.get("candidate_artifacts") != candidate_input_hashes(
        run_dir, manifest, "discovery"
    ):
        raise ConflictError("dedup report is stale; rerun dedup")
    rows = _screening_pool_rows(run_dir, manifest, report)
    by_lane = {
        lane: sorted(
            [row for row in rows if row[1]["discovery_lane"] == lane],
            key=lambda item: item[1]["candidate_id"],
        )
        for lane in manifest["config"]["discovery_lanes"]
    }
    batch_size = (
        manifest["config"]["scouts"] * manifest["config"]["seeds_per_scout"]
    ) // manifest["config"]["screening_batches"]
    per_lane = batch_size // len(by_lane)
    batches: list[dict[str, Any]] = []
    for index in range(manifest["config"]["screening_batches"]):
        batch_rows = [
            row
            for lane in manifest["config"]["discovery_lanes"]
            for row in by_lane[lane][index * per_lane : (index + 1) * per_lane]
        ]
        refs = [
            {
                "candidate_id": candidate["candidate_id"],
                "version": candidate["version"],
                "candidate_sha256": sha256_file(path),
            }
            for path, candidate in batch_rows
        ]
        batches.append(
            {
                "batch_id": f"batch-{index + 1:02d}",
                "candidate_refs": sorted(
                    refs, key=lambda item: (item["candidate_id"], item["version"])
                ),
            }
        )
    return {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "dedup_report_sha256": sha256_file(report_path),
        "batches": batches,
    }


def load_screening_batches(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    path = run_dir / "portfolio" / "screening-batches.json"
    if not path.is_file():
        raise InputError("canonical screening batches are missing")
    value = expect_object(
        load_json(path), "screening batches", exact_keys=SCREENING_BATCHES_KEYS
    )
    if value.get("schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError("screening batches schema_version differs from the workflow")
    batches = value.get("batches")
    if not isinstance(batches, list):
        raise InputError("screening batches.batches must be a list")
    for index, raw_batch in enumerate(batches):
        batch = expect_object(
            raw_batch,
            f"screening batches.batches[{index}]",
            exact_keys=SCREENING_BATCH_KEYS,
        )
        expect_nonempty_string(
            batch["batch_id"], f"screening batches.batches[{index}].batch_id"
        )
        if not isinstance(batch["candidate_refs"], list):
            raise InputError(
                f"screening batches.batches[{index}].candidate_refs must be a list"
            )
        for ref_index, ref in enumerate(batch["candidate_refs"]):
            _candidate_reference(
                ref,
                manifest,
                run_dir,
                f"screening batches.batches[{index}].candidate_refs[{ref_index}]",
            )
    expected = build_screening_batches(run_dir, manifest)
    if value != expected or path.read_bytes() != canonical_json_bytes(expected):
        raise InputError("screening batches differ from the deterministic lane-balanced split")
    return expected


def build_secondary_screening_plan(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    if not control_contract_enabled(manifest["config"]):
        raise ConflictError("this run does not use secondary screening")
    batches = load_screening_batches(run_dir, manifest)
    coverage = _require_working_evaluation_coverage(
        run_dir, manifest, "screening"
    )
    records = {record["candidate_id"]: record for record in coverage["records"]}
    planned: list[dict[str, Any]] = []
    advances = (
        manifest["config"]["shortlist_max"]
        // manifest["config"]["screening_batches"]
    )
    window = manifest["config"]["secondary_screening_candidates_per_side"]
    boundary = as_decimal(
        manifest["config"]["secondary_screening_close_margin"],
        "config.secondary_screening_close_margin",
    )
    if manifest["config"]["secondary_screening_enabled"]:
        for batch in batches["batches"]:
            ranked = sorted(
                batch["candidate_refs"],
                key=lambda ref: (
                    -as_decimal(
                        records[ref["candidate_id"]]["final_score"],
                        "primary screening score",
                    ),
                    ref["candidate_id"],
                ),
            )
            if advances >= len(ranked):
                continue
            upper = as_decimal(
                records[ranked[advances - 1]["candidate_id"]]["final_score"],
                "primary screening cutoff score",
            )
            lower = as_decimal(
                records[ranked[advances]["candidate_id"]]["final_score"],
                "primary screening excluded score",
            )
            margin = upper - lower
            if margin > boundary:
                continue
            around = ranked[
                max(0, advances - window) : min(len(ranked), advances + window)
            ]
            sorted_refs = sorted(
                (dict(ref) for ref in around),
                key=lambda ref: (ref["candidate_id"], ref["version"]),
            )
            primary_inputs = []
            for ref in sorted_refs:
                record = records[ref["candidate_id"]]
                primary_inputs.append(
                    {
                        "candidate_ref": ref,
                        "evaluation_path": record["evaluation_path"],
                        "evaluation_sha256": record["evaluation_sha256"],
                        "final_score": record["final_score"],
                    }
                )
            planned.append(
                {
                    "secondary_batch_id": f"secondary-{batch['batch_id']}",
                    "primary_batch_id": batch["batch_id"],
                    "candidate_refs": sorted_refs,
                    "primary_inputs": primary_inputs,
                    "cutoff_margin": decimal_json(
                        margin, quantum=FINAL_QUANTUM
                    ),
                }
            )
    return {
        "schema_version": manifest["config"]["schema_version"],
        "screening_batches_sha256": sha256_file(
            run_dir / "portfolio" / "screening-batches.json"
        ),
        "batches": planned,
    }


def load_secondary_screening_plan(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    path = run_dir / "portfolio" / "secondary-screening.json"
    if not path.is_file():
        raise InputError("canonical secondary-screening plan is missing")
    value = expect_object(
        load_json(path),
        "secondary screening plan",
        exact_keys=SECONDARY_SCREENING_KEYS,
    )
    batches = value["batches"]
    if not isinstance(batches, list):
        raise InputError("secondary screening plan.batches must be a list")
    for index, raw_batch in enumerate(batches):
        batch = expect_object(
            raw_batch,
            f"secondary screening plan.batches[{index}]",
            exact_keys=SECONDARY_SCREENING_BATCH_KEYS,
        )
        if not isinstance(batch["candidate_refs"], list) or not isinstance(
            batch["primary_inputs"], list
        ):
            raise InputError(
                "secondary screening candidate_refs and primary_inputs must be lists"
            )
        for input_index, item in enumerate(batch["primary_inputs"]):
            expect_object(
                item,
                f"secondary screening primary_inputs[{input_index}]",
                exact_keys=SECONDARY_SCREENING_INPUT_KEYS,
            )
    expected = build_secondary_screening_plan(run_dir, manifest)
    if value != expected or path.read_bytes() != canonical_json_bytes(expected):
        raise InputError(
            "secondary screening plan differs from the deterministic close-cutoff set"
        )
    return expected


def build_screening_aggregation(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    plan = load_secondary_screening_plan(run_dir, manifest)
    primary = _require_working_evaluation_coverage(
        run_dir, manifest, "screening"
    )
    secondary = _require_working_evaluation_coverage(
        run_dir, manifest, "screening_secondary"
    )
    primary_by_id = {record["candidate_id"]: record for record in primary["records"]}
    secondary_by_id = {
        record["candidate_id"]: record for record in secondary["records"]
    }
    rows: list[dict[str, Any]] = []
    for candidate_id, primary_record in sorted(primary_by_id.items()):
        candidate_path = run_dir / candidate_relpath(
            candidate_id, primary_record["candidate_version"]
        )
        ref = {
            "candidate_id": candidate_id,
            "version": primary_record["candidate_version"],
            "candidate_sha256": sha256_file(candidate_path),
        }
        secondary_record = secondary_by_id.get(candidate_id)
        primary_score = as_decimal(
            primary_record["final_score"], "primary screening score"
        )
        if secondary_record is None:
            canonical_score = primary_score
        else:
            secondary_score = as_decimal(
                secondary_record["final_score"], "secondary screening score"
            )
            canonical_score = (primary_score + secondary_score) / Decimal(2)
        rows.append(
            {
                "candidate_ref": ref,
                "primary_evaluation_path": primary_record["evaluation_path"],
                "primary_evaluation_sha256": primary_record["evaluation_sha256"],
                "primary_score": primary_record["final_score"],
                "secondary_evaluation_path": (
                    None
                    if secondary_record is None
                    else secondary_record["evaluation_path"]
                ),
                "secondary_evaluation_sha256": (
                    None
                    if secondary_record is None
                    else secondary_record["evaluation_sha256"]
                ),
                "secondary_score": (
                    None
                    if secondary_record is None
                    else secondary_record["final_score"]
                ),
                "canonical_score": decimal_json(
                    canonical_score, quantum=FINAL_QUANTUM
                ),
            }
        )
    return {
        "schema_version": manifest["config"]["schema_version"],
        "secondary_screening_sha256": sha256_file(
            run_dir / "portfolio" / "secondary-screening.json"
        ),
        "rule": manifest["config"]["secondary_screening_aggregation"],
        "candidates": rows,
    }


def load_screening_aggregation(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    path = run_dir / "portfolio" / "screening-aggregation.json"
    if not path.is_file():
        raise InputError("canonical screening aggregation is missing")
    value = expect_object(
        load_json(path),
        "screening aggregation",
        exact_keys=SCREENING_AGGREGATION_KEYS,
    )
    candidates = value["candidates"]
    if not isinstance(candidates, list):
        raise InputError("screening aggregation.candidates must be a list")
    for index, row in enumerate(candidates):
        expect_object(
            row,
            f"screening aggregation.candidates[{index}]",
            exact_keys=SCREENING_AGGREGATION_ROW_KEYS,
        )
    expected = build_screening_aggregation(run_dir, manifest)
    if value != expected or path.read_bytes() != canonical_json_bytes(expected):
        raise InputError(
            "screening aggregation differs from deterministic evaluation inputs"
        )
    return expected


def dedup_run(run_dir: Path) -> dict[str, Any]:
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        if state["stage"] not in {"discovery", "calibration"}:
            raise ConflictError("dedup is available only during discovery or calibration")
        report = build_dedup_report(run_dir, manifest)
        discovery_jobs = state["jobs"]["discovery"]
        gap_job = discovery_jobs.get("gap-scout")
        state_changed = False
        if report["needs_gap_scout"] and gap_job is None:
            gap_job = {
                "status": "pending",
                "attempts": 0,
                "max_attempts": manifest["config"]["mechanical_attempts"],
                "artifact": None,
                "artifact_sha256": None,
                "error": None,
                "updated_at": utc_now(),
            }
            discovery_jobs["gap-scout"] = gap_job
            state_changed = True
        elif not report["needs_gap_scout"] and gap_job is not None and gap_job["status"] in RETRYABLE_JOB_STATUSES:
            gap_job.update({"status": "skipped", "error": None, "updated_at": utc_now()})
            state_changed = True
        if gap_job is not None:
            report["gap_scout_job"] = {
                "job_id": "gap-scout",
                "status": gap_job["status"],
                "attempts": gap_job["attempts"],
                "max_attempts": gap_job["max_attempts"],
                "seed_budget": manifest["config"]["gap_scout_max"],
                "lane_shortfalls": report["lane_shortfalls"],
                **(
                    {
                        "mechanism_first_founder_access_shortfall": report[
                            "mechanism_first_founder_access_shortfall"
                        ]
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
            report["gap_scout_budget_exhausted"] = (
                gap_job["status"] in TERMINAL_JOB_STATUSES
                or (gap_job["status"] in {"failed", "interrupted"} and not job_is_retryable(gap_job))
            )
        else:
            report["gap_scout_job"] = None
            report["gap_scout_budget_exhausted"] = False
        if state_changed:
            save_state(run_dir, state, manifest)
        atomic_write(run_dir / "dedup" / "report.json", canonical_json_bytes(report), root=run_dir)
        append_event(
            run_dir,
            state,
            "dedup_completed",
            details={
                "exact_fingerprint_unique_count": report["exact_fingerprint_unique_count"],
                **(
                    {
                        "semantic_signature_unique_count": report[
                            "semantic_signature_unique_count"
                        ],
                        "mechanism_first_founder_access_count": report[
                            "mechanism_first_founder_access_count"
                        ],
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
                "lane_counts": report["lane_counts"],
                "unique_lane_counts": report["unique_lane_counts"],
                "needs_gap_scout": report["needs_gap_scout"],
                "gap_scout_job": report["gap_scout_job"],
            },
        )
        return {"run_id": state["run_id"], "artifact": "dedup/report.json", **report}


def _validate_stage_gate(run_dir: Path, manifest: Mapping[str, Any], state: Mapping[str, Any]) -> None:
    stage = state["stage"]
    if stage == "discovery":
        report_path = run_dir / "dedup" / "report.json"
        if not report_path.is_file():
            raise ConflictError("run dedup before leaving discovery")
        report = expect_object(load_json(report_path), "dedup report")
        if report.get("candidate_artifacts") != candidate_input_hashes(run_dir, manifest, "discovery"):
            raise ConflictError("dedup report is stale; rerun dedup")
        lane_counts = report.get("lane_counts")
        expected_lanes = manifest["config"]["discovery_lanes"]
        if not isinstance(lane_counts, dict) or set(lane_counts) != set(expected_lanes):
            raise ConflictError("dedup report does not cover every configured discovery lane")
        incomplete_lanes = [
            lane
            for lane in expected_lanes
            if lane_counts[lane] < manifest["config"]["seeds_per_scout"]
        ]
        if incomplete_lanes:
            raise ConflictError(
                "discovery must complete the configured seed budget for every lane: "
                + ", ".join(incomplete_lanes)
            )
        unique_metric = report.get("exact_fingerprint_unique_count", 0)
        below_minimum = unique_metric < manifest["config"]["unique_min"]
        if score_bracket_enabled(manifest["config"]):
            unique_lane_counts = report.get("unique_lane_counts")
            if not isinstance(unique_lane_counts, dict):
                raise ConflictError("dedup report is missing unique lane counts")
            short_lanes = [
                lane
                for lane in expected_lanes
                if unique_lane_counts.get(lane, 0)
                < manifest["config"]["seeds_per_scout"]
            ]
            if below_minimum or short_lanes:
                details = (
                    f"; lane shortfalls: {', '.join(short_lanes)}" if short_lanes else ""
                )
                raise ConflictError(
                    "score screening requires the full unique lane-balanced pool"
                    + details
                )
        if below_minimum:
            gap_job = state["jobs"]["discovery"].get("gap-scout")
            gap_exhausted = gap_job is not None and (
                gap_job["status"] in TERMINAL_JOB_STATUSES
                or (gap_job["status"] in {"failed", "interrupted"} and not job_is_retryable(gap_job))
            )
            if not gap_exhausted:
                raise ConflictError("discovery diversity target requires the one bounded gap-scout job")
        if control_contract_enabled(manifest["config"]):
            reserve = manifest["config"]["mechanism_first_founder_access_reserve"]
            observed = expect_int(
                report.get("mechanism_first_founder_access_count"),
                "dedup mechanism_first_founder_access_count",
                minimum=0,
            )
            if observed < reserve:
                raise ConflictError(
                    "mechanism-first discovery does not satisfy the configured legally usable founder-access reserve"
                )
    if stage == "calibration":
        if score_bracket_enabled(manifest["config"]):
            load_screening_batches(run_dir, manifest)
            _require_working_evaluation_coverage(run_dir, manifest, "screening")
            if control_contract_enabled(manifest["config"]):
                load_secondary_screening_plan(run_dir, manifest)
                _require_working_evaluation_coverage(
                    run_dir, manifest, "screening_secondary"
                )
        else:
            effective_portfolio_selection(run_dir, manifest)
    if stage == "research":
        portfolio = effective_portfolio_selection(run_dir, manifest)
        expected = {
            (item["candidate_id"], item["version"], item["candidate_sha256"])
            for item in portfolio["candidate_refs"]
        }
        actual = {
            (record["candidate_id"], record["candidate_version"], record["candidate_sha256"])
            for _, record in iter_research(run_dir, manifest)
        }
        if actual != expected:
            raise ConflictError(
                "research must exactly cover the immutable effective shortlist; substitutions require a versioned amendment"
            )
        research_coverage = _require_working_evaluation_coverage(
            run_dir, manifest, "research"
        )
        if score_bracket_enabled(manifest["config"]):
            screening_coverage = _require_working_evaluation_coverage(
                run_dir, manifest, "screening"
            )
            reused = sorted(
                {row["judge_id"] for row in research_coverage["records"]}
                & (
                    {row["judge_id"] for row in screening_coverage["records"]}
                    | (
                        {
                            row["judge_id"]
                            for row in _require_working_evaluation_coverage(
                                run_dir, manifest, "screening_secondary"
                            )["records"]
                        }
                        if control_contract_enabled(manifest["config"])
                        else set()
                    )
                )
            )
            if reused:
                raise ConflictError(
                    "research evaluators must be fresh from screening roles: "
                    + ", ".join(reused)
                )
        _load_portfolio_decision(run_dir, manifest)
    if stage == "development":
        decision = _load_portfolio_decision(run_dir, manifest)
        expected_ids = {
            item["candidate_id"]
            for item in decision["candidate_decisions"]
            if item["disposition"] == "develop"
        }
        result_paths = sorted((run_dir / "development").glob("*/constructor-result.json"))
        actual_ids = {path.parent.name for path in result_paths}
        if actual_ids != expected_ids:
            raise ConflictError("constructor results must exactly match the canonical portfolio decision")
        coverage = _require_working_evaluation_coverage(run_dir, manifest, "development")
        working_judges = {item["judge_id"] for item in coverage["records"]}
        all_working_evaluations = [
            evaluation
            for _, evaluation in iter_evaluations(run_dir, manifest)
            if evaluation["evaluation_type"].startswith("working_")
        ]
        all_working_judges = {
            evaluation["judge_id"] for evaluation in all_working_evaluations
        }
        constructor_ids: set[str] = set()
        redesigned_ids: set[str] = set()
        for candidate_id in sorted(actual_ids):
            _, result = _development_result_for_candidate(run_dir, manifest, candidate_id)
            constructor_ids.add(result["constructor_id"])
            if result["outcome"] == "redesigned":
                redesigned_ids.add(candidate_id)
        stored_redesign_ids = {
            candidate["candidate_id"]
            for _, candidate in iter_candidates(run_dir, manifest)
            if candidate["stage"] == "development"
        }
        if stored_redesign_ids != redesigned_ids:
            raise ConflictError(
                "development redesign artifacts must exactly match authorized redesigned outcomes"
            )
        reused = sorted(all_working_judges & constructor_ids)
        if reused:
            raise ConflictError(
                f"development constructor and working evaluator roles must be independent: {', '.join(reused)}"
            )
        if score_bracket_enabled(manifest["config"]):
            earlier_judges = {
                evaluation["judge_id"]
                for evaluation in all_working_evaluations
                if evaluation["evaluation_type"]
                in {
                    "working_screening",
                    "working_screening_secondary",
                    "working_research",
                }
            }
            reused = sorted(working_judges & earlier_judges)
            if reused:
                raise ConflictError(
                    "development evaluators must be fresh from earlier working roles: "
                    + ", ".join(reused)
                )
    if stage == "frozen":
        selection = load_finalist_selection(run_dir, manifest)
        expected = build_finalist_selection(run_dir, manifest)
        if selection != expected:
            raise ConflictError("finalists must be the deterministic top-ranked development prefix")
        for _, candidate in finalist_candidates(run_dir, manifest):
            validate_finalist_lineage(run_dir, manifest, candidate)
            try:
                _external_identity(run_dir, manifest, candidate["candidate_id"])
            except WorkflowError as exc:
                raise ConflictError(
                    f"canonical holdout packet is required for {candidate['candidate_id']}: {exc}"
                ) from exc


def advance_run(run_dir: Path) -> dict[str, Any]:
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, finalized = project_transition_state(events)
        require_job_event_state_match(events, state, manifest)
        if finalized is not None or projected_status != "active":
            raise ConflictError("use finalize to reconcile or inspect a terminal transition")
        if projected_stage != state["stage"]:
            projected_index = STAGES.index(projected_stage)
            state_index = STAGES.index(state["stage"])
            if projected_index == state_index + 1:
                previous = state["stage"]
                state["stage"] = projected_stage
                save_state(run_dir, state, manifest)
                return {
                    "run_id": state["run_id"],
                    "previous_stage": previous,
                    "stage": projected_stage,
                    "run_status": "active",
                    "idempotent": True,
                }
            if state_index == projected_index + 1:
                append_event(
                    run_dir,
                    state,
                    "stage_advanced",
                    stage=state["stage"],
                    details={"previous_stage": projected_stage, "stage": state["stage"]},
                )
                return {
                    "run_id": state["run_id"],
                    "previous_stage": projected_stage,
                    "stage": state["stage"],
                    "run_status": "active",
                    "idempotent": True,
                }
            raise InputError("state stage and event history differ by more than one transition")
        assert_active(state)
        if state["stage"] == "holdout":
            raise ConflictError("use finalize to leave holdout")
        blockers = current_stage_blockers(state)
        if blockers:
            raise ConflictError(f"current stage has running or retryable jobs: {', '.join(blockers)}")
        if state["stage"] == "calibration" and control_contract_enabled(
            manifest["config"]
        ):
            _require_working_evaluation_coverage(run_dir, manifest, "screening")
            secondary_path = run_dir / "portfolio" / "secondary-screening.json"
            expected_plan = build_secondary_screening_plan(run_dir, manifest)
            existed = secondary_path.is_file()
            write_immutable(
                secondary_path,
                canonical_json_bytes(expected_plan),
                root=run_dir,
            )
            plan_digest = sha256_file(secondary_path)
            plan_events = [
                event
                for event in load_events(
                    run_dir / "events.jsonl", state["run_id"]
                )
                if event["event"] == "secondary_screening_planned"
            ]
            if len(plan_events) > 1:
                raise InputError(
                    "event log contains duplicate secondary_screening_planned records"
                )
            expected_details = {
                "artifact": "portfolio/secondary-screening.json",
                "artifact_sha256": plan_digest,
                "secondary_batch_count": len(expected_plan["batches"]),
            }
            if plan_events and plan_events[0]["details"] != expected_details:
                raise InputError(
                    "secondary screening event differs from the deterministic plan"
                )
            if not plan_events:
                append_event(
                    run_dir,
                    state,
                    "secondary_screening_planned",
                    details=expected_details,
                )
            secondary_coverage = working_evaluation_coverage(
                run_dir, manifest, "screening_secondary"
            )
            if expected_plan["batches"] and not secondary_coverage["complete"]:
                return {
                    "run_id": state["run_id"],
                    "stage": state["stage"],
                    "run_status": state["run_status"],
                    "secondary_screening_required": True,
                    "secondary_screening_artifact": "portfolio/secondary-screening.json",
                    "secondary_batch_ids": [
                        batch["secondary_batch_id"]
                        for batch in expected_plan["batches"]
                    ],
                    "coverage": secondary_coverage,
                    "idempotent": existed,
                }
        _validate_stage_gate(run_dir, manifest, state)
        current = state["stage"]
        next_stage = STAGES[STAGES.index(current) + 1]
        if current == "discovery" and score_bracket_enabled(manifest["config"]):
            batches = build_screening_batches(run_dir, manifest)
            write_immutable(
                run_dir / "portfolio" / "screening-batches.json",
                canonical_json_bytes(batches),
                root=run_dir,
            )
        if current == "calibration" and score_bracket_enabled(manifest["config"]):
            if control_contract_enabled(manifest["config"]):
                aggregation = build_screening_aggregation(run_dir, manifest)
                aggregation_path = (
                    run_dir / "portfolio" / "screening-aggregation.json"
                )
                write_immutable(
                    aggregation_path,
                    canonical_json_bytes(aggregation),
                    root=run_dir,
                )
                aggregation_details = {
                    "artifact": "portfolio/screening-aggregation.json",
                    "artifact_sha256": sha256_file(aggregation_path),
                    "rule": aggregation["rule"],
                    "candidate_count": len(aggregation["candidates"]),
                }
                aggregation_events = [
                    event
                    for event in load_events(
                        run_dir / "events.jsonl", state["run_id"]
                    )
                    if event["event"] == "screening_aggregation_completed"
                ]
                if len(aggregation_events) > 1:
                    raise InputError(
                        "event log contains duplicate screening_aggregation_completed records"
                    )
                if aggregation_events:
                    if aggregation_events[0]["details"] != aggregation_details:
                        raise InputError(
                            "screening aggregation event differs from its deterministic artifact"
                        )
                else:
                    append_event(
                        run_dir,
                        state,
                        "screening_aggregation_completed",
                        details=aggregation_details,
                    )
            selection = build_score_portfolio_selection(run_dir, manifest)
            write_immutable(
                run_dir / "portfolio" / "selection.json",
                canonical_json_bytes(selection),
                root=run_dir,
            )
        if current == "development":
            if score_bracket_enabled(manifest["config"]):
                version_selection = build_version_selection(run_dir, manifest)
                write_immutable(
                    run_dir / "portfolio" / "version-selection.json",
                    canonical_json_bytes(version_selection),
                    root=run_dir,
                )
            finalists = build_finalist_selection(run_dir, manifest)
            write_immutable(
                run_dir / "portfolio" / "finalists.json",
                canonical_json_bytes(finalists),
                root=run_dir,
            )
        append_event(
            run_dir,
            state,
            "stage_advanced",
            stage=next_stage,
            details={"previous_stage": current, "stage": next_stage},
        )
        state["stage"] = next_stage
        save_state(run_dir, state, manifest)
        return {
            "run_id": state["run_id"],
            "previous_stage": current,
            "stage": next_stage,
            "run_status": "active",
            "idempotent": False,
        }


def external_response_schema(
    manifest: Mapping[str, Any], candidate: Mapping[str, Any]
) -> dict[str, Any]:
    factor_names = [name for name, _ in rubric_from_manifest(manifest)]
    diagnostics = sorted(
        EVALUATOR_RESPONSE_KEYS
        - {
            "candidate_id",
            "candidate_version",
            "judge_id",
            "factors",
            "interaction_adjustment",
            "assumptions",
        }
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "External opportunity holdout response",
        "type": "object",
        "additionalProperties": False,
        "required": sorted(EVALUATOR_RESPONSE_KEYS),
        "properties": {
            "candidate_id": {"const": candidate["candidate_id"]},
            "candidate_version": {"const": candidate["version"]},
            "judge_id": {"type": "string", "minLength": 1},
            "factors": {
                "type": "array",
                "minItems": len(factor_names),
                "maxItems": len(factor_names),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": sorted(FACTOR_BASE_KEYS),
                    "properties": {
                        "name": {"enum": factor_names},
                        "status": {"enum": ["scored", "excluded"]},
                        "score": {"type": ["number", "null"], "minimum": 1, "maximum": 10},
                        "rationale": {"type": "string", "minLength": 1},
                    },
                },
            },
            "interaction_adjustment": {"type": "number", "minimum": -0.5, "maximum": 0.5},
            "assumptions": {"type": "array", "items": {"type": "string", "minLength": 1}},
            **{key: {"type": "string", "minLength": 1} for key in diagnostics},
        },
    }


def candidate_lineage(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Return one fully validated, consecutive candidate lineage oldest first."""
    current = validate_candidate(candidate, manifest, run_dir)
    lineage: list[dict[str, Any]] = []
    visited: set[tuple[str, int]] = set()
    while True:
        reference = (current["candidate_id"], current["version"])
        if reference in visited:
            raise InputError("candidate lineage contains a cycle")
        visited.add(reference)
        lineage.append(current)
        parent = current["parent"]
        if parent is None:
            break
        parent_path = run_dir / candidate_relpath(parent["candidate_id"], parent["version"])
        _assert_safe_write_path(run_dir, parent_path, "candidate lineage artifact path")
        if not parent_path.is_file():
            raise InputError("candidate lineage parent artifact does not exist")
        current = validate_candidate(load_json(parent_path), manifest, run_dir)
    lineage.reverse()
    expected_versions = list(range(1, candidate["version"] + 1))
    if [item["version"] for item in lineage] != expected_versions:
        raise InputError("candidate lineage versions are not consecutive from v1")
    if any(item["candidate_id"] != candidate["candidate_id"] for item in lineage):
        raise InputError("candidate lineage crosses candidate identities")
    return lineage


def validate_finalist_selection(
    value: Any, manifest: Mapping[str, Any], run_dir: Path
) -> dict[str, Any]:
    selection = expect_object(
        value, "finalist selection", exact_keys=FINALIST_SELECTION_KEYS
    )
    if expect_int(
        selection["schema_version"], "finalist selection.schema_version"
    ) != ACTIVE_SCHEMA_VERSION:
        raise InputError(
            f"finalist selection.schema_version must be {ACTIVE_SCHEMA_VERSION}"
        )
    values = selection["candidate_refs"]
    if not isinstance(values, list) or not 1 <= len(values) <= manifest["config"]["finalists_max"]:
        raise InputError("finalist selection candidate_refs count is outside finalist limits")
    references: list[dict[str, Any]] = []
    identities: set[tuple[str, int]] = set()
    for index, raw in enumerate(values):
        reference, _, _ = _candidate_reference(
            raw,
            manifest,
            run_dir,
            f"finalist selection.candidate_refs[{index}]",
            required_stage={"discovery", "development"},
        )
        identity = (reference["candidate_id"], reference["version"])
        if identity in identities:
            raise InputError("finalist selection contains a duplicate candidate")
        identities.add(identity)
        references.append(reference)
    canonical = dict(selection)
    canonical["candidate_refs"] = sorted(
        references, key=lambda item: (item["candidate_id"], item["version"])
    )
    return canonical


def load_finalist_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    path = run_dir / "portfolio" / "finalists.json"
    if not path.is_file():
        raise InputError("canonical finalist selection is missing")
    selection = validate_finalist_selection(load_json(path), manifest, run_dir)
    if path.read_bytes() != canonical_json_bytes(selection):
        raise InputError("finalist selection is not canonical")
    return selection


def finalist_candidates(
    run_dir: Path, manifest: Mapping[str, Any]
) -> list[tuple[Path, dict[str, Any]]]:
    result: list[tuple[Path, dict[str, Any]]] = []
    for reference in load_finalist_selection(run_dir, manifest)["candidate_refs"]:
        _, path, candidate = _candidate_reference(
            reference,
            manifest,
            run_dir,
            "finalist selection candidate_ref",
            required_stage={"discovery", "development"},
        )
        result.append((path, candidate))
    return result


def finalist_candidate(
    run_dir: Path, manifest: Mapping[str, Any], candidate_id: str
) -> tuple[Path, dict[str, Any]]:
    matches = [
        item
        for item in finalist_candidates(run_dir, manifest)
        if item[1]["candidate_id"] == candidate_id
    ]
    if len(matches) != 1:
        raise InputError(f"no exact finalist reference found for {candidate_id}")
    return matches[0]


def build_finalist_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    ranked = _ranked_stage_candidates(run_dir, manifest, "development")
    if not ranked:
        raise ConflictError("development produced no evaluated constructor result")
    references = [
        {
            "candidate_id": candidate["candidate_id"],
            "version": candidate["version"],
            "candidate_sha256": sha256_file(path),
        }
        for path, candidate, _ in ranked[: manifest["config"]["finalists_max"]]
    ]
    return validate_finalist_selection(
        {"schema_version": ACTIVE_SCHEMA_VERSION, "candidate_refs": references},
        manifest,
        run_dir,
    )


def validate_finalist_lineage(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Require research, construction, and fresh evaluation of this exact finalist."""
    lineage = candidate_lineage(run_dir, manifest, candidate)
    base = lineage[0]
    base_path = run_dir / candidate_relpath(base["candidate_id"], base["version"])
    research_path = run_dir / research_relpath(base["candidate_id"], base["version"])
    if not research_path.is_file():
        raise InputError("finalist lineage is missing research for the immutable discovery candidate")
    validate_research(load_json(research_path), manifest, run_dir)
    research_evaluations = _working_evaluations_for_candidate(
        run_dir, manifest, base_path, base, "working_research"
    )
    candidate_path = run_dir / candidate_relpath(
        candidate["candidate_id"], candidate["version"]
    )
    _, result = _development_result_for_candidate(
        run_dir, manifest, candidate["candidate_id"]
    )
    if score_bracket_enabled(manifest["config"]):
        selection = load_version_selection(run_dir, manifest)
        rows = [
            row
            for row in selection["lineages"]
            if row["candidate_id"] == candidate["candidate_id"]
        ]
        if len(rows) != 1 or rows[0]["selected_candidate_ref"] != {
            "candidate_id": candidate["candidate_id"],
            "version": candidate["version"],
            "candidate_sha256": sha256_file(candidate_path),
        }:
            raise InputError(
                "finalist must reference the deterministic winning version in its lineage"
            )
        development_evaluations: list[tuple[Path, dict[str, Any]]] = []
        refs = [rows[0]["base_candidate_ref"]]
        if rows[0]["redesign_candidate_ref"] is not None:
            refs.append(rows[0]["redesign_candidate_ref"])
        for ref in refs:
            path = run_dir / candidate_relpath(ref["candidate_id"], ref["version"])
            version_candidate = validate_candidate(load_json(path), manifest, run_dir)
            development_evaluations.extend(
                _working_evaluations_for_candidate(
                    run_dir,
                    manifest,
                    path,
                    version_candidate,
                    "working_development",
                )
            )
        expected_development = len(refs) * (
            manifest["config"]["development_evaluators_per_lineage"]
            if control_contract_enabled(manifest["config"])
            else 1
        )
        if (
            len(research_evaluations) != 1
            or len(development_evaluations) != expected_development
        ):
            raise InputError(
                "finalist requires research plus complete paired development evaluation"
            )
    else:
        development_evaluations = _working_evaluations_for_candidate(
            run_dir, manifest, candidate_path, candidate, "working_development"
        )
        if (
            result["final_candidate_version"] != candidate["version"]
            or result["final_candidate_sha256"] != sha256_file(candidate_path)
        ):
            raise InputError("finalist must reference the exact constructor final candidate")
        if len(research_evaluations) != 1 or len(development_evaluations) != 1:
            raise InputError("finalist requires exactly one research and one development evaluation")
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_version": candidate["version"],
        "lineage_versions": [item["version"] for item in lineage],
        "working_evaluations": [
            research_evaluations[0][0].relative_to(run_dir).as_posix(),
            *[
                path.relative_to(run_dir).as_posix()
                for path, _ in development_evaluations
            ],
        ],
    }


def lineage_research_records(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate: Mapping[str, Any],
    *,
    required: bool = True,
) -> list[tuple[Path, dict[str, Any]]]:
    evidence: list[tuple[Path, dict[str, Any]]] = []
    current = dict(candidate)
    visited: set[tuple[str, int]] = set()
    while True:
        reference = (current["candidate_id"], current["version"])
        if reference in visited:
            raise InputError("candidate lineage contains a cycle")
        visited.add(reference)
        research_path = run_dir / research_relpath(*reference)
        if research_path.is_file():
            record = validate_research(load_json(research_path), manifest, run_dir)
            evidence.append((research_path, record))
        parent = current["parent"]
        if parent is None:
            break
        parent_path = run_dir / candidate_relpath(parent["candidate_id"], parent["version"])
        current = validate_candidate(load_json(parent_path), manifest, run_dir)
    if not evidence and required:
        raise InputError("external holdout requires a candidate-bound research artifact in the frozen lineage")
    return sorted(evidence, key=lambda item: item[0].as_posix())


def external_packet(
    run_dir: Path,
    candidate: Mapping[str, Any],
    candidate_digest: str,
    manifest: Mapping[str, Any],
) -> str:
    factor_names = [name for name, _ in rubric_from_manifest(manifest)]
    candidate_text = canonical_json_bytes(candidate).decode("utf-8").rstrip()
    factor_text = "\n".join(f"- {name}" for name in factor_names)
    founder_text = (run_dir / "inputs" / "founder.md").read_text(encoding="utf-8").rstrip()
    evaluator_text = (run_dir / "inputs" / "evaluator.txt").read_text(encoding="utf-8").rstrip()
    evidence = lineage_research_records(run_dir, manifest, candidate)
    evidence_text = "\n\n".join(
        f"### `{path.relative_to(run_dir).as_posix()}` (SHA-256 `{sha256_file(path)}`)\n\n"
        f"```json\n{canonical_json_bytes(record).decode('utf-8').rstrip()}\n```"
        for path, record in evidence
    )
    return f"""# Fresh external holdout

Evaluate only the exact frozen opportunity below. Be skeptical and independent. Do not infer traction or evidence that is not present. Missing validation is uncertainty; contradictory evidence is negative evidence.

Score every applicable factor from 1 to 10. A factor may be excluded only when it is structurally irrelevant, with a specific rationale and a null score. Use an interaction adjustment only for a material cross-factor effect not already counted, within -0.5 to +0.5.

Factors:
{factor_text}

Return exactly one JSON object matching `response_schema.json`. Do not wrap it in prose. Do not calculate weights, a total, a pass/fail result, or speculate about a target score.

## Immutable founder snapshot

The following is the run's exact founder input. Do not substitute or compress it.

<founder_snapshot sha256="{manifest['source_hashes']['PERSONALITY_SITUATION.md']}">
{founder_text}
</founder_snapshot>

## Immutable evaluator snapshot

Apply this exact evaluator. Its scoring weights are computed by the importing utility; return factor scores and the requested diagnostics only.

<evaluator_snapshot sha256="{manifest['rubric']['sha256']}">
{evaluator_text}
</evaluator_snapshot>

## Candidate-bound evidence

These canonical research records are bound by candidate identity and hash.

{evidence_text}

## Frozen candidate

Candidate SHA-256: `{candidate_digest}`

```json
{candidate_text}
```
"""


def export_external(run_dir: Path, candidate_id: str) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("CANDIDATE_ID must be a lowercase slug")
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        if state["stage"] not in {"frozen", "holdout"}:
            raise ConflictError("external export requires frozen or holdout stage")
        path, candidate = finalist_candidate(run_dir, manifest, candidate_id)
        validate_finalist_lineage(run_dir, manifest, candidate)
        digest = sha256_file(path)
        root = run_dir / "exports" / candidate_id
        packet_path = root / "holdout_packet.md"
        schema_path = root / "response_schema.json"
        existed = packet_path.exists() and schema_path.exists()
        packet_bytes = external_packet(run_dir, candidate, digest, manifest).encode("utf-8")
        schema_bytes = canonical_json_bytes(external_response_schema(manifest, candidate))
        write_immutable(packet_path, packet_bytes, root=run_dir)
        write_immutable(schema_path, schema_bytes, root=run_dir)
        export_events = [
            event
            for event in load_events(run_dir / "events.jsonl", state["run_id"])
            if event["event"] == "external_exported"
            and event["details"].get("candidate_id") == candidate_id
            and event["details"].get("candidate_version") == candidate["version"]
        ]
        if len(export_events) > 1:
            raise InputError("event log contains duplicate external_exported records")
        if not export_events:
            append_event(
                run_dir,
                state,
                "external_exported",
                details={"candidate_id": candidate_id, "candidate_version": candidate["version"]},
            )
        return {
            "run_id": state["run_id"],
            "candidate_id": candidate_id,
            "candidate_version": candidate["version"],
            "packet": f"exports/{candidate_id}/holdout_packet.md",
            "response_schema": f"exports/{candidate_id}/response_schema.json",
            "idempotent": existed,
        }


def native_holdout_assignment(
    run_dir: Path, candidate_id: str, response_destination: Path
) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("CANDIDATE_ID must be a lowercase slug")
    destination = Path(os.path.abspath(response_destination))
    # Resolve symlinks, then also compare directory identities: on a
    # case-insensitive filesystem realpath can preserve an alternate spelling.
    resolved_destination = destination.resolve()
    run_root = run_dir.resolve()
    if resolved_destination.is_relative_to(run_root) or any(
        parent.exists() and parent.samefile(run_root)
        for parent in resolved_destination.parents
    ):
        raise InputError(
            "native holdout response destination must be outside CLI-managed run state"
        )
    if destination.suffix.lower() != ".json":
        raise InputError("native holdout response destination must end in .json")
    if not destination.parent.is_dir():
        raise InputError("native holdout response destination parent does not exist")
    if destination.exists() or destination.is_symlink():
        raise ConflictError(
            "native holdout response destination already exists; use a fresh temporary path"
        )
    manifest, state = load_run(run_dir)
    if state["stage"] not in {"frozen", "holdout"}:
        raise ConflictError(
            "native holdout assignment requires frozen or holdout stage"
        )
    _, candidate, _ = _external_identity(
        run_dir, manifest, candidate_id
    )
    packet_path = run_dir / "exports" / candidate_id / "holdout_packet.md"
    schema_path = run_dir / "exports" / candidate_id / "response_schema.json"
    response_schema = load_json(schema_path)
    # Structured-output transports require explicit types even where const/enum
    # already imply them. Keep immutable exported schemas byte-stable.
    response_schema["properties"]["candidate_id"]["type"] = "string"
    response_schema["properties"]["candidate_version"]["type"] = "integer"
    response_schema["description"] = (
        "Write the complete response JSON yourself to temporary_response_destination "
        "from this assignment, then return that same JSON. A final chat response alone "
        "does not satisfy this contract. Use only the supplied immutable finalist packet; "
        "do not load repository instructions, workflow skills, history, other candidates, "
        "prior evaluations, or another judge's response."
    )
    response_schema["properties"]["judge_id"]["const"] = "native-" + sha256_bytes(
        canonical_json_bytes({
            "run_id": manifest["run_id"],
            "candidate_id": candidate_id,
            "destination": str(resolved_destination),
        })
    )[:24]
    factor_properties = response_schema["properties"]["factors"]["items"]["properties"]
    factor_properties["name"]["type"] = "string"
    factor_properties["status"]["type"] = "string"
    return {
        "immutable_finalist_packet": {
            "sha256": sha256_file(packet_path),
            "content": packet_path.read_text(encoding="utf-8"),
        },
        "strict_response_contract": response_schema,
        "temporary_response_destination": str(destination),
    }


def parse_external_object(raw: bytes, source: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8").strip()
    except UnicodeError as exc:
        raise InputError("external response must be UTF-8") from exc
    if not text:
        raise InputError("external response is empty")
    if text.startswith("```"):
        raise InputError("external response must be one plain JSON object")
    value = parse_json(text, source=source)
    return parse_evaluator_response(value, "external response")


def _external_identity(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate_id: str,
) -> tuple[Path, dict[str, Any], str]:
    candidate_path, candidate = finalist_candidate(run_dir, manifest, candidate_id)
    validate_finalist_lineage(run_dir, manifest, candidate)
    candidate_digest = sha256_file(candidate_path)
    export_root = run_dir / "exports" / candidate_id
    packet_path = export_root / "holdout_packet.md"
    schema_path = export_root / "response_schema.json"
    if not packet_path.is_file() or not schema_path.is_file():
        raise ConflictError("export the external packet before importing a response")
    if packet_path.read_bytes() != external_packet(run_dir, candidate, candidate_digest, manifest).encode("utf-8"):
        raise ConflictError("exported external packet does not match the frozen candidate")
    if schema_path.read_bytes() != canonical_json_bytes(
        external_response_schema(manifest, candidate)
    ):
        raise ConflictError("exported external response schema differs from this run")
    return candidate_path, candidate, candidate_digest


def import_external(run_dir: Path, candidate_id: str, raw_response: Path) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("CANDIDATE_ID must be a lowercase slug")
    try:
        raw = raw_response.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read external response {raw_response}: {exc}") from exc
    if not raw:
        raise InputError("external response is empty")
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        if state["stage"] != "holdout":
            raise ConflictError("external import requires holdout stage")
        _, candidate, candidate_digest = _external_identity(run_dir, manifest, candidate_id)
        raw_digest = sha256_bytes(raw)
        response_root = run_dir / "holdout" / candidate_id / f"v{candidate['version']}"
        raw_path = response_root / "raw" / f"external-{raw_digest}.txt"
        write_immutable(raw_path, raw, root=run_dir)
        raw_rel = raw_path.relative_to(run_dir).as_posix()
        event_path = response_root / "imports" / f"external-{raw_digest}.json"
        if event_path.is_file():
            existing = expect_object(load_json(event_path), "external import event")
            _ensure_import_receipt_event(run_dir, state, existing)
            validate_external_imports(run_dir, manifest)
            if existing.get("status") == "accepted":
                return {**existing, "idempotent": True}
            raise InputError(str(existing.get("error", "external response was previously rejected")))
        try:
            response = parse_external_object(raw, str(raw_response))
            if (
                response["candidate_id"] != candidate_id
                or response["candidate_version"] != candidate["version"]
            ):
                raise InputError("external response identity differs from the exact finalist")
            canonical = canonicalize_evaluator_response(
                response, manifest, run_dir, "holdout_external"
            )
        except WorkflowError as exc:
            event = {
                "schema_version": 1,
                "run_id": state["run_id"],
                "candidate_id": candidate_id,
                "raw_response_path": raw_rel,
                "raw_response_sha256": raw_digest,
                "status": "rejected",
                "error": str(exc),
            }
            write_immutable(event_path, canonical_json_bytes(event), root=run_dir)
            already_logged = any(
                item["event"] == "external_import_rejected"
                and item["details"].get("candidate_id") == candidate_id
                and item["details"].get("raw_response_sha256") == raw_digest
                for item in load_events(run_dir / "events.jsonl", state["run_id"])
            )
            if already_logged:
                validate_external_imports(run_dir, manifest)
            else:
                append_event(
                    run_dir,
                    state,
                    "external_import_rejected",
                    details={"candidate_id": candidate_id, "raw_response_sha256": raw_digest, "error": str(exc)},
                )
            raise
        evaluation_rel = evaluation_relpath(
            candidate_id, candidate["version"], "holdout_external", canonical["judge_id"]
        )
        evaluation_digest = write_immutable(
            run_dir / evaluation_rel,
            canonical_json_bytes(canonical),
            root=run_dir,
        )
        event = {
            "schema_version": 1,
            "run_id": state["run_id"],
            "candidate_id": candidate_id,
            "raw_response_path": raw_rel,
            "raw_response_sha256": raw_digest,
            "status": "accepted",
            "evaluation": evaluation_rel,
            "evaluation_sha256": evaluation_digest,
            "final_score": canonical["final_score"],
            "qualified": canonical["qualified"],
        }
        write_immutable(event_path, canonical_json_bytes(event), root=run_dir)
        already_logged = any(
            item["event"] == "external_import_accepted"
            and item["details"].get("evaluation") == evaluation_rel
            for item in load_events(run_dir / "events.jsonl", state["run_id"])
        )
        if already_logged:
            validate_external_imports(run_dir, manifest)
        else:
            append_event(
                run_dir,
                state,
                "external_import_accepted",
                details={
                    "candidate_id": candidate_id,
                    "evaluation": evaluation_rel,
                    "final_score": canonical["final_score"],
                },
            )
        return {**event, "idempotent": already_logged}


def _ensure_import_receipt_event(
    run_dir: Path,
    state: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> None:
    events = load_events(run_dir / "events.jsonl", state["run_id"])
    status = receipt.get("status")
    if status == "accepted":
        found = any(
            event["event"] == "external_import_accepted"
            and event["details"].get("evaluation") == receipt.get("evaluation")
            for event in events
        )
        if not found:
            append_event(
                run_dir,
                state,
                "external_import_accepted",
                details={
                    "candidate_id": receipt.get("candidate_id"),
                    "evaluation": receipt.get("evaluation"),
                    "final_score": receipt.get("final_score"),
                    "recovered_after_receipt_commit": True,
                },
            )
        return
    if status == "rejected":
        found = any(
            event["event"] == "external_import_rejected"
            and event["details"].get("candidate_id") == receipt.get("candidate_id")
            and event["details"].get("raw_response_sha256") == receipt.get("raw_response_sha256")
            for event in events
        )
        if not found:
            append_event(
                run_dir,
                state,
                "external_import_rejected",
                details={
                    "candidate_id": receipt.get("candidate_id"),
                    "raw_response_sha256": receipt.get("raw_response_sha256"),
                    "error": receipt.get("error"),
                    "recovered_after_receipt_commit": True,
                },
            )


def validate_external_imports(
    run_dir: Path,
    manifest: Mapping[str, Any],
) -> list[tuple[Path, dict[str, Any], dict[str, Any] | None]]:
    """Reconcile immutable import receipts with raw data, evaluations, and events."""
    receipts: list[tuple[Path, dict[str, Any], dict[str, Any] | None]] = []
    accepted_by_evaluation: dict[str, Path] = {}
    accepted_by_event_key: dict[str, Path] = {}
    rejected_by_event_key: dict[tuple[str, str], Path] = {}
    for receipt_path in sorted((run_dir / "holdout").glob("*/v*/imports/external-*.json")):
        _assert_safe_write_path(run_dir, receipt_path, "external import receipt path")
        relative = receipt_path.relative_to(run_dir)
        if len(relative.parts) != 5:
            raise InputError(f"external import receipt is stored at a noncanonical path: {relative}")
        _, path_candidate_id, version_part, imports_part, filename = relative.parts
        if imports_part != "imports" or not version_part.startswith("v"):
            raise InputError(f"external import receipt is stored at a noncanonical path: {relative}")
        candidate_id = expect_nonempty_string(path_candidate_id, "external import path candidate_id")
        if not SAFE_ID_RE.fullmatch(candidate_id):
            raise InputError("external import path candidate_id is invalid")
        try:
            version = int(version_part[1:])
        except ValueError as exc:
            raise InputError(f"external import receipt has an invalid version path: {relative}") from exc
        if version < 1:
            raise InputError(f"external import receipt has an invalid version path: {relative}")
        if version_part != f"v{version}":
            raise InputError(f"external import receipt has a noncanonical version path: {relative}")
        receipt = expect_object(load_json(receipt_path), "external import receipt")
        status = receipt.get("status")
        expected_keys = (
            IMPORT_RECEIPT_ACCEPTED_KEYS if status == "accepted" else IMPORT_RECEIPT_REJECTED_KEYS
            if status == "rejected" else set()
        )
        if not expected_keys:
            raise InputError("external import receipt status must be accepted or rejected")
        expect_object(receipt, "external import receipt", exact_keys=expected_keys)
        if expect_int(receipt["schema_version"], "external import receipt.schema_version") != 1:
            raise InputError("external import receipt.schema_version must be 1")
        if receipt["run_id"] != manifest["run_id"]:
            raise InputError("external import receipt identity differs from the run")
        if receipt["candidate_id"] != candidate_id:
            raise InputError("external import receipt candidate_id differs from its path")
        raw_digest = expect_nonempty_string(
            receipt["raw_response_sha256"], "external import raw_response_sha256"
        )
        if not SHA256_RE.fullmatch(raw_digest):
            raise InputError("external import raw_response_sha256 is invalid")
        expected_filename = f"external-{raw_digest}.json"
        if filename != expected_filename:
            raise InputError("external import receipt filename differs from its raw hash")
        expected_raw_rel = f"holdout/{candidate_id}/v{version}/raw/external-{raw_digest}.txt"
        if receipt["raw_response_path"] != expected_raw_rel:
            raise InputError("external import receipt raw_response_path is noncanonical")
        _, raw_path = run_relative_path(
            run_dir,
            receipt["raw_response_path"],
            "external import raw_response_path",
        )
        if sha256_file(raw_path) != raw_digest:
            raise InputError("external import raw response hash mismatch")
        candidate_path, candidate = finalist_candidate(run_dir, manifest, candidate_id)
        if candidate["version"] != version:
            raise InputError("external import receipt must bind the exact finalist version")
        canonical_evaluation: dict[str, Any] | None = None
        if status == "accepted":
            evaluation_rel, evaluation_path = run_relative_path(
                run_dir,
                receipt["evaluation"],
                "external import evaluation",
            )
            evaluation_digest = expect_nonempty_string(
                receipt["evaluation_sha256"], "external import evaluation_sha256"
            )
            if not SHA256_RE.fullmatch(evaluation_digest) or sha256_file(evaluation_path) != evaluation_digest:
                raise InputError("external import evaluation hash mismatch")
            canonical_evaluation = compute_evaluation(load_json(evaluation_path), manifest, run_dir)
            expected_evaluation_rel = evaluation_relpath(
                candidate_id,
                version,
                "holdout_external",
                canonical_evaluation["judge_id"],
            )
            if evaluation_rel != expected_evaluation_rel:
                raise InputError("external import evaluation path is noncanonical")
            if (
                canonical_evaluation["candidate_id"] != candidate_id
                or canonical_evaluation["candidate_version"] != version
                or canonical_evaluation["evaluation_type"] != "holdout_external"
            ):
                raise InputError("external import evaluation identity differs from its receipt")
            response = parse_external_object(raw_path.read_bytes(), str(raw_path))
            expected_evaluation = canonicalize_evaluator_response(
                response, manifest, run_dir, "holdout_external"
            )
            if canonical_evaluation != expected_evaluation:
                raise InputError("external import evaluation differs from its single raw response")
            if as_json_number(receipt["final_score"], "external import final_score") != as_json_number(
                canonical_evaluation["final_score"], "external evaluation final_score"
            ):
                raise InputError("external import final_score differs from its evaluation")
            if not isinstance(receipt["qualified"], bool) or receipt["qualified"] is not canonical_evaluation["qualified"]:
                raise InputError("external import qualified flag differs from its evaluation")
            if evaluation_rel in accepted_by_evaluation:
                raise InputError("multiple accepted import receipts reference one evaluation")
            accepted_by_evaluation[evaluation_rel] = receipt_path
            accepted_by_event_key[evaluation_rel] = receipt_path
        else:
            expect_nonempty_string(receipt["error"], "external import rejection error")
            rejected_by_event_key[(candidate_id, raw_digest)] = receipt_path
        receipts.append((receipt_path, dict(receipt), canonical_evaluation))

    external_paths = sorted((run_dir / "holdout").glob("*/v*/external-*.json"))
    for evaluation_path in external_paths:
        _assert_safe_write_path(run_dir, evaluation_path, "external evaluation path")
        evaluation = compute_evaluation(load_json(evaluation_path), manifest, run_dir)
        relative = evaluation_path.relative_to(run_dir).as_posix()
        if relative not in accepted_by_evaluation:
            raise InputError(f"external evaluation has no accepted import receipt: {relative}")

    events = load_events(run_dir / "events.jsonl", manifest["run_id"])
    accepted_events: dict[str, list[Mapping[str, Any]]] = {}
    rejected_events: dict[tuple[str, str], int] = {}
    for event in events:
        if event["event"] == "external_import_accepted":
            evaluation_rel = event["details"].get("evaluation")
            if not isinstance(evaluation_rel, str):
                raise InputError("external_import_accepted event is missing evaluation identity")
            accepted_events.setdefault(evaluation_rel, []).append(event)
        elif event["event"] == "external_import_rejected":
            key = (
                event["details"].get("candidate_id"),
                event["details"].get("raw_response_sha256"),
            )
            if not all(isinstance(value, str) for value in key):
                raise InputError("external_import_rejected event is missing raw response identity")
            rejected_events[key] = rejected_events.get(key, 0) + 1
    if set(accepted_events) != set(accepted_by_event_key) or any(len(items) != 1 for items in accepted_events.values()):
        raise InputError("accepted external import events and receipts do not reconcile")
    if set(rejected_events) != set(rejected_by_event_key) or any(count != 1 for count in rejected_events.values()):
        raise InputError("rejected external import events and receipts do not reconcile")
    receipt_by_path = {path: receipt for path, receipt, _ in receipts}
    for evaluation_rel, event_items in accepted_events.items():
        receipt = receipt_by_path[accepted_by_event_key[evaluation_rel]]
        details = event_items[0]["details"]
        if (
            details.get("candidate_id") != receipt["candidate_id"]
            or details.get("evaluation") != receipt["evaluation"]
            or as_json_number(details.get("final_score"), "external_import_accepted final_score")
            != as_json_number(receipt["final_score"], "external import receipt final_score")
        ):
            raise InputError("external_import_accepted event identity differs from its receipt")
    return receipts


def iter_evaluations(run_dir: Path, manifest: Mapping[str, Any]) -> Iterator[tuple[Path, dict[str, Any]]]:
    paths = sorted((run_dir / "evaluations").glob("*/v*/*.json")) + sorted(
        path
        for path in (run_dir / "holdout").glob("*/v*/*.json")
        if path.name.startswith(("native-", "external-"))
    )
    for path in paths:
        _assert_safe_write_path(run_dir, path, "evaluation artifact path")
        evaluation = compute_evaluation(load_json(path), manifest, run_dir)
        expected = run_dir / evaluation_relpath(
            evaluation["candidate_id"],
            evaluation["candidate_version"],
            evaluation["evaluation_type"],
            evaluation["judge_id"],
        )
        if path.resolve() != expected.resolve():
            raise InputError(f"evaluation stored at noncanonical path: {path.relative_to(run_dir)}")
        yield path, evaluation


def iter_research(run_dir: Path, manifest: Mapping[str, Any]) -> Iterator[tuple[Path, dict[str, Any]]]:
    for path in sorted((run_dir / "research").glob("*/v*.json")):
        _assert_safe_write_path(run_dir, path, "research artifact path")
        research = validate_research(load_json(path), manifest, run_dir)
        expected = run_dir / research_relpath(research["candidate_id"], research["candidate_version"])
        if path.resolve() != expected.resolve():
            raise InputError(f"research stored at noncanonical path: {path.relative_to(run_dir)}")
        yield path, research


def _candidate_reference(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    label: str,
    *,
    required_stage: str | set[str] = "discovery",
) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    reference = expect_object(value, label, exact_keys=PORTFOLIO_REF_KEYS)
    candidate_id = expect_nonempty_string(reference["candidate_id"], f"{label}.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError(f"{label}.candidate_id must be a lowercase slug")
    version = expect_int(reference["version"], f"{label}.version", minimum=1)
    digest = reference["candidate_sha256"]
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise InputError(f"{label}.candidate_sha256 is invalid")
    path = run_dir / candidate_relpath(candidate_id, version)
    if not path.is_file():
        raise InputError(f"{label} candidate artifact does not exist")
    if sha256_file(path) != digest:
        raise InputError(f"{label}.candidate_sha256 does not match the immutable candidate")
    candidate = validate_candidate(load_json(path), manifest, run_dir)
    allowed_stages = {required_stage} if isinstance(required_stage, str) else required_stage
    if candidate["stage"] not in allowed_stages:
        expected = ", ".join(sorted(allowed_stages))
        raise InputError(f"{label} must bind a candidate in stage: {expected}")
    return dict(reference), path, candidate


def _require_core_preliminary_evidence(
    candidate: Mapping[str, Any],
    control_evidence: Mapping[str, Any] | None,
    label: str,
) -> None:
    supported_types = {
        claim["claim_type"]
        for claim in candidate["claims"]
        if claim["evidence_refs"]
    }
    missing = sorted(CORE_READINESS_CLAIM_TYPES - supported_types)
    if missing:
        raise InputError(
            f"{label} is not ready for a core shortlist slot; missing source-backed claim types: {missing}"
        )
    if control_evidence is None or control_evidence["assessment"] != "credible_preliminary":
        raise InputError(
            f"{label} is not ready for a core shortlist slot; "
            "control-point acquisition evidence must be credible_preliminary"
        )


def _validate_control_point_acquisition_evidence(
    value: Any,
    candidate: Mapping[str, Any],
    label: str,
) -> dict[str, Any] | None:
    if value is None:
        return None
    evidence = expect_object(
        value,
        label,
        exact_keys=CONTROL_POINT_ACQUISITION_EVIDENCE_KEYS,
    )
    assessment = evidence["assessment"]
    if assessment not in CONTROL_POINT_ACQUISITION_ASSESSMENTS:
        raise InputError(f"{label}.assessment is invalid")
    acquisition_mode = evidence["acquisition_mode"]
    if acquisition_mode not in CONTROL_POINT_ACQUISITION_MODES:
        raise InputError(f"{label}.acquisition_mode is invalid")
    canonical: dict[str, Any] = {
        "assessment": assessment,
        "acquisition_mode": acquisition_mode,
    }
    for key in (
        "counterparty_or_source",
        "instrument_or_transaction",
        "founder_access_path",
        "credibility_rationale",
    ):
        canonical[key] = expect_nonempty_string(evidence[key], f"{label}.{key}").strip()
    claim_ids = expect_string_list(evidence["claim_ids"], f"{label}.claim_ids", unique=True)
    evidence_refs = expect_string_list(
        evidence["evidence_refs"], f"{label}.evidence_refs", unique=True
    )
    canonical["unresolved_preconditions"] = expect_string_list(
        evidence["unresolved_preconditions"],
        f"{label}.unresolved_preconditions",
        unique=True,
    )
    claims_by_id = {claim["claim_id"]: claim for claim in candidate["claims"]}
    unknown_claims = sorted(set(claim_ids) - set(claims_by_id))
    if unknown_claims:
        raise InputError(f"{label}.claim_ids reference unknown candidate claims: {unknown_claims}")
    unknown_sources = sorted(set(evidence_refs) - set(candidate["source_refs"]))
    if unknown_sources:
        raise InputError(f"{label}.evidence_refs reference unknown candidate sources: {unknown_sources}")
    cited_claim_sources = {
        source_ref
        for claim_id in claim_ids
        for source_ref in claims_by_id[claim_id]["evidence_refs"]
    }
    uncited_sources = sorted(set(evidence_refs) - cited_claim_sources)
    if uncited_sources:
        raise InputError(
            f"{label}.evidence_refs must be cited by its claim_ids: {uncited_sources}"
        )
    if assessment == "credible_preliminary":
        if not claim_ids or not evidence_refs:
            raise InputError(
                f"{label} credible_preliminary evidence requires nonempty claim_ids and evidence_refs"
            )
        if not any(
            claims_by_id[claim_id]["claim_type"] == "founder_control_point_path"
            for claim_id in claim_ids
        ):
            raise InputError(
                f"{label} credible_preliminary evidence must cite a founder_control_point_path claim"
            )
    canonical["claim_ids"] = claim_ids
    canonical["evidence_refs"] = evidence_refs
    return canonical


def _screening_structure_key(candidate: Mapping[str, Any]) -> tuple[str, ...]:
    if "structural_signature" in candidate:
        return structural_signature_key(candidate)
    return tuple(
        normalize_fingerprint(candidate["structure"][key])
        for key in sorted(STRUCTURE_KEYS)
    )


def _score_screening_winners(
    run_dir: Path, manifest: Mapping[str, Any]
) -> list[tuple[Path, dict[str, Any], dict[str, Any]]]:
    if control_contract_enabled(manifest["config"]):
        aggregation = load_screening_aggregation(run_dir, manifest)
        records = {
            row["candidate_ref"]["candidate_id"]: {
                "final_score": row["canonical_score"]
            }
            for row in aggregation["candidates"]
        }
    else:
        coverage = _require_working_evaluation_coverage(
            run_dir, manifest, "screening"
        )
        records = {
            record["candidate_id"]: record for record in coverage["records"]
        }
    batches = load_screening_batches(run_dir, manifest)
    ranked_by_batch: dict[
        str, list[tuple[Path, dict[str, Any], dict[str, Any]]]
    ] = {}
    for batch in batches["batches"]:
        rows: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
        for ref in batch["candidate_refs"]:
            candidate_path = run_dir / candidate_relpath(
                ref["candidate_id"], ref["version"]
            )
            candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
            record = records[candidate["candidate_id"]]
            evaluation = {"final_score": record["final_score"]}
            rows.append((candidate_path, candidate, evaluation))
        ranked_by_batch[batch["batch_id"]] = sorted(
            rows,
            key=lambda item: (
                -as_decimal(item[2]["final_score"], "screening final score"),
                item[1]["candidate_id"],
            ),
        )

    advance_count = (
        manifest["config"]["shortlist_max"]
        // manifest["config"]["screening_batches"]
    )
    initial = [
        (batch_id, *row)
        for batch_id, rows in ranked_by_batch.items()
        for row in rows[:advance_count]
    ]
    by_structure: dict[
        tuple[str, ...], list[tuple[str, Path, dict[str, Any], dict[str, Any]]]
    ] = {}
    for row in initial:
        by_structure.setdefault(_screening_structure_key(row[2]), []).append(row)
    selected: list[tuple[str, Path, dict[str, Any], dict[str, Any]]] = []
    dropped_batches: list[str] = []
    for rows in by_structure.values():
        ordered = sorted(
            rows,
            key=lambda item: (
                -as_decimal(item[3]["final_score"], "screening final score"),
                item[2]["candidate_id"],
            ),
        )
        selected.append(ordered[0])
        dropped_batches.extend(item[0] for item in ordered[1:])
    selected_ids = {row[2]["candidate_id"] for row in selected}
    selected_structures = {_screening_structure_key(row[2]) for row in selected}
    for batch_id in sorted(dropped_batches):
        replacement = next(
            (
                row
                for row in ranked_by_batch[batch_id]
                if row[1]["candidate_id"] not in selected_ids
                and _screening_structure_key(row[1]) not in selected_structures
            ),
            None,
        )
        if replacement is None:
            raise ConflictError(
                f"screening deduplication cannot backfill {batch_id} with a distinct scored candidate"
            )
        selected.append((batch_id, *replacement))
        selected_ids.add(replacement[1]["candidate_id"])
        selected_structures.add(_screening_structure_key(replacement[1]))
    if len(selected) != manifest["config"]["shortlist_max"]:
        raise ConflictError("screening did not produce the configured shortlist size")
    return [
        (path, candidate, evaluation)
        for _, path, candidate, evaluation in sorted(
            selected, key=lambda item: item[2]["candidate_id"]
        )
    ]


def build_score_portfolio_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    if not score_bracket_enabled(manifest["config"]):
        raise ConflictError("this run does not use score-bracket selection")
    batches = load_screening_batches(run_dir, manifest)
    calibrated: list[dict[str, Any]] = []
    for batch in batches["batches"]:
        for ref in batch["candidate_refs"]:
            candidate_path = run_dir / candidate_relpath(
                ref["candidate_id"], ref["version"]
            )
            candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
            calibrated.append(
                {
                    "candidate_ref": dict(ref),
                    "commercial_archetype": candidate["structure"]["commercial_archetype"],
                    "control_point": candidate["structure"]["control_point"],
                    "critical_dependency": candidate["structure"]["critical_dependency"],
                    "control_point_acquisition_evidence": None,
                }
            )
    payload = {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "selection_version": 1,
        "calibration": calibrated,
        "candidate_refs": [
            {
                "candidate_id": candidate["candidate_id"],
                "version": candidate["version"],
                "candidate_sha256": sha256_file(path),
            }
            for path, candidate, _ in _score_screening_winners(run_dir, manifest)
        ],
        "wildcard_candidate_refs": [],
        "missing_archetypes": [],
        "rationale": (
            "Deterministic top scores from each lane-balanced screening batch, "
            "with structural deduplication and same-batch score backfill."
        ),
    }
    return validate_portfolio_selection(
        payload, manifest, run_dir, _verify_generated=False
    )


def validate_portfolio_selection(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    *,
    _verify_generated: bool = True,
) -> dict[str, Any]:
    if manifest["config"]["schema_version"] != ACTIVE_SCHEMA_VERSION:
        raise InputError("portfolio selection requires the active workflow schema")
    selection = expect_object(value, "portfolio selection", exact_keys=PORTFOLIO_SELECTION_KEYS)
    if expect_int(selection["schema_version"], "portfolio selection.schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError(f"portfolio selection.schema_version must be {ACTIVE_SCHEMA_VERSION}")
    if expect_int(selection["selection_version"], "portfolio selection.selection_version") != 1:
        raise InputError("portfolio selection.selection_version must be 1")
    expect_nonempty_string(selection["rationale"], "portfolio selection.rationale")
    expect_string_list(
        selection["missing_archetypes"], "portfolio selection.missing_archetypes", unique=True
    )
    calibration_value = selection["calibration"]
    if not isinstance(calibration_value, list):
        raise InputError("portfolio selection.calibration must be a list")
    if score_bracket_enabled(manifest["config"]):
        batches = load_screening_batches(run_dir, manifest)
        discoveries = []
        for batch in batches["batches"]:
            for ref in batch["candidate_refs"]:
                path = run_dir / candidate_relpath(ref["candidate_id"], ref["version"])
                discoveries.append(
                    (path, validate_candidate(load_json(path), manifest, run_dir))
                )
    else:
        discoveries = latest_candidates_for_stage(run_dir, manifest, "discovery")
    expected_discovery_refs = {
        (candidate["candidate_id"], candidate["version"], sha256_file(path))
        for path, candidate in discoveries
    }
    calibration_rows: list[dict[str, Any]] = []
    calibrated_refs: set[tuple[str, int, str]] = set()
    for index, raw in enumerate(calibration_value):
        row = expect_object(
            raw,
            f"portfolio selection.calibration[{index}]",
            exact_keys=CALIBRATION_ROW_KEYS,
        )
        reference, _, candidate = _candidate_reference(
            row["candidate_ref"],
            manifest,
            run_dir,
            f"portfolio selection.calibration[{index}].candidate_ref",
        )
        identity = (
            reference["candidate_id"],
            reference["version"],
            reference["candidate_sha256"],
        )
        if identity in calibrated_refs:
            raise InputError("portfolio selection.calibration contains a duplicate candidate")
        calibrated_refs.add(identity)
        canonical_row = {"candidate_ref": reference}
        for key in STRUCTURE_KEYS:
            canonical_row[key] = expect_nonempty_string(
                row[key], f"portfolio selection.calibration[{index}].{key}"
            ).strip()
        canonical_row["control_point_acquisition_evidence"] = (
            _validate_control_point_acquisition_evidence(
                row["control_point_acquisition_evidence"],
                candidate,
                f"portfolio selection.calibration[{index}].control_point_acquisition_evidence",
            )
        )
        calibration_rows.append(canonical_row)
    if calibrated_refs != expected_discovery_refs:
        raise InputError(
            "portfolio selection.calibration must cover every discovery candidate exactly once with hash-bound refs"
        )

    values = selection["candidate_refs"]
    if not isinstance(values, list) or not 1 <= len(values) <= manifest["config"]["shortlist_max"]:
        raise InputError("portfolio selection candidate_refs count is outside shortlist limits")
    references: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    identities: set[tuple[str, int]] = set()
    fingerprints: set[tuple[str, ...]] = set()
    for index, raw in enumerate(values):
        reference, _, candidate = _candidate_reference(
            raw, manifest, run_dir, f"portfolio selection.candidate_refs[{index}]"
        )
        identity = (reference["candidate_id"], reference["version"])
        if identity in identities:
            raise InputError("portfolio selection contains a duplicate candidate reference")
        identities.add(identity)
        fingerprint = tuple(
            normalize_fingerprint(candidate["fingerprint"][key]) for key in sorted(FINGERPRINT_KEYS)
        )
        if fingerprint in fingerprints:
            raise InputError("portfolio selection contains duplicate exact fingerprints")
        fingerprints.add(fingerprint)
        full_identity = (
            reference["candidate_id"],
            reference["version"],
            reference["candidate_sha256"],
        )
        if full_identity not in calibrated_refs:
            raise InputError("portfolio selection candidate_refs must come from the calibrated pool")
        references.append(reference)
        candidates.append(candidate)

    discovery_unique_fingerprints = {
        tuple(
            normalize_fingerprint(candidate["fingerprint"][key])
            for key in sorted(FINGERPRINT_KEYS)
        )
        for _, candidate in discoveries
    }
    if (
        len(discovery_unique_fingerprints) >= manifest["config"]["shortlist_max"]
        and len(references) != manifest["config"]["shortlist_max"]
    ):
        raise InputError(
            "portfolio selection must fill every configured shortlist slot when the unique pool is large enough"
        )

    wildcard_values = selection["wildcard_candidate_refs"]
    if not isinstance(wildcard_values, list):
        raise InputError("portfolio selection.wildcard_candidate_refs must be a list")
    wildcard_refs: list[dict[str, Any]] = []
    wildcard_identities: set[tuple[str, int, str]] = set()
    selected_by_identity = {
        (ref["candidate_id"], ref["version"], ref["candidate_sha256"]): candidate
        for ref, candidate in zip(references, candidates, strict=True)
    }
    for index, raw in enumerate(wildcard_values):
        reference, _, _ = _candidate_reference(
            raw,
            manifest,
            run_dir,
            f"portfolio selection.wildcard_candidate_refs[{index}]",
        )
        identity = (
            reference["candidate_id"],
            reference["version"],
            reference["candidate_sha256"],
        )
        if identity in wildcard_identities:
            raise InputError("portfolio selection contains a duplicate wildcard reference")
        if identity not in selected_by_identity:
            raise InputError("portfolio wildcards must be a subset of candidate_refs")
        wildcard_identities.add(identity)
        wildcard_refs.append(reference)
    if score_bracket_enabled(manifest["config"]):
        if wildcard_refs:
            raise InputError(
                "score-bracket selection uses score advancement only; wildcard labels cannot alter selection"
            )
    else:
        wildcard_max = manifest["config"]["wildcard_shortlist_slots"]
        if len(wildcard_refs) > wildcard_max:
            raise InputError("portfolio selection exceeds wildcard_shortlist_slots")
        if len(references) == manifest["config"]["shortlist_max"]:
            if len(wildcard_refs) != wildcard_max:
                raise InputError(
                    "a full portfolio selection must preserve every configured wildcard slot"
                )
            if len(references) - len(wildcard_refs) != manifest["config"]["core_shortlist_slots"]:
                raise InputError(
                    "a full portfolio selection must fill every configured core slot"
                )

    calibration_by_identity = {
        (
            row["candidate_ref"]["candidate_id"],
            row["candidate_ref"]["version"],
            row["candidate_ref"]["candidate_sha256"],
        ): row
        for row in calibration_rows
    }
    if not score_bracket_enabled(manifest["config"]):
        core_identities = set(selected_by_identity) - wildcard_identities
        for identity in sorted(core_identities):
            calibration_row = calibration_by_identity[identity]
            _require_core_preliminary_evidence(
                selected_by_identity[identity],
                calibration_row["control_point_acquisition_evidence"],
                f"portfolio core candidate {identity[0]} v{identity[1]}",
            )
        core_triples = {
            tuple(normalize_fingerprint(calibration_by_identity[identity][key]) for key in sorted(STRUCTURE_KEYS))
            for identity in core_identities
        }
        for identity in wildcard_identities:
            triple = tuple(
                normalize_fingerprint(calibration_by_identity[identity][key])
                for key in sorted(STRUCTURE_KEYS)
            )
            if triple in core_triples:
                raise InputError(
                    "a wildcard cannot be an exact calibrated structural copy of a core candidate"
                )
    canonical = dict(selection)
    canonical["calibration"] = sorted(
        calibration_rows,
        key=lambda item: (
            item["candidate_ref"]["candidate_id"],
            item["candidate_ref"]["version"],
        ),
    )
    canonical["candidate_refs"] = sorted(references, key=lambda item: (item["candidate_id"], item["version"]))
    canonical["wildcard_candidate_refs"] = sorted(
        wildcard_refs, key=lambda item: (item["candidate_id"], item["version"])
    )
    canonical["rationale"] = selection["rationale"].strip()
    if score_bracket_enabled(manifest["config"]) and _verify_generated:
        expected = build_score_portfolio_selection(run_dir, manifest)
        if canonical != expected:
            raise InputError(
                "score-bracket portfolio selection differs from deterministic screening results"
            )
    return canonical


def _validate_portfolio_amendment_record(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    *,
    expected_version: int,
    expected_base_digest: str,
    current_refs: Sequence[Mapping[str, Any]],
    current_wildcard_refs: Sequence[Mapping[str, Any]],
    calibrated_refs: Sequence[Mapping[str, Any]],
    calibration_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    amendment = expect_object(value, "portfolio amendment", exact_keys=PORTFOLIO_AMENDMENT_KEYS)
    if expect_int(amendment["schema_version"], "portfolio amendment.schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError(
            f"portfolio amendment.schema_version must be {ACTIVE_SCHEMA_VERSION}"
        )
    version = expect_int(amendment["amendment_version"], "portfolio amendment.amendment_version", minimum=1)
    if version != expected_version:
        raise InputError(f"portfolio amendment version must be {expected_version}")
    if amendment["base_selection_sha256"] != expected_base_digest:
        raise InputError("portfolio amendment base_selection_sha256 does not match its immediate predecessor")
    expect_nonempty_string(amendment["reason"], "portfolio amendment.reason")
    remove_ref, _, _ = _candidate_reference(
        amendment["remove_candidate_ref"], manifest, run_dir, "portfolio amendment.remove_candidate_ref"
    )
    add_ref, _, add_candidate = _candidate_reference(
        amendment["add_candidate_ref"], manifest, run_dir, "portfolio amendment.add_candidate_ref"
    )
    current = [dict(item) for item in current_refs]
    remove_identity = (
        remove_ref["candidate_id"],
        remove_ref["version"],
        remove_ref["candidate_sha256"],
    )
    add_identity = (
        add_ref["candidate_id"],
        add_ref["version"],
        add_ref["candidate_sha256"],
    )
    identities = {
        (item["candidate_id"], item["version"], item["candidate_sha256"])
        for item in current
    }
    if remove_identity not in identities:
        raise InputError("portfolio amendment remove_candidate_ref is not in the effective shortlist")
    if (
        run_dir
        / research_relpath(remove_ref["candidate_id"], remove_ref["version"])
    ).is_file():
        raise ConflictError(
            "portfolio amendment cannot remove a candidate after immutable research exists"
        )
    if add_identity in identities:
        raise InputError("portfolio amendment add_candidate_ref is already in the effective shortlist")
    updated = [
        item
        for item in current
        if (item["candidate_id"], item["version"], item["candidate_sha256"])
        != remove_identity
    ]
    updated.append(add_ref)
    calibrated_identities = {
        (item["candidate_id"], item["version"], item["candidate_sha256"])
        for item in calibrated_refs
    }
    if (
        add_ref["candidate_id"],
        add_ref["version"],
        add_ref["candidate_sha256"],
    ) not in calibrated_identities:
        raise InputError("portfolio amendment addition must come from the hash-bound calibrated pool")
    wildcard_identities = {
        (item["candidate_id"], item["version"], item["candidate_sha256"])
        for item in current_wildcard_refs
    }
    updated_wildcards = [dict(item) for item in current_wildcard_refs]
    if remove_identity in wildcard_identities:
        updated_wildcards = [
            item
            for item in updated_wildcards
            if (item["candidate_id"], item["version"], item["candidate_sha256"])
            != remove_identity
        ]
        updated_wildcards.append(add_ref)
        core_refs = [
            item
            for item in current
            if (
                item["candidate_id"],
                item["version"],
                item["candidate_sha256"],
            )
            not in wildcard_identities
        ]
        add_triple = tuple(
            normalize_fingerprint(add_candidate["structure"][key])
            for key in sorted(STRUCTURE_KEYS)
        )
        for core_ref in core_refs:
            _, _, core_candidate = _candidate_reference(
                core_ref, manifest, run_dir, "portfolio amendment core candidate"
            )
            core_triple = tuple(
                normalize_fingerprint(core_candidate["structure"][key])
                for key in sorted(STRUCTURE_KEYS)
            )
            if add_triple == core_triple:
                raise InputError(
                    "a wildcard replacement cannot be an exact structural copy of a core candidate"
                )
    else:
        calibration_by_identity = {
            (
                row["candidate_ref"]["candidate_id"],
                row["candidate_ref"]["version"],
                row["candidate_ref"]["candidate_sha256"],
            ): row
            for row in calibration_rows
        }
        add_identity = (
            add_ref["candidate_id"],
            add_ref["version"],
            add_ref["candidate_sha256"],
        )
        _require_core_preliminary_evidence(
            add_candidate,
            calibration_by_identity[add_identity]["control_point_acquisition_evidence"],
            f"portfolio amendment core replacement {add_candidate['candidate_id']} v{add_candidate['version']}",
        )
    canonical = dict(amendment)
    canonical["remove_candidate_ref"] = remove_ref
    canonical["add_candidate_ref"] = add_ref
    canonical["reason"] = amendment["reason"].strip()
    return (
        canonical,
        sorted(updated, key=lambda item: (item["candidate_id"], item["version"])),
        sorted(
            updated_wildcards,
            key=lambda item: (item["candidate_id"], item["version"]),
        ),
    )


def effective_portfolio_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    selection_path = run_dir / "portfolio" / "selection.json"
    if not selection_path.is_file():
        raise InputError("canonical portfolio selection is missing")
    selection = validate_portfolio_selection(load_json(selection_path), manifest, run_dir)
    if selection_path.read_bytes() != canonical_json_bytes(selection):
        raise InputError("portfolio selection is not canonical")
    current_refs = list(selection["candidate_refs"])
    current_wildcard_refs = list(selection["wildcard_candidate_refs"])
    calibrated_refs = [row["candidate_ref"] for row in selection["calibration"]]
    base_digest = sha256_file(selection_path)
    amendments: list[dict[str, Any]] = []
    amendment_paths = sorted(
        (run_dir / "portfolio" / "amendments").glob("v*.json"),
        key=lambda path: int(path.stem[1:]) if path.stem[1:].isdigit() else -1,
    )
    if score_bracket_enabled(manifest["config"]) and amendment_paths:
        raise InputError("score-bracket portfolio selection cannot be amended manually")
    for expected_version, path in enumerate(amendment_paths, start=1):
        if path.stem != f"v{expected_version}":
            raise InputError("portfolio amendment versions must be contiguous")
        amendment, current_refs, current_wildcard_refs = _validate_portfolio_amendment_record(
            load_json(path), manifest, run_dir,
            expected_version=expected_version,
            expected_base_digest=base_digest,
            current_refs=current_refs,
            current_wildcard_refs=current_wildcard_refs,
            calibrated_refs=calibrated_refs,
            calibration_rows=selection["calibration"],
        )
        if path.read_bytes() != canonical_json_bytes(amendment):
            raise InputError(f"portfolio amendment v{expected_version} is not canonical")
        amendments.append(amendment)
        base_digest = sha256_file(path)
    return {
        "selection_path": "portfolio/selection.json",
        "selection_sha256": sha256_file(selection_path),
        "latest_binding_sha256": base_digest,
        "amendments": amendments,
        "candidate_refs": current_refs,
        "wildcard_candidate_refs": current_wildcard_refs,
        "calibration": selection["calibration"],
        "calibrated_refs": calibrated_refs,
    }


def _working_evaluations_for_candidate(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate_path: Path,
    candidate: Mapping[str, Any],
    evaluation_type: str,
) -> list[tuple[Path, dict[str, Any]]]:
    digest = sha256_file(candidate_path)
    return [
        (path, evaluation)
        for path, evaluation in iter_evaluations(run_dir, manifest)
        if evaluation["evaluation_type"] == evaluation_type
        and evaluation["candidate_id"] == candidate["candidate_id"]
        and evaluation["candidate_version"] == candidate["version"]
        and evaluation["candidate_sha256"] == digest
    ]


def working_evaluation_coverage(
    run_dir: Path, manifest: Mapping[str, Any], phase: str
) -> dict[str, Any]:
    batch_id_by_candidate: dict[str, str] = {}
    if phase == "screening":
        batches = load_screening_batches(run_dir, manifest)
        rows = []
        for batch in batches["batches"]:
            for ref in batch["candidate_refs"]:
                candidate_path = run_dir / candidate_relpath(
                    ref["candidate_id"], ref["version"]
                )
                rows.append(
                    (
                        candidate_path,
                        validate_candidate(load_json(candidate_path), manifest, run_dir),
                    )
                )
                batch_id_by_candidate[ref["candidate_id"]] = batch["batch_id"]
        evaluation_type = "working_screening"
    elif phase == "screening_secondary":
        plan = load_secondary_screening_plan(run_dir, manifest)
        rows = []
        for batch in plan["batches"]:
            for ref in batch["candidate_refs"]:
                candidate_path = run_dir / candidate_relpath(
                    ref["candidate_id"], ref["version"]
                )
                rows.append(
                    (
                        candidate_path,
                        validate_candidate(
                            load_json(candidate_path), manifest, run_dir
                        ),
                    )
                )
                batch_id_by_candidate[ref["candidate_id"]] = batch[
                    "secondary_batch_id"
                ]
        evaluation_type = "working_screening_secondary"
    elif phase == "research":
        rows = [
            (
                run_dir / candidate_relpath(record["candidate_id"], record["candidate_version"]),
                validate_candidate(
                    load_json(
                        run_dir
                        / candidate_relpath(record["candidate_id"], record["candidate_version"])
                    ),
                    manifest,
                    run_dir,
                ),
            )
            for _, record in iter_research(run_dir, manifest)
        ]
        evaluation_type = "working_research"
    elif phase == "development":
        rows = []
        decision_path = run_dir / "portfolio" / "development-decision.json"
        if decision_path.is_file():
            decision = _load_portfolio_decision(run_dir, manifest)
            for row in decision["candidate_decisions"]:
                if row["disposition"] != "develop":
                    continue
                result_path = run_dir / "development" / row["candidate_id"] / "constructor-result.json"
                if not result_path.is_file():
                    continue
                _, result = _development_result_for_candidate(
                    run_dir, manifest, row["candidate_id"]
                )
                versions = (
                    [result["base_candidate_version"], result["final_candidate_version"]]
                    if score_bracket_enabled(manifest["config"])
                    and result["outcome"] == "redesigned"
                    else [result["final_candidate_version"]]
                )
                for version in dict.fromkeys(versions):
                    candidate_path = run_dir / candidate_relpath(
                        row["candidate_id"], version
                    )
                    rows.append(
                        (
                            candidate_path,
                            validate_candidate(
                                load_json(candidate_path), manifest, run_dir
                            ),
                        )
                    )
        evaluation_type = "working_development"
    else:
        raise InputError(
            "working evaluation phase must be screening, screening_secondary, research, or development"
        )
    expected_per_candidate = (
        manifest["config"]["development_evaluators_per_lineage"]
        if phase == "development"
        and control_contract_enabled(manifest["config"])
        else 1
    )
    records: list[dict[str, Any]] = []
    missing: list[str] = []
    duplicates: list[str] = []
    evaluation_index: dict[
        tuple[str, str, int, str], list[tuple[Path, dict[str, Any]]]
    ] = {}
    for evaluation_path, evaluation in iter_evaluations(run_dir, manifest):
        key = (
            evaluation["evaluation_type"],
            evaluation["candidate_id"],
            evaluation["candidate_version"],
            evaluation["candidate_sha256"],
        )
        evaluation_index.setdefault(key, []).append((evaluation_path, evaluation))
    for candidate_path, candidate in rows:
        matching = evaluation_index.get(
            (
                evaluation_type,
                candidate["candidate_id"],
                candidate["version"],
                sha256_file(candidate_path),
            ),
            [],
        )
        identity = f"{candidate['candidate_id']} v{candidate['version']}"
        if len(matching) < expected_per_candidate:
            missing.append(identity)
        elif len(matching) > expected_per_candidate:
            duplicates.append(identity)
        for evaluation_path, evaluation in matching:
            record = {
                "candidate_id": candidate["candidate_id"],
                "candidate_version": candidate["version"],
                "candidate_sha256": sha256_file(candidate_path),
                "evaluation_phase": phase,
                "evaluation_path": evaluation_path.relative_to(run_dir).as_posix(),
                "evaluation_sha256": sha256_file(evaluation_path),
                "judge_id": evaluation["judge_id"],
                "final_score": evaluation["final_score"],
                "economics_score": None if _factor_score(evaluation, "Business model and economics") is None else decimal_json(_factor_score(evaluation, "Business model and economics")),
                "distribution_score": None if _factor_score(evaluation, "Distribution") is None else decimal_json(_factor_score(evaluation, "Distribution")),
                "primary_score_limiter": evaluation["primary_score_limiter"],
                "strongest_disconfirming_evidence": evaluation["strongest_disconfirming_evidence"],
                "evidence_needed_for_higher_score": evaluation["evidence_needed_for_higher_score"],
            }
            if phase in {"screening", "screening_secondary"}:
                record["screening_batch_id"] = batch_id_by_candidate[
                    candidate["candidate_id"]
                ]
            records.append(record)
    judge_conflicts: list[str] = []
    batch_rows: list[dict[str, Any]] = []
    if phase in {"screening", "screening_secondary"}:
        judges_by_batch: dict[str, set[str]] = {
            batch_id: set() for batch_id in sorted(set(batch_id_by_candidate.values()))
        }
        batches_by_judge: dict[str, set[str]] = {}
        for record in records:
            batch_id = record["screening_batch_id"]
            judge_id = record["judge_id"]
            judges_by_batch[batch_id].add(judge_id)
            batches_by_judge.setdefault(judge_id, set()).add(batch_id)
        for batch_id, judge_ids in sorted(judges_by_batch.items()):
            if len(judge_ids) > 1:
                judge_conflicts.append(
                    f"{batch_id} uses multiple evaluator identities"
                )
            batch_rows.append(
                {
                    "batch_id": batch_id,
                    "judge_id": next(iter(judge_ids)) if len(judge_ids) == 1 else None,
                    "completed_count": sum(
                        record["screening_batch_id"] == batch_id for record in records
                    ),
                }
            )
        for judge_id, batch_ids in sorted(batches_by_judge.items()):
            if len(batch_ids) > 1:
                judge_conflicts.append(
                    f"evaluator {judge_id} is reused across screening batches"
                )
        if phase == "screening_secondary":
            primary_judges = {
                evaluation["judge_id"]
                for _, evaluation in iter_evaluations(run_dir, manifest)
                if evaluation["evaluation_type"] == "working_screening"
            }
            reused = sorted(
                {record["judge_id"] for record in records} & primary_judges
            )
            if reused:
                judge_conflicts.append(
                    "secondary screening evaluators must be fresh from primary screening: "
                    + ", ".join(reused)
                )
    if phase == "development" and score_bracket_enabled(manifest["config"]):
        judges_by_candidate_version: dict[tuple[str, int], set[str]] = {}
        lineages_by_judge: dict[str, set[str]] = {}
        for record in records:
            judges_by_candidate_version.setdefault(
                (record["candidate_id"], record["candidate_version"]), set()
            ).add(record["judge_id"])
            lineages_by_judge.setdefault(record["judge_id"], set()).add(
                record["candidate_id"]
            )
        candidate_versions: dict[str, list[set[str]]] = {}
        for (candidate_id, _), judge_ids in sorted(
            judges_by_candidate_version.items()
        ):
            candidate_versions.setdefault(candidate_id, []).append(judge_ids)
        for candidate_id, judge_sets in sorted(candidate_versions.items()):
            if any(
                len(judge_ids) != expected_per_candidate
                for judge_ids in judge_sets
            ) or any(judge_ids != judge_sets[0] for judge_ids in judge_sets[1:]):
                judge_conflicts.append(
                    f"{candidate_id} base and redesign must use the same configured independent development evaluators"
                )
        for judge_id, candidate_ids in sorted(lineages_by_judge.items()):
            if len(candidate_ids) > 1:
                judge_conflicts.append(
                    f"development evaluator {judge_id} is reused across lineages"
                )
    required_count = len(rows) * expected_per_candidate
    result = {
        "candidate_count": len(rows),
        "completed_count": len(records),
        "complete": (
            required_count == len(records)
            and not missing
            and not duplicates
            and not judge_conflicts
        ),
        "missing": missing,
        "duplicates": duplicates,
        "records": sorted(
            records,
            key=lambda item: (
                item["candidate_id"],
                item["candidate_version"],
                item["judge_id"],
            ),
        ),
    }
    if control_contract_enabled(manifest["config"]):
        result["required_evaluation_count"] = required_count
    if phase in {"screening", "screening_secondary"}:
        result.update({"judge_conflicts": judge_conflicts, "batches": batch_rows})
    elif phase == "development" and score_bracket_enabled(manifest["config"]):
        result["judge_conflicts"] = judge_conflicts
    return result


def _require_working_evaluation_coverage(
    run_dir: Path, manifest: Mapping[str, Any], phase: str
) -> dict[str, Any]:
    coverage = working_evaluation_coverage(run_dir, manifest, phase)
    if not coverage["complete"]:
        details = [
            *(f"missing {item}" for item in coverage["missing"]),
            *(f"duplicate {item}" for item in coverage["duplicates"]),
            *coverage.get("judge_conflicts", []),
        ]
        if control_contract_enabled(manifest["config"]):
            prefix = (
                f"{phase} requires the configured working-evaluation coverage "
                "for every candidate: "
            )
        else:
            prefix = f"{phase} requires exactly one working evaluation per candidate: "
        raise ConflictError(prefix + ", ".join(details))
    return coverage


def _working_rank_key(
    candidate: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    config: Mapping[str, Any],
) -> tuple[Any, ...]:
    if score_bracket_enabled(config):
        return (
            -as_decimal(evaluation["final_score"], "working final score"),
            candidate["candidate_id"],
        )
    negative_infinity = Decimal("-Infinity")
    positive_infinity = Decimal("Infinity")
    economics = _factor_score(evaluation, "Business model and economics")
    distribution = _factor_score(evaluation, "Distribution")
    capital_value = candidate["economics"]["capital_required_pln"]
    capital = (
        as_decimal(capital_value, "candidate.economics.capital_required_pln")
        if not isinstance(capital_value, bool) and isinstance(capital_value, (int, float))
        else positive_infinity
    )
    if capital < 0:
        capital = positive_infinity
    return (
        -as_decimal(evaluation["final_score"], "working final score"),
        -(economics if economics is not None else negative_infinity),
        -(distribution if distribution is not None else negative_infinity),
        capital,
        candidate["candidate_id"],
    )


def _ranked_stage_candidates(
    run_dir: Path, manifest: Mapping[str, Any], phase: str
) -> list[tuple[Path, dict[str, Any], dict[str, Any]]]:
    if phase == "development" and score_bracket_enabled(manifest["config"]):
        selection = (
            load_version_selection(run_dir, manifest)
            if (run_dir / "portfolio" / "version-selection.json").is_file()
            else build_version_selection(run_dir, manifest)
        )
        evaluations_by_sha = (
            {
                sha256_file(path): evaluation
                for path, evaluation in iter_evaluations(run_dir, manifest)
                if evaluation["evaluation_type"] == "working_development"
            }
            if not control_contract_enabled(manifest["config"])
            else {}
        )
        selected: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
        for row in selection["lineages"]:
            ref = row["selected_candidate_ref"]
            candidate_path = run_dir / candidate_relpath(
                ref["candidate_id"], ref["version"]
            )
            candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
            if control_contract_enabled(manifest["config"]):
                evaluation = {
                    "final_score": row["selected_conservative_score"]
                }
            else:
                evaluation = evaluations_by_sha.get(
                    row["selected_evaluation_sha256"]
                )
                if evaluation is None:
                    raise InputError(
                        "version selection references a missing development evaluation"
                    )
            selected.append((candidate_path, candidate, evaluation))
        return sorted(
            selected,
            key=lambda item: _working_rank_key(
                item[1], item[2], manifest["config"]
            ),
        )
    ranked: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
    coverage = working_evaluation_coverage(run_dir, manifest, phase)
    for record in coverage["records"]:
        candidate_path = run_dir / candidate_relpath(
            record["candidate_id"], record["candidate_version"]
        )
        candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
        evaluation_path = run_dir / record["evaluation_path"]
        evaluation = validate_canonical_evaluation(
            load_json(evaluation_path), manifest, run_dir
        )
        matching = [(evaluation_path, evaluation)]
        if len(matching) != 1:
            continue
        ranked.append((candidate_path, candidate, matching[0][1]))
    return sorted(
        ranked,
        key=lambda item: _working_rank_key(item[1], item[2], manifest["config"]),
    )


def validate_portfolio_decision(
    value: Any, manifest: Mapping[str, Any], run_dir: Path
) -> dict[str, Any]:
    decision = expect_object(value, "portfolio decision", exact_keys=PORTFOLIO_DECISION_KEYS)
    if expect_int(decision["schema_version"], "portfolio decision.schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError(
            f"portfolio decision.schema_version must be {ACTIVE_SCHEMA_VERSION}"
        )
    portfolio = effective_portfolio_selection(run_dir, manifest)
    selected_identities = {
        (item["candidate_id"], item["version"], item["candidate_sha256"])
        for item in portfolio["candidate_refs"]
    }
    researched_identities = {
        (item["candidate_id"], item["candidate_version"], item["candidate_sha256"])
        for _, item in iter_research(run_dir, manifest)
    }
    if researched_identities != selected_identities:
        raise InputError(
            "portfolio decision requires complete research of the exact effective shortlist"
        )
    _require_working_evaluation_coverage(run_dir, manifest, "research")
    research_rows = list(iter_research(run_dir, manifest))
    expected: dict[tuple[str, int], tuple[Path, dict[str, Any]]] = {}
    for _, research in research_rows:
        candidate_path = run_dir / candidate_relpath(
            research["candidate_id"], research["candidate_version"]
        )
        candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
        expected[(candidate["candidate_id"], candidate["version"])] = (
            candidate_path,
            candidate,
        )
    raw_decisions = decision["candidate_decisions"]
    if not isinstance(raw_decisions, list) or len(raw_decisions) != len(expected):
        raise InputError("portfolio decision must cover every latest researched candidate exactly once")
    canonical_rows: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    fatal_identities: set[tuple[str, int]] = set()
    disposition_by_identity: dict[tuple[str, int], str] = {}
    for index, raw in enumerate(raw_decisions):
        row = expect_object(raw, f"portfolio decision.candidate_decisions[{index}]", exact_keys=PORTFOLIO_CANDIDATE_DECISION_KEYS)
        candidate_id = expect_nonempty_string(row["candidate_id"], f"portfolio decision.candidate_decisions[{index}].candidate_id")
        version = expect_int(row["candidate_version"], f"portfolio decision.candidate_decisions[{index}].candidate_version", minimum=1)
        identity = (candidate_id, version)
        if identity in seen or identity not in expected:
            raise InputError("portfolio decision contains a duplicate or non-current candidate version")
        seen.add(identity)
        candidate_path, _ = expected[identity]
        if row["candidate_sha256"] != sha256_file(candidate_path):
            raise InputError("portfolio decision candidate_sha256 does not match the exact candidate version")
        if not isinstance(row["disposition"], str) or row["disposition"] not in {"develop", "not_selected", "fatal"}:
            raise InputError("portfolio decision disposition is invalid")
        rationale = expect_nonempty_string(row["rationale"], f"portfolio decision.candidate_decisions[{index}].rationale")
        claim_ids = expect_string_list(row["fatal_claim_ids"], f"portfolio decision.candidate_decisions[{index}].fatal_claim_ids", unique=True)
        if row["disposition"] == "fatal":
            if not isinstance(row["fatal_reason"], str) or row["fatal_reason"] not in FATAL_RESEARCH_REASONS:
                raise InputError("fatal research disposition requires a permitted direct-evidence fatal_reason")
            if not claim_ids:
                raise InputError("fatal research disposition requires evidence-backed fatal_claim_ids")
            research_path = run_dir / research_relpath(candidate_id, version)
            if not research_path.is_file():
                raise InputError("fatal research disposition requires canonical research")
            research = validate_research(load_json(research_path), manifest, run_dir)
            claims = {claim["claim_id"]: claim for claim in research["claims"]}
            for claim_id in claim_ids:
                claim = claims.get(claim_id)
                if claim is None or claim["assessment"] != "evidence" or not claim["evidence_refs"]:
                    raise InputError(
                        "unknown or inferential research cannot be labeled fatal; fatal claims require direct evidence"
                    )
            fatal_identities.add(identity)
        else:
            if row["fatal_reason"] is not None or claim_ids:
                raise InputError("non-fatal portfolio decision must use null fatal_reason and no fatal_claim_ids")
        disposition_by_identity[identity] = row["disposition"]
        canonical_row = dict(row)
        canonical_row["rationale"] = rationale.strip()
        canonical_rows.append(canonical_row)
    ranked_nonfatal = [
        item for item in _ranked_stage_candidates(run_dir, manifest, "research")
        if (item[1]["candidate_id"], item[1]["version"]) not in fatal_identities
    ]
    expected_develop = {
        (candidate["candidate_id"], candidate["version"])
        for _, candidate, _ in ranked_nonfatal[: manifest["config"]["develop_max"]]
    }
    actual_develop = {identity for identity, disposition in disposition_by_identity.items() if disposition == "develop"}
    if actual_develop != expected_develop:
        raise InputError("portfolio development selection must match deterministic working-score ranking")
    canonical = dict(decision)
    canonical["candidate_decisions"] = sorted(
        canonical_rows, key=lambda item: (item["candidate_id"], item["candidate_version"])
    )
    return canonical


def _load_portfolio_decision(run_dir: Path, manifest: Mapping[str, Any]) -> dict[str, Any]:
    path = run_dir / "portfolio" / "development-decision.json"
    if not path.is_file():
        raise InputError("canonical portfolio development decision is missing")
    decision = validate_portfolio_decision(load_json(path), manifest, run_dir)
    if path.read_bytes() != canonical_json_bytes(decision):
        raise InputError("portfolio development decision is not canonical")
    return decision


def canonicalize_development_response(
    value: Any, manifest: Mapping[str, Any], run_dir: Path
) -> dict[str, Any]:
    uses_control_contract = control_contract_enabled(manifest["config"])
    response = expect_object(
        value,
        "development response",
        exact_keys=DEVELOPMENT_RESPONSE_KEYS
        | ({DEVELOPMENT_CONTROL_KEY} if uses_control_contract else set()),
    )
    if expect_int(
        response["schema_version"], "development response.schema_version"
    ) != ACTIVE_SCHEMA_VERSION:
        raise InputError(
            f"development response.schema_version must be {ACTIVE_SCHEMA_VERSION}"
        )
    candidate_id = expect_nonempty_string(
        response["candidate_id"], "development response.candidate_id"
    )
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("development response.candidate_id must be a lowercase slug")
    if not isinstance(response["outcome"], str) or response["outcome"] not in {"redesigned", "no_valid_redesign"}:
        raise InputError(
            "development response.outcome must be redesigned or no_valid_redesign"
        )
    decision = _load_portfolio_decision(run_dir, manifest)
    admitted = [
        row
        for row in decision["candidate_decisions"]
        if row["candidate_id"] == candidate_id and row["disposition"] == "develop"
    ]
    if len(admitted) != 1:
        raise InputError("development response candidate is not admitted by the portfolio decision")
    base_path = run_dir / candidate_relpath(
        candidate_id, admitted[0]["candidate_version"]
    )
    base = validate_candidate(load_json(base_path), manifest, run_dir)
    redesigned = [
        (path, candidate)
        for path, candidate in iter_candidates(run_dir, manifest)
        if candidate["candidate_id"] == candidate_id
        and candidate["stage"] == "development"
    ]
    if response["outcome"] == "redesigned":
        if len(redesigned) != 1:
            raise InputError(
                "redesigned development response requires one canonical structural redesign"
            )
        final_path, final = redesigned[0]
    else:
        if redesigned:
            raise InputError(
                "no_valid_redesign response cannot follow a stored redesign candidate"
            )
        final_path, final = base_path, base
    canonical = {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "base_candidate_version": base["version"],
        "base_candidate_sha256": sha256_file(base_path),
        "outcome": response["outcome"],
        "final_candidate_version": final["version"],
        "final_candidate_sha256": sha256_file(final_path),
        "constructor_id": response["constructor_id"],
        "rationale": response["rationale"],
        "falsification": response["falsification"],
    }
    if uses_control_contract:
        canonical[DEVELOPMENT_CONTROL_KEY] = response[DEVELOPMENT_CONTROL_KEY]
    return validate_development_result(canonical, manifest, run_dir)


def validate_construction_change(
    value: Any,
    label: str,
    research: Mapping[str, Any],
    final_candidate: Mapping[str, Any],
) -> dict[str, Any]:
    change = expect_object(value, label, exact_keys=CONSTRUCTION_CHANGE_KEYS)
    canonical = dict(change)
    for key in sorted(
        CONSTRUCTION_CHANGE_KEYS - {"supporting_research_claim_ids"}
    ):
        if key == "resulting_control_point_status":
            canonical[key] = _validated_enum(
                change[key], f"{label}.{key}", CONTROL_POINT_STATUSES
            )
        elif key == "customer_relationship_control":
            canonical[key] = _validated_enum(
                change[key], f"{label}.{key}", CUSTOMER_RELATIONSHIP_CONTROLS
            )
        else:
            canonical[key] = expect_nonempty_string(change[key], f"{label}.{key}")
    claim_ids = expect_string_list(
        change["supporting_research_claim_ids"],
        f"{label}.supporting_research_claim_ids",
        unique=True,
    )
    if not claim_ids:
        raise InputError(f"{label}.supporting_research_claim_ids must not be empty")
    known_claims = {claim["claim_id"] for claim in research["claims"]}
    missing = sorted(set(claim_ids) - known_claims)
    if missing:
        raise InputError(
            f"{label}.supporting_research_claim_ids reference unknown claims: {missing}"
        )
    canonical["supporting_research_claim_ids"] = claim_ids
    control = final_candidate["critical_control_point"]
    mechanics = final_candidate["commercial_mechanics"]
    if canonical["resulting_control_point_status"] != control["status"]:
        raise InputError(
            f"{label}.resulting_control_point_status differs from the redesign candidate"
        )
    if normalize_fingerprint(canonical["customer_relationship_owner"]) != normalize_fingerprint(
        mechanics["customer_relationship_owner"]
    ):
        raise InputError(
            f"{label}.customer_relationship_owner differs from the redesign candidate"
        )
    if canonical["customer_relationship_control"] != control[
        "customer_relationship_control"
    ]:
        raise InputError(
            f"{label}.customer_relationship_control differs from the redesign candidate"
        )
    return canonical


def validate_development_result(
    value: Any, manifest: Mapping[str, Any], run_dir: Path
) -> dict[str, Any]:
    uses_control_contract = control_contract_enabled(manifest["config"])
    result = expect_object(
        value,
        "development result",
        exact_keys=DEVELOPMENT_RESULT_KEYS
        | ({DEVELOPMENT_CONTROL_KEY} if uses_control_contract else set()),
    )
    if expect_int(result["schema_version"], "development result.schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError(f"development result.schema_version must be {ACTIVE_SCHEMA_VERSION}")
    candidate_id = expect_nonempty_string(result["candidate_id"], "development result.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("development result.candidate_id must be a lowercase slug")
    constructor_id = expect_nonempty_string(result["constructor_id"], "development result.constructor_id")
    if not SAFE_JUDGE_RE.fullmatch(constructor_id):
        raise InputError("development result.constructor_id is not path-safe")
    expect_nonempty_string(result["rationale"], "development result.rationale")
    decision = _load_portfolio_decision(run_dir, manifest)
    admitted = [
        row
        for row in decision["candidate_decisions"]
        if row["candidate_id"] == candidate_id and row["disposition"] == "develop"
    ]
    if len(admitted) != 1:
        raise InputError("development result candidate is not admitted by the portfolio decision")
    admitted_row = admitted[0]
    base_path = run_dir / candidate_relpath(
        candidate_id, admitted_row["candidate_version"]
    )
    base = validate_candidate(load_json(base_path), manifest, run_dir)
    if base["stage"] != "discovery" or base["version"] != 1:
        raise InputError("development result base must be the immutable researched discovery candidate")
    if result["base_candidate_version"] != base["version"] or result["base_candidate_sha256"] != sha256_file(base_path):
        raise InputError("development result does not bind the exact base development version")
    redesigned = [
        (path, candidate)
        for path, candidate in iter_candidates(run_dir, manifest)
        if candidate["candidate_id"] == candidate_id and candidate["stage"] == "development"
    ]
    if result["outcome"] == "redesigned":
        if len(redesigned) != 1:
            raise InputError("redesigned development result requires one valid structural redesign version")
        final_path, final = redesigned[0]
        if (
            final["version"] != 2
            or final["parent"] != {"candidate_id": candidate_id, "version": 1}
            or "redesign" not in final
        ):
            raise InputError("redesigned development result requires the admitted direct child")
    elif result["outcome"] == "no_valid_redesign":
        if redesigned:
            raise InputError("no_valid_redesign must preserve the unmodified base development version")
        final_path, final = base_path, base
    else:
        raise InputError("development result.outcome must be redesigned or no_valid_redesign")
    if result["final_candidate_version"] != final["version"] or result["final_candidate_sha256"] != sha256_file(final_path):
        raise InputError("development result does not bind the exact final candidate version")
    research_path = run_dir / research_relpath(candidate_id, base["version"])
    if not research_path.is_file():
        raise InputError("development result requires canonical discovery research")
    research = validate_research(load_json(research_path), manifest, run_dir)
    canonical = dict(result)
    canonical["rationale"] = result["rationale"].strip()
    canonical["falsification"] = validate_falsification_map(
        result["falsification"],
        "development result.falsification",
        {claim["claim_id"] for claim in research["claims"]},
    )
    if uses_control_contract:
        if result["outcome"] == "redesigned":
            validate_development_control_resolution(
                final,
                research,
                label="final candidate",
            )
            canonical[DEVELOPMENT_CONTROL_KEY] = validate_construction_change(
                result[DEVELOPMENT_CONTROL_KEY],
                "development result.structural_change",
                research,
                final,
            )
        else:
            if result[DEVELOPMENT_CONTROL_KEY] is not None:
                raise InputError(
                    "no_valid_redesign must use a null structural_change"
                )
            canonical[DEVELOPMENT_CONTROL_KEY] = None
    return canonical


def _development_result_for_candidate(
    run_dir: Path, manifest: Mapping[str, Any], candidate_id: str
) -> tuple[Path, dict[str, Any]]:
    path = run_dir / "development" / candidate_id / "constructor-result.json"
    if not path.is_file():
        raise InputError(f"development result is missing for {candidate_id}")
    result = validate_development_result(load_json(path), manifest, run_dir)
    if path.read_bytes() != canonical_json_bytes(result):
        raise InputError(f"development result is not canonical for {candidate_id}")
    return path, result


def build_version_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    if not score_bracket_enabled(manifest["config"]):
        raise ConflictError("this run does not use score-based version selection")
    coverage = _require_working_evaluation_coverage(run_dir, manifest, "development")
    records_by_identity: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for record in coverage["records"]:
        records_by_identity.setdefault(
            (record["candidate_id"], record["candidate_version"]), []
        ).append(record)
    decision = _load_portfolio_decision(run_dir, manifest)
    rows: list[dict[str, Any]] = []
    for decision_row in decision["candidate_decisions"]:
        if decision_row["disposition"] != "develop":
            continue
        candidate_id = decision_row["candidate_id"]
        _, result = _development_result_for_candidate(run_dir, manifest, candidate_id)
        base_path = run_dir / candidate_relpath(
            candidate_id, result["base_candidate_version"]
        )
        base = validate_candidate(load_json(base_path), manifest, run_dir)
        base_records = records_by_identity[(candidate_id, base["version"])]
        base_ref = {
            "candidate_id": candidate_id,
            "version": base["version"],
            "candidate_sha256": sha256_file(base_path),
        }
        redesign_ref: dict[str, Any] | None = None
        redesign_records: list[dict[str, Any]] | None = None
        selected_ref = base_ref
        reason = "no_valid_redesign"
        if control_contract_enabled(manifest["config"]):
            base_conservative = min(
                as_decimal(record["final_score"], "base development score")
                for record in base_records
            )
        else:
            base_record = base_records[0]
        if result["outcome"] == "redesigned":
            redesign_path = run_dir / candidate_relpath(
                candidate_id, result["final_candidate_version"]
            )
            redesign = validate_candidate(load_json(redesign_path), manifest, run_dir)
            redesign_records = records_by_identity[
                (candidate_id, redesign["version"])
            ]
            redesign_ref = {
                "candidate_id": candidate_id,
                "version": redesign["version"],
                "candidate_sha256": sha256_file(redesign_path),
            }
            redesign_score = (
                min(
                    as_decimal(
                        record["final_score"], "redesign development score"
                    )
                    for record in redesign_records
                )
                if control_contract_enabled(manifest["config"])
                else as_decimal(
                    redesign_records[0]["final_score"],
                    "redesign development score",
                )
            )
            base_score = (
                base_conservative
                if control_contract_enabled(manifest["config"])
                else as_decimal(
                    base_record["final_score"], "base development score"
                )
            )
            if redesign_score > base_score:
                selected_ref = redesign_ref
                reason = "redesign_score_strictly_higher"
            else:
                reason = "redesign_score_equal_or_lower"
        if control_contract_enabled(manifest["config"]):
            base_inputs = [
                {
                    "path": record["evaluation_path"],
                    "sha256": record["evaluation_sha256"],
                    "judge_id": record["judge_id"],
                    "final_score": record["final_score"],
                }
                for record in sorted(
                    base_records, key=lambda item: item["judge_id"]
                )
            ]
            redesign_inputs = (
                None
                if redesign_records is None
                else [
                    {
                        "path": record["evaluation_path"],
                        "sha256": record["evaluation_sha256"],
                        "judge_id": record["judge_id"],
                        "final_score": record["final_score"],
                    }
                    for record in sorted(
                        redesign_records, key=lambda item: item["judge_id"]
                    )
                ]
            )
            redesign_conservative = (
                None
                if redesign_records is None
                else min(
                    as_decimal(
                        record["final_score"], "redesign development score"
                    )
                    for record in redesign_records
                )
            )
            selected_conservative = (
                redesign_conservative
                if selected_ref is redesign_ref
                else base_conservative
            )
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "base_candidate_ref": base_ref,
                    "redesign_candidate_ref": redesign_ref,
                    "base_evaluations": base_inputs,
                    "redesign_evaluations": redesign_inputs,
                    "base_conservative_score": decimal_json(
                        base_conservative, quantum=FINAL_QUANTUM
                    ),
                    "redesign_conservative_score": (
                        None
                        if redesign_conservative is None
                        else decimal_json(
                            redesign_conservative, quantum=FINAL_QUANTUM
                        )
                    ),
                    "selected_candidate_ref": selected_ref,
                    "selected_conservative_score": decimal_json(
                        selected_conservative, quantum=FINAL_QUANTUM
                    ),
                    "selection_reason": reason,
                }
            )
        else:
            redesign_record = (
                None if redesign_records is None else redesign_records[0]
            )
            selected_record = (
                redesign_record if selected_ref is redesign_ref else base_record
            )
            rows.append({
                "candidate_id": candidate_id,
                "base_candidate_ref": base_ref,
                "redesign_candidate_ref": redesign_ref,
                "base_evaluation_sha256": base_record["evaluation_sha256"],
                "redesign_evaluation_sha256": (
                    None
                    if redesign_record is None
                    else redesign_record["evaluation_sha256"]
                ),
                "selected_candidate_ref": selected_ref,
                "selected_evaluation_sha256": selected_record["evaluation_sha256"],
                "selection_reason": reason,
            })
    return {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "lineages": sorted(rows, key=lambda item: item["candidate_id"]),
    }


def load_version_selection(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    path = run_dir / "portfolio" / "version-selection.json"
    if not path.is_file():
        raise InputError("canonical development version selection is missing")
    value = expect_object(
        load_json(path), "version selection", exact_keys=VERSION_SELECTION_KEYS
    )
    if value.get("schema_version") != ACTIVE_SCHEMA_VERSION:
        raise InputError("version selection schema_version differs from the workflow")
    lineages = value.get("lineages")
    if not isinstance(lineages, list):
        raise InputError("version selection.lineages must be a list")
    for index, row in enumerate(lineages):
        expect_object(
            row,
            f"version selection.lineages[{index}]",
            exact_keys=(
                VERSION_SELECTION_CONTROL_ROW_KEYS
                if control_contract_enabled(manifest["config"])
                else VERSION_SELECTION_ROW_KEYS
            ),
        )
        if control_contract_enabled(manifest["config"]):
            for field in ("base_evaluations", "redesign_evaluations"):
                values = row[field]
                if values is None:
                    if field == "base_evaluations":
                        raise InputError(
                            "version selection base_evaluations cannot be null"
                        )
                    continue
                if not isinstance(values, list):
                    raise InputError(
                        f"version selection {field} must be a list or null"
                    )
                for input_index, item in enumerate(values):
                    expect_object(
                        item,
                        f"version selection {field}[{input_index}]",
                        exact_keys=DEVELOPMENT_AGGREGATION_INPUT_KEYS,
                    )
    expected = build_version_selection(run_dir, manifest)
    if value != expected or path.read_bytes() != canonical_json_bytes(expected):
        raise InputError(
            "version selection differs from deterministic paired-score comparison"
        )
    return expected


def _factor_score(evaluation: Mapping[str, Any], factor_name: str) -> Decimal | None:
    for factor in evaluation["factors"]:
        if factor["name"] == factor_name:
            if factor["status"] == "excluded":
                return None
            return as_decimal(factor["score"], f"{factor_name} score")
    raise InputError(f"evaluation is missing tie-break factor: {factor_name}")


def _numeric_capital(candidate: Mapping[str, Any]) -> Decimal | None:
    value = candidate["economics"]["capital_required_pln"]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError("frozen candidate capital_required_pln must be numeric")
    capital = as_decimal(value, "candidate.economics.capital_required_pln")
    if capital < 0:
        raise InputError("frozen candidate capital_required_pln must be nonnegative")
    return capital


def _selection_key(item: Mapping[str, Any]) -> tuple[Decimal, Decimal, Decimal, Decimal, str]:
    negative_infinity = Decimal("-Infinity")
    positive_infinity = Decimal("Infinity")
    economics = (
        as_decimal(item["native_economics_floor"], "native economics floor")
        if item["native_economics_floor"] is not None
        else negative_infinity
    )
    distribution = (
        as_decimal(item["native_distribution_floor"], "native distribution floor")
        if item["native_distribution_floor"] is not None
        else negative_infinity
    )
    capital = (
        as_decimal(item["capital_required_pln_numeric"], "capital required")
        if item["capital_required_pln_numeric"] is not None
        else positive_infinity
    )
    return (
        -as_decimal(item["official_native_score"], "official native score"),
        -economics,
        -distribution,
        capital,
        item["candidate_id"],
    )


def _failed_job_summaries(state: Mapping[str, Any]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for stage in STAGES:
        for job_id, job in sorted(state["jobs"][stage].items()):
            if job["status"] not in {"failed", "interrupted"}:
                continue
            summaries.append(
                {
                    "stage": stage,
                    "job_id": job_id,
                    "status": job["status"],
                    "attempts": job["attempts"],
                    "max_attempts": job["max_attempts"],
                    "retryable": job_is_retryable(job),
                    "error": job["error"],
                }
            )
    return summaries


def _evaluation_coverage_report(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any]:
    if not score_bracket_enabled(manifest["config"]):
        research = working_evaluation_coverage(run_dir, manifest, "research")
        development = working_evaluation_coverage(run_dir, manifest, "development")
        records = [*research["records"], *development["records"]]
        highest = max(
            (
                as_decimal(item["final_score"], "working final score")
                for item in records
            ),
            default=None,
        )
        return {
            "research": research,
            "development": development,
            "total_candidate_versions": research["candidate_count"]
            + development["candidate_count"],
            "total_completed": research["completed_count"]
            + development["completed_count"],
            "complete": research["complete"] and development["complete"],
            "highest_working_score": (
                None
                if highest is None
                else decimal_json(highest, quantum=FINAL_QUANTUM)
            ),
        }
    screening = (
        working_evaluation_coverage(run_dir, manifest, "screening")
        if score_bracket_enabled(manifest["config"])
        and (run_dir / "portfolio" / "screening-batches.json").is_file()
        else {
            "candidate_count": 0,
            "required_evaluation_count": 0,
            "completed_count": 0,
            "complete": True,
            "missing": [],
            "duplicates": [],
            "judge_conflicts": [],
            "batches": [],
            "records": [],
        }
    )
    secondary_screening = (
        working_evaluation_coverage(
            run_dir, manifest, "screening_secondary"
        )
        if control_contract_enabled(manifest["config"])
        and (run_dir / "portfolio" / "secondary-screening.json").is_file()
        else {
            "candidate_count": 0,
            "required_evaluation_count": 0,
            "completed_count": 0,
            "complete": True,
            "missing": [],
            "duplicates": [],
            "judge_conflicts": [],
            "batches": [],
            "records": [],
        }
    )
    research = working_evaluation_coverage(run_dir, manifest, "research")
    development = working_evaluation_coverage(run_dir, manifest, "development")
    scored_stage_records = [*research["records"], *development["records"]]
    highest = max(
        (
            as_decimal(item["final_score"], "working final score")
            for item in scored_stage_records
        ),
        default=None,
    )
    return {
        "screening": screening,
        **(
            {"secondary_screening": secondary_screening}
            if control_contract_enabled(manifest["config"])
            else {}
        ),
        "research": research,
        "development": development,
        "total_candidate_versions": (
            screening["candidate_count"]
            + secondary_screening["candidate_count"]
            + research["candidate_count"]
            + development["candidate_count"]
        ),
        "total_completed": (
            screening["completed_count"]
            + secondary_screening["completed_count"]
            + research["completed_count"]
            + development["completed_count"]
        ),
        "complete": screening["complete"]
        and secondary_screening["complete"]
        and research["complete"]
        and development["complete"],
        "highest_working_score": None if highest is None else decimal_json(highest, quantum=FINAL_QUANTUM),
    }


def _portfolio_report(
    run_dir: Path, manifest: Mapping[str, Any]
) -> dict[str, Any] | None:
    portfolio = effective_portfolio_selection(run_dir, manifest)
    selection_path = run_dir / portfolio["selection_path"]
    selection = validate_portfolio_selection(load_json(selection_path), manifest, run_dir)
    amendment_artifacts = [
        {
            "path": f"portfolio/amendments/v{item['amendment_version']}.json",
            "sha256": sha256_file(run_dir / f"portfolio/amendments/v{item['amendment_version']}.json"),
        }
        for item in portfolio["amendments"]
    ]
    decision_path = run_dir / "portfolio" / "development-decision.json"
    decision_artifact = None
    decisions: list[dict[str, Any]] = []
    if decision_path.is_file():
        decision = _load_portfolio_decision(run_dir, manifest)
        decision_artifact = {
            "path": "portfolio/development-decision.json",
            "sha256": sha256_file(decision_path),
        }
        decisions = decision["candidate_decisions"]
    wildcard_identities = {
        (item["candidate_id"], item["version"], item["candidate_sha256"])
        for item in portfolio["wildcard_candidate_refs"]
    }
    shortlist_slots: list[dict[str, Any]] = []
    for reference in portfolio["candidate_refs"]:
        _, _, candidate = _candidate_reference(
            reference, manifest, run_dir, "portfolio report candidate"
        )
        identity = (
            reference["candidate_id"],
            reference["version"],
            reference["candidate_sha256"],
        )
        shortlist_slots.append(
            {
                "candidate_ref": reference,
                "slot_type": (
                    "score_selected"
                    if score_bracket_enabled(manifest["config"])
                    else "wildcard" if identity in wildcard_identities else "core"
                ),
                "discovery_lane": candidate["discovery_lane"],
                **(
                    {
                        "structural_signature": candidate[
                            "structural_signature"
                        ],
                        "critical_control_point_status": candidate[
                            "critical_control_point"
                        ]["status"],
                        "customer_relationship_control": candidate[
                            "critical_control_point"
                        ]["customer_relationship_control"],
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
        )
    result = {
        "selection_artifact": {
            "path": portfolio["selection_path"],
            "sha256": sha256_file(selection_path),
        },
        "amendment_artifacts": amendment_artifacts,
        "development_decision_artifact": decision_artifact,
        "missing_archetypes": selection["missing_archetypes"],
        "calibration": portfolio["calibration"],
        "shortlist_slots": shortlist_slots,
        "finalist_selection_artifact": (
            {
                "path": "portfolio/finalists.json",
                "sha256": sha256_file(run_dir / "portfolio" / "finalists.json"),
            }
            if (run_dir / "portfolio" / "finalists.json").is_file()
            else None
        ),
        "candidate_decisions": decisions,
    }
    if score_bracket_enabled(manifest["config"]):
        dedup_path = run_dir / "dedup" / "report.json"
        screening_path = run_dir / "portfolio" / "screening-batches.json"
        version_path = run_dir / "portfolio" / "version-selection.json"
        result.update(
            {
                "dedup_artifact": {
                    "path": "dedup/report.json",
                    "sha256": sha256_file(dedup_path),
                },
                "screening_batches_artifact": (
                    {
                        "path": "portfolio/screening-batches.json",
                        "sha256": sha256_file(screening_path),
                    }
                    if screening_path.is_file()
                    else None
                ),
                "version_selection_artifact": (
                    {
                        "path": "portfolio/version-selection.json",
                        "sha256": sha256_file(version_path),
                    }
                    if version_path.is_file()
                    else None
                ),
                "version_selection": (
                    load_version_selection(run_dir, manifest)["lineages"]
                    if version_path.is_file()
                    else []
                ),
            }
        )
    if control_contract_enabled(manifest["config"]):
        dedup = load_json(run_dir / "dedup" / "report.json")
        research_contracts: list[dict[str, Any]] = []
        decision_by_id = {
            row["candidate_id"]: row
            for row in decisions
        }
        selected_versions = {
            row["candidate_id"]: row["selected_candidate_ref"]["version"]
            for row in result.get("version_selection", [])
        }
        for _, research in iter_research(run_dir, manifest):
            candidate_path = run_dir / candidate_relpath(
                research["candidate_id"], research["candidate_version"]
            )
            candidate = validate_candidate(
                load_json(candidate_path), manifest, run_dir
            )
            final_status = research["critical_control_point_assessment"]["status"]
            decision_row = decision_by_id.get(research["candidate_id"])
            if decision_row is not None and decision_row["disposition"] == "develop":
                result_path = (
                    run_dir
                    / "development"
                    / research["candidate_id"]
                    / "constructor-result.json"
                )
                if result_path.is_file():
                    _, construction = _development_result_for_candidate(
                        run_dir, manifest, research["candidate_id"]
                    )
                    if construction["outcome"] == "redesigned" and (
                        not score_bracket_enabled(manifest["config"])
                        or selected_versions.get(research["candidate_id"]) == 2
                    ):
                        final_status = construction[DEVELOPMENT_CONTROL_KEY][
                            "resulting_control_point_status"
                        ]
            research_contracts.append(
                {
                    "candidate_id": research["candidate_id"],
                    "candidate_version": research["candidate_version"],
                    "claimed_control_point_status": candidate[
                        "critical_control_point"
                    ]["status"],
                    "researched_control_point_status": research[
                        "critical_control_point_assessment"
                    ]["status"],
                    "final_control_point_status": final_status,
                    "commercial_evidence": {
                        key: {
                            "status": research["commercial_evidence"][key][
                                "status"
                            ],
                            "claim_count": len(
                                research["commercial_evidence"][key]["claim_ids"]
                            ),
                            "source_count": len(
                                research["commercial_evidence"][key]["source_ids"]
                            ),
                        }
                        for key in sorted(COMMERCIAL_EVIDENCE_KEYS)
                    },
                }
            )
        result.update(
            {
                "semantic_variety": {
                    "discovery_signature_unique_count": dedup[
                        "semantic_signature_unique_count"
                    ],
                    "discovery_semantic_collision_count": len(
                        dedup["semantic_collision_groups"]
                    ),
                    "shortlist_signature_unique_count": len(
                        {
                            structural_signature_key(
                                _candidate_reference(
                                    ref,
                                    manifest,
                                    run_dir,
                                    "portfolio semantic variety",
                                )[2]
                            )
                            for ref in portfolio["candidate_refs"]
                        }
                    ),
                },
                "research_contracts": sorted(
                    research_contracts,
                    key=lambda item: item["candidate_id"],
                ),
                "secondary_screening_artifact": (
                    {
                        "path": "portfolio/secondary-screening.json",
                        "sha256": sha256_file(
                            run_dir / "portfolio" / "secondary-screening.json"
                        ),
                    }
                    if (run_dir / "portfolio" / "secondary-screening.json").is_file()
                    else None
                ),
                "screening_aggregation_artifact": (
                    {
                        "path": "portfolio/screening-aggregation.json",
                        "sha256": sha256_file(
                            run_dir / "portfolio" / "screening-aggregation.json"
                        ),
                    }
                    if (run_dir / "portfolio" / "screening-aggregation.json").is_file()
                    else None
                ),
            }
        )
    return result


def build_final_report(run_dir: Path, manifest: Mapping[str, Any], state: Mapping[str, Any]) -> dict[str, Any]:
    _validate_stage_gate(run_dir, manifest, {**state, "stage": "development"})
    frozen = finalist_candidates(run_dir, manifest)
    if not frozen:
        raise InputError("finalize requires at least one frozen finalist reference")
    validate_external_imports(run_dir, manifest)
    evaluations = list(iter_evaluations(run_dir, manifest))
    working_judge_ids = {
        evaluation["judge_id"]
        for _, evaluation in evaluations
        if evaluation["evaluation_type"].startswith("working_")
    }
    constructor_ids: set[str] = set()
    for _, candidate in frozen:
        _, result = _development_result_for_candidate(run_dir, manifest, candidate["candidate_id"])
        constructor_ids.add(result["constructor_id"])
    native_judges_seen: set[str] = set()
    threshold = as_decimal(manifest["config"]["threshold"], "config.threshold")
    results: list[dict[str, Any]] = []
    for candidate_path, candidate in sorted(frozen, key=lambda item: item[1]["candidate_id"]):
        _external_identity(run_dir, manifest, candidate["candidate_id"])
        digest = sha256_file(candidate_path)
        matching = [
            (path, evaluation)
            for path, evaluation in evaluations
            if evaluation["candidate_id"] == candidate["candidate_id"]
            and evaluation["candidate_version"] == candidate["version"]
            and evaluation["candidate_sha256"] == digest
        ]
        native = [(path, item) for path, item in matching if item["evaluation_type"] == "holdout_native"]
        external = [(path, item) for path, item in matching if item["evaluation_type"] == "holdout_external"]
        expected_native = manifest["config"]["native_holdout_judges"]
        if len(native) != expected_native:
            raise InputError(
                f"candidate {candidate['candidate_id']} requires exactly {expected_native} native holdout evaluations; found {len(native)}"
            )
        if len({item["judge_id"] for _, item in native}) != len(native):
            raise InputError(f"candidate {candidate['candidate_id']} has duplicate native judge ids")
        native_judge_ids = {item["judge_id"] for _, item in native}
        reused_roles = sorted(native_judge_ids & (working_judge_ids | constructor_ids))
        if reused_roles:
            raise InputError(
                f"native holdout judges must be fresh and role-independent: {', '.join(reused_roles)}"
            )
        reused_finalists = sorted(native_judge_ids & native_judges_seen)
        if reused_finalists:
            raise InputError(
                f"native holdout judge identities must not be reused across finalists: {', '.join(reused_finalists)}"
            )
        native_judges_seen.update(native_judge_ids)
        native_scores = [as_decimal(item["final_score"], "native final_score") for _, item in native]
        economics_scores = [_factor_score(item, "Business model and economics") for _, item in native]
        distribution_scores = [_factor_score(item, "Distribution") for _, item in native]
        economics_floor = min(score for score in economics_scores if score is not None) if all(
            score is not None for score in economics_scores
        ) else None
        distribution_floor = min(score for score in distribution_scores if score is not None) if all(
            score is not None for score in distribution_scores
        ) else None
        numeric_capital = _numeric_capital(candidate)
        native_official = min(native_scores)
        native_pass = native_official > threshold
        external_scores = [as_decimal(item["final_score"], "external final_score") for _, item in external]
        external_pass = all(score > threshold for score in external_scores)
        qualified = native_pass and external_pass
        contested = native_pass and not external_pass
        binding_scores = native_scores + external_scores
        binding_floor = min(binding_scores)
        holdout_matching = [
            (path, item)
            for path, item in matching
            if item["evaluation_type"] in {"holdout_native", "holdout_external"}
        ]
        diagnostics = [
            {
                "evaluation_type": item["evaluation_type"],
                "judge_id": item["judge_id"],
                "final_score": item["final_score"],
                "main_structural_strength": item["main_structural_strength"],
                "primary_score_limiter": item["primary_score_limiter"],
                "strongest_disconfirming_evidence": item["strongest_disconfirming_evidence"],
                "highest_value_structural_change": item["highest_value_structural_change"],
                "evidence_needed_for_higher_score": item["evidence_needed_for_higher_score"],
            }
            for _, item in sorted(holdout_matching, key=lambda pair: pair[0].as_posix())
        ]
        binding_diagnostics = [
            diagnostic
            for diagnostic in diagnostics
            if as_decimal(diagnostic["final_score"], "diagnostic final score") == binding_floor
        ]
        control_report: dict[str, Any] = {}
        if control_contract_enabled(manifest["config"]):
            research = lineage_research_records(
                run_dir, manifest, candidate
            )[0][1]
            control_report = {
                "critical_control_point_status": candidate[
                    "critical_control_point"
                ]["status"],
                "researched_control_point_status": research[
                    "critical_control_point_assessment"
                ]["status"],
                "customer_relationship_control": candidate[
                    "critical_control_point"
                ]["customer_relationship_control"],
                "structural_signature": candidate["structural_signature"],
            }
        results.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate_version": candidate["version"],
                "title": candidate["title"],
                "candidate_artifact": candidate_path.relative_to(run_dir).as_posix(),
                "candidate_sha256": digest,
                "native_scores": [decimal_json(score, quantum=FINAL_QUANTUM) for score in native_scores],
                "official_native_score": decimal_json(native_official, quantum=FINAL_QUANTUM),
                "external_scores": [decimal_json(score, quantum=FINAL_QUANTUM) for score in external_scores],
                "binding_score_floor": decimal_json(binding_floor, quantum=FINAL_QUANTUM),
                "native_economics_floor": None if economics_floor is None else decimal_json(economics_floor),
                "native_distribution_floor": None if distribution_floor is None else decimal_json(distribution_floor),
                "capital_required_pln_numeric": None if numeric_capital is None else decimal_json(numeric_capital),
                "qualified": qualified,
                "contested": contested,
                "binding_limiters": sorted(
                    {diagnostic["primary_score_limiter"] for diagnostic in binding_diagnostics}
                ),
                "evaluation_diagnostics": diagnostics,
                "evaluation_artifacts": [
                    {
                        "path": path.relative_to(run_dir).as_posix(),
                        "sha256": sha256_file(path),
                        "evaluation_type": item["evaluation_type"],
                        "judge_id": item["judge_id"],
                    }
                    for path, item in sorted(matching, key=lambda pair: pair[0].as_posix())
                    if item["evaluation_type"] in {"holdout_native", "holdout_external"}
                ],
                **control_report,
            }
        )
    qualified_results = [item for item in results if item["qualified"]]
    contested_results = [item for item in results if item["contested"]]
    if qualified_results:
        run_status = "qualified"
        selected = min(qualified_results, key=_selection_key)
    elif contested_results:
        run_status = "contested"
        selected = min(contested_results, key=_selection_key)
    else:
        run_status = "no_qualifier"
        selected = min(results, key=_selection_key)
    evaluation_coverage = _evaluation_coverage_report(run_dir, manifest)
    return {
        "schema_version": manifest["config"]["schema_version"],
        "run_id": state["run_id"],
        "campaign": manifest.get("campaign"),
        "founder_sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        "rubric_id": manifest["rubric"]["rubric_id"],
        "rubric_sha256": manifest["rubric"]["sha256"],
        "threshold": manifest["config"]["threshold"],
        "comparison": "strictly_greater_than",
        "run_status": run_status,
        "terminal_stage": "holdout",
        "qualification_label": QUALIFICATION_LABEL if run_status == "qualified" else None,
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_version": selected["candidate_version"],
        "official_score": selected["official_native_score"],
        "binding_score_floor": selected["binding_score_floor"],
        "no_finalist_reason": None,
        "highest_working_score": evaluation_coverage["highest_working_score"],
        "working_evaluation_coverage": evaluation_coverage,
        "portfolio_decision": _portfolio_report(run_dir, manifest),
        "binding_limiters": selected["binding_limiters"],
        "unresolved_evidence": sorted(
            {
                diagnostic["evidence_needed_for_higher_score"]
                for diagnostic in selected["evaluation_diagnostics"]
            }
        ),
        "strongest_candidates": [
            {
                "candidate_id": item["candidate_id"],
                "candidate_version": item["candidate_version"],
                "title": item["title"],
                "official_native_score": item["official_native_score"],
                "binding_score_floor": item["binding_score_floor"],
                "qualified": item["qualified"],
                "contested": item["contested"],
                "binding_limiters": item["binding_limiters"],
                **(
                    {
                        "critical_control_point_status": item[
                            "critical_control_point_status"
                        ],
                        "researched_control_point_status": item[
                            "researched_control_point_status"
                        ],
                        "customer_relationship_control": item[
                            "customer_relationship_control"
                        ],
                        "structural_signature": item[
                            "structural_signature"
                        ],
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
            for item in sorted(results, key=_selection_key)
        ],
        "failed_jobs": _failed_job_summaries(state),
        "candidates": results,
    }


def build_early_no_qualifier_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    reason: str,
    best_candidate_id: str | None = None,
) -> dict[str, Any]:
    return build_no_finalist_report(
        run_dir, manifest, state, reason, best_candidate_id
    )


def build_no_finalist_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    reason: str,
    best_candidate_id: str | None = None,
) -> dict[str, Any]:
    reason = expect_nonempty_string(reason, "no_finalist reason")
    coverage = _evaluation_coverage_report(run_dir, manifest)
    ranked_stage = "development" if coverage["development"]["candidate_count"] else "research"
    ranked = _ranked_stage_candidates(run_dir, manifest, ranked_stage)
    score_by_id = {
        item["candidate_id"]: item
        for item in coverage[ranked_stage]["records"]
    }
    preserved: list[tuple[Path, dict[str, Any]]] = []
    decision_path = run_dir / "portfolio" / "development-decision.json"
    if decision_path.is_file():
        decision = _load_portfolio_decision(run_dir, manifest)
        for row in decision["candidate_decisions"]:
            if row["disposition"] != "develop":
                continue
            result_path = run_dir / "development" / row["candidate_id"] / "constructor-result.json"
            if result_path.is_file():
                _, result = _development_result_for_candidate(run_dir, manifest, row["candidate_id"])
                path = run_dir / candidate_relpath(
                    row["candidate_id"], result["final_candidate_version"]
                )
                preserved.append((path, validate_candidate(load_json(path), manifest, run_dir)))
    if not preserved:
        for _, research in iter_research(run_dir, manifest):
            path = run_dir / candidate_relpath(
                research["candidate_id"], research["candidate_version"]
            )
            preserved.append((path, validate_candidate(load_json(path), manifest, run_dir)))
    preserved_by_id = {candidate["candidate_id"]: (path, candidate) for path, candidate in preserved}
    ranked_preserved_ids = [
        candidate["candidate_id"]
        for _, candidate, _ in ranked
        if candidate["candidate_id"] in preserved_by_id
    ]
    selected_id = ranked_preserved_ids[0] if ranked_preserved_ids else None
    if best_candidate_id is not None:
        requested = expect_nonempty_string(best_candidate_id, "--best-candidate")
        if requested != selected_id:
            raise InputError("--best-candidate must match the deterministic highest working-score candidate")
    selected_pair = preserved_by_id.get(selected_id) if selected_id is not None else None
    selected_version = selected_pair[1]["version"] if selected_pair is not None else None
    selected_score = score_by_id.get(selected_id) if selected_id is not None else None
    selected_candidate = selected_pair[1] if selected_pair is not None else None
    selected_unresolved = (
        sorted(set([*selected_candidate["uncertainties"], *selected_candidate["contrary_evidence"]]))
        if selected_candidate is not None
        else []
    )
    reopen_condition = (
        "Reopen only with new evidence that materially resolves: " + "; ".join(selected_unresolved)
        if selected_unresolved
        else f"Reopen only with new evidence that materially resolves the closure reason: {reason}"
    )
    ordered_ids = [*ranked_preserved_ids, *sorted(set(preserved_by_id) - set(ranked_preserved_ids))]
    strongest_candidates: list[dict[str, Any]] = []
    for candidate_id in ordered_ids:
        path, candidate = preserved_by_id[candidate_id]
        working = score_by_id.get(candidate_id)
        control_summary: dict[str, Any] = {}
        if control_contract_enabled(manifest["config"]):
            base_research_path = run_dir / research_relpath(candidate_id, 1)
            researched_status = (
                validate_research(
                    load_json(base_research_path), manifest, run_dir
                )["critical_control_point_assessment"]["status"]
                if base_research_path.is_file()
                else "unknown"
            )
            control_summary = {
                "critical_control_point_status": candidate[
                    "critical_control_point"
                ]["status"],
                "researched_control_point_status": researched_status,
                "customer_relationship_control": candidate[
                    "critical_control_point"
                ]["customer_relationship_control"],
                "structural_signature": candidate["structural_signature"],
            }
        strongest_candidates.append(
            {
                "candidate_id": candidate_id,
                "candidate_version": candidate["version"],
                "title": candidate["title"],
                "stage": candidate["stage"],
                "artifact": path.relative_to(run_dir).as_posix(),
                "artifact_sha256": sha256_file(path),
                "working_score": working["final_score"] if working else None,
                "working_evaluation_artifact": working["evaluation_path"] if working else None,
                "primary_score_limiter": working["primary_score_limiter"] if working else None,
                "strongest_disconfirming_evidence": (
                    working["strongest_disconfirming_evidence"] if working else None
                ),
                "risks": candidate["risks"],
                "uncertainties": candidate["uncertainties"],
                "contrary_evidence": candidate["contrary_evidence"],
                "is_selected": candidate_id == selected_id,
                "primary_limiter": reason if candidate_id == selected_id else None,
                "reopen_condition": reopen_condition if candidate_id == selected_id else None,
                **control_summary,
            }
        )
    binding_limiters = [reason]
    if selected_score and selected_score["primary_score_limiter"] not in binding_limiters:
        binding_limiters.append(selected_score["primary_score_limiter"])
    return {
        "schema_version": ACTIVE_SCHEMA_VERSION,
        "run_id": state["run_id"],
        "campaign": manifest.get("campaign"),
        "founder_sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        "rubric_id": manifest["rubric"]["rubric_id"],
        "rubric_sha256": manifest["rubric"]["sha256"],
        "threshold": manifest["config"]["threshold"],
        "comparison": "strictly_greater_than",
        "run_status": "no_finalist",
        "terminal_stage": state["stage"],
        "qualification_label": None,
        "selected_candidate_id": selected_id,
        "selected_candidate_version": selected_version,
        "official_score": None,
        "binding_score_floor": None,
        "highest_working_score": coverage["highest_working_score"],
        "working_evaluation_coverage": coverage,
        "portfolio_decision": _portfolio_report(run_dir, manifest),
        "no_finalist_reason": reason,
        "binding_limiters": binding_limiters,
        "strongest_candidates": strongest_candidates,
        "unresolved_evidence": selected_unresolved,
        "failed_jobs": _failed_job_summaries(state),
        "candidates": [],
    }


def render_report_markdown(
    report: Mapping[str, Any], *, legacy_coverage_label: bool = False,
) -> str:
    lines = [
        "# Opportunity Workflow Outcome",
        "",
        f"- Run: `{report['run_id']}`",
        f"- Status: `{report['run_status']}`",
        *( [f"- Terminal stage: `{report['terminal_stage']}`"] if report.get("terminal_stage") else [] ),
        f"- Rubric: `{report['rubric_id']}`",
        f"- Gate: final score `{report['comparison']}` `{report['threshold']}`",
    ]
    if report.get("qualification_label"):
        lines.append(f"- Qualification: {report['qualification_label']}")
    if report.get("selected_candidate_id") is not None:
        label = "Best preserved candidate" if report.get("official_score") is None else "Selected candidate"
        lines.append(
            f"- {label}: `{report['selected_candidate_id']}` v{report['selected_candidate_version']}"
        )
        if report.get("official_score") is not None:
            lines.extend(
                [
                    f"- Official native score: `{report['official_score']}`",
                    f"- Binding score floor: `{report['binding_score_floor']}`",
                ]
            )
    closure_reason = report.get("no_finalist_reason", report.get("no_qualifier_reason"))
    if closure_reason:
        lines.append(f"- Closure reason: {closure_reason}")
    if "highest_working_score" in report:
        value = report.get("highest_working_score")
        lines.append(f"- Highest working score: `{value if value is not None else 'N/A'}`")
        coverage = report.get("working_evaluation_coverage", {})
        if legacy_coverage_label:
            lines.append(
                f"- Working evaluation coverage: `{coverage.get('total_completed', 0)}/"
                f"{coverage.get('total_candidate_versions', 0)}` candidate versions"
            )
        else:
            lines.append(
                f"- Working evaluations: `{coverage.get('total_completed', 0)}` judgments across "
                f"`{coverage.get('total_candidate_versions', 0)}` phase-specific candidate versions"
            )
    lines.extend(["", "## Candidate decisions", ""])
    candidates = report.get("candidates", [])
    if not candidates:
        lines.append("No candidate reached a completed holdout decision.")
    for item in candidates:
        decision = "qualified" if item["qualified"] else "contested" if item["contested"] else "did not qualify"
        lines.append(
            f"- **{item['candidate_id']} v{item['candidate_version']} — {item['title']}** — {decision}; "
            f"native scores `{item['native_scores']}`, external scores `{item['external_scores']}`, "
            f"official native score `{item['official_native_score']}`, binding floor `{item['binding_score_floor']}`."
        )
        if item.get("critical_control_point_status") is not None:
            lines.append(
                "  - Critical control point: "
                f"`{item['critical_control_point_status']}` "
                f"(research: `{item['researched_control_point_status']}`); "
                "customer relationship: "
                f"`{item['customer_relationship_control']}`."
            )
        for limiter in item.get("binding_limiters", []):
            lines.append(f"  - Binding limiter: {limiter}")
    strongest = report.get("strongest_candidates", [])
    if not candidates and strongest:
        lines.extend(["", "## Strongest preserved candidates", ""])
        for item in strongest:
            lines.append(
                f"- **{item['candidate_id']} v{item['candidate_version']} — {item['title']}** "
                f"(`{item['stage']}`): `{item['artifact']}`"
            )
            if item.get("is_selected"):
                lines.append(f"  - Primary limiter: {item['primary_limiter']}")
                for contrary in item.get("contrary_evidence", []):
                    lines.append(f"  - Contrary evidence: {contrary}")
                lines.append(f"  - Reopen condition: {item['reopen_condition']}")
            if item.get("working_score") is not None:
                lines.append(f"  - Working score: `{item['working_score']}`")
                lines.append(f"  - Working score limiter: {item['primary_score_limiter']}")
            if item.get("critical_control_point_status") is not None:
                lines.append(
                    "  - Critical control point: "
                    f"`{item['critical_control_point_status']}` "
                    f"(research: `{item['researched_control_point_status']}`)."
                )
    if report.get("unresolved_evidence"):
        lines.extend(["", "## Unresolved evidence", ""])
        lines.extend(f"- {item}" for item in report["unresolved_evidence"])
    if report.get("failed_jobs"):
        lines.extend(["", "## Failed or interrupted jobs", ""])
        for job in report["failed_jobs"]:
            lines.append(
                f"- `{job['stage']}/{job['job_id']}` — {job['status']} after "
                f"{job['attempts']}/{job['max_attempts']} attempts: {job['error']}"
            )
    if report["run_status"] == "qualified":
        interpretation = (
            f"This result is {report['qualification_label']}. The label records only that the "
            "frozen candidate passed this run's binding score gate; it is not customer proof or "
            "a guarantee of business performance."
        )
    elif report["run_status"] == "contested":
        interpretation = (
            "This run produced no binding qualifier because at least one binding evaluation kept "
            "the result contested. It is not empirical market validation or permission to proceed."
        )
    elif report["run_status"] == "no_finalist":
        interpretation = (
            "No candidate reached held-out evaluation. Official and binding scores are N/A, not zero. "
            "The working scores above are development diagnostics only and cannot confirm an opportunity."
        )
    else:
        interpretation = (
            "This run produced no score-qualified candidate under holistic-11. It is an explicit "
            "non-confirmation; preserved candidates and reopen conditions remain research leads, "
            "not market-validated opportunities."
        )
    lines.extend(["", "## Interpretation", "", interpretation, ""])
    return "\n".join(lines)


def report_markdown_matches(report: Mapping[str, Any], actual: bytes) -> bool:
    # Published reports are immutable. Accept only the two exact deterministic
    # renderings; the legacy presentation changes no scores or coverage data.
    return actual in {
        render_report_markdown(report).encode("utf-8"),
        render_report_markdown(report, legacy_coverage_label=True).encode("utf-8"),
    }


def _derive_and_validate_final_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    previous_stage: str,
    closure_reason: str | None,
    selected_candidate_id: str | None,
) -> tuple[dict[str, Any], str]:
    if previous_stage not in STAGES[:-1]:
        raise InputError("run_finalized previous_stage is invalid")
    prior_state = dict(state)
    prior_state["stage"] = previous_stage
    prior_state["run_status"] = "active"
    if closure_reason is None:
        if previous_stage != "holdout":
            raise InputError("only a holdout-derived final report may omit a closure reason")
        expected = build_final_report(run_dir, manifest, prior_state)
    else:
        reason = expect_nonempty_string(closure_reason, "run_finalized closure reason")
        expected = build_early_no_qualifier_report(
            run_dir,
            manifest,
            prior_state,
            reason,
            selected_candidate_id,
        )
    report_path = run_dir / "final" / "report.json"
    markdown_path = run_dir / "report.md"
    if not report_path.is_file() or not markdown_path.is_file():
        raise InputError("finalized run is missing report artifacts")
    expected_bytes = canonical_json_bytes(expected)
    if report_path.read_bytes() != expected_bytes:
        raise InputError("final/report.json differs from the deterministically derived outcome")
    if not report_markdown_matches(expected, markdown_path.read_bytes()):
        raise InputError("report.md differs from the deterministically derived outcome")
    return expected, sha256_bytes(expected_bytes)


def validate_final_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    finalized_event: Mapping[str, Any],
) -> dict[str, Any]:
    reason_key = "no_finalist_reason"
    details = expect_object(
        finalized_event["details"],
        "run_finalized details",
        exact_keys=FINAL_EVENT_DETAIL_KEYS_V2,
    )
    report, report_digest = _derive_and_validate_final_report(
        run_dir,
        manifest,
        state,
        details["previous_stage"],
        details[reason_key],
        details["selected_candidate_id"],
    )
    if details["report_sha256"] != report_digest:
        raise InputError("run_finalized report hash differs from final/report.json")
    if (
        details["run_status"] != report["run_status"]
        or details["selected_candidate_id"] != report["selected_candidate_id"]
        or details["official_score"] != report["official_score"]
        or state["run_status"] != report["run_status"]
    ):
        raise InputError("run_finalized identity differs from the derived final report")
    return report


def _final_event_details(
    report: Mapping[str, Any],
    previous_stage: str,
    report_digest: str,
) -> dict[str, Any]:
    reason_key = "no_finalist_reason"
    return {
        "previous_stage": previous_stage,
        "run_status": report["run_status"],
        "selected_candidate_id": report["selected_candidate_id"],
        "official_score": report["official_score"],
        reason_key: report[reason_key],
        "report_sha256": report_digest,
    }


def finalize_run(
    run_dir: Path,
    no_finalist_reason: str | None = None,
    best_candidate_id: str | None = None,
) -> tuple[dict[str, Any], int]:
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, finalized_event = project_transition_state(events)
        require_job_event_state_match(events, state, manifest)
        if state["stage"] == "complete":
            if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
                raise InputError("complete state disagrees with the finalization event")
            if finalized_event is None:
                raise InputError("complete run is missing run_finalized event")
            report = validate_final_report(run_dir, manifest, state, finalized_event)
            code = 0 if state["run_status"] == "qualified" else 4
            return {**report, "idempotent": True}, code
        if finalized_event is not None and projected_stage == "complete" and state["run_status"] == "active":
            report = validate_final_report(
                run_dir,
                manifest,
                {**state, "stage": "complete", "run_status": projected_status},
                finalized_event,
            )
            state["stage"] = "complete"
            state["run_status"] = projected_status
            save_state(run_dir, state, manifest)
            code = 0 if projected_status == "qualified" else 4
            return {**report, "idempotent": True}, code
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before finalization")
        assert_active(state)
        blockers = current_stage_blockers(state)
        if blockers:
            raise ConflictError(f"current stage has running or retryable jobs: {', '.join(blockers)}")
        if no_finalist_reason is not None:
            reason = expect_nonempty_string(no_finalist_reason, "--no-finalist-reason")
            if state["stage"] != "research":
                raise ConflictError(
                    "no_finalist closure is allowed only after scored research proves every candidate has a direct-evidence fatal stop; admitted development must continue to holdout"
                )
            _validate_stage_gate(run_dir, manifest, state)
            decision = _load_portfolio_decision(run_dir, manifest)
            if any(
                item["disposition"] != "fatal"
                for item in decision["candidate_decisions"]
            ):
                raise ConflictError(
                    "research closure requires every portfolio decision to be a direct-evidence fatal stop"
                )
            report = build_early_no_qualifier_report(
                run_dir,
                manifest,
                state,
                reason,
                best_candidate_id,
            )
        else:
            if best_candidate_id is not None:
                raise InputError("--best-candidate requires --no-finalist-reason")
            if state["stage"] != "holdout":
                raise ConflictError("finalize without --no-finalist-reason requires holdout stage")
            report = build_final_report(run_dir, manifest, state)
        report_bytes = canonical_json_bytes(report)
        report_digest = write_immutable(
            run_dir / "final" / "report.json", report_bytes, root=run_dir
        )
        write_immutable(
            run_dir / "report.md",
            render_report_markdown(report).encode("utf-8"),
            root=run_dir,
        )
        previous_stage = state["stage"]
        append_event(
            run_dir,
            state,
            "run_finalized",
            stage="complete",
            details=_final_event_details(report, previous_stage, report_digest),
        )
        state["stage"] = "complete"
        state["run_status"] = report["run_status"]
        save_state(run_dir, state, manifest)
        code = 0 if report["run_status"] == "qualified" else 4
        return {**report, "idempotent": False}, code


def build_learning_digest_rows(
    run_dir: Path,
    manifest: Mapping[str, Any],
    report: Mapping[str, Any],
) -> list[dict[str, Any]]:
    portfolio = effective_portfolio_selection(run_dir, manifest)
    calibrated_structures = {
        (
            row["candidate_ref"]["candidate_id"],
            row["candidate_ref"]["version"],
            row["candidate_ref"]["candidate_sha256"],
        ): {key: row[key] for key in STRUCTURE_KEYS}
        for row in portfolio["calibration"]
    }
    decision = _load_portfolio_decision(run_dir, manifest)
    decisions = {
        (row["candidate_id"], row["candidate_version"]): row
        for row in decision["candidate_decisions"]
    }
    research_coverage = working_evaluation_coverage(run_dir, manifest, "research")
    development_coverage = working_evaluation_coverage(run_dir, manifest, "development")
    research_scores = {
        row["candidate_id"]: row for row in research_coverage["records"]
    }
    if score_bracket_enabled(manifest["config"]) and (
        run_dir / "portfolio" / "version-selection.json"
    ).is_file():
        development_by_sha = {
            row["evaluation_sha256"]: row
            for row in development_coverage["records"]
        }
        if control_contract_enabled(manifest["config"]):
            development_scores = {}
            for row in load_version_selection(run_dir, manifest)["lineages"]:
                selected_inputs = (
                    row["redesign_evaluations"]
                    if row["redesign_candidate_ref"] is not None
                    and row["selected_candidate_ref"]
                    == row["redesign_candidate_ref"]
                    else row["base_evaluations"]
                )
                binding_input = min(
                    selected_inputs,
                    key=lambda item: (
                        as_decimal(
                            item["final_score"],
                            "development conservative input score",
                        ),
                        item["judge_id"],
                    ),
                )
                development_scores[row["candidate_id"]] = development_by_sha[
                    binding_input["sha256"]
                ]
        else:
            development_scores = {
                row["candidate_id"]: development_by_sha[
                    row["selected_evaluation_sha256"]
                ]
                for row in load_version_selection(run_dir, manifest)["lineages"]
            }
    else:
        development_scores = {
            row["candidate_id"]: row for row in development_coverage["records"]
        }
    holdouts = {
        row["candidate_id"]: row for row in report.get("candidates", [])
    }
    rows: list[dict[str, Any]] = []
    for _, research in iter_research(run_dir, manifest):
        identity = (research["candidate_id"], research["candidate_version"])
        calibrated_structure = calibrated_structures.get(
            (*identity, research["candidate_sha256"])
        )
        if calibrated_structure is None:
            raise InputError(
                "learning digest research is missing its hash-bound calibration row"
            )
        decision_row = decisions.get(identity)
        if decision_row is None:
            raise InputError("learning digest research is missing its portfolio disposition")
        constructor_outcome: str | None = None
        score_record = research_scores.get(research["candidate_id"])
        if decision_row["disposition"] == "develop":
            _, constructor = _development_result_for_candidate(
                run_dir, manifest, research["candidate_id"]
            )
            constructor_outcome = constructor["outcome"]
            score_record = development_scores.get(research["candidate_id"])
        if score_record is None:
            raise InputError("learning digest candidate lacks its fresh working evaluation")
        evaluation_path = run_dir / score_record["evaluation_path"]
        evaluation = validate_canonical_evaluation(
            load_json(evaluation_path), manifest, run_dir
        )
        holdout = holdouts.get(research["candidate_id"])
        objections: list[str] = []
        reopen: list[str] = []
        if holdout is not None:
            floor = as_decimal(holdout["binding_score_floor"], "holdout binding floor")
            binding = [
                item
                for item in holdout["evaluation_diagnostics"]
                if as_decimal(item["final_score"], "holdout diagnostic score") == floor
            ]
            objections = sorted({item["primary_score_limiter"] for item in binding})
            reopen = sorted({item["evidence_needed_for_higher_score"] for item in binding})
        if not reopen:
            reopen = [evaluation["evidence_needed_for_higher_score"]]
        fresh = {
            "path": score_record["evaluation_path"],
            "sha256": sha256_file(evaluation_path),
            "evaluation_type": evaluation["evaluation_type"],
            "candidate_version": evaluation["candidate_version"],
            "candidate_sha256": evaluation["candidate_sha256"],
            "final_score": evaluation["final_score"],
        }
        expect_object(
            fresh,
            "learning digest fresh_evaluation",
            exact_keys=LEARNING_FRESH_EVALUATION_KEYS,
        )
        row = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "run_id": manifest["run_id"],
            "candidate_id": research["candidate_id"],
            "candidate_version": research["candidate_version"],
            "candidate_sha256": research["candidate_sha256"],
            "structure": calibrated_structure,
            "working_limiter": evaluation["primary_score_limiter"],
            "disconfirming_evidence": evaluation["strongest_disconfirming_evidence"],
            "disposition": decision_row["disposition"],
            "constructor_outcome": constructor_outcome,
            "fresh_evaluation": fresh,
            "holdout_objection": "; ".join(objections) if objections else None,
            "reopen_condition": "; ".join(reopen) if reopen else None,
        }
        expect_object(row, "learning digest row", exact_keys=LEARNING_ROW_KEYS)
        rows.append(row)
    identities = [(row["candidate_id"], row["candidate_version"]) for row in rows]
    if len(identities) != len(set(identities)):
        raise InputError("learning digest contains duplicate researched candidates")
    return sorted(rows, key=lambda row: (row["candidate_id"], row["candidate_version"]))


def learning_digest_bytes(rows: Sequence[Mapping[str, Any]]) -> bytes:
    return "".join(
        json.dumps(
            dict(row),
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        + "\n"
        for row in rows
    ).encode("utf-8")


def validate_learning_digest(
    outcome_dir: Path,
    manifest: Mapping[str, Any],
    report: Mapping[str, Any],
) -> list[dict[str, Any]]:
    path = outcome_dir / "learning-digest.jsonl"
    if not path.is_file():
        raise InputError("published outcome is missing learning-digest.jsonl")
    expected = build_learning_digest_rows(outcome_dir, manifest, report)
    if path.read_bytes() != learning_digest_bytes(expected):
        raise InputError("published learning digest differs from canonical researched-candidate coverage")
    return expected


def publish_run(run_dir: Path, outcomes_dir: Path, knowledge_dir: Path) -> dict[str, Any]:
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        if state["stage"] != "complete":
            raise ConflictError("publish requires a finalized run")
        _, finalized_event = require_event_state_match(run_dir, state, manifest)
        if finalized_event is None:
            raise InputError("complete run is missing run_finalized event")
        report_path = run_dir / "final" / "report.json"
        markdown_path = run_dir / "report.md"
        report = validate_final_report(run_dir, manifest, state, finalized_event)
        import_receipts = validate_external_imports(run_dir, manifest)
        if report.get("candidates"):
            _validate_stage_gate(run_dir, manifest, {**state, "stage": "frozen"})
        learning_rows = build_learning_digest_rows(run_dir, manifest, report)
        learning_bytes = learning_digest_bytes(learning_rows)
        destination = outcomes_dir / state["run_id"]
        with file_lock(outcomes_dir / ".publish.lock", root=outcomes_dir):
            copied: list[dict[str, str]] = []
            sources: list[tuple[Path, str]] = [
                (report_path, "report.json"),
                (markdown_path, "report.md"),
                (run_dir / "manifest.json", "manifest.json"),
                (run_dir / "inputs" / "founder.md", "inputs/founder.md"),
                (run_dir / "inputs" / "evaluator.txt", "inputs/evaluator.txt"),
                (run_dir / "inputs" / "config.json", "inputs/config.json"),
                (run_dir / "events.jsonl", "events.jsonl"),
            ]
            published_candidates = list(iter_candidates(run_dir, manifest))
            sources.extend(
                (path, path.relative_to(run_dir).as_posix())
                for path, _ in published_candidates
            )
            sources.extend(
                (path, path.relative_to(run_dir).as_posix())
                for path, _ in iter_research(run_dir, manifest)
            )
            sources.extend(
                (path, path.relative_to(run_dir).as_posix())
                for path, _ in iter_evaluations(run_dir, manifest)
            )
            portfolio = report.get("portfolio_decision") or {}
            portfolio_artifacts = [
                portfolio.get("dedup_artifact"),
                portfolio.get("screening_batches_artifact"),
                portfolio.get("secondary_screening_artifact"),
                portfolio.get("screening_aggregation_artifact"),
                portfolio.get("selection_artifact"),
                *portfolio.get("amendment_artifacts", []),
                portfolio.get("development_decision_artifact"),
                portfolio.get("version_selection_artifact"),
                portfolio.get("finalist_selection_artifact"),
            ]
            for artifact in portfolio_artifacts:
                if not artifact:
                    continue
                relative, path = run_relative_path(
                    run_dir, artifact["path"], "published portfolio artifact"
                )
                if sha256_file(path) != artifact["sha256"]:
                    raise InputError("published portfolio artifact hash differs from final report")
                sources.append((path, relative))
            for result_path in sorted((run_dir / "development").glob("*/constructor-result.json")):
                result = validate_development_result(load_json(result_path), manifest, run_dir)
                expected = run_dir / "development" / result["candidate_id"] / "constructor-result.json"
                if result_path.resolve() != expected.resolve():
                    raise InputError("development result stored at noncanonical path")
                sources.append((result_path, result_path.relative_to(run_dir).as_posix()))
            if (run_dir / "portfolio" / "finalists.json").is_file():
                for _, candidate in finalist_candidates(run_dir, manifest):
                    export_root = run_dir / "exports" / candidate["candidate_id"]
                    if export_root.exists():
                        _external_identity(run_dir, manifest, candidate["candidate_id"])
                    for name in ("holdout_packet.md", "response_schema.json"):
                        export_path = export_root / name
                        if export_path.is_file():
                            sources.append(
                                (export_path, export_path.relative_to(run_dir).as_posix())
                            )
            for receipt_path, receipt, _ in import_receipts:
                sources.append(
                    (receipt_path, receipt_path.relative_to(run_dir).as_posix())
                )
                raw_rel, raw_path = run_relative_path(
                    run_dir,
                    receipt["raw_response_path"],
                    "published external raw response",
                )
                sources.append((raw_path, raw_rel))
            seen: set[str] = set()
            for source, relative in sources:
                if relative in seen:
                    continue
                seen.add(relative)
                data = source.read_bytes()
                if relative == "events.jsonl":
                    # The immutable published snapshot ends at finalization.  The
                    # live run records run_published after the snapshot is
                    # durable, so filtering that receipt keeps retries byte-stable.
                    published_events = [
                        event
                        for event in load_events(source, state["run_id"])
                        if event["event"] != "run_published"
                    ]
                    data = "".join(
                        json.dumps(
                            event,
                            sort_keys=True,
                            ensure_ascii=False,
                            allow_nan=False,
                            separators=(",", ":"),
                        )
                        + "\n"
                        for event in published_events
                    ).encode("utf-8")
                digest = write_immutable(destination / relative, data, root=destination)
                copied.append({"path": relative, "sha256": digest})
            learning_digest = write_immutable(
                destination / "learning-digest.jsonl",
                learning_bytes,
                root=destination,
            )
            copied.append(
                {"path": "learning-digest.jsonl", "sha256": learning_digest}
            )
            history_path = knowledge_dir / "history_index.jsonl"
            entries = load_history_entries(history_path)
            existing = [
                entry
                for entry in entries
                if entry.get("record_type") == "opportunity_outcome_v2"
                and entry.get("run_id") == state["run_id"]
            ]
            selected_pair = next(
                (
                    pair
                    for pair in published_candidates
                    if pair[1]["candidate_id"] == report.get("selected_candidate_id")
                    and pair[1]["version"] == report.get("selected_candidate_version")
                ),
                None,
            )
            history_candidate_path: Path | None = selected_pair[0] if selected_pair else None
            history_candidate: dict[str, Any] | None = selected_pair[1] if selected_pair else None
            terminal_objection = (
                report["binding_limiters"][0]
                if report.get("binding_limiters")
                else report.get("no_finalist_reason", report.get("no_qualifier_reason"))
            )
            unresolved = report.get("unresolved_evidence", [])
            selected_summary = next(
                (
                    item
                    for item in report.get("strongest_candidates", [])
                    if item.get("candidate_id") == report.get("selected_candidate_id")
                    and item.get("candidate_version") == report.get("selected_candidate_version")
                ),
                None,
            )
            history_entry = expect_object({
                "record_type": "opportunity_outcome_v2",
                "run_id": state["run_id"],
                "run_status": state["run_status"],
                "qualification_label": report.get("qualification_label"),
                "rubric_id": report["rubric_id"],
                "rubric_sha256": report["rubric_sha256"],
                "score_scale": "/10",
                "official_score": report.get("official_score"),
                "binding_score_floor": report.get("binding_score_floor"),
                "selected_candidate_id": report.get("selected_candidate_id"),
                "selected_candidate_version": report.get("selected_candidate_version"),
                "selected_title": history_candidate.get("title") if history_candidate else None,
                "selected_fingerprint": history_candidate.get("fingerprint") if history_candidate else None,
                "source_candidate_path": (
                    history_candidate_path.relative_to(run_dir).as_posix() if history_candidate_path else None
                ),
                "source_candidate_sha256": sha256_file(history_candidate_path) if history_candidate_path else None,
                "report_sha256": sha256_file(report_path),
                "outcome_path": f"outcomes/{state['run_id']}",
                "terminal_objection": terminal_objection,
                "reopen_condition": (
                    selected_summary.get("reopen_condition")
                    if selected_summary and selected_summary.get("reopen_condition")
                    else "; ".join(unresolved)
                    if unresolved
                    else "New evidence must materially resolve the terminal objection before reopening."
                ),
                "learning_digest_path": f"outcomes/{state['run_id']}/learning-digest.jsonl",
                "learning_digest_sha256": learning_digest,
                "learning_row_count": len(learning_rows),
            }, "published opportunity history entry", exact_keys=OUTCOME_HISTORY_V2_KEYS)
            if existing and existing != [history_entry]:
                raise ConflictError("knowledge history contains a conflicting run entry")
            if not existing:
                entries.append(history_entry)
                update_history_verification(entries)
                atomic_write(
                    history_path, history_jsonl_bytes(entries), root=knowledge_dir
                )
            publication_events = [
                event
                for event in load_events(run_dir / "events.jsonl", state["run_id"])
                if event["event"] == "run_published"
                and event["details"].get("outcome_path") == history_entry["outcome_path"]
                and event["details"].get("run_status") == state["run_status"]
            ]
            if len(publication_events) > 1:
                raise InputError("event log contains duplicate run_published records")
            if not publication_events:
                append_event(
                    run_dir,
                    state,
                    "run_published",
                    details={"outcome_path": history_entry["outcome_path"], "run_status": state["run_status"]},
                )
            result: dict[str, Any] = {
                "run_id": state["run_id"],
                "run_status": state["run_status"],
                "outcome_dir": str(destination),
                "history": str(history_path),
                "artifacts": copied,
                "idempotent": bool(existing),
                "learning_row_count": len(learning_rows),
            }
            campaign_receipt = record_campaign_publication(
                run_dir, manifest, report, outcomes_dir
            )
            if campaign_receipt is not None:
                result["campaign"] = campaign_receipt
            return result


def _preflight_candidate_ref_template() -> dict[str, Any]:
    return {
        "candidate_id": "candidate-id",
        "version": 1,
        "candidate_sha256": "0" * 64,
    }


def _preflight_control_evidence_template() -> dict[str, Any]:
    return {
        "assessment": "credible_preliminary",
        "acquisition_mode": "commercial_contract",
        "counterparty_or_source": "string",
        "instrument_or_transaction": "string",
        "founder_access_path": "string",
        "claim_ids": ["claim-id"],
        "evidence_refs": ["https://example.invalid/source"],
        "unresolved_preconditions": ["string"],
        "credibility_rationale": "string",
    }


def _preflight_critical_control_point_template() -> dict[str, Any]:
    return {
        "subject_type": "workflow_position",
        "subject": "string",
        "current_owner": "string or unknown",
        "launch_controller": "string or unknown",
        "acquisition_instrument_type": "long_term_contract",
        "acquisition_instrument": "string or unknown",
        "exclusivity": "nonexclusive",
        "duration": "string or unknown",
        "revocability": "for_cause",
        "transferability": "consent_required",
        "renewal": "string or unknown",
        "counterparty_refusal_fallback": "string or unknown",
        "replaceability": "replaceable",
        "customer_relationship_owner": "the prospective business, counterparty, or unknown",
        "customer_relationship_control": "owned",
        "mechanism_control": "dependent",
        "status": "unknown",
        "founder_access_basis": "none",
        "founder_access_description": "string or unknown",
        "confidential_employer_resource_dependency": "none",
    }


def _preflight_commercial_mechanics_template() -> dict[str, Any]:
    return {
        "paid_event_or_measurable_loss": "string",
        "payer": "string or unknown",
        "budget_owner": "string or unknown",
        "purchase_trigger": "string or unknown",
        "renewal_event": "string or unknown",
        "distribution_origin": "string or unknown",
        "customer_relationship_owner": "the prospective business, counterparty, or unknown",
        "fully_loaded_economics": {
            key: "string or unknown"
            for key in sorted(FULLY_LOADED_ECONOMICS_KEYS)
        },
        "likely_incumbent_response": "string or unknown",
        "bundling_resistance": "string or unknown",
    }


def _preflight_structural_signature_template() -> dict[str, Any]:
    return {
        "commercial_model_category": "managed_service",
        "commercial_model_descriptor": "normalized descriptor",
        "control_point_category": "workflow_integration",
        "control_point_descriptor": "normalized descriptor",
        "critical_dependency_category": "distribution_channel",
        "critical_dependency_descriptor": "normalized descriptor",
    }


def _preflight_role(kind: str, stage: str) -> str:
    if kind == "candidate":
        return "discovery_scout" if stage == "discovery" else "structural_constructor"
    if kind == "research":
        return "candidate_researcher"
    if kind == "secondary-evaluation":
        return "working_secondary_screening_evaluator"
    if kind == "evaluation":
        return {
            "calibration": "working_screening_evaluator",
            "research": "working_research_evaluator",
            "development": "working_development_evaluator",
            "holdout": "native_holdout_judge",
        }.get(stage, "evaluator")
    return {
        "portfolio-selection": "calibration_selector",
        "portfolio-amendment": "calibration_selector",
        "portfolio-decision": "supervising_selector",
        "development-result": "structural_constructor",
    }[kind]


def preflight_contract(
    manifest: Mapping[str, Any], state: Mapping[str, Any], kind: str
) -> dict[str, Any]:
    if kind not in PREFLIGHT_ARTIFACT_KINDS:
        raise InputError(f"preflight does not support artifact kind: {kind}")
    stage = state["stage"]
    if score_bracket_enabled(manifest["config"]) and kind in {
        "portfolio-selection",
        "portfolio-amendment",
    }:
        raise ConflictError(
            f"{kind} is generated or disabled by score-bracket workflow state"
        )
    candidate_ref = _preflight_candidate_ref_template()
    falsification = {key: ["research-claim-id"] for key in sorted(FALSIFICATION_KEYS)}
    enums: dict[str, list[Any]] = {}
    nullable_paths: list[str] = []
    constraints: dict[str, Any] = {}
    canonical_factor_names: list[str] = []

    if kind == "candidate":
        if stage not in {"discovery", "development"}:
            raise ConflictError(f"candidate preflight is unavailable during {stage}")
        development = stage == "development"
        template: dict[str, Any] = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "candidate_id": "candidate-id",
            "version": 2 if development else 1,
            "parent": {"candidate_id": "candidate-id", "version": 1}
            if development
            else None,
            "stage": stage,
            "discovery_lane": "choose-one-configured-lane",
            "title": "string",
            "thesis": "string",
            "fingerprint": {key: "string" for key in sorted(FINGERPRINT_KEYS)},
            "structure": {key: "string" for key in sorted(STRUCTURE_KEYS)},
            "founder_fit": ["string"],
            "source_refs": ["https://example.invalid/source"],
            "economics": {
                "pricing": "string",
                "gross_margin_basis": "string",
                "acquisition_route": "string",
                "payback": "string",
                "retention_or_repeat": "string",
                "capital_required_pln": 0,
                "founder_time": "string",
                "founder_net_worth_path": "string",
            },
            "claims": [
                {
                    "claim_id": "claim-id",
                    "claim_type": "other",
                    "statement": "string",
                    "evidence_refs": ["https://example.invalid/source"],
                    "confidence": "string",
                }
            ],
            "contrary_evidence": ["string"],
            "uncertainties": ["string"],
            "risks": ["string"],
        }
        if control_contract_enabled(manifest["config"]):
            template.update(
                {
                    "critical_control_point": _preflight_critical_control_point_template(),
                    "commercial_mechanics": _preflight_commercial_mechanics_template(),
                    "structural_signature": _preflight_structural_signature_template(),
                }
            )
        if development:
            template["redesign"] = {
                "changed_fingerprint_fields": ["offer_and_business_model"],
                "economic_effect": "string",
                **(
                    {
                        "changed_structural_fields": [
                            "critical_control_point"
                        ]
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
            enums["/redesign/changed_fingerprint_fields/*"] = sorted(FINGERPRINT_KEYS)
            if control_contract_enabled(manifest["config"]):
                enums["/redesign/changed_structural_fields/*"] = sorted(STRUCTURAL_CHANGE_FIELDS)
        nullable_paths.append("/parent")
        enums.update(
            {
                "/stage": [stage],
                "/discovery_lane": list(manifest["config"]["discovery_lanes"]),
                "/claims/*/claim_type": sorted(CLAIM_TYPES),
                **(
                    {
                        "/critical_control_point/subject_type": sorted(
                            CONTROL_POINT_SUBJECT_TYPES
                        ),
                        "/critical_control_point/acquisition_instrument_type": sorted(
                            ACQUISITION_INSTRUMENT_TYPES
                        ),
                        "/critical_control_point/exclusivity": sorted(
                            EXCLUSIVITY_STATUSES
                        ),
                        "/critical_control_point/revocability": sorted(
                            REVOCABILITY_STATUSES
                        ),
                        "/critical_control_point/transferability": sorted(
                            TRANSFERABILITY_STATUSES
                        ),
                        "/critical_control_point/replaceability": sorted(
                            REPLACEABILITY_STATUSES
                        ),
                        "/critical_control_point/customer_relationship_control": sorted(
                            CUSTOMER_RELATIONSHIP_CONTROLS
                        ),
                        "/critical_control_point/mechanism_control": sorted(
                            MECHANISM_CONTROLS
                        ),
                        "/critical_control_point/status": sorted(
                            CONTROL_POINT_STATUSES
                        ),
                        "/critical_control_point/founder_access_basis": sorted(
                            FOUNDER_ACCESS_BASES
                        ),
                        "/critical_control_point/confidential_employer_resource_dependency": sorted(
                            EMPLOYER_RESOURCE_DEPENDENCIES
                        ),
                        "/structural_signature/commercial_model_category": sorted(
                            COMMERCIAL_MODEL_CATEGORIES
                        ),
                        "/structural_signature/control_point_category": sorted(
                            SIGNATURE_CONTROL_POINT_CATEGORIES
                        ),
                        "/structural_signature/critical_dependency_category": sorted(
                            CRITICAL_DEPENDENCY_CATEGORIES
                        ),
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
        )
        constraints = {
            "source_refs_max": manifest["config"]["sources_max"],
            "claim_evidence_refs": (
                "Each evidence reference must appear in source_refs. A development v2 may "
                "also cite #claim_id fragments of an explicitly listed "
                "runs/<run-id>/research/<candidate-id>/v1.json source, but only when that "
                "exact current-run parent research is canonical, bound to the immutable "
                "parent candidate hash, and contains the cited claim ID. This does not "
                "resolve arbitrary URL fragments or change any claim or evidence status."
            ),
            "founder_fit": "nonempty array of distinct strings",
            **(
                {
                    "mechanism_first_founder_access_reserve": manifest[
                        "config"
                    ]["mechanism_first_founder_access_reserve"],
                    "mechanism_first_contract": (
                        "starts from realistically obtainable control and a current paid event; "
                        "discovery rejects critical_control_point.status externally_controlled, "
                        "paid_event_or_measurable_loss unknown, and "
                        "confidential_employer_resource_dependency present. "
                        "Unknown proof remains allowed: distinguish an unverified acquisition "
                        "path from an established externally controlled mechanism. Describe "
                        "present ownership and proposed launch control separately; unsigned "
                        "agreements are not acquired rights. Never relabel an externally "
                        "controlled mechanism as unknown merely to pass validation."
                    ),
                    "customer_relationship_owner_agreement": (
                        "critical_control_point.customer_relationship_owner and "
                        "commercial_mechanics.customer_relationship_owner must agree after "
                        "fingerprint normalization; use the same description in both fields, "
                        "including any present uncertainty and proposed future ownership"
                    ),
                    "critical_control_status_consistency": (
                        "every affirmative control status requires a stated acquisition "
                        "instrument; owned requires ownership or purchase; "
                        "exclusively_contracted requires a concrete contract instrument "
                        "and exclusive terms; durably_contracted requires a concrete "
                        "contract instrument, known duration, and non-at-will revocability; "
                        "replaceable_access requires a non-ownership concrete acquisition "
                        "instrument and replaceable terms"
                    ),
                    "weak_signal_contract": (
                        "starts from observed purchasing, workaround, pricing, labor-allocation, or transaction change"
                    ),
                    "future_backcast_contract": (
                        "starts from a future operating state missing a physical, contractual, financial, or coordination mechanism"
                    ),
                }
                if control_contract_enabled(manifest["config"])
                else {}
            ),
        }
        if development:
            constraints["redesign_change_declarations"] = (
                "The changed_fingerprint_fields list must exactly name normalized fingerprint "
                "changes against the immutable parent. The changed_structural_fields list, "
                "when required, must exactly name changed top-level commercial structure "
                "containers from its enum, not descriptive fields inside structure. "
                "These two lists are derived declarations; correcting them cannot change "
                "the candidate, economics, evidence, or economic_effect rationale."
            )
        if development and control_contract_enabled(manifest["config"]):
            constraints["externally_controlled_research_resolution"] = (
                "v2 must change the critical-control structure and cannot remain "
                "externally_controlled; honest unknown proof is allowed with a concrete "
                "acquisition instrument, launch controller, and refusal fallback"
            )
    elif kind == "research":
        template = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "candidate_id": "candidate-id",
            "candidate_version": 1,
            "candidate_sha256": "0" * 64,
            "sources": [
                {
                    "source_id": "source-id",
                    "url": "https://example.invalid/source",
                    "title": "string",
                    "publisher": "string",
                    "published_at": "string",
                    "accessed_at": "string",
                    "source_type": "string",
                    **(
                        {"evidence_class": "other"}
                        if control_contract_enabled(manifest["config"])
                        else {}
                    ),
                    "stance": "supporting",
                }
            ],
            "claims": [
                {
                    "claim_id": "research-claim-id",
                    "statement": "string",
                    "assessment": "evidence",
                    "evidence_refs": ["source-id"],
                }
            ],
            "contrary_evidence": ["string"],
            "unknowns": ["string"],
            "falsification": falsification,
        }
        if control_contract_enabled(manifest["config"]):
            template.update(
                {
                    "commercial_evidence": {
                        key: {
                            "status": "evidence",
                            "claim_ids": ["research-claim-id"],
                            "source_ids": ["source-id"],
                        }
                        for key in sorted(COMMERCIAL_EVIDENCE_KEYS)
                    },
                    "critical_control_point_assessment": {
                        "status": "durably_contracted",
                        "assessment": "evidence",
                        "claim_ids": ["research-claim-id"],
                        "source_ids": ["source-id"],
                    },
                }
            )
        enums.update(
            {
                "/sources/*/stance": ["supporting", "contradicting", "context"],
                "/claims/*/assessment": ["evidence", "inference", "unknown"],
                **(
                    {
                        "/sources/*/evidence_class": sorted(EVIDENCE_CLASSES),
                        "/commercial_evidence/*/status": sorted(
                            COMMERCIAL_EVIDENCE_STATUSES
                        ),
                        "/critical_control_point_assessment/status": sorted(
                            CONTROL_POINT_STATUSES
                        ),
                        "/critical_control_point_assessment/assessment": sorted(
                            COMMERCIAL_EVIDENCE_STATUSES
                        ),
                    }
                    if control_contract_enabled(manifest["config"])
                    else {}
                ),
            }
        )
        constraints = {
            "sources_min": manifest["config"]["sources_min"],
            "sources_max": manifest["config"]["sources_max"],
            "requires_contradicting_source": True,
            "falsification_keys": sorted(FALSIFICATION_KEYS),
            **(
                {
                    "commercial_evidence_keys": sorted(
                        COMMERCIAL_EVIDENCE_KEYS
                    ),
                    "explicit_unknown": (
                        "use an unknown claim with no source_ids; absence of private validation is not fatal"
                    ),
                    "commercial_evidence_source_classes": {
                        key: sorted(classes)
                        for key, classes in sorted(COMMERCIAL_EVIDENCE_SOURCE_CLASSES.items())
                    },
                    "claim_source_coverage": (
                        "Each category and critical-control assessment requires nonempty claim_ids. "
                        "All source_ids must occur in those claims' evidence_refs. Evidence and "
                        "inference require a cited source and a claim with the same assessment. "
                        "Unknown requires only unknown claims and no source_ids. Commercial "
                        "evidence or inference also requires a source in the category's allowed "
                        "evidence classes. Choose honest classifications in the first response; "
                        "do not change a judgment or source class after rejection to make it fit."
                    ),
                }
                if control_contract_enabled(manifest["config"])
                else {}
            ),
        }
    elif kind in {"evaluation", "secondary-evaluation"}:
        if stage not in {"calibration", "research", "development", "holdout"}:
            raise ConflictError(f"evaluation preflight is unavailable during {stage}")
        canonical_factor_names = [row["name"] for row in manifest["rubric"]["factors"]]
        template = {
            "candidate_id": "candidate-id",
            "candidate_version": 1,
            "judge_id": "fresh-judge-id",
            "factors": [
                {
                    "name": name,
                    "status": "scored",
                    "score": 1,
                    "rationale": "string",
                }
                for name in canonical_factor_names
            ],
            "interaction_adjustment": 0,
            "assumptions": ["string"],
            "main_structural_strength": "string",
            "primary_score_limiter": "string",
            "strongest_disconfirming_evidence": "string",
            "highest_value_structural_change": "string",
            "evidence_needed_for_higher_score": "string",
        }
        enums["/factors/*/status"] = ["scored", "excluded"]
        nullable_paths.append("/factors/*/score")
        constraints = {
            "score_range": [1, 10],
            "interaction_adjustment_range": [-0.5, 0.5],
            "excluded_factor_score": None,
            "authored_total_forbidden": True,
            **(
                {
                    "development_evaluators_per_lineage": manifest[
                        "config"
                    ]["development_evaluators_per_lineage"],
                    "development_score_aggregation": manifest["config"][
                        "development_score_aggregation"
                    ],
                }
                if stage == "development"
                and control_contract_enabled(manifest["config"])
                else {}
            ),
        }
    elif kind == "portfolio-selection":
        template = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "selection_version": 1,
            "calibration": [
                {
                    "candidate_ref": candidate_ref,
                    "commercial_archetype": "Calibrated commercial archetype",
                    "control_point": "Calibrated control point",
                    "critical_dependency": "Calibrated critical dependency",
                    "control_point_acquisition_evidence": _preflight_control_evidence_template(),
                }
            ],
            "candidate_refs": [candidate_ref],
            "wildcard_candidate_refs": [candidate_ref],
            "missing_archetypes": ["Observed missing archetype, or use an empty list"],
            "rationale": "Evidence-backed selection rationale",
        }
        enums.update(
            {
                "/calibration/*/control_point_acquisition_evidence/assessment": sorted(
                    CONTROL_POINT_ACQUISITION_ASSESSMENTS
                ),
                "/calibration/*/control_point_acquisition_evidence/acquisition_mode": sorted(
                    CONTROL_POINT_ACQUISITION_MODES
                ),
            }
        )
        nullable_paths.append("/calibration/*/control_point_acquisition_evidence")
        constraints = {
            "shortlist_max": manifest["config"]["shortlist_max"],
            "core_shortlist_slots": manifest["config"]["core_shortlist_slots"],
            "wildcard_shortlist_slots": manifest["config"]["wildcard_shortlist_slots"],
            "core_control_evidence_assessment": "credible_preliminary",
            "wildcard_control_evidence_required": False,
        }
    elif kind == "portfolio-amendment":
        template = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "amendment_version": 1,
            "base_selection_sha256": "0" * 64,
            "remove_candidate_ref": candidate_ref,
            "add_candidate_ref": candidate_ref,
            "reason": "Evidence-backed substitution reason",
        }
    elif kind == "portfolio-decision":
        template = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "candidate_decisions": [
                {
                    "candidate_id": "candidate-id",
                    "candidate_version": 1,
                    "candidate_sha256": "0" * 64,
                    "disposition": "develop",
                    "fatal_reason": None,
                    "fatal_claim_ids": [],
                    "rationale": "Evidence-backed disposition rationale",
                }
            ],
        }
        enums.update(
            {
                "/candidate_decisions/*/disposition": [
                    "develop",
                    "not_selected",
                    "fatal",
                ],
                "/candidate_decisions/*/fatal_reason": [None]
                + sorted(FATAL_RESEARCH_REASONS),
            }
        )
        nullable_paths.append("/candidate_decisions/*/fatal_reason")
    else:
        template = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "candidate_id": "candidate-id",
            "outcome": "no_valid_redesign",
            "constructor_id": "fresh-constructor-id",
            "rationale": "Evidence-backed constructor outcome rationale",
            "falsification": falsification,
            **(
                {"structural_change": None}
                if control_contract_enabled(manifest["config"])
                else {}
            ),
        }
        enums["/outcome"] = ["redesigned", "no_valid_redesign"]
        if control_contract_enabled(manifest["config"]):
            enums.update(
                {
                    "/structural_change/resulting_control_point_status": sorted(
                        CONTROL_POINT_STATUSES
                    ),
                    "/structural_change/customer_relationship_control": sorted(
                        CUSTOMER_RELATIONSHIP_CONTROLS
                    ),
                }
            )
            nullable_paths.append("/structural_change")
        constraints = {
            "response_is_hash_free": True,
            **(
                {
                    "redesigned_structural_change_keys": sorted(
                        CONSTRUCTION_CHANGE_KEYS
                    ),
                    "no_valid_redesign_structural_change": None,
                    "prior_scores_rankings_evaluator_and_qualification_rule_forbidden": True,
                }
                if control_contract_enabled(manifest["config"])
                else {}
            ),
        }

    constraints["string_whitespace"] = (
        "String fields must not contain surrounding whitespace. A same-author "
        "correction may trim only surrounding string whitespace; internal "
        "content, judgments, numbers, and structure must remain unchanged."
    )
    return {
        "role": _preflight_role(kind, stage),
        "template": template,
        "enums": enums,
        "nullable_paths": nullable_paths,
        "constraints": constraints,
        "canonical_factor_names": canonical_factor_names,
    }


def _json_pointer_escape(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _scout_output_schema(
    value: Any, enums: Mapping[str, list[Any]], pointer: str = ""
) -> dict[str, Any]:
    """Derive transport shape from the canonical discovery template, not a second validator."""
    if isinstance(value, dict):
        return {
            "type": "object",
            "properties": {
                key: _scout_output_schema(item, enums, pointer + "/" + _json_pointer_escape(key))
                for key, item in value.items()
            },
            "required": list(value),
            "additionalProperties": False,
        }
    if isinstance(value, list):
        return {"type": "array", "items": _scout_output_schema(value[0], enums, pointer + "/*")}
    schema: dict[str, Any] = {
        "type": "null" if value is None else "number" if isinstance(value, (int, float)) else "string"
    }
    if pointer in enums:
        schema["enum"] = enums[pointer]
    elif pointer in {"/schema_version", "/version"}:
        schema["type"] = "integer"
        schema["enum"] = [value]
    return schema


def scout_contract(run_dir: Path, lane: str) -> dict[str, Any]:
    """Return only discovery-safe inputs and an exact-size structured response schema."""
    manifest, state = load_run(run_dir)
    if state["stage"] != "discovery":
        raise ConflictError("scout contract is available only during discovery")
    if lane not in manifest["config"]["discovery_lanes"]:
        raise InputError("scout lane must be a configured discovery lane")
    contract = preflight_contract(manifest, state, "candidate")
    contract["template"]["discovery_lane"] = lane
    contract["enums"]["/discovery_lane"] = [lane]
    count = manifest["config"]["seeds_per_scout"]
    return {
        "scope": "discovery_scout",
        "discovery_lane": lane,
        "candidate_count": count,
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "candidate_contract": contract,
        "strict_response_contract": {
            "type": "object",
            "properties": {
                "response": {
                    "anyOf": [
                        {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["progress"]},
                                "message": {"type": "string"},
                            },
                            "required": ["type", "message"],
                            "additionalProperties": False,
                        },
                        {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["candidates"]},
                                "candidates": {
                                    "type": "array",
                                    "minItems": count,
                                    "maxItems": count,
                                    "items": _scout_output_schema(contract["template"], contract["enums"]),
                                },
                            },
                            "required": ["type", "candidates"],
                            "additionalProperties": False,
                        },
                    ],
                },
            },
            "required": ["response"],
            "additionalProperties": False,
        },
    }


def _append_preflight_error(
    errors: list[dict[str, str]], pointer: str, code: str, message: str
) -> None:
    record = {"pointer": pointer, "code": code, "message": message}
    if record not in errors:
        errors.append(record)


def _pointer_from_validation_message(message: str) -> str:
    if message.startswith(("evaluation factors differ", "duplicate evaluation factor")):
        return "/factors"
    if message.startswith("evaluation must score"):
        return "/factors"
    prefixes = (
        "portfolio selection",
        "portfolio amendment",
        "portfolio decision",
        "development response",
        "evaluator response",
        "candidate",
        "research",
    )
    for prefix in prefixes:
        if not message.startswith(prefix):
            continue
        remainder = message[len(prefix) :]
        if not remainder.startswith((".", "[")):
            return ""
        token = remainder.split(" ", 1)[0]
        token = re.sub(r"\[(\d+)\]", r".\1", token).lstrip(".")
        parts = [part for part in token.split(".") if part]
        return "" if not parts else "/" + "/".join(
            _json_pointer_escape(part) for part in parts
        )
    return ""


def correction_content_differences(
    original: Any, corrected: Any, kind: str, pointer: str = "",
) -> list[str]:
    """Compare authored content, except canonically checked references/declarations."""
    # The candidate validator recomputes these declarations against the immutable
    # parent. Repairing them cannot change the underlying candidate content.
    if kind == "candidate" and pointer in {
        "/redesign/changed_fingerprint_fields",
        "/redesign/changed_structural_fields",
    }:
        return []
    reference_parents = {
        "/commercial_evidence/" + key for key in COMMERCIAL_EVIDENCE_KEYS
    } | {"/critical_control_point_assessment"}
    parent, _, field = pointer.rpartition("/")
    if kind == "research" and parent in reference_parents and field in {"claim_ids", "source_ids"}:
        return []
    if type(original) is not type(corrected):
        return [pointer]
    if isinstance(original, str):
        # Canonical string fields reject surrounding whitespace. Removing only
        # that boundary whitespace changes no authored words or classifications.
        return [] if original == corrected or original.strip() == corrected else [pointer]
    if isinstance(original, dict):
        differences = []
        for key in sorted(original.keys() | corrected.keys()):
            child = pointer + "/" + _json_pointer_escape(key)
            if key not in original or key not in corrected:
                differences.append(child)
            else:
                differences.extend(correction_content_differences(
                    original[key], corrected[key], kind, child,
                ))
        return differences
    if isinstance(original, list):
        if len(original) != len(corrected):
            return [pointer]
        return [
            changed
            for index, (before, after) in enumerate(zip(original, corrected))
            for changed in correction_content_differences(
                before, after, kind, pointer + "/" + str(index),
            )
        ]
    return [] if original == corrected else [pointer]


def preflight_artifact(
    run_dir: Path,
    kind: str,
    input_path: Path | None = None,
    job_id: str | None = None,
    original_input_path: Path | None = None,
) -> tuple[dict[str, Any], bool]:
    if original_input_path is not None and input_path is None:
        raise InputError("--original-input requires --input")
    manifest, state = load_run(run_dir)
    contract = preflight_contract(manifest, state, kind)
    attestation_required = preflight_attestation_enabled(manifest["config"])
    if job_id is not None and not SAFE_JOB_RE.fullmatch(job_id):
        raise InputError("--job-id is not path-safe")
    result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": state["run_id"],
        "stage": state["stage"],
        "kind": kind,
        "role": contract["role"],
        "non_mutating": True,
        "attempts_consumed": 0,
        "template": contract["template"],
        "enums": contract["enums"],
        "nullable_paths": contract["nullable_paths"],
        "constraints": contract["constraints"],
        "canonical_factor_names": contract["canonical_factor_names"],
        "completion_attestation": {
            "required": attestation_required,
            "version": (
                PREFLIGHT_ATTESTATION_VERSION if attestation_required else None
            ),
        },
        "validation": {"checked": False, "valid": None, "errors": []},
    }
    if job_id is not None:
        result["job_id"] = job_id
    if input_path is None:
        return result, True
    errors: list[dict[str, str]] = []
    digest: str | None = None
    canonical_digest: str | None = None
    try:
        digest = sha256_file(input_path)
        _, canonical_bytes, _ = _artifact_for_input(
            run_dir,
            manifest,
            state,
            job_id or "preflight",
            input_path,
            kind,
        )
        canonical_digest = sha256_bytes(canonical_bytes)
    except WorkflowError as exc:
        message = str(exc)
        _append_preflight_error(
            errors,
            _pointer_from_validation_message(message),
            "invalid_json" if message.startswith("invalid JSON") else "canonical_validation",
            message,
        )
    original_digest = None
    correction_blocked = False
    if original_input_path is not None:
        try:
            original_digest = sha256_file(original_input_path)
            differences = correction_content_differences(
                load_json(original_input_path), load_json(input_path), kind,
            )
            for pointer in differences:
                correction_blocked = True
                _append_preflight_error(
                    errors, pointer, "semantic_correction_forbidden",
                    "correction changes authored content; preserve the first response and do not admit it",
                )
        except WorkflowError as exc:
            correction_blocked = True
            _append_preflight_error(errors, "", "correction_unverifiable", str(exc))
    if attestation_required and job_id is None:
        _append_preflight_error(
            errors,
            "",
            "job_id_required",
            "--job-id is required to issue a completion preflight receipt",
        )
    valid = not errors
    result["validation"] = {
        "checked": True,
        "valid": valid,
        "input_path": str(input_path),
        "input_sha256": digest,
        "canonical_artifact_sha256": canonical_digest,
        "schema_retry_required": not valid and not correction_blocked,
        "errors": errors,
    }
    if original_input_path is not None:
        result["validation"]["original_input_sha256"] = original_digest
        result["validation"]["correction_content_preserved"] = not correction_blocked
    if (
        valid
        and attestation_required
        and job_id is not None
        and digest is not None
        and canonical_digest is not None
    ):
        result["validation"]["preflight_receipt"] = build_preflight_receipt(
            manifest,
            state["stage"],
            job_id,
            kind,
            digest,
            canonical_digest,
        )
    return result, valid


def validate_artifact(run_dir: Path, input_path: Path, kind: str) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    if kind == "candidate":
        candidate = validate_candidate(load_json(input_path), manifest, run_dir)
        canonical_bytes = canonical_json_bytes(candidate)
        return {
            "valid": True,
            "kind": kind,
            "candidate_id": candidate["candidate_id"],
            "version": candidate["version"],
            "canonical_path": candidate_relpath(candidate["candidate_id"], candidate["version"]),
            "canonical_sha256": sha256_bytes(canonical_bytes),
        }
    if kind in {"evaluation", "secondary-evaluation"}:
        evaluation_type = (
            "working_screening_secondary"
            if kind == "secondary-evaluation" and state["stage"] == "calibration"
            else {
                "calibration": "working_screening",
                "research": "working_research",
                "development": "working_development",
                "holdout": "holdout_native",
            }.get(state["stage"])
            if kind == "evaluation"
            else None
        )
        if evaluation_type is None:
            raise ConflictError(
                f"evaluation artifacts are not accepted during {state['stage']}"
            )
        evaluation = canonicalize_evaluator_response(
            load_json(input_path), manifest, run_dir, evaluation_type
        )
        return {
            "valid": True,
            "kind": kind,
            "candidate_id": evaluation["candidate_id"],
            "candidate_version": evaluation["candidate_version"],
            "judge_id": evaluation["judge_id"],
            "final_score": evaluation["final_score"],
            "qualified": evaluation["qualified"],
        }
    if kind == "research":
        research = validate_research(load_json(input_path), manifest, run_dir)
        return {
            "valid": True,
            "kind": kind,
            "candidate_id": research["candidate_id"],
            "candidate_version": research["candidate_version"],
            "canonical_path": research_relpath(research["candidate_id"], research["candidate_version"]),
        }
    if kind == "portfolio-selection":
        selection = validate_portfolio_selection(load_json(input_path), manifest, run_dir)
        return {
            "valid": True,
            "kind": kind,
            "candidate_count": len(selection["candidate_refs"]),
            "canonical_path": "portfolio/selection.json",
        }
    if kind == "portfolio-amendment":
        effective = effective_portfolio_selection(run_dir, manifest)
        expected_version = len(effective["amendments"]) + 1
        amendment, _, _ = _validate_portfolio_amendment_record(
            load_json(input_path), manifest, run_dir,
            expected_version=expected_version,
            expected_base_digest=effective["latest_binding_sha256"],
            current_refs=effective["candidate_refs"],
            current_wildcard_refs=effective["wildcard_candidate_refs"],
            calibrated_refs=effective["calibrated_refs"],
            calibration_rows=effective["calibration"],
        )
        return {
            "valid": True,
            "kind": kind,
            "amendment_version": amendment["amendment_version"],
            "canonical_path": f"portfolio/amendments/v{expected_version}.json",
        }
    if kind == "portfolio-decision":
        decision = validate_portfolio_decision(load_json(input_path), manifest, run_dir)
        return {
            "valid": True,
            "kind": kind,
            "candidate_count": len(decision["candidate_decisions"]),
            "canonical_path": "portfolio/development-decision.json",
        }
    if kind == "development-result":
        result = canonicalize_development_response(
            load_json(input_path), manifest, run_dir
        )
        return {
            "valid": True,
            "kind": kind,
            "candidate_id": result["candidate_id"],
            "outcome": result["outcome"],
            "base_candidate_sha256": result["base_candidate_sha256"],
            "final_candidate_sha256": result["final_candidate_sha256"],
            "canonical_path": f"development/{result['candidate_id']}/constructor-result.json",
        }
    validate_generic_input(input_path, kind)
    return {"valid": True, "kind": kind, "input": str(input_path), "stage": state["stage"]}


def candidate_research_context(run_dir: Path, candidate_id: str) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("candidate context requires a lowercase path-safe candidate id")
    manifest, state = load_run(run_dir)
    portfolio = effective_portfolio_selection(run_dir, manifest)
    matches = [
        ref for ref in portfolio["candidate_refs"] if ref["candidate_id"] == candidate_id
    ]
    if len(matches) != 1:
        raise InputError("candidate context is available only for one exact active shortlist ref")
    reference = matches[0]
    candidate_path = run_dir / candidate_relpath(
        reference["candidate_id"], reference["version"]
    )
    candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
    research_path = run_dir / research_relpath(candidate_id, reference["version"])
    result: dict[str, Any] = {
        "scope": "candidate_research",
        "run_id": state["run_id"],
        "stage": state["stage"],
        "run_status": state["run_status"],
        "candidate_ref": reference,
        "candidate_artifact": candidate_path.relative_to(run_dir).as_posix(),
        "candidate": candidate,
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "expected_research_artifact": research_relpath(
            candidate_id, reference["version"]
        ),
        "research_status": "missing",
    }
    if research_path.is_file():
        research = validate_research(load_json(research_path), manifest, run_dir)
        result["research_status"] = "completed"
        result["research_artifact"] = {
            "path": research_path.relative_to(run_dir).as_posix(),
            "sha256": sha256_file(research_path),
            "candidate_sha256": research["candidate_sha256"],
        }
    return result


def constructor_context(run_dir: Path, candidate_id: str) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("constructor context requires a lowercase path-safe candidate id")
    manifest, state = load_run(run_dir)
    if state["stage"] != "development":
        raise ConflictError("constructor context is available only during development")
    decision = _load_portfolio_decision(run_dir, manifest)
    matches = [
        row
        for row in decision["candidate_decisions"]
        if row["candidate_id"] == candidate_id and row["disposition"] == "develop"
    ]
    if len(matches) != 1:
        raise InputError("constructor context requires one admitted development lineage")
    row = matches[0]
    candidate_path = run_dir / candidate_relpath(
        candidate_id, row["candidate_version"]
    )
    research_path = run_dir / research_relpath(
        candidate_id, row["candidate_version"]
    )
    return {
        "scope": "structural_constructor",
        "candidate": validate_candidate(
            load_json(candidate_path), manifest, run_dir
        ),
        "candidate_artifact": {
            "path": candidate_path.relative_to(run_dir).as_posix(),
            "sha256": sha256_file(candidate_path),
        },
        "research": validate_research(
            load_json(research_path), manifest, run_dir
        ),
        "research_artifact": {
            "path": research_path.relative_to(run_dir).as_posix(),
            "sha256": sha256_file(research_path),
        },
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "response_kind": "development-result",
    }


def development_lineage_context(
    run_dir: Path, candidate_id: str
) -> dict[str, Any]:
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError(
            "development lineage context requires a lowercase path-safe candidate id"
        )
    manifest, state = load_run(run_dir)
    if state["stage"] != "development":
        raise ConflictError(
            "development lineage context is available only during development"
        )
    _, result = _development_result_for_candidate(run_dir, manifest, candidate_id)
    versions = [result["base_candidate_version"]]
    if result["outcome"] == "redesigned":
        versions.append(result["final_candidate_version"])
    candidates = [
        validate_candidate(
            load_json(run_dir / candidate_relpath(candidate_id, version)),
            manifest,
            run_dir,
        )
        for version in dict.fromkeys(versions)
    ]
    research_path = run_dir / research_relpath(
        candidate_id, result["base_candidate_version"]
    )
    research = validate_research(
        load_json(research_path), manifest, run_dir
    )
    return {
        "scope": "development_lineage_evaluation",
        "candidates": candidates,
        "candidate_artifacts": [
            {
                "path": candidate_relpath(candidate_id, candidate["version"]),
                "sha256": sha256_file(
                    run_dir / candidate_relpath(candidate_id, candidate["version"])
                ),
            }
            for candidate in candidates
        ],
        "research": research,
        "research_artifact": {
            "path": research_path.relative_to(run_dir).as_posix(),
            "sha256": sha256_file(research_path),
        },
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "evaluator_snapshot": {
            "path": "inputs/evaluator.txt",
            "sha256": manifest["source_hashes"]["Personalities/ZeroToOne.txt"],
        },
        "required_independent_evaluators": (
            manifest["config"]["development_evaluators_per_lineage"]
            if control_contract_enabled(manifest["config"])
            else 1
        ),
    }


def screening_batch_context(run_dir: Path, batch_id: str) -> dict[str, Any]:
    if not re.fullmatch(r"batch-[0-9]{2}", batch_id):
        raise InputError("screening batch id must use batch-NN format")
    manifest, state = load_run(run_dir)
    if state["stage"] != "calibration":
        raise ConflictError("screening batch context is available only during calibration")
    batches = load_screening_batches(run_dir, manifest)
    matches = [batch for batch in batches["batches"] if batch["batch_id"] == batch_id]
    if len(matches) != 1:
        raise InputError(f"unknown canonical screening batch: {batch_id}")
    candidates: list[dict[str, Any]] = []
    for ref in matches[0]["candidate_refs"]:
        path = run_dir / candidate_relpath(ref["candidate_id"], ref["version"])
        candidates.append(
            {
                "candidate_ref": ref,
                "candidate_artifact": path.relative_to(run_dir).as_posix(),
                "candidate": validate_candidate(load_json(path), manifest, run_dir),
            }
        )
    return {
        "scope": "screening_batch",
        "run_id": state["run_id"],
        "stage": state["stage"],
        "batch_id": batch_id,
        "evaluation_type": "working_screening",
        "candidates": candidates,
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "evaluator_snapshot": {
            "path": "inputs/evaluator.txt",
            "sha256": manifest["source_hashes"]["Personalities/ZeroToOne.txt"],
        },
    }


def secondary_screening_batch_context(
    run_dir: Path, secondary_batch_id: str
) -> dict[str, Any]:
    if not re.fullmatch(r"secondary-batch-[0-9]{2}", secondary_batch_id):
        raise InputError(
            "secondary screening batch id must use secondary-batch-NN format"
        )
    manifest, state = load_run(run_dir)
    if state["stage"] != "calibration":
        raise ConflictError(
            "secondary screening context is available only during calibration"
        )
    plan = load_secondary_screening_plan(run_dir, manifest)
    matches = [
        batch
        for batch in plan["batches"]
        if batch["secondary_batch_id"] == secondary_batch_id
    ]
    if len(matches) != 1:
        raise InputError(
            f"unknown canonical secondary screening batch: {secondary_batch_id}"
        )
    candidates: list[dict[str, Any]] = []
    for ref in matches[0]["candidate_refs"]:
        path = run_dir / candidate_relpath(ref["candidate_id"], ref["version"])
        candidates.append(
            {
                "candidate_ref": ref,
                "candidate_artifact": path.relative_to(run_dir).as_posix(),
                "candidate": validate_candidate(
                    load_json(path), manifest, run_dir
                ),
            }
        )
    return {
        "scope": "secondary_screening_batch",
        "evaluation_type": "working_screening_secondary",
        "candidates": candidates,
        "founder_snapshot": {
            "path": "inputs/founder.md",
            "sha256": manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
        },
        "evaluator_snapshot": {
            "path": "inputs/evaluator.txt",
            "sha256": manifest["source_hashes"]["Personalities/ZeroToOne.txt"],
        },
    }


def status_run(run_dir: Path, full_json: bool) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    counts = {status: 0 for status in sorted(JOB_STATUSES)}
    for stage_jobs in state["jobs"].values():
        for job in stage_jobs.values():
            counts[job["status"]] += 1
    result = {
        "run_id": state["run_id"],
        "stage": state["stage"],
        "run_status": state["run_status"],
        "current_stage_blockers": current_stage_blockers(state) if state["stage"] != "complete" else [],
        "job_counts": counts,
        "exhausted_jobs": [
            {
                "stage": stage,
                "job_id": job_id,
                "attempts": job["attempts"],
                "max_attempts": job["max_attempts"],
                "error": job["error"],
            }
            for stage in STAGES
            for job_id, job in sorted(state["jobs"][stage].items())
            if job_is_exhausted(job)
        ],
    }
    coverage = _evaluation_coverage_report(run_dir, manifest)
    result["highest_working_score"] = coverage["highest_working_score"]
    result["working_evaluation_coverage"] = coverage
    if (run_dir / "portfolio" / "selection.json").is_file():
        result["portfolio_decision"] = _portfolio_report(run_dir, manifest)
    if state["stage"] == "complete":
        _, finalized_event = require_event_state_match(run_dir, state, manifest)
        if finalized_event is None:
            raise InputError("complete run is missing run_finalized event")
        report = validate_final_report(run_dir, manifest, state, finalized_event)
        result["terminal_stage"] = report.get("terminal_stage")
        result["official_score"] = report.get("official_score")
    if full_json:
        result.update({"manifest": manifest, "state": state})
    return result


def _campaign_top_four_median(scores: Sequence[Decimal]) -> Decimal | None:
    top = sorted(scores, reverse=True)[:4]
    if not top:
        return None
    ordered = sorted(top)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        value = ordered[middle]
    else:
        value = (ordered[middle - 1] + ordered[middle]) / Decimal(2)
    return value.quantize(FINAL_QUANTUM, rounding=ROUND_HALF_UP)


def _sanitized_missing_archetypes(
    raw_labels: Any, candidates: Sequence[Mapping[str, Any]]
) -> list[str]:
    labels = expect_string_list(raw_labels, "portfolio missing_archetypes", unique=True)
    protected: set[str] = set()
    for candidate in candidates:
        protected.add(normalize_fingerprint(candidate["candidate_id"]))
        protected.add(normalize_fingerprint(candidate["title"]))
        structure = expect_object(
            candidate["structure"], "campaign candidate.structure", exact_keys=STRUCTURE_KEYS
        )
        protected.update(normalize_fingerprint(structure[key]) for key in STRUCTURE_KEYS)
    result: set[str] = set()
    for raw in labels:
        normalized = normalize_fingerprint(raw)
        if not _gap_archetype_label_is_safe(normalized):
            continue
        if any(
            protected_label
            and len(protected_label) >= 3
            and (protected_label in normalized or normalized in protected_label)
            for protected_label in protected
        ):
            continue
        result.add(normalized)
    return sorted(result)


def derive_campaign_cohort_metrics(
    run_dir: Path,
    manifest: Mapping[str, Any],
    report: Mapping[str, Any],
) -> dict[str, Any]:
    candidates = {
        (candidate["candidate_id"], candidate["version"]): candidate
        for _, candidate in iter_candidates(run_dir, manifest)
    }
    coverage = _evaluation_coverage_report(run_dir, manifest)
    latest_records = {
        record["candidate_id"]: record
        for record in coverage["research"]["records"]
    }
    if score_bracket_enabled(manifest["config"]) and (
        run_dir / "portfolio" / "version-selection.json"
    ).is_file():
        development_by_sha = {
            record["evaluation_sha256"]: record
            for record in coverage["development"]["records"]
        }
        if control_contract_enabled(manifest["config"]):
            for row in load_version_selection(run_dir, manifest)["lineages"]:
                selected_inputs = (
                    row["redesign_evaluations"]
                    if row["redesign_candidate_ref"] is not None
                    and row["selected_candidate_ref"]
                    == row["redesign_candidate_ref"]
                    else row["base_evaluations"]
                )
                binding_input = min(
                    selected_inputs,
                    key=lambda item: (
                        as_decimal(
                            item["final_score"],
                            "campaign development conservative input",
                        ),
                        item["judge_id"],
                    ),
                )
                latest_records[row["candidate_id"]] = development_by_sha[
                    binding_input["sha256"]
                ]
        else:
            latest_records.update(
                {
                    row["candidate_id"]: development_by_sha[
                        row["selected_evaluation_sha256"]
                    ]
                    for row in load_version_selection(run_dir, manifest)["lineages"]
                }
            )
    else:
        latest_records.update(
            {
                record["candidate_id"]: record
                for record in coverage["development"]["records"]
            }
        )
    latest: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for record in latest_records.values():
        identity = (record["candidate_id"], record["candidate_version"])
        candidate = candidates.get(identity)
        if candidate is None:
            raise InputError("working evaluation candidate is missing from campaign run")
        evaluation = validate_canonical_evaluation(
            load_json(run_dir / record["evaluation_path"]), manifest, run_dir
        )
        latest.append((candidate, evaluation))
    score_rows: list[tuple[Decimal, dict[str, Any], dict[str, Any]]] = []
    for candidate, evaluation in latest:
        score_rows.append(
            (
                as_decimal(evaluation["final_score"], "campaign working score"),
                candidate,
                evaluation,
            )
        )
    scores = [item[0] for item in score_rows]
    median = _campaign_top_four_median(scores)
    factor_totals: dict[str, tuple[Decimal, int]] = {}
    for _, _, evaluation in score_rows:
        for factor in evaluation["factors"]:
            if factor["status"] != "scored":
                continue
            name = factor["name"]
            factor_score = as_decimal(factor["score"], f"campaign factor {name}")
            total, count = factor_totals.get(name, (Decimal(0), 0))
            factor_totals[name] = (total + factor_score, count + 1)
    factor_averages = [
        (total / Decimal(count), name)
        for name, (total, count) in factor_totals.items()
        if count
    ]
    deficient_factors = [name for _, name in sorted(factor_averages)[:3]]
    portfolio = _portfolio_report(run_dir, manifest)
    if portfolio is None:
        raise InputError("campaign run is missing its structured portfolio report")
    official = _optional_campaign_score(report.get("official_score"), "report.official_score")
    return {
        "official_score": None if official is None else decimal_json(official, quantum=FINAL_QUANTUM),
        "top_four_working_median": None if median is None else decimal_json(median, quantum=FINAL_QUANTUM),
        "deficient_factors": deficient_factors,
        "missing_archetypes": _sanitized_missing_archetypes(
            portfolio["missing_archetypes"], list(candidates.values())
        ),
    }


def campaign_progress_signals(
    state: Mapping[str, Any],
    metrics: Mapping[str, Any],
    config: Mapping[str, Any],
    *,
    legacy_published: bool = False,
) -> dict[str, bool]:
    if not state["cohorts"]:
        signals = {
            "official_score": False,
            "working_median": False,
        }
        if legacy_published:
            signals["novel_archetype"] = False
        return signals
    official = _optional_campaign_score(metrics["official_score"], "campaign metric official_score")
    prior_official = _optional_campaign_score(
        state["best_official_score"], "campaign best official score"
    )
    official_progress = official is not None and (
        prior_official is None
        or official - prior_official
        >= as_decimal(
            config["campaign_official_improvement"],
            "config.campaign_official_improvement",
        )
    )
    median = _optional_campaign_score(
        metrics["top_four_working_median"], "campaign metric working median"
    )
    prior_median = _optional_campaign_score(
        state["best_working_median"], "campaign best working median"
    )
    median_progress = median is not None and (
        prior_median is None
        or median - prior_median
        >= as_decimal(
            config["campaign_working_median_improvement"],
            "config.campaign_working_median_improvement",
        )
    )
    signals = {
        "official_score": official_progress,
        "working_median": median_progress,
    }
    if legacy_published:
        current_best = _optional_campaign_score(
            metrics["best_working_score"], "campaign metric best working score"
        )
        prior_best = _optional_campaign_score(
            state["best_working_score"], "campaign best working score"
        )
        comparison_best = max(
            (item for item in (current_best, prior_best) if item is not None),
            default=None,
        )
        seen = set(state["seen_archetypes"])
        novelty_gap = as_decimal(
            config["campaign_novelty_score_gap"],
            "config.campaign_novelty_score_gap",
        )
        novel_progress = False
        if comparison_best is not None:
            for archetype, raw_score in metrics["archetype_scores"].items():
                score = _optional_campaign_score(
                    raw_score, f"campaign archetype score {archetype}"
                )
                if (
                    archetype not in seen
                    and score is not None
                    and comparison_best - score <= novelty_gap
                ):
                    novel_progress = True
                    break
        signals["novel_archetype"] = novel_progress
    return signals


def record_campaign_publication(
    run_dir: Path,
    manifest: Mapping[str, Any],
    report: Mapping[str, Any],
    outcomes_dir: Path,
) -> dict[str, Any] | None:
    binding = manifest.get("campaign")
    if binding is None:
        return None
    campaign_dir = resolve_campaign(
        outcomes_dir.parent / "campaigns", binding["campaign_id"]
    )
    report_path = outcomes_dir / report["run_id"] / "report.json"
    if not report_path.is_file():
        raise InputError("campaign registration requires the published report")
    report_digest = sha256_file(report_path)
    metrics = derive_campaign_cohort_metrics(run_dir, manifest, report)
    outcome_dir = outcomes_dir / report["run_id"]
    metric_receipt = build_campaign_metric_receipt(
        outcome_dir, binding, report["run_id"], report_digest, metrics
    )
    metric_path = outcome_dir / "campaign-metrics.json"
    metric_digest = write_immutable(
        metric_path, canonical_json_bytes(metric_receipt), root=outcome_dir
    )
    with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
        campaign_manifest, state = load_campaign(campaign_dir)
        reconcile_campaign_events(campaign_dir, campaign_manifest, state)
        validate_campaign_publication_receipts(
            campaign_dir, campaign_manifest, state
        )
        existing = next(
            (item for item in state["cohorts"] if item["run_id"] == report["run_id"]),
            None,
        )
        if existing is not None:
            if (
                existing["cohort_number"] != binding["cohort_number"]
                or existing["report_sha256"] != report_digest
                or existing["metrics_sha256"] != metric_digest
            ):
                raise ConflictError("campaign contains a conflicting cohort receipt")
            return {**existing, "idempotent": True, "campaign_status": state["status"]}
        if state["status"] != "active":
            raise ConflictError(f"campaign is already terminal: {state['status']}")
        if state["active_run_id"] != report["run_id"]:
            raise ConflictError("published run is not the campaign's active cohort")
        if state["active_cohort_number"] != binding["cohort_number"]:
            raise ConflictError("published run cohort number differs from campaign state")
        signals = campaign_progress_signals(state, metrics, campaign_manifest["config"])
        made_progress = any(signals.values())
        if not state["cohorts"]:
            streak = 0
        elif made_progress:
            streak = 0
        else:
            streak = state["no_progress_streak"] + 1
        cohort = {
            "cohort_number": binding["cohort_number"],
            "run_id": report["run_id"],
            "run_status": report["run_status"],
            "report_path": f"outcomes/{report['run_id']}/report.json",
            "report_sha256": report_digest,
            "metrics_path": f"outcomes/{report['run_id']}/campaign-metrics.json",
            "metrics_sha256": metric_digest,
            "gap_brief_path": binding["gap_brief_path"],
            "gap_brief_sha256": binding["gap_brief_sha256"],
            **metrics,
            "progress_signals": signals,
            "made_progress": made_progress,
            "no_progress_streak": streak,
        }
        validate_campaign_cohort(cohort, "campaign cohort receipt", campaign_manifest)
        validate_campaign_publication_receipts(
            campaign_dir,
            campaign_manifest,
            {**state, "cohorts": [*state["cohorts"], cohort]},
        )
        state["cohorts"].append(cohort)
        state["active_run_id"] = None
        state["active_cohort_number"] = None
        state["no_progress_streak"] = streak
        for state_key, metric_key in (
            ("best_official_score", "official_score"),
            ("best_working_median", "top_four_working_median"),
        ):
            current = _optional_campaign_score(state[state_key], f"campaign state {state_key}")
            observed = _optional_campaign_score(metrics[metric_key], f"campaign metric {metric_key}")
            if observed is not None and (current is None or observed > current):
                state[state_key] = decimal_json(observed, quantum=FINAL_QUANTUM)
        count = len(state["cohorts"])
        config = campaign_manifest["config"]
        if report["run_status"] == "qualified":
            state["status"] = "qualified"
        elif count >= config["campaign_max_cohorts"]:
            state["status"] = "max_cohorts"
        elif (
            count >= config["campaign_min_cohorts"]
            and streak >= config["campaign_plateau_patience"]
        ):
            state["status"] = "plateau"
        state["terminal_reason"] = campaign_terminal_reason(state["status"])
        save_campaign_state(campaign_dir, state, campaign_manifest)
        _ensure_campaign_event(
            campaign_dir,
            state["campaign_id"],
            "cohort_published",
            {
                "cohort_number": cohort["cohort_number"],
                "run_id": cohort["run_id"],
                "run_status": cohort["run_status"],
                "report_sha256": cohort["report_sha256"],
                "metrics_sha256": cohort["metrics_sha256"],
                "made_progress": cohort["made_progress"],
                "no_progress_streak": cohort["no_progress_streak"],
                "campaign_status": state["status"],
            },
            identity={"cohort_number": cohort["cohort_number"]},
        )
        return {**cohort, "idempotent": False, "campaign_status": state["status"]}


def campaign_next(campaign_dir: Path) -> dict[str, Any]:
    with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
        manifest, state = load_campaign(campaign_dir)
        reconcile_campaign_events(campaign_dir, manifest, state)
        validate_campaign_publication_receipts(campaign_dir, manifest, state)
        if state["status"] != "active":
            return {
                "campaign_id": state["campaign_id"],
                "action": "stop",
                "status": state["status"],
                "reason": state["terminal_reason"],
            }
        if state["active_run_id"] is not None:
            raise ConflictError(
                f"campaign cohort is still active: {state['active_run_id']}"
            )
        cohort_number = len(state["cohorts"]) + 1
        if cohort_number == 1:
            return {
                "campaign_id": state["campaign_id"],
                "action": "create_cohort",
                "cohort_number": 1,
                "gap_brief_path": None,
                "gap_brief_sha256": None,
                "idempotent": True,
            }
        latest = state["cohorts"][-1]
        brief = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "campaign_id": state["campaign_id"],
            "cohort_number": cohort_number,
            "deficient_factors": latest["deficient_factors"],
            "missing_archetypes": latest["missing_archetypes"],
        }
        validate_campaign_gap_brief(brief, manifest, cohort_number)
        relative = f"briefs/cohort-{cohort_number}.json"
        path = campaign_dir / relative
        existed = path.exists()
        digest = write_immutable(path, canonical_json_bytes(brief), root=campaign_dir)
        if not existed:
            _ensure_campaign_event(
                campaign_dir,
                state["campaign_id"],
                "gap_brief_created",
                {"cohort_number": cohort_number, "gap_brief_sha256": digest},
                identity={"cohort_number": cohort_number},
            )
        return {
            "campaign_id": state["campaign_id"],
            "action": "create_cohort",
            "cohort_number": cohort_number,
            "gap_brief_path": relative,
            "gap_brief_sha256": digest,
            "idempotent": existed,
        }


def render_campaign_report(receipt: Mapping[str, Any]) -> str:
    best_official = receipt["best_official_score"]
    working_line = (
        f"- Best working score: `{receipt['best_working_score'] if receipt['best_working_score'] is not None else 'N/A'}`"
        if "best_working_score" in receipt
        else f"- Best top-four working median: `{receipt['best_working_median'] if receipt['best_working_median'] is not None else 'N/A'}`"
    )
    lines = [
        "# Opportunity Campaign Outcome",
        "",
        f"- Campaign: `{receipt['campaign_id']}`",
        f"- Status: `{receipt['status']}`",
        f"- Cohorts: `{receipt['cohort_count']}`",
        f"- Best official score: `{best_official if best_official is not None else 'N/A'}`",
        working_line,
        f"- Quality objective achieved: `{'yes' if receipt['quality_objective_achieved'] else 'no'}`",
        f"- Campaign manifest SHA-256: `{receipt['campaign_manifest_sha256']}`",
        f"- Terminal reason: {receipt['terminal_reason']}",
        "",
        "## Cohorts",
        "",
    ]
    for cohort in receipt["cohorts"]:
        lines.append(
            f"- Cohort {cohort['cohort_number']} `{cohort['run_id']}` — `{cohort['run_status']}`; "
            f"official `{cohort['official_score'] if cohort['official_score'] is not None else 'N/A'}`, "
            f"top-four working median `{cohort['top_four_working_median'] if cohort['top_four_working_median'] is not None else 'N/A'}`, "
            f"patience `{cohort['no_progress_streak']}`."
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "The campaign found a score-qualified planning-stage opportunity. This is evaluator alignment, not empirical market validation."
                if receipt["quality_objective_achieved"]
                else "The configured campaign ended without a strict qualifier. The quality objective is unachieved; recorded scores remain unchanged and no threshold was lowered."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def finalize_campaign(campaign_dir: Path) -> tuple[dict[str, Any], int]:
    with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
        manifest, state = load_campaign(campaign_dir)
        reconcile_campaign_events(campaign_dir, manifest, state)
        validate_campaign_publication_receipts(campaign_dir, manifest, state)
        if state["status"] == "active":
            raise ConflictError("campaign cannot finalize before a deterministic stop condition")
        manifest_path = campaign_dir / "manifest.json"
        receipt = {
            "schema_version": ACTIVE_SCHEMA_VERSION,
            "campaign_id": state["campaign_id"],
            "status": state["status"],
            "terminal_reason": state["terminal_reason"],
            "cohort_count": len(state["cohorts"]),
            "best_official_score": state["best_official_score"],
            "best_working_median": state["best_working_median"],
            "quality_objective_achieved": state["status"] == "qualified",
            "campaign_manifest_sha256": sha256_file(manifest_path),
            "cohorts": state["cohorts"],
        }
        expect_object(receipt, "campaign receipt", exact_keys=CAMPAIGN_RECEIPT_KEYS)
        receipt_path = campaign_dir / "receipt.json"
        report_path = campaign_dir / "report.md"
        existed = receipt_path.exists() or report_path.exists()
        write_immutable(
            receipt_path, canonical_json_bytes(receipt), root=campaign_dir
        )
        write_immutable(
            report_path, render_campaign_report(receipt).encode("utf-8"), root=campaign_dir
        )
        _ensure_campaign_event(
            campaign_dir,
            state["campaign_id"],
            "campaign_finalized",
            {
                "status": state["status"],
                "receipt_sha256": sha256_file(receipt_path),
            },
            identity={},
        )
        source_paths = [
            (receipt_path, "receipt.json"),
            (report_path, "report.md"),
            (manifest_path, "manifest.json"),
            (campaign_dir / "events.jsonl", "events.jsonl"),
            (campaign_dir / "inputs" / "founder.md", "inputs/founder.md"),
            (campaign_dir / "inputs" / "evaluator.txt", "inputs/evaluator.txt"),
        ]
        for brief_path in sorted((campaign_dir / "briefs").glob("cohort-*.json")):
            source_paths.append(
                (brief_path, brief_path.relative_to(campaign_dir).as_posix())
            )
        outcome = {
            **receipt,
            "idempotent": existed,
        }
    # Do not hold the campaign lock while taking the publication lock.  Run
    # publication takes these locks in the opposite phase, so separating them
    # prevents a campaign/outcome lock cycle.
    outcomes_dir = campaign_dir.parent.parent / "outcomes"
    destination = outcomes_dir / "campaigns" / state["campaign_id"]
    with file_lock(outcomes_dir / ".publish.lock", root=outcomes_dir):
        for source, relative in source_paths:
            write_immutable(
                destination / relative, source.read_bytes(), root=destination
            )
    return {
        **outcome,
        "outcome_dir": str(destination),
    }, 0 if state["status"] == "qualified" else 4


def check_run(run_dir: Path, config_path: Path | None = None) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    events, finalized_event = require_event_state_match(run_dir, state, manifest)
    if state["stage"] != "complete" and (
        (run_dir / "final" / "report.json").exists() or (run_dir / "report.md").exists()
    ):
        raise InputError("active run contains unreconciled finalization artifacts")
    checked: list[str] = ["manifest.json", "state.json", "events.jsonl"]
    if manifest.get("campaign") is not None:
        binding = manifest["campaign"]
        campaign_dir = resolve_campaign(
            run_dir.parent.parent / "campaigns", binding["campaign_id"]
        )
        with file_lock(campaign_dir / ".campaign.lock", root=campaign_dir):
            campaign_manifest, campaign_state = load_campaign(campaign_dir)
            reconcile_campaign_events(campaign_dir, campaign_manifest, campaign_state)
            validate_campaign_publication_receipts(
                campaign_dir, campaign_manifest, campaign_state
            )
        if campaign_manifest["config"] != manifest["config"]:
            raise InputError("run config differs from its immutable campaign config")
        if (
            campaign_manifest["founder_sha256"]
            != manifest["source_hashes"]["PERSONALITY_SITUATION.md"]
            or campaign_manifest["rubric"]["sha256"]
            != manifest["rubric"]["sha256"]
            or campaign_manifest["rubric"]["factors"]
            != manifest["rubric"]["factors"]
        ):
            raise InputError("run founder or evaluator snapshot differs from its campaign")
        if binding["gap_brief_path"] is not None:
            gap_path = campaign_dir / binding["gap_brief_path"]
            brief = validate_campaign_gap_brief(
                load_json(gap_path), campaign_manifest, binding["cohort_number"]
            )
            if gap_path.read_bytes() != canonical_json_bytes(brief):
                raise InputError("run campaign gap brief is not canonical")
            if sha256_file(gap_path) != binding["gap_brief_sha256"]:
                raise InputError("run campaign gap brief hash differs from its manifest")
        recorded = any(
            item["run_id"] == state["run_id"]
            and item["cohort_number"] == binding["cohort_number"]
            for item in campaign_state["cohorts"]
        )
        active = (
            campaign_state["active_run_id"] == state["run_id"]
            and campaign_state["active_cohort_number"] == binding["cohort_number"]
        )
        if not (recorded or active):
            raise InputError("run is not attached to its campaign ledger")
    for source, snapshot in INPUT_SNAPSHOTS.items():
        snapshot_path = run_dir / snapshot
        if not snapshot_path.is_file():
            raise InputError(f"run is missing immutable input snapshot: {snapshot}")
        if sha256_file(snapshot_path) != manifest["source_hashes"][source]:
            raise InputError(f"input snapshot hash mismatch: {snapshot}")
        checked.append(snapshot)
    for stage, jobs in state["jobs"].items():
        for job_id, job in jobs.items():
            if job["status"] == "completed":
                relative, artifact = run_relative_path(run_dir, job["artifact"], f"job {stage}/{job_id} artifact")
                if sha256_file(artifact) != job["artifact_sha256"]:
                    raise InputError(f"job artifact hash mismatch: {relative}")
                checked.append(relative)
    stored_candidates = list(iter_candidates(run_dir, manifest))
    for path, _ in stored_candidates:
        checked.append(path.relative_to(run_dir).as_posix())
    screening_path = run_dir / "portfolio" / "screening-batches.json"
    if screening_path.is_file():
        load_screening_batches(run_dir, manifest)
        checked.append("portfolio/screening-batches.json")
    secondary_screening_path = run_dir / "portfolio" / "secondary-screening.json"
    if secondary_screening_path.is_file():
        load_secondary_screening_plan(run_dir, manifest)
        checked.append("portfolio/secondary-screening.json")
    screening_aggregation_path = run_dir / "portfolio" / "screening-aggregation.json"
    if screening_aggregation_path.is_file():
        load_screening_aggregation(run_dir, manifest)
        checked.append("portfolio/screening-aggregation.json")
    version_selection_path = run_dir / "portfolio" / "version-selection.json"
    if version_selection_path.is_file():
        load_version_selection(run_dir, manifest)
        checked.append("portfolio/version-selection.json")
    finalist_path = run_dir / "portfolio" / "finalists.json"
    if state["stage"] in {"frozen", "holdout"} and not finalist_path.is_file():
        raise InputError("frozen or holdout run is missing canonical finalist selection")
    if finalist_path.is_file():
        if load_finalist_selection(run_dir, manifest) != build_finalist_selection(
            run_dir, manifest
        ):
            raise InputError("finalist selection differs from deterministic ranking")
        checked.append("portfolio/finalists.json")
        for _, candidate in finalist_candidates(run_dir, manifest):
            validate_finalist_lineage(run_dir, manifest, candidate)
    for path, _ in iter_research(run_dir, manifest):
        checked.append(path.relative_to(run_dir).as_posix())
    import_receipts = validate_external_imports(run_dir, manifest)
    for receipt_path, receipt, _ in import_receipts:
        checked.extend(
            [
                receipt_path.relative_to(run_dir).as_posix(),
                receipt["raw_response_path"],
            ]
        )
        if receipt["status"] == "accepted":
            checked.append(receipt["evaluation"])
    for path, _ in iter_evaluations(run_dir, manifest):
        checked.append(path.relative_to(run_dir).as_posix())
    require_packets = state["stage"] == "holdout"
    report: dict[str, Any] | None = None
    if state["stage"] == "complete":
        if finalized_event is None:
            raise InputError("complete run is missing run_finalized event")
        report = validate_final_report(run_dir, manifest, state, finalized_event)
        require_packets = bool(report["candidates"])
    if require_packets:
        for _, candidate in finalist_candidates(run_dir, manifest):
            try:
                _external_identity(run_dir, manifest, candidate["candidate_id"])
            except ConflictError as exc:
                raise InputError(str(exc)) from exc
            checked.extend(
                [
                    f"exports/{candidate['candidate_id']}/holdout_packet.md",
                    f"exports/{candidate['candidate_id']}/response_schema.json",
                ]
            )
    if state["stage"] == "complete":
        checked.extend(["final/report.json", "report.md"])
    drift: list[str] = []
    for relative, pinned_hash in manifest["source_hashes"].items():
        current_path = config_path if relative == "config/opportunity-workflow.json" and config_path else REPO_ROOT / relative
        if not current_path.is_file():
            drift.append(relative)
            continue
        if relative == "config/opportunity-workflow.json":
            current_hash = sha256_bytes(
                canonical_json_bytes(validate_config(load_json(current_path)))
            )
        else:
            current_hash = sha256_file(current_path)
        if current_hash != pinned_hash:
            drift.append(relative)
    return {
        "valid": True,
        "run_id": state["run_id"],
        "stage": state["stage"],
        "run_status": state["run_status"],
        "checked_artifacts": sorted(set(checked)),
        "source_drift": drift,
    }


def check_environment(config_path: Path) -> dict[str, Any]:
    config = validate_config(load_json(config_path))
    factors, digest = parse_rubric(REPO_ROOT / "Personalities" / "ZeroToOne.txt")
    missing = [relative for relative in SOURCE_PATHS[:-1] if not (REPO_ROOT / relative).is_file()]
    if missing:
        raise InputError(f"missing source files: {', '.join(missing)}")
    published = validate_published_outcomes(REPO_ROOT / "outcomes")
    return {
        "valid": True,
        "config": str(config_path),
        "schema_version": config["schema_version"],
        "rubric_id": config["rubric_id"],
        "rubric_sha256": digest,
        "factor_count": len(factors),
        "weight_total": decimal_json(sum((weight for _, weight in factors), Decimal(0))),
        "published_outcomes": published,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="workflow config path")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR, help="run storage directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new = subparsers.add_parser("new", help="create a new immutable run manifest")
    new.add_argument("--campaign", help="attach this run as the next campaign cohort")

    campaign = subparsers.add_parser("campaign", help="create and advance a scored multi-cohort campaign")
    campaign_commands = campaign.add_subparsers(dest="campaign_command", required=True)
    campaign_commands.add_parser("new", help="create a new immutable campaign ledger")
    campaign_status_parser = campaign_commands.add_parser("status", help="show campaign status")
    campaign_status_parser.add_argument("campaign")
    campaign_status_parser.add_argument("--json", action="store_true", help="include campaign manifest and state")
    campaign_next_parser = campaign_commands.add_parser("next", help="return the deterministic next campaign action")
    campaign_next_parser.add_argument("campaign")
    campaign_finalize_parser = campaign_commands.add_parser("finalize", help="write a terminal campaign receipt")
    campaign_finalize_parser.add_argument("campaign")

    status = subparsers.add_parser("status", help="show run status")
    status.add_argument("run")
    status_scope = status.add_mutually_exclusive_group()
    status_scope.add_argument("--json", action="store_true", help="include complete manifest and state")
    status_scope.add_argument(
        "--candidate",
        help="show role-safe context for one active-shortlist researcher",
    )
    status_scope.add_argument(
        "--batch",
        help="show role-safe context for one lane-balanced screening evaluator",
    )
    status_scope.add_argument(
        "--secondary-batch",
        help="show candidate-only context for one deterministic close-cutoff evaluator",
    )
    status_scope.add_argument(
        "--constructor",
        help="show score-blind context for one admitted structural constructor",
    )
    status_scope.add_argument(
        "--development-lineage",
        help="show equivalent-condition context for one development lineage evaluator",
    )

    resume = subparsers.add_parser("resume", help="recover interrupted jobs and list eligible retries")
    resume.add_argument("run")

    job = subparsers.add_parser("job", help="start, complete, or fail one mechanical job")
    job.add_argument("run")
    job.add_argument("job_id")
    job.add_argument("action", choices=("start", "complete", "fail"))
    job.add_argument("--stage", choices=STAGES)
    job.add_argument("--input", type=Path)
    job.add_argument("--kind", choices=tuple(sorted(ARTIFACT_KINDS)))
    job.add_argument("--error")
    job.add_argument(
        "--preflight-sha256",
        help="require job-complete input bytes to match a successful preflight",
    )
    job.add_argument(
        "--preflight-receipt-sha256",
        help="bind a structured completion to its contextual preflight receipt",
    )

    preflight = subparsers.add_parser(
        "preflight",
        help="emit a role-specific template and validate output without consuming an attempt",
    )
    preflight.add_argument("run")
    preflight.add_argument("--kind", choices=tuple(sorted(PREFLIGHT_ARTIFACT_KINDS)), required=True)
    preflight.add_argument("--input", type=Path)
    preflight.add_argument("--original-input", type=Path, help="Preserved first response for content-preserving correction checks")
    preflight.add_argument("--job-id")

    scout = subparsers.add_parser("scout-contract", help="emit discovery-safe context and an exact-size output schema")
    scout.add_argument("run")
    scout.add_argument("--lane", required=True)

    validate = subparsers.add_parser("validate", help="validate an artifact without storing it")
    validate.add_argument("run")
    validate.add_argument("--input", type=Path, required=True)
    validate.add_argument("--kind", choices=tuple(sorted(ARTIFACT_KINDS)), required=True)

    dedup = subparsers.add_parser("dedup", help="deduplicate discovery candidates by structural fingerprint")
    dedup.add_argument("run")

    advance = subparsers.add_parser("advance", help="advance after all current-stage jobs are terminal")
    advance.add_argument("run")

    export = subparsers.add_parser("export-external", help="write a deterministic external holdout packet")
    export.add_argument("run")
    export.add_argument("candidate_id")

    holdout_assignment = subparsers.add_parser(
        "holdout-assignment",
        help="emit only the immutable packet, strict response contract, and temporary destination",
    )
    holdout_assignment.add_argument("run")
    holdout_assignment.add_argument("candidate_id")
    holdout_assignment.add_argument(
        "--response-destination", type=Path, required=True
    )

    import_parser = subparsers.add_parser("import-external", help="preserve and import one external response")
    import_parser.add_argument("run")
    import_parser.add_argument("candidate_id")
    import_parser.add_argument("raw_response", type=Path)

    finalize = subparsers.add_parser("finalize", help="apply native and binding external score gates")
    finalize.add_argument("run")
    finalize.add_argument("--no-finalist-reason")
    finalize.add_argument("--best-candidate")

    publish = subparsers.add_parser("publish", help="publish any terminal outcome idempotently")
    publish.add_argument("run")

    quarantine = subparsers.add_parser(
        "quarantine-outcome",
        help="immutably exclude a published outcome from business-decision use",
    )
    quarantine.add_argument("run")
    quarantine.add_argument(
        "--reason-code",
        choices=tuple(sorted(OUTCOME_QUARANTINE_REASON_CODES)),
        required=True,
    )
    quarantine.add_argument("--reason", required=True)

    check = subparsers.add_parser("check", help="check configuration or a stored run")
    check.add_argument("run", nargs="?")
    return parser


def emit(value: Mapping[str, Any], *, stream: Any | None = None) -> None:
    if stream is None:
        stream = sys.stdout
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False), file=stream)


def dispatch(args: argparse.Namespace) -> int:
    config_path = args.config.resolve()
    runs_dir = args.runs_dir.resolve()
    campaigns_dir = campaign_storage_for_runs(runs_dir).resolve()
    if args.command == "new":
        emit(make_run(config_path, runs_dir, args.campaign, campaigns_dir))
        return 0
    if args.command == "campaign":
        if args.campaign_command == "new":
            emit(new_campaign(config_path, campaigns_dir))
            return 0
        campaign_dir = resolve_campaign(campaigns_dir, args.campaign)
        if args.campaign_command == "status":
            emit(campaign_status(campaign_dir, args.json))
            return 0
        if args.campaign_command == "next":
            emit(campaign_next(campaign_dir))
            return 0
        if args.campaign_command == "finalize":
            result, code = finalize_campaign(campaign_dir)
            emit(result)
            return code
        raise InputError(f"unknown campaign command: {args.campaign_command}")
    if args.command == "check" and args.run is None:
        emit(check_environment(config_path))
        return 0
    if args.command == "quarantine-outcome":
        emit(
            quarantine_published_outcome(
                args.run,
                runs_dir.parent / "outcomes",
                runs_dir.parent / "knowledge",
                args.reason_code,
                args.reason,
            )
        )
        return 0
    run_dir = resolve_run(runs_dir, args.run)
    if args.command == "status":
        if args.candidate is not None:
            emit(candidate_research_context(run_dir, args.candidate))
        elif args.constructor is not None:
            emit(constructor_context(run_dir, args.constructor))
        elif args.development_lineage is not None:
            emit(
                development_lineage_context(
                    run_dir, args.development_lineage
                )
            )
        elif args.secondary_batch is not None:
            emit(
                secondary_screening_batch_context(
                    run_dir, args.secondary_batch
                )
            )
        elif args.batch is not None:
            emit(screening_batch_context(run_dir, args.batch))
        else:
            emit(status_run(run_dir, args.json))
        return 0
    if args.command == "resume":
        emit(resume_run(run_dir))
        return 0
    if args.command == "preflight":
        result, valid = preflight_artifact(
            run_dir,
            args.kind,
            args.input.resolve() if args.input is not None else None,
            args.job_id,
            args.original_input.resolve() if args.original_input is not None else None,
        )
        emit(result)
        return 0 if valid else InputError.exit_code
    if args.command == "scout-contract":
        emit(scout_contract(run_dir, args.lane))
        return 0
    if args.command == "job":
        if args.action == "start":
            if (
                args.input is not None
                or args.kind is not None
                or args.error is not None
                or args.preflight_sha256 is not None
                or args.preflight_receipt_sha256 is not None
            ):
                raise InputError("job start accepts only optional --stage")
            emit(start_job(run_dir, args.job_id, args.stage))
            return 0
        if args.stage is not None:
            raise InputError("--stage is valid only for job start")
        if args.action == "complete":
            if args.input is None or args.kind is None or args.error is not None:
                raise InputError("job complete requires --input and --kind, and does not accept --error")
            emit(
                complete_job(
                    run_dir,
                    args.job_id,
                    args.input.resolve(),
                    args.kind,
                    args.preflight_sha256,
                    args.preflight_receipt_sha256,
                )
            )
            return 0
        if (
            args.error is None
            or args.input is not None
            or args.kind is not None
            or args.preflight_sha256 is not None
            or args.preflight_receipt_sha256 is not None
        ):
            raise InputError("job fail requires --error, and does not accept --input or --kind")
        emit(fail_job(run_dir, args.job_id, args.error))
        return 0
    if args.command == "validate":
        emit(validate_artifact(run_dir, args.input.resolve(), args.kind))
        return 0
    if args.command == "dedup":
        emit(dedup_run(run_dir))
        return 0
    if args.command == "advance":
        emit(advance_run(run_dir))
        return 0
    if args.command == "export-external":
        emit(export_external(run_dir, args.candidate_id))
        return 0
    if args.command == "holdout-assignment":
        emit(
            native_holdout_assignment(
                run_dir,
                args.candidate_id,
                args.response_destination,
            )
        )
        return 0
    if args.command == "import-external":
        emit(import_external(run_dir, args.candidate_id, args.raw_response.resolve()))
        return 0
    if args.command == "finalize":
        result, code = finalize_run(run_dir, args.no_finalist_reason, args.best_candidate)
        emit(result)
        return code
    if args.command == "publish":
        emit(publish_run(run_dir, runs_dir.parent / "outcomes", runs_dir.parent / "knowledge"))
        return 0
    if args.command == "check":
        emit(check_run(run_dir, config_path))
        return 0
    raise InputError(f"unknown command: {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args)
    except WorkflowError as exc:
        emit({"error": str(exc), "error_type": exc.__class__.__name__}, stream=sys.stderr)
        return exc.exit_code
    except KeyboardInterrupt:
        emit({"error": "interrupted", "error_type": "KeyboardInterrupt"}, stream=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
