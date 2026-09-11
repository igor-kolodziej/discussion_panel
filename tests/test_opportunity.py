from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts import opportunity as op


class OpportunityTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.runs_dir = self.root / "runs"
        legacy_config = op.load_json(op.DEFAULT_CONFIG)
        legacy_config.pop("screening_batches")
        for key in (
            op.CONTROL_CONTRACT_CONFIG_KEYS
            | op.PREFLIGHT_ATTESTATION_CONFIG_KEYS
        ):
            legacy_config.pop(key)
        legacy_config.update(
            {
                "unique_min": 24,
                "shortlist_max": 8,
                "core_shortlist_slots": 6,
                "wildcard_shortlist_slots": 2,
            }
        )
        self.config_path = self.root / "legacy-opportunity-workflow.json"
        self.config_path.write_bytes(op.canonical_json_bytes(legacy_config))
        created = op.make_run(self.config_path, self.runs_dir)
        self.run_id = created["run_id"]
        self.run_dir = Path(created["run_dir"])

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def load(self):
        return op.load_run(self.run_dir)

    def run_cli(self, argv: list[str]) -> tuple[int, dict, dict]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = op.main(argv)
        output = json.loads(stdout.getvalue()) if stdout.getvalue().strip() else {}
        error = json.loads(stderr.getvalue()) if stderr.getvalue().strip() else {}
        return code, output, error

    def set_stage(self, stage: str) -> None:
        manifest, state = self.load()
        if op.STAGES.index(stage) < op.STAGES.index(state["stage"]):
            raise AssertionError("test helper cannot move a run backward")
        while state["stage"] != stage:
            previous = state["stage"]
            advanced = op.STAGES[op.STAGES.index(previous) + 1]
            op.append_event(
                self.run_dir,
                state,
                "stage_advanced",
                stage=advanced,
                details={"previous_stage": previous, "stage": advanced},
            )
            state["stage"] = advanced
            op.save_state(self.run_dir, state, manifest)

    def candidate(
        self,
        candidate_id: str = "alpha",
        *,
        version: int = 1,
        stage: str = "discovery",
        parent: dict | None = None,
        fingerprint_seed: str | None = None,
        capital: object = 100000,
        discovery_lane: str = "mechanism-first",
    ) -> dict:
        seed = fingerprint_seed or candidate_id
        schema_version = json.loads(self.config_path.read_text(encoding="utf-8"))["schema_version"]
        sources = [
            f"https://example.com/{candidate_id}/loss",
            f"https://example.com/{candidate_id}/budget",
            f"https://example.com/{candidate_id}/control",
        ]
        candidate = {
            "schema_version": schema_version,
            "candidate_id": candidate_id,
            "version": version,
            "parent": parent,
            "stage": stage,
            "discovery_lane": discovery_lane,
            "title": f"Opportunity {candidate_id}",
            "thesis": f"A specific structural thesis for {candidate_id}.",
            "fingerprint": {
                "customer": f"industrial buyer {seed}",
                "problem_trigger": f"mandatory failure event {seed}",
                "payer_and_paid_event": f"operations lead pays at incident {seed}",
                "offer_and_business_model": f"managed evidence service subscription {seed}",
                "distribution_mechanism": f"specialist broker referral {seed}",
                "compounding_advantage": f"accepted case memory {seed}",
            },
            "structure": {
                "commercial_archetype": f"specialist workflow assurance {seed}",
                "control_point": f"accepted incident evidence {seed}",
                "critical_dependency": f"broker access agreement {seed}",
            },
            "founder_fit": ["AI-assisted research", "Warsaw base"],
            "source_refs": sources,
            "economics": {
                "pricing": "120000 PLN annual contract",
                "gross_margin_basis": "70% after specialist review",
                "acquisition_route": "broker referrals",
                "payback": "under six months",
                "retention_or_repeat": "annual renewal",
                "capital_required_pln": capital,
                "founder_time": "20 hours weekly",
                "founder_net_worth_path": "retained earnings and owner distributions",
            },
            "claims": [
                {
                    "claim_id": "claim-loss",
                    "claim_type": "paid_event_or_measurable_loss",
                    "statement": "The triggering workflow is costly and recurring.",
                    "evidence_refs": [sources[0]],
                    "confidence": "medium",
                },
                {
                    "claim_id": "claim-budget",
                    "claim_type": "payer_and_budget",
                    "statement": "An operating budget owner pays after the trigger.",
                    "evidence_refs": [sources[1]],
                    "confidence": "medium",
                },
                {
                    "claim_id": "claim-control",
                    "claim_type": "founder_control_point_path",
                    "statement": "The founder can contract for the proposed control point.",
                    "evidence_refs": [sources[2]],
                    "confidence": "medium",
                }
            ],
            "contrary_evidence": ["Some buyers may internalize the work."],
            "uncertainties": ["Referral conversion remains untested."],
            "risks": ["A platform could narrow the workflow gap."],
        }
        if op.control_contract_enabled(op.load_json(self.config_path)):
            customer_owner = f"business {candidate_id}"
            candidate.update(
                {
                    "critical_control_point": {
                        "subject_type": "workflow_position",
                        "subject": f"accepted incident evidence workflow {seed}",
                        "current_owner": customer_owner,
                        "launch_controller": customer_owner,
                        "acquisition_instrument_type": "ownership",
                        "acquisition_instrument": "Founder-built and business-owned operating workflow.",
                        "exclusivity": "not_applicable",
                        "duration": "Indefinite while the business operates.",
                        "revocability": "not_applicable",
                        "transferability": "transferable",
                        "renewal": "No counterparty renewal is required.",
                        "counterparty_refusal_fallback": "Sell directly through another specialist channel.",
                        "replaceability": "replaceable",
                        "customer_relationship_owner": customer_owner,
                        "customer_relationship_control": "owned",
                        "mechanism_control": "owned",
                        "status": "owned",
                        "founder_access_basis": "owned_or_controlled_asset",
                        "founder_access_description": "The founder can lawfully build and own the bounded workflow.",
                        "confidential_employer_resource_dependency": "none",
                    },
                    "commercial_mechanics": {
                        "paid_event_or_measurable_loss": f"Recurring incident remediation spend {seed}",
                        "payer": f"Industrial operator {seed}",
                        "budget_owner": "Operations director",
                        "purchase_trigger": "A documented incident or annual assurance renewal.",
                        "renewal_event": "Annual operating assurance renewal.",
                        "distribution_origin": f"Specialist broker referral {seed}",
                        "customer_relationship_owner": customer_owner,
                        "fully_loaded_economics": {
                            "revenue_basis": "120000 PLN annual contract",
                            "variable_costs": "Specialist review per incident",
                            "delivery_and_support_costs": "Named implementation and support labor",
                            "acquisition_cost": "Broker referral fee and founder sales time",
                            "overhead_and_compliance": "Insurance, software, and compliance review",
                            "contribution_margin": "Positive after all listed delivery costs",
                            "cash_conversion": "Annual prepayment with monthly delivery",
                        },
                        "likely_incumbent_response": "Bundle a narrower assurance feature.",
                        "bundling_resistance": "Independent evidence acceptance and cross-platform workflow depth.",
                    },
                    "structural_signature": {
                        "commercial_model_category": "other",
                        "commercial_model_descriptor": f"specialist workflow assurance {seed}",
                        "control_point_category": "other",
                        "control_point_descriptor": f"accepted incident evidence {seed}",
                        "critical_dependency_category": "other",
                        "critical_dependency_descriptor": f"broker access agreement {seed}",
                    },
                }
            )
        if version == 2 and stage == "development":
            candidate["fingerprint"]["offer_and_business_model"] += " redesigned"
            candidate["economics"]["pricing"] = "150000 PLN annual redesigned contract"
            candidate["redesign"] = {
                "changed_fingerprint_fields": ["offer_and_business_model"],
                "economic_effect": "Raises contract value while preserving the controlled workflow.",
            }
            if "commercial_mechanics" in candidate:
                candidate["commercial_mechanics"]["fully_loaded_economics"][
                    "revenue_basis"
                ] = "150000 PLN annual redesigned contract"
                candidate["redesign"]["changed_structural_fields"] = [
                    "commercial_mechanics"
                ]
        return candidate

    def store_candidate(self, candidate: dict) -> tuple[Path, dict]:
        manifest, _ = self.load()
        canonical = op.validate_candidate(candidate, manifest, self.run_dir)
        path = self.run_dir / op.candidate_relpath(canonical["candidate_id"], canonical["version"])
        op.write_immutable(path, op.canonical_json_bytes(canonical))
        return path, canonical

    def research(self, candidate: dict) -> dict:
        path = self.run_dir / op.candidate_relpath(candidate["candidate_id"], candidate["version"])
        sources = [
            {
                "source_id": f"source-{index}",
                "url": f"https://example.com/source-{index}",
                "title": f"Source {index}",
                "publisher": "Example Authority",
                "published_at": "2026-01-01",
                "accessed_at": "2026-08-24",
                "source_type": "primary",
                "stance": "contradicting" if index == 5 else "supporting",
                **(
                    {
                        "evidence_class": (
                            "direct_buyer",
                            "distribution",
                            "unit_economics",
                            "rights_control_access",
                            "market_context",
                            "incumbent",
                        )[index]
                    }
                    if op.control_contract_enabled(self.load()[0]["config"])
                    else {}
                ),
            }
            for index in range(6)
        ]
        result = {
            "schema_version": candidate["schema_version"],
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "candidate_sha256": op.sha256_file(path),
            "sources": sources,
            "claims": [
                {
                    "claim_id": f"research-claim-{index + 1}",
                    "statement": f"Research addresses falsification category {index + 1}.",
                    "assessment": "evidence" if index < 4 or index == 5 else "inference",
                    "evidence_refs": [f"source-{index}"],
                }
                for index in range(6)
            ],
            "contrary_evidence": ["One source describes an internal substitute."],
            "unknowns": ["Observed conversion is not yet available."],
            "falsification": {
                key: [f"research-claim-{index + 1}"]
                for index, key in enumerate(sorted(op.FALSIFICATION_KEYS))
            },
        }
        if op.control_contract_enabled(self.load()[0]["config"]):
            result.update(
                {
                    "commercial_evidence": {
                        "buyer_or_paid_event": {
                            "status": "evidence",
                            "claim_ids": ["research-claim-1"],
                            "source_ids": ["source-0"],
                        },
                        "distribution_and_acquisition": {
                            "status": "evidence",
                            "claim_ids": ["research-claim-2"],
                            "source_ids": ["source-1"],
                        },
                        "fully_loaded_unit_economics": {
                            "status": "evidence",
                            "claim_ids": ["research-claim-3"],
                            "source_ids": ["source-2"],
                        },
                        "rights_control_access_contractibility": {
                            "status": "evidence",
                            "claim_ids": ["research-claim-4"],
                            "source_ids": ["source-3"],
                        },
                    },
                    "critical_control_point_assessment": {
                        "status": candidate["critical_control_point"]["status"],
                        "assessment": "evidence",
                        "claim_ids": ["research-claim-4"],
                        "source_ids": ["source-3"],
                    },
                }
            )
        return result

    def store_research(self, research: dict) -> Path:
        manifest, _ = self.load()
        canonical = op.validate_research(research, manifest, self.run_dir)
        path = self.run_dir / op.research_relpath(canonical["candidate_id"], canonical["candidate_version"])
        op.write_immutable(path, op.canonical_json_bytes(canonical))
        return path

    def candidate_ref(self, candidate: dict) -> dict:
        path = self.run_dir / op.candidate_relpath(candidate["candidate_id"], candidate["version"])
        return {
            "candidate_id": candidate["candidate_id"],
            "version": candidate["version"],
            "candidate_sha256": op.sha256_file(path),
        }

    def control_point_acquisition_evidence(
        self,
        candidate: dict,
        *,
        assessment: str = "credible_preliminary",
    ) -> dict:
        return {
            "assessment": assessment,
            "acquisition_mode": "commercial_contract",
            "counterparty_or_source": "A named workflow operator with authority to contract.",
            "instrument_or_transaction": "A bounded paid workflow-access agreement.",
            "founder_access_path": "Direct outreach through the documented specialist channel.",
            "claim_ids": ["claim-control"] if assessment == "credible_preliminary" else [],
            "evidence_refs": [candidate["source_refs"][2]]
            if assessment == "credible_preliminary"
            else [],
            "unresolved_preconditions": ["Counterparty signature remains untested."],
            "credibility_rationale": "The cited route identifies the counterparty, instrument, and bounded founder access path.",
        }

    def complete_json_job(
        self,
        job_id: str,
        kind: str,
        payload: dict,
        *,
        stage: str | None = None,
    ) -> dict:
        if stage is not None:
            self.set_stage(stage)
        path = self.root / f"{job_id}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        preflight_sha256 = None
        preflight_receipt_sha256 = None
        if op.preflight_attestation_enabled(self.load()[0]["config"]):
            report, valid = op.preflight_artifact(
                self.run_dir,
                kind,
                path,
                job_id,
            )
            if not valid:
                raise AssertionError(report["validation"]["errors"])
            preflight_sha256 = report["validation"]["input_sha256"]
            preflight_receipt_sha256 = report["validation"][
                "preflight_receipt"
            ]["receipt_sha256"]
        op.start_job(self.run_dir, job_id, stage)
        return op.complete_job(
            self.run_dir,
            job_id,
            path,
            kind,
            preflight_sha256,
            preflight_receipt_sha256,
        )

    def store_portfolio_selection(
        self,
        candidates: list[dict],
        *,
        calibration_overrides: dict[str, dict[str, object]] | None = None,
        wildcard_ids: set[str] | None = None,
    ) -> dict:
        manifest, _ = self.load()
        overrides = calibration_overrides or {}
        discoveries = [
            candidate
            for _, candidate in op.latest_candidates_for_stage(
                self.run_dir, manifest, "discovery"
            )
        ]
        if wildcard_ids is None:
            wildcard_ids = (
                {
                    candidate["candidate_id"]
                    for candidate in candidates[
                        -manifest["config"]["wildcard_shortlist_slots"] :
                    ]
                }
                if len(candidates) == manifest["config"]["shortlist_max"]
                else set()
            )
        payload = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "selection_version": 1,
            "calibration": [
                {
                    "candidate_ref": self.candidate_ref(candidate),
                    "commercial_archetype": overrides.get(
                        candidate["candidate_id"], {}
                    ).get(
                        "commercial_archetype",
                        candidate["structure"]["commercial_archetype"],
                    ),
                    "control_point": overrides.get(
                        candidate["candidate_id"], {}
                    ).get(
                        "control_point", candidate["structure"]["control_point"]
                    ),
                    "critical_dependency": overrides.get(
                        candidate["candidate_id"], {}
                    ).get(
                        "critical_dependency",
                        candidate["structure"]["critical_dependency"],
                    ),
                    "control_point_acquisition_evidence": overrides.get(
                        candidate["candidate_id"], {}
                    ).get(
                        "control_point_acquisition_evidence",
                        self.control_point_acquisition_evidence(candidate),
                    ),
                }
                for candidate in discoveries
            ],
            "candidate_refs": [self.candidate_ref(candidate) for candidate in candidates],
            "wildcard_candidate_refs": [
                self.candidate_ref(candidate)
                for candidate in candidates
                if candidate["candidate_id"] in wildcard_ids
            ],
            "missing_archetypes": [],
            "rationale": "A bounded shortlist spanning materially different commercial structures.",
        }
        return self.complete_json_job(
            "portfolio-selection",
            "portfolio-selection",
            payload,
            stage="calibration",
        )

    def portfolio_decision(self, candidates: list[dict], develop_ids: set[str]) -> dict:
        return {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "candidate_decisions": [
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_version": candidate["version"],
                    "candidate_sha256": self.candidate_ref(candidate)["candidate_sha256"],
                    "disposition": "develop" if candidate["candidate_id"] in develop_ids else "not_selected",
                    "fatal_reason": None,
                    "fatal_claim_ids": [],
                    "rationale": "Selected by the deterministic working-score ranking."
                    if candidate["candidate_id"] in develop_ids
                    else "Outside the bounded deterministic development prefix.",
                }
                for candidate in candidates
            ],
        }

    def development_result(
        self,
        candidate: dict,
        *,
        constructor_id: str,
        outcome: str = "no_valid_redesign",
        base_candidate: dict | None = None,
    ) -> dict:
        result = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "candidate_id": candidate["candidate_id"],
            "outcome": outcome,
            "constructor_id": constructor_id,
            "rationale": "One bounded constructor pass found no defensible structural redesign."
            if outcome == "no_valid_redesign"
            else "One bounded constructor pass produced the recorded structural redesign.",
            "falsification": {
                key: [f"research-claim-{index + 1}"]
                for index, key in enumerate(sorted(op.FALSIFICATION_KEYS))
            },
        }
        if op.control_contract_enabled(self.load()[0]["config"]):
            result["structural_change"] = (
                {
                    "dependency_change": "Replaces the unbounded dependency with the recorded business-controlled workflow.",
                    "resulting_control_point_status": candidate[
                        "critical_control_point"
                    ]["status"],
                    "control_instrument": candidate["critical_control_point"][
                        "acquisition_instrument"
                    ],
                    "distribution_instrument": candidate["commercial_mechanics"][
                        "distribution_origin"
                    ],
                    "customer_relationship_owner": candidate[
                        "commercial_mechanics"
                    ]["customer_relationship_owner"],
                    "customer_relationship_control": candidate[
                        "critical_control_point"
                    ]["customer_relationship_control"],
                    "fully_loaded_economic_effects": candidate[
                        "commercial_mechanics"
                    ]["fully_loaded_economics"]["revenue_basis"],
                    "incumbent_response_defensibility": candidate[
                        "commercial_mechanics"
                    ]["bundling_resistance"],
                    "supporting_research_claim_ids": ["research-claim-4"],
                }
                if outcome == "redesigned"
                else None
            )
        return result

    def prepare_fatal_research_closure(self, candidate_id: str = "alpha") -> dict:
        discovery = self.candidate(candidate_id)
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        self.store_research(self.research(discovery))
        self.store_evaluation(
            self.evaluation_input(
                discovery,
                f"research-judge-{candidate_id}",
                score=6.5,
                evaluation_type="working_research",
            )
        )
        decision = self.portfolio_decision([discovery], set())
        decision["candidate_decisions"][0].update(
            {
                "disposition": "fatal",
                "fatal_reason": "impossible_conservative_economics",
                "fatal_claim_ids": ["research-claim-1"],
                "rationale": "Direct sourced evidence makes the conservative unit economics impossible.",
            }
        )
        self.complete_json_job("portfolio-decision", "portfolio-decision", decision)
        return discovery

    def evaluation_input(
        self,
        candidate: dict,
        judge_id: str,
        *,
        score: float = 9.0,
        evaluation_type: str = "holdout_native",
        factor_overrides: dict[str, float | None] | None = None,
        excluded: set[str] | None = None,
        adjustment: float = 0,
    ) -> dict:
        manifest, _ = self.load()
        candidate_path = self.run_dir / op.candidate_relpath(candidate["candidate_id"], candidate["version"])
        if evaluation_type == "working":
            evaluation_type = (
                "working_development"
                if (
                    self.run_dir
                    / "development"
                    / candidate["candidate_id"]
                    / "constructor-result.json"
                ).is_file()
                else "working_research"
            )
        overrides = factor_overrides or {}
        excluded_names = excluded or set()
        factors = []
        for row in manifest["rubric"]["factors"]:
            name = row["name"]
            is_excluded = name in excluded_names
            factors.append(
                {
                    "name": name,
                    "status": "excluded" if is_excluded else "scored",
                    "score": None if is_excluded else overrides.get(name, score),
                    "rationale": "Structurally irrelevant to this exact model." if is_excluded else f"Independent rationale for {name}.",
                }
            )
        evaluation = {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "judge_id": judge_id,
            "factors": factors,
            "interaction_adjustment": adjustment,
            "assumptions": ["Competent execution from the planning stage."],
            "main_structural_strength": f"Specific strength identified by {judge_id}.",
            "primary_score_limiter": f"Specific limiter identified by {judge_id}.",
            "strongest_disconfirming_evidence": f"Disconfirming evidence identified by {judge_id}.",
            "highest_value_structural_change": f"Structural change proposed by {judge_id}.",
            "evidence_needed_for_higher_score": f"Evidence request from {judge_id}.",
            "_test_evaluation_type": evaluation_type,
        }
        return evaluation

    def store_evaluation(self, evaluation_input: dict) -> tuple[Path, dict]:
        manifest, _ = self.load()
        response = copy.deepcopy(evaluation_input)
        evaluation_type = response.pop("_test_evaluation_type")
        canonical = op.canonicalize_evaluator_response(
            response, manifest, self.run_dir, evaluation_type
        )
        path = self.run_dir / op.evaluation_relpath(
            canonical["candidate_id"],
            canonical["candidate_version"],
            canonical["evaluation_type"],
            canonical["judge_id"],
        )
        op.write_immutable(path, op.canonical_json_bytes(canonical))
        return path, canonical

    def ensure_direct_portfolio_contracts(self) -> None:
        manifest, _ = self.load()
        selection_path = self.run_dir / "portfolio/selection.json"
        discoveries = [candidate for _, candidate in op.latest_candidates_for_stage(self.run_dir, manifest, "discovery")]
        if not selection_path.exists():
            selection = {
                "schema_version": op.ACTIVE_SCHEMA_VERSION,
                "selection_version": 1,
                "calibration": [
                    {
                        "candidate_ref": self.candidate_ref(candidate),
                        "commercial_archetype": candidate["structure"]["commercial_archetype"],
                        "control_point": candidate["structure"]["control_point"],
                        "critical_dependency": candidate["structure"]["critical_dependency"],
                        "control_point_acquisition_evidence": self.control_point_acquisition_evidence(
                            candidate
                        ),
                    }
                    for candidate in discoveries
                ],
                "candidate_refs": [self.candidate_ref(candidate) for candidate in discoveries],
                "wildcard_candidate_refs": [
                    self.candidate_ref(candidate)
                    for candidate in discoveries[
                        -manifest["config"]["wildcard_shortlist_slots"] :
                    ]
                ]
                if len(discoveries) == manifest["config"]["shortlist_max"]
                else [],
                "missing_archetypes": [],
                "rationale": "Canonical test shortlist covering every direct-lineage fixture candidate.",
            }
            canonical_selection = op.validate_portfolio_selection(selection, manifest, self.run_dir)
            op.write_immutable(selection_path, op.canonical_json_bytes(canonical_selection))
        decision_path = self.run_dir / "portfolio/development-decision.json"
        if not decision_path.exists():
            researched = [
                op.validate_candidate(
                    op.load_json(
                        self.run_dir
                        / op.candidate_relpath(
                            research["candidate_id"], research["candidate_version"]
                        )
                    ),
                    manifest,
                    self.run_dir,
                )
                for _, research in op.iter_research(self.run_dir, manifest)
            ]
            develop_ids = {candidate["candidate_id"] for candidate in researched}
            decision = self.portfolio_decision(researched, develop_ids)
            canonical_decision = op.validate_portfolio_decision(decision, manifest, self.run_dir)
            op.write_immutable(decision_path, op.canonical_json_bytes(canonical_decision))

    def store_complete_lineage(
        self,
        candidate_id: str = "alpha",
        *,
        capital: object = 100000,
    ) -> dict:
        discovery = self.candidate(candidate_id, stage="discovery", version=1, capital=capital)
        self.store_candidate(discovery)
        manifest, _ = self.load()
        selection = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "selection_version": 1,
            "calibration": [
                {
                    "candidate_ref": self.candidate_ref(discovery),
                    "commercial_archetype": discovery["structure"]["commercial_archetype"],
                    "control_point": discovery["structure"]["control_point"],
                    "critical_dependency": discovery["structure"]["critical_dependency"],
                    "control_point_acquisition_evidence": self.control_point_acquisition_evidence(
                        discovery
                    ),
                }
            ],
            "candidate_refs": [self.candidate_ref(discovery)],
            "wildcard_candidate_refs": [],
            "missing_archetypes": [],
            "rationale": "One exact candidate for a complete lineage fixture.",
        }
        canonical_selection = op.validate_portfolio_selection(
            selection, manifest, self.run_dir
        )
        op.write_immutable(
            self.run_dir / "portfolio/selection.json",
            op.canonical_json_bytes(canonical_selection),
        )
        self.store_research(self.research(discovery))
        self.store_evaluation(
            self.evaluation_input(
                discovery,
                f"working-research-{candidate_id}",
                score=7.8,
                evaluation_type="working_research",
            )
        )
        decision = self.portfolio_decision([discovery], {candidate_id})
        canonical_decision = op.validate_portfolio_decision(
            decision, manifest, self.run_dir
        )
        op.write_immutable(
            self.run_dir / "portfolio/development-decision.json",
            op.canonical_json_bytes(canonical_decision),
        )
        result = self.development_result(
            discovery,
            constructor_id=f"constructor-{candidate_id}",
        )
        canonical_result = op.canonicalize_development_response(
            result, manifest, self.run_dir
        )
        op.write_immutable(
            self.run_dir / f"development/{candidate_id}/constructor-result.json",
            op.canonical_json_bytes(canonical_result),
        )
        self.store_evaluation(
            self.evaluation_input(
                discovery,
                f"working-{candidate_id}",
                score=8,
                evaluation_type="working_development",
            )
        )
        finalists = op.build_finalist_selection(self.run_dir, manifest)
        op.write_immutable(
            self.run_dir / "portfolio/finalists.json",
            op.canonical_json_bytes(finalists),
        )
        return discovery

    def external_response(self, manifest: dict, *, judge_id: str, score: float) -> dict:
        _, candidate = op.finalist_candidates(self.run_dir, manifest)[0]
        return {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "judge_id": judge_id,
            "factors": [
                {
                    "name": row["name"],
                    "status": "scored",
                    "score": score,
                    "rationale": f"External rationale for {row['name']}.",
                }
                for row in manifest["rubric"]["factors"]
            ],
            "interaction_adjustment": 0,
            "assumptions": ["Planning-stage execution is competent."],
            "main_structural_strength": "External structural strength.",
            "primary_score_limiter": "External binding limiter.",
            "strongest_disconfirming_evidence": "External contrary evidence.",
            "highest_value_structural_change": "External structural change.",
            "evidence_needed_for_higher_score": "External evidence request.",
        }


class RunAndStateTests(OpportunityTestCase):
    def test_new_run_snapshots_sources_rubric_and_event(self) -> None:
        manifest, state = self.load()
        self.assertEqual(state["stage"], "initialized")
        self.assertEqual(
            set(manifest["source_hashes"]),
            {"PERSONALITY_SITUATION.md", "Personalities/ZeroToOne.txt", "config/opportunity-workflow.json"},
        )
        self.assertEqual((self.run_dir / "inputs/founder.md").read_bytes(), (op.REPO_ROOT / "PERSONALITY_SITUATION.md").read_bytes())
        self.assertEqual((self.run_dir / "inputs/evaluator.txt").read_bytes(), (op.REPO_ROOT / "Personalities/ZeroToOne.txt").read_bytes())
        self.assertEqual(
            (self.run_dir / "inputs/config.json").read_bytes(),
            op.canonical_json_bytes(op.validate_config(op.load_json(self.config_path))),
        )
        self.assertEqual(sum(row["weight"] for row in manifest["rubric"]["factors"]), 100)
        events = op.load_events(self.run_dir / "events.jsonl", self.run_id)
        self.assertEqual([event["event"] for event in events], ["run_created"])
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_config_source_drift_uses_canonical_json_semantics(self) -> None:
        config = op.validate_config(op.load_json(self.config_path))
        reordered = {key: config[key] for key in reversed(list(config))}
        reordered_path = self.root / "reordered-config.json"
        reordered_path.write_text(
            json.dumps(reordered, separators=(",", ":")), encoding="utf-8"
        )
        checked = op.check_run(self.run_dir, reordered_path)
        self.assertNotIn("config/opportunity-workflow.json", checked["source_drift"])

        changed = copy.deepcopy(reordered)
        changed["seeds_per_scout"] += 1
        changed_path = self.root / "changed-config.json"
        changed_path.write_text(json.dumps(changed), encoding="utf-8")
        drifted = op.check_run(self.run_dir, changed_path)
        self.assertIn("config/opportunity-workflow.json", drifted["source_drift"])

    def test_resume_retries_and_exhausted_failure_no_longer_blocks(self) -> None:
        op.advance_run(self.run_dir)
        first = op.start_job(self.run_dir, "scout-a", None)
        self.assertEqual(first["attempts"], 1)
        resumed = op.resume_run(self.run_dir)
        self.assertEqual(resumed["eligible_jobs"][0]["status"], "interrupted")
        second = op.start_job(self.run_dir, "scout-a", "discovery")
        self.assertEqual(second["attempts"], 2)
        failed = op.fail_job(self.run_dir, "scout-a", "provider process ended")
        self.assertFalse(failed["retryable"])
        _, state = self.load()
        self.assertNotIn("scout-a", op.current_stage_blockers(state))
        with self.assertRaises(op.ConflictError):
            op.start_job(self.run_dir, "scout-a", None)
        names = [event["event"] for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)]
        self.assertEqual(names.count("job_started"), 2)
        self.assertIn("run_resumed", names)
        self.assertIn("job_failed", names)

    def test_job_append_failures_leave_state_clean_and_retryable(self) -> None:
        op.advance_run(self.run_dir)
        with mock.patch.object(op, "append_event", side_effect=OSError("start event failed")):
            with self.assertRaisesRegex(OSError, "start event failed"):
                op.start_job(self.run_dir, "atomic", None)
        self.assertNotIn("atomic", self.load()[1]["jobs"]["discovery"])
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

        op.start_job(self.run_dir, "atomic", None)
        with mock.patch.object(op, "append_event", side_effect=OSError("fail event failed")):
            with self.assertRaisesRegex(OSError, "fail event failed"):
                op.fail_job(self.run_dir, "atomic", "mechanical failure")
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["atomic"]["status"], "running")
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])
        op.fail_job(self.run_dir, "atomic", "mechanical failure")

        op.start_job(self.run_dir, "resume-atomic", None)
        with mock.patch.object(op, "append_event", side_effect=OSError("resume event failed")):
            with self.assertRaisesRegex(OSError, "resume event failed"):
                op.resume_run(self.run_dir)
        self.assertEqual(
            self.load()[1]["jobs"]["discovery"]["resume-atomic"]["status"],
            "running",
        )
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])
        resumed = op.resume_run(self.run_dir)
        self.assertEqual(
            resumed["interrupted"],
            [{"stage": "discovery", "job_id": "resume-atomic"}],
        )

    def test_event_first_job_state_failures_reconcile_idempotently(self) -> None:
        op.advance_run(self.run_dir)
        with mock.patch.object(op, "save_state", side_effect=OSError("start state failed")):
            with self.assertRaisesRegex(OSError, "start state failed"):
                op.start_job(self.run_dir, "recover-start", None)
        self.assertNotIn("recover-start", self.load()[1]["jobs"]["discovery"])
        with self.assertRaisesRegex(op.InputError, "job lifecycle disagrees"):
            op.check_run(self.run_dir, self.config_path)
        recovered_start = op.start_job(self.run_dir, "recover-start", None)
        self.assertTrue(recovered_start["idempotent"])
        self.assertEqual(recovered_start["attempts"], 1)

        with mock.patch.object(op, "save_state", side_effect=OSError("fail state failed")):
            with self.assertRaisesRegex(OSError, "fail state failed"):
                op.fail_job(self.run_dir, "recover-start", "bounded failure")
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["recover-start"]["status"], "running")
        with self.assertRaisesRegex(op.InputError, "job lifecycle disagrees"):
            op.check_run(self.run_dir, self.config_path)
        recovered_fail = op.fail_job(self.run_dir, "recover-start", "bounded failure")
        self.assertTrue(recovered_fail["idempotent"])
        self.assertEqual(recovered_fail["status"], "failed")

        op.start_job(self.run_dir, "recover-resume", None)
        with mock.patch.object(op, "save_state", side_effect=OSError("resume state failed")):
            with self.assertRaisesRegex(OSError, "resume state failed"):
                op.resume_run(self.run_dir)
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["recover-resume"]["status"], "running")
        recovered_resume = op.resume_run(self.run_dir)
        self.assertTrue(recovered_resume["idempotent"])
        self.assertEqual(
            recovered_resume["interrupted"],
            [{"stage": "discovery", "job_id": "recover-resume"}],
        )
        events = op.load_events(self.run_dir / "events.jsonl", self.run_id)
        self.assertEqual(
            len([item for item in events if item["event"] == "job_started" and item["job_id"] == "recover-start"]),
            1,
        )
        self.assertEqual(
            len([item for item in events if item["event"] == "job_failed" and item["job_id"] == "recover-start"]),
            1,
        )
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_job_commands_reconcile_when_append_raises_after_durable_write(self) -> None:
        op.advance_run(self.run_dir)
        real_append = op.append_event

        def durable_then_raise(*args, **kwargs):
            real_append(*args, **kwargs)
            raise OSError("raised after durable event write")

        with mock.patch.object(op, "append_event", side_effect=durable_then_raise):
            with self.assertRaisesRegex(OSError, "after durable event"):
                op.start_job(self.run_dir, "durable-start", None)
        self.assertNotIn("durable-start", self.load()[1]["jobs"]["discovery"])
        self.assertTrue(op.start_job(self.run_dir, "durable-start", None)["idempotent"])

        with mock.patch.object(op, "append_event", side_effect=durable_then_raise):
            with self.assertRaisesRegex(OSError, "after durable event"):
                op.fail_job(self.run_dir, "durable-start", "durable failure")
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["durable-start"]["status"], "running")
        self.assertTrue(op.fail_job(self.run_dir, "durable-start", "durable failure")["idempotent"])

        op.start_job(self.run_dir, "durable-resume", None)
        with mock.patch.object(op, "append_event", side_effect=durable_then_raise):
            with self.assertRaisesRegex(OSError, "after durable event"):
                op.resume_run(self.run_dir)
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["durable-resume"]["status"], "running")
        recovered = op.resume_run(self.run_dir)
        self.assertTrue(recovered["idempotent"])
        self.assertEqual(
            recovered["interrupted"],
            [{"stage": "discovery", "job_id": "durable-resume"}],
        )
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_check_detects_missing_and_tampered_job_events(self) -> None:
        op.advance_run(self.run_dir)
        payload = self.root / "payload.txt"
        payload.write_text("auditable output", encoding="utf-8")
        op.start_job(self.run_dir, "audited", None)
        op.complete_job(self.run_dir, "audited", payload, "generic")
        events_path = self.run_dir / "events.jsonl"
        original = events_path.read_bytes()
        records = events_path.read_text(encoding="utf-8").splitlines()
        events_path.write_text("\n".join(records[:-1]) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "job lifecycle disagrees"):
            op.check_run(self.run_dir, self.config_path)
        events_path.write_bytes(original)

        records = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        started = next(item for item in records if item["event"] == "job_started")
        started["details"]["attempt"] = 2
        events_path.write_text(
            "".join(json.dumps(item, sort_keys=True) + "\n" for item in records),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(op.InputError, "attempt is not consecutive"):
            op.check_run(self.run_dir, self.config_path)

    def test_candidate_job_completion_is_canonical_and_idempotent(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate()
        input_path = self.root / "candidate.json"
        input_path.write_text(json.dumps(candidate), encoding="utf-8")
        op.start_job(self.run_dir, "candidate-alpha", None)
        first = op.complete_job(self.run_dir, "candidate-alpha", input_path, "candidate")
        self.assertEqual(first["artifact"], "candidates/alpha/v1.json")
        second = op.complete_job(self.run_dir, "candidate-alpha", input_path, "candidate")
        self.assertTrue(second["idempotent"])
        changed = copy.deepcopy(candidate)
        changed["thesis"] = "Different immutable content."
        input_path.write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaises(op.ConflictError):
            op.complete_job(self.run_dir, "candidate-alpha", input_path, "candidate")

    def test_artifact_first_interruption_recovers_without_overwrite(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate()
        input_path = self.root / "candidate.json"
        input_path.write_text(json.dumps(candidate), encoding="utf-8")
        op.start_job(self.run_dir, "artifact-first", None)
        real_save = op.save_state
        with mock.patch.object(op, "save_state", side_effect=RuntimeError("fault after artifact write")):
            with self.assertRaisesRegex(RuntimeError, "fault after artifact"):
                op.complete_job(self.run_dir, "artifact-first", input_path, "candidate")
        artifact = self.run_dir / "candidates/alpha/v1.json"
        self.assertTrue(artifact.is_file())
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["artifact-first"]["status"], "running")
        op.resume_run(self.run_dir)
        op.start_job(self.run_dir, "artifact-first", None)
        completed = op.complete_job(self.run_dir, "artifact-first", input_path, "candidate")
        self.assertEqual(completed["artifact_sha256"], op.sha256_file(artifact))
        self.assertIs(op.save_state, real_save)

    def test_artifact_write_failure_leaves_running_job_resumable(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate()
        input_path = self.root / "candidate.json"
        input_path.write_text(json.dumps(candidate), encoding="utf-8")
        op.start_job(self.run_dir, "write-failure", None)
        artifact = self.run_dir / "candidates/alpha/v1.json"
        with mock.patch.object(op, "write_immutable", side_effect=OSError("simulated disk failure")):
            with self.assertRaisesRegex(OSError, "simulated disk failure"):
                op.complete_job(self.run_dir, "write-failure", input_path, "candidate")
        self.assertFalse(artifact.exists())
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["write-failure"]["status"], "running")
        resumed = op.resume_run(self.run_dir)
        self.assertEqual(resumed["interrupted"], [{"stage": "discovery", "job_id": "write-failure"}])
        op.start_job(self.run_dir, "write-failure", None)
        completed = op.complete_job(self.run_dir, "write-failure", input_path, "candidate")
        self.assertEqual(completed["status"], "completed")
        self.assertTrue(artifact.is_file())

    def test_event_failure_after_state_commit_replays_without_artifact_rewrite(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate()
        input_path = self.root / "candidate.json"
        input_path.write_text(json.dumps(candidate), encoding="utf-8")
        op.start_job(self.run_dir, "event-failure", None)
        with mock.patch.object(op, "append_event", side_effect=OSError("simulated event failure")):
            with self.assertRaisesRegex(OSError, "simulated event failure"):
                op.complete_job(self.run_dir, "event-failure", input_path, "candidate")
        artifact = self.run_dir / "candidates/alpha/v1.json"
        artifact_hash = op.sha256_file(artifact)
        artifact_mtime = artifact.stat().st_mtime_ns
        job = self.load()[1]["jobs"]["discovery"]["event-failure"]
        self.assertEqual(job["status"], "completed")
        self.assertFalse(
            any(
                event["event"] == "job_completed" and event["job_id"] == "event-failure"
                for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            )
        )
        replay = op.complete_job(self.run_dir, "event-failure", input_path, "candidate")
        self.assertTrue(replay["idempotent"])
        self.assertEqual(op.sha256_file(artifact), artifact_hash)
        self.assertEqual(artifact.stat().st_mtime_ns, artifact_mtime)
        completion_events = [
            event
            for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            if event["event"] == "job_completed" and event["job_id"] == "event-failure"
        ]
        self.assertEqual(len(completion_events), 1)
        self.assertTrue(completion_events[0]["details"]["recovered_after_state_commit"])

    def test_advance_event_failure_does_not_commit_and_retry_is_single_transition(self) -> None:
        with mock.patch.object(op, "append_event", side_effect=OSError("simulated event failure")):
            with self.assertRaisesRegex(OSError, "simulated event failure"):
                op.advance_run(self.run_dir)
        self.assertEqual(self.load()[1]["stage"], "initialized")
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])
        replay = op.advance_run(self.run_dir)
        self.assertEqual(replay["stage"], "discovery")
        events = op.load_events(self.run_dir / "events.jsonl", self.run_id)
        self.assertEqual([event["event"] for event in events].count("stage_advanced"), 1)

    def test_advance_state_failure_after_event_is_reconciled_idempotently(self) -> None:
        with mock.patch.object(op, "save_state", side_effect=OSError("simulated state failure")):
            with self.assertRaisesRegex(OSError, "simulated state failure"):
                op.advance_run(self.run_dir)
        self.assertEqual(self.load()[1]["stage"], "initialized")
        with self.assertRaisesRegex(op.InputError, "lifecycle disagrees"):
            op.check_run(self.run_dir, self.config_path)
        recovered = op.advance_run(self.run_dir)
        self.assertTrue(recovered["idempotent"])
        self.assertEqual(recovered["stage"], "discovery")
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_finalize_event_failure_leaves_visible_recoverable_artifacts(self) -> None:
        self.prepare_fatal_research_closure()
        with mock.patch.object(op, "append_event", side_effect=OSError("simulated final event failure")):
            with self.assertRaisesRegex(OSError, "simulated final event failure"):
                op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertEqual(self.load()[1]["stage"], "research")
        self.assertTrue((self.run_dir / "final/report.json").is_file())
        with self.assertRaisesRegex(op.InputError, "unreconciled finalization artifacts"):
            op.check_run(self.run_dir, self.config_path)
        report, code = op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertTrue(report["idempotent"] is False)
        self.assertEqual(code, 4)
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_finalize_state_failure_after_event_is_reconciled(self) -> None:
        self.prepare_fatal_research_closure()
        original_save_state = op.save_state
        with mock.patch.object(op, "save_state", side_effect=OSError("simulated final state failure")):
            with self.assertRaisesRegex(OSError, "simulated final state failure"):
                op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertEqual(self.load()[1]["stage"], "research")
        with self.assertRaisesRegex(op.InputError, "lifecycle disagrees"):
            op.check_run(self.run_dir, self.config_path)
        with mock.patch.object(op, "save_state", wraps=original_save_state):
            report, code = op.finalize_run(
                self.run_dir, "No viable researched candidate remained"
            )
        self.assertTrue(report["idempotent"])
        self.assertEqual(code, 4)
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

    def test_candidate_completion_rejects_symlinked_artifact_parent(self) -> None:
        op.advance_run(self.run_dir)
        outside = self.root / "outside"
        outside.mkdir()
        (self.run_dir / "candidates").mkdir()
        (self.run_dir / "candidates/alpha").symlink_to(outside, target_is_directory=True)
        input_path = self.root / "candidate.json"
        input_path.write_text(json.dumps(self.candidate()), encoding="utf-8")
        op.start_job(self.run_dir, "symlink-attempt", None)
        with self.assertRaisesRegex(op.InputError, "symlink component"):
            op.complete_job(self.run_dir, "symlink-attempt", input_path, "candidate")
        self.assertFalse((outside / "v1.json").exists())

    def test_exhausted_failure_does_not_block_independent_completed_work(self) -> None:
        discovery = self.candidate()
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        self.store_research(self.research(discovery))
        self.store_evaluation(
            self.evaluation_input(
                discovery,
                "research-judge-alpha",
                score=8,
                evaluation_type="working_research",
            )
        )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision([discovery], {"alpha"}),
        )
        op.advance_run(self.run_dir)
        self.complete_json_job(
            "constructor-alpha",
            "development-result",
            self.development_result(
                discovery,
                constructor_id="constructor-agent-alpha",
            ),
        )
        self.store_evaluation(
            self.evaluation_input(
                discovery,
                "development-judge-alpha",
                score=8,
                evaluation_type="working_development",
            )
        )
        good = self.root / "good.md"
        good.write_text("independent completed evidence", encoding="utf-8")
        op.start_job(self.run_dir, "good-candidate", None)
        op.complete_job(self.run_dir, "good-candidate", good, "generic")
        op.start_job(self.run_dir, "failed-candidate", None)
        op.fail_job(self.run_dir, "failed-candidate", "attempt one")
        op.start_job(self.run_dir, "failed-candidate", None)
        op.fail_job(self.run_dir, "failed-candidate", "attempt two")
        advanced = op.advance_run(self.run_dir)
        self.assertEqual(advanced["stage"], "frozen")

    def test_no_finalist_closes_and_publishes_idempotently(self) -> None:
        candidate = self.prepare_fatal_research_closure()
        report, code = op.finalize_run(self.run_dir, "Bounded discovery produced no viable shortlist")
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "no_finalist")
        self.assertEqual(report["strongest_candidates"][0]["candidate_id"], "alpha")
        self.assertEqual(report["selected_candidate_id"], "alpha")
        self.assertEqual(report["selected_candidate_version"], 1)
        self.assertEqual(
            report["binding_limiters"][0],
            "Bounded discovery produced no viable shortlist",
        )
        self.assertIn("Specific limiter identified by research-judge-alpha.", report["binding_limiters"])
        self.assertTrue(report["strongest_candidates"][0]["is_selected"])
        self.assertTrue(report["strongest_candidates"][0]["contrary_evidence"])
        self.assertIn("Reopen only with new evidence", report["strongest_candidates"][0]["reopen_condition"])
        self.assertIsNone(report["qualification_label"])
        markdown = (self.run_dir / "report.md").read_text(encoding="utf-8")
        self.assertIn("No candidate reached held-out evaluation", markdown)
        self.assertIn("N/A, not zero", markdown)
        self.assertNotIn("A score-qualified result passed", markdown)
        knowledge = self.root / "knowledge"
        knowledge.mkdir()
        baseline_meta = {
            "record_type": "index_meta",
            "verification": {
                "non_meta_rows": 0,
                "opportunity_outcome_corrections": 0,
                "opportunity_outcomes": 0,
                "opportunity_outcome_quarantines": 0,
                "total_rows_including_meta": 1,
            },
        }
        (knowledge / "history_index.jsonl").write_text(
            json.dumps(baseline_meta, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        first = op.publish_run(self.run_dir, self.root / "outcomes", knowledge)
        second = op.publish_run(self.run_dir, self.root / "outcomes", knowledge)
        self.assertFalse(first["idempotent"])
        self.assertTrue(second["idempotent"])
        self.assertTrue((self.root / "outcomes" / self.run_id / "report.md").is_file())
        outcome_dir = self.root / "outcomes" / self.run_id
        self.assertTrue((outcome_dir / "candidates/alpha/v1.json").is_file())
        self.assertTrue((outcome_dir / "research/alpha/v1.json").is_file())
        self.assertTrue((outcome_dir / "learning-digest.jsonl").is_file())
        history = (knowledge / "history_index.jsonl").read_text().splitlines()
        self.assertEqual(len(history), 2)
        meta = json.loads(history[0])
        self.assertEqual(
            meta["verification"],
            {
                "non_meta_rows": 1,
                "opportunity_outcome_corrections": 0,
                "opportunity_outcomes": 1,
                "opportunity_outcome_quarantines": 0,
                "total_rows_including_meta": 2,
            },
        )
        entry = json.loads(history[1])
        self.assertEqual(
            history[1],
            json.dumps(
                entry,
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        )
        self.assertEqual(entry["record_type"], "opportunity_outcome_v2")
        self.assertEqual(entry["score_scale"], "/10")
        self.assertIsNone(entry["qualification_label"])
        self.assertEqual(entry["selected_candidate_id"], "alpha")
        self.assertEqual(entry["selected_title"], candidate["title"])
        self.assertEqual(entry["selected_fingerprint"], candidate["fingerprint"])
        self.assertEqual(entry["source_candidate_path"], "candidates/alpha/v1.json")
        self.assertEqual(entry["terminal_objection"], "Bounded discovery produced no viable shortlist")
        self.assertIn("Reopen only with new evidence", entry["reopen_condition"])
        learning_rows = [
            json.loads(line)
            for line in (outcome_dir / "learning-digest.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(len(learning_rows), 1)
        self.assertEqual(learning_rows[0]["candidate_id"], "alpha")
        self.assertEqual(entry["learning_row_count"], 1)
        self.assertEqual(entry["learning_digest_path"], f"outcomes/{self.run_id}/learning-digest.jsonl")
        self.assertEqual(entry["learning_digest_sha256"], op.sha256_file(outcome_dir / "learning-digest.jsonl"))

    def test_published_outcome_quarantine_is_immutable_auditable_and_idempotent(self) -> None:
        self.prepare_fatal_research_closure()
        report, code = op.finalize_run(
            self.run_dir, "Bounded discovery produced no viable shortlist"
        )
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "no_finalist")
        knowledge = self.root / "knowledge"
        knowledge.mkdir()
        baseline_meta = {
            "record_type": "index_meta",
            "verification": {
                "non_meta_rows": 0,
                "opportunity_outcome_corrections": 0,
                "opportunity_outcome_quarantines": 0,
                "opportunity_outcomes": 0,
                "total_rows_including_meta": 1,
            },
        }
        history_path = knowledge / "history_index.jsonl"
        history_path.write_text(
            json.dumps(baseline_meta, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        outcomes = self.root / "outcomes"
        op.publish_run(self.run_dir, outcomes, knowledge)
        outcome_dir = outcomes / self.run_id
        original_report = (outcome_dir / "report.json").read_bytes()
        original_history_row = history_path.read_text(encoding="utf-8").splitlines()[1]
        reason = (
            "A required evaluator context boundary was violated; retain this run only "
            "as workflow acceptance evidence."
        )

        cli_args = [
            "--runs-dir",
            str(self.runs_dir),
            "quarantine-outcome",
            self.run_id,
            "--reason-code",
            "procedural_context_violation",
            "--reason",
            reason,
        ]
        first_code, first, first_error = self.run_cli(cli_args)
        self.assertEqual((first_code, first_error), (0, {}))
        self.assertFalse(first["idempotent"])
        second_code, second, second_error = self.run_cli(cli_args)
        self.assertEqual((second_code, second_error), (0, {}))
        self.assertTrue(second["idempotent"])
        self.assertEqual(first["quarantine_sha256"], second["quarantine_sha256"])

        sidecar_path = outcome_dir / "quarantine.json"
        sidecar_bytes = sidecar_path.read_bytes()
        sidecar = json.loads(sidecar_bytes)
        self.assertEqual(sidecar_bytes, op.canonical_json_bytes(sidecar))
        self.assertFalse(sidecar["business_decision_eligible"])
        self.assertEqual(sidecar["permitted_use"], "workflow_test_evidence_only")
        self.assertEqual(sidecar["report_sha256"], op.sha256_file(outcome_dir / "report.json"))
        history_rows = [
            json.loads(line)
            for line in history_path.read_text(encoding="utf-8").splitlines()
        ]
        quarantines = [
            row
            for row in history_rows
            if row.get("record_type") == "opportunity_outcome_quarantine_v1"
        ]
        self.assertEqual(len(quarantines), 1)
        self.assertEqual(quarantines[0]["quarantine_sha256"], op.sha256_file(sidecar_path))
        self.assertEqual(history_rows[0]["verification"]["opportunity_outcome_quarantines"], 1)
        self.assertEqual(history_rows[1], json.loads(original_history_row))
        self.assertEqual((outcome_dir / "report.json").read_bytes(), original_report)
        validated = op.validate_published_outcomes(outcomes, history_path)
        self.assertEqual(validated["quarantined_run_count"], 1)

        with self.assertRaisesRegex(op.ConflictError, "different reason"):
            op.quarantine_published_outcome(
                self.run_id,
                outcomes,
                knowledge,
                "acceptance_test_only",
                "Different reason.",
            )
        tampered = {**sidecar, "reason": "Tampered reason."}
        sidecar_path.write_bytes(op.canonical_json_bytes(tampered))
        try:
            with self.assertRaisesRegex(op.InputError, "differs from its history"):
                op.validate_published_outcomes(outcomes, history_path)
        finally:
            sidecar_path.write_bytes(sidecar_bytes)

    def test_no_finalist_best_candidate_is_deterministic_for_multiple_candidates(self) -> None:
        discoveries = [self.candidate("alpha"), self.candidate("beta")]
        for discovery in discoveries:
            self.store_candidate(discovery)
        self.store_portfolio_selection(discoveries)
        self.set_stage("research")
        researched = []
        for discovery, score in zip(discoveries, (7.0, 8.0), strict=True):
            candidate = discovery
            self.store_research(self.research(candidate))
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"research-judge-{candidate['candidate_id']}",
                    score=score,
                    evaluation_type="working_research",
                )
            )
            researched.append(candidate)
        decision = self.portfolio_decision(researched, set())
        for row in decision["candidate_decisions"]:
            row.update(
                {
                    "disposition": "fatal",
                    "fatal_reason": "impossible_conservative_economics",
                    "fatal_claim_ids": ["research-claim-1"],
                    "rationale": "Direct sourced evidence makes the conservative unit economics impossible.",
                }
            )
        self.complete_json_job("portfolio-decision", "portfolio-decision", decision)
        with self.assertRaisesRegex(op.InputError, "must match the deterministic highest"):
            op.finalize_run(self.run_dir, "No researched candidate can work", "alpha")
        report, code = op.finalize_run(self.run_dir, "No researched candidate can work")
        self.assertEqual(code, 4)
        self.assertEqual(report["selected_candidate_id"], "beta")
        self.assertEqual(report["strongest_candidates"][0]["candidate_id"], "beta")


class ValidationAndScoringTests(OpportunityTestCase):
    def test_rubric_parser_rejects_missing_section_and_wrong_weight_total(self) -> None:
        missing = self.root / "missing-rubric.txt"
        missing.write_text("No scoring section here.", encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "weight section was not found"):
            op.parse_rubric(missing)
        wrong_total = self.root / "wrong-total.txt"
        text = (op.REPO_ROOT / "Personalities/ZeroToOne.txt").read_text(encoding="utf-8")
        wrong_total.write_text(text.replace("Execution and risks: 4%", "Execution and risks: 3%"), encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "sum to 100"):
            op.parse_rubric(wrong_total)

    def _canonical_response(
        self,
        candidate: dict,
        judge_id: str,
        *,
        score: float = 9.0,
        evaluation_type: str = "working_research",
        excluded: set[str] | None = None,
        adjustment: float = 0,
    ) -> dict:
        response = self.evaluation_input(
            candidate,
            judge_id,
            score=score,
            evaluation_type=evaluation_type,
            excluded=excluded,
            adjustment=adjustment,
        )
        response.pop("_test_evaluation_type")
        return op.canonicalize_evaluator_response(
            response,
            self.load()[0],
            self.run_dir,
            evaluation_type,
        )

    def test_candidate_and_research_shapes_are_strict(self) -> None:
        manifest, _ = self.load()
        candidate = self.candidate()
        self.store_candidate(candidate)

        extra = copy.deepcopy(candidate)
        extra["unexpected"] = True
        with self.assertRaisesRegex(op.InputError, "candidate keys differ"):
            op.validate_candidate(extra, manifest, self.run_dir)

        nonnumeric_capital = copy.deepcopy(candidate)
        nonnumeric_capital["economics"]["capital_required_pln"] = "50,000 PLN"
        with self.assertRaisesRegex(op.InputError, "must be a JSON number"):
            op.validate_candidate(nonnumeric_capital, manifest, self.run_dir)

        research = self.research(candidate)
        research["sources"] = research["sources"][:1]
        with self.assertRaisesRegex(op.InputError, "sources count must be between"):
            op.validate_research(research, manifest, self.run_dir)

    def test_scalar_founder_fit_is_a_visible_retryable_candidate_failure(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate()
        candidate["founder_fit"] = "AI-assisted research"
        path = self.root / "scalar-founder-fit.json"
        path.write_text(json.dumps(candidate), encoding="utf-8")
        op.start_job(self.run_dir, "scout-alpha", "discovery")
        with self.assertRaisesRegex(op.InputError, "candidate.founder_fit must be a list"):
            op.complete_job(self.run_dir, "scout-alpha", path, "candidate")
        failed = self.load()[1]["jobs"]["discovery"]["scout-alpha"]
        self.assertEqual(failed["status"], "failed")
        self.assertTrue(op.job_is_retryable(failed))
        self.assertIn("mechanical candidate output failure", failed["error"])

        candidate["founder_fit"] = ["AI-assisted research"]
        path.write_text(json.dumps(candidate), encoding="utf-8")
        self.assertEqual(
            op.start_job(self.run_dir, "scout-alpha", "discovery")["attempts"],
            2,
        )
        completed = op.complete_job(
            self.run_dir, "scout-alpha", path, "candidate"
        )
        self.assertEqual(completed["status"], "completed")

    def test_core_readiness_and_asymmetric_wildcard_quota_are_enforced(self) -> None:
        count = self.load()[0]["config"]["shortlist_max"]
        candidates = [self.candidate(f"candidate-{index + 1}") for index in range(count)]
        candidates[0]["claims"][2]["evidence_refs"] = []
        for candidate in candidates:
            self.store_candidate(candidate)

        calibration_overrides = {
            candidates[0]["candidate_id"]: {
                "control_point_acquisition_evidence": None,
            }
        }

        with self.assertRaisesRegex(op.InputError, "not ready for a core shortlist slot"):
            self.store_portfolio_selection(
                candidates, calibration_overrides=calibration_overrides
            )
        op.fail_job(
            self.run_dir,
            "portfolio-selection",
            "under-evidenced candidate was correctly rejected from a core slot",
        )
        wildcard_ids = {
            candidates[0]["candidate_id"],
            candidates[-1]["candidate_id"],
        }
        self.store_portfolio_selection(
            candidates,
            wildcard_ids=wildcard_ids,
            calibration_overrides=calibration_overrides,
        )
        report = op._portfolio_report(self.run_dir, self.load()[0])
        self.assertIsNotNone(report)
        slots = report["shortlist_slots"]
        self.assertEqual(
            sum(slot["slot_type"] == "core" for slot in slots),
            self.load()[0]["config"]["core_shortlist_slots"],
        )
        self.assertEqual(
            sum(slot["slot_type"] == "wildcard" for slot in slots),
            self.load()[0]["config"]["wildcard_shortlist_slots"],
        )
        stored = op.load_json(self.run_dir / "portfolio/selection.json")
        under_evidenced = next(
            row
            for row in stored["calibration"]
            if row["candidate_ref"]["candidate_id"] == candidates[0]["candidate_id"]
        )
        self.assertIsNone(under_evidenced["control_point_acquisition_evidence"])

    def test_core_control_point_evidence_is_bound_to_candidate_claims_and_sources(self) -> None:
        candidate = self.candidate("contractible-core")
        self.store_candidate(candidate)
        bad_evidence = self.control_point_acquisition_evidence(candidate)
        bad_evidence["claim_ids"] = ["claim-budget"]
        bad_evidence["evidence_refs"] = [candidate["source_refs"][1]]
        with self.assertRaisesRegex(
            op.InputError, "must cite a founder_control_point_path claim"
        ):
            self.store_portfolio_selection(
                [candidate],
                calibration_overrides={
                    candidate["candidate_id"]: {
                        "control_point_acquisition_evidence": bad_evidence,
                    }
                },
            )

        op.fail_job(
            self.run_dir,
            "portfolio-selection",
            "calibration evidence cited the wrong claim type",
        )
        invalid_source = self.control_point_acquisition_evidence(candidate)
        invalid_source["evidence_refs"] = [candidate["source_refs"][0]]
        with self.assertRaisesRegex(op.InputError, "must be cited by its claim_ids"):
            self.store_portfolio_selection(
                [candidate],
                calibration_overrides={
                    candidate["candidate_id"]: {
                        "control_point_acquisition_evidence": invalid_source,
                    }
                },
            )

    def test_candidate_scoped_status_does_not_leak_portfolio_or_scores(self) -> None:
        alpha = self.candidate("alpha")
        beta = self.candidate("beta")
        self.store_candidate(alpha)
        self.store_candidate(beta)
        self.store_portfolio_selection([alpha, beta])
        context = op.candidate_research_context(self.run_dir, "alpha")
        serialized = json.dumps(context, sort_keys=True)
        self.assertEqual(context["scope"], "candidate_research")
        self.assertEqual(context["candidate_ref"]["candidate_id"], "alpha")
        self.assertNotIn("beta", serialized)
        self.assertNotIn("portfolio_decision", context)
        self.assertNotIn("highest_working_score", context)
        self.assertNotIn("working_evaluation_coverage", context)

    def test_research_cannot_alter_selected_candidate_commercial_core(self) -> None:
        candidate = self.candidate()
        candidate_path, _ = self.store_candidate(candidate)
        original_bytes = candidate_path.read_bytes()
        self.store_portfolio_selection([candidate])
        self.set_stage("research")

        disguised_rewrite = self.research(candidate)
        disguised_rewrite["title"] = "Silently rewritten opportunity"
        with self.assertRaisesRegex(op.InputError, "research keys differ"):
            op.validate_research(disguised_rewrite, self.load()[0], self.run_dir)

        research_path = self.root / "research-alpha.json"
        research_path.write_text(json.dumps(self.research(candidate)), encoding="utf-8")
        op.start_job(self.run_dir, "research-alpha", "research")
        completed = op.complete_job(
            self.run_dir, "research-alpha", research_path, "research"
        )
        self.assertEqual(completed["artifact"], "research/alpha/v1.json")
        self.assertEqual(candidate_path.read_bytes(), original_bytes)
        self.assertFalse((self.run_dir / "candidates/alpha/v2.json").exists())

    def test_single_response_has_one_canonical_score(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        response = self.evaluation_input(
            candidate,
            "deterministic-judge",
            score=8.55,
            evaluation_type="working_research",
        )
        response.pop("_test_evaluation_type")
        manifest, _ = self.load()
        first = op.canonicalize_evaluator_response(
            copy.deepcopy(response), manifest, self.run_dir, "working_research"
        )
        second = op.canonicalize_evaluator_response(
            copy.deepcopy(response), manifest, self.run_dir, "working_research"
        )
        self.assertEqual(first, second)
        self.assertEqual(first["final_score"], 8.6)
        forged = copy.deepcopy(first)
        forged["final_score"] = 9.9
        with self.assertRaisesRegex(op.InputError, "single response or deterministic score"):
            op.validate_canonical_evaluation(forged, manifest, self.run_dir)

    def test_deterministic_scoring_handles_threshold_exclusion_and_clamp(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        boundary = self._canonical_response(candidate, "boundary", score=8.5)
        self.assertEqual(boundary["final_score"], 8.5)
        self.assertFalse(boundary["qualified"])

        excluded = self._canonical_response(
            candidate,
            "excluded",
            score=9,
            excluded={"Core insight"},
        )
        core = next(item for item in excluded["factors"] if item["name"] == "Core insight")
        economics = next(
            item
            for item in excluded["factors"]
            if item["name"] == "Business model and economics"
        )
        self.assertEqual(core["effective_weight"], 0)
        self.assertEqual(economics["effective_weight"], 22.44898)

        clamped = self._canonical_response(
            candidate, "clamped", score=10, adjustment=0.5
        )
        self.assertEqual(clamped["unrounded_score"], 10.5)
        self.assertEqual(clamped["constrained_score"], 10)
        self.assertEqual(clamped["final_score"], 10)

    def test_strict_evaluator_response_rejects_malformed_or_extra_fields(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        manifest, _ = self.load()
        response = self.evaluation_input(candidate, "invalid-response")
        response.pop("_test_evaluation_type")
        self.set_stage("research")
        response_path = self.root / "strict-response.json"
        response_path.write_text(json.dumps(response), encoding="utf-8")
        validated = op.validate_artifact(
            self.run_dir, response_path, "evaluation"
        )
        self.assertEqual(validated["final_score"], 9)
        self.assertTrue(validated["qualified"])

        missing = copy.deepcopy(response)
        missing["factors"].pop()
        with self.assertRaisesRegex(op.InputError, "factors differ from rubric"):
            op.canonicalize_evaluator_response(
                missing, manifest, self.run_dir, "working_research"
            )

        extra = copy.deepcopy(response)
        extra["final_score"] = 10
        with self.assertRaisesRegex(op.InputError, "evaluator response keys differ"):
            op.canonicalize_evaluator_response(
                extra, manifest, self.run_dir, "working_research"
            )

        wrong_version = copy.deepcopy(response)
        wrong_version["candidate_version"] = 99
        with self.assertRaisesRegex(op.InputError, "candidate artifact does not exist"):
            op.canonicalize_evaluator_response(
                wrong_version, manifest, self.run_dir, "working_research"
            )

    def test_authorized_amendment_and_development_redesign_follow_lineage(self) -> None:
        alpha = self.candidate("alpha")
        beta = self.candidate("beta")
        self.store_candidate(alpha)
        self.store_candidate(beta)
        self.store_portfolio_selection([alpha])
        self.set_stage("research")

        selection_path = self.run_dir / "portfolio/selection.json"
        amendment = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "amendment_version": 1,
            "base_selection_sha256": op.sha256_file(selection_path),
            "remove_candidate_ref": self.candidate_ref(alpha),
            "add_candidate_ref": self.candidate_ref(beta),
            "reason": "The calibrated beta candidate is the explicit replacement.",
        }
        self.complete_json_job(
            "portfolio-amendment-v1", "portfolio-amendment", amendment
        )
        effective = op.effective_portfolio_selection(self.run_dir, self.load()[0])
        self.assertEqual(
            [(row["candidate_id"], row["version"]) for row in effective["candidate_refs"]],
            [("beta", 1)],
        )

        self.store_research(self.research(beta))
        self.store_evaluation(
            self.evaluation_input(
                beta,
                "research-judge-beta",
                score=8,
                evaluation_type="working_research",
            )
        )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision([beta], {"beta"}),
        )
        op.advance_run(self.run_dir)

        redesign = self.candidate(
            "beta",
            version=2,
            stage="development",
            parent={"candidate_id": "beta", "version": 1},
        )
        self.complete_json_job("develop-beta", "candidate", redesign)
        result = self.development_result(
            redesign,
            constructor_id="constructor-beta",
            outcome="redesigned",
            base_candidate=beta,
        )
        self.complete_json_job("constructor-beta", "development-result", result)
        self.store_evaluation(
            self.evaluation_input(
                redesign,
                "development-judge-beta",
                score=8.2,
                evaluation_type="working_development",
            )
        )
        advanced = op.advance_run(self.run_dir)
        self.assertEqual(advanced["stage"], "frozen")
        finalists = op.load_finalist_selection(self.run_dir, self.load()[0])
        self.assertEqual(finalists["candidate_refs"], [self.candidate_ref(redesign)])
        self.assertEqual(redesign["parent"], {"candidate_id": "beta", "version": 1})

        third = copy.deepcopy(redesign)
        third["version"] = 3
        third["parent"] = {"candidate_id": "beta", "version": 2}
        with self.assertRaisesRegex(op.InputError, "only one admitted development redesign"):
            op.validate_candidate(third, self.load()[0], self.run_dir)

    def test_constructor_binding_is_derived_after_candidate_normalization(self) -> None:
        base = self.candidate("alpha")
        self.store_candidate(base)
        self.store_portfolio_selection([base])
        self.set_stage("research")
        self.store_research(self.research(base))
        self.store_evaluation(
            self.evaluation_input(
                base,
                "research-judge-alpha",
                score=8,
                evaluation_type="working_research",
            )
        )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision([base], {"alpha"}),
        )
        op.advance_run(self.run_dir)

        redesign = self.candidate(
            "alpha",
            version=2,
            stage="development",
            parent={"candidate_id": "alpha", "version": 1},
        )
        raw_path = self.root / "noncanonical-redesign.json"
        raw_path.write_text(json.dumps(redesign, separators=(",", ":")), encoding="utf-8")
        raw_hash = op.sha256_file(raw_path)
        op.start_job(self.run_dir, "develop-alpha", "development")
        completed_candidate = op.complete_job(
            self.run_dir, "develop-alpha", raw_path, "candidate"
        )
        self.assertNotEqual(raw_hash, completed_candidate["artifact_sha256"])

        completed_result = self.complete_json_job(
            "constructor-alpha",
            "development-result",
            self.development_result(
                redesign,
                constructor_id="constructor-alpha",
                outcome="redesigned",
                base_candidate=base,
            ),
        )
        canonical_result = op.load_json(self.run_dir / completed_result["artifact"])
        self.assertEqual(
            canonical_result["final_candidate_sha256"],
            completed_candidate["artifact_sha256"],
        )
        self.assertEqual(
            canonical_result["base_candidate_sha256"],
            self.candidate_ref(base)["candidate_sha256"],
        )

    def test_malformed_output_retries_successfully_and_exhaustion_is_visible(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        self.store_portfolio_selection([candidate])
        self.set_stage("research")
        self.store_research(self.research(candidate))
        malformed = self.root / "malformed-evaluation.json"
        malformed.write_text('{"candidate_id":"alpha",,}', encoding="utf-8")

        op.start_job(self.run_dir, "evaluation-retry", "research")
        with self.assertRaisesRegex(op.InputError, "invalid JSON"):
            op.complete_job(
                self.run_dir, "evaluation-retry", malformed, "evaluation"
            )
        first_job = self.load()[1]["jobs"]["research"]["evaluation-retry"]
        self.assertEqual(first_job["status"], "failed")
        self.assertTrue(op.job_is_retryable(first_job))

        valid = self.evaluation_input(
            candidate,
            "retry-judge",
            score=7.5,
            evaluation_type="working_research",
        )
        valid.pop("_test_evaluation_type")
        valid_path = self.root / "valid-evaluation.json"
        valid_path.write_text(json.dumps(valid), encoding="utf-8")
        self.assertEqual(
            op.start_job(self.run_dir, "evaluation-retry", "research")["attempts"],
            2,
        )
        completed = op.complete_job(
            self.run_dir, "evaluation-retry", valid_path, "evaluation"
        )
        self.assertEqual(completed["status"], "completed")

        for attempt in range(2):
            op.start_job(self.run_dir, "evaluation-exhausted", "research")
            with self.assertRaisesRegex(op.InputError, "invalid JSON"):
                op.complete_job(
                    self.run_dir,
                    "evaluation-exhausted",
                    malformed,
                    "evaluation",
                )
        exhausted = self.load()[1]["jobs"]["research"]["evaluation-exhausted"]
        self.assertTrue(op.job_is_exhausted(exhausted))
        resumed = op.resume_run(self.run_dir)
        self.assertIn(
            "evaluation-exhausted",
            [row["job_id"] for row in resumed["exhausted_jobs"]],
        )

    def test_valid_adverse_evaluation_is_never_retried(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        self.store_portfolio_selection([candidate])
        self.set_stage("research")
        self.store_research(self.research(candidate))
        response = self.evaluation_input(
            candidate,
            "adverse-judge",
            score=2,
            evaluation_type="working_research",
        )
        response.pop("_test_evaluation_type")
        response_path = self.root / "adverse.json"
        response_path.write_text(json.dumps(response), encoding="utf-8")
        op.start_job(self.run_dir, "adverse-evaluation", "research")
        completed = op.complete_job(
            self.run_dir, "adverse-evaluation", response_path, "evaluation"
        )
        self.assertEqual(completed["status"], "completed")
        canonical = op.load_json(self.run_dir / completed["artifact"])
        self.assertFalse(canonical["qualified"])
        self.assertEqual(canonical["final_score"], 2)
        with self.assertRaisesRegex(op.ConflictError, "job is terminal"):
            op.start_job(self.run_dir, "adverse-evaluation", "research")

    def test_evaluator_failure_event_recovers_after_state_write_interruption(self) -> None:
        candidate = self.candidate()
        self.store_candidate(candidate)
        self.store_portfolio_selection([candidate])
        self.set_stage("research")
        self.store_research(self.research(candidate))
        malformed = self.root / "interrupted-malformed.json"
        malformed.write_text('{"candidate_id":"alpha",,}', encoding="utf-8")
        op.start_job(self.run_dir, "interrupted-evaluator", "research")

        with mock.patch.object(
            op, "save_state", side_effect=OSError("simulated evaluator state failure")
        ):
            with self.assertRaisesRegex(OSError, "simulated evaluator state failure"):
                op.complete_job(
                    self.run_dir,
                    "interrupted-evaluator",
                    malformed,
                    "evaluation",
                )
        self.assertEqual(
            self.load()[1]["jobs"]["research"]["interrupted-evaluator"]["status"],
            "running",
        )
        with self.assertRaisesRegex(op.ConflictError, "is failed"):
            op.complete_job(
                self.run_dir,
                "interrupted-evaluator",
                malformed,
                "evaluation",
            )
        failed_events = [
            event
            for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            if event["event"] == "job_failed"
            and event["job_id"] == "interrupted-evaluator"
        ]
        self.assertEqual(len(failed_events), 1)
        reconciled = self.load()[1]["jobs"]["research"]["interrupted-evaluator"]
        self.assertEqual(reconciled["status"], "failed")
        self.assertTrue(op.job_is_retryable(reconciled))

        response = self.evaluation_input(
            candidate,
            "recovered-judge",
            score=7,
            evaluation_type="working_research",
        )
        response.pop("_test_evaluation_type")
        valid = self.root / "recovered-evaluation.json"
        valid.write_text(json.dumps(response), encoding="utf-8")
        self.assertEqual(
            op.start_job(
                self.run_dir, "interrupted-evaluator", "research"
            )["attempts"],
            2,
        )
        completed = op.complete_job(
            self.run_dir, "interrupted-evaluator", valid, "evaluation"
        )
        self.assertEqual(completed["status"], "completed")
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])


class WorkflowContractTests(OpportunityTestCase):
    def test_active_skill_requires_scoped_evaluators_to_load_bound_snapshots(self) -> None:
        skill = (
            op.REPO_ROOT / ".agents/skills/business-opportunity/SKILL.md"
        ).read_text(encoding="utf-8")
        workflow = (
            op.REPO_ROOT
            / ".agents/skills/business-opportunity/references/workflow.md"
        ).read_text(encoding="utf-8")
        contracts = (
            op.REPO_ROOT
            / ".agents/skills/business-opportunity/references/artifact-contracts.md"
        ).read_text(encoding="utf-8")

        self.assertIn("must read the founder and evaluator snapshot paths", skill)
        self.assertIn("verify each file against its returned SHA-256", skill)
        self.assertIn("a prompt must never prohibit them", skill)
        self.assertIn("both reads are mandatory", workflow)
        self.assertIn("verify both hashes", contracts)

    def researched_pool(
        self,
        count: int,
        *,
        scores: list[float] | None = None,
    ) -> tuple[list[dict], list[dict]]:
        values = scores or [8.0 - index / 10 for index in range(count)]
        discoveries = [self.candidate(f"candidate-{index + 1}") for index in range(count)]
        for discovery in discoveries:
            self.store_candidate(discovery)
        self.store_portfolio_selection(discoveries)
        self.set_stage("research")
        researched: list[dict] = []
        for discovery, score in zip(discoveries, values, strict=True):
            candidate = discovery
            self.store_research(self.research(candidate))
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"research-judge-{candidate['candidate_id']}",
                    score=score,
                    evaluation_type="working_research",
                )
            )
            researched.append(candidate)
        return discoveries, researched

    def test_research_advance_and_finalize_require_exact_working_coverage(self) -> None:
        discovery = self.candidate("alpha")
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        researched = discovery
        self.store_research(self.research(researched))

        with self.assertRaisesRegex(op.ConflictError, "exactly one working evaluation"):
            op.advance_run(self.run_dir)
        with self.assertRaisesRegex(op.ConflictError, "exactly one working evaluation"):
            op.finalize_run(self.run_dir, "Research budget ended before development")

        self.store_evaluation(
            self.evaluation_input(
                researched,
                "research-judge-alpha",
                score=7.4,
                evaluation_type="working_research",
            )
        )
        coverage = op.working_evaluation_coverage(self.run_dir, self.load()[0], "research")
        self.assertTrue(coverage["complete"])
        self.assertEqual(coverage["completed_count"], 1)

        self.store_evaluation(
            self.evaluation_input(
                researched,
                "research-judge-alpha-duplicate",
                score=7.5,
                evaluation_type="working_research",
            )
        )
        coverage = op.working_evaluation_coverage(self.run_dir, self.load()[0], "research")
        self.assertFalse(coverage["complete"])
        self.assertEqual(coverage["duplicates"], ["alpha v1"])
        with self.assertRaisesRegex(op.ConflictError, "duplicate alpha v1"):
            op.advance_run(self.run_dir)

    def test_research_candidate_substitution_requires_versioned_amendment(self) -> None:
        alpha = self.candidate("alpha")
        beta = self.candidate("beta")
        self.store_candidate(alpha)
        self.store_candidate(beta)
        self.store_portfolio_selection([alpha])
        self.set_stage("research")
        researched_beta = self.research(beta)
        path = self.root / "unamended-beta.json"
        path.write_text(json.dumps(researched_beta), encoding="utf-8")
        op.start_job(self.run_dir, "unamended-beta", "research")
        with self.assertRaisesRegex(op.ConflictError, "versioned portfolio amendment"):
            op.complete_job(self.run_dir, "unamended-beta", path, "research")
        op.fail_job(self.run_dir, "unamended-beta", "shortlist binding correctly rejected substitution")

        selection_path = self.run_dir / "portfolio/selection.json"
        amendment = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "amendment_version": 1,
            "base_selection_sha256": op.sha256_file(selection_path),
            "remove_candidate_ref": self.candidate_ref(alpha),
            "add_candidate_ref": self.candidate_ref(beta),
            "reason": "New evidence invalidated alpha and justified beta as the explicit replacement.",
        }
        completed = self.complete_json_job(
            "portfolio-amendment-v1",
            "portfolio-amendment",
            amendment,
        )
        self.assertEqual(completed["artifact"], "portfolio/amendments/v1.json")
        accepted = self.complete_json_job(
            "amended-beta",
            "research",
            researched_beta,
        )
        self.assertEqual(accepted["artifact"], "research/beta/v1.json")

    def test_unknown_or_inferential_claim_cannot_be_a_fatal_stop(self) -> None:
        _, researched = self.researched_pool(1, scores=[7.8])
        candidate = researched[0]
        research_path = self.run_dir / op.research_relpath(candidate["candidate_id"], candidate["version"])
        research = json.loads(research_path.read_text(encoding="utf-8"))
        research["claims"][0]["assessment"] = "unknown"
        research["claims"][0]["evidence_refs"] = []
        research_path.write_bytes(op.canonical_json_bytes(research))
        decision = self.portfolio_decision(researched, set())
        row = decision["candidate_decisions"][0]
        row.update(
            {
                "disposition": "fatal",
                "fatal_reason": "impossible_conservative_economics",
                "fatal_claim_ids": ["research-claim-1"],
                "rationale": "This must be rejected because the cited claim is still unknown.",
            }
        )
        with self.assertRaisesRegex(op.InputError, "unknown or inferential research cannot be labeled fatal"):
            op.validate_portfolio_decision(decision, self.load()[0], self.run_dir)

    def test_development_requires_fresh_exact_version_score_and_role_separation(self) -> None:
        _, researched = self.researched_pool(1, scores=[8.1])
        decision = self.portfolio_decision(researched, {researched[0]["candidate_id"]})
        self.complete_json_job("portfolio-decision", "portfolio-decision", decision)
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "development")

        research_candidate = researched[0]
        developed = self.candidate(
            research_candidate["candidate_id"],
            version=2,
            stage="development",
            parent={"candidate_id": research_candidate["candidate_id"], "version": 1},
        )
        self.complete_json_job("develop-alpha", "candidate", developed)
        self.complete_json_job(
            "constructor-alpha",
            "development-result",
            self.development_result(
                developed,
                constructor_id="same-agent",
                outcome="redesigned",
                base_candidate=research_candidate,
            ),
        )

        with self.assertRaisesRegex(op.ConflictError, "missing candidate-1 v2"):
            op.advance_run(self.run_dir)
        self.store_evaluation(
            self.evaluation_input(
                developed,
                "same-agent",
                score=8.2,
                evaluation_type="working_development",
            )
        )
        with self.assertRaisesRegex(op.ConflictError, "constructor and working evaluator roles must be independent"):
            op.advance_run(self.run_dir)

    def test_multiple_development_redesigns_can_be_admitted_sequentially(self) -> None:
        _, researched = self.researched_pool(2, scores=[8.1, 8.0])
        developed_ids = {candidate["candidate_id"] for candidate in researched}
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision(researched, developed_ids),
        )
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "development")

        admitted = []
        for research_candidate in researched:
            developed = self.candidate(
                research_candidate["candidate_id"],
                version=2,
                stage="development",
                parent={
                    "candidate_id": research_candidate["candidate_id"],
                    "version": 1,
                },
            )
            completed = self.complete_json_job(
                f"develop-{research_candidate['candidate_id']}",
                "candidate",
                developed,
            )
            admitted.append(completed["artifact"])

        self.assertEqual(
            admitted,
            [
                "candidates/candidate-1/v2.json",
                "candidates/candidate-2/v2.json",
            ],
        )

    def test_native_holdout_judge_cannot_reuse_a_development_role(self) -> None:
        frozen = self.store_complete_lineage("alpha")
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        reused = self.evaluation_input(frozen, "working-alpha", score=8.8)
        reused.pop("_test_evaluation_type")
        input_path = self.root / "reused-native-response.json"
        input_path.write_text(json.dumps(reused), encoding="utf-8")
        op.start_job(self.run_dir, "reused-native-response", "holdout")
        with self.assertRaisesRegex(
            op.ConflictError,
            "native holdout judge must be fresh and independent",
        ):
            op.complete_job(
                self.run_dir,
                "reused-native-response",
                input_path,
                "evaluation",
            )

    def test_constructor_cannot_reuse_any_working_evaluator_role(self) -> None:
        _, researched = self.researched_pool(1, scores=[7.0])
        candidate = researched[0]
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision(researched, {candidate["candidate_id"]}),
        )
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "development")
        with self.assertRaisesRegex(
            op.ConflictError,
            "constructor and working evaluator roles must be independent",
        ):
            self.complete_json_job(
                "constructor-role-reuse",
                "development-result",
                self.development_result(
                    candidate,
                    constructor_id=f"research-judge-{candidate['candidate_id']}",
                ),
            )

    def test_complete_eight_four_two_four_scored_fixture(self) -> None:
        scores = [8.4, 8.3, 8.2, 8.1, 7.9, 7.8, 7.7, 7.6]
        _, researched = self.researched_pool(8, scores=scores)
        developed_ids = {candidate["candidate_id"] for candidate in researched[:4]}
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision(researched, developed_ids),
        )
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "development")

        developed: list[dict] = []
        for index, research_candidate in enumerate(researched[:4]):
            candidate_id = research_candidate["candidate_id"]
            candidate = research_candidate
            self.complete_json_job(
                f"constructor-{candidate_id}",
                "development-result",
                self.development_result(
                    candidate,
                    constructor_id=f"constructor-agent-{candidate_id}",
                ),
            )
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"development-judge-{candidate_id}",
                    score=8.4 - index / 10,
                    evaluation_type="working_development",
                )
            )
            developed.append(candidate)

        self.assertEqual(op.advance_run(self.run_dir)["stage"], "frozen")
        frozen = developed[:2]
        for candidate in frozen:
            candidate_id = candidate["candidate_id"]
            op.export_external(self.run_dir, candidate_id)

        self.assertEqual(op.advance_run(self.run_dir)["stage"], "holdout")
        holdout_scores = ((8.4, 8.3), (8.3, 8.2))
        for candidate, pair in zip(frozen, holdout_scores, strict=True):
            for judge_index, score in enumerate(pair, start=1):
                judge_id = f"native-{judge_index}-{candidate['candidate_id']}"
                self.store_evaluation(
                    self.evaluation_input(candidate, judge_id, score=score)
                )

        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "no_qualifier")
        self.assertEqual(report["selected_candidate_id"], "candidate-1")
        self.assertEqual(report["official_score"], 8.3)
        self.assertEqual(report["binding_score_floor"], 8.3)
        self.assertEqual(len(report["candidates"]), 2)
        self.assertEqual(
            sum(
                len(candidate["evaluation_artifacts"])
                for candidate in report["candidates"]
            ),
            4,
        )
        coverage = report["working_evaluation_coverage"]
        self.assertTrue(coverage["complete"])
        self.assertEqual(coverage["research"]["completed_count"], 8)
        self.assertEqual(coverage["development"]["completed_count"], 4)
        self.assertEqual(coverage["total_candidate_versions"], 12)
        self.assertEqual(
            len(report["portfolio_decision"]["candidate_decisions"]),
            8,
        )
        manifest, _ = self.load()
        campaign_metrics = op.derive_campaign_cohort_metrics(
            self.run_dir,
            manifest,
            report,
        )
        self.assertEqual(campaign_metrics["top_four_working_median"], 8.3)
        self.assertTrue(campaign_metrics["deficient_factors"])
        self.assertNotIn("best_working_score", campaign_metrics)
        self.assertNotIn("archetype_scores", campaign_metrics)
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])
        published = op.publish_run(
            self.run_dir,
            self.root / "outcomes",
            self.root / "knowledge",
        )
        self.assertEqual(published["run_status"], "no_qualifier")
        published_root = self.root / "outcomes" / self.run_id
        self.assertTrue((published_root / "report.json").is_file())
        self.assertTrue((published_root / "portfolio/selection.json").is_file())
        self.assertTrue(
            (published_root / "portfolio/development-decision.json").is_file()
        )
        self.assertEqual(
            len(list(published_root.glob("evaluations/*/v*/*.json"))),
            12,
        )
        published_holdouts = []
        for finalist in report["candidates"]:
            self.assertTrue(
                (published_root / finalist["candidate_artifact"]).is_file()
            )
            export_root = published_root / "exports" / finalist["candidate_id"]
            self.assertTrue((export_root / "holdout_packet.md").is_file())
            self.assertTrue((export_root / "response_schema.json").is_file())
            for artifact in finalist["evaluation_artifacts"]:
                evaluation_path = published_root / artifact["path"]
                self.assertTrue(evaluation_path.is_file())
                self.assertEqual(op.sha256_file(evaluation_path), artifact["sha256"])
                published_holdouts.append(evaluation_path)
        self.assertEqual(len(published_holdouts), 4)
        validated_publication = op.validate_published_run_outcome(published_root)
        self.assertEqual(validated_publication["run_id"], self.run_id)
        working_record = report["working_evaluation_coverage"]["research"]["records"][0]
        working_path = published_root / working_record["evaluation_path"]
        working_evaluation = json.loads(working_path.read_text(encoding="utf-8"))
        working_evaluation["final_score"] = 10
        working_path.write_text(json.dumps(working_evaluation), encoding="utf-8")
        with self.assertRaises(op.InputError):
            op.validate_published_run_outcome(published_root)

    def test_direct_evidence_research_closure_is_no_finalist_with_score_coverage(self) -> None:
        self.prepare_fatal_research_closure()
        report, code = op.finalize_run(
            self.run_dir,
            "Direct sourced evidence proves the conservative economics cannot work.",
        )
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "no_finalist")
        self.assertEqual(report["terminal_stage"], "research")
        self.assertIsNone(report["official_score"])
        self.assertIsNone(report["binding_score_floor"])
        self.assertEqual(report["highest_working_score"], 6.5)
        self.assertTrue(report["working_evaluation_coverage"]["complete"])
        self.assertEqual(report["working_evaluation_coverage"]["total_candidate_versions"], 1)
        self.assertEqual(report["working_evaluation_coverage"]["total_completed"], 1)
        self.assertEqual(
            report["portfolio_decision"]["development_decision_artifact"]["path"],
            "portfolio/development-decision.json",
        )


class ScoreBracketWorkflowTests(OpportunityTestCase):
    def test_scout_contract_is_scoped_complete_and_nonmutating(self) -> None:
        op.advance_run(self.run_dir)
        before = {name: (self.run_dir / name).read_bytes() for name in ("state.json", "events.jsonl")}
        manifest, _ = self.load()
        for lane in manifest["config"]["discovery_lanes"]:
            code, contract, error = self.run_cli([
                "--runs-dir", str(self.runs_dir), "scout-contract", self.run_id, "--lane", lane,
            ])
            self.assertEqual(code, 0, error)
            self.assertEqual(contract["candidate_count"], manifest["config"]["seeds_per_scout"])
            schema = contract["strict_response_contract"]
            progress, completed = schema["properties"]["response"]["anyOf"]
            self.assertEqual(set(progress["properties"]), {"type", "message"})
            self.assertEqual(progress["properties"]["type"]["enum"], ["progress"])
            self.assertEqual(completed["properties"]["type"]["enum"], ["candidates"])
            array = completed["properties"]["candidates"]
            self.assertEqual(array["minItems"], contract["candidate_count"])
            self.assertEqual(array["maxItems"], contract["candidate_count"])
            item = array["items"]
            self.assertFalse(item["additionalProperties"])
            self.assertEqual(set(item["required"]), set(contract["candidate_contract"]["template"]))
            props = item["properties"]
            self.assertEqual(props["discovery_lane"]["enum"], [lane])
            self.assertEqual(props["parent"]["type"], "null")
            self.assertEqual(props["version"]["type"], "integer")
            self.assertIn("subject_type", props["critical_control_point"]["required"])
            self.assertIn("bundling_resistance", props["commercial_mechanics"]["required"])
            self.assertEqual(props["founder_fit"]["type"], "array")
            self.assertEqual(props["claims"]["items"]["properties"]["claim_type"]["enum"], sorted(op.CLAIM_TYPES))
            self.assertEqual(contract["candidate_contract"]["template"]["critical_control_point"]["status"], "unknown")
            binding = contract["founder_snapshot"]
            self.assertEqual(op.sha256_file(self.run_dir / binding["path"]), binding["sha256"])
            for forbidden in ("threshold", "rubric", "ranking", "evaluator_snapshot", "history", "score"):
                self.assertNotIn(forbidden, json.dumps(contract))
        for name, content in before.items():
            self.assertEqual((self.run_dir / name).read_bytes(), content)
        with self.assertRaisesRegex(op.InputError, "configured discovery lane"):
            op.scout_contract(self.run_dir, "invented")
        self.set_stage("research")
        with self.assertRaisesRegex(op.ConflictError, "only during discovery"):
            op.scout_contract(self.run_dir, "mechanism-first")

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.runs_dir = self.root / "runs"
        self.config_path = op.DEFAULT_CONFIG
        created = op.make_run(self.config_path, self.runs_dir)
        self.run_id = created["run_id"]
        self.run_dir = Path(created["run_dir"])

    def test_unhashable_role_enums_return_diagnostics_and_record_failures(self) -> None:
        candidate = self.candidate("enum-probe")
        self.set_stage("discovery")
        for stage, kind, field_paths in (
            ("discovery", "candidate", [("claims", 0, "claim_type")]),
            ("research", "research", [("sources", 0, "stance"), ("claims", 0, "assessment")]),
            ("development", "development-result", [("outcome",)]),
        ):
            self.set_stage(stage)
            if kind == "candidate":
                response = candidate
            elif kind == "research":
                self.store_candidate(candidate)
                response = self.research(candidate)
            else:
                response = op.preflight_artifact(self.run_dir, kind)[0]["template"]
                response["candidate_id"] = candidate["candidate_id"]
            for field_index, fields in enumerate(field_paths):
                for value_index, malformed in enumerate(([], {})):
                    with self.subTest(kind=kind, fields=fields, malformed=malformed):
                        value = copy.deepcopy(response)
                        parent = value
                        for field in fields[:-1]:
                            parent = parent[field]
                        parent[fields[-1]] = malformed
                        path = self.root / "malformed-enum.json"
                        path.write_bytes(op.canonical_json_bytes(value))
                        job_id = f"enum-{kind}-{field_index}-{value_index}"
                        before = {name: (self.run_dir / name).read_bytes() for name in ("state.json", "events.jsonl")}
                        code, report, error = self.run_cli([
                            "--runs-dir", str(self.runs_dir), "preflight", self.run_id,
                            "--kind", kind, "--job-id", job_id,
                            "--input", str(path), "--original-input", str(path),
                        ])
                        self.assertEqual(code, 2, error)
                        self.assertEqual(report["validation"]["errors"][0]["pointer"], "/" + "/".join(map(str, fields)))
                        self.assertNotIn("preflight_receipt", report["validation"])
                        for name, raw in before.items():
                            self.assertEqual((self.run_dir / name).read_bytes(), raw)

                        # A malformed response reaching completion must still become
                        # a visible schema failure before receipt verification.
                        op.start_job(self.run_dir, job_id, stage)
                        code, _, error = self.run_cli([
                            "--runs-dir", str(self.runs_dir), "job", self.run_id,
                            job_id, "complete", "--kind", kind, "--input", str(path),
                            "--preflight-sha256", op.sha256_file(path),
                            "--preflight-receipt-sha256", "0" * 64,
                        ])
                        self.assertEqual(code, 2)
                        self.assertEqual(error["error_type"], "InputError")
                        manifest, state = self.load()
                        self.assertEqual(state["jobs"][stage][job_id]["status"], "failed")
                        self.assertEqual(state["jobs"][stage][job_id]["attempts"], 1)
                        op.require_job_event_state_match(
                            op.load_events(self.run_dir / "events.jsonl", self.run_id), state, manifest,
                        )

    def test_unhashable_portfolio_enums_are_input_errors(self) -> None:
        candidate = self.candidate("portfolio-enum-probe")
        self.store_candidate(candidate)
        self.store_research(self.research(candidate))
        self.set_stage("research")
        selection = {"candidate_refs": [self.candidate_ref(candidate)]}
        with mock.patch.object(op, "effective_portfolio_selection", return_value=selection), mock.patch.object(
            op, "_require_working_evaluation_coverage", return_value={},
        ):
            for field in ("disposition", "fatal_reason"):
                for malformed in ([], {}):
                    with self.subTest(field=field, malformed=malformed):
                        decision = self.portfolio_decision([candidate], {candidate["candidate_id"]})
                        row = decision["candidate_decisions"][0]
                        if field == "fatal_reason":
                            row["disposition"] = "fatal"
                        row[field] = malformed
                        path = self.root / "malformed-portfolio.json"
                        path.write_bytes(op.canonical_json_bytes(decision))
                        code, report, error = self.run_cli([
                            "--runs-dir", str(self.runs_dir), "preflight", self.run_id,
                            "--kind", "portfolio-decision", "--job-id", "portfolio-enum",
                            "--input", str(path), "--original-input", str(path),
                        ])
                        self.assertEqual(code, 2, error)
                        self.assertIn(field, report["validation"]["errors"][0]["message"])
                        self.assertNotIn("preflight_receipt", report["validation"])
        self.assertEqual(self.load()[1]["jobs"]["research"], {})

    def test_preflight_allows_only_trimming_string_boundary_whitespace(self) -> None:
        self.set_stage("discovery")
        candidate = self.candidate("whitespace-probe")
        original = copy.deepcopy(candidate)
        original["commercial_mechanics"]["fully_loaded_economics"]["revenue_basis"] += " \n"
        first = self.root / "original.json"
        corrected = self.root / "corrected.json"
        first.write_bytes(op.canonical_json_bytes(original))
        corrected.write_bytes(op.canonical_json_bytes(candidate))
        before = {name: (self.run_dir / name).read_bytes() for name in ("state.json", "events.jsonl")}
        report, valid = op.preflight_artifact(self.run_dir, "candidate", first, "trim-probe", first)
        self.assertFalse(valid)
        self.assertTrue(report["validation"]["schema_retry_required"])
        report, valid = op.preflight_artifact(self.run_dir, "candidate", corrected, "trim-probe", first)
        self.assertTrue(valid, report["validation"]["errors"])
        self.assertTrue(report["validation"]["correction_content_preserved"])
        self.assertEqual(report["validation"]["original_input_sha256"], op.sha256_file(first))
        self.assertIn("preflight_receipt", report["validation"])
        for name, raw in before.items():
            self.assertEqual((self.run_dir / name).read_bytes(), raw)
        for old, new in (("paid event", "paidevent"), ("unknown", "evidence"), ("five", "six"), (4, 5), ("claim", " claim ")):
            self.assertTrue(op.correction_content_differences({"value": old}, {"value": new}, "evaluation"))

    def test_report_coverage_units_and_exact_legacy_rendering(self) -> None:
        config = self.load()[0]["config"]
        report = {
            "run_id": self.run_id, "run_status": "no_finalist",
            "rubric_id": config["rubric_id"], "threshold": config["threshold"],
            "comparison": config["comparison"], "highest_working_score": 5,
            "working_evaluation_coverage": {
                "total_completed": 64, "total_candidate_versions": 59,
            },
        }
        current = op.render_report_markdown(report).encode()
        legacy = op.render_report_markdown(report, legacy_coverage_label=True).encode()
        self.assertIn(b"`64` judgments across `59` phase-specific candidate versions", current)
        self.assertIn(b"`64/59` candidate versions", legacy)
        self.assertTrue(op.report_markdown_matches(report, current))
        self.assertTrue(op.report_markdown_matches(report, legacy))
        self.assertFalse(op.report_markdown_matches(report, legacy.replace(b"64/59", b"63/59")))
        self.assertFalse(op.report_markdown_matches(report, current + b"Forged conclusion"))

    def complete_evaluation_job(
        self, job_id: str, candidate: dict, judge_id: str, score: float, phase: str
    ) -> None:
        payload = self.evaluation_input(
            candidate,
            judge_id,
            score=score,
            evaluation_type=phase,
        )
        if phase == "working_screening" and job_id.endswith("-01"):
            payload.pop("_test_evaluation_type")
            self.complete_json_job(job_id, "evaluation", payload)
        else:
            self.store_evaluation(payload)

    def test_control_commercial_signature_and_explicit_unknown_contracts(self) -> None:
        candidate = self.candidate(
            "control-contract", discovery_lane="weak-signal"
        )
        _, canonical = self.store_candidate(candidate)
        self.assertEqual(canonical["critical_control_point"]["status"], "owned")
        self.assertEqual(
            canonical["commercial_mechanics"]["customer_relationship_owner"],
            canonical["critical_control_point"]["customer_relationship_owner"],
        )

        missing_mechanic = copy.deepcopy(candidate)
        missing_mechanic["commercial_mechanics"].pop("purchase_trigger")
        with self.assertRaisesRegex(op.InputError, "commercial_mechanics"):
            op.validate_candidate(missing_mechanic, self.load()[0], self.run_dir)

        externally_controlled = self.candidate(
            "external-mechanism", discovery_lane="mechanism-first"
        )
        externally_controlled["critical_control_point"].update(
            {
                "status": "externally_controlled",
                "mechanism_control": "dependent",
                "current_owner": "Incumbent platform",
                "launch_controller": "Incumbent platform",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "obtainable control point"
        ):
            op.validate_candidate(
                externally_controlled, self.load()[0], self.run_dir
            )

        left = self.candidate("signature-left", discovery_lane="weak-signal")
        right = self.candidate("signature-right", discovery_lane="future-backcast")
        for item in (left, right):
            item["structural_signature"].update(
                {
                    "commercial_model_category": "managed_service",
                    "control_point_category": "workflow_integration",
                    "critical_dependency_category": "distribution_channel",
                }
            )
        left["structural_signature"]["commercial_model_descriptor"] = (
            "EU factory incident service"
        )
        right["structural_signature"]["commercial_model_descriptor"] = (
            "Asian hospital workflow operator"
        )
        left_canonical = op.validate_candidate(left, self.load()[0], self.run_dir)
        right_canonical = op.validate_candidate(right, self.load()[0], self.run_dir)
        self.assertEqual(
            op.structural_signature_key(left_canonical),
            op.structural_signature_key(right_canonical),
        )

        research = self.research(canonical)
        research["claims"].append(
            {
                "claim_id": "research-unknown-private-proof",
                "statement": "Direct private validation is not available.",
                "assessment": "unknown",
                "evidence_refs": [],
            }
        )
        research["commercial_evidence"]["buyer_or_paid_event"] = {
            "status": "unknown",
            "claim_ids": ["research-unknown-private-proof"],
            "source_ids": [],
        }
        research["critical_control_point_assessment"] = {
            "status": "unknown",
            "assessment": "unknown",
            "claim_ids": ["research-unknown-private-proof"],
            "source_ids": [],
        }
        validated_research = op.validate_research(
            research, self.load()[0], self.run_dir
        )
        self.assertEqual(
            validated_research["commercial_evidence"]["buyer_or_paid_event"][
                "status"
            ],
            "unknown",
        )
        uncontrolled_label = copy.deepcopy(research)
        uncontrolled_label["sources"][0]["evidence_class"] = "buyer_quote"
        with self.assertRaisesRegex(op.InputError, "evidence_class"):
            op.validate_research(
                uncontrolled_label, self.load()[0], self.run_dir
            )

    def test_control_status_requires_coherent_acquisition_terms(self) -> None:
        self.set_stage("discovery")
        manifest, state = self.load()
        contract = op.preflight_contract(manifest, state, "candidate")
        self.assertIn(
            "critical_control_status_consistency",
            contract["constraints"],
        )

        unknown_owned_control = self.candidate(
            "unknown-owned-control", discovery_lane="weak-signal"
        )
        unknown_owned_control["critical_control_point"].update(
            {
                "acquisition_instrument_type": "unknown",
                "acquisition_instrument": "unknown",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "owned status requires ownership or purchase"
        ):
            op.validate_candidate(unknown_owned_control, manifest, self.run_dir)

        contracted_owned_control = self.candidate(
            "contracted-owned-control", discovery_lane="weak-signal"
        )
        contracted_owned_control["critical_control_point"].update(
            {
                "acquisition_instrument_type": "long_term_contract",
                "acquisition_instrument": "A proposed long-term access contract.",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "owned status requires ownership or purchase"
        ):
            op.validate_candidate(contracted_owned_control, manifest, self.run_dir)

        nonexclusive_control = self.candidate(
            "nonexclusive-control", discovery_lane="weak-signal"
        )
        nonexclusive_control["critical_control_point"].update(
            {
                "status": "exclusively_contracted",
                "mechanism_control": "dependent",
                "acquisition_instrument_type": "exclusive_contract",
                "acquisition_instrument": "A proposed exclusive control contract.",
                "exclusivity": "nonexclusive",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "exclusively_contracted status requires exclusive terms"
        ):
            op.validate_candidate(nonexclusive_control, manifest, self.run_dir)

        unknown_contract = copy.deepcopy(nonexclusive_control)
        unknown_contract["candidate_id"] = "unknown-exclusive-contract"
        unknown_contract["critical_control_point"].update(
            {
                "exclusivity": "exclusive",
                "acquisition_instrument": "unknown",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "affirmative control status requires a stated acquisition instrument"
        ):
            op.validate_candidate(unknown_contract, manifest, self.run_dir)

        durable_at_will = self.candidate(
            "durable-at-will", discovery_lane="weak-signal"
        )
        durable_at_will["critical_control_point"].update(
            {
                "status": "durably_contracted",
                "mechanism_control": "dependent",
                "acquisition_instrument_type": "long_term_contract",
                "acquisition_instrument": "A proposed long-term control contract.",
                "duration": "unknown",
                "revocability": "at_will",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "durably_contracted status requires a known duration"
        ):
            op.validate_candidate(durable_at_will, manifest, self.run_dir)
        durable_at_will["critical_control_point"]["duration"] = "Five years"
        with self.assertRaisesRegex(
            op.InputError, "durably_contracted status cannot be at_will or unknown"
        ):
            op.validate_candidate(durable_at_will, manifest, self.run_dir)

        irreplaceable_access = self.candidate(
            "irreplaceable-access", discovery_lane="weak-signal"
        )
        irreplaceable_access["critical_control_point"].update(
            {
                "status": "replaceable_access",
                "mechanism_control": "dependent",
                "acquisition_instrument_type": "long_term_contract",
                "acquisition_instrument": "A proposed access contract.",
                "replaceability": "not_replaceable",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "replaceable_access status requires replaceable terms"
        ):
            op.validate_candidate(irreplaceable_access, manifest, self.run_dir)

        unknown_replaceable_access = self.candidate(
            "unknown-replaceable-access", discovery_lane="weak-signal"
        )
        unknown_replaceable_access["critical_control_point"].update(
            {
                "status": "replaceable_access",
                "mechanism_control": "dependent",
                "acquisition_instrument_type": "unknown",
                "acquisition_instrument": "unknown",
                "replaceability": "replaceable",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "replaceable_access status requires a concrete acquisition instrument"
        ):
            op.validate_candidate(
                unknown_replaceable_access, manifest, self.run_dir
            )

        owned_replaceable_access = copy.deepcopy(unknown_replaceable_access)
        owned_replaceable_access["candidate_id"] = "owned-replaceable-access"
        owned_replaceable_access["critical_control_point"].update(
            {
                "acquisition_instrument_type": "ownership",
                "acquisition_instrument": "Ownership of the critical mechanism.",
            }
        )
        with self.assertRaisesRegex(
            op.InputError, "replaceable_access status cannot use ownership"
        ):
            op.validate_candidate(
                owned_replaceable_access, manifest, self.run_dir
            )

    def test_research_control_status_cannot_overstate_unknown_assessment(self) -> None:
        candidate = self.candidate(
            "unknown-control-assessment", discovery_lane="weak-signal"
        )
        _, canonical = self.store_candidate(candidate)
        research = self.research(canonical)
        research["claims"].append(
            {
                "claim_id": "unknown-control-proof",
                "statement": "Control-point ownership could not be established.",
                "assessment": "unknown",
                "evidence_refs": [],
            }
        )
        research["critical_control_point_assessment"] = {
            "status": "owned",
            "assessment": "unknown",
            "claim_ids": ["unknown-control-proof"],
            "source_ids": [],
        }
        with self.assertRaisesRegex(
            op.InputError, "explicit unknown assessment requires status unknown"
        ):
            op.validate_research(research, self.load()[0], self.run_dir)

    def test_scout_contract_exposes_rejected_lane_and_owner_combinations(self) -> None:
        op.advance_run(self.run_dir)
        contract, valid = op.preflight_artifact(self.run_dir, "candidate")
        self.assertTrue(valid)
        constraints = contract["constraints"]
        lane_rule = constraints["mechanism_first_contract"]
        for required in (
            "externally_controlled",
            "paid_event_or_measurable_loss unknown",
            "confidential_employer_resource_dependency present",
            "Never relabel",
        ):
            self.assertIn(required, lane_rule)
        owner_rule = constraints["customer_relationship_owner_agreement"]
        self.assertIn("critical_control_point.customer_relationship_owner", owner_rule)
        self.assertIn("commercial_mechanics.customer_relationship_owner", owner_rule)

        candidate = self.candidate("scout-contract")
        path = self.root / "scout-response.json"
        variants = []
        external = copy.deepcopy(candidate)
        external["critical_control_point"].update(
            status="externally_controlled", mechanism_control="dependent"
        )
        variants.append((external, "externally controlled mechanism"))
        no_event = copy.deepcopy(candidate)
        no_event["commercial_mechanics"]["paid_event_or_measurable_loss"] = "unknown"
        variants.append((no_event, "existing paid event"))
        employer = copy.deepcopy(candidate)
        employer["critical_control_point"]["confidential_employer_resource_dependency"] = "present"
        variants.append((employer, "confidential employer resources"))
        mismatched_owner = copy.deepcopy(candidate)
        mismatched_owner["commercial_mechanics"]["customer_relationship_owner"] = "unrelated owner"
        variants.append((mismatched_owner, "customer_relationship_owner must agree"))
        for response, expected in variants:
            with self.subTest(expected=expected):
                path.write_bytes(op.canonical_json_bytes(response))
                report, valid = op.preflight_artifact(
                    self.run_dir, "candidate", path, "discover-contract"
                )
                self.assertFalse(valid)
                self.assertIn(expected, report["validation"]["errors"][0]["message"])

        uncertain = copy.deepcopy(candidate)
        uncertain["critical_control_point"].update(
            status="unknown", mechanism_control="unknown",
            acquisition_instrument_type="unknown",
        )
        path.write_bytes(op.canonical_json_bytes(uncertain))
        report, valid = op.preflight_artifact(
            self.run_dir, "candidate", path, "discover-contract"
        )
        self.assertTrue(valid, report["validation"]["errors"])
        self.assertEqual(self.load()[1]["jobs"]["discovery"], {})

    def test_research_contract_exposes_validator_source_classes(self) -> None:
        self.set_stage("research")
        candidate = self.candidate("research-contract")
        self.store_candidate(candidate)
        research = self.research(candidate)
        contract, valid = op.preflight_artifact(self.run_dir, "research")
        self.assertTrue(valid)
        mapping = contract["constraints"]["commercial_evidence_source_classes"]
        self.assertEqual(set(mapping), set(research["commercial_evidence"]))
        self.assertIn("same assessment", contract["constraints"]["claim_source_coverage"])
        for category, classes in mapping.items():
            source_id = research["commercial_evidence"][category]["source_ids"][0]
            for evidence_class in classes:
                with self.subTest(category=category, evidence_class=evidence_class):
                    response = copy.deepcopy(research)
                    next(s for s in response["sources"] if s["source_id"] == source_id)["evidence_class"] = evidence_class
                    op.validate_research(response, self.load()[0], self.run_dir)
            response = copy.deepcopy(research)
            next(s for s in response["sources"] if s["source_id"] == source_id)["evidence_class"] = "market_context"
            with self.assertRaisesRegex(op.InputError, "matching bounded evidence_class"):
                op.validate_research(response, self.load()[0], self.run_dir)

    def test_preflight_correction_blocks_changed_judgments_without_attempt(self) -> None:
        self.set_stage("research")
        candidate = self.candidate("correction-guard")
        self.store_candidate(candidate)
        research = self.research(candidate)
        research["claims"].append({
            "claim_id": "unknown-buyer", "statement": "No exact-offer buyer validation.",
            "assessment": "unknown", "evidence_refs": [],
        })
        first = self.root / "first-response.json"
        corrected = self.root / "corrected.json"
        first.write_bytes(op.canonical_json_bytes(research))
        before_state = (self.run_dir / "state.json").read_bytes()
        before_events = (self.run_dir / "events.jsonl").read_bytes()
        selection = {"candidate_refs": [{
            "candidate_id": candidate["candidate_id"], "version": 1,
            "candidate_sha256": research["candidate_sha256"],
        }]}
        changed = copy.deepcopy(research)
        changed["commercial_evidence"]["buyer_or_paid_event"] = {
            "status": "unknown", "claim_ids": ["unknown-buyer"], "source_ids": [],
        }
        corrected.write_bytes(op.canonical_json_bytes(changed))
        with mock.patch.object(op, "effective_portfolio_selection", return_value=selection):
            # The altered research is canonically valid, but not a permitted correction.
            self.assertTrue(op.preflight_artifact(
                self.run_dir, "research", corrected, "research-guard",
            )[1])
            code, report, error = self.run_cli([
                "--runs-dir", str(self.runs_dir), "preflight", self.run_id,
                "--kind", "research", "--job-id", "research-guard",
                "--input", str(corrected), "--original-input", str(first),
            ])
            self.assertEqual(code, 2, error)
            validation = report["validation"]
            self.assertFalse(validation["schema_retry_required"])
            self.assertNotIn("preflight_receipt", validation)
            self.assertEqual(validation["errors"][0]["code"], "semantic_correction_forbidden")
            self.assertEqual(validation["errors"][0]["pointer"], "/commercial_evidence/buyer_or_paid_event/status")

            # A wrong reference can be repaired without changing the evidence judgment.
            original = copy.deepcopy(research)
            original["commercial_evidence"]["buyer_or_paid_event"]["claim_ids"] = ["research-claim-2"]
            first.write_bytes(op.canonical_json_bytes(original))
            corrected.write_text(json.dumps(research, indent=4), encoding="utf-8")
            report, valid = op.preflight_artifact(
                self.run_dir, "research", corrected, "research-guard", first,
            )
            self.assertTrue(valid, report["validation"]["errors"])
            self.assertTrue(report["validation"]["correction_content_preserved"])
            self.assertEqual(report["validation"]["original_input_sha256"], op.sha256_file(first))
            self.assertIn("preflight_receipt", report["validation"])
        self.assertEqual((self.run_dir / "state.json").read_bytes(), before_state)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), before_events)
        for key, value in [("assessment", "inference"), ("statement", "Changed finding")]:
            changed = copy.deepcopy(research)
            changed["claims"][0][key] = value
            self.assertTrue(op.correction_content_differences(research, changed, "research"))
        changed = copy.deepcopy(research)
        changed["sources"][0]["evidence_class"] = "other"
        self.assertTrue(op.correction_content_differences(research, changed, "research"))
        self.assertTrue(op.correction_content_differences({"score": 4}, {"score": 5}, "evaluation"))

    def research_supplement_fixture(self) -> tuple[dict, dict, dict]:
        self.set_stage("research")
        candidate = self.candidate("research-supplement")
        self.store_candidate(candidate)
        original = self.research(candidate)
        original["sources"][1]["evidence_class"] = "market_context"
        supplemented = copy.deepcopy(original)
        source = copy.deepcopy(original["sources"][1])
        source.update(source_id="new-distribution", url="https://example.org/new-channel",
                      title="New channel evidence", evidence_class="distribution")
        supplemented["sources"].append(source)
        supplemented["claims"].append({
            "claim_id": "new-channel-finding", "statement": "A documented channel exists; access is unvalidated.",
            "assessment": "evidence", "evidence_refs": ["new-distribution"],
        })
        coverage = supplemented["commercial_evidence"]["distribution_and_acquisition"]
        coverage["claim_ids"].append("new-channel-finding")
        coverage["source_ids"].append("new-distribution")
        return candidate, original, supplemented

    def test_research_supplement_cli_preserves_original_and_completion(self) -> None:
        candidate, original, supplemented = self.research_supplement_fixture()
        first = self.root / "first-research.json"
        last = self.root / "supplemented-research.json"
        first.write_bytes(op.canonical_json_bytes(original))
        last.write_bytes(op.canonical_json_bytes(supplemented))
        before = [(self.run_dir / name).read_bytes() for name in ("state.json", "events.jsonl")]
        selection = {"candidate_refs": [self.candidate_ref(candidate)]}
        args = ["--runs-dir", str(self.runs_dir), "preflight", self.run_id,
                "--kind", "research", "--job-id", "research-supplement",
                "--input", str(last), "--original-input", str(first)]
        with mock.patch.object(op, "effective_portfolio_selection", return_value=selection):
            code, report, error = self.run_cli(args)
            self.assertEqual(code, 2, error)  # Default corrections still reject additions.
            self.assertNotIn("preflight_receipt", report["validation"])
            code, report, error = self.run_cli(args + ["--research-supplement"])
            self.assertEqual(code, 0, error)
            self.assertEqual(report["research_supplement"]["added_source_ids"], ["new-distribution"])
            self.assertEqual(report["validation"]["original_input_sha256"], op.sha256_file(first))
            self.assertTrue(report["validation"]["correction_content_preserved"])
            self.assertEqual(before, [(self.run_dir / name).read_bytes() for name in ("state.json", "events.jsonl")])
            op.start_job(self.run_dir, "research-supplement", None)
            op.complete_job(
                self.run_dir, "research-supplement", last, "research",
                report["validation"]["input_sha256"],
                report["validation"]["preflight_receipt"]["receipt_sha256"],
            )
            stored = op.load_json(self.run_dir / op.research_relpath(candidate["candidate_id"], 1))
            self.assertEqual(stored["sources"][:len(original["sources"])], original["sources"])
            code, report, error = self.run_cli(args + ["--research-supplement"])
            self.assertEqual(code, 2, error)
            self.assertIn("already admitted", str(report["validation"]["errors"]))

    def test_research_supplement_rejects_rewritten_or_reused_evidence(self) -> None:
        _, original, supplemented = self.research_supplement_fixture()
        manifest, state = self.load()
        def verify(value: dict) -> dict:
            return op.validate_research_supplement(original, value, manifest, state, self.run_dir)
        self.assertEqual(verify(supplemented)["added_claim_ids"], ["new-channel-finding"])
        variants = []
        def changed(label: str, mutate) -> None:
            value = copy.deepcopy(supplemented)
            mutate(value)
            variants.append((label, value))
        changed("source class", lambda v: v["sources"][1].update(evidence_class="distribution"))
        changed("claim", lambda v: v["claims"][0].update(statement="Better finding"))
        changed("status", lambda v: v["critical_control_point_assessment"].update(status="unknown"))
        changed("unknowns", lambda v: v.update(unknowns=[]))
        changed("contrary evidence", lambda v: v.update(contrary_evidence=[]))
        changed("removed refs", lambda v: v["commercial_evidence"]["distribution_and_acquisition"].update(
            claim_ids=["new-channel-finding"], source_ids=["new-distribution"]))
        changed("duplicate URL", lambda v: v["sources"][-1].update(url=original["sources"][0]["url"] + "#different"))
        changed("duplicate source ID", lambda v: v["sources"][-1].update(source_id="source-0"))
        changed("duplicate claim ID", lambda v: v["claims"][-1].update(claim_id="research-claim-1"))
        changed("no new evidence for claim", lambda v: v["claims"][-1].update(evidence_refs=["source-1"]))
        changed("no new claims", lambda v: v.update(claims=v["claims"][:-1]))
        changed("source limit", lambda v: v["sources"].extend([v["sources"][-1]] * manifest["config"]["sources_max"]))
        for label, value in variants:
            with self.subTest(label=label), self.assertRaises(op.WorkflowError):
                verify(value)

    def test_research_supplement_requires_invalid_original_and_explicit_scope(self) -> None:
        _, original, supplemented = self.research_supplement_fixture()
        manifest, state = self.load()
        valid_original = copy.deepcopy(original)
        valid_original["sources"][1]["evidence_class"] = "distribution"
        valid_supplement = copy.deepcopy(supplemented)
        valid_supplement["sources"][1]["evidence_class"] = "distribution"
        with self.assertRaisesRegex(op.InputError, "valid original"):
            op.validate_research_supplement(valid_original, valid_supplement, manifest, state, self.run_dir)
        with self.assertRaisesRegex(op.InputError, "only during research"):
            op.validate_research_supplement(original, supplemented, manifest, {**state, "stage": "development"}, self.run_dir)
        with self.assertRaisesRegex(op.InputError, "requires --kind research"):
            op.preflight_artifact(self.run_dir, "candidate", research_supplement=True)
        with self.assertRaisesRegex(op.InputError, "requires --kind research"):
            op.preflight_artifact(self.run_dir, "research", research_supplement=True)
        for changed_type in (True, 1.0):
            invalid_identity = copy.deepcopy(original)
            invalid_identity["candidate_version"] = changed_type
            with self.subTest(version=changed_type), self.assertRaisesRegex(op.InputError, "original authored content"):
                op.validate_research_supplement(invalid_identity, supplemented, manifest, state, self.run_dir)

    def test_research_supplement_can_supply_missing_source_without_rewriting_claim(self) -> None:
        _, original, supplemented = self.research_supplement_fixture()
        original["claims"][0]["evidence_refs"].append("new-distribution")
        supplemented["claims"][0] = copy.deepcopy(original["claims"][0])
        manifest, state = self.load()
        result = op.validate_research_supplement(original, supplemented, manifest, state, self.run_dir)
        self.assertEqual(result["added_source_ids"], ["new-distribution"])

    def test_redesign_research_fragments_bind_listed_parent_research(self) -> None:
        self.set_stage("development")
        base = self.candidate("research-fragments")
        base_path, _ = self.store_candidate(base)
        research = self.research(base)
        research_path = self.store_research(research)
        candidate = self.candidate(
            base["candidate_id"], version=2, stage="development",
            parent={"candidate_id": base["candidate_id"], "version": 1},
        )
        source = f"runs/{self.run_id}/{research_path.relative_to(self.run_dir).as_posix()}"
        reference = f"{source}#{research['claims'][0]['claim_id']}"
        candidate["source_refs"].append(source)
        candidate["claims"][0]["evidence_refs"] = [reference]
        original = self.root / "research-fragment-original.json"
        original.write_bytes(op.canonical_json_bytes(candidate))
        before_state = (self.run_dir / "state.json").read_bytes()
        before_events = (self.run_dir / "events.jsonl").read_bytes()
        decision = {"candidate_decisions": [{
            "candidate_id": base["candidate_id"], "candidate_version": 1,
            "candidate_sha256": op.sha256_file(base_path), "disposition": "develop",
        }]}
        with mock.patch.object(op, "_load_portfolio_decision", return_value=decision), mock.patch.object(
            op, "_working_evaluations_for_candidate", return_value=[{}],
        ):
            report, valid = op.preflight_artifact(
                self.run_dir, "candidate", original, "research-fragment", original,
            )
        self.assertTrue(valid, report["validation"]["errors"])
        self.assertTrue(report["validation"]["correction_content_preserved"])
        self.assertEqual(report["validation"]["input_sha256"], op.sha256_file(original))
        manifest, _ = self.load()
        canonical = op.validate_candidate(candidate, manifest, self.run_dir)
        self.assertEqual(canonical["claims"], candidate["claims"])
        self.assertEqual(canonical["source_refs"], candidate["source_refs"])
        invalid = [
            (source, f"{source}#missing-claim"),
            (source, f"{source}#"),
            (source.replace(self.run_id, "another-run"), reference.replace(self.run_id, "another-run")),
            (source.replace("research-fragments", "another-candidate"), reference.replace("research-fragments", "another-candidate")),
            (source.replace("v1.json", "v2.json"), reference.replace("v1.json", "v2.json")),
            ("https://example.com/report", "https://example.com/report#research-claim-1"),
        ]
        for listed, cited in invalid:
            with self.subTest(cited=cited):
                changed = copy.deepcopy(candidate)
                changed["source_refs"][-1] = listed
                changed["claims"][0]["evidence_refs"] = [cited]
                with self.assertRaisesRegex(op.InputError, "unknown source_refs"):
                    op.validate_candidate(changed, manifest, self.run_dir)
        unlisted = copy.deepcopy(candidate)
        unlisted["source_refs"].remove(source)
        with self.assertRaisesRegex(op.InputError, "unknown source_refs"):
            op.validate_candidate(unlisted, manifest, self.run_dir)
        tampered = copy.deepcopy(research)
        tampered["candidate_sha256"] = "0" * 64
        research_path.write_bytes(op.canonical_json_bytes(tampered))
        with self.assertRaisesRegex(op.InputError, "immutable candidate"):
            op.validate_candidate(candidate, manifest, self.run_dir)
        research_path.write_bytes(op.canonical_json_bytes(research))
        self.assertEqual((self.run_dir / "state.json").read_bytes(), before_state)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), before_events)

    def test_redesign_contract_and_derived_declaration_repair(self) -> None:
        self.set_stage("development")
        base = self.candidate("declaration-repair")
        base_path, _ = self.store_candidate(base)
        self.store_research(self.research(base))
        candidate = self.candidate(
            "declaration-repair", version=2, stage="development",
            parent={"candidate_id": "declaration-repair", "version": 1},
        )
        contract, _ = op.preflight_artifact(self.run_dir, "candidate")
        self.assertEqual(
            set(contract["enums"]["/redesign/changed_structural_fields/*"]),
            op.STRUCTURAL_CHANGE_FIELDS,
        )
        self.assertEqual(
            set(contract["enums"]["/redesign/changed_fingerprint_fields/*"]),
            op.FINGERPRINT_KEYS,
        )
        self.assertIn("immutable parent", contract["constraints"]["redesign_change_declarations"])
        original = copy.deepcopy(candidate)
        original["redesign"]["changed_structural_fields"] = ["commercial_archetype"]
        original["redesign"]["changed_fingerprint_fields"] = ["thesis"]
        first = self.root / "first-redesign.json"
        corrected = self.root / "corrected-redesign.json"
        first.write_bytes(op.canonical_json_bytes(original))
        corrected.write_bytes(op.canonical_json_bytes(candidate))
        before_state = (self.run_dir / "state.json").read_bytes()
        before_events = (self.run_dir / "events.jsonl").read_bytes()
        decision = {"candidate_decisions": [{
            "candidate_id": base["candidate_id"], "candidate_version": 1,
            "candidate_sha256": op.sha256_file(base_path), "disposition": "develop",
        }]}
        with mock.patch.object(op, "_load_portfolio_decision", return_value=decision), mock.patch.object(
            op, "_working_evaluations_for_candidate", return_value=[{}],
        ):
            rejected, valid = op.preflight_artifact(
                self.run_dir, "candidate", first, "redesign-declarations", first,
            )
            self.assertFalse(valid)
            self.assertEqual(rejected["validation"]["errors"][0]["code"], "canonical_validation")
            report, valid = op.preflight_artifact(
                self.run_dir, "candidate", corrected, "redesign-declarations", first,
            )
            self.assertTrue(valid, report["validation"]["errors"])
            self.assertTrue(report["validation"]["correction_content_preserved"])
            self.assertIn("preflight_receipt", report["validation"])

            # An allowed field name still fails if it does not describe actual changes.
            wrong = copy.deepcopy(candidate)
            wrong["redesign"]["changed_structural_fields"] = ["critical_control_point"]
            corrected.write_bytes(op.canonical_json_bytes(wrong))
            report, valid = op.preflight_artifact(
                self.run_dir, "candidate", corrected, "redesign-declarations", first,
            )
            self.assertFalse(valid)
            self.assertIn("exactly match", report["validation"]["errors"][0]["message"])
            self.assertNotIn("preflight_receipt", report["validation"])

            # Canonically valid substantive changes cannot accompany a declaration repair.
            changed = copy.deepcopy(candidate)
            changed["economics"]["pricing"] = "Unsupported improved pricing"
            corrected.write_bytes(op.canonical_json_bytes(changed))
            self.assertTrue(op.preflight_artifact(
                self.run_dir, "candidate", corrected, "redesign-declarations",
            )[1])
            report, valid = op.preflight_artifact(
                self.run_dir, "candidate", corrected, "redesign-declarations", first,
            )
            self.assertFalse(valid)
            self.assertIn("semantic_correction_forbidden", [e["code"] for e in report["validation"]["errors"]])
            self.assertNotIn("preflight_receipt", report["validation"])
        self.assertEqual((self.run_dir / "state.json").read_bytes(), before_state)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), before_events)

    def test_malformed_research_preflight_is_attempt_neutral(self) -> None:
        self.set_stage("research")
        malformed = self.root / "malformed-research.json"
        malformed.write_text("{", encoding="utf-8")
        state_before = (self.run_dir / "state.json").read_bytes()
        events_before = (self.run_dir / "events.jsonl").read_bytes()
        report, valid = op.preflight_artifact(
            self.run_dir,
            "research",
            malformed,
            "research-malformed",
        )
        self.assertFalse(valid)
        self.assertIn(
            "invalid JSON",
            report["validation"]["errors"][0]["message"],
        )
        self.assertEqual((self.run_dir / "state.json").read_bytes(), state_before)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), events_before)

    def test_preflight_receipt_is_required_persisted_and_checked(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate("receipt-bound")
        path = self.root / "receipt-bound.json"
        path.write_bytes(op.canonical_json_bytes(candidate))

        missing_identity, valid = op.preflight_artifact(
            self.run_dir,
            "candidate",
            path,
        )
        self.assertFalse(valid)
        self.assertEqual(
            missing_identity["validation"]["errors"][0]["code"],
            "job_id_required",
        )

        report, valid = op.preflight_artifact(
            self.run_dir,
            "candidate",
            path,
            "receipt-bound",
        )
        self.assertTrue(valid)
        receipt = report["validation"]["preflight_receipt"]
        self.assertEqual(receipt["input_sha256"], op.sha256_file(path))

        op.start_job(self.run_dir, "receipt-bound", "discovery")
        with self.assertRaisesRegex(
            op.InputError,
            "structured job completion requires",
        ):
            op.complete_job(
                self.run_dir,
                "receipt-bound",
                path,
                "candidate",
            )
        self.assertEqual(
            self.load()[1]["jobs"]["discovery"]["receipt-bound"]["status"],
            "running",
        )
        with self.assertRaisesRegex(op.ConflictError, "receipt differs"):
            op.complete_job(
                self.run_dir,
                "receipt-bound",
                path,
                "candidate",
                receipt["input_sha256"],
                "0" * 64,
            )

        code, completed, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "job",
                self.run_id,
                "receipt-bound",
                "complete",
                "--input",
                str(path),
                "--kind",
                "candidate",
                "--preflight-sha256",
                receipt["input_sha256"],
                "--preflight-receipt-sha256",
                receipt["receipt_sha256"],
            ]
        )
        self.assertEqual(code, 0, error)
        self.assertEqual(
            receipt["canonical_artifact_sha256"],
            completed["artifact_sha256"],
        )
        events_path = self.run_dir / "events.jsonl"
        events = op.load_events(events_path, self.run_id)
        completion = next(
            event
            for event in events
            if event["event"] == "job_completed"
            and event["job_id"] == "receipt-bound"
        )
        self.assertEqual(completion["details"]["preflight_receipt"], receipt)
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

        completion["details"]["preflight_receipt"]["input_sha256"] = "f" * 64
        events_path.write_text(
            "".join(
                json.dumps(event, sort_keys=True) + "\n" for event in events
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            op.InputError,
            "preflight receipt differs from its immutable context",
        ):
            op.check_run(self.run_dir, self.config_path)

    def test_lane_balanced_score_bracket_and_strict_version_competition(self) -> None:
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "discovery")
        config = self.load()[0]["config"]
        candidates: dict[str, dict] = {}
        for lane in config["discovery_lanes"]:
            for index in range(config["seeds_per_scout"]):
                candidate_id = f"{lane}-{index:02d}"
                candidate = self.candidate(
                    candidate_id,
                    discovery_lane=lane,
                )
                candidates[candidate_id] = candidate

        # The pool dedup is fingerprint-based.  This later structural duplicate
        # exercises winner dedup plus same-batch score backfill.
        candidates["future-backcast-02"]["structural_signature"] = copy.deepcopy(
            candidates["future-backcast-00"]["structural_signature"]
        )
        for candidate in candidates.values():
            self.store_candidate(candidate)

        dedup = op.dedup_run(self.run_dir)
        self.assertEqual(dedup["exact_fingerprint_unique_count"], 36)
        self.assertEqual(dedup["semantic_signature_unique_count"], 35)
        self.assertIn(
            [
                {"candidate_id": "future-backcast-00", "version": 1},
                {"candidate_id": "future-backcast-02", "version": 1},
            ],
            dedup["semantic_collision_groups"],
        )
        self.assertEqual(dedup["mechanism_first_founder_access_count"], 12)
        self.assertEqual(
            dedup["unique_lane_counts"],
            {lane: 12 for lane in config["discovery_lanes"]},
        )
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "calibration")

        manifest, _ = self.load()
        batches = op.load_screening_batches(self.run_dir, manifest)
        self.assertEqual(len(batches["batches"]), 6)
        for batch in batches["batches"]:
            lane_counts = {lane: 0 for lane in config["discovery_lanes"]}
            for ref in batch["candidate_refs"]:
                lane_counts[candidates[ref["candidate_id"]]["discovery_lane"]] += 1
            self.assertEqual(set(lane_counts.values()), {2})

        context = op.screening_batch_context(self.run_dir, "batch-01")
        context_text = json.dumps(context, sort_keys=True)
        self.assertEqual(len(context["candidates"]), 6)
        self.assertNotIn("future-backcast-02", context_text)
        self.assertNotIn("final_score", context_text)
        self.assertNotIn("ranking", context_text)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = op.main(
                [
                    "--runs-dir",
                    str(self.runs_dir),
                    "status",
                    self.run_id,
                    "--batch",
                    "batch-01",
                ]
            )
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["batch_id"], "batch-01")

        for batch_index, batch in enumerate(batches["batches"]):
            for rank_index, ref in enumerate(batch["candidate_refs"]):
                self.complete_evaluation_job(
                    f"screen-{batch_index + 1:02d}-{rank_index + 1:02d}",
                    candidates[ref["candidate_id"]],
                    f"screening-judge-{batch_index + 1:02d}",
                    9.0 - rank_index * 0.2 - batch_index * 0.01,
                    "working_screening",
                )
        screening = op.working_evaluation_coverage(
            self.run_dir, manifest, "screening"
        )
        self.assertTrue(screening["complete"])
        self.assertEqual(screening["candidate_count"], 36)
        self.assertEqual(len({row["judge_id"] for row in screening["batches"]}), 6)

        secondary_required = op.advance_run(self.run_dir)
        self.assertEqual(secondary_required["stage"], "calibration")
        self.assertTrue(secondary_required["secondary_screening_required"])
        resumed_secondary = op.advance_run(self.run_dir)
        self.assertTrue(resumed_secondary["idempotent"])
        self.assertEqual(
            sum(
                event["event"] == "secondary_screening_planned"
                for event in op.load_events(
                    self.run_dir / "events.jsonl", self.run_id
                )
            ),
            1,
        )
        plan = op.load_secondary_screening_plan(self.run_dir, manifest)
        self.assertTrue(plan["batches"])
        secondary_context = op.secondary_screening_batch_context(
            self.run_dir, plan["batches"][0]["secondary_batch_id"]
        )
        secondary_context_text = json.dumps(secondary_context, sort_keys=True)
        for forbidden in (
            "primary_inputs",
            "primary_score",
            "cutoff_margin",
            "rank",
            "rationale",
        ):
            self.assertNotIn(forbidden, secondary_context_text)
        first_secondary_ref = plan["batches"][0]["candidate_refs"][0]
        primary_evaluation = op.load_json(
            self.run_dir
            / plan["batches"][0]["primary_inputs"][0]["evaluation_path"]
        )
        reused_response = self.evaluation_input(
            candidates[first_secondary_ref["candidate_id"]],
            primary_evaluation["judge_id"],
            score=primary_evaluation["final_score"],
            evaluation_type="working_screening_secondary",
        )
        reused_response.pop("_test_evaluation_type")
        reused_path = self.root / "secondary-reused-primary.json"
        reused_path.write_text(json.dumps(reused_response), encoding="utf-8")
        with self.assertRaisesRegex(
            op.ConflictError, "fresh from primary screening"
        ):
            op._artifact_for_input(
                self.run_dir,
                manifest,
                self.load()[1],
                "secondary-reused-primary",
                reused_path,
                "secondary-evaluation",
            )
        for batch_index, batch in enumerate(plan["batches"], start=1):
            primary_scores = {
                item["candidate_ref"]["candidate_id"]: item["final_score"]
                for item in batch["primary_inputs"]
            }
            for ref in batch["candidate_refs"]:
                self.complete_evaluation_job(
                    f"secondary-{batch_index:02d}-{ref['candidate_id']}",
                    candidates[ref["candidate_id"]],
                    f"secondary-judge-{batch_index:02d}",
                    primary_scores[ref["candidate_id"]],
                    "working_screening_secondary",
                )
        secondary = op.working_evaluation_coverage(
            self.run_dir, manifest, "screening_secondary"
        )
        self.assertTrue(secondary["complete"])
        real_write_immutable = op.write_immutable
        failed_selection_write = False

        def fail_selection_once(path, data, **kwargs):
            nonlocal failed_selection_write
            if (
                Path(path) == self.run_dir / "portfolio" / "selection.json"
                and not failed_selection_write
            ):
                failed_selection_write = True
                raise OSError("simulated selection write interruption")
            return real_write_immutable(path, data, **kwargs)

        with mock.patch.object(
            op, "write_immutable", side_effect=fail_selection_once
        ):
            with self.assertRaisesRegex(
                OSError, "simulated selection write interruption"
            ):
                op.advance_run(self.run_dir)
        self.assertEqual(self.load()[1]["stage"], "calibration")
        self.assertEqual(
            sum(
                event["event"] == "screening_aggregation_completed"
                for event in op.load_events(
                    self.run_dir / "events.jsonl", self.run_id
                )
            ),
            1,
        )
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "research")
        self.assertEqual(
            sum(
                event["event"] == "screening_aggregation_completed"
                for event in op.load_events(
                    self.run_dir / "events.jsonl", self.run_id
                )
            ),
            1,
        )
        aggregation = op.load_screening_aggregation(self.run_dir, manifest)
        self.assertEqual(aggregation["rule"], "mean")
        for row in aggregation["candidates"]:
            if row["secondary_score"] is not None:
                self.assertEqual(row["canonical_score"], row["primary_score"])
        selection = op.effective_portfolio_selection(self.run_dir, manifest)
        selected_ids = [ref["candidate_id"] for ref in selection["candidate_refs"]]
        self.assertEqual(len(selected_ids), 12)
        self.assertNotIn("future-backcast-02", selected_ids)
        self.assertIn("mechanism-first-02", selected_ids)
        self.assertEqual(selection["wildcard_candidate_refs"], [])

        ordered_selected = sorted(selected_ids)
        externally_controlled_id = ordered_selected[1]
        for candidate_id in ordered_selected:
            candidate = candidates[candidate_id]
            research = self.research(candidate)
            if candidate_id == externally_controlled_id:
                research["critical_control_point_assessment"]["status"] = (
                    "externally_controlled"
                )
            self.store_research(research)
        research_scores = {
            candidate_id: (
                8.0
                if index < 3
                else 7.5
                if index < 5
                else 6.0 - index * 0.01
            )
            for index, candidate_id in enumerate(ordered_selected)
        }
        for index, candidate_id in enumerate(ordered_selected):
            self.complete_evaluation_job(
                f"research-{index + 1:02d}",
                candidates[candidate_id],
                f"research-judge-{index + 1:02d}",
                research_scores[candidate_id],
                "working_research",
            )
        expected_develop = set(ordered_selected[:4])
        decision = self.portfolio_decision(
            [candidates[candidate_id] for candidate_id in ordered_selected],
            expected_develop,
        )
        self.complete_json_job("portfolio-decision", "portfolio-decision", decision)
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "development")

        developed_ids = sorted(expected_develop)
        paired_scores = [
            ((8.0, 8.1), (7.0, 7.1)),
            ((7.5, 7.6), (8.2, 8.2)),
            ((7.8, 7.9), (7.8, 8.0)),
            ((7.0, 7.2), None),
        ]
        for index, (candidate_id, scores) in enumerate(
            zip(developed_ids, paired_scores, strict=True), start=1
        ):
            base = candidates[candidate_id]
            if index == 1:
                constructor_context = op.constructor_context(
                    self.run_dir, candidate_id
                )
                constructor_text = json.dumps(
                    constructor_context, sort_keys=True
                )
                self.assertEqual(
                    set(constructor_context),
                    {
                        "scope",
                        "candidate",
                        "candidate_artifact",
                        "research",
                        "research_artifact",
                        "founder_snapshot",
                        "response_kind",
                    },
                )
                for field in ("candidate", "research"):
                    binding = constructor_context[f"{field}_artifact"]
                    bound_path = self.run_dir / binding["path"]
                    self.assertEqual(op.sha256_file(bound_path), binding["sha256"])
                    self.assertEqual(op.load_json(bound_path), constructor_context[field])
                for forbidden in (
                    "final_score",
                    "ranking",
                    "threshold",
                    "rubric",
                    "qualification",
                ):
                    self.assertNotIn(forbidden, constructor_text)
            if scores[1] is None:
                self.complete_json_job(
                    f"constructor-{index:02d}",
                    "development-result",
                    self.development_result(
                        base,
                        constructor_id=f"constructor-agent-{index:02d}",
                        outcome="no_valid_redesign",
                        base_candidate=base,
                    ),
                )
                for judge_offset, judge_suffix in enumerate(("a", "b")):
                    self.complete_evaluation_job(
                        f"development-base-{index:02d}-{judge_suffix}",
                        base,
                        f"development-judge-{index:02d}-{judge_suffix}",
                        scores[0][judge_offset],
                        "working_development",
                    )
                continue
            redesign = copy.deepcopy(base)
            redesign.update(
                {
                    "version": 2,
                    "parent": {"candidate_id": candidate_id, "version": 1},
                    "stage": "development",
                    "redesign": {
                        "changed_fingerprint_fields": ["offer_and_business_model"],
                        "economic_effect": "Changes the recorded repeat economics.",
                    },
                }
            )
            redesign["fingerprint"]["offer_and_business_model"] += " redesigned"
            redesign["economics"]["pricing"] = "150000 PLN redesigned contract"
            redesign["commercial_mechanics"]["fully_loaded_economics"][
                "revenue_basis"
            ] = "150000 PLN redesigned contract"
            redesign["redesign"]["changed_structural_fields"] = [
                "commercial_mechanics"
            ]
            if index == 1:
                # This redesign loses: its weaker control status must not leak
                # into the final report for the selected original version.
                redesign["critical_control_point"]["status"] = "unknown"
                redesign["redesign"]["changed_structural_fields"].append("critical_control_point")
            if candidate_id == externally_controlled_id:
                redesign["critical_control_point"].update(
                    {
                        "status": "externally_controlled",
                        "mechanism_control": "dependent",
                        "current_owner": "Independent counterparty",
                        "launch_controller": "Independent counterparty",
                        "acquisition_instrument_type": "long_term_contract",
                        "acquisition_instrument": "A signed launch-time control agreement.",
                        "counterparty_refusal_fallback": "Use a replaceable qualified counterparty.",
                    }
                )
                redesign["redesign"]["changed_structural_fields"].append(
                    "critical_control_point"
                )
                blocked_path = self.root / "externally-controlled-redesign.json"
                blocked_path.write_text(json.dumps(redesign), encoding="utf-8")
                blocked, valid = op.preflight_artifact(
                    self.run_dir,
                    "candidate",
                    blocked_path,
                    f"redesign-{index:02d}",
                )
                self.assertFalse(valid)
                self.assertEqual(blocked["attempts_consumed"], 0)
                self.assertIn(
                    "must change from externally_controlled",
                    blocked["validation"]["errors"][0]["message"],
                )
                self.assertFalse(
                    (
                        self.run_dir
                        / op.candidate_relpath(candidate_id, redesign["version"])
                    ).exists()
                )

                redesign["critical_control_point"].update(
                    {
                        "status": "unknown",
                        "launch_controller": "unknown",
                        "acquisition_instrument_type": "unknown",
                        "acquisition_instrument": "unknown",
                    }
                )
                blocked_path.write_text(json.dumps(redesign), encoding="utf-8")
                blocked, valid = op.preflight_artifact(
                    self.run_dir,
                    "candidate",
                    blocked_path,
                    f"redesign-{index:02d}",
                )
                self.assertFalse(valid)
                self.assertEqual(blocked["attempts_consumed"], 0)
                self.assertIn(
                    "acquisition_instrument_type",
                    blocked["validation"]["errors"][0]["message"],
                )

                redesign["critical_control_point"].update(
                    {
                        "launch_controller": "The business after the agreement is signed.",
                        "acquisition_instrument_type": "long_term_contract",
                        "acquisition_instrument": "A signed launch-time control agreement.",
                    }
                )
            self.complete_json_job(f"redesign-{index:02d}", "candidate", redesign)
            self.complete_json_job(
                f"constructor-{index:02d}",
                "development-result",
                self.development_result(
                    redesign,
                    constructor_id=f"constructor-agent-{index:02d}",
                    outcome="redesigned",
                    base_candidate=base,
                ),
            )
            if index == 1:
                lineage_context = op.development_lineage_context(
                    self.run_dir, candidate_id
                )
                self.assertEqual(len(lineage_context["candidates"]), 2)
                self.assertEqual(len(lineage_context["candidate_artifacts"]), 2)
                for candidate, binding in zip(
                    lineage_context["candidates"],
                    lineage_context["candidate_artifacts"],
                    strict=True,
                ):
                    bound_path = self.run_dir / binding["path"]
                    self.assertEqual(op.sha256_file(bound_path), binding["sha256"])
                    self.assertEqual(op.load_json(bound_path), candidate)
                research_binding = lineage_context["research_artifact"]
                research_path = self.run_dir / research_binding["path"]
                self.assertEqual(op.sha256_file(research_path), research_binding["sha256"])
                self.assertEqual(op.load_json(research_path), lineage_context["research"])
                self.assertEqual(
                    lineage_context["required_independent_evaluators"], 2
                )
                lineage_text = json.dumps(lineage_context, sort_keys=True)
                for forbidden in ("final_score", "ranking", "threshold"):
                    self.assertNotIn(forbidden, lineage_text)
            for judge_offset, judge_suffix in enumerate(("a", "b")):
                judge_id = f"development-judge-{index:02d}-{judge_suffix}"
                self.complete_evaluation_job(
                    f"development-base-{index:02d}-{judge_suffix}",
                    base,
                    judge_id,
                    scores[0][judge_offset],
                    "working_development",
                )
                self.complete_evaluation_job(
                    f"development-redesign-{index:02d}-{judge_suffix}",
                    redesign,
                    judge_id,
                    scores[1][judge_offset],
                    "working_development",
                )

        self.assertEqual(op.advance_run(self.run_dir)["stage"], "frozen")
        version_selection = op.load_version_selection(self.run_dir, manifest)
        rows = {row["candidate_id"]: row for row in version_selection["lineages"]}
        self.assertEqual(
            rows[developed_ids[0]]["selection_reason"],
            "redesign_score_equal_or_lower",
        )
        self.assertEqual(rows[developed_ids[0]]["selected_candidate_ref"]["version"], 1)
        self.assertEqual(
            rows[developed_ids[1]]["selection_reason"],
            "redesign_score_strictly_higher",
        )
        self.assertEqual(rows[developed_ids[1]]["selected_candidate_ref"]["version"], 2)
        self.assertEqual(rows[developed_ids[2]]["selected_candidate_ref"]["version"], 1)
        self.assertEqual(
            rows[developed_ids[2]]["base_conservative_score"], 7.8
        )
        self.assertEqual(
            rows[developed_ids[2]]["redesign_conservative_score"], 7.8
        )
        self.assertEqual(
            rows[developed_ids[3]]["selection_reason"], "no_valid_redesign"
        )

        finalists = op.load_finalist_selection(self.run_dir, manifest)
        finalist_versions = {
            ref["candidate_id"]: ref["version"] for ref in finalists["candidate_refs"]
        }
        self.assertEqual(
            finalist_versions,
            {developed_ids[0]: 1, developed_ids[1]: 2},
        )
        self.assertTrue(op.check_run(self.run_dir, self.config_path)["valid"])

        frozen = op.finalist_candidates(self.run_dir, manifest)
        for _, candidate in frozen:
            op.export_external(self.run_dir, candidate["candidate_id"])
        assignment_destination = self.root / "holdout-response.json"
        assignment = op.native_holdout_assignment(
            self.run_dir,
            frozen[0][1]["candidate_id"],
            assignment_destination,
        )
        self.assertEqual(
            set(assignment),
            {
                "immutable_finalist_packet",
                "strict_response_contract",
                "temporary_response_destination",
            },
        )
        self.assertEqual(
            assignment["temporary_response_destination"],
            str(assignment_destination),
        )
        self.assertFalse(assignment_destination.exists())
        self.assertEqual(
            set(assignment["immutable_finalist_packet"]),
            {"sha256", "content"},
        )
        for forbidden in (
            "workflow_context",
            "preflight_output",
            "prior_evaluations",
            "rankings",
            "competing_candidates",
            "other_judge_output",
            "qualification_rule",
        ):
            self.assertNotIn(forbidden, assignment)
        self.assertEqual(op.advance_run(self.run_dir)["stage"], "holdout")
        for _, candidate in frozen:
            for judge_index in range(2):
                self.store_evaluation(
                    self.evaluation_input(
                        candidate,
                        f"native-{candidate['candidate_id']}-{judge_index + 1}",
                        score=1.0,
                    )
                )
        report, _ = op.finalize_run(self.run_dir)
        self.assertEqual(report["highest_working_score"], 8.2)
        control_rows = {
            row["candidate_id"]: row
            for row in report["portfolio_decision"]["research_contracts"]
        }
        self.assertEqual(control_rows[developed_ids[0]]["final_control_point_status"], "owned")
        self.assertEqual(control_rows[developed_ids[1]]["final_control_point_status"], "unknown")
        op.publish_run(
            self.run_dir,
            self.root / "outcomes",
            self.root / "knowledge",
        )
        published_root = self.root / "outcomes" / self.run_id
        self.assertTrue((published_root / "dedup/report.json").is_file())
        validated = op.validate_published_run_outcome(published_root)
        self.assertIn("dedup/report.json", validated["checked_artifacts"])
        for artifact in (
            "portfolio/secondary-screening.json",
            "portfolio/screening-aggregation.json",
            "portfolio/version-selection.json",
        ):
            self.assertIn(artifact, validated["checked_artifacts"])


class CampaignContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.campaigns_dir = self.root / "campaigns"
        self.outcomes_dir = self.root / "outcomes"
        self.config_path = op.DEFAULT_CONFIG
        created = op.new_campaign(self.config_path, self.campaigns_dir)
        self.campaign_id = created["campaign_id"]
        self.campaign_dir = Path(created["campaign_dir"])
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def metrics(
        self,
        score: float,
        *,
        median: float | None = None,
        missing_archetypes: list[str] | None = None,
    ) -> dict:
        return {
            "official_score": score,
            "top_four_working_median": score if median is None else median,
            "deficient_factors": ["Distribution", "Business model and economics"],
            "missing_archetypes": missing_archetypes or ["asset aggregation"],
        }

    def register_cohort(
        self,
        cohort_number: int,
        metrics: dict,
        *,
        run_status: str = "no_qualifier",
    ) -> dict:
        campaign_manifest, state = op.load_campaign(self.campaign_dir)
        run_id = f"20260825T{cohort_number:06d}Z-{cohort_number:06x}"
        gap_path = None
        gap_digest = None
        if cohort_number > 1:
            gap_path = f"briefs/cohort-{cohort_number}.json"
            brief = {
                "schema_version": op.ACTIVE_SCHEMA_VERSION,
                "campaign_id": self.campaign_id,
                "cohort_number": cohort_number,
                "deficient_factors": state["cohorts"][-1]["deficient_factors"],
                "missing_archetypes": state["cohorts"][-1]["missing_archetypes"],
            }
            brief_file = self.campaign_dir / gap_path
            gap_digest = op.write_immutable(
                brief_file, op.canonical_json_bytes(brief), root=self.campaign_dir
            )
            op._ensure_campaign_event(
                self.campaign_dir,
                self.campaign_id,
                "gap_brief_created",
                {
                    "cohort_number": cohort_number,
                    "gap_brief_sha256": gap_digest,
                },
                identity={"cohort_number": cohort_number},
            )
        binding = {
            "campaign_id": self.campaign_id,
            "cohort_number": cohort_number,
            "gap_brief_path": gap_path,
            "gap_brief_sha256": gap_digest,
        }
        run_manifest_path = self.root / "runs" / run_id / "manifest.json"
        run_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        run_manifest_path.write_bytes(
            op.canonical_json_bytes({"campaign": binding})
        )
        state["active_run_id"] = run_id
        state["active_cohort_number"] = cohort_number
        op.save_campaign_state(self.campaign_dir, state, campaign_manifest)
        report = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "run_id": run_id,
            "run_status": run_status,
            "campaign": binding,
            "founder_sha256": campaign_manifest["founder_sha256"],
            "rubric_id": campaign_manifest["rubric"]["rubric_id"],
            "rubric_sha256": campaign_manifest["rubric"]["sha256"],
            "threshold": campaign_manifest["config"]["threshold"],
            "comparison": "strictly_greater_than",
            "official_score": metrics["official_score"],
            "binding_score_floor": metrics["official_score"],
        }
        report_path = self.outcomes_dir / run_id / "report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_bytes(op.canonical_json_bytes(report))
        run_manifest = {"campaign": binding}
        with mock.patch.object(op, "derive_campaign_cohort_metrics", return_value=metrics):
            return op.record_campaign_publication(
                self.root / f"run-{cohort_number}",
                run_manifest,
                report,
                self.outcomes_dir,
            )

    def test_campaign_single_regression_does_not_stop_and_plateau_requires_three(self) -> None:
        receipts = []
        for cohort_number, score in enumerate((7.2, 6.8, 6.7, 6.6), start=1):
            receipts.append(self.register_cohort(cohort_number, self.metrics(score)))
            if cohort_number < 4:
                self.assertEqual(receipts[-1]["campaign_status"], "active")
        self.assertEqual(receipts[0]["no_progress_streak"], 0)
        self.assertEqual(receipts[1]["no_progress_streak"], 1)
        self.assertEqual(receipts[2]["no_progress_streak"], 2)
        self.assertEqual(receipts[3]["no_progress_streak"], 3)
        self.assertEqual(receipts[3]["campaign_status"], "plateau")
        stopped = op.campaign_next(self.campaign_dir)
        self.assertEqual(stopped["action"], "stop")
        self.assertEqual(stopped["status"], "plateau")
        receipt, code = op.finalize_campaign(self.campaign_dir)
        self.assertEqual(code, 4)
        self.assertFalse(receipt["quality_objective_achieved"])
        published = self.root / "outcomes" / "campaigns" / self.campaign_id
        self.assertTrue((published / "receipt.json").is_file())
        self.assertTrue((published / "report.md").is_file())
        validated = op.validate_published_campaign(published, self.outcomes_dir)
        self.assertEqual(validated["cohort_count"], 4)
        self.assertEqual(validated["repair_count"], 0)

    def test_published_campaign_rejects_cross_cohort_event_reordering(self) -> None:
        for cohort_number, score in enumerate((7.2, 6.8, 6.7, 6.6), start=1):
            self.register_cohort(cohort_number, self.metrics(score))
        op.finalize_campaign(self.campaign_dir)
        published = self.outcomes_dir / "campaigns" / self.campaign_id
        events_path = published / "events.jsonl"
        events = op.load_campaign_events(events_path, self.campaign_id)
        created = events[0]
        finalized = events[-1]
        cohort_one = [
            event
            for event in events
            if event["details"].get("cohort_number") == 1
        ]
        cohort_two = [
            event
            for event in events
            if event["details"].get("cohort_number") == 2
        ]
        remaining = [
            event
            for event in events
            if event is not created
            and event is not finalized
            and event not in cohort_one
            and event not in cohort_two
        ]
        reordered = [created, *cohort_two, *cohort_one, *remaining, finalized]
        for sequence, event in enumerate(reordered, start=1):
            event["sequence"] = sequence
        events_path.write_text(
            "".join(
                json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n"
                for event in reordered
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(op.InputError, "out of cohort order"):
            op.validate_published_campaign(published, self.outcomes_dir)

    def test_published_campaign_rejects_boolean_event_integer_identities(self) -> None:
        for cohort_number, score in enumerate((7.2, 6.8, 6.7, 6.6), start=1):
            self.register_cohort(cohort_number, self.metrics(score))
        op.finalize_campaign(self.campaign_dir)
        published = self.outcomes_dir / "campaigns" / self.campaign_id
        events_path = published / "events.jsonl"
        events = op.load_campaign_events(events_path, self.campaign_id)

        def write_events() -> None:
            events_path.write_text(
                "".join(
                    json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n"
                    for event in events
                ),
                encoding="utf-8",
            )

        events[0]["sequence"] = True
        write_events()
        with self.assertRaisesRegex(op.InputError, "sequence must be an integer"):
            op.validate_published_campaign(published, self.outcomes_dir)

        events[0]["sequence"] = 1
        for event in events:
            if (
                event["event"] in {"cohort_attached", "cohort_published"}
                and event["details"].get("cohort_number") == 1
            ):
                event["details"]["cohort_number"] = True
        write_events()
        with self.assertRaisesRegex(op.InputError, "cohort_number must be an integer"):
            op.validate_published_campaign(published, self.outcomes_dir)

    def test_campaign_progress_resets_on_each_configured_signal(self) -> None:
        state = {
            "cohorts": [{}],
            "best_official_score": 7.2,
            "best_working_median": 7.0,
        }
        cases = (
            (
                self.metrics(7.3, median=7.0),
                "official_score",
            ),
            (
                self.metrics(7.2, median=7.2),
                "working_median",
            ),
        )
        for metrics, expected_signal in cases:
            with self.subTest(expected_signal=expected_signal):
                signals = op.campaign_progress_signals(state, metrics, self.config)
                self.assertTrue(signals[expected_signal])
                self.assertEqual(sum(signals.values()), 1)

    def test_reworded_or_industry_swapped_archetypes_do_not_reset_campaign_patience(self) -> None:
        receipts = []
        labels = [
            ["industrial evidence exchange"],
            ["healthcare compliance network"],
            ["energy asset orchestration"],
            ["logistics rights marketplace"],
        ]
        for number, (score, missing) in enumerate(
            zip((7.2, 6.9, 6.8, 6.7), labels, strict=True), start=1
        ):
            receipts.append(
                self.register_cohort(
                    number,
                    self.metrics(score, missing_archetypes=missing),
                )
            )
        self.assertEqual(
            [row["no_progress_streak"] for row in receipts], [0, 1, 2, 3]
        )
        self.assertEqual(receipts[-1]["campaign_status"], "plateau")

    def test_campaign_gap_brief_is_sanitized_and_cohort_binding_is_immutable(self) -> None:
        first = op.campaign_next(self.campaign_dir)
        self.assertEqual(first["cohort_number"], 1)
        runs_dir = self.root / "runs"
        created = op.make_run(
            self.config_path,
            runs_dir,
            campaign_id=self.campaign_id,
            campaigns_dir=self.campaigns_dir,
        )
        manifest = op.load_json(Path(created["run_dir"]) / "manifest.json")
        self.assertEqual(manifest["campaign"]["cohort_number"], 1)
        self.assertIsNone(manifest["campaign"]["gap_brief_sha256"])
        campaign_manifest, _ = op.load_campaign(self.campaign_dir)
        self.assertEqual(
            (Path(created["run_dir"]) / "inputs" / "founder.md").read_bytes(),
            (self.campaign_dir / "inputs" / "founder.md").read_bytes(),
        )
        self.assertEqual(
            (Path(created["run_dir"]) / "inputs" / "evaluator.txt").read_bytes(),
            (self.campaign_dir / "inputs" / "evaluator.txt").read_bytes(),
        )
        self.assertEqual(
            manifest["source_hashes"]["PERSONALITY_SITUATION.md"],
            campaign_manifest["founder_sha256"],
        )
        with self.assertRaisesRegex(op.ConflictError, "already has active run"):
            op.make_run(
                self.config_path,
                runs_dir,
                campaign_id=self.campaign_id,
                campaigns_dir=self.campaigns_dir,
            )

        replacement = op.new_campaign(self.config_path, self.campaigns_dir)
        self.campaign_id = replacement["campaign_id"]
        self.campaign_dir = Path(replacement["campaign_dir"])
        self.register_cohort(1, self.metrics(7.2))
        next_action = op.campaign_next(self.campaign_dir)
        self.assertEqual(next_action["cohort_number"], 2)
        brief_path = self.campaign_dir / next_action["gap_brief_path"]
        self.assertEqual(op.sha256_file(brief_path), next_action["gap_brief_sha256"])
        brief = op.load_json(brief_path)
        self.assertEqual(
            set(brief),
            {
                "schema_version",
                "campaign_id",
                "cohort_number",
                "deficient_factors",
                "missing_archetypes",
            },
        )
        serialized = json.dumps(brief).lower()
        for forbidden in ("candidate_id", "title", "score", "ranking", "threshold", "holdout"):
            self.assertNotIn(forbidden, serialized)
        contaminated = {
            **brief,
            "missing_archetypes": ["specialist workflow candidate one"],
        }
        with self.assertRaisesRegex(op.InputError, "candidate-like"):
            op.validate_campaign_gap_brief(
                contaminated, op.load_campaign(self.campaign_dir)[0], 2
            )

    def test_campaign_report_tampering_blocks_status_next_and_finalize(self) -> None:
        for cohort_number, score in enumerate((7.2, 6.8, 6.7, 6.6), start=1):
            self.register_cohort(cohort_number, self.metrics(score))
        report_path = self.outcomes_dir / "20260825T000001Z-000001" / "report.json"
        original = report_path.read_bytes()
        report_path.unlink()
        with self.assertRaisesRegex(op.InputError, "report is missing"):
            op.campaign_status(self.campaign_dir)
        with self.assertRaisesRegex(op.InputError, "report is missing"):
            op.campaign_next(self.campaign_dir)
        with self.assertRaisesRegex(op.InputError, "report is missing"):
            op.finalize_campaign(self.campaign_dir)
        report_path.write_bytes(original)
        forged = json.loads(original)
        forged["official_score"] = 9.9
        report_path.write_bytes(op.canonical_json_bytes(forged))
        with self.assertRaisesRegex(op.InputError, "report hash differs"):
            op.finalize_campaign(self.campaign_dir)

    def test_campaign_event_recovery_repairs_state_first_publication(self) -> None:
        original = op._ensure_campaign_event
        failed = False

        def fail_once(*args, **kwargs):
            nonlocal failed
            if len(args) >= 3 and args[2] == "cohort_published" and not failed:
                failed = True
                raise OSError("injected campaign event failure")
            return original(*args, **kwargs)

        with mock.patch.object(op, "_ensure_campaign_event", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "injected"):
                self.register_cohort(1, self.metrics(7.2))
        _, state = op.load_campaign(self.campaign_dir)
        self.assertEqual(len(state["cohorts"]), 1)
        self.assertFalse(
            any(
                event["event"] == "cohort_published"
                for event in op.load_campaign_events(
                    self.campaign_dir / "events.jsonl", self.campaign_id
                )
            )
        )
        status = op.campaign_status(self.campaign_dir)
        self.assertEqual(status["cohort_count"], 1)
        published = [
            event
            for event in op.load_campaign_events(
                self.campaign_dir / "events.jsonl", self.campaign_id
            )
            if event["event"] == "cohort_published"
        ]
        self.assertEqual(len(published), 1)

    def test_campaign_state_recomputes_scores_and_progress_signals(self) -> None:
        self.register_cohort(1, self.metrics(7.2))
        manifest, state = op.load_campaign(self.campaign_dir)
        forged = copy.deepcopy(state)
        forged["cohorts"][0]["progress_signals"]["official_score"] = True
        forged["cohorts"][0]["made_progress"] = True
        with self.assertRaisesRegex(op.InputError, "progress signals"):
            op.validate_campaign_state(forged, manifest)
        forged = copy.deepcopy(state)
        forged["cohorts"][0]["run_status"] = "qualified"
        forged["status"] = "qualified"
        forged["terminal_reason"] = "forged"
        with self.assertRaisesRegex(op.InputError, "strictly exceed"):
            op.validate_campaign_state(forged, manifest)

        metric_forgery = copy.deepcopy(state)
        metric_forgery["cohorts"][0]["top_four_working_median"] = 9.9
        metric_forgery["best_working_median"] = 9.9
        op.atomic_write(
            self.campaign_dir / "state.json",
            op.canonical_json_bytes(metric_forgery),
            root=self.campaign_dir,
        )
        with self.assertRaisesRegex(op.InputError, "immutable metric receipt"):
            op.campaign_status(self.campaign_dir)
        op.atomic_write(
            self.campaign_dir / "state.json",
            op.canonical_json_bytes(state),
            root=self.campaign_dir,
        )

        self.register_cohort(2, self.metrics(6.8))
        manifest, two_cohorts = op.load_campaign(self.campaign_dir)
        terminal_prefix = copy.deepcopy(two_cohorts)
        terminal_prefix["cohorts"][0]["run_status"] = "qualified"
        terminal_prefix["cohorts"][0]["official_score"] = 8.6
        terminal_prefix["best_official_score"] = 8.6
        terminal_prefix["status"] = "qualified"
        terminal_prefix["terminal_reason"] = op.campaign_terminal_reason("qualified")
        with self.assertRaisesRegex(op.InputError, "earlier terminal stop"):
            op.validate_campaign_state(terminal_prefix, manifest)

    def test_campaign_rejects_extra_events_and_nondeterministic_reason(self) -> None:
        future_brief = {
            "schema_version": op.ACTIVE_SCHEMA_VERSION,
            "campaign_id": self.campaign_id,
            "cohort_number": 99,
            "deficient_factors": ["Distribution"],
            "missing_archetypes": [],
        }
        future_path = self.campaign_dir / "briefs/cohort-99.json"
        op.write_immutable(
            future_path, op.canonical_json_bytes(future_brief), root=self.campaign_dir
        )
        with self.assertRaisesRegex(op.InputError, "unexpected cohort"):
            op.campaign_status(self.campaign_dir)
        future_path.unlink()
        op.append_campaign_event(
            self.campaign_dir,
            self.campaign_id,
            "cohort_published",
            {"cohort_number": 99},
        )
        with self.assertRaisesRegex(op.InputError, "state-inconsistent"):
            op.campaign_status(self.campaign_dir)

        clean_root = self.root / "terminal-reason"
        clean_campaigns = clean_root / "campaigns"
        created = op.new_campaign(self.config_path, clean_campaigns)
        old = (self.root, self.campaign_id, self.campaign_dir, self.outcomes_dir)
        self.root = clean_root
        self.campaign_id = created["campaign_id"]
        self.campaign_dir = Path(created["campaign_dir"])
        self.outcomes_dir = clean_root / "outcomes"
        try:
            for cohort_number, score in enumerate((7.2, 6.8, 6.7, 6.6), start=1):
                self.register_cohort(cohort_number, self.metrics(score))
            manifest, state = op.load_campaign(self.campaign_dir)
            state["terminal_reason"] = "An editorial explanation."
            with self.assertRaisesRegex(op.InputError, "terminal reason"):
                op.save_campaign_state(self.campaign_dir, state, manifest)
        finally:
            self.root, self.campaign_id, self.campaign_dir, self.outcomes_dir = old

    def test_qualifier_stops_immediately_and_maximum_is_ten(self) -> None:
        qualified = self.register_cohort(
            1,
            self.metrics(8.6),
            run_status="qualified",
        )
        self.assertEqual(qualified["campaign_status"], "qualified")
        receipt, code = op.finalize_campaign(self.campaign_dir)
        self.assertEqual(code, 0)
        self.assertTrue(receipt["quality_objective_achieved"])
        self.assertTrue(
            (self.root / "outcomes" / "campaigns" / self.campaign_id / "receipt.json").is_file()
        )
        campaign_outcome = (
            self.root / "outcomes" / "campaigns" / self.campaign_id
        )
        self.assertTrue((campaign_outcome / "manifest.json").is_file())
        self.assertTrue((campaign_outcome / "events.jsonl").is_file())
        self.assertTrue((campaign_outcome / "inputs" / "founder.md").is_file())
        self.assertTrue((campaign_outcome / "inputs" / "evaluator.txt").is_file())
        self.assertEqual(
            receipt["campaign_manifest_sha256"],
            op.sha256_file(campaign_outcome / "manifest.json"),
        )

        other_root = self.root / "maximum"
        other_campaigns = other_root / "campaigns"
        other_outcomes = other_root / "outcomes"
        created = op.new_campaign(self.config_path, other_campaigns)
        old = (self.root, self.campaign_id, self.campaign_dir, self.outcomes_dir)
        self.root = other_root
        self.campaign_id = created["campaign_id"]
        self.campaign_dir = Path(created["campaign_dir"])
        self.outcomes_dir = other_outcomes
        try:
            final = None
            for cohort_number in range(1, 11):
                score = 6 + cohort_number / 10
                final = self.register_cohort(cohort_number, self.metrics(score))
            self.assertIsNotNone(final)
            self.assertEqual(final["campaign_status"], "max_cohorts")
            self.assertEqual(op.campaign_status(self.campaign_dir)["cohort_count"], 10)
        finally:
            self.root, self.campaign_id, self.campaign_dir, self.outcomes_dir = old


class DedupAndHoldoutTests(OpportunityTestCase):
    def test_native_schema_has_explicit_types_without_rewriting_exports(self) -> None:
        self.store_complete_lineage()
        self.set_stage("frozen")
        op.export_external(self.run_dir, "alpha")
        schema_path = self.run_dir / "exports/alpha/response_schema.json"
        packet_path = self.run_dir / "exports/alpha/holdout_packet.md"
        before = {path: path.read_bytes() for path in (
            schema_path, packet_path, self.run_dir / "state.json", self.run_dir / "events.jsonl",
        )}
        assignment = op.native_holdout_assignment(
            self.run_dir, "alpha", self.root / "typed-response.json",
        )
        schema = assignment["strict_response_contract"]
        def assert_typed(node):
            self.assertIn("type", node)
            for child in node.get("properties", {}).values():
                assert_typed(child)
            if "items" in node:
                assert_typed(node["items"])
        assert_typed(schema)
        self.assertEqual(schema["properties"]["candidate_id"]["type"], "string")
        self.assertEqual(schema["properties"]["candidate_version"]["type"], "integer")
        # Remove transport types, the write instruction, and the identity binding before
        # comparing with the immutable exported schema.
        comparable = copy.deepcopy(schema)
        self.assertIn("temporary_response_destination", comparable.pop("description"))
        del comparable["properties"]["candidate_id"]["type"]
        del comparable["properties"]["candidate_version"]["type"]
        judge_id = comparable["properties"]["judge_id"].pop("const")
        self.assertRegex(judge_id, r"^native-[0-9a-f]{24}$")
        other = op.native_holdout_assignment(
            self.run_dir, "alpha", self.root / "other-typed-response.json",
        )
        self.assertNotEqual(judge_id, other["strict_response_contract"]["properties"]["judge_id"]["const"])
        repeated = op.native_holdout_assignment(
            self.run_dir, "alpha", self.root / "typed-response.json",
        )
        self.assertEqual(judge_id, repeated["strict_response_contract"]["properties"]["judge_id"]["const"])
        factor_properties = comparable["properties"]["factors"]["items"]["properties"]
        del factor_properties["name"]["type"]
        del factor_properties["status"]["type"]
        self.assertEqual(comparable, json.loads(before[schema_path]))
        self.assertEqual(assignment["immutable_finalist_packet"]["sha256"], op.sha256_file(packet_path))
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_holdout_assignment_rejects_managed_destination_aliases(self) -> None:
        self.store_complete_lineage()
        self.set_stage("frozen")
        op.export_external(self.run_dir, "alpha")
        alias = self.root / "run-alias"
        alias.symlink_to(self.run_dir, target_is_directory=True)
        destinations = [
            self.run_dir / "response.json",
            self.run_dir.resolve() / "response.json",
            alias / "response.json",
        ]
        case_alias = self.run_dir.with_name(self.run_dir.name.swapcase())
        if case_alias.is_dir():
            destinations.append(case_alias / "response.json")
        for destination in destinations:
            with self.subTest(destination=str(destination)):
                code, _, error = self.run_cli([
                    "--runs-dir", str(self.runs_dir), "holdout-assignment",
                    self.run_id, "alpha", "--response-destination", str(destination),
                ])
                self.assertEqual(code, 2)
                self.assertIn("outside CLI-managed run state", error["error"])
                self.assertFalse(destination.exists())

        outside = self.root / "outside-response.json"
        assignment = op.native_holdout_assignment(self.run_dir, "alpha", outside)
        self.assertEqual(assignment["temporary_response_destination"], str(outside))
        self.assertFalse(outside.exists())
        outside.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(op.ConflictError, "already exists"):
            op.native_holdout_assignment(self.run_dir, "alpha", outside)
        dangling = self.root / "dangling-response.json"
        dangling.symlink_to(self.root / "missing-response.json")
        with self.assertRaisesRegex(op.ConflictError, "already exists"):
            op.native_holdout_assignment(self.run_dir, "alpha", dangling)

    def test_dedup_exact_similarity_and_one_bounded_gap_scout(self) -> None:
        self.set_stage("discovery")
        lanes = self.load()[0]["config"]["discovery_lanes"]
        candidates = []
        for lane_index, lane in enumerate(lanes):
            for seed_index in range(self.load()[0]["config"]["seeds_per_scout"]):
                candidate_id = f"lane-{lane_index + 1}-candidate-{seed_index + 1}"
                fingerprint_seed = (
                    "shared stable structures"
                    if lane_index == 0 and seed_index == 1
                    else "shared stable structure"
                )
                candidates.append(
                    self.candidate(
                        candidate_id,
                        fingerprint_seed=fingerprint_seed,
                        discovery_lane=lane,
                    )
                )
        for candidate in candidates:
            self.store_candidate(candidate)
        first = op.dedup_run(self.run_dir)
        self.assertEqual(
            first["candidate_count"],
            len(lanes) * self.load()[0]["config"]["seeds_per_scout"],
        )
        self.assertEqual(first["exact_fingerprint_unique_count"], 2)
        self.assertEqual(len(first["duplicate_groups"]), 1)
        self.assertTrue(first["similarity_flags"])
        self.assertEqual(
            first["lane_counts"],
            {
                lane: self.load()[0]["config"]["seeds_per_scout"]
                for lane in lanes
            },
        )
        self.assertEqual(first["gap_scout_job"]["status"], "pending")
        second = op.dedup_run(self.run_dir)
        self.assertEqual(second["gap_scout_job"]["job_id"], "gap-scout")
        _, state = self.load()
        self.assertEqual(list(state["jobs"]["discovery"]).count("gap-scout"), 1)
        op.start_job(self.run_dir, "gap-scout", None)
        op.fail_job(self.run_dir, "gap-scout", "first mechanical attempt failed")
        op.start_job(self.run_dir, "gap-scout", None)
        op.fail_job(self.run_dir, "gap-scout", "bounded gap attempt exhausted")
        final_dedup = op.dedup_run(self.run_dir)
        self.assertTrue(final_dedup["gap_scout_budget_exhausted"])
        advanced = op.advance_run(self.run_dir)
        self.assertEqual(advanced["stage"], "calibration")

    def _store_lineage_with_research(self, candidate_id: str = "alpha", *, capital: object = 100000) -> dict:
        return self.store_complete_lineage(candidate_id, capital=capital)

    def _store_lineages(self, specs: list[tuple[str, object]]) -> dict[str, dict]:
        candidates = {
            candidate_id: self.candidate(candidate_id, capital=capital)
            for candidate_id, capital in specs
        }
        for candidate in candidates.values():
            self.store_candidate(candidate)
        calibration = {
            candidate_id: {
                "commercial_archetype": f"calibrated archetype {candidate_id}",
                "control_point": f"calibrated control point {candidate_id}",
                "critical_dependency": f"calibrated dependency {candidate_id}",
            }
            for candidate_id in candidates
        }
        self.store_portfolio_selection(
            list(candidates.values()), calibration_overrides=calibration
        )
        self.set_stage("research")
        for candidate in candidates.values():
            self.store_research(self.research(candidate))
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"working-research-{candidate['candidate_id']}",
                    score=8,
                    evaluation_type="working_research",
                )
            )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision(
                list(candidates.values()), set(candidates)
            ),
        )
        op.advance_run(self.run_dir)
        for candidate in candidates.values():
            candidate_id = candidate["candidate_id"]
            self.complete_json_job(
                f"constructor-{candidate_id}",
                "development-result",
                self.development_result(
                    candidate,
                    constructor_id=f"constructor-{candidate_id}",
                ),
            )
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"working-{candidate_id}",
                    score=8,
                    evaluation_type="working_development",
                )
            )
        op.advance_run(self.run_dir)
        return candidates

    def test_external_packet_import_rejection_preservation_and_binding(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        exported = op.export_external(self.run_dir, "alpha")
        packet = (self.run_dir / exported["packet"]).read_text(encoding="utf-8")
        self.assertIn((self.run_dir / "inputs/founder.md").read_text().strip(), packet)
        self.assertIn((self.run_dir / "inputs/evaluator.txt").read_text().strip(), packet)
        self.assertIn("research/alpha/v1.json", packet)
        self.assertEqual(
            sorted(path.name for path in (self.run_dir / "exports/alpha").iterdir()),
            ["holdout_packet.md", "response_schema.json"],
        )

        malformed = self.root / "malformed.txt"
        malformed.write_text('prose before {"not": "allowed"}', encoding="utf-8")
        with self.assertRaises(op.InputError):
            op.import_external(self.run_dir, "alpha", malformed)
        malformed_digest = op.sha256_file(malformed)
        self.assertTrue(
            (self.run_dir / f"holdout/alpha/v1/raw/external-{malformed_digest}.txt").is_file()
        )
        rejected = op.load_json(
            self.run_dir / f"holdout/alpha/v1/imports/external-{malformed_digest}.json"
        )
        self.assertEqual(rejected["status"], "rejected")

        manifest, _ = self.load()
        response = self.external_response(manifest, judge_id="external-a", score=8.5)
        response_path = self.root / "external.json"
        response_path.write_text(json.dumps(response), encoding="utf-8")
        imported = op.import_external(self.run_dir, "alpha", response_path)
        self.assertEqual(imported["status"], "accepted")
        self.assertFalse(imported["qualified"])
        self.assertTrue((self.run_dir / imported["evaluation"]).is_file())

        self.store_evaluation(self.evaluation_input(frozen, "native-a", score=9))
        self.store_evaluation(self.evaluation_input(frozen, "native-b", score=9))
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "contested")
        self.assertIn("External binding limiter.", report["binding_limiters"])
        self.assertIn(
            "produced no binding qualifier",
            (self.run_dir / "report.md").read_text(encoding="utf-8"),
        )

    def test_export_and_publication_events_reconcile_after_durable_writes(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        with mock.patch.object(op, "append_event", side_effect=OSError("export event failure")):
            with self.assertRaisesRegex(OSError, "export event failure"):
                op.export_external(self.run_dir, "alpha")
        self.assertTrue((self.run_dir / "exports/alpha/holdout_packet.md").is_file())
        replayed_export = op.export_external(self.run_dir, "alpha")
        self.assertTrue(replayed_export["idempotent"])
        export_events = [
            event
            for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            if event["event"] == "external_exported"
            and event["details"].get("candidate_id") == "alpha"
        ]
        self.assertEqual(len(export_events), 1)

        self.store_evaluation(self.evaluation_input(frozen, "native-event-a", score=8.2))
        self.store_evaluation(self.evaluation_input(frozen, "native-event-b", score=8.1))
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "no_qualifier")
        self.assertEqual(report["official_score"], 8.1)
        outcomes = self.root / "outcomes"
        knowledge = self.root / "knowledge"
        with mock.patch.object(op, "append_event", side_effect=OSError("publish event failure")):
            with self.assertRaisesRegex(OSError, "publish event failure"):
                op.publish_run(self.run_dir, outcomes, knowledge)
        self.assertTrue((knowledge / "history_index.jsonl").is_file())
        replayed_publish = op.publish_run(self.run_dir, outcomes, knowledge)
        self.assertTrue(replayed_publish["idempotent"])
        publish_events = [
            event
            for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            if event["event"] == "run_published"
        ]
        self.assertEqual(len(publish_events), 1)

    def test_external_import_receipt_raw_evaluation_and_event_reconcile(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        manifest, _ = self.load()
        response = self.external_response(manifest, judge_id="external-binding", score=8.5)
        response_path = self.root / "external-binding.json"
        response_path.write_text(json.dumps(response), encoding="utf-8")
        imported = op.import_external(self.run_dir, "alpha", response_path)
        evaluation_path = self.run_dir / imported["evaluation"]
        evaluation_bytes = evaluation_path.read_bytes()
        receipt_path = (
            self.run_dir
            / f"holdout/alpha/v1/imports/external-{imported['raw_response_sha256']}.json"
        )
        receipt_bytes = receipt_path.read_bytes()

        evaluation_path.unlink()
        with self.assertRaisesRegex(op.InputError, "external import evaluation.*does not exist"):
            op.check_run(self.run_dir, self.config_path)
        with self.assertRaises(op.InputError):
            op.finalize_run(self.run_dir)
        evaluation_path.write_bytes(evaluation_bytes)

        forged = json.loads(evaluation_bytes)
        forged["primary_score_limiter"] = "Forged limiter not present in raw response."
        evaluation_path.write_text(json.dumps(forged), encoding="utf-8")
        with self.assertRaises(op.WorkflowError):
            op.import_external(self.run_dir, "alpha", response_path)
        evaluation_path.write_bytes(evaluation_bytes)

        receipt_path.unlink()
        with self.assertRaisesRegex(op.InputError, "no accepted import receipt"):
            op.check_run(self.run_dir, self.config_path)
        recovered = op.import_external(self.run_dir, "alpha", response_path)
        self.assertTrue(recovered["idempotent"])
        accepted_events = [
            event
            for event in op.load_events(self.run_dir / "events.jsonl", self.run_id)
            if event["event"] == "external_import_accepted"
        ]
        self.assertEqual(len(accepted_events), 1)
        evaluation_path.unlink()
        receipt_path.unlink()
        with self.assertRaisesRegex(op.InputError, "events and receipts do not reconcile"):
            op.check_run(self.run_dir, self.config_path)

        evaluation_path.write_bytes(evaluation_bytes)
        receipt_path.write_bytes(receipt_bytes)
        self.store_evaluation(self.evaluation_input(frozen, "native-a", score=9))
        self.store_evaluation(self.evaluation_input(frozen, "native-b", score=9))
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "contested")

    def test_native_holdout_job_accepts_one_strict_response(self) -> None:
        finalist = self._store_lineage_with_research()
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        response = self.evaluation_input(
            finalist,
            "native-strict",
            score=8.7,
            evaluation_type="holdout_native",
        )
        response.pop("_test_evaluation_type")
        response_path = self.root / "native-strict.json"
        response_path.write_text(json.dumps(response), encoding="utf-8")
        op.start_job(self.run_dir, "native-strict", "holdout")
        completed = op.complete_job(
            self.run_dir, "native-strict", response_path, "evaluation"
        )
        canonical = op.load_json(self.run_dir / completed["artifact"])
        self.assertEqual(canonical["evaluation_type"], "holdout_native")
        self.assertEqual(canonical["candidate_version"], 1)
        self.assertEqual(canonical["final_score"], 8.7)
        self.assertNotIn("raw_response_path", canonical)
        self.assertNotIn("raw_response_sha256", canonical)

    def test_frozen_cannot_advance_or_close_without_matching_packet(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("frozen")
        with self.assertRaisesRegex(op.ConflictError, "canonical holdout packet is required"):
            op.advance_run(self.run_dir)
        op.export_external(self.run_dir, frozen["candidate_id"])
        packet_path = self.run_dir / "exports/alpha/holdout_packet.md"
        packet_bytes = packet_path.read_bytes()
        packet_path.write_bytes(packet_bytes + b"\ntampered")
        with self.assertRaisesRegex(op.ConflictError, "canonical holdout packet is required"):
            op.advance_run(self.run_dir)
        packet_path.write_bytes(packet_bytes)
        advanced = op.advance_run(self.run_dir)
        self.assertEqual(advanced["stage"], "holdout")
        packet_path.unlink()
        with self.assertRaisesRegex(op.InputError, "external packet"):
            op.check_run(self.run_dir, self.config_path)
        packet_path.write_bytes(packet_bytes)

        other = OpportunityTestCase(methodName="runTest")
        other.setUp()
        try:
            other.store_complete_lineage()
            other.set_stage("frozen")
            with self.assertRaisesRegex(op.ConflictError, "must continue to holdout"):
                op.finalize_run(other.run_dir, "Holdout packet could not be completed")
        finally:
            other.tearDown()

    def test_every_researched_candidate_appears_in_published_learning_digest(self) -> None:
        lineages = self._store_lineages(
            [("alpha", 50000), ("beta", 200000)]
        )
        alpha = lineages["alpha"]
        beta = lineages["beta"]
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        op.export_external(self.run_dir, "beta")
        for judge in ("native-a", "native-b"):
            self.store_evaluation(
                self.evaluation_input(
                    alpha,
                    f"{judge}-alpha",
                    score=9,
                    factor_overrides={"Business model and economics": 8.9},
                )
            )
            self.store_evaluation(
                self.evaluation_input(
                    beta,
                    f"{judge}-beta",
                    score=9,
                    factor_overrides={"Distribution": 8.9},
                )
            )
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 0)
        self.assertEqual(report["run_status"], "qualified")
        self.assertEqual(report["selected_candidate_id"], "beta")
        self.assertEqual(report["qualification_label"], op.QUALIFICATION_LABEL)
        self.assertTrue(report["binding_limiters"])
        markdown = (self.run_dir / "report.md").read_text()
        self.assertIn("Binding limiter", markdown)
        self.assertIn(op.QUALIFICATION_LABEL, markdown)
        self.assertNotIn("produced no score-qualified candidate", markdown)
        publication = op.publish_run(self.run_dir, self.root / "outcomes", self.root / "knowledge")
        published = self.root / "outcomes" / self.run_id
        self.assertTrue((published / "candidates/beta/v1.json").is_file())
        self.assertTrue((published / "research/beta/v1.json").is_file())
        self.assertTrue((published / "exports/beta/holdout_packet.md").is_file())
        self.assertTrue((published / "holdout/beta/v1/native-native-a-beta.json").is_file())
        self.assertTrue((published / "candidates/alpha/v1.json").is_file())
        self.assertTrue((published / "exports/alpha/holdout_packet.md").is_file())
        self.assertTrue((published / "exports/alpha/response_schema.json").is_file())
        self.assertTrue((published / "holdout/alpha/v1/native-native-a-alpha.json").is_file())
        self.assertTrue((published / "holdout/alpha/v1/native-native-b-alpha.json").is_file())
        alpha_result = next(
            item for item in report["candidates"] if item["candidate_id"] == "alpha"
        )
        self.assertEqual(len(alpha_result["evaluation_artifacts"]), 2)
        for artifact in alpha_result["evaluation_artifacts"]:
            self.assertTrue((published / artifact["path"]).is_file())
        self.assertEqual(publication["run_status"], "qualified")
        history = json.loads((self.root / "knowledge/history_index.jsonl").read_text().strip())
        self.assertEqual(history["score_scale"], "/10")
        self.assertEqual(history["rubric_id"], "holistic-11-v1")
        self.assertEqual(history["selected_title"], beta["title"])
        self.assertEqual(history["selected_fingerprint"], beta["fingerprint"])
        learning_rows = [
            json.loads(line)
            for line in (published / "learning-digest.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertEqual(
            {row["candidate_id"] for row in learning_rows}, {"alpha", "beta"}
        )
        for row in learning_rows:
            candidate_id = row["candidate_id"]
            self.assertEqual(
                row["structure"],
                {
                    "commercial_archetype": f"calibrated archetype {candidate_id}",
                    "control_point": f"calibrated control point {candidate_id}",
                    "critical_dependency": f"calibrated dependency {candidate_id}",
                },
            )
        self.assertEqual(history["learning_row_count"], 2)
        self.assertEqual(
            op.validate_published_run_outcome(published)["run_id"], self.run_id
        )
        published_report_path = published / "report.json"
        forged = op.load_json(published_report_path)
        forged["official_score"] = 9.9
        forged["binding_score_floor"] = 9.9
        published_report_path.write_bytes(op.canonical_json_bytes(forged))
        (published / "report.md").write_text(
            op.render_report_markdown(forged), encoding="utf-8"
        )
        with self.assertRaisesRegex(
            op.InputError, "deterministically rederived outcome"
        ):
            op.validate_published_run_outcome(published)

    def test_ranking_cascade_and_passing_external_does_not_reorder_native_scores(self) -> None:
        base = {
            "official_native_score": 9,
            "native_economics_floor": 9,
            "native_distribution_floor": 9,
            "capital_required_pln_numeric": 100,
            "candidate_id": "alpha",
        }
        cases = [
            ({**base, "candidate_id": "worse-official", "official_native_score": 8.9, "native_economics_floor": 10}, "alpha"),
            ({**base, "candidate_id": "worse-economics", "native_economics_floor": 8.9, "native_distribution_floor": 10}, "alpha"),
            ({**base, "candidate_id": "worse-distribution", "native_distribution_floor": 8.9, "capital_required_pln_numeric": 1}, "alpha"),
            ({**base, "candidate_id": "worse-capital", "capital_required_pln_numeric": 101}, "alpha"),
            ({**base, "candidate_id": "zeta"}, "alpha"),
        ]
        for challenger, expected in cases:
            with self.subTest(challenger=challenger["candidate_id"]):
                self.assertEqual(min([base, challenger], key=op._selection_key)["candidate_id"], expected)

        lineages = self._store_lineages([("alpha", 100000), ("beta", 100000)])
        alpha = lineages["alpha"]
        beta = lineages["beta"]
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        op.export_external(self.run_dir, "beta")
        for judge in ("native-a", "native-b"):
            self.store_evaluation(self.evaluation_input(alpha, f"{judge}-alpha", score=9.2))
            self.store_evaluation(self.evaluation_input(beta, f"{judge}-beta", score=9.0))
        manifest, _ = self.load()
        for candidate_id, judge_id, score in (
            ("alpha", "external-alpha", 8.6),
            ("beta", "external-beta", 9.5),
        ):
            response_path = self.root / f"{judge_id}.json"
            response = self.external_response(
                manifest, judge_id=judge_id, score=score
            )
            response["candidate_id"] = candidate_id
            response["candidate_version"] = 1
            response_path.write_text(
                json.dumps(response),
                encoding="utf-8",
            )
            op.import_external(self.run_dir, candidate_id, response_path)
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 0)
        self.assertEqual(report["selected_candidate_id"], "alpha")
        self.assertEqual(report["official_score"], 9.2)
        self.assertEqual(report["binding_score_floor"], 8.6)
        op.publish_run(self.run_dir, self.root / "outcomes", self.root / "knowledge")
        published = self.root / "outcomes" / self.run_id
        self.assertTrue((published / "exports/alpha/holdout_packet.md").is_file())
        self.assertTrue((published / "holdout/alpha/v1/native-native-a-alpha.json").is_file())
        alpha_receipts = list((published / "holdout/alpha/v1/imports").glob("external-*.json"))
        alpha_raw = list((published / "holdout/alpha/v1/raw").glob("external-*.txt"))
        self.assertEqual(len(alpha_receipts), 1)
        self.assertEqual(len(alpha_raw), 1)

    def test_forged_final_reports_are_rejected_by_check_and_publish(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        self.store_evaluation(self.evaluation_input(frozen, "native-a", score=9))
        self.store_evaluation(self.evaluation_input(frozen, "native-b", score=9))
        op.finalize_run(self.run_dir)
        report_path = self.run_dir / "final/report.json"
        forged = json.loads(report_path.read_text())
        forged["selected_candidate_id"] = "forged-selection"
        report_path.write_bytes(op.canonical_json_bytes(forged))
        (self.run_dir / "report.md").write_text(op.render_report_markdown(forged), encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "deterministically derived outcome"):
            op.check_run(self.run_dir, self.config_path)
        with self.assertRaisesRegex(op.InputError, "deterministically derived outcome"):
            op.publish_run(self.run_dir, self.root / "outcomes", self.root / "knowledge")

    def test_forged_early_closure_report_is_rejected(self) -> None:
        self.prepare_fatal_research_closure()
        op.finalize_run(self.run_dir, "No candidate survived bounded research")
        report_path = self.run_dir / "final/report.json"
        forged = json.loads(report_path.read_text())
        forged["no_finalist_reason"] = "A substituted closure rationale"
        report_path.write_bytes(op.canonical_json_bytes(forged))
        (self.run_dir / "report.md").write_text(op.render_report_markdown(forged), encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "deterministically derived outcome"):
            op.check_run(self.run_dir, self.config_path)


class IntegrityAndExitCodeTests(OpportunityTestCase):
    def test_check_detects_snapshot_and_event_corruption(self) -> None:
        originals = {
            "inputs/founder.md": (op.REPO_ROOT / "PERSONALITY_SITUATION.md").read_bytes(),
            "inputs/evaluator.txt": (op.REPO_ROOT / "Personalities/ZeroToOne.txt").read_bytes(),
            "inputs/config.json": op.canonical_json_bytes(
                op.validate_config(op.load_json(self.config_path))
            ),
        }
        for relative, original in originals.items():
            with self.subTest(snapshot=relative):
                snapshot = self.run_dir / relative
                snapshot.write_bytes(original + b"\ntampered")
                with self.assertRaisesRegex(op.InputError, f"snapshot hash mismatch: {relative}"):
                    op.load_run(self.run_dir)
                snapshot.write_bytes(original)
        events = self.run_dir / "events.jsonl"
        record = json.loads(events.read_text().splitlines()[0])
        record["sequence"] = 2
        events.write_text(json.dumps(record) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "not contiguous"):
            op.check_run(self.run_dir, self.config_path)

    def test_cli_candidate_validation_and_scoped_status(self) -> None:
        alpha = self.candidate("alpha")
        beta = self.candidate("beta")
        alpha_input = self.root / "alpha-input.json"
        alpha_input.write_text(json.dumps(alpha, separators=(",", ":")), encoding="utf-8")
        code, validated, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "validate",
                self.run_id,
                "--input",
                str(alpha_input),
                "--kind",
                "candidate",
            ]
        )
        self.assertEqual(code, 0, error)
        self.assertRegex(validated["canonical_sha256"], r"^[0-9a-f]{64}$")

        self.store_candidate(alpha)
        self.store_candidate(beta)
        self.store_portfolio_selection([alpha, beta])
        code, scoped, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "status",
                self.run_id,
                "--candidate",
                "alpha",
            ]
        )
        self.assertEqual(code, 0, error)
        self.assertEqual(scoped["scope"], "candidate_research")
        self.assertNotIn("beta", json.dumps(scoped, sort_keys=True))
        self.assertNotIn("portfolio_decision", scoped)

    def test_preflight_is_attempt_neutral_and_hash_binds_job_completion(self) -> None:
        op.advance_run(self.run_dir)
        candidate = self.candidate("preflight-candidate")
        candidate["founder_fit"] = "scalar founder fit"
        candidate_input = self.root / "preflight-candidate.json"
        candidate_input.write_bytes(op.canonical_json_bytes(candidate))
        state_before = (self.run_dir / "state.json").read_bytes()
        events_before = (self.run_dir / "events.jsonl").read_bytes()

        code, report, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "candidate",
                "--job-id",
                "scout-preflight",
                "--input",
                str(candidate_input),
            ]
        )
        self.assertEqual(code, op.InputError.exit_code, error)
        self.assertFalse(report["validation"]["valid"])
        self.assertIn(
            "/founder_fit",
            {row["pointer"] for row in report["validation"]["errors"]},
        )
        self.assertEqual(report["attempts_consumed"], 0)
        self.assertEqual((self.run_dir / "state.json").read_bytes(), state_before)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), events_before)

        candidate["founder_fit"] = ["AI-assisted research"]
        candidate_input.write_bytes(op.canonical_json_bytes(candidate))
        accepted_bytes = candidate_input.read_bytes()
        code, report, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "candidate",
                "--job-id",
                "scout-preflight",
                "--input",
                str(candidate_input),
            ]
        )
        self.assertEqual(code, 0, error)
        self.assertTrue(report["validation"]["valid"])
        digest = report["validation"]["input_sha256"]
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        self.assertEqual((self.run_dir / "state.json").read_bytes(), state_before)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), events_before)

        op.start_job(self.run_dir, "scout-preflight", "discovery")
        candidate["title"] = "Changed after preflight"
        candidate_input.write_bytes(op.canonical_json_bytes(candidate))
        with self.assertRaisesRegex(op.ConflictError, "differ from the successful preflight"):
            op.complete_job(
                self.run_dir,
                "scout-preflight",
                candidate_input,
                "candidate",
                digest,
            )
        self.assertEqual(
            self.load()[1]["jobs"]["discovery"]["scout-preflight"]["status"],
            "running",
        )
        candidate_input.write_bytes(accepted_bytes)
        completed = op.complete_job(
            self.run_dir,
            "scout-preflight",
            candidate_input,
            "candidate",
            digest,
        )
        self.assertEqual(completed["status"], "completed")
        self.assertEqual(completed["attempts"], 1)

    def test_evaluator_preflight_emits_exact_factors_enums_and_pointer_errors(self) -> None:
        candidate = self.candidate("preflight-evaluation")
        self.store_candidate(candidate)
        self.store_portfolio_selection([candidate])
        self.set_stage("research")
        self.store_research(self.research(candidate))
        state_before = (self.run_dir / "state.json").read_bytes()
        events_before = (self.run_dir / "events.jsonl").read_bytes()
        code, contract, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "evaluation",
                "--job-id",
                "working-preflight",
            ]
        )
        self.assertEqual(code, 0, error)
        expected_names = [row["name"] for row in self.load()[0]["rubric"]["factors"]]
        self.assertEqual(contract["canonical_factor_names"], expected_names)
        self.assertEqual(
            [row["name"] for row in contract["template"]["factors"]],
            expected_names,
        )
        self.assertEqual(
            contract["enums"]["/factors/*/status"], ["scored", "excluded"]
        )

        malformed = copy.deepcopy(contract["template"])
        malformed["candidate_id"] = candidate["candidate_id"]
        malformed["candidate_version"] = candidate["version"]
        malformed["evidence_needed_for_higher_score"] = ["wrong type"]
        malformed_path = self.root / "malformed-evaluation.json"
        malformed_path.write_bytes(op.canonical_json_bytes(malformed))
        code, report, error = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "evaluation",
                "--job-id",
                "working-preflight",
                "--input",
                str(malformed_path),
            ]
        )
        self.assertEqual(code, op.InputError.exit_code, error)
        errors = {(row["pointer"], row["code"]) for row in report["validation"]["errors"]}
        self.assertEqual(
            errors,
            {("/evidence_needed_for_higher_score", "canonical_validation")},
        )
        self.assertTrue(report["validation"]["schema_retry_required"])

        malformed["evidence_needed_for_higher_score"] = "string"
        malformed["factors"][0]["name"] = "core_insight"
        malformed_path.write_bytes(op.canonical_json_bytes(malformed))
        _, factor_report, _ = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "evaluation",
                "--job-id",
                "working-preflight",
                "--input",
                str(malformed_path),
            ]
        )
        self.assertEqual(
            factor_report["validation"]["errors"][0]["pointer"], "/factors"
        )

        malformed["factors"][0]["name"] = expected_names[0]
        malformed["factors"][0]["status"] = "score"
        malformed_path.write_bytes(op.canonical_json_bytes(malformed))
        _, status_report, _ = self.run_cli(
            [
                "--runs-dir",
                str(self.runs_dir),
                "preflight",
                self.run_id,
                "--kind",
                "evaluation",
                "--job-id",
                "working-preflight",
                "--input",
                str(malformed_path),
            ]
        )
        self.assertEqual(
            status_report["validation"]["errors"][0]["pointer"],
            "/factors/0/status",
        )
        self.assertEqual((self.run_dir / "state.json").read_bytes(), state_before)
        self.assertEqual((self.run_dir / "events.jsonl").read_bytes(), events_before)

    def test_resume_reports_corrupt_state_clearly(self) -> None:
        (self.run_dir / "state.json").write_text('{"stage":', encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "invalid JSON in .*state.json"):
            op.resume_run(self.run_dir)

    def test_run_resolution_and_state_lock_reject_symlink_escapes(self) -> None:
        with self.assertRaisesRegex(op.InputError, "canonical run id"):
            op.resolve_run(self.runs_dir, str(self.run_dir))
        with self.assertRaisesRegex(op.InputError, "canonical run id"):
            op.resolve_run(self.runs_dir, f"../{self.run_id}")

        alias = "20260824T000000Z-abcdef"
        (self.runs_dir / alias).symlink_to(self.run_dir, target_is_directory=True)
        with self.assertRaisesRegex(op.InputError, "symlink component"):
            op.resolve_run(self.runs_dir, alias)

        outside_lock = self.root / "outside.lock"
        outside_lock.write_text("do not touch", encoding="utf-8")
        (self.run_dir / ".state.lock").symlink_to(outside_lock)
        with self.assertRaisesRegex(op.InputError, "symlink component"):
            op.start_job(self.run_dir, "escape", None)
        self.assertEqual(outside_lock.read_text(encoding="utf-8"), "do not touch")

    def test_boolean_schema_versions_and_event_sequence_are_rejected(self) -> None:
        manifest, state = self.load()
        bad_config = copy.deepcopy(manifest["config"])
        bad_config["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_config(bad_config)

        bad_manifest = copy.deepcopy(manifest)
        bad_manifest["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_manifest(bad_manifest)
        bad_state = copy.deepcopy(state)
        bad_state["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_state(bad_state, manifest)

        bad_candidate = self.candidate()
        bad_candidate["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_candidate(bad_candidate, manifest, self.run_dir)
        discovery = self.candidate()
        self.store_candidate(discovery)
        bad_research = self.research(discovery)
        bad_research["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_research(bad_research, manifest, self.run_dir)

        response = self.evaluation_input(
            discovery,
            "working-bool-schema",
            evaluation_type="working_research",
        )
        response.pop("_test_evaluation_type")
        bad_evaluation = op.canonicalize_evaluator_response(
            response, manifest, self.run_dir, "working_research"
        )
        bad_evaluation["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_canonical_evaluation(
                bad_evaluation, manifest, self.run_dir
            )

        raw = b"{}\n"
        raw_digest = op.sha256_bytes(raw)
        raw_rel = f"holdout/alpha/v1/raw/external-{raw_digest}.txt"
        op.write_immutable(self.run_dir / raw_rel, raw, root=self.run_dir)
        receipt = {
            "schema_version": True,
            "run_id": self.run_id,
            "candidate_id": "alpha",
            "raw_response_path": raw_rel,
            "raw_response_sha256": raw_digest,
            "status": "rejected",
            "error": "fixture rejection",
        }
        receipt_path = (
            self.run_dir
            / f"holdout/alpha/v1/imports/external-{raw_digest}.json"
        )
        op.write_immutable(receipt_path, op.canonical_json_bytes(receipt), root=self.run_dir)
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_external_imports(self.run_dir, manifest)

        event_path = self.run_dir / "events.jsonl"
        original_events = event_path.read_bytes()
        first = json.loads(event_path.read_text(encoding="utf-8").splitlines()[0])
        first["sequence"] = True
        event_path.write_text(json.dumps(first) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.load_events(event_path, self.run_id)
        event_path.write_bytes(original_events)

    def test_cli_exit_codes_for_input_and_premature_finalization_conflicts(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = op.main(["--runs-dir", str(self.runs_dir), "status", "missing"])
        self.assertEqual(code, 2)

        op.advance_run(self.run_dir)
        op.start_job(self.run_dir, "running", None)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            conflict = op.main(
                ["--runs-dir", str(self.runs_dir), "job", self.run_id, "running", "start"]
            )
        self.assertEqual(conflict, 3)
        op.resume_run(self.run_dir)
        op.start_job(self.run_dir, "running", None)
        op.fail_job(self.run_dir, "running", "exhausted")
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            premature = op.main(
                [
                    "--runs-dir",
                    str(self.runs_dir),
                    "finalize",
                    self.run_id,
                    "--no-finalist-reason",
                    "No viable candidates remained",
                ]
            )
        self.assertEqual(premature, 3)

    def test_command_level_new_status_resume_rejects_scoreless_finalize(self) -> None:
        isolated = self.root / "cli" / "runs"
        code, created, _ = self.run_cli(["--runs-dir", str(isolated), "new"])
        self.assertEqual(code, 0)
        run_id = created["run_id"]
        code, status, _ = self.run_cli(["--runs-dir", str(isolated), "status", run_id, "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(status["state"]["stage"], "initialized")
        self.assertEqual(self.run_cli(["--runs-dir", str(isolated), "job", run_id, "probe", "start"])[0], 0)
        code, resumed, _ = self.run_cli(["--runs-dir", str(isolated), "resume", run_id])
        self.assertEqual(code, 0)
        self.assertEqual(resumed["eligible_jobs"][0]["job_id"], "probe")
        self.assertEqual(self.run_cli(["--runs-dir", str(isolated), "job", run_id, "probe", "start"])[0], 0)
        self.assertEqual(
            self.run_cli(
                ["--runs-dir", str(isolated), "job", run_id, "probe", "fail", "--error", "bounded failure"]
            )[0],
            0,
        )
        code, final, _ = self.run_cli(
            [
                "--runs-dir",
                str(isolated),
                "finalize",
                run_id,
                "--no-finalist-reason",
                "Dry-run work was intentionally bounded",
            ]
        )
        self.assertEqual(code, 3)
        self.assertEqual(final, {})
        code, _, error = self.run_cli(["--runs-dir", str(isolated), "publish", run_id])
        self.assertEqual(code, 3)
        self.assertIn("publish requires a finalized run", error["error"])
        self.assertFalse((self.root / "cli/outcomes" / run_id / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
