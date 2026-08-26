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
        created = op.make_run(op.DEFAULT_CONFIG, self.runs_dir)
        self.run_id = created["run_id"]
        self.run_dir = Path(created["run_dir"])

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def load(self):
        return op.load_run(self.run_dir)

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
    ) -> dict:
        seed = fingerprint_seed or candidate_id
        schema_version = json.loads(op.DEFAULT_CONFIG.read_text(encoding="utf-8"))["schema_version"]
        sources = [] if stage == "discovery" else [f"source-{index}" for index in range(6)]
        return {
            "schema_version": schema_version,
            "candidate_id": candidate_id,
            "version": version,
            "parent": parent,
            "stage": stage,
            "title": f"Opportunity {candidate_id} v{version}",
            "thesis": f"A specific structural thesis for {candidate_id} version {version}.",
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
                    "claim_id": "claim-1",
                    "statement": "The triggering workflow is costly and recurring.",
                    "evidence_refs": sources[:1],
                    "confidence": "medium",
                }
            ],
            "contrary_evidence": ["Some buyers may internalize the work."],
            "uncertainties": ["Referral conversion remains untested."],
            "risks": ["A platform could narrow the workflow gap."],
        }

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
            }
            for index in range(6)
        ]
        return {
            "schema_version": candidate["schema_version"],
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "candidate_sha256": op.sha256_file(path),
            "sources": sources,
            "claims": [
                {
                    "claim_id": "research-claim-1",
                    "statement": "Primary sources support a recurring paid event.",
                    "assessment": "evidence",
                    "evidence_refs": ["source-0", "source-1"],
                }
            ],
            "contrary_evidence": ["One source describes an internal substitute."],
            "unknowns": ["Observed conversion is not yet available."],
        }

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
        op.start_job(self.run_dir, job_id, stage)
        return op.complete_job(self.run_dir, job_id, path, kind)

    def store_portfolio_selection(self, candidates: list[dict]) -> dict:
        payload = {
            "schema_version": 2,
            "selection_version": 1,
            "candidate_refs": [self.candidate_ref(candidate) for candidate in candidates],
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
            "schema_version": 2,
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
        base = base_candidate or candidate
        return {
            "schema_version": 2,
            "candidate_id": candidate["candidate_id"],
            "base_candidate_version": base["version"],
            "base_candidate_sha256": self.candidate_ref(base)["candidate_sha256"],
            "outcome": outcome,
            "final_candidate_version": candidate["version"],
            "final_candidate_sha256": self.candidate_ref(candidate)["candidate_sha256"],
            "constructor_id": constructor_id,
            "rationale": "One bounded constructor pass found no defensible structural redesign."
            if outcome == "no_valid_redesign"
            else "One bounded constructor pass produced the recorded structural redesign.",
        }

    def prepare_fatal_research_closure(self, candidate_id: str = "alpha") -> dict:
        discovery = self.candidate(candidate_id)
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        researched = self.candidate(
            candidate_id,
            version=2,
            stage="research",
            parent={"candidate_id": candidate_id, "version": 1},
        )
        self.store_candidate(researched)
        self.store_research(self.research(researched))
        self.store_evaluation(
            self.evaluation_input(
                researched,
                f"research-judge-{candidate_id}",
                score=6.5,
                evaluation_type="working",
            )
        )
        decision = self.portfolio_decision([researched], set())
        decision["candidate_decisions"][0].update(
            {
                "disposition": "fatal",
                "fatal_reason": "impossible_conservative_economics",
                "fatal_claim_ids": ["research-claim-1"],
                "rationale": "Direct sourced evidence makes the conservative unit economics impossible.",
            }
        )
        self.complete_json_job("portfolio-decision", "portfolio-decision", decision)
        return researched

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
            "schema_version": candidate["schema_version"],
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "candidate_sha256": op.sha256_file(candidate_path),
            "rubric_id": manifest["rubric"]["rubric_id"],
            "rubric_sha256": manifest["rubric"]["sha256"],
            "judge_id": judge_id,
            "evaluation_type": evaluation_type,
            "factors": factors,
            "interaction_adjustment": adjustment,
            "assumptions": ["Competent execution from the planning stage."],
            "main_structural_strength": f"Specific strength identified by {judge_id}.",
            "primary_score_limiter": f"Specific limiter identified by {judge_id}.",
            "strongest_disconfirming_evidence": f"Disconfirming evidence identified by {judge_id}.",
            "highest_value_structural_change": f"Structural change proposed by {judge_id}.",
            "evidence_needed_for_higher_score": f"Evidence request from {judge_id}.",
        }
        if evaluation_type == "holdout_native":
            raw_rel = f"holdout/jobs/{judge_id}.json"
        elif evaluation_type == "holdout_external":
            raw_rel = f"holdout/{candidate['candidate_id']}/v{candidate['version']}/raw/{judge_id}.json"
        else:
            raw_rel = f"evaluations/{candidate['candidate_id']}/v{candidate['version']}/raw/{judge_id}.txt"
        raw_path = self.run_dir / raw_rel
        if evaluation_type.startswith("holdout"):
            response = {key: evaluation[key] for key in op.EXTERNAL_RESPONSE_KEYS}
            raw = op.canonical_json_bytes(response)
        else:
            raw = f"raw independent response from {judge_id}\n".encode()
        op.write_immutable(raw_path, raw, root=self.run_dir)
        evaluation["raw_response_path"] = raw_rel
        evaluation["raw_response_sha256"] = op.sha256_bytes(raw)
        if evaluation_type == "holdout_native":
            manifest, state = self.load()
            if state["stage"] == "holdout":
                op.start_job(self.run_dir, judge_id, "holdout")
                op.complete_job(self.run_dir, judge_id, raw_path, "generic")
            else:
                # Isolated schema/scoring tests do not exercise run integrity.
                state["jobs"]["holdout"][judge_id] = {
                    "status": "completed",
                    "attempts": 1,
                    "max_attempts": manifest["config"]["mechanical_attempts"],
                    "artifact": raw_rel,
                    "artifact_sha256": op.sha256_bytes(raw),
                    "error": None,
                    "updated_at": op.utc_now(),
                }
                op.save_state(self.run_dir, state, manifest)
        return evaluation

    def store_evaluation(self, evaluation_input: dict) -> tuple[Path, dict]:
        manifest, _ = self.load()
        canonical = op.compute_evaluation(evaluation_input, manifest, self.run_dir)
        path = self.run_dir / op.evaluation_relpath(
            canonical["candidate_id"],
            canonical["candidate_version"],
            canonical["evaluation_type"],
            canonical["judge_id"],
        )
        op.write_immutable(path, op.canonical_json_bytes(canonical))
        if canonical["evaluation_type"] == "holdout_native" and manifest["config"]["schema_version"] == 2:
            self.ensure_direct_portfolio_contracts()
        return path, canonical

    def ensure_direct_portfolio_contracts(self) -> None:
        manifest, _ = self.load()
        selection_path = self.run_dir / "portfolio/selection.json"
        discoveries = [candidate for _, candidate in op.latest_candidates_for_stage(self.run_dir, manifest, "discovery")]
        if not selection_path.exists():
            selection = {
                "schema_version": 2,
                "selection_version": 1,
                "candidate_refs": [self.candidate_ref(candidate) for candidate in discoveries],
                "missing_archetypes": [],
                "rationale": "Canonical test shortlist covering every direct-lineage fixture candidate.",
            }
            canonical_selection = op.validate_portfolio_selection(selection, manifest, self.run_dir)
            op.write_immutable(selection_path, op.canonical_json_bytes(canonical_selection))
        decision_path = self.run_dir / "portfolio/development-decision.json"
        if not decision_path.exists():
            researched = [candidate for _, candidate in op.latest_candidates_for_stage(self.run_dir, manifest, "research")]
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
        researched = self.candidate(
            candidate_id,
            stage="research",
            version=2,
            parent={"candidate_id": candidate_id, "version": 1},
            capital=capital,
        )
        self.store_candidate(researched)
        self.store_research(self.research(researched))
        self.store_evaluation(
            self.evaluation_input(
                researched,
                f"working-research-{candidate_id}",
                score=7.8,
                evaluation_type="working",
            )
        )
        developed = self.candidate(
            candidate_id,
            stage="development",
            version=3,
            parent={"candidate_id": candidate_id, "version": 2},
            capital=capital,
        )
        self.store_candidate(developed)
        self.store_evaluation(
            self.evaluation_input(
                developed,
                f"working-{candidate_id}",
                score=8,
                evaluation_type="working",
            )
        )
        result = self.development_result(
            developed,
            constructor_id=f"constructor-{candidate_id}",
        )
        canonical_result = op.validate_development_result(result, self.load()[0], self.run_dir)
        op.write_immutable(
            self.run_dir / f"development/{candidate_id}/constructor-result.json",
            op.canonical_json_bytes(canonical_result),
        )
        frozen = self.candidate(
            candidate_id,
            stage="frozen",
            version=4,
            parent={"candidate_id": candidate_id, "version": 3},
            capital=capital,
        )
        self.store_candidate(frozen)
        return frozen

    def external_response(self, manifest: dict, *, judge_id: str, score: float) -> dict:
        return {
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
        self.assertEqual((self.run_dir / "inputs/config.json").read_bytes(), op.DEFAULT_CONFIG.read_bytes())
        self.assertEqual(sum(row["weight"] for row in manifest["rubric"]["factors"]), 100)
        events = op.load_events(self.run_dir / "events.jsonl", self.run_id)
        self.assertEqual([event["event"] for event in events], ["run_created"])
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

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
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

        op.start_job(self.run_dir, "atomic", None)
        with mock.patch.object(op, "append_event", side_effect=OSError("fail event failed")):
            with self.assertRaisesRegex(OSError, "fail event failed"):
                op.fail_job(self.run_dir, "atomic", "mechanical failure")
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["atomic"]["status"], "running")
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])
        op.fail_job(self.run_dir, "atomic", "mechanical failure")

        op.start_job(self.run_dir, "resume-atomic", None)
        with mock.patch.object(op, "append_event", side_effect=OSError("resume event failed")):
            with self.assertRaisesRegex(OSError, "resume event failed"):
                op.resume_run(self.run_dir)
        self.assertEqual(
            self.load()[1]["jobs"]["discovery"]["resume-atomic"]["status"],
            "running",
        )
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
        recovered_start = op.start_job(self.run_dir, "recover-start", None)
        self.assertTrue(recovered_start["idempotent"])
        self.assertEqual(recovered_start["attempts"], 1)

        with mock.patch.object(op, "save_state", side_effect=OSError("fail state failed")):
            with self.assertRaisesRegex(OSError, "fail state failed"):
                op.fail_job(self.run_dir, "recover-start", "bounded failure")
        self.assertEqual(self.load()[1]["jobs"]["discovery"]["recover-start"]["status"], "running")
        with self.assertRaisesRegex(op.InputError, "job lifecycle disagrees"):
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
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
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

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
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
        events_path.write_bytes(original)

        records = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines()]
        started = next(item for item in records if item["event"] == "job_started")
        started["details"]["attempt"] = 2
        events_path.write_text(
            "".join(json.dumps(item, sort_keys=True) + "\n" for item in records),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(op.InputError, "attempt is not consecutive"):
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)

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
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
        recovered = op.advance_run(self.run_dir)
        self.assertTrue(recovered["idempotent"])
        self.assertEqual(recovered["stage"], "discovery")
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

    def test_finalize_event_failure_leaves_visible_recoverable_artifacts(self) -> None:
        self.prepare_fatal_research_closure()
        with mock.patch.object(op, "append_event", side_effect=OSError("simulated final event failure")):
            with self.assertRaisesRegex(OSError, "simulated final event failure"):
                op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertEqual(self.load()[1]["stage"], "research")
        self.assertTrue((self.run_dir / "final/report.json").is_file())
        with self.assertRaisesRegex(op.InputError, "unreconciled finalization artifacts"):
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
        report, code = op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertTrue(report["idempotent"] is False)
        self.assertEqual(code, 4)
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

    def test_finalize_state_failure_after_event_is_reconciled(self) -> None:
        self.prepare_fatal_research_closure()
        original_save_state = op.save_state
        with mock.patch.object(op, "save_state", side_effect=OSError("simulated final state failure")):
            with self.assertRaisesRegex(OSError, "simulated final state failure"):
                op.finalize_run(self.run_dir, "No viable researched candidate remained")
        self.assertEqual(self.load()[1]["stage"], "research")
        with self.assertRaisesRegex(op.InputError, "lifecycle disagrees"):
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
        with mock.patch.object(op, "save_state", wraps=original_save_state):
            report, code = op.finalize_run(
                self.run_dir, "No viable researched candidate remained"
            )
        self.assertTrue(report["idempotent"])
        self.assertEqual(code, 4)
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])

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
        discovery = self.candidate(stage="discovery")
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        researched = self.candidate(version=2, stage="research", parent={"candidate_id": "alpha", "version": 1})
        self.store_candidate(researched)
        self.store_research(self.research(researched))
        self.store_evaluation(
            self.evaluation_input(researched, "research-judge-alpha", score=8, evaluation_type="working")
        )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision([researched], {"alpha"}),
        )
        op.advance_run(self.run_dir)
        developed = self.candidate(
            version=3,
            stage="development",
            parent={"candidate_id": "alpha", "version": 2},
        )
        self.complete_json_job("develop-alpha", "candidate", developed)
        self.store_evaluation(
            self.evaluation_input(developed, "development-judge-alpha", score=8, evaluation_type="working")
        )
        self.complete_json_job(
            "constructor-alpha",
            "development-result",
            self.development_result(developed, constructor_id="constructor-agent-alpha"),
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
        self.assertEqual(report["selected_candidate_version"], 2)
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
        self.assertTrue((self.root / "outcomes" / self.run_id / "candidates/alpha/v2.json").is_file())
        self.assertTrue((self.root / "outcomes" / self.run_id / "research/alpha/v2.json").is_file())
        history = (knowledge / "history_index.jsonl").read_text().splitlines()
        self.assertEqual(len(history), 2)
        meta = json.loads(history[0])
        self.assertEqual(
            meta["verification"],
            {
                "non_meta_rows": 1,
                "opportunity_outcome_corrections": 0,
                "opportunity_outcomes": 1,
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
        self.assertEqual(entry["record_type"], "opportunity_outcome_v1")
        self.assertEqual(entry["score_scale"], "/10")
        self.assertIsNone(entry["qualification_label"])
        self.assertEqual(entry["selected_candidate_id"], "alpha")
        self.assertEqual(entry["selected_title"], candidate["title"])
        self.assertEqual(entry["selected_fingerprint"], candidate["fingerprint"])
        self.assertEqual(entry["source_candidate_path"], "candidates/alpha/v2.json")
        self.assertEqual(entry["terminal_objection"], "Bounded discovery produced no viable shortlist")
        self.assertIn("Reopen only with new evidence", entry["reopen_condition"])

    def test_no_finalist_best_candidate_is_deterministic_for_multiple_candidates(self) -> None:
        discoveries = [self.candidate("alpha"), self.candidate("beta")]
        for discovery in discoveries:
            self.store_candidate(discovery)
        self.store_portfolio_selection(discoveries)
        self.set_stage("research")
        researched = []
        for discovery, score in zip(discoveries, (7.0, 8.0), strict=True):
            candidate = self.candidate(
                discovery["candidate_id"],
                version=2,
                stage="research",
                parent={"candidate_id": discovery["candidate_id"], "version": 1},
            )
            self.store_candidate(candidate)
            self.store_research(self.research(candidate))
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"research-judge-{candidate['candidate_id']}",
                    score=score,
                    evaluation_type="working",
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

    def test_candidate_exact_shape_and_researched_source_minimum(self) -> None:
        manifest, _ = self.load()
        self.store_candidate(self.candidate(stage="discovery"))
        invalid = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        invalid["source_refs"] = ["only-one"]
        with self.assertRaisesRegex(op.InputError, "at least 6 sources"):
            op.validate_candidate(invalid, manifest, self.run_dir)
        extra = self.candidate()
        extra["unexpected"] = True
        with self.assertRaisesRegex(op.InputError, "keys differ"):
            op.validate_candidate(extra, manifest, self.run_dir)
        dangling = self.candidate()
        dangling["claims"][0]["evidence_refs"] = ["not-in-source-refs"]
        with self.assertRaisesRegex(op.InputError, "unknown source_refs"):
            op.validate_candidate(dangling, manifest, self.run_dir)

    def test_identity_whitespace_and_frozen_capital_are_unambiguous(self) -> None:
        manifest, _ = self.load()
        whitespace = self.candidate()
        whitespace["candidate_id"] = " alpha "
        with self.assertRaisesRegex(op.InputError, "surrounding whitespace"):
            op.validate_candidate(whitespace, manifest, self.run_dir)
        early_string = self.candidate(capital="50,000 PLN")
        self.assertEqual(
            op.validate_candidate(early_string, manifest, self.run_dir)["economics"]["capital_required_pln"],
            "50,000 PLN",
        )
        frozen_string = copy.deepcopy(self.store_complete_lineage())
        frozen_string["economics"]["capital_required_pln"] = "50,000 PLN"
        with self.assertRaisesRegex(op.InputError, "must be a JSON number"):
            op.validate_candidate(frozen_string, manifest, self.run_dir)
        frozen_negative = copy.deepcopy(frozen_string)
        frozen_negative["economics"]["capital_required_pln"] = -1
        with self.assertRaisesRegex(op.InputError, "must be nonnegative"):
            op.validate_candidate(frozen_negative, manifest, self.run_dir)

    def test_research_contract_hash_references_and_canonical_job_path(self) -> None:
        self.set_stage("research")
        self.store_candidate(self.candidate(stage="discovery"))
        candidate = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(candidate)
        research = self.research(candidate)
        input_path = self.root / "research.json"
        input_path.write_text(json.dumps(research), encoding="utf-8")
        op.start_job(self.run_dir, "research-alpha", None)
        completed = op.complete_job(self.run_dir, "research-alpha", input_path, "research")
        self.assertEqual(completed["artifact"], "research/alpha/v2.json")
        invalid = copy.deepcopy(research)
        invalid["claims"][0]["evidence_refs"] = ["missing-source"]
        with self.assertRaisesRegex(op.InputError, "unknown sources"):
            op.validate_research(invalid, self.load()[0], self.run_dir)

    def test_decimal_half_up_strict_threshold_exclusion_and_clamp(self) -> None:
        candidate = self.store_complete_lineage()
        manifest, _ = self.load()

        rounded = op.compute_evaluation(
            self.evaluation_input(candidate, "rounding", score=8.55), manifest, self.run_dir
        )
        self.assertEqual(rounded["final_score"], 8.6)
        self.assertTrue(rounded["qualified"])

        boundary = op.compute_evaluation(
            self.evaluation_input(candidate, "boundary", score=8.5), manifest, self.run_dir
        )
        self.assertEqual(boundary["final_score"], 8.5)
        self.assertFalse(boundary["qualified"])

        excluded = op.compute_evaluation(
            self.evaluation_input(candidate, "excluded", score=9, excluded={"Core insight"}),
            manifest,
            self.run_dir,
        )
        self.assertEqual(excluded["base_score"], 9)
        core = next(item for item in excluded["factors"] if item["name"] == "Core insight")
        economics = next(item for item in excluded["factors"] if item["name"] == "Business model and economics")
        self.assertEqual(core["effective_weight"], 0)
        self.assertEqual(economics["effective_weight"], 22.44898)

        clamped_input = self.evaluation_input(candidate, "clamped", score=10, adjustment=0.5)
        clamped = op.compute_evaluation(clamped_input, manifest, self.run_dir)
        self.assertEqual(clamped["unrounded_score"], 10.5)
        self.assertEqual(clamped["constrained_score"], 10)
        self.assertEqual(clamped["final_score"], 10)

    def test_model_supplied_wrong_arithmetic_is_rejected(self) -> None:
        candidate = self.store_complete_lineage()
        manifest, _ = self.load()
        evaluation = self.evaluation_input(candidate, "bad-math", score=9)
        evaluation["base_score"] = 9.1
        with self.assertRaisesRegex(op.InputError, "does not match deterministic scoring"):
            op.compute_evaluation(evaluation, manifest, self.run_dir)

    def test_evaluation_rejects_missing_invalid_ambiguous_and_unbound_inputs(self) -> None:
        candidate = self.store_complete_lineage()
        manifest, _ = self.load()

        missing_factor = self.evaluation_input(candidate, "missing-factor")
        missing_factor["factors"].pop()
        with self.assertRaisesRegex(op.InputError, "factors differ from rubric"):
            op.compute_evaluation(missing_factor, manifest, self.run_dir)

        invalid_exclusion = self.evaluation_input(candidate, "invalid-exclusion")
        invalid_exclusion["factors"][0].update({"status": "excluded", "score": 7})
        with self.assertRaisesRegex(op.InputError, "must have null score"):
            op.compute_evaluation(invalid_exclusion, manifest, self.run_dir)

        out_of_range = self.evaluation_input(candidate, "scale-85")
        out_of_range["factors"][0]["score"] = 85
        with self.assertRaisesRegex(op.InputError, r"must be in \[1, 10\]"):
            op.compute_evaluation(out_of_range, manifest, self.run_dir)

        ambiguous = self.evaluation_input(candidate, "ambiguous")
        ambiguous["factors"][0]["score"] = "9"
        with self.assertRaisesRegex(op.InputError, "must be a JSON number"):
            op.compute_evaluation(ambiguous, manifest, self.run_dir)

        wrong_hash = self.evaluation_input(candidate, "wrong-hash")
        wrong_hash["candidate_sha256"] = "0" * 64
        with self.assertRaisesRegex(op.InputError, "does not match the immutable candidate"):
            op.compute_evaluation(wrong_hash, manifest, self.run_dir)

        wrong_version = self.evaluation_input(candidate, "wrong-version")
        wrong_version["candidate_version"] = 99
        with self.assertRaisesRegex(op.InputError, "candidate artifact does not exist"):
            op.compute_evaluation(wrong_version, manifest, self.run_dir)

        missing_raw = self.evaluation_input(candidate, "missing-raw")
        del missing_raw["raw_response_path"]
        with self.assertRaisesRegex(op.InputError, "missing=.*raw_response_path"):
            op.compute_evaluation(missing_raw, manifest, self.run_dir)

        malformed = self.root / "malformed.json"
        malformed.write_text('{"score": 9,,}', encoding="utf-8")
        with self.assertRaisesRegex(op.InputError, "invalid JSON"):
            op.load_json(malformed)

    def test_stage_and_lineage_bindings_reject_contamination(self) -> None:
        manifest, _ = self.load()
        discovery = self.candidate(stage="discovery")
        self.store_candidate(discovery)
        bad_parent = self.candidate(
            "beta",
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        with self.assertRaisesRegex(op.InputError, "same candidate_id"):
            op.validate_candidate(bad_parent, manifest, self.run_dir)
        skipped = self.candidate(
            version=3,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        with self.assertRaisesRegex(op.InputError, "version N-1"):
            op.validate_candidate(skipped, manifest, self.run_dir)

        wrong_research = self.research(discovery)
        with self.assertRaisesRegex(op.InputError, "research-stage candidate"):
            op.validate_research(wrong_research, manifest, self.run_dir)

        researched = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(researched)
        research_working = self.evaluation_input(
            researched,
            "working-research",
            evaluation_type="working",
        )
        computed = op.compute_evaluation(research_working, manifest, self.run_dir)
        self.assertEqual(computed["evaluation_type"], "working")
        self.assertEqual(computed["candidate_version"], 2)

        wrong_working = self.evaluation_input(discovery, "working-wrong", evaluation_type="working")
        with self.assertRaisesRegex(op.InputError, "development or research-stage candidate"):
            op.compute_evaluation(wrong_working, manifest, self.run_dir)

        wrong_holdout = self.evaluation_input(researched, "holdout-wrong")
        with self.assertRaisesRegex(op.InputError, "frozen-stage candidate"):
            op.compute_evaluation(wrong_holdout, manifest, self.run_dir)

    def test_finalist_requires_monotonic_full_lineage_and_own_working_evaluation(self) -> None:
        manifest, _ = self.load()
        alpha_discovery = self.candidate("alpha", stage="discovery", version=1)
        self.store_candidate(alpha_discovery)
        skipped = self.candidate(
            "alpha",
            stage="development",
            version=2,
            parent={"candidate_id": "alpha", "version": 1},
        )
        with self.assertRaisesRegex(op.InputError, "without skipping"):
            op.validate_candidate(skipped, manifest, self.run_dir)
        alpha_research = self.candidate(
            "alpha",
            stage="research",
            version=2,
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(alpha_research)
        self.store_research(self.research(alpha_research))
        backwards = self.candidate(
            "alpha",
            stage="discovery",
            version=3,
            parent={"candidate_id": "alpha", "version": 2},
        )
        with self.assertRaisesRegex(op.InputError, "monotonically"):
            op.validate_candidate(backwards, manifest, self.run_dir)
        repeated_research = self.candidate(
            "alpha",
            stage="research",
            version=3,
            parent={"candidate_id": "alpha", "version": 2},
        )
        with self.assertRaisesRegex(op.InputError, "only development"):
            op.validate_candidate(repeated_research, manifest, self.run_dir)
        alpha_development = self.candidate(
            "alpha",
            stage="development",
            version=3,
            parent={"candidate_id": "alpha", "version": 2},
        )
        self.store_candidate(alpha_development)

        beta_discovery = self.candidate("beta", stage="discovery", version=1)
        self.store_candidate(beta_discovery)
        beta_research = self.candidate(
            "beta",
            stage="research",
            version=2,
            parent={"candidate_id": "beta", "version": 1},
        )
        self.store_candidate(beta_research)
        beta_development = self.candidate(
            "beta",
            stage="development",
            version=3,
            parent={"candidate_id": "beta", "version": 2},
        )
        self.store_candidate(beta_development)
        self.store_evaluation(
            self.evaluation_input(
                beta_development,
                "working-beta",
                evaluation_type="working",
            )
        )

        alpha_frozen = self.candidate(
            "alpha",
            stage="frozen",
            version=4,
            parent={"candidate_id": "alpha", "version": 3},
        )
        candidate_input = self.root / "alpha-frozen.json"
        candidate_input.write_text(json.dumps(alpha_frozen), encoding="utf-8")
        self.set_stage("frozen")
        op.start_job(self.run_dir, "freeze-alpha", "frozen")
        with self.assertRaisesRegex(op.InputError, "requires exactly 1 working evaluation.*v3"):
            op.complete_job(self.run_dir, "freeze-alpha", candidate_input, "candidate")
        self.store_evaluation(
            self.evaluation_input(
                alpha_development,
                "working-alpha",
                evaluation_type="working",
            )
        )
        development_result = self.development_result(
            alpha_development,
            constructor_id="constructor-alpha",
        )
        canonical_result = op.validate_development_result(
            development_result,
            self.load()[0],
            self.run_dir,
        )
        op.write_immutable(
            self.run_dir / "development/alpha/constructor-result.json",
            op.canonical_json_bytes(canonical_result),
        )
        completed = op.complete_job(self.run_dir, "freeze-alpha", candidate_input, "candidate")
        self.assertEqual(completed["artifact"], "candidates/alpha/v4.json")
        exported = op.export_external(self.run_dir, "alpha")
        self.assertEqual(exported["candidate_version"], 4)

    def test_development_allows_two_versions_not_three(self) -> None:
        discovery = self.candidate(stage="discovery")
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        v1 = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(v1)
        self.store_research(self.research(v1))
        self.store_evaluation(
            self.evaluation_input(v1, "research-judge-alpha", score=8, evaluation_type="working")
        )
        self.complete_json_job(
            "portfolio-decision",
            "portfolio-decision",
            self.portfolio_decision([v1], {"alpha"}),
        )
        op.advance_run(self.run_dir)
        v2 = self.candidate(version=3, stage="development", parent={"candidate_id": "alpha", "version": 2})
        p2 = self.root / "v2.json"
        p2.write_text(json.dumps(v2), encoding="utf-8")
        op.start_job(self.run_dir, "develop-v2", None)
        op.complete_job(self.run_dir, "develop-v2", p2, "candidate")
        v3 = self.candidate(version=4, stage="development", parent={"candidate_id": "alpha", "version": 3})
        with self.assertRaisesRegex(op.InputError, "requires candidate.redesign"):
            op.validate_candidate(v3, self.load()[0], self.run_dir)
        v3["fingerprint"]["customer"] = "A structurally narrower customer with a different purchasing authority"
        v3["economics"]["pricing"] = "Outcome-linked pricing tied to the redesigned paid event"
        v3["redesign"] = {
            "changed_fingerprint_fields": ["customer"],
            "economic_effect": "The narrower authority shortens approval time and supports outcome-linked pricing.",
        }
        p3 = self.root / "v3.json"
        p3.write_text(json.dumps(v3), encoding="utf-8")
        op.start_job(self.run_dir, "develop-v3", None)
        op.complete_job(self.run_dir, "develop-v3", p3, "candidate")
        v4 = self.candidate(version=5, stage="development", parent={"candidate_id": "alpha", "version": 4})
        v4["redesign"] = {
            "changed_fingerprint_fields": ["customer"],
            "economic_effect": "This forbidden second redesign would restore the original customer and economics.",
        }
        p4 = self.root / "v4.json"
        p4.write_text(json.dumps(v4), encoding="utf-8")
        op.start_job(self.run_dir, "develop-v4", None)
        with self.assertRaisesRegex(op.ConflictError, "at most two"):
            op.complete_job(self.run_dir, "develop-v4", p4, "candidate")
        self.assertEqual(op._stage_candidate_count(self.run_dir, self.load()[0], "development"), 1)

    def test_development_redesign_requires_fingerprint_change_and_economic_effect(self) -> None:
        discovery = self.candidate(stage="discovery")
        self.store_candidate(discovery)
        researched = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(researched)
        developed = self.candidate(
            version=3,
            stage="development",
            parent={"candidate_id": "alpha", "version": 2},
        )
        self.store_candidate(developed)
        revision = self.candidate(
            version=4,
            stage="development",
            parent={"candidate_id": "alpha", "version": 3},
        )
        revision["redesign"] = {
            "changed_fingerprint_fields": ["customer"],
            "economic_effect": "A claimed effect without an actual structural change.",
        }
        with self.assertRaisesRegex(op.InputError, "exactly match normalized fingerprint changes"):
            op.validate_candidate(revision, self.load()[0], self.run_dir)

        revision["fingerprint"]["customer"] = "A materially different buyer with its own budget"
        with self.assertRaisesRegex(op.InputError, "update at least one economics field"):
            op.validate_candidate(revision, self.load()[0], self.run_dir)

        revision["economics"]["pricing"] = "A documented annual contract funded by that buyer"
        canonical = op.validate_candidate(revision, self.load()[0], self.run_dir)
        self.assertEqual(canonical["redesign"]["changed_fingerprint_fields"], ["customer"])


class WorkflowV2ContractTests(OpportunityTestCase):
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
            candidate = self.candidate(
                discovery["candidate_id"],
                version=2,
                stage="research",
                parent={"candidate_id": discovery["candidate_id"], "version": 1},
            )
            self.store_candidate(candidate)
            self.store_research(self.research(candidate))
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"research-judge-{candidate['candidate_id']}",
                    score=score,
                    evaluation_type="working",
                )
            )
            researched.append(candidate)
        return discoveries, researched

    def test_research_advance_and_finalize_require_exact_working_coverage(self) -> None:
        discovery = self.candidate("alpha")
        self.store_candidate(discovery)
        self.store_portfolio_selection([discovery])
        self.set_stage("research")
        researched = self.candidate(
            "alpha",
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(researched)
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
                evaluation_type="working",
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
                evaluation_type="working",
            )
        )
        coverage = op.working_evaluation_coverage(self.run_dir, self.load()[0], "research")
        self.assertFalse(coverage["complete"])
        self.assertEqual(coverage["duplicates"], ["alpha v2"])
        with self.assertRaisesRegex(op.ConflictError, "duplicate alpha v2"):
            op.advance_run(self.run_dir)

    def test_research_candidate_substitution_requires_versioned_amendment(self) -> None:
        alpha = self.candidate("alpha")
        beta = self.candidate("beta")
        self.store_candidate(alpha)
        self.store_candidate(beta)
        self.store_portfolio_selection([alpha])
        self.set_stage("research")
        researched_beta = self.candidate(
            "beta",
            version=2,
            stage="research",
            parent={"candidate_id": "beta", "version": 1},
        )
        path = self.root / "unamended-beta.json"
        path.write_text(json.dumps(researched_beta), encoding="utf-8")
        op.start_job(self.run_dir, "unamended-beta", "research")
        with self.assertRaisesRegex(op.ConflictError, "versioned amendment before substitution"):
            op.complete_job(self.run_dir, "unamended-beta", path, "candidate")
        op.fail_job(self.run_dir, "unamended-beta", "shortlist binding correctly rejected substitution")

        selection_path = self.run_dir / "portfolio/selection.json"
        amendment = {
            "schema_version": 2,
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
            "candidate",
            researched_beta,
        )
        self.assertEqual(accepted["artifact"], "candidates/beta/v2.json")

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
            version=3,
            stage="development",
            parent={"candidate_id": research_candidate["candidate_id"], "version": 2},
        )
        self.complete_json_job("develop-alpha", "candidate", developed)
        self.complete_json_job(
            "constructor-alpha",
            "development-result",
            self.development_result(developed, constructor_id="same-agent"),
        )

        with self.assertRaisesRegex(op.ConflictError, "missing candidate-1 v3"):
            op.advance_run(self.run_dir)
        self.store_evaluation(
            self.evaluation_input(
                developed,
                "same-agent",
                score=8.2,
                evaluation_type="working",
            )
        )
        with self.assertRaisesRegex(op.ConflictError, "constructor and working evaluator roles must be independent"):
            op.advance_run(self.run_dir)

    def test_native_holdout_judge_cannot_reuse_a_development_role(self) -> None:
        frozen = self.store_complete_lineage("alpha")
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        reused = self.evaluation_input(frozen, "working-alpha", score=8.8)
        input_path = self.root / "reused-native-wrapper.json"
        input_path.write_text(json.dumps(reused), encoding="utf-8")
        op.start_job(self.run_dir, "reused-native-wrapper", "holdout")
        with self.assertRaisesRegex(
            op.ConflictError,
            "native holdout judge must be fresh and independent",
        ):
            op.complete_job(
                self.run_dir,
                "reused-native-wrapper",
                input_path,
                "evaluation",
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
            candidate = self.candidate(
                candidate_id,
                version=3,
                stage="development",
                parent={"candidate_id": candidate_id, "version": 2},
            )
            self.complete_json_job(f"develop-{candidate_id}", "candidate", candidate)
            self.store_evaluation(
                self.evaluation_input(
                    candidate,
                    f"development-judge-{candidate_id}",
                    score=8.4 - index / 10,
                    evaluation_type="working",
                )
            )
            self.complete_json_job(
                f"constructor-{candidate_id}",
                "development-result",
                self.development_result(
                    candidate,
                    constructor_id=f"constructor-agent-{candidate_id}",
                ),
            )
            developed.append(candidate)

        self.assertEqual(op.advance_run(self.run_dir)["stage"], "frozen")
        frozen: list[dict] = []
        for developed_candidate in developed[:2]:
            candidate_id = developed_candidate["candidate_id"]
            candidate = self.candidate(
                candidate_id,
                version=4,
                stage="frozen",
                parent={"candidate_id": candidate_id, "version": 3},
            )
            self.complete_json_job(f"freeze-{candidate_id}", "candidate", candidate)
            op.export_external(self.run_dir, candidate_id)
            frozen.append(candidate)

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
        self.assertEqual(campaign_metrics["best_working_score"], 8.4)
        self.assertEqual(campaign_metrics["top_four_working_median"], 8.3)
        self.assertEqual(len(campaign_metrics["archetype_scores"]), 8)
        self.assertTrue(campaign_metrics["deficient_factors"])
        self.assertTrue(op.check_run(self.run_dir, op.DEFAULT_CONFIG)["valid"])
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
            len(list(published_root.glob("evaluations/*/v*/working-*.json"))),
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
                evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
                raw_path = published_root / evaluation["raw_response_path"]
                self.assertTrue(raw_path.is_file())
                self.assertEqual(
                    op.sha256_file(raw_path), evaluation["raw_response_sha256"]
                )
                published_holdouts.append(evaluation_path)
        self.assertEqual(len(published_holdouts), 4)
        validated_publication = op.validate_published_run_outcome(published_root)
        self.assertEqual(validated_publication["run_id"], self.run_id)
        working_record = report["working_evaluation_coverage"]["research"]["records"][0]
        working_evaluation = json.loads(
            (published_root / working_record["evaluation_path"]).read_text(
                encoding="utf-8"
            )
        )
        (published_root / working_evaluation["raw_response_path"]).unlink()
        with self.assertRaisesRegex(
            op.InputError, "working evaluation raw response"
        ):
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


class CampaignContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.campaigns_dir = self.root / "campaigns"
        self.outcomes_dir = self.root / "outcomes"
        created = op.new_campaign(op.DEFAULT_CONFIG, self.campaigns_dir)
        self.campaign_id = created["campaign_id"]
        self.campaign_dir = Path(created["campaign_dir"])
        self.config = json.loads(op.DEFAULT_CONFIG.read_text(encoding="utf-8"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def metrics(
        self,
        score: float,
        *,
        archetype: str = "baseline archetype",
        median: float | None = None,
        best: float | None = None,
    ) -> dict:
        return {
            "official_score": score,
            "top_four_working_median": score if median is None else median,
            "best_working_score": score if best is None else best,
            "archetype_scores": {archetype: score if best is None else best},
            "deficient_factors": ["Distribution", "Business model and economics"],
            "missing_archetypes": ["asset aggregation"],
            "dominant_patterns": {
                "commercial_archetype": "managed workflow",
                "control_point": "case evidence",
                "critical_dependency": "referral access",
            },
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
                "schema_version": 2,
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
            "schema_version": 2,
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
            "best_working_score": 7.5,
            "seen_archetypes": ["baseline archetype"],
        }
        cases = (
            (
                self.metrics(7.3, median=7.0, best=7.5),
                "official_score",
            ),
            (
                self.metrics(7.2, median=7.2, best=7.5),
                "working_median",
            ),
            (
                self.metrics(7.2, archetype="novel archetype", median=7.0, best=7.0),
                "novel_archetype",
            ),
        )
        for metrics, expected_signal in cases:
            with self.subTest(expected_signal=expected_signal):
                signals = op.campaign_progress_signals(state, metrics, self.config)
                self.assertTrue(signals[expected_signal])
                self.assertEqual(sum(signals.values()), 1)

    def test_campaign_gap_brief_is_sanitized_and_cohort_binding_is_immutable(self) -> None:
        first = op.campaign_next(self.campaign_dir)
        self.assertEqual(first["cohort_number"], 1)
        runs_dir = self.root / "runs"
        created = op.make_run(
            op.DEFAULT_CONFIG,
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
                op.DEFAULT_CONFIG,
                runs_dir,
                campaign_id=self.campaign_id,
                campaigns_dir=self.campaigns_dir,
            )

        replacement = op.new_campaign(op.DEFAULT_CONFIG, self.campaigns_dir)
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
        metric_forgery["cohorts"][0]["best_working_score"] = 9.9
        metric_forgery["cohorts"][0]["archetype_scores"] = {
            "baseline archetype": 9.9
        }
        metric_forgery["best_working_median"] = 9.9
        metric_forgery["best_working_score"] = 9.9
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
            "schema_version": 2,
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
        created = op.new_campaign(op.DEFAULT_CONFIG, clean_campaigns)
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
        created = op.new_campaign(op.DEFAULT_CONFIG, other_campaigns)
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
    def test_dedup_exact_similarity_and_one_bounded_gap_scout(self) -> None:
        self.set_stage("discovery")
        alpha = self.candidate("alpha", fingerprint_seed="shared stable structure")
        beta = self.candidate("beta", fingerprint_seed="shared stable structures")
        duplicate = self.candidate("gamma", fingerprint_seed="shared stable structure")
        for candidate in (alpha, beta, duplicate):
            self.store_candidate(candidate)
        first = op.dedup_run(self.run_dir)
        self.assertEqual(first["candidate_count"], 3)
        self.assertEqual(first["exact_fingerprint_unique_count"], 2)
        self.assertEqual(len(first["duplicate_groups"]), 1)
        self.assertTrue(first["similarity_flags"])
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

    def test_dominant_structure_groups_payer_and_business_model_not_distribution(self) -> None:
        self.set_stage("discovery")
        alpha = self.candidate("alpha", fingerprint_seed="alpha")
        beta = self.candidate("beta", fingerprint_seed="beta")
        gamma = self.candidate("gamma", fingerprint_seed="gamma")
        beta["fingerprint"]["payer_and_paid_event"] = alpha["fingerprint"]["payer_and_paid_event"]
        beta["fingerprint"]["offer_and_business_model"] = alpha["fingerprint"]["offer_and_business_model"]
        beta["fingerprint"]["distribution_mechanism"] = "a deliberately different direct channel"
        for candidate in (alpha, beta, gamma):
            self.store_candidate(candidate)
        report = op.build_dedup_report(self.run_dir, self.load()[0])
        self.assertEqual(report["dominant_structure"]["count"], 2)
        self.assertNotIn("distribution_mechanism", report["dominant_structure"])

    def _store_lineage_with_research(self, candidate_id: str = "alpha", *, capital: object = 100000) -> dict:
        return self.store_complete_lineage(candidate_id, capital=capital)

    def test_external_packet_import_rejection_preservation_and_binding(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        exported = op.export_external(self.run_dir, "alpha")
        packet = (self.run_dir / exported["packet"]).read_text(encoding="utf-8")
        self.assertIn((self.run_dir / "inputs/founder.md").read_text().strip(), packet)
        self.assertIn((self.run_dir / "inputs/evaluator.txt").read_text().strip(), packet)
        self.assertIn("research/alpha/v2.json", packet)
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
            (self.run_dir / f"holdout/alpha/v4/raw/external-{malformed_digest}.txt").is_file()
        )
        rejected = op.load_json(
            self.run_dir / f"holdout/alpha/v4/imports/external-{malformed_digest}.json"
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
            / f"holdout/alpha/v4/imports/external-{imported['raw_response_sha256']}.json"
        )
        receipt_bytes = receipt_path.read_bytes()

        evaluation_path.unlink()
        with self.assertRaisesRegex(op.InputError, "external import evaluation.*does not exist"):
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)

        evaluation_path.write_bytes(evaluation_bytes)
        receipt_path.write_bytes(receipt_bytes)
        self.store_evaluation(self.evaluation_input(frozen, "native-a", score=9))
        self.store_evaluation(self.evaluation_input(frozen, "native-b", score=9))
        report, code = op.finalize_run(self.run_dir)
        self.assertEqual(code, 4)
        self.assertEqual(report["run_status"], "contested")

    def test_native_holdout_raw_body_job_and_wrapper_are_strictly_bound(self) -> None:
        frozen = self._store_lineage_with_research()
        self.set_stage("holdout")
        op.export_external(self.run_dir, "alpha")
        manifest, state = self.load()

        arbitrary = self.evaluation_input(frozen, "native-arbitrary", score=9)
        arbitrary_path = self.run_dir / arbitrary["raw_response_path"]
        original_arbitrary_bytes = arbitrary_path.read_bytes()
        arbitrary_bytes = b"not JSON and not an evaluation\n"
        arbitrary_path.write_bytes(arbitrary_bytes)
        arbitrary["raw_response_sha256"] = op.sha256_bytes(arbitrary_bytes)
        state = self.load()[1]
        state["jobs"]["holdout"]["native-arbitrary"]["artifact_sha256"] = arbitrary["raw_response_sha256"]
        op.save_state(self.run_dir, state, manifest)
        with self.assertRaisesRegex(op.InputError, "invalid JSON"):
            op.compute_evaluation(arbitrary, manifest, self.run_dir)
        arbitrary_path.write_bytes(original_arbitrary_bytes)
        state = self.load()[1]
        state["jobs"]["holdout"]["native-arbitrary"]["artifact_sha256"] = op.sha256_bytes(
            original_arbitrary_bytes
        )
        op.save_state(self.run_dir, state, manifest)

        mismatch = self.evaluation_input(frozen, "native-mismatch", score=9)
        mismatch["primary_score_limiter"] = "A wrapper-only substituted limiter."
        with self.assertRaisesRegex(op.InputError, "primary_score_limiter differs"):
            op.compute_evaluation(mismatch, manifest, self.run_dir)

        unbound = self.evaluation_input(frozen, "native-unbound", score=9)
        state = self.load()[1]
        del state["jobs"]["holdout"]["native-unbound"]
        op.save_state(self.run_dir, state, manifest)
        with self.assertRaisesRegex(op.InputError, "not bound to exactly one completed holdout job"):
            op.compute_evaluation(unbound, manifest, self.run_dir)

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

        other = OpportunityTestCase(methodName="runTest")
        other.setUp()
        try:
            discovery = other.candidate()
            other.store_candidate(discovery)
            researched = other.candidate(
                version=2,
                stage="research",
                parent={"candidate_id": "alpha", "version": 1},
            )
            other.store_candidate(researched)
            other.store_research(other.research(researched))
            developed = other.candidate(
                version=3,
                stage="development",
                parent={"candidate_id": "alpha", "version": 2},
            )
            other.store_candidate(developed)
            other.store_evaluation(
                other.evaluation_input(
                    developed,
                    "working-alpha",
                    score=8,
                    evaluation_type="working",
                )
            )
            frozen_without_packet = other.candidate(
                version=4,
                stage="frozen",
                parent={"candidate_id": "alpha", "version": 3},
            )
            other.store_candidate(frozen_without_packet)
            other.set_stage("frozen")
            with self.assertRaisesRegex(op.ConflictError, "must continue to holdout"):
                op.finalize_run(other.run_dir, "Holdout packet could not be completed")
        finally:
            other.tearDown()

    def test_final_tie_break_report_and_qualified_publication(self) -> None:
        alpha = self._store_lineage_with_research("alpha", capital=50000)
        beta = self._store_lineage_with_research("beta", capital=200000)
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
        self.assertTrue((published / "candidates/beta/v4.json").is_file())
        self.assertTrue((published / "research/beta/v2.json").is_file())
        self.assertTrue((published / "exports/beta/holdout_packet.md").is_file())
        self.assertTrue((published / "holdout/jobs/native-a-beta.json").is_file())
        self.assertTrue((published / "candidates/alpha/v4.json").is_file())
        self.assertTrue((published / "exports/alpha/holdout_packet.md").is_file())
        self.assertTrue((published / "exports/alpha/response_schema.json").is_file())
        self.assertTrue((published / "holdout/jobs/native-a-alpha.json").is_file())
        self.assertTrue((published / "holdout/jobs/native-b-alpha.json").is_file())
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

        alpha = self._store_lineage_with_research("alpha")
        beta = self._store_lineage_with_research("beta")
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
            response_path.write_text(
                json.dumps(self.external_response(manifest, judge_id=judge_id, score=score)),
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
        self.assertTrue((published / "holdout/jobs/native-a-alpha.json").is_file())
        alpha_receipts = list((published / "holdout/alpha/v4/imports").glob("external-*.json"))
        alpha_raw = list((published / "holdout/alpha/v4/raw").glob("external-*.txt"))
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)


class IntegrityAndExitCodeTests(OpportunityTestCase):
    def run_cli(self, argv: list[str]) -> tuple[int, dict, dict]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = op.main(argv)
        output = json.loads(stdout.getvalue()) if stdout.getvalue().strip() else {}
        error = json.loads(stderr.getvalue()) if stderr.getvalue().strip() else {}
        return code, output, error

    def test_check_detects_snapshot_and_event_corruption(self) -> None:
        originals = {
            "inputs/founder.md": (op.REPO_ROOT / "PERSONALITY_SITUATION.md").read_bytes(),
            "inputs/evaluator.txt": (op.REPO_ROOT / "Personalities/ZeroToOne.txt").read_bytes(),
            "inputs/config.json": op.DEFAULT_CONFIG.read_bytes(),
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
            op.check_run(self.run_dir, op.DEFAULT_CONFIG)

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
        researched = self.candidate(
            version=2,
            stage="research",
            parent={"candidate_id": "alpha", "version": 1},
        )
        self.store_candidate(researched)
        bad_research = self.research(researched)
        bad_research["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.validate_research(bad_research, manifest, self.run_dir)

        developed = self.candidate(
            version=3,
            stage="development",
            parent={"candidate_id": "alpha", "version": 2},
        )
        self.store_candidate(developed)
        bad_evaluation = self.evaluation_input(
            developed,
            "working-bool-schema",
            evaluation_type="working",
        )
        bad_evaluation["schema_version"] = True
        with self.assertRaisesRegex(op.InputError, "must be an integer"):
            op.compute_evaluation(bad_evaluation, manifest, self.run_dir)

        raw = b"{}\n"
        raw_digest = op.sha256_bytes(raw)
        raw_rel = f"holdout/alpha/v4/raw/external-{raw_digest}.txt"
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
            / f"holdout/alpha/v4/imports/external-{raw_digest}.json"
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

    def test_schema_v1_runs_are_readable_but_all_active_mutations_are_rejected(self) -> None:
        run_id = "20260820T000000Z-abc123"
        run_dir = self.root / "legacy-runs" / run_id
        run_dir.mkdir(parents=True)
        config = json.loads(op.DEFAULT_CONFIG.read_text(encoding="utf-8"))
        config["schema_version"] = 1
        for key in op.CONFIG_V2_EXTRA_KEYS:
            config.pop(key)
        config_bytes = op.canonical_json_bytes(config)
        founder_bytes = (op.REPO_ROOT / "PERSONALITY_SITUATION.md").read_bytes()
        evaluator_path = op.REPO_ROOT / "Personalities" / "ZeroToOne.txt"
        evaluator_bytes = evaluator_path.read_bytes()
        factors, rubric_digest = op.parse_rubric(evaluator_path)
        source_hashes = {
            "PERSONALITY_SITUATION.md": op.sha256_bytes(founder_bytes),
            "Personalities/ZeroToOne.txt": op.sha256_bytes(evaluator_bytes),
            "config/opportunity-workflow.json": op.sha256_bytes(config_bytes),
        }
        created_at = op.utc_now()
        manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "created_at": created_at,
            "config": config,
            "source_hashes": source_hashes,
            "rubric": {
                "rubric_id": config["rubric_id"],
                "sha256": rubric_digest,
                "factors": [
                    {"name": name, "weight": op.decimal_json(weight)}
                    for name, weight in factors
                ],
            },
        }
        state = {
            "schema_version": 1,
            "run_id": run_id,
            "stage": "initialized",
            "run_status": "active",
            "updated_at": created_at,
            "jobs": {stage: {} for stage in op.STAGES},
        }
        for relative, data in (
            ("inputs/founder.md", founder_bytes),
            ("inputs/evaluator.txt", evaluator_bytes),
            ("inputs/config.json", config_bytes),
            ("manifest.json", op.canonical_json_bytes(manifest)),
            ("state.json", op.canonical_json_bytes(state)),
        ):
            op.write_immutable(run_dir / relative, data, root=run_dir)
        op.append_event(
            run_dir,
            state,
            "run_created",
            details={"source_hashes": source_hashes},
        )
        self.assertEqual(op.status_run(run_dir, False)["stage"], "initialized")
        self.assertEqual(op.check_run(run_dir)["valid"], True)
        raw = self.root / "legacy-import.json"
        raw.write_text("{}", encoding="utf-8")
        mutation_calls = (
            lambda: op.resume_run(run_dir),
            lambda: op.start_job(run_dir, "legacy", None),
            lambda: op.fail_job(run_dir, "legacy", "failure"),
            lambda: op.complete_job(run_dir, "legacy", raw, "generic"),
            lambda: op.dedup_run(run_dir),
            lambda: op.advance_run(run_dir),
            lambda: op.export_external(run_dir, "alpha"),
            lambda: op.import_external(run_dir, "alpha", raw),
            lambda: op.finalize_run(run_dir, "legacy closure"),
            lambda: op.publish_run(
                run_dir, self.root / "legacy-outcomes", self.root / "legacy-knowledge"
            ),
        )
        for mutation in mutation_calls:
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(op.ConflictError, "schema-v1 runs are read-only"):
                    mutation()

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
