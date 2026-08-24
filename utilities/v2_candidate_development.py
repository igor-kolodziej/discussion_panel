"""Isolated, candidate-owned development stages for V2 matched runs.

The caller supplies the experiment-manager module as ``api``.  This keeps the
run registration and trace parser in one place while making the admission
logic independently testable.  Every admitted agent owns one candidate, one
allocation, one return, and one immutable run-local trace.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ALLOWED_EVIDENCE_STATUSES = {
    "verified",
    "interpreted",
    "counsel-required",
    "unknown",
    "contradicted",
}
RESEARCH_FIELDS = {
    "query_text",
    "opened_url",
    "source_title",
    "source_date",
    "proposition",
    "status",
    "contradiction",
}
RETURN_FIELDS = {
    "agent_id",
    "assigned_ids",
    "output_ids",
    "files_read",
    "concept_id",
    "research",
    "cheapest_resolving_test",
}


def _utc(value: datetime) -> datetime:
    """Normalize an aware timestamp before chronology comparisons."""
    if value.tzinfo is None:
        raise RuntimeError("development chronology requires offset-aware timestamps")
    return value.astimezone(timezone.utc)


def _chunks(values: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def _normal(value: str) -> str:
    return " ".join(value.split())


def _exact_nonempty_strings(payload: dict[str, Any], fields: set[str], label: str) -> None:
    for field in fields:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise RuntimeError(f"{label} lacks nonempty {field}")


def _dossier_section_word_counts(
    api: Any, dossier: dict[str, str]
) -> dict[str, int]:
    return {
        key: len(re.findall(r"\b[\w'-]+\b", dossier[key], flags=re.UNICODE))
        for key in api.COUNTED_DOSSIER_KEYS
    }


def _dossier_word_count(api: Any, dossier: dict[str, str]) -> int:
    return sum(_dossier_section_word_counts(api, dossier).values())


def _validate_dossier_depth(
    api: Any, *, stage: str, dossier: dict[str, str], agent_id: str
) -> int:
    prose_contract = api.development_contract()["dossier_prose_word_ranges"][
        "level2" if stage == "level2" else "frozen"
    ]
    minimum = prose_contract["minimum"]
    maximum = prose_contract["maximum"]
    minimum_per_section = prose_contract["minimum_per_section"]
    section_words = _dossier_section_word_counts(api, dossier)
    prose_words = sum(section_words.values())
    if not minimum <= prose_words <= maximum:
        raise RuntimeError(
            f"{agent_id} counted dossier prose is {prose_words} words; "
            f"expected {minimum}–{maximum}"
        )
    shallow_sections = [
        key for key, words in section_words.items() if words < minimum_per_section
    ]
    if shallow_sections:
        raise RuntimeError(
            f"{agent_id} dossier sections fall below the neutral "
            f"{minimum_per_section}-word floor: {shallow_sections}"
        )
    return prose_words


def _render_dossier(
    api: Any,
    concept_id: str,
    dossier: dict[str, str],
    *,
    arm: str,
    stage: str,
) -> str:
    owner = "Baseline" if arm == "matched_baseline" else "Shadow"
    stage_title = "Frozen Dossier" if stage == "fact_closure" else "Level-2 Dossier"
    blocks = [
        f"# {owner} {stage_title} — {concept_id}",
        "",
        f"- Arm: `{arm}`",
        "- Routing state: `frozen_nonrouting`",
        "- Shadow only: `true`",
        "- Validation eligible: `false`",
        "",
    ]
    for heading, key in zip(api.DOSSIER_SECTIONS, api.DOSSIER_KEYS):
        blocks.extend([heading, "", dossier[key], ""])
    return "\n".join(blocks).rstrip() + "\n"


def _remaining_development_fit(
    api: Any, run_record: dict[str, Any], required_minutes: int
) -> None:
    deadline = datetime.fromisoformat(run_record["deadline_at"])
    latest_start = deadline - timedelta(minutes=required_minutes)
    if _utc(api.now()) >= _utc(latest_start):
        raise RuntimeError(
            "run deadline cannot accommodate the remaining isolated development "
            f"reservation of {required_minutes} batch-wall minutes"
        )


def _assert_run_open(run_record: dict[str, Any]) -> None:
    if run_record.get("ended_at") is not None:
        raise RuntimeError("stopped development run is immutable and cannot be resumed")


def _admission_failure_code(message: str) -> str:
    normalized = message.casefold()
    if "exceeds its direct" in normalized or "cap" in normalized:
        return "DEVELOPMENT_CONTRACT_CAP_EXCEEDED"
    if "trace" in normalized or "web call" in normalized:
        return "DEVELOPMENT_TRACE_ADMISSION_FAILED"
    if "return" in normalized or "dossier" in normalized or "research" in normalized:
        return "DEVELOPMENT_RETURN_ADMISSION_FAILED"
    return "DEVELOPMENT_STAGE_ADMISSION_FAILED"


def _record_admission_failure(
    api: Any,
    run_dir: Path,
    *,
    stage: str,
    error: Exception,
) -> None:
    """Stop at the last real checkpoint without fabricating stage telemetry."""
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = api.read_jsonl(manifest_path)
    states = [
        record.get("state")
        for record in records
        if record.get("record_type") == "checkpoint"
    ]
    required_state = (
        "level2_cohort_sealed"
        if stage == "level2"
        else "fact_closure_cohort_sealed"
    )
    run_record = records[0]
    if states[-1:] != [required_state] or run_record.get("ended_at") is not None:
        return
    last_checkpoint = next(
        record
        for record in reversed(records)
        if record.get("record_type") == "checkpoint"
    )
    last_checkpoint_at = datetime.fromisoformat(last_checkpoint["occurred_at"])
    stopped_at = api.now()
    if _utc(stopped_at) <= _utc(last_checkpoint_at):
        raise RuntimeError("actual stage stop time does not follow the last checkpoint")

    arm = run_record.get("arm")
    agent_prefix = "baseline" if arm == "matched_baseline" else "shadow"
    launch_path = run_dir / f"{agent_prefix}_{stage}_launch.json"
    evidence_files: list[dict[str, str]] = []
    causal_traces: list[dict[str, str]] = []
    launch: dict[str, Any] = {}
    launch_items: list[dict[str, Any]] = []
    if launch_path.is_file() and not launch_path.is_symlink():
        evidence_files.append(
            {
                "path": launch_path.relative_to(run_dir).as_posix(),
                "sha256": api.sha256(launch_path),
            }
        )
        try:
            launch = json.loads(launch_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            launch = {}
        batches = launch.get("batches") if isinstance(launch, dict) else None
        if isinstance(batches, list):
            launch_items = list(
                candidate
                for batch in batches
                if isinstance(batch, list)
                for candidate in batch
                if isinstance(candidate, dict)
            )
            trace_task_names = [
                item["task_name"]
                for item in launch_items
                if isinstance(item.get("task_name"), str)
                and item["task_name"]
            ]
            try:
                source_traces = (
                    api.find_trace_paths(trace_task_names) if trace_task_names else {}
                )
            except RuntimeError:
                # Ambiguous or duplicate task identities are not safe evidence.
                source_traces = {}
            for item in launch_items:
                for field in ("allocation_precommit_path", "output_path"):
                    raw_path = item.get(field)
                    if not isinstance(raw_path, str):
                        continue
                    path = Path(raw_path)
                    if path.is_file() and not path.is_symlink():
                        try:
                            relative = path.resolve().relative_to(run_dir).as_posix()
                        except ValueError:
                            continue
                        evidence_files.append(
                            {"path": relative, "sha256": api.sha256(path)}
                        )

                agent_id = item.get("agent_id")
                task_name = item.get("task_name")
                if not isinstance(agent_id, str) or not isinstance(task_name, str):
                    continue
                source_trace = source_traces.get(task_name)
                if source_trace is None or not source_trace.is_file() or source_trace.is_symlink():
                    continue
                trace_copy = run_dir / "failure_evidence" / stage / f"{agent_id}.jsonl"
                if not trace_copy.exists():
                    api.write_exclusive(trace_copy, source_trace.read_bytes())
                relative = trace_copy.relative_to(run_dir).as_posix()
                digest = api.sha256(trace_copy)
                evidence_files.append({"path": relative, "sha256": digest})
                causal_traces.append(
                    {
                        "agent_id": agent_id,
                        "trace_task_name": task_name,
                        "path": relative,
                        "sha256": digest,
                    }
                )

    for field in ("pre_stage_manifest", "pre_stage_ledger"):
        item = launch.get(field) if isinstance(launch, dict) else None
        raw_path = item.get("path") if isinstance(item, dict) else None
        digest = item.get("sha256") if isinstance(item, dict) else None
        if isinstance(raw_path, str) and isinstance(digest, str):
            path = run_dir / raw_path
            if path.is_file() and not path.is_symlink() and api.sha256(path) == digest:
                evidence_files.append({"path": raw_path, "sha256": digest})

    meter_root = run_dir / "live_metering"
    if meter_root.is_dir() and not meter_root.is_symlink():
        for path in meter_root.glob(f"{agent_prefix}_{stage}_batch_*.jsonl"):
            if path.is_file() and not path.is_symlink():
                evidence_files.append(
                    {
                        "path": path.relative_to(run_dir).as_posix(),
                        "sha256": api.sha256(path),
                    }
                )

    canonical_candidates: list[Path] = []
    dossier_root = run_dir / f"{agent_prefix}_{stage}"
    if dossier_root.is_dir() and not dossier_root.is_symlink():
        canonical_candidates.extend(path for path in dossier_root.rglob("*") if path.is_file())
    for root_name in ("runtime_traces", "trace_attestations"):
        root = run_dir / root_name
        if root.is_dir() and not root.is_symlink():
            canonical_candidates.extend(
                path
                for path in root.glob(f"{agent_prefix}-{'level2' if stage == 'level2' else 'fact-closure'}-*.json*")
                if path.is_file() and not path.is_symlink()
            )
    report_path = run_dir / ("03a_level2_research.md" if stage == "level2" else "04_fact_closure.md")
    if report_path.is_file() and not report_path.is_symlink():
        canonical_candidates.append(report_path)
    pre_ledger = launch.get("pre_stage_ledger") if isinstance(launch, dict) else None
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    if (
        isinstance(pre_ledger, dict)
        and ledger_path.is_file()
        and api.sha256(ledger_path) != pre_ledger.get("sha256")
    ):
        canonical_candidates.append(ledger_path)
    materialized_stage_artifacts = sorted(
        (
            {
                "path": path.relative_to(run_dir).as_posix(),
                "sha256": api.sha256(path),
            }
            for path in set(canonical_candidates)
        ),
        key=lambda item: item["path"],
    )

    future_artifacts = []
    if stage == "level2":
        future_names = (
            "02d_fact_closure_candidates.json",
            "04_fact_closure.md",
            "00c_pre_freeze_manifest_snapshot.jsonl",
        )
    else:
        future_names = ("00c_pre_freeze_manifest_snapshot.jsonl",)
    for name in future_names:
        path = run_dir / name
        if path.exists() or path.is_symlink():
            future_artifacts.append(name)
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
        future_artifacts.extend(
            path.relative_to(run_dir).as_posix()
            for path in run_dir.glob(pattern)
            if path.exists() or path.is_symlink()
        )
    if stage == "level2" and arm == "matched_baseline":
        child_path = run_dir / api.CHILD_RELATIVE_PATH
        if child_path.exists() or child_path.is_symlink():
            future_artifacts.append(api.CHILD_RELATIVE_PATH)
    later_states = {
        "level2": {"level2_complete", "fact_closure_cohort_sealed", "closure_complete", "frozen", "complete"},
        "fact_closure": {"closure_complete", "frozen", "complete"},
    }[stage]
    future_artifacts.extend(
        f"checkpoint:{record.get('state')}"
        for record in records
        if record.get("record_type") == "checkpoint" and record.get("state") in later_states
    )

    receipt = {
        "schema": "zt1-development-admission-failure-v2",
        "run_id": run_record.get("run_id"),
        "scope_id": run_record.get("scope_id"),
        "stage": stage,
        "primary_cause": {
            "code": _admission_failure_code(str(error)),
            "exception_type": type(error).__name__,
            "message": str(error),
        },
        "stopped_at": api.iso(stopped_at),
        "last_reached_checkpoint": required_state,
        "pre_stage_manifest": launch.get("pre_stage_manifest"),
        "pre_stage_ledger": launch.get("pre_stage_ledger"),
        "preserved_evidence": sorted(
            {item["path"]: item for item in evidence_files}.values(),
            key=lambda item: item["path"],
        ),
        "causal_traces": sorted(causal_traces, key=lambda item: item["agent_id"]),
        "materialized_stage_artifacts": materialized_stage_artifacts,
        "future_lifecycle_artifacts": sorted(set(future_artifacts)),
        "telemetry_reconstruction_performed": False,
    }
    receipt_path = run_dir / f"10_{stage}_admission_failure.json"
    api.write_exclusive(receipt_path, api.json_bytes(receipt))
    run_record["ended_at"] = api.iso(stopped_at)
    run_record["failure_receipt_path"] = receipt_path.relative_to(run_dir).as_posix()
    run_record["failure_receipt_sha256"] = api.sha256(receipt_path)
    # The lifecycle remains at the final real checkpoint.  No synthetic
    # failed checkpoint, allocation, dossier, child, or seal is invented.
    api.write_replace(manifest_path, api.jsonl_bytes(records))


def _packet(
    api: Any,
    *,
    run_dir: Path,
    seed: str,
    scope_id: str,
    arm: str,
    stage: str,
    agent_id: str,
    concept_id: str,
    output_path: Path,
    packet_relative: str,
    query_cap: int,
    caps: dict[str, int],
    prose_minimum: int,
    prose_maximum: int,
    prose_minimum_per_section: int,
    candidate_input: dict[str, Any],
) -> str:
    dossier_field = "frozen_dossier" if stage == "fact_closure" else "dossier"
    section_example = {key: "substantive neutral prose" for key in api.DOSSIER_KEYS}
    stage_name = "fact closure" if stage == "fact_closure" else "Level-2 development"
    contradiction_rule = (
        "If public evidence contradicts an indispensable premise, record status "
        "`contradicted`; no replacement is permitted."
        if stage == "fact_closure"
        else "Preserve contradictions and unresolved assumptions explicitly."
    )
    return f"""# Immutable Candidate-Owned {stage_name.title()} Packet

## Identity And Allocation

- Scope: `{scope_id}`
- Arm: `{arm}`
- Stage: `{stage}`
- Seed: `{seed}`
- Agent ID: `{agent_id}`
- Role: `{'fact_closure_researcher' if stage == 'fact_closure' else 'level2_researcher'}`
- Assigned/output candidate: `{concept_id}`
- Required return path: `{output_path}`
- Query opportunity: up to `{query_cap}` decision-relevant public web calls.
- Hard admission ceilings: `{caps['uncached_input_tokens']}` uncached input tokens, `{caps['output_tokens']}` output tokens, and `{caps['elapsed_minutes']}` elapsed minutes.
- Counted persuasive dossier prose: `{prose_minimum}`–`{prose_maximum}` words across the first eight standardized sections, with at least `{prose_minimum_per_section}` words in every one of those sections. The title, headings, Evidence And Sources section, source ledger, telemetry, and machine metadata do not count.

Read exactly `{packet_relative}` and no other file, using one exact `sed -n '1,9999p' {str((output_path.parents[1] / packet_relative).resolve())}` command. Research only what is useful for this candidate. Do not consume unused query capacity, add filler prose, contact a person or chatbot, execute a private proof, purchase anything, route, regenerate, or invoke downstream judgment. {contradiction_rule}

The dossier must neutrally cover customer loss and payer evidence; proposed transaction and paid trigger; acquisition route; incumbent substitute and route-around; unit economics with sensitivity; control point or compounding asset; execution dependencies and cheapest proof; decision-critical unknowns and contradictions; and evidence and sources. Keep source/trace metadata outside persuasive section bodies.

Return exactly one JSON object with `agent_id`, singleton `assigned_ids`, singleton `output_ids`, singleton `files_read`, `concept_id`, `research`, `cheapest_resolving_test`, and `{dossier_field}`. `files_read` is exactly `[{json.dumps(packet_relative)}]`. `research` contains one entry per actual web call, in trace order, and may contain fewer than `{query_cap}` entries. Every `opened_url` must occur verbatim in that exact call's returned tool output; never infer or rewrite a URL. Every entry uses exactly `query_text`, `opened_url`, `source_title`, `source_date`, `proposition`, `status`, and `contradiction`; allowed status values are verified, interpreted, counsel-required, unknown, and contradicted. Use this exact dossier shape:

```json
{json.dumps(section_example, indent=2)}
```

All strings must be nonempty. Create only the required return file after research is complete.

{api.bounded_return_instruction(output_path, run_dir)}

## Candidate Input

```json
{json.dumps(candidate_input, indent=2, sort_keys=True)}
```
"""


def _prepare(
    api: Any,
    run_dir: Path,
    *,
    stage: str,
    selected_ids: list[str],
    selected_at: str,
    inputs: dict[str, dict[str, Any]],
    selection_categories: dict[str, str] | None = None,
) -> None:
    seed = api.authenticated_run_seed(run_dir)
    count = 12 if stage == "level2" else 6
    query_cap = 12 if stage == "level2" else 8
    caps = api.LEVEL2_CAPS if stage == "level2" else api.FACT_CLOSURE_CAPS
    prose_contract = api.development_contract()["dossier_prose_word_ranges"][
        "level2" if stage == "level2" else "frozen"
    ]
    prose_minimum = prose_contract["minimum"]
    prose_maximum = prose_contract["maximum"]
    prose_minimum_per_section = prose_contract["minimum_per_section"]
    if len(selected_ids) != count or len(set(selected_ids)) != count:
        raise RuntimeError(f"{stage} requires exactly {count} unique sealed candidates")
    run_record = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")[0]
    _assert_run_open(run_record)
    arm = run_record.get("arm")
    scope_id = run_record.get("scope_id")
    if arm not in {"matched_baseline", "shadow"} or not isinstance(scope_id, str):
        raise RuntimeError("isolated matched development requires a typed arm and scope")
    agent_prefix = "baseline" if arm == "matched_baseline" else "shadow"
    id_prefix = "B" if arm == "matched_baseline" else "S"
    batches = (count + 2) // 3
    required_minutes = (
        4 * api.LEVEL2_CAPS["elapsed_minutes"]
        + 2 * api.FACT_CLOSURE_CAPS["elapsed_minutes"]
        if stage == "level2"
        else 2 * api.FACT_CLOSURE_CAPS["elapsed_minutes"]
    )
    _remaining_development_fit(api, run_record, required_minutes)

    launch_agents: list[dict[str, Any]] = []
    stage_slug = "level2" if stage == "level2" else "fact-closure"
    allocation_slug = "L2" if stage == "level2" else "FC"
    role = "level2_researcher" if stage == "level2" else "fact_closure_researcher"
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    baseline_dir = run_dir / "stage_admission_baselines"
    manifest_baseline = baseline_dir / f"{agent_prefix}_{stage}_manifest.jsonl"
    ledger_baseline = baseline_dir / f"{agent_prefix}_{stage}_ledger.jsonl"
    api.write_exclusive(manifest_baseline, manifest_path.read_bytes())
    api.write_exclusive(ledger_baseline, ledger_path.read_bytes())
    for index, concept_id in enumerate(selected_ids, 1):
        agent_id = f"{agent_prefix}-{stage_slug}-{index:02d}"
        packet_path = run_dir / "context" / f"{agent_id}.md"
        output_path = run_dir / "agent_returns" / f"{agent_id}.json"
        packet_relative = packet_path.relative_to(run_dir).as_posix()
        output_relative = output_path.relative_to(run_dir).as_posix()
        allocation_id = f"ALLOC-{id_prefix}-{allocation_slug}-{index:03d}"
        query_ids = [
            f"Q-{id_prefix}-{allocation_slug}-{index:03d}-{offset:02d}"
            for offset in range(1, query_cap + 1)
        ]
        evidence_ids = [
            f"EV-{id_prefix}-{allocation_slug}-{index:03d}-{offset:02d}"
            for offset in range(1, query_cap + 1)
        ]
        packet_text = _packet(
            api,
            run_dir=run_dir,
            seed=seed,
            scope_id=scope_id,
            arm=arm,
            stage=stage,
            agent_id=agent_id,
            concept_id=concept_id,
            output_path=output_path,
            packet_relative=packet_relative,
            query_cap=query_cap,
            caps=caps,
            prose_minimum=prose_minimum,
            prose_maximum=prose_maximum,
            prose_minimum_per_section=prose_minimum_per_section,
            candidate_input=inputs[concept_id],
        )
        api.write_exclusive(packet_path, packet_text.encode("utf-8"))
        api.assert_bounded_return_packet(packet_path, output_path, run_dir)
        created_at = api.iso(api.now())
        precommit = {
            "schema": "zt1-candidate-allocation-precommit-v2",
            "scope_id": scope_id,
            "arm": arm,
            "stage": stage,
            "agent_id": agent_id,
            "role": role,
            "seed": seed,
            "entity_id": concept_id,
            "assigned_ids": [concept_id],
            "output_ids": [concept_id],
            "allocation_id": allocation_id,
            "query_cap": query_cap,
            "query_ids": query_ids,
            "evidence_ids": evidence_ids,
            "batch_index": (index - 1) // 3 + 1,
            "created_at": created_at,
            "selected_at": selected_at,
            "metering_basis": "trace_derived_exact",
            "packet_path": packet_relative,
            "packet_sha256": api.sha256(packet_path),
            "output_path": output_relative,
            "model": api.MODEL,
            "reasoning_effort": api.REASONING,
            "trace_task_name": api.trace_task_name(run_dir, agent_id),
            "budget": dict(caps),
            "live_stop_threshold": dict(api.DEVELOPMENT_LIVE_STOP_THRESHOLDS[stage]),
            "meter_poll_interval_milliseconds": api.DEVELOPMENT_METERING_MONITOR[
                "poll_interval_milliseconds"
            ],
        }
        if stage == "level2" and arm == "shadow":
            if selection_categories is None or concept_id not in selection_categories:
                raise RuntimeError("shadow Level-2 preparation requires a sealed category per candidate")
            precommit["selection_category"] = selection_categories[concept_id]
        precommit_path = run_dir / "allocation_precommits" / f"{allocation_id}.json"
        api.write_exclusive(precommit_path, api.json_bytes(precommit))
        api.assert_bounded_return_precommit(
            packet_path,
            output_path,
            run_dir,
            precommit_path,
            expected_agent_id=agent_id,
            expected_stage=stage,
        )
        launch_agents.append(
            {
                "agent_id": agent_id,
                "entity_id": concept_id,
                "batch_index": precommit["batch_index"],
                "packet_path": str(packet_path),
                "packet_sha256": precommit["packet_sha256"],
                "output_path": str(output_path),
                "allocation_precommit_path": str(precommit_path),
                "task_name": precommit["trace_task_name"],
            }
        )
    batch_records = _chunks(launch_agents, 3)
    launch = {
        "schema": "zt1-isolated-development-launch-v2",
        "stage": stage,
        "scope_id": scope_id,
        "arm": arm,
        "seed": seed,
        "model": api.MODEL,
        "reasoning_effort": api.REASONING,
        "max_concurrency": 3,
        "candidate_count": count,
        "pre_stage_manifest": {
            "path": manifest_baseline.relative_to(run_dir).as_posix(),
            "sha256": api.sha256(manifest_baseline),
        },
        "pre_stage_ledger": {
            "path": ledger_baseline.relative_to(run_dir).as_posix(),
            "sha256": api.sha256(ledger_baseline),
        },
        "live_metering": {
            "poll_interval_milliseconds": api.DEVELOPMENT_METERING_MONITOR[
                "poll_interval_milliseconds"
            ],
            "required_action": "interrupt_candidate_agent_and_fail_stage_admission",
        },
        "batches": batch_records,
    }
    launch_path = run_dir / f"{agent_prefix}_{stage}_launch.json"
    api.write_exclusive(launch_path, api.json_bytes(launch))
    print(str(launch_path))


def prepare_baseline_level2(api: Any, run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    seed = api.authenticated_run_seed(run_dir)
    records = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    if records[0].get("arm") != "matched_baseline":
        raise RuntimeError("baseline Level-2 preparation requires matched_baseline arm")
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != [
        "registered",
        "raw_frozen",
        "history_frozen",
        "mapped",
        "cluster_audited",
        "level2_cohort_sealed",
    ]:
        raise RuntimeError("Level-2 preparation requires the exact sealed cohort prefix")
    selection = json.loads((run_dir / "02c_baseline_level2_cohort.json").read_text(encoding="utf-8"))
    if selection.get("seed") != seed:
        raise RuntimeError("sealed baseline Level-2 cohort seed differs from registration")
    selected_ids = selection.get("candidate_ids")
    level1 = json.loads((run_dir / "agent_returns" / "baseline-level1-01.json").read_text(encoding="utf-8"))
    cards = api.validate_baseline_level1(level1)
    cards_by_id = {item["concept_id"]: item for item in cards}
    if not isinstance(selected_ids, list) or any(concept_id not in cards_by_id for concept_id in selected_ids):
        raise RuntimeError("sealed baseline Level-2 cohort is invalid")
    _prepare(
        api,
        run_dir,
        stage="level2",
        selected_ids=selected_ids,
        selected_at=selection["selected_at"],
        inputs={concept_id: cards_by_id[concept_id] for concept_id in selected_ids},
    )


def prepare_shadow_level2(
    api: Any,
    run_dir: Path,
    *,
    cohort_file: Path,
    inputs_file: Path,
) -> None:
    run_dir = run_dir.resolve()
    seed = api.authenticated_run_seed(run_dir)
    records = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    if records[0].get("arm") != "shadow":
        raise RuntimeError("shadow Level-2 preparation requires shadow arm")
    states = [
        record.get("state")
        for record in records
        if record.get("record_type") == "checkpoint"
    ]
    if states[-1:] != ["level2_cohort_sealed"]:
        raise RuntimeError("shadow Level-2 preparation requires its sealed cohort")
    cohort_file = cohort_file.resolve()
    inputs_file = inputs_file.resolve()
    for path in (cohort_file, inputs_file):
        try:
            path.relative_to(run_dir)
        except ValueError as exc:
            raise RuntimeError("shadow Level-2 inputs must be run-owned") from exc
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("shadow Level-2 input is missing or unsafe")
    last_checkpoint = next(
        record
        for record in reversed(records)
        if record.get("record_type") == "checkpoint"
    )
    bound_artifacts = {
        item.get("path"): item.get("sha256")
        for item in last_checkpoint.get("artifacts", [])
        if isinstance(item, dict)
    }
    cohort_relative = cohort_file.relative_to(run_dir).as_posix()
    inputs_relative = inputs_file.relative_to(run_dir).as_posix()
    if (
        bound_artifacts.get(cohort_relative) != api.sha256(cohort_file)
        or bound_artifacts.get(inputs_relative) != api.sha256(inputs_file)
    ):
        raise RuntimeError("shadow Level-2 cohort and input cards must both be checkpoint hash-bound")
    cohort = json.loads(cohort_file.read_text(encoding="utf-8"))
    if cohort.get("seed") != seed:
        raise RuntimeError("sealed shadow Level-2 cohort seed differs from registration")
    selected_ids = cohort.get("candidate_ids")
    selected_at = cohort.get("selected_at")
    selection_categories = cohort.get("selection_categories")
    raw_inputs = json.loads(inputs_file.read_text(encoding="utf-8"))
    cards = raw_inputs.get("cards") if isinstance(raw_inputs, dict) else None
    if not isinstance(cards, list):
        raise RuntimeError("shadow Level-2 inputs require a cards array")
    cards_by_id = {
        item.get("concept_id"): item
        for item in cards
        if isinstance(item, dict) and isinstance(item.get("concept_id"), str)
    }
    if (
        not isinstance(selected_ids, list)
        or not isinstance(selected_at, str)
        or not isinstance(selection_categories, dict)
        or set(selection_categories) != set(selected_ids)
        or any(concept_id not in cards_by_id for concept_id in selected_ids)
    ):
        raise RuntimeError("sealed shadow Level-2 cohort is not backed by input cards")
    required_categories = {
        "main_provisional": 6,
        "selector_or_challenger": 3,
        "rejected": 1,
        "near_cutoff": 1,
        "singleton": 1,
    }
    observed_categories = {
        category: sum(value == category for value in selection_categories.values())
        for category in required_categories
    }
    if observed_categories != required_categories or any(
        value not in required_categories for value in selection_categories.values()
    ):
        raise RuntimeError("sealed shadow Level-2 categories must use exact 6/3/1/1/1 opportunity")
    _prepare(
        api,
        run_dir,
        stage="level2",
        selected_ids=selected_ids,
        selected_at=selected_at,
        inputs={concept_id: cards_by_id[concept_id] for concept_id in selected_ids},
        selection_categories=selection_categories,
    )


def _prepare_fact_closure(api: Any, run_dir: Path, *, expected_arm: str) -> None:
    run_dir = run_dir.resolve()
    seed = api.authenticated_run_seed(run_dir)
    records = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    if records[0].get("arm") != expected_arm:
        raise RuntimeError(f"fact closure requires {expected_arm} arm")
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states[-1:] != ["fact_closure_cohort_sealed"]:
        raise RuntimeError("fact-closure preparation requires the sealed closure cohort")
    closure = json.loads((run_dir / "02d_fact_closure_candidates.json").read_text(encoding="utf-8"))
    if closure.get("seed") != seed:
        raise RuntimeError("sealed fact-closure cohort seed differs from registration")
    selected_ids = closure.get("candidate_ids")
    ledger = api.read_jsonl(run_dir / "02b_raw_to_direction_ledger.jsonl")
    level2_by_id = {
        record["concept_id"]: record
        for record in ledger
        if record.get("record_type") == "level2"
        and record.get("development_status") == "complete"
    }
    if not isinstance(selected_ids, list) or any(concept_id not in level2_by_id for concept_id in selected_ids):
        raise RuntimeError("sealed closure cohort is not backed by complete Level-2 dossiers")
    inputs: dict[str, dict[str, Any]] = {}
    agent_prefix = "baseline" if expected_arm == "matched_baseline" else "shadow"
    for concept_id in selected_ids:
        record = level2_by_id[concept_id]
        index = next(
            offset
            for offset in range(1, 13)
            if (run_dir / "agent_returns" / f"{agent_prefix}-level2-{offset:02d}.json").exists()
            and json.loads(
                (run_dir / "agent_returns" / f"{agent_prefix}-level2-{offset:02d}.json").read_text(encoding="utf-8")
            ).get("concept_id") == concept_id
        )
        prior_return = json.loads(
            (run_dir / "agent_returns" / f"{agent_prefix}-level2-{index:02d}.json").read_text(encoding="utf-8")
        )
        inputs[concept_id] = {
            "concept_id": concept_id,
            "level2_dossier": (run_dir / record["artifact_path"]).read_text(encoding="utf-8"),
            "level2_research": prior_return["research"],
            "closure_instruction": "Close or bound the most decision-critical remaining public uncertainty without replacing the sealed candidate.",
        }
    _prepare(
        api,
        run_dir,
        stage="fact_closure",
        selected_ids=selected_ids,
        selected_at=closure["selected_at"],
        inputs=inputs,
    )


def prepare_baseline_fact_closure(api: Any, run_dir: Path) -> None:
    _prepare_fact_closure(api, run_dir, expected_arm="matched_baseline")


def prepare_shadow_fact_closure(api: Any, run_dir: Path) -> None:
    _prepare_fact_closure(api, run_dir, expected_arm="shadow")


def _validate_return(
    api: Any,
    *,
    stage: str,
    precommit: dict[str, Any],
    output: Any,
    trace: dict[str, Any],
    packet_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    dossier_field = "frozen_dossier" if stage == "fact_closure" else "dossier"
    expected_fields = RETURN_FIELDS | {dossier_field}
    entity_id = precommit["entity_id"]
    agent_id = precommit["agent_id"]
    if not isinstance(output, dict) or set(output) != expected_fields:
        raise RuntimeError(f"{agent_id} return has an invalid closed schema")
    if (
        output["agent_id"] != agent_id
        or output["assigned_ids"] != [entity_id]
        or output["output_ids"] != [entity_id]
        or output["concept_id"] != entity_id
        or output["files_read"] != [precommit["packet_path"]]
    ):
        raise RuntimeError(f"{agent_id} does not reconcile its singleton assignment")
    if not isinstance(output["cheapest_resolving_test"], str) or not output["cheapest_resolving_test"].strip():
        raise RuntimeError(f"{agent_id} lacks a cheapest resolving test")
    research = output["research"]
    if not isinstance(research, list) or not 1 <= len(research) <= precommit["query_cap"]:
        raise RuntimeError(f"{agent_id} must use between one and its useful-query cap")
    if len(research) != len(trace["web_calls"]):
        raise RuntimeError(f"{agent_id} research ledger and exact web-call trace differ")
    for item in research:
        if not isinstance(item, dict) or set(item) != RESEARCH_FIELDS:
            raise RuntimeError(f"{agent_id} research entry has an invalid closed schema")
        _exact_nonempty_strings(item, RESEARCH_FIELDS, f"{agent_id} research entry")
        if item["status"] not in ALLOWED_EVIDENCE_STATUSES:
            raise RuntimeError(f"{agent_id} research entry has an invalid evidence status")
    dossier = output[dossier_field]
    if not isinstance(dossier, dict) or list(dossier) != api.DOSSIER_KEYS:
        raise RuntimeError(f"{agent_id} dossier must use the exact standardized section order")
    _exact_nonempty_strings(dossier, set(api.DOSSIER_KEYS), f"{agent_id} dossier")
    _validate_dossier_depth(
        api, stage=stage, dossier=dossier, agent_id=agent_id
    )

    api.assert_single_packet_read(trace, packet_path, output_path)
    start = api.parse_timestamp(trace["started_at"]).astimezone(api.LOCAL_TZ)
    end = api.parse_timestamp(trace["ended_at"]).astimezone(api.LOCAL_TZ)
    created_at = datetime.fromisoformat(precommit["created_at"])
    selected_at = datetime.fromisoformat(precommit["selected_at"])
    completed_at = datetime.fromisoformat(api.apply_patch_completion_time(trace, output_path))
    if not (
        _utc(selected_at)
        < _utc(created_at)
        < _utc(start)
        <= _utc(completed_at)
        <= _utc(end)
    ):
        raise RuntimeError(f"{agent_id} selection/allocation/return/trace chronology is invalid")
    resources = {
        "uncached_input_tokens": trace["uncached_input_tokens"],
        "output_tokens": trace["output_tokens"],
        "elapsed_microseconds": api.elapsed_microseconds(start, end),
    }
    caps = precommit["budget"]
    if resources["uncached_input_tokens"] > caps["uncached_input_tokens"]:
        raise RuntimeError(f"{agent_id} exceeds its direct uncached-input cap")
    if resources["output_tokens"] > caps["output_tokens"]:
        raise RuntimeError(f"{agent_id} exceeds its direct output cap")
    if resources["elapsed_microseconds"] > caps["elapsed_minutes"] * 60_000_000:
        raise RuntimeError(f"{agent_id} exceeds its direct elapsed-time cap")
    deadline = datetime.fromisoformat(api.read_jsonl(packet_path.parents[1] / "00a_context_and_resource_manifest.jsonl")[0]["deadline_at"])
    if _utc(end) > _utc(deadline):
        raise RuntimeError(f"{agent_id} ended after the actual run deadline")
    for research_item, call in zip(research, trace["web_calls"]):
        actual_query = api.normalize_query_from_call(call, research_item["opened_url"])
        if _normal(actual_query) != _normal(research_item["query_text"]):
            raise RuntimeError(f"{agent_id} research text is not trace-derived")
        call_id = call.get("payload", {}).get("call_id")
        if not isinstance(call_id, str) or not api.call_output_contains_url(
            trace, call_id, research_item["opened_url"]
        ):
            raise RuntimeError(
                f"{agent_id} declared source URL is absent from its exact tool output"
            )
    return {
        "precommit": precommit,
        "output": output,
        "trace": trace,
        "start": start,
        "end": end,
        "completed_at": api.iso(completed_at),
        "resources": resources,
        "dossier_text": _render_dossier(
            api,
            entity_id,
            dossier,
            arm=precommit["arm"],
            stage=stage,
        ),
    }


def _assert_batch_execution(admissions: list[dict[str, Any]]) -> None:
    by_batch: dict[int, list[dict[str, Any]]] = {}
    for admission in admissions:
        by_batch.setdefault(admission["precommit"]["batch_index"], []).append(admission)
    if any(len(values) > 3 for values in by_batch.values()):
        raise RuntimeError("development launch exceeded three agents in one batch")
    for batch_index in range(2, max(by_batch, default=0) + 1):
        previous_end = max(
            (_utc(item["end"]) for item in by_batch[batch_index - 1])
        )
        current_start = min(
            (_utc(item["start"]) for item in by_batch[batch_index])
        )
        if current_start <= previous_end:
            raise RuntimeError("a development batch started before the prior batch fully ended")


def meter_batch_snapshot(
    api: Any,
    run_dir: Path,
    *,
    stage: str,
    batch_index: int,
    trace_paths: dict[str, Path | None] | None = None,
) -> dict[str, Any]:
    """Return the exact live interrupt decision for one dispatched batch.

    The blocking controller calls this once per contract poll interval and the
    root immediately interrupts every task named in ``interrupt_task_names``.
    Final integration still verifies the higher hard admission ceilings.
    """
    run_dir = run_dir.resolve()
    records = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    _assert_run_open(records[0])
    arm = records[0].get("arm")
    prefix = "baseline" if arm == "matched_baseline" else "shadow"
    launch_path = run_dir / f"{prefix}_{stage}_launch.json"
    launch = json.loads(launch_path.read_text(encoding="utf-8"))
    batches = launch.get("batches") if isinstance(launch, dict) else None
    if (
        not isinstance(batch_index, int)
        or isinstance(batch_index, bool)
        or batch_index < 1
        or not isinstance(batches, list)
        or batch_index > len(batches)
    ):
        raise RuntimeError("live metering requires one valid one-based batch index")
    batch = batches[batch_index - 1]
    if not isinstance(batch, list) or not 1 <= len(batch) <= 3:
        raise RuntimeError("live metering batch violates the at-most-three launch plan")
    precommits = [
        json.loads(
            Path(launch_item["allocation_precommit_path"]).read_text(encoding="utf-8")
        )
        for launch_item in batch
    ]
    for launch_item, precommit in zip(batch, precommits):
        if precommit.get("trace_task_name") != launch_item.get("task_name"):
            raise RuntimeError("live meter task identity differs from its precommit")
    task_names = [precommit["trace_task_name"] for precommit in precommits]
    if trace_paths is None:
        usage_by_task = api.partial_trace_usages(task_names)
    else:
        if set(trace_paths) != set(task_names):
            raise RuntimeError("live meter trace-path cache differs from its batch tasks")
        usage_by_task = api.partial_trace_usages_from_paths(trace_paths)
    agents: list[dict[str, Any]] = []
    interrupt_task_names: list[str] = []
    for precommit in precommits:
        usage = usage_by_task[precommit["trace_task_name"]]
        threshold = precommit["live_stop_threshold"]
        reasons: list[str] = []
        if usage["uncached_input_tokens"] >= threshold["uncached_input_tokens"]:
            reasons.append("uncached_input_tokens")
        if usage["output_tokens"] >= threshold["output_tokens"]:
            reasons.append("output_tokens")
        if usage["elapsed_microseconds"] >= threshold["elapsed_minutes"] * 60_000_000:
            reasons.append("elapsed_microseconds")
        if reasons and usage["status"] != "complete":
            interrupt_task_names.append(precommit["trace_task_name"])
        agents.append(
            {
                "agent_id": precommit["agent_id"],
                "entity_id": precommit["entity_id"],
                "task_name": precommit["trace_task_name"],
                "status": usage["status"],
                "measured_at": usage["measured_at"],
                "resources": {
                    "uncached_input_tokens": usage["uncached_input_tokens"],
                    "output_tokens": usage["output_tokens"],
                    "elapsed_microseconds": usage["elapsed_microseconds"],
                },
                "live_stop_reasons": reasons,
            }
        )
    snapshot = {
        "schema": "zt1-development-live-meter-snapshot-v2",
        "scope_id": records[0].get("scope_id"),
        "arm": arm,
        "stage": stage,
        "batch_index": batch_index,
        "polled_at": api.iso(api.now()),
        "poll_interval_milliseconds": api.DEVELOPMENT_METERING_MONITOR[
            "poll_interval_milliseconds"
        ],
        "agents": agents,
        "interrupt_task_names": interrupt_task_names,
        "stage_admission_must_fail": bool(interrupt_task_names),
    }
    meter_path = (
        run_dir
        / "live_metering"
        / f"{prefix}_{stage}_batch_{batch_index:02d}.jsonl"
    )
    api.ensure_safe_directory(meter_path.parent)
    with meter_path.open("ab") as handle:
        handle.write(api.jsonl_bytes([snapshot]))
        handle.flush()
    return snapshot


def monitor_batch(
    api: Any, run_dir: Path, *, stage: str, batch_index: int
) -> dict[str, Any]:
    """Block on a real one-second meter loop until completion or interruption.

    The root starts this controller before dispatching the batch, then waits on
    its process.  An ``interrupt_required`` result is the exact collaboration
    interrupt channel: the root immediately interrupts every task in
    ``abort_batch_task_names`` and does not admit the stage; the narrower
    ``interrupt_task_names`` identifies the threshold-crossing candidates.
    """
    run_dir = run_dir.resolve()
    records = api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    _assert_run_open(records[0])
    prefix = "baseline" if records[0].get("arm") == "matched_baseline" else "shadow"
    arm = records[0].get("arm")
    scope_id = records[0].get("scope_id")
    seed = api.authenticated_run_seed(run_dir)
    launch = json.loads(
        (run_dir / f"{prefix}_{stage}_launch.json").read_text(encoding="utf-8")
    )
    batches = launch.get("batches")
    expected_candidate_count = 12 if stage == "level2" else 6
    if (
        stage not in {"level2", "fact_closure"}
        or not isinstance(launch, dict)
        or launch.get("schema") != "zt1-isolated-development-launch-v2"
        or launch.get("stage") != stage
        or launch.get("arm") != arm
        or launch.get("scope_id") != scope_id
        or launch.get("seed") != seed
        or launch.get("candidate_count") != expected_candidate_count
        or launch.get("max_concurrency") != 3
        or not isinstance(batches, list)
        or len(batches) != expected_candidate_count // 3
        or not isinstance(batch_index, int)
        or isinstance(batch_index, bool)
        or not 1 <= batch_index <= len(batches)
    ):
        raise RuntimeError("batch controller requires one valid launch batch")
    batch = batches[batch_index - 1]
    if not isinstance(batch, list) or not 1 <= len(batch) <= 3:
        raise RuntimeError("batch controller launch batch must contain one to three agents")
    remaining_stage_batches = len(batches) - batch_index + 1
    required_minutes = remaining_stage_batches * (
        api.LEVEL2_CAPS["elapsed_minutes"]
        if stage == "level2"
        else api.FACT_CLOSURE_CAPS["elapsed_minutes"]
    )
    if stage == "level2":
        required_minutes += 2 * api.FACT_CLOSURE_CAPS["elapsed_minutes"]
    _remaining_development_fit(api, records[0], required_minutes)
    stage_slug = "level2" if stage == "level2" else "fact-closure"
    allocation_slug = "L2" if stage == "level2" else "FC"
    id_prefix = "B" if arm == "matched_baseline" else "S"
    role = "level2_researcher" if stage == "level2" else "fact_closure_researcher"
    precommits: list[dict[str, Any]] = []
    for offset, launch_item in enumerate(batch, 1):
        index = (batch_index - 1) * 3 + offset
        agent_id = f"{prefix}-{stage_slug}-{index:02d}"
        packet_path = run_dir / "context" / f"{agent_id}.md"
        output_path = run_dir / "agent_returns" / f"{agent_id}.json"
        precommit_path = (
            run_dir
            / "allocation_precommits"
            / f"ALLOC-{id_prefix}-{allocation_slug}-{index:03d}.json"
        )
        precommit = api.assert_bounded_return_precommit(
            packet_path,
            output_path,
            run_dir,
            precommit_path,
            expected_agent_id=agent_id,
            expected_stage=stage,
        )
        expected_task_name = api.trace_task_name(run_dir, agent_id)
        if (
            not isinstance(launch_item, dict)
            or set(launch_item)
            != {
                "agent_id",
                "entity_id",
                "batch_index",
                "packet_path",
                "packet_sha256",
                "output_path",
                "allocation_precommit_path",
                "task_name",
            }
            or launch_item.get("agent_id") != agent_id
            or launch_item.get("batch_index") != batch_index
            or launch_item.get("entity_id") != precommit.get("entity_id")
            or Path(launch_item["packet_path"]) != packet_path
            or Path(launch_item["output_path"]) != output_path
            or Path(launch_item["allocation_precommit_path"]) != precommit_path
            or launch_item.get("packet_sha256") != precommit.get("packet_sha256")
            or launch_item.get("task_name") != expected_task_name
            or precommit.get("schema") != "zt1-candidate-allocation-precommit-v2"
            or precommit.get("scope_id") != scope_id
            or precommit.get("arm") != arm
            or precommit.get("seed") != seed
            or precommit.get("role") != role
            or precommit.get("allocation_id")
            != f"ALLOC-{id_prefix}-{allocation_slug}-{index:03d}"
            or precommit.get("batch_index") != batch_index
            or precommit.get("assigned_ids") != [precommit.get("entity_id")]
            or precommit.get("output_ids") != [precommit.get("entity_id")]
            or precommit.get("trace_task_name") != expected_task_name
        ):
            raise RuntimeError(
                "development dispatch identity, paths, or immutable packet bytes differ "
                "from the deterministic batch authorization"
            )
        precommits.append(precommit)
    task_names = [item["trace_task_name"] for item in precommits]
    created_after = min(
        datetime.fromisoformat(item["created_at"]) for item in precommits
    )
    trace_paths: dict[str, Path | None] = {task_name: None for task_name in task_names}
    interval_seconds = (
        api.DEVELOPMENT_METERING_MONITOR["poll_interval_milliseconds"] / 1000
    )
    next_poll = time.monotonic()
    polls = 0
    while True:
        unresolved = [
            task_name for task_name, path in trace_paths.items() if path is None
        ]
        if unresolved:
            discovered = api.find_trace_paths(
                unresolved, created_after=created_after
            )
            trace_paths.update(
                {
                    task_name: path
                    for task_name, path in discovered.items()
                    if path is not None
                }
            )
        snapshot = meter_batch_snapshot(
            api,
            run_dir,
            stage=stage,
            batch_index=batch_index,
            trace_paths=trace_paths,
        )
        polls += 1
        if snapshot["interrupt_task_names"]:
            return {
                "schema": "zt1-development-batch-controller-result-v2",
                "outcome": "interrupt_required",
                "stage": stage,
                "batch_index": batch_index,
                "polls": polls,
                "interrupt_task_names": snapshot["interrupt_task_names"],
                "abort_batch_task_names": sorted(
                    item["task_name"]
                    for item in snapshot["agents"]
                    if item["status"] != "complete"
                ),
                "last_snapshot": snapshot,
            }
        if all(item["status"] == "complete" for item in snapshot["agents"]):
            return {
                "schema": "zt1-development-batch-controller-result-v2",
                "outcome": "batch_complete",
                "stage": stage,
                "batch_index": batch_index,
                "polls": polls,
                "interrupt_task_names": [],
                "abort_batch_task_names": [],
                "last_snapshot": snapshot,
            }
        next_poll += interval_seconds
        delay = next_poll - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        else:
            next_poll = time.monotonic()


def _assert_live_metering_coverage(
    api: Any,
    run_dir: Path,
    *,
    stage: str,
    arm: str,
    admissions: list[dict[str, Any]],
) -> list[dict[str, str]]:
    prefix = "baseline" if arm == "matched_baseline" else "shadow"
    artifacts: list[dict[str, str]] = []
    by_batch: dict[int, list[dict[str, Any]]] = {}
    for admission in admissions:
        by_batch.setdefault(admission["precommit"]["batch_index"], []).append(admission)
    maximum_gap = timedelta(
        milliseconds=api.DEVELOPMENT_METERING_MONITOR["poll_interval_milliseconds"] * 2
    )
    for batch_index, batch in sorted(by_batch.items()):
        path = (
            run_dir
            / "live_metering"
            / f"{prefix}_{stage}_batch_{batch_index:02d}.jsonl"
        )
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"{stage} batch {batch_index} lacks its live-meter log")
        snapshots = api.read_jsonl(path)
        poll_times = [
            _utc(datetime.fromisoformat(item["polled_at"]))
            for item in snapshots
            if isinstance(item, dict)
            and item.get("schema") == "zt1-development-live-meter-snapshot-v2"
            and item.get("stage") == stage
            and item.get("arm") == arm
            and item.get("batch_index") == batch_index
        ]
        if len(poll_times) != len(snapshots) or not poll_times:
            raise RuntimeError(f"{stage} batch {batch_index} live-meter log is malformed")
        if poll_times != sorted(poll_times) or any(
            later - earlier > maximum_gap
            for earlier, later in zip(poll_times, poll_times[1:])
        ):
            raise RuntimeError(f"{stage} batch {batch_index} live-meter polling has a gap")
        batch_start = min(_utc(item["start"]) for item in batch)
        batch_end = max(_utc(item["end"]) for item in batch)
        if poll_times[0] - batch_start > maximum_gap or batch_end - poll_times[-1] > maximum_gap:
            raise RuntimeError(f"{stage} batch {batch_index} live-meter boundary coverage is incomplete")
        if any(
            item.get("stage_admission_must_fail") is True
            for item in snapshots
        ):
            raise RuntimeError(f"{stage} batch {batch_index} crossed a live stop threshold")
        artifacts.append(
            {
                "path": path.relative_to(run_dir).as_posix(),
                "sha256": api.sha256(path),
            }
        )
    return artifacts


def _integrate(api: Any, run_dir: Path, *, stage: str) -> None:
    seed = api.authenticated_run_seed(run_dir)
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = api.read_jsonl(manifest_path)
    _assert_run_open(records[0])
    run_record = records[0]
    arm = run_record.get("arm")
    scope_id = run_record.get("scope_id")
    if arm not in {"matched_baseline", "shadow"} or not isinstance(scope_id, str):
        raise RuntimeError("isolated matched development requires a typed arm and scope")
    agent_prefix = "baseline" if arm == "matched_baseline" else "shadow"
    id_prefix = "B" if arm == "matched_baseline" else "S"
    required_state = "level2_cohort_sealed" if stage == "level2" else "fact_closure_cohort_sealed"
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states[-1:] != [required_state]:
        raise RuntimeError(f"{stage} integration requires the exact sealed input boundary")
    launch_path = run_dir / f"{agent_prefix}_{stage}_launch.json"
    launch = json.loads(launch_path.read_text(encoding="utf-8"))
    if launch.get("seed") != seed:
        raise RuntimeError(f"{stage} launch seed differs from registration")
    expected_count = 12 if stage == "level2" else 6
    batches = launch.get("batches")
    if (
        not isinstance(batches, list)
        or launch.get("schema") != "zt1-isolated-development-launch-v2"
        or launch.get("stage") != stage
        or launch.get("max_concurrency") != 3
        or any(not isinstance(batch, list) or not 1 <= len(batch) <= 3 for batch in batches)
    ):
        raise RuntimeError(f"{stage} launch is not a valid at-most-three batch plan")
    launches = [item for batch in batches for item in batch]
    if len(launches) != expected_count:
        raise RuntimeError(f"{stage} launch must contain {expected_count} isolated agents")

    admissions: list[dict[str, Any]] = []
    for launch_item in launches:
        precommit_path = Path(launch_item["allocation_precommit_path"])
        packet_path = Path(launch_item["packet_path"])
        output_path = Path(launch_item["output_path"])
        precommit = json.loads(precommit_path.read_text(encoding="utf-8"))
        if precommit.get("seed") != seed:
            raise RuntimeError(f"{stage} precommit seed differs from registration")
        if precommit.get("entity_id") != launch_item.get("entity_id"):
            raise RuntimeError("launch and singleton precommit entity IDs differ")
        output = json.loads(output_path.read_text(encoding="utf-8"))
        if launch_item.get("task_name") != precommit.get("trace_task_name"):
            raise RuntimeError("launch and precommit trace task identities differ")
        trace = api.parse_trace(precommit["trace_task_name"])
        admissions.append(
            _validate_return(
                api,
                stage=stage,
                precommit=precommit,
                output=output,
                trace=trace,
                packet_path=packet_path,
                output_path=output_path,
            )
        )
    entity_ids = [item["precommit"]["entity_id"] for item in admissions]
    agent_ids = [item["precommit"]["agent_id"] for item in admissions]
    trace_hashes = [item["trace"]["trace_sha256"] for item in admissions]
    if len(set(entity_ids)) != expected_count or len(set(agent_ids)) != expected_count or len(set(trace_hashes)) != expected_count:
        raise RuntimeError("development admission requires unique one-to-one entities, agents, and traces")
    _assert_batch_execution(admissions)
    live_meter_artifacts = _assert_live_metering_coverage(
        api, run_dir, stage=stage, arm=arm, admissions=admissions
    )
    checkpoint_at = api.now()
    latest_end = max(_utc(item["end"]) for item in admissions)
    deadline = datetime.fromisoformat(records[0]["deadline_at"])
    if not latest_end < _utc(checkpoint_at) < _utc(deadline):
        raise RuntimeError(
            f"{stage} checkpoint must use an actual time after all agents and before deadline"
        )

    # No run artifacts or lifecycle records are materialized until every
    # singleton return and direct trace cap has passed the admission above.
    new_manifest: list[dict[str, Any]] = []
    new_evidence: list[dict[str, Any]] = []
    level2_records: list[dict[str, Any]] = []
    artifacts: list[dict[str, str]] = list(live_meter_artifacts)
    owner_title = "Baseline" if arm == "matched_baseline" else "Shadow"
    report_lines = [f"# {owner_title} Level-2 Research" if stage == "level2" else f"# {owner_title} Fact Closure", ""]
    dossier_dir = run_dir / (
        f"{agent_prefix}_level2"
        if stage == "level2"
        else f"{agent_prefix}_fact_closure"
    )
    trace_dir = run_dir / "runtime_traces"
    attestation_dir = run_dir / "trace_attestations"
    for index, admission in enumerate(admissions, 1):
        precommit = admission["precommit"]
        output = admission["output"]
        trace = admission["trace"]
        agent_id = precommit["agent_id"]
        entity_id = precommit["entity_id"]
        allocation_id = precommit["allocation_id"]
        trace_path = trace_dir / f"{agent_id}.jsonl"
        dossier_path = dossier_dir / (
            f"level2_{entity_id.casefold()}.md" if stage == "level2" else f"closure_{entity_id.casefold()}.md"
        )
        attestation_path = attestation_dir / f"{agent_id}.json"
        for path in (trace_path, dossier_path, attestation_path):
            if path.exists() or path.is_symlink():
                raise RuntimeError(f"refusing to overwrite isolated development artifact: {path}")
        trace_relative = trace_path.relative_to(run_dir).as_posix()
        new_manifest.append(
            {
                "record_type": "agent",
                "scope_id": scope_id,
                "agent_id": agent_id,
                "arm": arm,
                "stage": stage,
                "role": precommit["role"],
                "fork_turns": "none",
                "context_classes": ["founder_constraints", "safety_legal", "neutral_evidence"],
                "context_files": [{"path": precommit["packet_path"], "sha256": precommit["packet_sha256"]}],
                "allowlisted_files": [precommit["packet_path"]],
                "files_read": [precommit["packet_path"]],
                "model": trace["model"],
                "reasoning_effort": trace["reasoning_effort"],
                "metering_basis": "trace_derived_exact",
                "started_at": api.iso(admission["start"]),
                "ended_at": api.iso(admission["end"]),
                "resources": admission["resources"],
                "assigned_ids": [entity_id],
                "output_ids": [entity_id],
                "trace_path": trace_relative,
                "trace_sha256": trace["trace_sha256"],
                "trace_entity_id": entity_id,
                "trace_task_name": precommit["trace_task_name"],
            }
        )
        used_queries = len(output["research"])
        new_manifest.append(
            {
                "record_type": "allocation",
                "scope_id": scope_id,
                "allocation_id": allocation_id,
                "agent_id": agent_id,
                "arm": arm,
                "stage": stage,
                "entity_ids": [entity_id],
                "created_at": precommit["created_at"],
                "metering_basis": "trace_derived_exact",
                "resources": admission["resources"],
                "query_cap": precommit["query_cap"],
                "used_unique_queries": used_queries,
                "unused_queries": precommit["query_cap"] - used_queries,
            }
        )
        evidence_ids: list[str] = []
        trace_calls: list[dict[str, str]] = []
        for offset, (research_item, call) in enumerate(zip(output["research"], trace["web_calls"]), 1):
            query_id = precommit["query_ids"][offset - 1]
            evidence_id = precommit["evidence_ids"][offset - 1]
            source_id = f"SRC-{id_prefix}-{'L2' if stage == 'level2' else 'FC'}-{index:03d}-{offset:02d}"
            call_id = call["payload"]["call_id"]
            create_time = call["payload"].get("internal_chat_message_metadata_passthrough", {}).get("create_time")
            if not isinstance(create_time, (int, float)) or isinstance(create_time, bool):
                raise RuntimeError(f"{agent_id} web call lacks exact create_time")
            new_manifest.extend(
                [
                    {
                        "record_type": "query",
                        "scope_id": scope_id,
                        "query_id": query_id,
                        "allocation_id": allocation_id,
                        "agent_id": agent_id,
                        "arm": arm,
                        "stage": stage,
                        "query": _normal(research_item["query_text"]),
                        "entity_ids": [entity_id],
                        "occurred_at": api.timestamp_from_epoch(float(create_time)),
                    },
                    {
                        "record_type": "tool_event",
                        "scope_id": scope_id,
                        "call_id": call_id,
                        "query_id": query_id,
                        "allocation_id": allocation_id,
                        "agent_id": agent_id,
                        "arm": arm,
                        "stage": stage,
                        "tool": "web_search",
                        "event_type": "tool_call",
                        "occurred_at": api.iso(api.parse_timestamp(call["timestamp"]).astimezone(api.LOCAL_TZ)),
                    },
                    {
                        "record_type": "source_open",
                        "scope_id": scope_id,
                        "source_event_id": source_id,
                        "query_id": query_id,
                        "call_id": call_id,
                        "allocation_id": allocation_id,
                        "agent_id": agent_id,
                        "arm": arm,
                        "stage": stage,
                        "url": research_item["opened_url"],
                        "entity_ids": [entity_id],
                        "evidence_ids": [evidence_id],
                        "occurred_at": api.call_source_time(trace, call_id),
                    },
                ]
            )
            evidence_ids.append(evidence_id)
            trace_calls.append({"query_id": query_id, "call_id": call_id, "source_event_id": source_id})
            new_evidence.append(
                {
                    "record_type": "evidence",
                    "scope_id": scope_id,
                    "allocation_id": allocation_id,
                    "agent_id": agent_id,
                    "arm": arm,
                    "stage": stage,
                    "evidence_id": evidence_id,
                    "direction_id": entity_id,
                    "concept_id": entity_id,
                    "entity_ids": [entity_id],
                    "source_event_ids": [source_id],
                    "recorded_at": admission["completed_at"],
                    "decision_critical": True,
                    "status": research_item["status"],
                    "proposition": research_item["proposition"],
                    "source": research_item["opened_url"],
                    "source_date": research_item["source_date"],
                    "cheapest_resolving_test": output["cheapest_resolving_test"],
                }
            )
            report_lines.extend(
                [
                    f"## {evidence_id} — {entity_id}",
                    "",
                    f"- Proposition: {research_item['proposition']}",
                    f"- Status: `{research_item['status']}`",
                    f"- Source: {research_item['source_title']} — {research_item['opened_url']}",
                    f"- Source date: {research_item['source_date']}",
                    f"- Contradiction: {research_item['contradiction']}",
                    f"- Recorded at: `{admission['completed_at']}`",
                    "",
                ]
            )
        dossier_relative = dossier_path.relative_to(run_dir).as_posix()
        if stage == "level2":
            level2_record = {
                "record_type": "level2",
                "concept_id": entity_id,
                "selected_at": precommit["selected_at"],
                "completed_at": admission["completed_at"],
                "development_status": "complete",
                "artifact_path": dossier_relative,
                "sha256": api.sha256_bytes(admission["dossier_text"].encode("utf-8")),
                "evidence_ids": evidence_ids,
            }
            if arm == "shadow":
                level2_record["selection_category"] = precommit["selection_category"]
            level2_records.append(level2_record)
        attestation = {
            "schema": "zt1-runtime-trace-attestation-v2",
            "agent_id": agent_id,
            "trace_path": trace_relative,
            "trace_sha256": trace["trace_sha256"],
            "trace_entity_id": entity_id,
            "trace_task_name": precommit["trace_task_name"],
            "model": trace["model"],
            "reasoning_effort": trace["reasoning_effort"],
            "started_at": api.iso(admission["start"]),
            "ended_at": api.iso(admission["end"]),
            "input_tokens": trace["input_tokens"],
            "cached_input_tokens": trace["cached_input_tokens"],
            "uncached_input_tokens": trace["uncached_input_tokens"],
            "output_tokens": trace["output_tokens"],
            "elapsed_microseconds": admission["resources"]["elapsed_microseconds"],
            "web_calls": trace_calls,
            "packet_path": precommit["packet_path"],
            "packet_sha256": precommit["packet_sha256"],
            "return_path": precommit["output_path"],
            "return_sha256": api.sha256(run_dir / precommit["output_path"]),
        }
        admission["write_paths"] = (trace_path, dossier_path, attestation_path)
        admission["attestation"] = attestation
        artifacts.extend(
            [
                {"path": precommit["output_path"], "sha256": api.sha256(run_dir / precommit["output_path"])},
                {"path": dossier_relative, "sha256": api.sha256_bytes(admission["dossier_text"].encode("utf-8"))},
                {"path": trace_relative, "sha256": trace["trace_sha256"]},
                {"path": attestation_path.relative_to(run_dir).as_posix(), "sha256": api.sha256_bytes(api.json_bytes(attestation))},
            ]
        )

    for admission in admissions:
        trace_path, dossier_path, attestation_path = admission["write_paths"]
        api.write_exclusive(trace_path, admission["trace"]["trace_path"].read_bytes())
        api.write_exclusive(dossier_path, admission["dossier_text"].encode("utf-8"))
        api.write_exclusive(attestation_path, api.json_bytes(admission["attestation"]))
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    api.write_replace(ledger_path, api.jsonl_bytes(api.read_jsonl(ledger_path) + level2_records + new_evidence))
    report_path = run_dir / ("03a_level2_research.md" if stage == "level2" else "04_fact_closure.md")
    api.write_exclusive(report_path, ("\n".join(report_lines).rstrip() + "\n").encode("utf-8"))
    artifacts.extend(
        [
            {"path": ledger_path.name, "sha256": api.sha256(ledger_path)},
            {"path": report_path.name, "sha256": api.sha256(report_path)},
        ]
    )
    records.extend(new_manifest)
    state = "level2_complete" if stage == "level2" else "closure_complete"
    checkpoint_number = (
        7 if arm == "matched_baseline" and stage == "level2"
        else 9 if arm == "matched_baseline"
        else 10 if stage == "level2"
        else 12
    )
    predecessor_number = checkpoint_number - 1
    predecessor = f"CP-{scope_id}-{predecessor_number:02d}-{required_state}"
    checkpoint_id = f"CP-{scope_id}-{checkpoint_number:02d}-{state}"
    totals = api.checkpoint_resource_totals(
        records, datetime.fromisoformat(records[0]["started_at"]), checkpoint_at
    )
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": checkpoint_id,
        "state": state,
        "predecessor_id": predecessor,
        "occurred_at": api.iso(checkpoint_at),
        "completed_agent_ids": sorted(
            record["agent_id"] for record in records if record.get("record_type") == "agent"
        ),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": artifacts,
    }
    records.append(checkpoint)
    records[0]["lifecycle_state"] = state
    records[0]["resource_totals"] = dict(totals)
    api.write_replace(manifest_path, api.jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def integrate_baseline_level2(api: Any, run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    api.authenticated_run_seed(run_dir)
    if api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")[0].get("arm") != "matched_baseline":
        raise RuntimeError("baseline Level-2 integration requires matched_baseline arm")
    try:
        _integrate(api, run_dir, stage="level2")
    except Exception as error:
        _record_admission_failure(
            api, run_dir, stage="level2", error=error
        )
        raise


def integrate_baseline_fact_closure(api: Any, run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    api.authenticated_run_seed(run_dir)
    if api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")[0].get("arm") != "matched_baseline":
        raise RuntimeError("baseline closure integration requires matched_baseline arm")
    try:
        _integrate(api, run_dir, stage="fact_closure")
    except Exception as error:
        _record_admission_failure(
            api, run_dir, stage="fact_closure", error=error
        )
        raise


def integrate_shadow_level2(api: Any, run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    api.authenticated_run_seed(run_dir)
    if api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")[0].get("arm") != "shadow":
        raise RuntimeError("shadow Level-2 integration requires shadow arm")
    try:
        _integrate(api, run_dir, stage="level2")
    except Exception as error:
        _record_admission_failure(api, run_dir, stage="level2", error=error)
        raise


def integrate_shadow_fact_closure(api: Any, run_dir: Path) -> None:
    run_dir = run_dir.resolve()
    api.authenticated_run_seed(run_dir)
    if api.read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")[0].get("arm") != "shadow":
        raise RuntimeError("shadow closure integration requires shadow arm")
    try:
        _integrate(api, run_dir, stage="fact_closure")
    except Exception as error:
        _record_admission_failure(api, run_dir, stage="fact_closure", error=error)
        raise
