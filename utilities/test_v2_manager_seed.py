"""Regression checks for V2 matched seed registration and binding."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from unittest import mock


UTILITIES = Path(__file__).resolve().parent
if str(UTILITIES) not in sys.path:
    sys.path.insert(0, str(UTILITIES))

import v2_candidate_development as development  # noqa: E402
import v2_matched_experiment_manager as manager  # noqa: E402


class ManagerSeedRegistrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.working = self.root / "working_folder"
        self.anchors = self.root / "audit_anchors"
        self.working.mkdir()
        self.anchors.mkdir()

        fixture_dir = self.root / "fixed"
        fixture_dir.mkdir()
        fixed_names = {
            "founder-profile": "founder.md",
            "success-safety-contract": "contract.md",
            "goal": "goal.md",
            "validator": "validator.md",
            "orchestration-prompt": "prompt.md",
            "generator-skill": "generator-skill.md",
            "evaluator-skill": "evaluator-skill.md",
            "pivot-skill": "pivot-skill.md",
        }
        self.fixed_paths = {
            label: fixture_dir / name for label, name in fixed_names.items()
        }
        for label, path in self.fixed_paths.items():
            content = f"fixture: {label}\n"
            if label == "orchestration-prompt":
                content += "## Validation Gates\nfixed gates\n## Workflow\nfixed workflow\n"
            path.write_text(content, encoding="utf-8")
        workflow_auditor = fixture_dir / "audit_funnel.py"
        workflow_protocol = fixture_dir / "blind-search-protocol.md"
        workflow_auditor.write_text("# fixture auditor\n", encoding="utf-8")
        workflow_protocol.write_text("# fixture protocol\n", encoding="utf-8")
        self.workflow_paths = {
            "audit-funnel": workflow_auditor,
            "blind-search-protocol": workflow_protocol,
            "v2-candidate-development": Path(development.__file__).resolve(),
            "v2-matched-experiment-manager": Path(manager.__file__).resolve(),
        }
        self.patches = [
            mock.patch.object(manager, "WORKSPACE", self.root),
            mock.patch.object(manager, "WORKING_FOLDER", self.working),
            mock.patch.object(manager, "ANCHOR_ROOT", self.anchors),
            mock.patch.object(manager, "AUDITOR", workflow_auditor),
            mock.patch.object(manager, "FIXED_PATHS", self.fixed_paths),
            mock.patch.object(manager, "WORKFLOW_PATHS", self.workflow_paths),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temporary.cleanup()

    def _fake_auditor(self, args: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        anchor_path = Path(args[-1])
        anchor_data = manager.json_bytes({"schema": "fixture-protection-anchor"})
        anchor_path.write_bytes(anchor_data)
        digest = hashlib.sha256(anchor_data).hexdigest()
        return subprocess.CompletedProcess(
            args,
            0,
            stdout=f"PROTECTION_ANCHOR_SHA256={digest}\n",
            stderr="",
        )

    def _register(self, stamp: str, seed: str) -> tuple[Path, dict[str, object], str]:
        output = io.StringIO()
        with (
            mock.patch.object(manager.subprocess, "run", side_effect=self._fake_auditor),
            contextlib.redirect_stdout(output),
        ):
            manager.register(stamp, seed)
        run_dir = self.working / f"zero_to_one_candidates_{stamp}"
        receipt = json.loads(
            (self.anchors / f"v2_matched_{stamp}" / "registration_receipt.json").read_text(
                encoding="utf-8"
            )
        )
        return run_dir, receipt, output.getvalue()

    @staticmethod
    def _run_record(run_dir: Path) -> dict[str, object]:
        return manager.read_jsonl(
            run_dir / "00a_context_and_resource_manifest.jsonl"
        )[0]

    @staticmethod
    def _write_records(run_dir: Path, records: list[dict[str, object]]) -> None:
        (run_dir / "00a_context_and_resource_manifest.jsonl").write_bytes(
            manager.jsonl_bytes(records)
        )

    def test_explicit_fresh_seed_registration_succeeds_and_binds_identity(self) -> None:
        seed = "v2-matched-20990101_000001-a1b2c3d4e5f6"
        run_dir, receipt, output = self._register("20990101_000001", seed)
        run_record = self._run_record(run_dir)
        reservation = Path(str(receipt["seed_reservation_path"]))
        reservation_record = json.loads(reservation.read_text(encoding="utf-8"))
        run_registration = Path(str(receipt["run_registration_path"]))
        run_registration_record = json.loads(
            run_registration.read_text(encoding="utf-8")
        )

        self.assertIn(f"RESERVED_SEED={seed}", output)
        self.assertEqual(receipt["schema"], manager.REGISTRATION_RECEIPT_SCHEMA)
        self.assertEqual(receipt["run_id"], run_dir.name)
        self.assertEqual(receipt["run_dir"], str(run_dir.resolve()))
        self.assertEqual(receipt["child_dir"], str((run_dir / manager.CHILD_RELATIVE_PATH).resolve()))
        self.assertEqual(receipt["seed"], seed)
        self.assertEqual(receipt["candidate_order_seed"], seed)
        self.assertEqual(run_record["seed"], seed)
        self.assertEqual(run_record["candidate_order_seed"], seed)
        self.assertEqual(reservation_record["seed"], seed)
        self.assertEqual(reservation_record["candidate_order_seed"], seed)
        self.assertEqual(reservation_record["registered_at"], receipt["registered_at"])
        self.assertEqual(stat.S_IMODE(reservation.stat().st_mode), 0o400)
        self.assertEqual(run_registration_record["seed"], seed)
        self.assertEqual(run_registration_record["candidate_order_seed"], seed)
        self.assertEqual(
            run_registration_record["seed_reservation_sha256"],
            receipt["seed_reservation_sha256"],
        )
        self.assertEqual(stat.S_IMODE(run_registration.stat().st_mode), 0o400)
        self.assertEqual(manager.authenticated_run_seed(run_dir), seed)
        self.assertFalse((run_dir / manager.CHILD_RELATIVE_PATH).exists())

    def test_omitted_seed_fails_without_creating_registration_artifacts(self) -> None:
        stderr = io.StringIO()
        with (
            mock.patch.object(
                sys,
                "argv",
                ["manager", "register", "--stamp", "20990101_000002"],
            ),
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit) as raised,
        ):
            manager.main()
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--seed", stderr.getvalue())
        self.assertEqual(list(self.working.iterdir()), [])
        self.assertEqual(list(self.anchors.iterdir()), [])

    def test_malformed_and_overlong_seeds_fail_before_reservation(self) -> None:
        malformed = [
            "too-short",
            "v2-matched-UPPERCASE-1234",
            "v2-matched-path/escape-1234",
            "v2-matched-trailing-hyphen-",
            "v2-matched-space value-1234",
            "v2-matched-" + "a" * (manager.SEED_MAX_LENGTH + 1),
        ]
        for index, seed in enumerate(malformed, 1):
            with self.subTest(seed=seed), self.assertRaisesRegex(RuntimeError, "seed"):
                manager.register(f"20990102_{index:06d}", seed)
        self.assertEqual(list(self.working.iterdir()), [])
        self.assertEqual(list(self.anchors.iterdir()), [])

    def test_seed_in_historical_registration_receipt_is_rejected(self) -> None:
        seed = "v2-matched-20990103_000001-usedreceipt"
        historical_anchor = self.anchors / "v2_matched_20980101_000001"
        historical_anchor.mkdir()
        (historical_anchor / "registration_receipt.json").write_bytes(
            manager.json_bytes(
                {
                    "schema": "zt1-v2-matched-registration-receipt-v1",
                    "seed": seed,
                }
            )
        )
        with self.assertRaisesRegex(RuntimeError, "already reserved or registered"):
            manager.register("20990103_000002", seed)
        self.assertFalse((self.working / "zero_to_one_candidates_20990103_000002").exists())

    def test_seed_in_canonical_run_record_without_receipt_is_rejected(self) -> None:
        seed = "v2-matched-20990103_000003-usedrunrecord"
        historical_run = self.working / "zero_to_one_candidates_20980101_000002"
        historical_run.mkdir()
        (historical_run / "00a_context_and_resource_manifest.jsonl").write_bytes(
            manager.jsonl_bytes(
                [
                    {
                        "record_type": "run",
                        "schema": "zt1-generation-run-v2",
                        "seed": seed,
                        "candidate_order_seed": seed,
                    }
                ]
            )
        )
        with self.assertRaisesRegex(RuntimeError, "already reserved or registered"):
            manager.register("20990103_000004", seed)
        self.assertFalse((self.working / "zero_to_one_candidates_20990103_000004").exists())

    def test_simultaneous_duplicate_reservation_cannot_both_succeed(self) -> None:
        seed = "v2-matched-20990104_000001-raceproof"
        barrier = threading.Barrier(2)

        def attempt(stamp: str) -> str:
            run_dir = self.working / f"zero_to_one_candidates_{stamp}"
            barrier.wait()
            try:
                manager.reserve_seed(
                    stamp=stamp,
                    seed=seed,
                    run_dir=run_dir,
                    child_dir=run_dir / manager.CHILD_RELATIVE_PATH,
                    anchor_dir=self.anchors / f"v2_matched_{stamp}",
                    registered_at=manager.iso(manager.now()),
                )
            except RuntimeError:
                return "rejected"
            return "reserved"

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(attempt, ("20990104_000001", "20990104_000002"))
            )
        self.assertEqual(sorted(results), ["rejected", "reserved"])
        self.assertEqual(len(list((self.anchors / manager.SEED_RESERVATION_DIRNAME).glob("*.json"))), 1)

    def test_same_seed_under_different_timestamp_still_fails(self) -> None:
        seed = "v2-matched-20990105_000001-crossstamp"
        self._register("20990105_000001", seed)
        with self.assertRaisesRegex(RuntimeError, "already reserved or registered"):
            manager.register("20990105_000002", seed)
        self.assertFalse((self.working / "zero_to_one_candidates_20990105_000002").exists())

    def test_receipt_run_and_candidate_order_disagreement_fail_closed(self) -> None:
        cases = ("receipt_candidate", "run_seed", "run_candidate")
        for index, case in enumerate(cases, 1):
            with self.subTest(case=case):
                stamp = f"20990106_{index:06d}"
                seed = f"v2-matched-{stamp}-binding{index}"
                run_dir, receipt, _output = self._register(stamp, seed)
                if case == "receipt_candidate":
                    receipt["candidate_order_seed"] = f"v2-matched-{stamp}-substitute"
                    (self.anchors / f"v2_matched_{stamp}" / "registration_receipt.json").write_bytes(
                        manager.json_bytes(receipt)
                    )
                else:
                    records = manager.read_jsonl(
                        run_dir / "00a_context_and_resource_manifest.jsonl"
                    )
                    field = "seed" if case == "run_seed" else "candidate_order_seed"
                    records[0][field] = f"v2-matched-{stamp}-substitute"
                    self._write_records(run_dir, records)
                with self.assertRaisesRegex(RuntimeError, "disagree"):
                    manager.authenticated_run_seed(run_dir)

    def test_post_registration_seed_substitution_is_not_accepted_or_written(self) -> None:
        stamp = "20990107_000001"
        seed = "v2-matched-20990107_000001-original"
        run_dir, _receipt, _output = self._register(stamp, seed)
        stderr = io.StringIO()
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "manager",
                    "prepare-baseline-generation",
                    str(run_dir),
                    "--seed",
                    "v2-matched-20990107_000001-substitute",
                ],
            ),
            contextlib.redirect_stderr(stderr),
            self.assertRaises(SystemExit) as raised,
        ):
            manager.main()
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(list((run_dir / "context").iterdir()), [])

        records = manager.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
        records[0]["candidate_order_seed"] = "v2-matched-20990107_000001-substitute"
        self._write_records(run_dir, records)
        with self.assertRaisesRegex(RuntimeError, "disagree"):
            manager.prepare_baseline_generation(run_dir)
        self.assertEqual(list((run_dir / "context").iterdir()), [])

    def test_coordinated_seed_substitution_cannot_replace_run_registration(self) -> None:
        stamp = "20990107_000002"
        original = "v2-matched-20990107_000002-original"
        substitute = "v2-matched-20990107_000002-substitute"
        run_dir, receipt, _output = self._register(stamp, original)
        alternate_path, alternate_digest = manager.reserve_seed(
            stamp=stamp,
            seed=substitute,
            run_dir=run_dir,
            child_dir=run_dir / manager.CHILD_RELATIVE_PATH,
            anchor_dir=self.anchors / f"v2_matched_{stamp}",
            registered_at=str(receipt["registered_at"]),
        )
        receipt["seed"] = substitute
        receipt["candidate_order_seed"] = substitute
        receipt["seed_reservation_path"] = str(alternate_path.resolve())
        receipt["seed_reservation_sha256"] = alternate_digest
        receipt_path = self.anchors / f"v2_matched_{stamp}" / "registration_receipt.json"
        receipt_path.write_bytes(manager.json_bytes(receipt))
        records = manager.read_jsonl(
            run_dir / "00a_context_and_resource_manifest.jsonl"
        )
        records[0]["seed"] = substitute
        records[0]["candidate_order_seed"] = substitute
        self._write_records(run_dir, records)
        human_path = run_dir / "00_run_manifest.md"
        human_path.write_text(
            human_path.read_text(encoding="utf-8").replace(original, substitute),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(RuntimeError, "run registration.*disagree"):
            manager.authenticated_run_seed(run_dir)

    def test_symlinked_output_directory_and_run_prefix_fail_before_write(self) -> None:
        stamp = "20990107_000003"
        seed = "v2-matched-20990107_000003-pathsafe"
        run_dir, _receipt, _output = self._register(stamp, seed)
        outside = self.root / "outside"
        outside.mkdir()
        context_dir = run_dir / "context"
        context_dir.rmdir()
        context_dir.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "context.*unsafe"):
            manager.prepare_baseline_generation(run_dir)
        self.assertEqual(list(outside.iterdir()), [])

        working_alias = self.root / "working-alias"
        working_alias.symlink_to(self.working, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "noncanonical or symlinked prefix"):
            manager.authenticated_run_seed(working_alias / run_dir.name)

    def test_extra_conflicting_run_registration_pin_fails_closed(self) -> None:
        stamp = "20990107_000004"
        seed = "v2-matched-20990107_000004-runpin"
        run_dir, receipt, _output = self._register(stamp, seed)
        canonical_pin = Path(str(receipt["run_registration_path"]))
        conflicting = json.loads(canonical_pin.read_text(encoding="utf-8"))
        conflicting["seed"] = "v2-matched-20990107_000004-conflict"
        conflicting["candidate_order_seed"] = conflicting["seed"]
        extra_pin = canonical_pin.with_name("f" * 64 + ".json")
        manager.write_exclusive(extra_pin, manager.json_bytes(conflicting))
        with self.assertRaisesRegex(
            RuntimeError,
            "exactly one canonical run registration|filename does not match",
        ):
            manager.authenticated_run_seed(run_dir)

    def test_same_seed_and_inputs_produce_identical_ordering(self) -> None:
        seed = "v2-matched-20990108_000001-repeatable"
        values = [f"value-{index:02d}" for index in range(30)]
        self.assertEqual(
            manager.seeded_order(seed, "test-order", values),
            manager.seeded_order(seed, "test-order", values),
        )

    def test_different_seeds_change_a_seeded_ordering(self) -> None:
        values = [f"value-{index:02d}" for index in range(30)]
        first = manager.seeded_order(
            "v2-matched-20990109_000001-firstseed", "test-order", values
        )
        second = manager.seeded_order(
            "v2-matched-20990109_000001-secondseed", "test-order", values
        )
        self.assertNotEqual(first, second)

    def test_generated_packets_and_selection_records_use_registered_seed(self) -> None:
        stamp = "20990110_000001"
        seed = "v2-matched-20990110_000001-packetbinding"
        run_dir, receipt, _output = self._register(stamp, seed)
        manager.prepare_baseline_generation(run_dir)

        prior_history = (
            self.working
            / "zero_to_one_candidates_20260822_110713"
            / "01b_history_fingerprints.md"
        )
        prior_history.parent.mkdir()
        prior_history.write_text(
            "\n".join(
                f"- `HIST-{index:03d}` — neutral fingerprint {index}"
                for index in range(1, 29)
            )
            + "\n",
            encoding="utf-8",
        )
        manager.prepare_baseline_history(run_dir)

        raw_pool = "\n\n".join(
            f"### RAW-{index:03d} — neutral idea {index}\n\n- Field: value"
            for index in range(1, 49)
        )
        (run_dir / "02a_raw_pool.md").write_text(raw_pool + "\n", encoding="utf-8")
        (run_dir / "01b_history_fingerprints.md").write_text(
            "# Neutral Historical Fingerprints\n", encoding="utf-8"
        )
        run_record = self._run_record(run_dir)
        states = ["registered", "raw_frozen", "history_frozen"]
        self._write_records(
            run_dir,
            [run_record]
            + [{"record_type": "checkpoint", "state": state} for state in states],
        )
        manager.prepare_baseline_cartography(run_dir)

        directions = [{"direction_id": "DIR-001", "raw_ids": ["RAW-001"]}]
        mappings = [{"raw_id": "RAW-001", "direction_id": "DIR-001"}]
        (run_dir / "agent_returns" / "baseline-cartography-01.json").write_text(
            "{}\n", encoding="utf-8"
        )
        self._write_records(
            run_dir,
            [run_record]
            + [
                {"record_type": "checkpoint", "state": state}
                for state in [*states, "mapped"]
            ],
        )
        with mock.patch.object(
            manager,
            "validate_baseline_cartography",
            return_value=(directions, mappings),
        ):
            manager.prepare_baseline_cluster_audit(run_dir)

        (run_dir / "agent_returns" / "baseline-cluster-audit-01.json").write_text(
            "{}\n", encoding="utf-8"
        )
        (run_dir / "03_research_and_sources.md").write_text(
            "# Discovery Evidence\n", encoding="utf-8"
        )
        self._write_records(
            run_dir,
            [run_record]
            + [
                {"record_type": "checkpoint", "state": state}
                for state in [*states, "mapped", "cluster_audited"]
            ],
        )
        with (
            mock.patch.object(
                manager,
                "validate_baseline_cartography",
                return_value=(directions, mappings),
            ),
            mock.patch.object(
                manager, "validate_baseline_cluster_audit", return_value=mappings
            ),
        ):
            manager.prepare_baseline_level1(run_dir)

        (run_dir / "02b_raw_to_direction_ledger.jsonl").write_bytes(
            manager.jsonl_bytes([])
        )
        selected_ids = [f"DIR-{index:03d}" for index in range(1, 13)]
        development._prepare(
            manager,
            run_dir,
            stage="level2",
            selected_ids=selected_ids,
            selected_at=manager.iso(manager.now()),
            inputs={concept_id: {"concept_id": concept_id} for concept_id in selected_ids},
        )

        packets = sorted((run_dir / "context").glob("*.md"))
        self.assertEqual(len(packets), 21)
        for packet in packets:
            packet_text = packet.read_text(encoding="utf-8")
            self.assertIn(f"- Seed: `{seed}`", packet_text)
        for precommit in (run_dir / "allocation_precommits").glob("*.json"):
            payload = json.loads(precommit.read_text(encoding="utf-8"))
            self.assertEqual(payload["seed"], seed)
            packet_path = run_dir / payload["packet_path"]
            output_path = run_dir / payload["output_path"]
            packet_text = packet_path.read_text(encoding="utf-8")
            if not output_path.exists():
                manager.assert_bounded_return_packet(packet_path, output_path, run_dir)
            self.assertEqual(
                packet_text.count(f"*** Add File: {output_path}"), 1
            )
            self.assertEqual(
                packet_text.count(f"- Required return path: `{output_path}`"), 1
            )
            self.assertEqual(
                packet_text.count(manager.CANONICAL_BOUNDED_RETURN_WRAPPER), 1
            )
            self.assertIsNone(
                manager._OUTPUT_PATH_PLACEHOLDER_RE.search(packet_text)
            )
        self.assertEqual(receipt["seed"], seed)
        self.assertEqual(receipt["candidate_order_seed"], seed)
        self.assertEqual(
            json.loads((run_dir / "baseline_generation_launch.json").read_text(encoding="utf-8"))["seed"],
            seed,
        )
        self.assertEqual(
            json.loads((run_dir / "baseline_level2_launch.json").read_text(encoding="utf-8"))["seed"],
            seed,
        )

        cards = [
            {
                "concept_id": f"DIR-{index:03d}",
                "problem_payer_evidence": "evidence",
                "proposed_transaction_paid_event": "transaction",
                "current_workaround_and_persistence": "workaround",
                "initial_acquisition_route": "route",
                "possible_compounding_mechanism": "asset",
                "decisive_assumptions_and_contradictions": ["unknown"],
                "cheapest_falsification": "test",
                "founder_constraint_tension": "tension",
                "sources": ["source"],
                "explicit_unknowns": ["unknown"],
            }
            for index in range(1, 17)
        ]
        mocked_agent = {
            "record_type": "agent",
            "agent_id": "baseline-level1-01",
            "ended_at": manager.iso(manager.now() - timedelta(seconds=1)),
            "resources": {
                "uncached_input_tokens": 0,
                "output_tokens": 0,
            },
        }
        (run_dir / "agent_returns" / "baseline-level1-01.json").write_text(
            "{}\n", encoding="utf-8"
        )
        with (
            mock.patch.object(
                manager,
                "integrate_zero_query_agent",
                return_value=(mocked_agent, {"record_type": "allocation"}, {}),
            ),
            mock.patch.object(manager, "validate_baseline_level1", return_value=cards),
        ):
            manager.integrate_baseline_level1_and_seal(
                run_dir, [f"DIR-{index:03d}" for index in range(1, 13)]
            )
        self.assertEqual(
            json.loads((run_dir / "02c_baseline_level2_cohort.json").read_text(encoding="utf-8"))["seed"],
            seed,
        )

        records = manager.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
        records = [records[0]] + [
            {"record_type": "checkpoint", "state": state}
            for state in [
                "registered",
                "raw_frozen",
                "history_frozen",
                "mapped",
                "cluster_audited",
                "level2_cohort_sealed",
                "level2_complete",
            ]
        ]
        (run_dir / "02b_raw_to_direction_ledger.jsonl").write_bytes(
            manager.jsonl_bytes(
                [
                    {
                        "record_type": "level2",
                        "concept_id": f"DIR-{index:03d}",
                        "development_status": "complete",
                    }
                    for index in range(1, 13)
                ]
            )
        )
        self._write_records(run_dir, records)
        manager.seal_baseline_fact_closure(
            run_dir, [f"DIR-{index:03d}" for index in range(1, 7)]
        )
        self.assertEqual(
            json.loads((run_dir / "02d_fact_closure_candidates.json").read_text(encoding="utf-8"))["seed"],
            seed,
        )

    def test_manager_stops_before_launch_when_rendered_packet_lacks_path_binding(self) -> None:
        run_dir, _receipt, _output = self._register(
            "20990111_000001",
            "v2-matched-20990111_000001-packetguard",
        )
        generic_instruction = (
            "Use this wrapper exactly:\n\n```javascript\n"
            + manager.CANONICAL_BOUNDED_RETURN_WRAPPER
            + "\n```"
        )
        with (
            mock.patch.object(
                manager,
                "bounded_return_instruction",
                return_value=generic_instruction,
            ),
            self.assertRaisesRegex(RuntimeError, "Add File|path-bound instruction"),
        ):
            manager.prepare_baseline_generation(run_dir)
        self.assertFalse((run_dir / "baseline_generation_launch.json").exists())

    def test_no_hardcoded_operational_seed_or_implicit_fallback_remains(self) -> None:
        manager_source = Path(manager.__file__).read_text(encoding="utf-8")
        runtime_source = Path(development.__file__).read_text(encoding="utf-8")
        combined = manager_source + runtime_source
        self.assertNotIn("v2-matched-20260823-314159", combined)
        self.assertNotRegex(manager_source, r"(?m)^SEED\s*=")
        self.assertNotIn("api.SEED", runtime_source)
        self.assertNotIn("os.environ", manager_source)
        self.assertNotIn("os.getenv", manager_source)
        self.assertIn('register_parser.add_argument("--seed", required=True)', manager_source)

    def test_registration_does_not_change_fixed_or_validation_boundaries(self) -> None:
        before = {path: manager.sha256(path) for path in self.fixed_paths.values()}
        prompt = self.fixed_paths["orchestration-prompt"]
        block_before = manager.sha256_bytes(
            manager.marker_block(prompt, "## Validation Gates", "## Workflow")
        )
        self._register(
            "20990111_000001", "v2-matched-20990111_000001-protected"
        )
        after = {path: manager.sha256(path) for path in self.fixed_paths.values()}
        block_after = manager.sha256_bytes(
            manager.marker_block(prompt, "## Validation Gates", "## Workflow")
        )
        self.assertEqual(after, before)
        self.assertEqual(block_after, block_before)
        self.assertEqual(len(manager.BASELINE_ROLES), 5)
        self.assertEqual(len(manager.BASELINE_PACKET_PATHS), 27)
        self.assertEqual(len(manager.SHADOW_PACKET_PATHS), 40)
        self.assertEqual(manager.development_contract()["aggregate_opportunity"]["total_queries"], 300)


if __name__ == "__main__":
    unittest.main()
