"""Security regression tests for strict bounded apply-patch trace admission."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


UTILITIES = Path(__file__).resolve().parent
if str(UTILITIES) not in sys.path:
    sys.path.insert(0, str(UTILITIES))

import v2_matched_experiment_manager as manager  # noqa: E402


IMMUTABLE_FAILED_RUN = Path(
    "/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260823_235627"
)
IMMUTABLE_TRACE = Path(
    "/Users/igor/.codex/sessions/2026/08/23/"
    "rollout-2026-08-23T23-57-03-01a030a0-8e0f-7783-9759-42411185d235.jsonl"
)
IMMUTABLE_TRACE_SHA256 = "3cf4ae25b7deffeddde9917d1c6d319c2ea000cce55dd7145ae74b1c96b15578"
IMMUTABLE_TASK_NAME = "zero_to_one_candidates_20260823_235627_baseline_gen_fpe"
LEGITIMATE_RUN = Path(
    "/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260823_103406"
)
LEGITIMATE_TRACE = Path(
    "/Users/igor/.codex/sessions/2026/08/23/"
    "rollout-2026-08-23T10-42-10-01a02dc8-d062-7532-a325-66bd6ee48ac1.jsonl"
)
LEGITIMATE_TRACE_SHA256 = "da5adb5a5fe79cdf2f706917f1ead91c2a3c2bfb6b9d748b87a8dc4056aa3de6"
SECOND_FAILED_RUN = Path(
    "/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260824_111939"
)
SECOND_FAILED_RUN_FIXTURES = {
    "baseline-gen-tse": {
        "trace": Path(
            "/Users/igor/.codex/sessions/2026/08/24/"
            "rollout-2026-08-24T11-25-49-01a03317-2457-7bd2-ac38-8b3b08b1e643.jsonl"
        ),
        "trace_sha256": "1a23d4d2ee1c2bcade3de28c50dd728797b2bd1340104b2a59f8d59aee277303",
        "return_sha256": "32e0b6b2e9c1c98d3e5e26a66bfab65e5acc3b60cde3a46db78af2f2d95ac11e",
        "return_bytes": 23_541,
        "completed_at": "2026-08-24T11:28:50.499000+02:00",
        "form": "long",
    },
    "baseline-gen-ih": {
        "trace": Path(
            "/Users/igor/.codex/sessions/2026/08/24/"
            "rollout-2026-08-24T11-25-53-01a03317-3399-72d0-b3fe-b285c73267d7.jsonl"
        ),
        "trace_sha256": "76900f39d39bc1bfb3d863678eecc2d14da8afa868a30f4f01854a1ed148e036",
        "return_sha256": "a07c5b0f288b8ac06c585bdc9cefa36c962a987437848f22de803ac534e27ae3",
        "return_bytes": 23_505,
        "completed_at": "2026-08-24T11:28:59.045000+02:00",
        "form": "long",
    },
    "baseline-gen-ia": {
        "trace": Path(
            "/Users/igor/.codex/sessions/2026/08/24/"
            "rollout-2026-08-24T11-21-31-01a03313-353a-7d00-9c93-b0bca9df0b5c.jsonl"
        ),
        "trace_sha256": "2bff26b31d288c62892e3c3a73d81ff7df23b70addb4ad3d5fe295f4dba7717b",
        "return_sha256": "c252c78adf2ebb50b9682db0bb39db01e3b70b02ae8df493d486fdfe8cb695a3",
        "return_bytes": 27_717,
        "completed_at": "2026-08-24T11:25:41.011000+02:00",
        "form": "long",
    },
    "baseline-gen-rsa": {
        "trace": Path(
            "/Users/igor/.codex/sessions/2026/08/24/"
            "rollout-2026-08-24T11-21-46-01a03313-6f9f-7fe3-b10d-63cb0f97d427.jsonl"
        ),
        "trace_sha256": "9ebe6833c7f56f56c68cbf00d63f3b9bff640e533df06a5a05f76a631d06db7b",
        "return_sha256": "fcb7686adfb291032c5bea3c57a0a508020e2daed8c6a6ef0f3f291f6e64729f",
        "return_bytes": 26_332,
        "completed_at": "2026-08-24T11:25:17.781000+02:00",
        "form": "long-relative-target",
    },
    "baseline-gen-fpe": {
        "trace": Path(
            "/Users/igor/.codex/sessions/2026/08/24/"
            "rollout-2026-08-24T11-21-40-01a03313-576a-7940-a961-a63db5168e95.jsonl"
        ),
        "trace_sha256": "0800fe49bc8ae01d75def18b8a8027ae94511bd90f307ac4d83ee89ce8f26b54",
        "return_sha256": "90dbb93da3b164bf5f7fe8b5b99483119a71bcf74ca964ba4fe36a2dc999cdc6",
        "return_bytes": 25_402,
        "completed_at": "2026-08-24T11:25:10.912000+02:00",
        "form": "inline-await",
    },
}


class StrictBoundedApplyPatchTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=UTILITIES)
        self.root = Path(self.temporary.name).resolve()
        self.packet_path = self.root / "packet.md"
        self.output_path = self.root / "return.json"
        self.packet_path.write_text("bounded packet\n", encoding="utf-8")
        self.added_bytes = b'{"message": "quoted value"}\n'

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _patch(target: str | Path, added_lines: list[str] | None = None) -> str:
        lines = added_lines if added_lines is not None else ['{"message": "quoted value"}']
        return "\n".join(
            [
                "*** Begin Patch",
                f"*** Add File: {target}",
                *(f"+{line}" for line in lines),
                "*** End Patch",
            ]
        )

    @staticmethod
    def _wrapper(patch: str, *, spaced: bool = False) -> str:
        literal = json.dumps(patch)
        if spaced:
            return (
                f"\n const\tpatch =\n {literal} ;\n"
                "const result = await tools . apply_patch ( patch ) ;\n"
                "text ( result ) ; \n"
            )
        return (
            f"const patch = {literal};\n"
            "const result = await tools.apply_patch(patch);\n"
            "text(result);\n"
        )

    @staticmethod
    def _inline_wrapper(patch: str, *, spaced: bool = False) -> str:
        literal = json.dumps(patch)
        if spaced:
            return (
                f"\n const\tpatch =\n {literal} ;\n"
                "text ( await\n tools . apply_patch ( patch ) ) ; \n"
            )
        return (
            f"const patch = {literal};\n"
            "text(await tools.apply_patch(patch));\n"
        )

    def _trace(
        self,
        write_input: str,
        *,
        write_name: str = "exec",
        result_path: Path | None = None,
        result_bytes: bytes | None = None,
        include_custom_output: bool = True,
        create_file: bool = True,
    ) -> dict[str, object]:
        result_path = result_path or self.output_path
        result_bytes = self.added_bytes if result_bytes is None else result_bytes
        if create_file:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            self.output_path.write_bytes(self.added_bytes)

        read_id = "call-read"
        write_id = "call-write"
        read_command = f"sed -n '1,10p' {self.packet_path}"
        read_call = {
            "timestamp": "2026-08-23T10:00:00.100Z",
            "ordinal": 10,
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "name": "exec",
                "status": "completed",
                "call_id": read_id,
                "input": (
                    "const r = await tools.exec_command("
                    f'{{"cmd": {json.dumps(read_command)}}}'
                    ");\ntext(r.output);"
                ),
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-read"},
            },
        }
        write_call = {
            "timestamp": "2026-08-23T10:00:01.100Z",
            "ordinal": 20,
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "name": write_name,
                "status": "completed",
                "call_id": write_id,
                "input": write_input,
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-write"},
            },
        }
        write_output = {
            "timestamp": "2026-08-23T10:00:01.300Z",
            "ordinal": 22,
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": write_id,
                "output": [{"type": "input_text", "text": "{}"}],
                "internal_chat_message_metadata_passthrough": {"turn_id": "turn-write"},
            },
        }
        file_change = {
            "timestamp": "2026-08-23T10:00:01.200Z",
            "ordinal": 21,
            "type": "event_msg",
            "payload": {
                "type": "item_completed",
                "turn_id": "turn-write",
                "item": {
                    "type": "FileChange",
                    "status": "completed",
                    "changes": {
                        str(result_path): {
                            "type": "add",
                            "content": result_bytes.decode("utf-8"),
                        }
                    },
                    "stdout": (
                        "Success. Updated the following files:\n"
                        f"A {result_path}\n"
                    ),
                    "stderr": "",
                },
            },
        }
        outputs = {
            read_id: {
                "timestamp": "2026-08-23T10:00:00.200Z",
                "ordinal": 11,
                "payload": {
                    "call_id": read_id,
                    "internal_chat_message_metadata_passthrough": {"turn_id": "turn-read"},
                },
            }
        }
        if include_custom_output:
            outputs[write_id] = write_output
        return {
            "custom_calls": [read_call, write_call],
            "custom_outputs": outputs,
            "file_change_events": [file_change],
            "web_calls": [],
        }

    def _valid_trace(self, *, spaced: bool = False) -> dict[str, object]:
        patch = self._patch(self.output_path)
        return self._trace(self._wrapper(patch, spaced=spaced))

    def test_exact_immutable_failed_trace_now_passes_bounded_write_verification(self) -> None:
        self.assertEqual(manager.sha256(IMMUTABLE_TRACE), IMMUTABLE_TRACE_SHA256)
        trace = manager._parse_trace_at_path(IMMUTABLE_TASK_NAME, IMMUTABLE_TRACE)
        packet_path = IMMUTABLE_FAILED_RUN / "context/baseline-gen-fpe.md"
        output_path = IMMUTABLE_FAILED_RUN / "agent_returns/baseline-gen-fpe.json"

        attestation = manager.verify_single_bounded_apply_patch(trace, output_path)
        manager.assert_single_packet_read(trace, packet_path, output_path)

        self.assertEqual(attestation["representation"], "json-string-wrapper")
        self.assertEqual(attestation["path"], str(output_path))
        self.assertEqual(
            manager.apply_patch_completion_time(trace, output_path),
            "2026-08-24T00:00:03.381000+02:00",
        )

    def test_exact_second_failing_inline_await_trace_now_passes(self) -> None:
        fixture = SECOND_FAILED_RUN_FIXTURES["baseline-gen-fpe"]
        trace_path = fixture["trace"]
        output_path = SECOND_FAILED_RUN / "agent_returns/baseline-gen-fpe.json"
        task_name = "zero_to_one_candidates_20260824_111939_baseline_gen_fpe"

        self.assertEqual(manager.sha256(trace_path), fixture["trace_sha256"])
        self.assertEqual(manager.sha256(output_path), fixture["return_sha256"])
        trace = manager._parse_trace_at_path(task_name, trace_path)
        attestation = manager.verify_single_bounded_apply_patch(trace, output_path)

        self.assertEqual(attestation["representation"], "json-string-wrapper")
        self.assertEqual(attestation["path"], str(output_path))
        self.assertEqual(attestation["added_sha256"], fixture["return_sha256"])
        self.assertEqual(
            manager.apply_patch_completion_time(trace, output_path),
            fixture["completed_at"],
        )

    def test_all_second_failed_run_discovery_traces_replay_read_only(self) -> None:
        for agent_id, fixture in SECOND_FAILED_RUN_FIXTURES.items():
            with self.subTest(agent_id=agent_id):
                trace_path = fixture["trace"]
                output_path = SECOND_FAILED_RUN / "agent_returns" / f"{agent_id}.json"
                task_name = (
                    "zero_to_one_candidates_20260824_111939_"
                    + agent_id.replace("-", "_")
                )
                self.assertEqual(manager.sha256(trace_path), fixture["trace_sha256"])
                returned_bytes = output_path.read_bytes()
                self.assertEqual(len(returned_bytes), fixture["return_bytes"])
                self.assertEqual(manager.sha256_bytes(returned_bytes), fixture["return_sha256"])

                trace = manager._parse_trace_at_path(task_name, trace_path)
                write_call = [
                    call for call in trace["custom_calls"]
                    if manager._is_apply_patch_call(call)
                ][0]
                raw = write_call["payload"]["input"]
                if fixture["form"] == "inline-await":
                    self.assertIsNotNone(
                        manager._APPLY_PATCH_INLINE_AWAIT_WRAPPER_RE.fullmatch(raw)
                    )
                else:
                    self.assertIsNotNone(
                        manager._APPLY_PATCH_LONG_WRAPPER_RE.fullmatch(raw)
                    )

                event = trace["file_change_events"][0]
                change = event["payload"]["item"]["changes"][str(output_path)]
                self.assertEqual(change["content"].encode("utf-8"), returned_bytes)
                self.assertEqual(
                    manager.iso(
                        manager.parse_timestamp(event["timestamp"]).astimezone(
                            manager.LOCAL_TZ
                        )
                    ),
                    fixture["completed_at"],
                )

                if fixture["form"] == "long-relative-target":
                    with self.assertRaisesRegex(RuntimeError, "target is not canonical"):
                        manager.verify_single_bounded_apply_patch(trace, output_path)
                    continue

                attestation = manager.verify_single_bounded_apply_patch(
                    trace, output_path
                )
                self.assertEqual(attestation["path"], str(output_path))
                self.assertEqual(attestation["added_sha256"], fixture["return_sha256"])
                self.assertEqual(
                    manager.apply_patch_completion_time(trace, output_path),
                    fixture["completed_at"],
                )

    def test_rsa_trace_clone_with_exact_absolute_target_attests(self) -> None:
        fixture = SECOND_FAILED_RUN_FIXTURES["baseline-gen-rsa"]
        output_path = SECOND_FAILED_RUN / "agent_returns/baseline-gen-rsa.json"
        task_name = "zero_to_one_candidates_20260824_111939_baseline_gen_rsa"
        trace = manager._parse_trace_at_path(task_name, fixture["trace"])
        write_call = next(
            call for call in trace["custom_calls"] if manager._is_apply_patch_call(call)
        )
        wrapper = manager._APPLY_PATCH_LONG_WRAPPER_RE.fullmatch(
            write_call["payload"]["input"]
        )
        self.assertIsNotNone(wrapper)
        patch = json.loads(wrapper.group("patch_literal"))
        relative_header = (
            "*** Add File: working_folder/zero_to_one_candidates_20260824_111939/"
            "agent_returns/baseline-gen-rsa.json"
        )
        absolute_header = f"*** Add File: {output_path}"
        self.assertEqual(patch.count(relative_header), 1)
        corrected_patch = patch.replace(relative_header, absolute_header)
        write_call["payload"]["input"] = (
            f"const patch = {json.dumps(corrected_patch)};\n"
            "const result = await tools.apply_patch(patch);\n"
            "text(result);"
        )
        trace["file_change_events"][0]["payload"]["item"]["stdout"] = (
            f"Success. Updated the following files:\nA {output_path}\n"
        )

        attestation = manager.verify_single_bounded_apply_patch(trace, output_path)
        self.assertEqual(attestation["path"], str(output_path))
        self.assertEqual(attestation["added_sha256"], fixture["return_sha256"])
        self.assertEqual(
            manager.apply_patch_completion_time(trace, output_path),
            fixture["completed_at"],
        )

    def test_immutable_rsa_trace_remains_rejected(self) -> None:
        fixture = SECOND_FAILED_RUN_FIXTURES["baseline-gen-rsa"]
        output_path = SECOND_FAILED_RUN / "agent_returns/baseline-gen-rsa.json"
        task_name = "zero_to_one_candidates_20260824_111939_baseline_gen_rsa"
        self.assertEqual(manager.sha256(fixture["trace"]), fixture["trace_sha256"])
        trace = manager._parse_trace_at_path(task_name, fixture["trace"])
        with self.assertRaisesRegex(RuntimeError, "target is not canonical"):
            manager.verify_single_bounded_apply_patch(trace, output_path)

    def test_second_failed_run_has_no_integrated_discovery_output(self) -> None:
        records = manager.read_jsonl(
            SECOND_FAILED_RUN / "00a_context_and_resource_manifest.jsonl"
        )
        self.assertEqual(
            [record.get("state") for record in records if record.get("record_type") == "checkpoint"],
            ["registered"],
        )
        self.assertFalse(any(record.get("record_type") == "agent" for record in records))
        self.assertFalse((SECOND_FAILED_RUN / "02a_raw_pool.md").exists())
        self.assertEqual(
            sorted(path.name for path in (SECOND_FAILED_RUN / "trace_attestations").iterdir()),
            ["baseline-gen-ia.json"],
        )

    def test_archipelago_protocol_requires_canonical_wrapper_in_all_return_packets(self) -> None:
        protocol = manager.PROTOCOL.read_text(encoding="utf-8")
        self.assertIn(
            "```javascript\n"
            + manager.CANONICAL_BOUNDED_RETURN_WRAPPER
            + "\n```",
            protocol,
        )
        mandatory_sentence = next(
            paragraph
            for paragraph in protocol.split("\n\n")
            if paragraph.startswith("This path-bound rendering and pre-dispatch check")
        )
        self.assertIn("packet-specific canonical absolute output path", protocol)
        self.assertIn("exactly one absolute `Required return path` declaration", protocol)
        self.assertIn("exactly one literal `*** Add File:` line", protocol)
        self.assertIn("Packet bytes must still match their precommit hash", protocol)
        bounded_section = protocol.split("Every bounded-return packet uses", 1)[1].split(
            "### Allowed common content", 1
        )[0]
        self.assertNotIn("zero_to_one_candidates_", bounded_section)
        self.assertNotIn("<EXACT_ABSOLUTE_OUTPUT_PATH>", bounded_section)
        for stage_label in (
            "Audited Funnel discovery",
            "discovery/scout",
            "direct-builder",
            "inversion",
            "recombination",
            "history",
            "cartography/mapping",
            "cluster-audit",
            "Level-1",
            "provisional-selector",
            "ranker",
            "challenger",
            "Level-2",
            "finalist-selector",
            "fact-closure",
        ):
            self.assertIn(stage_label, mandatory_sentence)

    def test_approved_legacy_raw_patch_passes_separate_strict_path(self) -> None:
        patch = self._patch(self.output_path)
        trace = self._trace(patch, write_name="apply_patch")
        attestation = manager.verify_single_bounded_apply_patch(trace, self.output_path)
        manager.assert_single_packet_read(trace, self.packet_path, self.output_path)
        self.assertEqual(attestation["representation"], "legacy-raw-patch")

    def test_both_json_wrappers_decode_escaped_content_and_whitespace(self) -> None:
        lines = ['{"message": "quoted value"}']
        patch = self._patch(self.output_path, lines)
        for form, wrapper in (
            ("long", self._wrapper(patch, spaced=True)),
            ("inline-await", self._inline_wrapper(patch, spaced=True)),
        ):
            with self.subTest(form=form):
                self.assertIn("\\n", wrapper)
                self.assertIn('\\"quoted value\\"', wrapper)
                trace = self._trace(wrapper)
                manager.assert_single_packet_read(
                    trace, self.packet_path, self.output_path
                )

    def test_wrong_target_path_is_rejected(self) -> None:
        wrong = self.root / "wrong.json"
        trace = self._trace(self._wrapper(self._patch(wrong)))
        with self.assertRaisesRegex(RuntimeError, "does not equal expected canonical path"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_path_traversal_is_rejected(self) -> None:
        traversal = f"{self.output_path.parent}/../escape.json"
        trace = self._trace(self._wrapper(self._patch(traversal)))
        with self.assertRaisesRegex(RuntimeError, "target is not canonical"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_absolute_sibling_path_is_rejected(self) -> None:
        sibling = self.output_path.with_name("sibling.json")
        trace = self._trace(self._wrapper(self._patch(sibling)))
        with self.assertRaisesRegex(RuntimeError, "does not equal expected canonical path"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_two_add_file_headers_are_rejected(self) -> None:
        sibling = self.output_path.with_name("second.json")
        patch = "\n".join(
            [
                "*** Begin Patch",
                f"*** Add File: {self.output_path}",
                "+first",
                f"*** Add File: {sibling}",
                "+second",
                "*** End Patch",
            ]
        )
        trace = self._trace(self._wrapper(patch))
        with self.assertRaisesRegex(RuntimeError, "exactly one begin, add-file, and end"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_update_delete_and_move_headers_are_rejected(self) -> None:
        cases = {
            "update": "\n".join(
                [
                    "*** Begin Patch",
                    f"*** Update File: {self.output_path}",
                    "@@",
                    "-old",
                    "+new",
                    "*** End Patch",
                ]
            ),
            "delete": "\n".join(
                [
                    "*** Begin Patch",
                    f"*** Delete File: {self.output_path}",
                    "*** End Patch",
                ]
            ),
            "move": "\n".join(
                [
                    "*** Begin Patch",
                    f"*** Add File: {self.output_path}",
                    '+{"message": "quoted value"}',
                    f"*** Move to: {self.output_path.with_name('moved.json')}",
                    "*** End Patch",
                ]
            ),
        }
        for label, patch in cases.items():
            with self.subTest(label=label):
                trace = self._trace(self._wrapper(patch))
                with self.assertRaises(RuntimeError):
                    manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_extra_javascript_statement_is_encoding_error(self) -> None:
        wrapper = self._wrapper(self._patch(self.output_path)) + "const ignored = 1;\n"
        trace = self._trace(wrapper)
        with self.assertRaisesRegex(
            manager.ApplyPatchTraceEncodingError, "unsupported apply_patch trace encoding"
        ):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_extra_statements_before_or_after_inline_call_are_encoding_errors(self) -> None:
        inline = self._inline_wrapper(self._patch(self.output_path))
        cases = {
            "before": "const ignored = 1;\n" + inline,
            "after": inline + "const ignored = 1;\n",
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_second_inline_apply_patch_call_is_encoding_error(self) -> None:
        inline = self._inline_wrapper(self._patch(self.output_path))
        wrapper = inline.replace(
            "text(await tools.apply_patch(patch));",
            "text(await tools.apply_patch(patch));\n"
            "text(await tools.apply_patch(patch));",
        )
        trace = self._trace(wrapper)
        with self.assertRaisesRegex(
            manager.ApplyPatchTraceEncodingError,
            "unsupported apply_patch trace encoding",
        ):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_nested_additional_tool_calls_are_encoding_errors(self) -> None:
        patch = self._patch(self.output_path)
        literal = json.dumps(patch)
        cases = {
            "patch-argument": (
                f"const patch = {literal};\n"
                "text(await tools.apply_patch(await tools.exec_command({})));\n"
            ),
            "output-argument": (
                f"const patch = {literal};\n"
                "text(await tools.apply_patch(patch), await tools.view_image({}));\n"
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_second_nested_tool_call_is_encoding_error(self) -> None:
        wrapper = self._wrapper(self._patch(self.output_path)).replace(
            "const result =",
            "const duplicate = await tools.apply_patch(patch);\nconst result =",
        )
        trace = self._trace(wrapper)
        with self.assertRaisesRegex(
            manager.ApplyPatchTraceEncodingError, "unsupported apply_patch trace encoding"
        ):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_bracket_optional_and_commented_apply_patch_spellings_are_encoding_errors(self) -> None:
        base = self._wrapper(self._patch(self.output_path))
        cases = {
            "bracket": base.replace("tools.apply_patch", 'tools["apply_patch"]'),
            "computed": base.replace("tools.apply_patch", "tools[method]"),
            "computed-concatenation": base.replace(
                "tools.apply_patch", 'tools["apply_" + "patch"]'
            ),
            "optional": base.replace("tools.apply_patch", "tools?.apply_patch"),
            "commented": base.replace("tools.apply_patch", "tools/*x*/.apply_patch"),
            "alternate-tool": base.replace("tools.apply_patch", "toolbox.apply_patch"),
            "alternate-property": base.replace("tools.apply_patch", "tools.applyPatch"),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_eval_indirect_execution_and_non_json_escape_decoding_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        literal = json.dumps(patch)
        cases = {
            "eval": (
                f"const patch = {literal};\n"
                'text(await eval("tools.apply_patch(patch)"));\n'
            ),
            "indirect-eval": (
                f"const patch = {literal};\n"
                'text(await (0, eval)("tools.apply_patch(patch)"));\n'
            ),
            "function": (
                f"const patch = {literal};\n"
                'text(await Function("return tools.apply_patch(patch)")());\n'
            ),
            "json-parse": (
                f"const patch = JSON.parse({json.dumps(json.dumps(patch))});\n"
                "text(await tools.apply_patch(patch));\n"
            ),
            "javascript-hex-escape": (
                r'const patch = "\x2a\x2a\x2a Begin Patch";'
                "\n"
                "text(await tools.apply_patch(patch));\n"
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_concatenated_template_and_dynamic_patch_construction_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        suffix = (
            "const result = await tools.apply_patch(patch);\n"
            "text(result);\n"
        )
        cases = {
            "concatenated": f"const patch = {json.dumps(patch)} + \"\";\n{suffix}",
            "template": f"const patch = `{patch}`;\n{suffix}",
            "dynamic": f"const patch = buildPatch();\n{suffix}",
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_alternate_output_functions_and_promise_chaining_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        literal = json.dumps(patch)
        cases = {
            "notify": (
                f"const patch = {literal};\n"
                "notify(await tools.apply_patch(patch));\n"
            ),
            "image": (
                f"const patch = {literal};\n"
                "image(await tools.apply_patch(patch));\n"
            ),
            "then": (
                f"const patch = {literal};\n"
                "text(tools.apply_patch(patch).then(text));\n"
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_extra_arguments_are_encoding_errors(self) -> None:
        inline = self._inline_wrapper(self._patch(self.output_path))
        cases = {
            "apply-patch": inline.replace(
                "tools.apply_patch(patch)", "tools.apply_patch(patch, null)"
            ),
            "text": inline.replace(
                "text(await tools.apply_patch(patch))",
                "text(await tools.apply_patch(patch), null)",
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_comma_conditional_sequence_spread_and_assignment_expressions_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        literal = json.dumps(patch)
        prefix = f"const patch = {literal};\n"
        cases = {
            "comma": prefix + "text((0, await tools.apply_patch(patch)));\n",
            "conditional": (
                prefix
                + "text(true ? await tools.apply_patch(patch) : null);\n"
            ),
            "sequence": (
                prefix
                + "text((await tools.apply_patch(patch), patch));\n"
            ),
            "spread": prefix + "text(await tools.apply_patch(...[patch]));\n",
            "assignment": (
                prefix
                + "text(await tools.apply_patch(patch = \"replacement\"));\n"
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_alternate_variables_and_additional_assignments_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        literal = json.dumps(patch)
        cases = {
            "patch-variable": (
                f"const p = {literal};\n"
                "text(await tools.apply_patch(p));\n"
            ),
            "result-variable": (
                f"const patch = {literal};\n"
                "const output = await tools.apply_patch(patch);\n"
                "text(output);\n"
            ),
            "additional-assignment": (
                f"const patch = {literal};\n"
                "let result;\n"
                "result = await tools.apply_patch(patch);\n"
                "text(result);\n"
            ),
        }
        for label, wrapper in cases.items():
            with self.subTest(label=label):
                trace = self._trace(wrapper)
                with self.assertRaisesRegex(
                    manager.ApplyPatchTraceEncodingError,
                    "unsupported apply_patch trace encoding",
                ):
                    manager.verify_single_bounded_apply_patch(
                        trace, self.output_path
                    )

    def test_mismatched_tool_output_is_rejected(self) -> None:
        sibling = self.output_path.with_name("reported-sibling.json")
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), result_path=sibling
        )
        with self.assertRaisesRegex(RuntimeError, "does not attest one added expected path"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_patch_result_and_file_byte_disagreements_are_rejected(self) -> None:
        patch = self._patch(self.output_path)
        patch_result_mismatch = self._trace(
            self._wrapper(patch), result_bytes=b"different result bytes\n"
        )
        with self.assertRaisesRegex(RuntimeError, "patch bytes and tool result differ"):
            manager.verify_single_bounded_apply_patch(
                patch_result_mismatch, self.output_path
            )

        different = b"different but mutually attested bytes\n"
        matching_patch = self._patch(
            self.output_path, [different.decode("utf-8").rstrip("\n")]
        )
        result_file_mismatch = self._trace(
            self._wrapper(matching_patch), result_bytes=different
        )
        with self.assertRaisesRegex(RuntimeError, "bytes differ from resulting file"):
            manager.verify_single_bounded_apply_patch(
                result_file_mismatch, self.output_path
            )

    def test_missing_custom_tool_output_is_rejected(self) -> None:
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), include_custom_output=False
        )
        with self.assertRaisesRegex(RuntimeError, "lacks corresponding custom-tool output"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_symlink_target_is_rejected(self) -> None:
        real_file = self.root / "real.json"
        real_file.write_bytes(self.added_bytes)
        self.output_path.symlink_to(real_file)
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), create_file=False
        )
        with self.assertRaisesRegex(RuntimeError, "contains a symlink"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_symlinked_path_component_is_rejected(self) -> None:
        real_directory = self.root / "real-directory"
        real_directory.mkdir()
        alias = self.root / "alias"
        alias.symlink_to(real_directory, target_is_directory=True)
        self.output_path = alias / "return.json"
        (real_directory / "return.json").write_bytes(self.added_bytes)
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), create_file=False
        )
        with self.assertRaisesRegex(RuntimeError, "contains a symlink"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_patch_bytes_differing_from_resulting_file_are_rejected(self) -> None:
        trace = self._trace(self._wrapper(self._patch(self.output_path)))
        self.output_path.write_bytes(b"different bytes\n")
        with self.assertRaisesRegex(RuntimeError, "bytes differ from resulting file"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_existing_legitimate_one_read_one_write_path_passes(self) -> None:
        trace = self._valid_trace()
        manager.assert_single_packet_read(trace, self.packet_path, self.output_path)

        self.assertEqual(manager.sha256(LEGITIMATE_TRACE), LEGITIMATE_TRACE_SHA256)
        historical = manager._parse_trace_at_path("baseline_gen_fpe", LEGITIMATE_TRACE)
        manager.assert_single_packet_read(
            historical,
            LEGITIMATE_RUN / "context/baseline-gen-fpe.md",
            LEGITIMATE_RUN / "agent_returns/baseline-gen-fpe.json",
        )

    def test_undeclared_tool_and_second_packet_read_remain_rejected(self) -> None:
        undeclared = self._valid_trace()
        undeclared["custom_calls"].append(
            {
                "ordinal": 15,
                "payload": {
                    "call_id": "call-undeclared",
                    "name": "exec",
                    "status": "completed",
                    "input": "const result = await tools.view_image({}); text(result);",
                },
            }
        )
        with self.assertRaisesRegex(RuntimeError, "undeclared non-research tool"):
            manager.assert_single_packet_read(
                undeclared, self.packet_path, self.output_path
            )

        second_read = self._valid_trace()
        duplicate = copy.deepcopy(second_read["custom_calls"][0])
        duplicate["ordinal"] = 12
        duplicate["payload"]["call_id"] = "call-read-again"
        second_read["custom_calls"].insert(1, duplicate)
        with self.assertRaisesRegex(RuntimeError, "one allowlisted packet"):
            manager.assert_single_packet_read(
                second_read, self.packet_path, self.output_path
            )

    def test_two_nested_exec_commands_in_one_outer_call_are_rejected(self) -> None:
        trace = self._valid_trace()
        read_call = trace["custom_calls"][0]
        read_call["payload"]["input"] = read_call["payload"]["input"].replace(
            ");\ntext(r.output);",
            ");\n"
            'const leak = await tools.exec_command({"cmd":"sed -n \'1,2p\' /etc/hosts"});\n'
            "text(r.output);",
        )
        with self.assertRaisesRegex(RuntimeError, "unsupported wrapper or nested statement"):
            manager.assert_single_packet_read(trace, self.packet_path, self.output_path)

    def test_web_wrapper_cannot_hide_a_nested_exec_command(self) -> None:
        trace = self._valid_trace()
        trace["custom_calls"].insert(
            1,
            {
                "ordinal": 15,
                "payload": {
                    "call_id": "call-web-with-hidden-exec",
                    "name": "exec",
                    "status": "completed",
                    "input": (
                        'const r = await tools.web__run({search_query:[{q:"safe"}],'
                        'response_length:"long"});\n'
                        'const leak = await tools.exec_command({"cmd":"sed -n \'1,2p\' /etc/hosts"});\n'
                        "text(r)"
                    ),
                },
            },
        )
        with self.assertRaisesRegex(RuntimeError, "nested or extra statements are forbidden"):
            manager.assert_single_packet_read(trace, self.packet_path, self.output_path)

    def test_directory_result_is_rejected_as_non_regular(self) -> None:
        self.output_path.mkdir()
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), create_file=False
        )
        with self.assertRaisesRegex(RuntimeError, "not a regular file"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_hard_linked_result_is_rejected_as_alias(self) -> None:
        outside = self.root / "outside.json"
        outside.write_bytes(self.added_bytes)
        os.link(outside, self.output_path)
        trace = self._trace(
            self._wrapper(self._patch(self.output_path)), create_file=False
        )
        with self.assertRaisesRegex(RuntimeError, "hard-link alias"):
            manager.verify_single_bounded_apply_patch(trace, self.output_path)

    def test_case_aliased_result_spelling_is_rejected(self) -> None:
        actual = self.root / "Return.JSON"
        expected = self.root / "return.json"
        actual.write_bytes(self.added_bytes)
        if not expected.exists():
            self.skipTest("filesystem is case-sensitive")
        trace = self._trace(
            self._wrapper(self._patch(expected)),
            result_path=expected,
            create_file=False,
        )
        with self.assertRaisesRegex(RuntimeError, "alternate filesystem spelling"):
            manager.verify_single_bounded_apply_patch(trace, expected)

    def test_synthetic_attestation_hash_is_reconstructed_from_patch_bytes(self) -> None:
        trace = self._valid_trace()
        attestation = manager.verify_single_bounded_apply_patch(trace, self.output_path)
        self.assertEqual(
            attestation["added_sha256"], hashlib.sha256(self.added_bytes).hexdigest()
        )


class PathBoundBoundedReturnPacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=UTILITIES)
        self.run_dir = (Path(self.temporary.name) / "synthetic-run").resolve()
        self.context_dir = self.run_dir / "context"
        self.return_dir = self.run_dir / "agent_returns"
        self.context_dir.mkdir(parents=True)
        self.return_dir.mkdir()
        self.packet_path = self.context_dir / "agent.md"
        self.output_path = self.return_dir / "agent.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _packet_text(self) -> str:
        return (
            "# Immutable Test Packet\n\n"
            f"- Required return path: `{self.output_path}`\n\n"
            + manager.bounded_return_instruction(self.output_path, self.run_dir)
            + "\n"
        )

    def _write_and_validate(self, packet_text: str) -> None:
        self.packet_path.write_text(packet_text, encoding="utf-8")
        manager.assert_bounded_return_packet(
            self.packet_path, self.output_path, self.run_dir
        )

    def test_rendered_instruction_binds_exact_absolute_path_without_path_placeholder(self) -> None:
        packet_text = self._packet_text()
        exact_header = f"*** Add File: {self.output_path}"
        self.assertEqual(packet_text.count(exact_header), 1)
        self.assertEqual(
            packet_text.count(f"- Required return path: `{self.output_path}`"), 1
        )
        self.assertEqual(
            packet_text.count(manager.CANONICAL_BOUNDED_RETURN_WRAPPER), 1
        )
        for placeholder in (
            "<EXACT_ABSOLUTE_OUTPUT_PATH>",
            "<ABSOLUTE_OUTPUT_PATH>",
            "<OUTPUT_PATH>",
            "<RETURN_PATH>",
        ):
            self.assertNotIn(placeholder, packet_text)
        self._write_and_validate(packet_text)

    def test_relative_workspace_relative_and_mismatched_headers_fail_predispatch(self) -> None:
        exact_header = f"*** Add File: {self.output_path}"
        cases = {
            "relative": "*** Add File: agent_returns/agent.json",
            "workspace-relative": (
                "*** Add File: working_folder/synthetic-run/agent_returns/agent.json"
            ),
            "mismatched-absolute": f"*** Add File: {self.return_dir / 'other.json'}",
            "placeholder": "*** Add File: <EXACT_ABSOLUTE_OUTPUT_PATH>",
        }
        for label, replacement in cases.items():
            with self.subTest(label=label):
                packet_text = self._packet_text().replace(exact_header, replacement)
                self.packet_path.write_text(packet_text, encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "Add File|instruction"):
                    manager.assert_bounded_return_packet(
                        self.packet_path, self.output_path, self.run_dir
                    )

    def test_relative_workspace_relative_and_mismatched_return_declarations_fail(self) -> None:
        declaration = f"- Required return path: `{self.output_path}`"
        cases = {
            "relative": "- Required return path: `agent_returns/agent.json`",
            "workspace-relative": (
                "- Required return path: `working_folder/synthetic-run/"
                "agent_returns/agent.json`"
            ),
            "mismatched-absolute": (
                f"- Required return path: `{self.return_dir / 'other.json'}`"
            ),
            "placeholder": "- Required return path: `<EXACT_ABSOLUTE_OUTPUT_PATH>`",
        }
        for label, replacement in cases.items():
            with self.subTest(label=label):
                packet_text = self._packet_text().replace(declaration, replacement)
                self.packet_path.write_text(packet_text, encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "return path"):
                    manager.assert_bounded_return_packet(
                        self.packet_path, self.output_path, self.run_dir
                    )

    def test_duplicate_headers_return_paths_and_wrappers_fail_predispatch(self) -> None:
        packet_text = self._packet_text()
        declaration = f"- Required return path: `{self.output_path}`"
        header = f"*** Add File: {self.output_path}"
        cases = {
            "duplicate-return": packet_text + declaration + "\n",
            "duplicate-header": packet_text + header + "\n",
            "duplicate-wrapper": (
                packet_text + manager.CANONICAL_BOUNDED_RETURN_WRAPPER + "\n"
            ),
            "alternate-operation": packet_text + f"*** Update File: {self.output_path}\n",
            "indented-operation": packet_text + f"  *** Delete File: {self.output_path}\n",
            "quoted-operation": packet_text + f"> *** Delete File: {self.output_path}\n",
            "commented-operation": (
                packet_text + f"<!-- *** Delete File: {self.output_path} -->\n"
            ),
            "markdown-escaped-operation": (
                packet_text + r"> \*\*\* Delete File: /tmp/escape" + "\n"
            ),
            "html-entity-operation": (
                packet_text + "&#42;&#42;&#42; Delete File: /tmp/escape\n"
            ),
            "alternate-wrapper": (
                packet_text + "text(await tools . apply_patch(other));\n"
            ),
            "brace-placeholder": packet_text + "{OUTPUT_PATH}\n",
            "dollar-placeholder": packet_text + "$RETURN_PATH\n",
            "target-placeholder": packet_text + "<TARGET_FILE>\n",
            "relative-alternative": packet_text + "Alternative: agent_returns/agent.json\n",
            "parent-relative-alternative": (
                packet_text + "Alternative: synthetic-run/agent_returns/agent.json\n"
            ),
            "different-relative-alternative": (
                packet_text + "Alternative output path: agent_returns/escape.json\n"
            ),
            "absolute-alternative": (
                packet_text + "Alternative output path: /tmp/escape.json\n"
            ),
            "bare-alternative": packet_text + "Output path: escape.json\n",
            "write-alternative": packet_text + "Write output to /tmp/escape.json\n",
        }
        for label, malformed in cases.items():
            with self.subTest(label=label):
                self.packet_path.write_text(malformed, encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    manager.assert_bounded_return_packet(
                        self.packet_path, self.output_path, self.run_dir
                    )

    def test_relative_outside_traversal_and_symlinked_output_paths_fail_rendering(self) -> None:
        cases = {
            "relative-output": Path("agent_returns/agent.json"),
            "outside-return-dir": self.run_dir / "other" / "agent.json",
            "traversal": Path(f"{self.return_dir}/../escape.json"),
            "header-injection": self.return_dir / "agent\n*** Add File: escape.json",
        }
        for label, output_path in cases.items():
            with self.subTest(label=label), self.assertRaises(RuntimeError):
                manager.bounded_return_instruction(output_path, self.run_dir)

        for character in ("\u0085", "\u200b", "\u2028", "\u202e", "\u2066"):
            with self.subTest(codepoint=f"U+{ord(character):04X}"), self.assertRaisesRegex(
                RuntimeError, "control or format"
            ):
                manager.bounded_return_instruction(
                    self.return_dir / f"agent{character}.json", self.run_dir
                )

        with self.assertRaisesRegex(RuntimeError, "canonical Unicode form"):
            manager.bounded_return_instruction(
                self.return_dir / "cafe\u0301.json", self.run_dir
            )

        outside_file = self.run_dir / "outside.json"
        outside_file.write_text("{}\n", encoding="utf-8")
        hard_link = self.return_dir / "hard-link.json"
        os.link(outside_file, hard_link)
        with self.assertRaisesRegex(RuntimeError, "already exists|aliases"):
            manager.bounded_return_instruction(hard_link, self.run_dir)

        real_output = self.return_dir / "real.json"
        real_output.write_text("{}\n", encoding="utf-8")
        self.output_path.symlink_to(real_output)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            manager.bounded_return_instruction(self.output_path, self.run_dir)

    def test_hard_linked_packet_fails_predispatch(self) -> None:
        outside_packet = self.run_dir / "outside-packet.md"
        outside_packet.write_text(self._packet_text(), encoding="utf-8")
        os.link(outside_packet, self.packet_path)
        with self.assertRaisesRegex(RuntimeError, "immutable run-owned regular file"):
            manager.assert_bounded_return_packet(
                self.packet_path, self.output_path, self.run_dir
            )

    def test_symlinked_agent_returns_directory_fails_rendering(self) -> None:
        other_run = self.run_dir.parent / "symlinked-run"
        other_run.mkdir()
        real_returns = self.run_dir.parent / "real-returns"
        real_returns.mkdir()
        (other_run / "agent_returns").symlink_to(real_returns, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            manager.bounded_return_instruction(
                other_run / "agent_returns/agent.json", other_run
            )

    def test_case_aliased_run_directory_fails_rendering(self) -> None:
        actual_run = self.run_dir.parent / "RunCase"
        (actual_run / "agent_returns").mkdir(parents=True)
        aliased_run = self.run_dir.parent / "runcase"
        if not aliased_run.exists():
            self.skipTest("filesystem is case-sensitive")
        with self.assertRaisesRegex(RuntimeError, "alternate filesystem spelling"):
            manager.bounded_return_instruction(
                aliased_run / "agent_returns/agent.json", aliased_run
            )


if __name__ == "__main__":
    unittest.main()
