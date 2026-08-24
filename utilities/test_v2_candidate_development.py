"""Non-experimental unit checks for the V2 candidate-development runtime."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock


UTILITIES = Path(__file__).resolve().parent
if str(UTILITIES) not in sys.path:
    sys.path.insert(0, str(UTILITIES))

import v2_candidate_development as development  # noqa: E402
import v2_matched_experiment_manager as manager  # noqa: E402


class CandidateDevelopmentRuntimeTests(unittest.TestCase):
    TEST_SEED = "v2-matched-runtime-tests-0001"

    def setUp(self) -> None:
        self.seed_authentication = mock.patch.object(
            manager, "authenticated_run_seed", return_value=self.TEST_SEED
        )
        self.seed_authentication.start()

    def tearDown(self) -> None:
        self.seed_authentication.stop()

    def _prepared_run(
        self,
        root: Path,
        state: str,
        *,
        arm: str = "matched_baseline",
    ) -> tuple[Path, str]:
        run_dir = (root / "synthetic_runtime").resolve()
        for relative in ("context", "agent_returns", "allocation_precommits"):
            (run_dir / relative).mkdir(parents=True, exist_ok=True)
        started = manager.now() - timedelta(minutes=1)
        deadline = started + timedelta(hours=3)
        selected_at = manager.iso(started + timedelta(seconds=1))
        records = [
            {
                "record_type": "run",
                "run_id": run_dir.name,
                "started_at": manager.iso(started),
                "deadline_at": manager.iso(deadline),
                "ended_at": None,
                "lifecycle_state": state,
                "arm": arm,
                "scope_id": "baseline-w01" if arm == "matched_baseline" else "shadow-w01",
            },
            {
                "record_type": "checkpoint",
                "state": state,
                "occurred_at": selected_at,
            },
        ]
        (run_dir / "00a_context_and_resource_manifest.jsonl").write_bytes(
            manager.jsonl_bytes(records)
        )
        (run_dir / "02b_raw_to_direction_ledger.jsonl").write_bytes(
            manager.jsonl_bytes([])
        )
        return run_dir, selected_at

    def test_exact_contract_and_machine_time_types(self) -> None:
        contract = manager.development_contract()
        self.assertEqual(contract["level2_sections"], contract["frozen_sections"])
        self.assertEqual(len(contract["level2_sections"]), 9)
        self.assertEqual(
            contract["candidate_budgets"],
            {
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
            },
        )
        self.assertEqual(
            contract["dossier_prose_word_ranges"],
            {
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
            },
        )
        start = datetime.fromisoformat("2026-08-23T10:00:00.000001+02:00")
        end = datetime.fromisoformat("2026-08-23T10:00:01.234568+02:00")
        elapsed = manager.elapsed_microseconds(start, end)
        self.assertIs(type(elapsed), int)
        self.assertEqual(elapsed, 1_234_567)
        dst_start = datetime.fromisoformat("2026-10-25T02:30:00+02:00")
        dst_end = datetime.fromisoformat("2026-10-25T02:30:00+01:00")
        self.assertEqual(manager.elapsed_microseconds(dst_start, dst_end), 3_600_000_000)
        folded_end = datetime.fromisoformat("2026-10-25T02:15:00+01:00")
        self.assertEqual(
            manager.elapsed_microseconds(dst_start, folded_end), 2_700_000_000
        )
        self.assertLess(development._utc(dst_start), development._utc(folded_end))
        for stage, hard in contract["candidate_budgets"].items():
            live = contract["candidate_live_stop_thresholds"][stage]
            self.assertGreaterEqual(
                hard["uncached_input_tokens"] - live["uncached_input_tokens"],
                contract["metering_monitor"]["minimum_uncached_reserve_tokens"],
            )
            self.assertGreaterEqual(
                hard["output_tokens"] - live["output_tokens"],
                contract["metering_monitor"]["minimum_output_reserve_tokens"],
            )

    def test_level2_and_closure_launches_are_singleton_batches(self) -> None:
        cases = (("level2", 12, 4), ("fact_closure", 6, 2))
        for arm in ("matched_baseline", "shadow"):
            for stage, count, batch_count in cases:
                with self.subTest(arm=arm, stage=stage), tempfile.TemporaryDirectory() as temporary:
                    prefix = "baseline" if arm == "matched_baseline" else "shadow"
                    run_dir, selected_at = self._prepared_run(
                        Path(temporary),
                        "level2_cohort_sealed"
                        if stage == "level2"
                        else "fact_closure_cohort_sealed",
                        arm=arm,
                    )
                    ids = [f"DIR-{index:03d}" for index in range(1, count + 1)]
                    development._prepare(
                        manager,
                        run_dir,
                        stage=stage,
                        selected_ids=ids,
                        selected_at=selected_at,
                        inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
                        selection_categories=(
                            {
                                candidate_id: (
                                    "main_provisional"
                                    if index <= 6
                                    else "selector_or_challenger"
                                    if index <= 9
                                    else ("rejected", "near_cutoff", "singleton")[index - 10]
                                )
                                for index, candidate_id in enumerate(ids, 1)
                            }
                            if arm == "shadow" and stage == "level2"
                            else None
                        ),
                    )

                    launch = json.loads(
                        (run_dir / f"{prefix}_{stage}_launch.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertEqual(launch["arm"], arm)
                    self.assertEqual(launch["seed"], self.TEST_SEED)
                    self.assertEqual(len(launch["batches"]), batch_count)
                    self.assertTrue(all(1 <= len(batch) <= 3 for batch in launch["batches"]))
                    agents = [item for batch in launch["batches"] for item in batch]
                    self.assertEqual(len(agents), count)
                    self.assertEqual(len({item["agent_id"] for item in agents}), count)
                    self.assertEqual(len({item["entity_id"] for item in agents}), count)
                    self.assertEqual(len({item["task_name"] for item in agents}), count)
                    for item in agents:
                        precommit = json.loads(
                            Path(item["allocation_precommit_path"]).read_text(
                                encoding="utf-8"
                            )
                        )
                        self.assertEqual(precommit["arm"], arm)
                        self.assertEqual(precommit["seed"], self.TEST_SEED)
                        self.assertEqual(precommit["assigned_ids"], [item["entity_id"]])
                        self.assertEqual(precommit["output_ids"], [item["entity_id"]])
                        self.assertEqual(precommit["entity_id"], item["entity_id"])
                        self.assertEqual(precommit["metering_basis"], "trace_derived_exact")
                        self.assertEqual(precommit["trace_task_name"], item["task_name"])
                        self.assertIn("_synthetic_runtime_", item["task_name"])
                        packet_path = Path(item["packet_path"])
                        output_path = Path(item["output_path"])
                        packet_text = packet_path.read_text(
                            encoding="utf-8"
                        )
                        self.assertIn(
                            f"- Seed: `{self.TEST_SEED}`",
                            packet_text,
                        )
                        manager.assert_bounded_return_packet(
                            packet_path, output_path, run_dir
                        )
                        self.assertEqual(
                            packet_text.count(f"*** Add File: {output_path}"), 1
                        )
                        self.assertEqual(
                            packet_text.count(
                                f"- Required return path: `{output_path}`"
                            ),
                            1,
                        )
                        self.assertEqual(
                            packet_text.count(manager.CANONICAL_BOUNDED_RETURN_WRAPPER),
                            1,
                        )
                        self.assertIsNone(
                            manager._OUTPUT_PATH_PLACEHOLDER_RE.search(packet_text)
                        )

    def test_shadow_trace_task_names_include_parent_run_identity(self) -> None:
        first = (
            manager.WORKING_FOLDER
            / "zero_to_one_candidates_20990101_000001"
            / manager.CHILD_RELATIVE_PATH
        )
        second = (
            manager.WORKING_FOLDER
            / "zero_to_one_candidates_20990101_000002"
            / manager.CHILD_RELATIVE_PATH
        )
        first_name = manager.trace_task_name(first, "shadow-level2-01")
        second_name = manager.trace_task_name(second, "shadow-level2-01")
        self.assertNotEqual(first_name, second_name)
        self.assertIn("zero_to_one_candidates_20990101_000001", first_name)
        self.assertIn("shadow_archipelago_lite", first_name)

    def test_failed_level2_admission_does_not_advance_or_materialize_child(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, _selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            launches = []
            for index in range(1, 13):
                agent_id = f"baseline-level2-{index:02d}"
                entity_id = f"DIR-{index:03d}"
                precommit_path = run_dir / "allocation_precommits" / f"L2-{index:02d}.json"
                output_path = run_dir / "agent_returns" / f"{agent_id}.json"
                packet_path = run_dir / "context" / f"{agent_id}.md"
                packet_path.write_text("synthetic packet\n", encoding="utf-8")
                precommit_path.write_text(
                    json.dumps(
                        {
                            "agent_id": agent_id,
                            "entity_id": entity_id,
                            "seed": self.TEST_SEED,
                            "trace_task_name": manager.trace_task_name(run_dir, agent_id),
                        }
                    ),
                    encoding="utf-8",
                )
                output_path.write_text("{}\n", encoding="utf-8")
                launches.append(
                    {
                        "agent_id": agent_id,
                        "entity_id": entity_id,
                        "packet_path": str(packet_path),
                        "output_path": str(output_path),
                        "allocation_precommit_path": str(precommit_path),
                        "task_name": manager.trace_task_name(run_dir, agent_id),
                    }
                )
            launch = {
                "schema": "zt1-isolated-development-launch-v2",
                "stage": "level2",
                "seed": self.TEST_SEED,
                "max_concurrency": 3,
                "batches": [launches[index : index + 3] for index in range(0, 12, 3)],
            }
            (run_dir / "baseline_level2_launch.json").write_text(
                json.dumps(launch), encoding="utf-8"
            )
            before = {
                path.relative_to(run_dir).as_posix(): path.read_bytes()
                for path in run_dir.rglob("*")
                if path.is_file()
            }

            with mock.patch.object(manager, "parse_trace", return_value={}):
                with self.assertRaisesRegex(RuntimeError, "invalid closed schema"):
                    development.integrate_baseline_level2(manager, run_dir)

            after = {
                path.relative_to(run_dir).as_posix(): path.read_bytes()
                for path in run_dir.rglob("*")
                if path.is_file()
            }
            permitted_changes = {
                "00a_context_and_resource_manifest.jsonl",
                "10_level2_admission_failure.json",
            }
            self.assertEqual(
                {key: value for key, value in after.items() if key not in permitted_changes},
                {key: value for key, value in before.items() if key not in permitted_changes},
            )
            records = manager.read_jsonl(
                run_dir / "00a_context_and_resource_manifest.jsonl"
            )
            self.assertEqual(records[0]["lifecycle_state"], "level2_cohort_sealed")
            self.assertIsNotNone(records[0]["ended_at"])
            self.assertEqual(records[-1]["state"], "level2_cohort_sealed")
            receipt = json.loads(
                (run_dir / "10_level2_admission_failure.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                receipt["primary_cause"]["code"],
                "DEVELOPMENT_RETURN_ADMISSION_FAILED",
            )
            self.assertFalse(receipt["telemetry_reconstruction_performed"])
            self.assertEqual(receipt["future_lifecycle_artifacts"], [])
            self.assertEqual(receipt["materialized_stage_artifacts"], [])
            self.assertEqual(records[0]["failure_receipt_path"], "10_level2_admission_failure.json")
            self.assertEqual(
                records[0]["failure_receipt_sha256"],
                manager.sha256(run_dir / "10_level2_admission_failure.json"),
            )
            self.assertFalse((run_dir / manager.CHILD_RELATIVE_PATH).exists())
            self.assertFalse((run_dir / "baseline_level2").exists())
            self.assertFalse((run_dir / "runtime_traces").exists())
            with mock.patch.object(manager, "parse_trace", return_value={}):
                with self.assertRaisesRegex(RuntimeError, "immutable"):
                    development.integrate_baseline_level2(manager, run_dir)

    def test_live_meter_snapshot_requests_interrupt_at_lower_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 13)]
            development._prepare(
                manager,
                run_dir,
                stage="level2",
                selected_ids=ids,
                selected_at=selected_at,
                inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
            )
            below = {
                "status": "running",
                "trace_path": "/synthetic/trace",
                "measured_at": manager.iso(manager.now()),
                "uncached_input_tokens": 91_999,
                "output_tokens": 10_999,
                "elapsed_microseconds": 13 * 60_000_000,
            }
            with mock.patch.object(
                manager,
                "partial_trace_usages",
                side_effect=lambda task_names: {name: dict(below) for name in task_names},
            ):
                safe = development.meter_batch_snapshot(
                    manager, run_dir, stage="level2", batch_index=1
                )
            self.assertEqual(safe["interrupt_task_names"], [])

            boundary = dict(below)
            boundary["uncached_input_tokens"] = 92_000
            with mock.patch.object(
                manager,
                "partial_trace_usages",
                side_effect=lambda task_names: {name: dict(boundary) for name in task_names},
            ):
                stop = development.meter_batch_snapshot(
                    manager, run_dir, stage="level2", batch_index=1
                )
            self.assertEqual(len(stop["interrupt_task_names"]), 3)
            self.assertTrue(stop["stage_admission_must_fail"])
            self.assertTrue(
                (run_dir / "live_metering/baseline_level2_batch_01.jsonl").is_file()
            )

    def test_live_trace_startup_race_is_not_started_until_task_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            trace_path = Path(temporary) / "partial.jsonl"
            session = {"type": "session_meta", "payload": {"source": {}}}
            trace_path.write_text(
                json.dumps(session) + "\n" + '{"type":', encoding="utf-8"
            )
            usage = manager._partial_trace_usage_at_path("candidate-task", trace_path)
            self.assertEqual(usage["status"], "not_started")
            self.assertEqual(usage["trace_path"], str(trace_path))
            self.assertEqual(usage["uncached_input_tokens"], 0)
            self.assertEqual(usage["output_tokens"], 0)
            self.assertEqual(usage["elapsed_microseconds"], 0)

            token_without_start = {
                "type": "event_msg",
                "payload": {"type": "token_count"},
            }
            trace_path.write_text(
                "\n".join(json.dumps(item) for item in (session, token_without_start))
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "before task start"):
                manager._partial_trace_usage_at_path("candidate-task", trace_path)

    def test_blocking_controller_reuses_paths_and_interrupts_at_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 13)]
            development._prepare(
                manager,
                run_dir,
                stage="level2",
                selected_ids=ids,
                selected_at=selected_at,
                inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
            )
            launch = json.loads(
                (run_dir / "baseline_level2_launch.json").read_text(encoding="utf-8")
            )
            task_names = [item["task_name"] for item in launch["batches"][0]]
            paths = {
                task_name: Path(temporary) / f"trace-{index}.jsonl"
                for index, task_name in enumerate(task_names, 1)
            }
            calls = 0

            def usages(trace_paths: dict[str, Path | None]) -> dict[str, dict[str, object]]:
                nonlocal calls
                calls += 1
                boundary = calls > 1
                return {
                    task_name: {
                        "status": "running" if boundary else "not_started",
                        "trace_path": str(trace_paths[task_name]),
                        "measured_at": manager.iso(manager.now()),
                        "uncached_input_tokens": (
                            92_000
                            if boundary and task_name == task_names[0]
                            else 0
                        ),
                        "output_tokens": 0,
                        "elapsed_microseconds": 0,
                    }
                    for task_name in task_names
                }

            with (
                mock.patch.object(manager, "find_trace_paths", return_value=paths) as discover,
                mock.patch.object(
                    manager, "partial_trace_usages_from_paths", side_effect=usages
                ) as direct_meter,
                mock.patch.object(development.time, "monotonic", return_value=0),
                mock.patch.object(development.time, "sleep") as sleep,
            ):
                result = development.monitor_batch(
                    manager, run_dir, stage="level2", batch_index=1
                )

            self.assertEqual(result["outcome"], "interrupt_required")
            self.assertEqual(result["interrupt_task_names"], [task_names[0]])
            self.assertEqual(result["abort_batch_task_names"], sorted(task_names))
            discover.assert_called_once()
            self.assertEqual(direct_meter.call_count, 2)
            sleep.assert_called_once_with(1.0)

    def test_batch_controller_rechecks_remaining_deadline_reservation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 13)]
            development._prepare(
                manager,
                run_dir,
                stage="level2",
                selected_ids=ids,
                selected_at=selected_at,
                inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
            )
            manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
            records = manager.read_jsonl(manifest_path)
            records[0]["deadline_at"] = manager.iso(manager.now() + timedelta(minutes=83))
            manifest_path.write_bytes(manager.jsonl_bytes(records))

            with mock.patch.object(manager, "find_trace_paths") as discover:
                with self.assertRaisesRegex(RuntimeError, "remaining isolated development"):
                    development.monitor_batch(
                        manager, run_dir, stage="level2", batch_index=1
                    )
            discover.assert_not_called()

    def test_batch_controller_rejects_hash_consistent_relative_header_before_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 13)]
            development._prepare(
                manager,
                run_dir,
                stage="level2",
                selected_ids=ids,
                selected_at=selected_at,
                inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
            )
            launch_path = run_dir / "baseline_level2_launch.json"
            launch = json.loads(launch_path.read_text(encoding="utf-8"))
            launch_item = launch["batches"][0][0]
            packet_path = Path(launch_item["packet_path"])
            output_path = Path(launch_item["output_path"])
            packet_text = packet_path.read_text(encoding="utf-8").replace(
                f"*** Add File: {output_path}",
                "*** Add File: agent_returns/baseline-level2-01.json",
            )
            packet_path.write_text(packet_text, encoding="utf-8")
            packet_digest = manager.sha256(packet_path)

            precommit_path = Path(launch_item["allocation_precommit_path"])
            precommit = json.loads(precommit_path.read_text(encoding="utf-8"))
            precommit["packet_sha256"] = packet_digest
            precommit_path.write_bytes(manager.json_bytes(precommit))
            launch_item["packet_sha256"] = packet_digest
            launch_path.write_bytes(manager.json_bytes(launch))

            with mock.patch.object(manager, "find_trace_paths") as discover:
                with self.assertRaisesRegex(RuntimeError, "Add File|instruction"):
                    development.monitor_batch(
                        manager, run_dir, stage="level2", batch_index=1
                    )
            discover.assert_not_called()

    def test_batch_controller_rejects_coordinated_run_owned_path_substitution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed"
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 13)]
            development._prepare(
                manager,
                run_dir,
                stage="level2",
                selected_ids=ids,
                selected_at=selected_at,
                inputs={candidate_id: {"concept_id": candidate_id} for candidate_id in ids},
            )
            launch_path = run_dir / "baseline_level2_launch.json"
            launch = json.loads(launch_path.read_text(encoding="utf-8"))
            launch_item = launch["batches"][0][0]
            original_packet = Path(launch_item["packet_path"])
            original_output = Path(launch_item["output_path"])
            alternate_packet = run_dir / "context/alternate-level2.md"
            alternate_output = run_dir / "agent_returns/alternate-level2.json"
            alternate_packet.write_text(
                original_packet.read_text(encoding="utf-8").replace(
                    str(original_output), str(alternate_output)
                ),
                encoding="utf-8",
            )

            precommit_path = Path(launch_item["allocation_precommit_path"])
            precommit = json.loads(precommit_path.read_text(encoding="utf-8"))
            precommit["packet_path"] = alternate_packet.relative_to(run_dir).as_posix()
            precommit["output_path"] = alternate_output.relative_to(run_dir).as_posix()
            precommit["packet_sha256"] = manager.sha256(alternate_packet)
            precommit_path.write_bytes(manager.json_bytes(precommit))
            launch_item["packet_path"] = str(alternate_packet)
            launch_item["output_path"] = str(alternate_output)
            launch_item["packet_sha256"] = precommit["packet_sha256"]
            launch_path.write_bytes(manager.json_bytes(launch))

            with mock.patch.object(manager, "find_trace_paths") as discover:
                with self.assertRaisesRegex(
                    RuntimeError, "dispatch identity|differ from precommit"
                ):
                    development.monitor_batch(
                        manager, run_dir, stage="level2", batch_index=1
                    )
            discover.assert_not_called()

    def test_dossier_depth_requires_every_neutral_section_floor(self) -> None:
        balanced_counts = [113, 113, 113, 113, 112, 112, 112, 112]
        balanced = {
            key: " ".join(["word"] * count)
            for key, count in zip(manager.COUNTED_DOSSIER_KEYS, balanced_counts)
        }
        balanced["evidence_and_sources"] = "source"
        self.assertEqual(
            development._validate_dossier_depth(
                manager,
                stage="level2",
                dossier=balanced,
                agent_id="balanced",
            ),
            900,
        )

        shallow_counts = [1, 125, 129, 129, 129, 129, 129, 129]
        shallow = {
            key: " ".join(["word"] * count)
            for key, count in zip(manager.COUNTED_DOSSIER_KEYS, shallow_counts)
        }
        shallow["evidence_and_sources"] = "source"
        self.assertEqual(sum(shallow_counts), 900)
        with self.assertRaisesRegex(RuntimeError, "75-word floor"):
            development._validate_dossier_depth(
                manager,
                stage="level2",
                dossier=shallow,
                agent_id="shallow",
            )

    def test_shadow_level2_requires_hash_bound_inputs_and_exact_categories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir, selected_at = self._prepared_run(
                Path(temporary), "level2_cohort_sealed", arm="shadow"
            )
            ids = [f"SDIR-{index:03d}" for index in range(1, 13)]
            categories = (
                ["main_provisional"] * 6
                + ["selector_or_challenger"] * 3
                + ["rejected", "near_cutoff", "singleton"]
            )
            cohort = run_dir / "sealed_shadow_level2.json"
            inputs = run_dir / "sealed_shadow_inputs.json"
            cohort.write_text(
                json.dumps(
                    {
                        "candidate_ids": ids,
                        "selected_at": selected_at,
                        "seed": self.TEST_SEED,
                        "selection_categories": dict(zip(ids, categories)),
                    }
                ),
                encoding="utf-8",
            )
            inputs.write_text(
                json.dumps({"cards": [{"concept_id": value} for value in ids]}),
                encoding="utf-8",
            )
            manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
            records = manager.read_jsonl(manifest_path)
            records[-1]["artifacts"] = [
                {"path": cohort.name, "sha256": manager.sha256(cohort)},
            ]
            manifest_path.write_bytes(manager.jsonl_bytes(records))

            with self.assertRaisesRegex(RuntimeError, "both be checkpoint hash-bound"):
                development.prepare_shadow_level2(
                    manager, run_dir, cohort_file=cohort, inputs_file=inputs
                )

            records[-1]["artifacts"].append(
                {"path": inputs.name, "sha256": manager.sha256(inputs)}
            )
            manifest_path.write_bytes(manager.jsonl_bytes(records))

            development.prepare_shadow_level2(
                manager, run_dir, cohort_file=cohort, inputs_file=inputs
            )

            launch = json.loads(
                (run_dir / "shadow_level2_launch.json").read_text(encoding="utf-8")
            )
            precommits = [
                json.loads(Path(item["allocation_precommit_path"]).read_text(encoding="utf-8"))
                for batch in launch["batches"]
                for item in batch
            ]
            self.assertEqual(
                [item["selection_category"] for item in precommits], categories
            )

    def test_freeze_validates_all_finalists_before_first_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "freeze_runtime"
            (run_dir / "agent_returns").mkdir(parents=True)
            (run_dir / "baseline_fact_closure").mkdir()
            started = manager.now() - timedelta(hours=1)
            records = [
                {
                    "record_type": "run",
                    "started_at": manager.iso(started),
                    "lifecycle_state": "closure_complete",
                },
                {"record_type": "checkpoint", "state": "closure_complete"},
            ]
            (run_dir / "00a_context_and_resource_manifest.jsonl").write_bytes(
                manager.jsonl_bytes(records)
            )
            ids = [f"DIR-{index:03d}" for index in range(1, 7)]
            (run_dir / "02d_fact_closure_candidates.json").write_text(
                json.dumps({"candidate_ids": ids, "seed": self.TEST_SEED}),
                encoding="utf-8",
            )
            ledger = []
            for index, candidate_id in enumerate(ids, 1):
                (run_dir / "agent_returns" / f"baseline-fact-closure-{index:02d}.json").write_text(
                    json.dumps({"concept_id": candidate_id, "research": []}),
                    encoding="utf-8",
                )
                (run_dir / "baseline_fact_closure" / f"closure_{candidate_id.casefold()}.md").write_text(
                    f"# frozen {candidate_id}\n", encoding="utf-8"
                )
                if index <= 5:
                    ledger.append(
                        {
                            "record_type": "mapping",
                            "raw_id": f"RAW-{index:03d}",
                            "direction_id": candidate_id,
                            "disposition": "retained",
                        }
                    )
                ledger.append(
                    {
                        "record_type": "evidence",
                        "evidence_id": f"EV-{index:03d}",
                        "stage": "fact_closure",
                        "concept_id": candidate_id,
                    }
                )
            (run_dir / "02b_raw_to_direction_ledger.jsonl").write_bytes(
                manager.jsonl_bytes(ledger)
            )

            with self.assertRaisesRegex(RuntimeError, "lacks retained or merged raw ancestry"):
                manager.freeze_baseline(run_dir)

            self.assertEqual(
                list(run_dir.glob("baseline_shadow_finalist_*.md")), []
            )

    def test_runtime_source_has_no_aggregate_level2_partition_path(self) -> None:
        source = Path(manager.__file__).read_text(encoding="utf-8")
        source += Path(development.__file__).read_text(encoding="utf-8")
        self.assertNotIn("ALLOC-B-L2-MULTI", source)
        self.assertNotIn("def partition_integer", source)


if __name__ == "__main__":
    unittest.main()
