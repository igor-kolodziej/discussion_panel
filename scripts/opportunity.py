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
CANDIDATE_STAGES = ("discovery", "research", "development", "frozen")
RUN_STATUSES = {"active", "qualified", "no_qualifier", "contested", "failed"}
JOB_STATUSES = {"pending", "running", "completed", "failed", "interrupted", "skipped"}
RETRYABLE_JOB_STATUSES = {"pending", "failed", "interrupted"}
TERMINAL_JOB_STATUSES = {"completed", "skipped"}
CONFIG_KEYS = {
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
CANDIDATE_OPTIONAL_KEYS = {"redesign"}
REDESIGN_KEYS = {"changed_fingerprint_fields", "economic_effect"}
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
CLAIM_KEYS = {"claim_id", "statement", "evidence_refs", "confidence"}
RESEARCH_KEYS = {
    "schema_version",
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "sources",
    "claims",
    "contrary_evidence",
    "unknowns",
}
RESEARCH_SOURCE_KEYS = {
    "source_id",
    "url",
    "title",
    "publisher",
    "published_at",
    "accessed_at",
    "source_type",
    "stance",
}
RESEARCH_CLAIM_KEYS = {"claim_id", "statement", "assessment", "evidence_refs"}
EVALUATION_INPUT_KEYS = {
    "schema_version",
    "candidate_id",
    "candidate_version",
    "candidate_sha256",
    "rubric_id",
    "rubric_sha256",
    "judge_id",
    "evaluation_type",
    "factors",
    "interaction_adjustment",
    "assumptions",
    "main_structural_strength",
    "primary_score_limiter",
    "strongest_disconfirming_evidence",
    "highest_value_structural_change",
    "evidence_needed_for_higher_score",
    "raw_response_path",
    "raw_response_sha256",
}
EVALUATION_DERIVED_KEYS = {
    "base_score",
    "unrounded_score",
    "constrained_score",
    "final_score",
    "qualified",
}
EXTERNAL_RESPONSE_KEYS = {
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
IMPORT_RECEIPT_ACCEPTED_KEYS = IMPORT_RECEIPT_COMMON_KEYS | {
    "evaluation",
    "evaluation_sha256",
    "final_score",
    "qualified",
}
IMPORT_RECEIPT_REJECTED_KEYS = IMPORT_RECEIPT_COMMON_KEYS | {"error"}
FINAL_EVENT_DETAIL_KEYS = {
    "previous_stage",
    "run_status",
    "selected_candidate_id",
    "official_score",
    "no_qualifier_reason",
    "report_sha256",
}
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
MANIFEST_KEYS = {"schema_version", "run_id", "created_at", "config", "source_hashes", "rubric"}
EVENT_KEYS = {"sequence", "at", "event", "run_id", "stage", "job_id", "details"}
SAFE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SAFE_JOB_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SAFE_JUDGE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
RUN_ID_RE = re.compile(r"^\d{8}T\d{6}Z-[0-9a-f]{6}$")
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
            allowed = {"artifact", "artifact_sha256", "kind", "recovered_after_state_commit"}
            required = {"artifact", "artifact_sha256", "kind"}
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
            if details["kind"] not in {"candidate", "research", "evaluation", "generic"}:
                raise InputError("job_completed kind is invalid")
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


def validate_config(value: Any) -> dict[str, Any]:
    config = expect_object(value, "config", exact_keys=CONFIG_KEYS)
    if expect_int(config["schema_version"], "config.schema_version", minimum=1) != 1:
        raise InputError("config.schema_version must be 1")
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
    ratio = as_json_number(config["dominant_structure_ratio"], "config.dominant_structure_ratio")
    if ratio <= 0 or ratio > 1:
        raise InputError("config.dominant_structure_ratio must be in (0, 1]")
    similarity = as_json_number(config["similarity_flag_threshold"], "config.similarity_flag_threshold")
    if similarity <= 0 or similarity > 1:
        raise InputError("config.similarity_flag_threshold must be in (0, 1]")
    if config["sources_min"] > config["sources_max"]:
        raise InputError("config.sources_min must not exceed sources_max")
    if config["finalists_max"] > config["develop_max"] or config["develop_max"] > config["shortlist_max"]:
        raise InputError("config limits must satisfy finalists_max <= develop_max <= shortlist_max")
    return dict(config)


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
    if expect_int(manifest["schema_version"], "manifest.schema_version") != 1:
        raise InputError("manifest.schema_version must be 1")
    run_id = expect_nonempty_string(manifest["run_id"], "manifest.run_id")
    if not RUN_ID_RE.fullmatch(run_id):
        raise InputError("manifest.run_id is not canonical")
    expect_nonempty_string(manifest["created_at"], "manifest.created_at")
    validate_config(manifest["config"])
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
    if expect_int(state["schema_version"], "state.schema_version") != 1:
        raise InputError("state.schema_version must be 1")
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
    if evaluation_type == "working":
        return f"evaluations/{candidate_id}/v{version}/working-{judge_id}.json"
    if evaluation_type == "holdout_native":
        return f"holdout/{candidate_id}/v{version}/native-{judge_id}.json"
    if evaluation_type == "holdout_external":
        return f"holdout/{candidate_id}/v{version}/external-{judge_id}.json"
    raise InputError(f"unsupported evaluation type: {evaluation_type}")


def validate_candidate(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
    *,
    verify_parent: bool = True,
) -> dict[str, Any]:
    candidate = expect_object(value, "candidate")
    missing = sorted(CANDIDATE_KEYS - set(candidate))
    extra = sorted(set(candidate) - CANDIDATE_KEYS - CANDIDATE_OPTIONAL_KEYS)
    if missing or extra:
        raise InputError(f"candidate keys differ; missing={missing}, extra={extra}")
    if expect_int(candidate["schema_version"], "candidate.schema_version") != manifest["config"]["schema_version"]:
        raise InputError("candidate.schema_version differs from workflow schema")
    candidate_id = expect_nonempty_string(candidate["candidate_id"], "candidate.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("candidate.candidate_id must be a lowercase slug")
    version = expect_int(candidate["version"], "candidate.version", minimum=1)
    stage = candidate["stage"]
    if stage not in CANDIDATE_STAGES:
        raise InputError("candidate.stage is invalid")
    parent = candidate["parent"]
    redesign_parent: dict[str, Any] | None = None
    if parent is not None:
        parent_obj = expect_object(parent, "candidate.parent", exact_keys={"candidate_id", "version"})
        parent_id = expect_nonempty_string(parent_obj["candidate_id"], "candidate.parent.candidate_id")
        if not SAFE_ID_RE.fullmatch(parent_id):
            raise InputError("candidate.parent.candidate_id must be a lowercase slug")
        parent_version = expect_int(parent_obj["version"], "candidate.parent.version", minimum=1)
        if parent_id != candidate_id or parent_version != version - 1:
            raise InputError("candidate parent must be the same candidate_id at exactly version N-1")
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
            parent_stage = parent_candidate["stage"]
            stage_delta = CANDIDATE_STAGES.index(stage) - CANDIDATE_STAGES.index(parent_stage)
            if stage_delta < 0 or stage_delta > 1:
                raise InputError("candidate stages must advance monotonically without skipping a stage")
            if stage_delta == 0 and stage != "development":
                raise InputError("only development may create a same-stage candidate version")
            if stage_delta == 0:
                redesign_parent = parent_candidate
    elif version != 1:
        raise InputError("candidate versions after v1 require a parent")
    elif stage != "discovery":
        raise InputError("candidate v1 must begin at discovery stage")
    expect_nonempty_string(candidate["title"], "candidate.title")
    expect_nonempty_string(candidate["thesis"], "candidate.thesis")
    fingerprint = expect_object(candidate["fingerprint"], "candidate.fingerprint", exact_keys=FINGERPRINT_KEYS)
    for key in FINGERPRINT_KEYS:
        expect_nonempty_string(fingerprint[key], f"candidate.fingerprint.{key}")
    expect_string_list(candidate["founder_fit"], "candidate.founder_fit", unique=True)
    source_refs = expect_string_list(candidate["source_refs"], "candidate.source_refs", unique=True)
    maximum = manifest["config"]["sources_max"]
    minimum = manifest["config"]["sources_min"]
    if len(source_refs) > maximum:
        raise InputError(f"candidate.source_refs exceeds sources_max={maximum}")
    if candidate["stage"] in {"research", "development", "frozen"} and len(source_refs) < minimum:
        raise InputError(f"{candidate['stage']} candidate requires at least {minimum} sources")
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
        if candidate["stage"] != "development":
            raise InputError("candidate.redesign is valid only for a same-stage development revision")
        redesign = expect_object(candidate["redesign"], "candidate.redesign", exact_keys=REDESIGN_KEYS)
        declared_fields = expect_string_list(
            redesign["changed_fingerprint_fields"],
            "candidate.redesign.changed_fingerprint_fields",
            unique=True,
        )
        if not declared_fields or any(field not in FINGERPRINT_KEYS for field in declared_fields):
            raise InputError("candidate.redesign.changed_fingerprint_fields must name fingerprint fields")
        expect_nonempty_string(redesign["economic_effect"], "candidate.redesign.economic_effect")
    if redesign_parent is None:
        if redesign is not None and verify_parent:
            raise InputError("candidate.redesign is valid only for a same-stage development revision")
    else:
        if redesign is None:
            raise InputError("same-stage development revision requires candidate.redesign")
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
            raise InputError("same-stage development revision must update at least one economics field")
    if candidate["stage"] == "frozen":
        capital = economics["capital_required_pln"]
        if isinstance(capital, bool) or not isinstance(capital, (int, float)):
            raise InputError("frozen candidate.economics.capital_required_pln must be a JSON number")
        if as_json_number(capital, "candidate.economics.capital_required_pln") < 0:
            raise InputError("frozen candidate.economics.capital_required_pln must be nonnegative")
    claims = candidate["claims"]
    if not isinstance(claims, list):
        raise InputError("candidate.claims must be a list")
    claim_ids: set[str] = set()
    for index, raw_claim in enumerate(claims):
        claim = expect_object(raw_claim, f"candidate.claims[{index}]", exact_keys=CLAIM_KEYS)
        claim_id = expect_nonempty_string(claim["claim_id"], f"candidate.claims[{index}].claim_id")
        if claim_id in claim_ids:
            raise InputError(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        expect_nonempty_string(claim["statement"], f"candidate.claims[{index}].statement")
        evidence_refs = expect_string_list(
            claim["evidence_refs"], f"candidate.claims[{index}].evidence_refs", unique=True
        )
        missing_evidence = sorted(set(evidence_refs) - set(source_refs))
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
    return dict(candidate)


def research_relpath(candidate_id: str, version: int) -> str:
    return f"research/{candidate_id}/v{version}.json"


def validate_research(value: Any, manifest: Mapping[str, Any], run_dir: Path) -> dict[str, Any]:
    research = expect_object(value, "research", exact_keys=RESEARCH_KEYS)
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
    if candidate["stage"] != "research":
        raise InputError("research must bind a canonical research-stage candidate")
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
        source = expect_object(raw_source, f"research.sources[{index}]", exact_keys=RESEARCH_SOURCE_KEYS)
        for key in RESEARCH_SOURCE_KEYS - {"stance"}:
            expect_nonempty_string(source[key], f"research.sources[{index}].{key}")
        source_id = source["source_id"].strip()
        if source_id in source_ids:
            raise InputError(f"duplicate research source id: {source_id}")
        source_ids.add(source_id)
        if source["stance"] not in {"supporting", "contradicting", "context"}:
            raise InputError(f"research.sources[{index}].stance is invalid")
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
        if claim["assessment"] not in {"evidence", "inference", "unknown"}:
            raise InputError(f"research.claims[{index}].assessment is invalid")
        refs = expect_string_list(
            claim["evidence_refs"], f"research.claims[{index}].evidence_refs", unique=True
        )
        missing_refs = sorted(set(refs) - source_ids)
        if missing_refs:
            raise InputError(f"research claim {claim_id} references unknown sources: {missing_refs}")
        canonical_claims.append(dict(claim))
    expect_string_list(research["contrary_evidence"], "research.contrary_evidence", unique=True)
    expect_string_list(research["unknowns"], "research.unknowns", unique=True)
    canonical = dict(research)
    canonical["sources"] = canonical_sources
    canonical["claims"] = canonical_claims
    return canonical


def compute_evaluation(
    value: Any,
    manifest: Mapping[str, Any],
    run_dir: Path,
) -> dict[str, Any]:
    evaluation = expect_object(value, "evaluation")
    allowed = EVALUATION_INPUT_KEYS | EVALUATION_DERIVED_KEYS
    if not EVALUATION_INPUT_KEYS.issubset(evaluation) or not set(evaluation).issubset(allowed):
        missing = sorted(EVALUATION_INPUT_KEYS - set(evaluation))
        extra = sorted(set(evaluation) - allowed)
        raise InputError(f"evaluation keys differ; missing={missing}, extra={extra}")
    if expect_int(evaluation["schema_version"], "evaluation.schema_version") != manifest["config"]["schema_version"]:
        raise InputError("evaluation.schema_version differs from workflow schema")
    candidate_id = expect_nonempty_string(evaluation["candidate_id"], "evaluation.candidate_id")
    if not SAFE_ID_RE.fullmatch(candidate_id):
        raise InputError("evaluation.candidate_id must be a lowercase slug")
    version = expect_int(evaluation["candidate_version"], "evaluation.candidate_version", minimum=1)
    candidate_path = run_dir / candidate_relpath(candidate_id, version)
    if not candidate_path.is_file():
        raise InputError("evaluation candidate artifact does not exist")
    candidate_digest = sha256_file(candidate_path)
    if evaluation["candidate_sha256"] != candidate_digest:
        raise InputError("evaluation.candidate_sha256 does not match the immutable candidate")
    candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
    if evaluation["rubric_id"] != manifest["rubric"]["rubric_id"]:
        raise InputError("evaluation.rubric_id does not match the run rubric")
    if evaluation["rubric_sha256"] != manifest["rubric"]["sha256"]:
        raise InputError("evaluation.rubric_sha256 does not match the run rubric")
    judge_id = expect_nonempty_string(evaluation["judge_id"], "evaluation.judge_id")
    if not SAFE_JUDGE_RE.fullmatch(judge_id):
        raise InputError("evaluation.judge_id is not path-safe")
    if evaluation["evaluation_type"] not in {"working", "holdout_native", "holdout_external"}:
        raise InputError("evaluation.evaluation_type is invalid")
    required_candidate_stage = {
        "working": "development",
        "holdout_native": "frozen",
        "holdout_external": "frozen",
    }[evaluation["evaluation_type"]]
    if candidate["stage"] != required_candidate_stage:
        raise InputError(
            f"{evaluation['evaluation_type']} evaluation must bind a {required_candidate_stage}-stage candidate"
        )
    if evaluation["evaluation_type"] in {"holdout_native", "holdout_external"}:
        validate_finalist_lineage(run_dir, manifest, candidate)
    expect_string_list(evaluation["assumptions"], "evaluation.assumptions", unique=True)
    for key in (
        "main_structural_strength",
        "primary_score_limiter",
        "strongest_disconfirming_evidence",
        "highest_value_structural_change",
        "evidence_needed_for_higher_score",
    ):
        expect_nonempty_string(evaluation[key], f"evaluation.{key}")
    raw_rel, raw_path = run_relative_path(run_dir, evaluation["raw_response_path"], "evaluation.raw_response_path")
    if evaluation["evaluation_type"] in {"holdout_native", "holdout_external"} and not raw_rel.startswith("holdout/"):
        raise InputError("holdout evaluation raw response must live under holdout/")
    raw_digest = sha256_file(raw_path)
    if evaluation["raw_response_sha256"] != raw_digest:
        raise InputError("evaluation.raw_response_sha256 does not match the raw response")
    adjustment = as_json_number(evaluation["interaction_adjustment"], "evaluation.interaction_adjustment")
    if adjustment < Decimal("-0.5") or adjustment > Decimal("0.5"):
        raise InputError("evaluation.interaction_adjustment must be in [-0.5, 0.5]")

    rubric = rubric_from_manifest(manifest)
    expected_names = [name for name, _ in rubric]
    factors_value = evaluation["factors"]
    if not isinstance(factors_value, list):
        raise InputError("evaluation.factors must be a list")
    supplied_by_name: dict[str, dict[str, Any]] = {}
    for index, raw_factor in enumerate(factors_value):
        factor = expect_object(raw_factor, f"evaluation.factors[{index}]")
        if not FACTOR_BASE_KEYS.issubset(factor) or not set(factor).issubset(FACTOR_BASE_KEYS | FACTOR_DERIVED_KEYS):
            missing = sorted(FACTOR_BASE_KEYS - set(factor))
            extra = sorted(set(factor) - FACTOR_BASE_KEYS - FACTOR_DERIVED_KEYS)
            raise InputError(f"evaluation.factors[{index}] keys differ; missing={missing}, extra={extra}")
        name = expect_nonempty_string(factor["name"], f"evaluation.factors[{index}].name")
        if name in supplied_by_name:
            raise InputError(f"duplicate evaluation factor: {name}")
        supplied_by_name[name] = factor
    if set(supplied_by_name) != set(expected_names):
        missing = sorted(set(expected_names) - set(supplied_by_name))
        extra = sorted(set(supplied_by_name) - set(expected_names))
        raise InputError(f"evaluation factors differ from rubric; missing={missing}, extra={extra}")

    scored_weight = Decimal(0)
    scored_values: dict[str, Decimal] = {}
    for name, weight in rubric:
        factor = supplied_by_name[name]
        status = factor["status"]
        rationale = expect_nonempty_string(factor["rationale"], f"evaluation factor {name} rationale")
        if status == "scored":
            score = as_json_number(factor["score"], f"evaluation factor {name} score")
            if score < 1 or score > 10:
                raise InputError(f"evaluation factor {name} score must be in [1, 10]")
            scored_values[name] = score
            scored_weight += weight
        elif status == "excluded":
            if factor["score"] is not None:
                raise InputError(f"excluded evaluation factor {name} must have null score")
            if not rationale:
                raise InputError(f"excluded evaluation factor {name} requires a rationale")
        else:
            raise InputError(f"evaluation factor {name} status must be scored or excluded")
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
        expected_original = Decimal(str(decimal_json(weight, quantum=DERIVED_QUANTUM)))
        expected_effective = Decimal(str(decimal_json(effective, quantum=DERIVED_QUANTUM)))
        if "original_weight" in supplied and as_json_number(
            supplied["original_weight"], f"evaluation factor {name} original_weight"
        ) != expected_original:
            raise InputError(f"evaluation factor {name} original_weight does not match the rubric")
        if "effective_weight" in supplied and as_json_number(
            supplied["effective_weight"], f"evaluation factor {name} effective_weight"
        ) != expected_effective:
            raise InputError(f"evaluation factor {name} effective_weight does not match renormalization")
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
    for key, expected in expected_derived.items():
        if key not in evaluation:
            continue
        if key == "qualified":
            if not isinstance(evaluation[key], bool) or evaluation[key] is not expected:
                raise InputError("evaluation.qualified does not match computed qualification")
        elif as_json_number(evaluation[key], f"evaluation.{key}") != Decimal(str(expected)):
            raise InputError(f"evaluation.{key} does not match deterministic scoring")

    canonical = {key: evaluation[key] for key in EVALUATION_INPUT_KEYS}
    canonical["raw_response_path"] = raw_rel
    canonical["interaction_adjustment"] = decimal_json(adjustment)
    canonical["factors"] = canonical_factors
    canonical.update(expected_derived)
    if canonical["evaluation_type"] in {"holdout_native", "holdout_external"}:
        validate_holdout_response_binding(
            raw_path,
            raw_rel,
            raw_digest,
            canonical,
            manifest,
            run_dir,
        )
    return canonical


def validate_generic_input(path: Path, kind: str) -> bytes:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read input artifact {path}: {exc}") from exc
    if not data:
        raise InputError(f"{kind} artifact must not be empty")
    return data


def make_run(config_path: Path, runs_dir: Path) -> dict[str, Any]:
    config = validate_config(load_json(config_path))
    rubric_path = REPO_ROOT / "Personalities" / "ZeroToOne.txt"
    factors, rubric_digest = parse_rubric(rubric_path)
    if config_path.resolve() != (REPO_ROOT / "config" / "opportunity-workflow.json").resolve():
        config_source_digest = sha256_file(config_path)
    else:
        config_source_digest = sha256_file(REPO_ROOT / "config" / "opportunity-workflow.json")
    source_hashes: dict[str, str] = {}
    source_bytes: dict[str, bytes] = {}
    for relative in SOURCE_PATHS:
        path = REPO_ROOT / relative
        if relative == "config/opportunity-workflow.json":
            source_hashes[relative] = config_source_digest
            source_bytes[relative] = config_path.read_bytes()
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
        "schema_version": 1,
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
    state = {
        "schema_version": 1,
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
    except BaseException:
        # A just-created empty run directory has no historical value.  Keep any
        # partially written files visible rather than attempting broad cleanup.
        raise
    return {"run_id": run_id, "run_dir": str(run_dir), "stage": "initialized", "run_status": "active"}


def assert_active(state: Mapping[str, Any]) -> None:
    if state["stage"] == "complete" or state["run_status"] != "active":
        raise ConflictError(f"run is terminal: {state['run_status']}")


def job_is_retryable(job: Mapping[str, Any]) -> bool:
    return job["status"] in RETRYABLE_JOB_STATUSES and job["attempts"] < job["max_attempts"]


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
        return {
            "run_id": state["run_id"],
            "stage": state["stage"],
            "job_id": job_id,
            **job,
            "retryable": job_is_retryable(job),
            "idempotent": False,
        }


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
        stage_limits = {
            "research": manifest["config"]["shortlist_max"],
            "development": manifest["config"]["develop_max"],
            "frozen": manifest["config"]["finalists_max"],
        }
        if state["stage"] not in {"discovery", "research", "development", "frozen"}:
            raise ConflictError(f"candidate artifacts are not accepted during {state['stage']}")
        if state["stage"] in stage_limits:
            existing_ids = {
                item["candidate_id"]
                for _, item in iter_candidates(run_dir, manifest, verify_parents=False)
                if item["stage"] == state["stage"]
            }
            if canonical["candidate_id"] not in existing_ids and len(existing_ids) >= stage_limits[state["stage"]]:
                raise ConflictError(f"{state['stage']} candidate limit is {stage_limits[state['stage']]}")
        relative = candidate_relpath(canonical["candidate_id"], canonical["version"])
        existing_candidate_paths = [
            path
            for path, item in iter_candidates(run_dir, manifest, verify_parents=False)
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
            development_versions = [
                item
                for _, item in iter_candidates(run_dir, manifest, verify_parents=False)
                if item["stage"] == "development" and item["candidate_id"] == canonical["candidate_id"]
            ]
            if not (run_dir / relative).exists() and len(development_versions) >= 2:
                raise ConflictError("a candidate may have at most two development-stage versions")
        if state["stage"] == "frozen":
            validate_finalist_lineage(run_dir, manifest, canonical)
        return relative, canonical_json_bytes(canonical), canonical
    if kind == "evaluation":
        canonical = compute_evaluation(load_json(input_path), manifest, run_dir)
        expected_type = "working" if state["stage"] == "development" else "holdout_native" if state["stage"] == "holdout" else None
        if expected_type is None:
            raise ConflictError(f"evaluation artifacts are not accepted during {state['stage']}")
        if canonical["evaluation_type"] != expected_type:
            raise ConflictError(f"{state['stage']} requires evaluation_type={expected_type}")
        relative = evaluation_relpath(
            canonical["candidate_id"], canonical["candidate_version"], canonical["evaluation_type"], canonical["judge_id"]
        )
        return relative, canonical_json_bytes(canonical), canonical
    if kind == "research":
        if state["stage"] != "research":
            raise ConflictError("research artifacts are accepted only during research stage")
        canonical = validate_research(load_json(input_path), manifest, run_dir)
        relative = research_relpath(canonical["candidate_id"], canonical["candidate_version"])
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


def complete_job(run_dir: Path, job_id: str, input_path: Path, kind: str) -> dict[str, Any]:
    if not SAFE_JOB_RE.fullmatch(job_id):
        raise InputError("JOB_ID is not path-safe")
    with file_lock(run_dir / ".state.lock", root=run_dir):
        manifest, state = load_run(run_dir)
        assert_active(state)
        events = load_events(run_dir / "events.jsonl", state["run_id"])
        projected_stage, projected_status, _ = project_transition_state(events)
        if (projected_stage, projected_status) != (state["stage"], state["run_status"]):
            raise InputError("state lifecycle disagrees with events.jsonl before job completion")
        jobs = state["jobs"][state["stage"]]
        if job_id not in jobs:
            raise InputError(f"unknown job in current stage: {job_id}")
        job = jobs[job_id]
        relative, data, _ = _artifact_for_input(run_dir, manifest, state, job_id, input_path, kind)
        digest = sha256_bytes(data)
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
                            "artifact": relative,
                            "artifact_sha256": digest,
                            "kind": kind,
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
        if job["status"] != "running":
            raise ConflictError(f"only a running job can complete: {job_id} is {job['status']}")
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
            details={"artifact": relative, "artifact_sha256": digest, "kind": kind},
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
            return {
                "run_id": state["run_id"],
                "stage": state["stage"],
                "interrupted": interrupted,
                "eligible_jobs": sorted(eligible, key=lambda item: (item["stage"], item["job_id"])),
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
        return {
            "run_id": state["run_id"],
            "stage": state["stage"],
            "interrupted": interrupted,
            "eligible_jobs": sorted(eligible, key=lambda item: (item["stage"], item["job_id"])),
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
    structure_groups: dict[tuple[str, ...], list[dict[str, Any]]] = {}
    lexical_rows: list[tuple[dict[str, Any], tuple[str, ...], set[str]]] = []
    ordered_keys = sorted(FINGERPRINT_KEYS)
    for _, candidate in rows:
        reference = {"candidate_id": candidate["candidate_id"], "version": candidate["version"]}
        fingerprint = tuple(normalize_fingerprint(candidate["fingerprint"][key]) for key in ordered_keys)
        fingerprint_groups.setdefault(fingerprint, []).append(reference)
        structure = tuple(
            normalize_fingerprint(candidate["fingerprint"][key])
            for key in ("payer_and_paid_event", "offer_and_business_model")
        )
        structure_groups.setdefault(structure, []).append(reference)
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
    dominant_key, dominant_members = min(
        structure_groups.items(),
        key=lambda item: (-len(item[1]), item[0]),
    )
    candidate_count = len(rows)
    unique_count = len(sorted_groups)
    ratio = Decimal(len(dominant_members)) / Decimal(candidate_count)
    unique_shortfall = max(0, manifest["config"]["unique_min"] - unique_count)
    ratio_exceeded = ratio > as_decimal(
        manifest["config"]["dominant_structure_ratio"], "config.dominant_structure_ratio"
    )
    needs_gap = unique_shortfall > 0 or ratio_exceeded
    gap_slots = 0
    if needs_gap:
        gap_slots = min(
            manifest["config"]["gap_scout_max"],
            max(1 if ratio_exceeded else 0, unique_shortfall),
        )
    return {
        "schema_version": 1,
        "candidate_artifacts": candidate_input_hashes(run_dir, manifest, "discovery"),
        "candidate_count": candidate_count,
        "unique_count": unique_count,
        "unique_candidate_refs": unique_refs,
        "duplicate_groups": duplicate_groups,
        "similarity_flags": similarity_flags,
        "dominant_structure": {
            "payer_and_paid_event": dominant_key[0],
            "offer_and_business_model": dominant_key[1],
            "count": len(dominant_members),
            "ratio": decimal_json(ratio, quantum=DERIVED_QUANTUM),
        },
        "limits": {
            "unique_min": manifest["config"]["unique_min"],
            "dominant_structure_ratio": manifest["config"]["dominant_structure_ratio"],
            "similarity_flag_threshold": manifest["config"]["similarity_flag_threshold"],
            "gap_scout_max": manifest["config"]["gap_scout_max"],
        },
        "needs_gap_scout": needs_gap,
        "gap_scout_slots": gap_slots,
    }


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
                "unique_count": report["unique_count"],
                "needs_gap_scout": report["needs_gap_scout"],
                "gap_scout_job": report["gap_scout_job"],
            },
        )
        return {"run_id": state["run_id"], "artifact": "dedup/report.json", **report}


def _stage_candidate_count(run_dir: Path, manifest: Mapping[str, Any], stage: str) -> int:
    return len(latest_candidates_for_stage(run_dir, manifest, stage))


def _validate_stage_gate(run_dir: Path, manifest: Mapping[str, Any], state: Mapping[str, Any]) -> None:
    stage = state["stage"]
    if stage == "discovery":
        report_path = run_dir / "dedup" / "report.json"
        if not report_path.is_file():
            raise ConflictError("run dedup before leaving discovery")
        report = expect_object(load_json(report_path), "dedup report")
        if report.get("candidate_artifacts") != candidate_input_hashes(run_dir, manifest, "discovery"):
            raise ConflictError("dedup report is stale; rerun dedup")
        below_minimum = report.get("unique_count", 0) < manifest["config"]["unique_min"]
        dominant = expect_object(report.get("dominant_structure"), "dedup dominant_structure")
        ratio_exceeded = as_decimal(dominant.get("ratio"), "dedup dominant ratio") > as_decimal(
            manifest["config"]["dominant_structure_ratio"], "config.dominant_structure_ratio"
        )
        if below_minimum or ratio_exceeded:
            gap_job = state["jobs"]["discovery"].get("gap-scout")
            gap_exhausted = gap_job is not None and (
                gap_job["status"] in TERMINAL_JOB_STATUSES
                or (gap_job["status"] in {"failed", "interrupted"} and not job_is_retryable(gap_job))
            )
            if not gap_exhausted:
                raise ConflictError("discovery diversity target requires the one bounded gap-scout job")
    stage_limits = {
        "research": ("research", manifest["config"]["shortlist_max"]),
        "development": ("development", manifest["config"]["develop_max"]),
        "frozen": ("frozen", manifest["config"]["finalists_max"]),
    }
    if stage in stage_limits:
        candidate_stage, maximum = stage_limits[stage]
        count = _stage_candidate_count(run_dir, manifest, candidate_stage)
        if count < 1:
            raise ConflictError(f"{stage} requires at least one {candidate_stage} candidate")
        if count > maximum:
            raise ConflictError(f"{stage} has {count} candidates, exceeding limit {maximum}")
    if stage == "frozen":
        for _, candidate in latest_candidates_for_stage(run_dir, manifest, "frozen"):
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
        _validate_stage_gate(run_dir, manifest, state)
        current = state["stage"]
        next_stage = STAGES[STAGES.index(current) + 1]
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


def _latest_candidate(run_dir: Path, manifest: Mapping[str, Any], candidate_id: str, stage: str) -> tuple[Path, dict[str, Any]]:
    matches = [
        (path, candidate)
        for path, candidate in iter_candidates(run_dir, manifest)
        if candidate["candidate_id"] == candidate_id and candidate["stage"] == stage
    ]
    if not matches:
        raise InputError(f"no {stage} candidate found for {candidate_id}")
    return max(matches, key=lambda item: item[1]["version"])


def external_response_schema(manifest: Mapping[str, Any]) -> dict[str, Any]:
    factor_names = [name for name, _ in rubric_from_manifest(manifest)]
    diagnostics = sorted(EXTERNAL_RESPONSE_KEYS - {"judge_id", "factors", "interaction_adjustment", "assumptions"})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "External opportunity holdout response",
        "type": "object",
        "additionalProperties": False,
        "required": sorted(EXTERNAL_RESPONSE_KEYS),
        "properties": {
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


def validate_finalist_lineage(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Require a complete stage lineage and diagnosis for this exact finalist."""
    if candidate.get("stage") != "frozen":
        raise InputError("finalist lineage validation requires a frozen candidate")
    lineage = candidate_lineage(run_dir, manifest, candidate)
    stages = [item["stage"] for item in lineage]
    if set(stages) != set(CANDIDATE_STAGES):
        raise InputError(
            "frozen candidate lineage must include discovery, research, development, and frozen stages"
        )
    development = lineage[-2]
    if development["stage"] != "development":
        raise InputError("frozen candidate must directly descend from a development version")
    development_path = run_dir / candidate_relpath(
        development["candidate_id"], development["version"]
    )
    development_digest = sha256_file(development_path)
    evaluation_root = (
        run_dir
        / "evaluations"
        / development["candidate_id"]
        / f"v{development['version']}"
    )
    matching_working: list[str] = []
    for path in sorted(evaluation_root.glob("working-*.json")):
        _assert_safe_write_path(run_dir, path, "working evaluation path")
        evaluation = compute_evaluation(load_json(path), manifest, run_dir)
        expected_path = run_dir / evaluation_relpath(
            evaluation["candidate_id"],
            evaluation["candidate_version"],
            evaluation["evaluation_type"],
            evaluation["judge_id"],
        )
        if path.resolve() != expected_path.resolve():
            raise InputError(f"working evaluation stored at noncanonical path: {path.relative_to(run_dir)}")
        if (
            evaluation["evaluation_type"] == "working"
            and evaluation["candidate_id"] == development["candidate_id"]
            and evaluation["candidate_version"] == development["version"]
            and evaluation["candidate_sha256"] == development_digest
        ):
            matching_working.append(path.relative_to(run_dir).as_posix())
    if not matching_working:
        raise InputError(
            f"frozen candidate {candidate['candidate_id']} v{candidate['version']} requires a working evaluation "
            f"of its development parent v{development['version']}"
        )
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_version": candidate["version"],
        "lineage_versions": [item["version"] for item in lineage],
        "working_evaluations": matching_working,
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
        path, candidate = _latest_candidate(run_dir, manifest, candidate_id, "frozen")
        validate_finalist_lineage(run_dir, manifest, candidate)
        digest = sha256_file(path)
        root = run_dir / "exports" / candidate_id
        packet_path = root / "holdout_packet.md"
        schema_path = root / "response_schema.json"
        existed = packet_path.exists() and schema_path.exists()
        packet_bytes = external_packet(run_dir, candidate, digest, manifest).encode("utf-8")
        schema_bytes = canonical_json_bytes(external_response_schema(manifest))
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


def parse_external_object(raw: bytes, source: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8").strip()
    except UnicodeError as exc:
        raise InputError("external response must be UTF-8") from exc
    if not text:
        raise InputError("external response is empty")
    if text.startswith("```"):
        match = re.fullmatch(r"```(?:json)?[ \t]*\r?\n([\s\S]*?)\r?\n```", text, flags=re.IGNORECASE)
        if not match:
            raise InputError("external response must be one plain JSON object or one JSON fenced block")
        text = match.group(1).strip()
    value = parse_json(text, source=source)
    return expect_object(value, "external response", exact_keys=EXTERNAL_RESPONSE_KEYS)


def _plain_response_object(raw: bytes, source: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8").strip()
    except UnicodeError as exc:
        raise InputError("native holdout response must be UTF-8 JSON") from exc
    if not text or text.startswith("```"):
        raise InputError("native holdout raw response must be one plain response-schema JSON object")
    return expect_object(
        parse_json(text, source=source),
        "native holdout response",
        exact_keys=EXTERNAL_RESPONSE_KEYS,
    )


def _factor_response_projection(evaluation: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {key: factor[key] for key in FACTOR_BASE_KEYS}
        for factor in evaluation["factors"]
    ]


def validate_holdout_response_binding(
    raw_path: Path,
    raw_rel: str,
    raw_digest: str,
    evaluation: Mapping[str, Any],
    manifest: Mapping[str, Any],
    run_dir: Path,
) -> None:
    raw = raw_path.read_bytes()
    if evaluation["evaluation_type"] == "holdout_native":
        response = _plain_response_object(raw, str(raw_path))
    else:
        response = parse_external_object(raw, str(raw_path))

    if expect_nonempty_string(response["judge_id"], "holdout response judge_id") != evaluation["judge_id"]:
        raise InputError("holdout raw response judge_id differs from the canonical evaluation")
    if as_json_number(
        response["interaction_adjustment"], "holdout response interaction_adjustment"
    ) != as_json_number(evaluation["interaction_adjustment"], "evaluation.interaction_adjustment"):
        raise InputError("holdout raw response interaction_adjustment differs from the canonical evaluation")
    response_assumptions = expect_string_list(
        response["assumptions"], "holdout response assumptions", unique=True
    )
    canonical_assumptions = expect_string_list(
        evaluation["assumptions"], "evaluation.assumptions", unique=True
    )
    if response_assumptions != canonical_assumptions:
        raise InputError("holdout raw response assumptions differ from the canonical evaluation")
    for key in EXTERNAL_RESPONSE_KEYS - {"judge_id", "factors", "interaction_adjustment", "assumptions"}:
        if expect_nonempty_string(response[key], f"holdout response {key}") != expect_nonempty_string(
            evaluation[key], f"evaluation.{key}"
        ):
            raise InputError(f"holdout raw response {key} differs from the canonical evaluation")

    raw_factors = response["factors"]
    if not isinstance(raw_factors, list):
        raise InputError("holdout response factors must be a list")
    raw_by_name: dict[str, dict[str, Any]] = {}
    for index, raw_factor in enumerate(raw_factors):
        factor = expect_object(
            raw_factor,
            f"holdout response factors[{index}]",
            exact_keys=FACTOR_BASE_KEYS,
        )
        name = expect_nonempty_string(factor["name"], f"holdout response factors[{index}].name")
        if name in raw_by_name:
            raise InputError(f"duplicate holdout response factor: {name}")
        raw_by_name[name] = factor
    expected_factors = _factor_response_projection(evaluation)
    if set(raw_by_name) != {factor["name"] for factor in expected_factors}:
        raise InputError("holdout raw response factors differ from the canonical evaluation")
    for expected in expected_factors:
        raw_factor = raw_by_name[expected["name"]]
        if raw_factor["status"] != expected["status"]:
            raise InputError(f"holdout raw response factor {expected['name']} status differs")
        if expect_nonempty_string(
            raw_factor["rationale"], f"holdout response factor {expected['name']} rationale"
        ) != expected["rationale"]:
            raise InputError(f"holdout raw response factor {expected['name']} rationale differs")
        if expected["status"] == "excluded":
            if raw_factor["score"] is not None:
                raise InputError(f"holdout raw response excluded factor {expected['name']} must have null score")
        elif as_json_number(
            raw_factor["score"], f"holdout response factor {expected['name']} score"
        ) != as_json_number(expected["score"], f"evaluation factor {expected['name']} score"):
            raise InputError(f"holdout raw response factor {expected['name']} score differs")

    if evaluation["evaluation_type"] == "holdout_native":
        if not raw_rel.startswith("holdout/jobs/"):
            raise InputError("native holdout raw response must be a completed generic holdout job artifact")
        state = validate_state(load_json(run_dir / "state.json"), manifest)
        matching_jobs = [
            (job_id, job)
            for job_id, job in state["jobs"]["holdout"].items()
            if job["status"] == "completed"
            and job["artifact"] == raw_rel
            and job["artifact_sha256"] == raw_digest
        ]
        if len(matching_jobs) != 1:
            raise InputError("native holdout raw response is not bound to exactly one completed holdout job")


def _external_identity(
    run_dir: Path,
    manifest: Mapping[str, Any],
    candidate_id: str,
) -> tuple[Path, dict[str, Any], str]:
    candidate_path, candidate = _latest_candidate(run_dir, manifest, candidate_id, "frozen")
    validate_finalist_lineage(run_dir, manifest, candidate)
    candidate_digest = sha256_file(candidate_path)
    export_root = run_dir / "exports" / candidate_id
    packet_path = export_root / "holdout_packet.md"
    schema_path = export_root / "response_schema.json"
    if not packet_path.is_file() or not schema_path.is_file():
        raise ConflictError("export the external packet before importing a response")
    if packet_path.read_bytes() != external_packet(run_dir, candidate, candidate_digest, manifest).encode("utf-8"):
        raise ConflictError("exported external packet does not match the frozen candidate")
    if schema_path.read_bytes() != canonical_json_bytes(external_response_schema(manifest)):
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
            judge_id = expect_nonempty_string(response["judge_id"], "external response judge_id")
            evaluation_input = {
                "schema_version": manifest["config"]["schema_version"],
                "candidate_id": candidate_id,
                "candidate_version": candidate["version"],
                "candidate_sha256": candidate_digest,
                "rubric_id": manifest["rubric"]["rubric_id"],
                "rubric_sha256": manifest["rubric"]["sha256"],
                "judge_id": judge_id,
                "evaluation_type": "holdout_external",
                "factors": response["factors"],
                "interaction_adjustment": response["interaction_adjustment"],
                "assumptions": response["assumptions"],
                "main_structural_strength": response["main_structural_strength"],
                "primary_score_limiter": response["primary_score_limiter"],
                "strongest_disconfirming_evidence": response["strongest_disconfirming_evidence"],
                "highest_value_structural_change": response["highest_value_structural_change"],
                "evidence_needed_for_higher_score": response["evidence_needed_for_higher_score"],
                "raw_response_path": raw_rel,
                "raw_response_sha256": raw_digest,
            }
            canonical = compute_evaluation(evaluation_input, manifest, run_dir)
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
        candidate_path = run_dir / candidate_relpath(candidate_id, version)
        if not candidate_path.is_file():
            raise InputError("external import receipt candidate does not exist")
        candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
        if candidate["stage"] != "frozen":
            raise InputError("external import receipt must bind a frozen candidate")
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
                or canonical_evaluation["raw_response_path"] != expected_raw_rel
                or canonical_evaluation["raw_response_sha256"] != raw_digest
            ):
                raise InputError("external import evaluation identity differs from its receipt")
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


def build_final_report(run_dir: Path, manifest: Mapping[str, Any], state: Mapping[str, Any]) -> dict[str, Any]:
    frozen = latest_candidates_for_stage(run_dir, manifest, "frozen")
    if not frozen:
        raise InputError("finalize requires at least one frozen candidate")
    if len(frozen) > manifest["config"]["finalists_max"]:
        raise InputError("frozen candidate count exceeds finalists_max")
    validate_external_imports(run_dir, manifest)
    evaluations = list(iter_evaluations(run_dir, manifest))
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
        if len({item["raw_response_path"] for _, item in native}) != len(native):
            raise InputError(f"candidate {candidate['candidate_id']} native judges must use distinct raw response paths")
        if len({item["raw_response_sha256"] for _, item in native}) != len(native):
            raise InputError(f"candidate {candidate['candidate_id']} native judges must use distinct raw response hashes")
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
    return {
        "schema_version": 1,
        "run_id": state["run_id"],
        "rubric_id": manifest["rubric"]["rubric_id"],
        "rubric_sha256": manifest["rubric"]["sha256"],
        "threshold": manifest["config"]["threshold"],
        "comparison": "strictly_greater_than",
        "run_status": run_status,
        "qualification_label": QUALIFICATION_LABEL if run_status == "qualified" else None,
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_version": selected["candidate_version"],
        "official_score": selected["official_native_score"],
        "binding_score_floor": selected["binding_score_floor"],
        "no_qualifier_reason": None,
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
    preserved: list[tuple[Path, dict[str, Any]]] = []
    for stage in ("frozen", "development", "research", "discovery"):
        preserved = latest_candidates_for_stage(run_dir, manifest, stage)
        if preserved:
            break
    if preserved and preserved[0][1]["stage"] == "frozen":
        for _, candidate in preserved:
            validate_finalist_lineage(run_dir, manifest, candidate)
    selected: tuple[Path, dict[str, Any]] | None = None
    if best_candidate_id is not None:
        candidate_id = expect_nonempty_string(best_candidate_id, "--best-candidate")
        if not SAFE_ID_RE.fullmatch(candidate_id):
            raise InputError("--best-candidate must be a lowercase candidate slug")
        selected = next(
            (item for item in preserved if item[1]["candidate_id"] == candidate_id),
            None,
        )
        if selected is None:
            raise InputError("--best-candidate is not among the strongest current-stage candidates")
    elif len(preserved) == 1:
        selected = preserved[0]
    elif len(preserved) > 1:
        raise ConflictError("early finalization with multiple candidates requires --best-candidate")
    selected_id = selected[1]["candidate_id"] if selected is not None else None
    selected_version = selected[1]["version"] if selected is not None else None
    selected_unresolved = sorted(
        set([*selected[1]["uncertainties"], *selected[1]["contrary_evidence"]])
    ) if selected is not None else []
    reopen_condition = (
        "Reopen only with new evidence that materially resolves: " + "; ".join(selected_unresolved)
        if selected_unresolved
        else f"Reopen only with new evidence that materially resolves the closure reason: {reason}"
    )
    ordered_preserved = sorted(
        preserved,
        key=lambda item: (item[1]["candidate_id"] != selected_id, item[1]["candidate_id"]),
    )
    strongest_candidates = [
        {
            "candidate_id": candidate["candidate_id"],
            "candidate_version": candidate["version"],
            "title": candidate["title"],
            "stage": candidate["stage"],
            "artifact": path.relative_to(run_dir).as_posix(),
            "artifact_sha256": sha256_file(path),
            "risks": candidate["risks"],
            "uncertainties": candidate["uncertainties"],
            "contrary_evidence": candidate["contrary_evidence"],
            "is_selected": candidate["candidate_id"] == selected_id,
            "primary_limiter": reason if candidate["candidate_id"] == selected_id else None,
            "reopen_condition": reopen_condition if candidate["candidate_id"] == selected_id else None,
        }
        for path, candidate in ordered_preserved
    ]
    return {
        "schema_version": 1,
        "run_id": state["run_id"],
        "rubric_id": manifest["rubric"]["rubric_id"],
        "rubric_sha256": manifest["rubric"]["sha256"],
        "threshold": manifest["config"]["threshold"],
        "comparison": "strictly_greater_than",
        "run_status": "no_qualifier",
        "qualification_label": None,
        "selected_candidate_id": selected_id,
        "selected_candidate_version": selected_version,
        "official_score": None,
        "binding_score_floor": None,
        "no_qualifier_reason": reason,
        "binding_limiters": [reason],
        "strongest_candidates": strongest_candidates,
        "unresolved_evidence": selected_unresolved,
        "failed_jobs": _failed_job_summaries(state),
        "candidates": [],
    }


def render_report_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Opportunity Workflow Outcome",
        "",
        f"- Run: `{report['run_id']}`",
        f"- Status: `{report['run_status']}`",
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
    if report.get("no_qualifier_reason"):
        lines.append(f"- Closure reason: {report['no_qualifier_reason']}")
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
    else:
        interpretation = (
            "This run produced no score-qualified candidate under holistic-11. It is an explicit "
            "non-confirmation; preserved candidates and reopen conditions remain research leads, "
            "not market-validated opportunities."
        )
    lines.extend(["", "## Interpretation", "", interpretation, ""])
    return "\n".join(lines)


def _derive_and_validate_final_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    previous_stage: str,
    no_qualifier_reason: str | None,
    selected_candidate_id: str | None,
) -> tuple[dict[str, Any], str]:
    if previous_stage not in STAGES[:-1]:
        raise InputError("run_finalized previous_stage is invalid")
    prior_state = dict(state)
    prior_state["stage"] = previous_stage
    prior_state["run_status"] = "active"
    if no_qualifier_reason is None:
        if previous_stage != "holdout":
            raise InputError("only a holdout-derived final report may omit a closure reason")
        expected = build_final_report(run_dir, manifest, prior_state)
    else:
        reason = expect_nonempty_string(no_qualifier_reason, "run_finalized no_qualifier_reason")
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
    expected_markdown = render_report_markdown(expected).encode("utf-8")
    if markdown_path.read_bytes() != expected_markdown:
        raise InputError("report.md differs from the deterministically derived outcome")
    return expected, sha256_bytes(expected_bytes)


def validate_final_report(
    run_dir: Path,
    manifest: Mapping[str, Any],
    state: Mapping[str, Any],
    finalized_event: Mapping[str, Any],
) -> dict[str, Any]:
    details = expect_object(
        finalized_event["details"],
        "run_finalized details",
        exact_keys=FINAL_EVENT_DETAIL_KEYS,
    )
    report, report_digest = _derive_and_validate_final_report(
        run_dir,
        manifest,
        state,
        details["previous_stage"],
        details["no_qualifier_reason"],
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
    return {
        "previous_stage": previous_stage,
        "run_status": report["run_status"],
        "selected_candidate_id": report["selected_candidate_id"],
        "official_score": report["official_score"],
        "no_qualifier_reason": report["no_qualifier_reason"],
        "report_sha256": report_digest,
    }


def finalize_run(
    run_dir: Path,
    no_qualifier_reason: str | None = None,
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
        if no_qualifier_reason is not None:
            reason = expect_nonempty_string(no_qualifier_reason, "--no-qualifier-reason")
            report = build_early_no_qualifier_report(
                run_dir,
                manifest,
                state,
                reason,
                best_candidate_id,
            )
        else:
            if best_candidate_id is not None:
                raise InputError("--best-candidate requires --no-qualifier-reason")
            if state["stage"] != "holdout":
                raise ConflictError("finalize without --no-qualifier-reason requires holdout stage")
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
        selected = next(
            (
                item
                for item in report.get("candidates", [])
                if item.get("candidate_id") == report.get("selected_candidate_id")
                and item.get("candidate_version") == report.get("selected_candidate_version")
            ),
            None,
        )
        destination = outcomes_dir / state["run_id"]
        with file_lock(outcomes_dir / ".publish.lock", root=outcomes_dir):
            copied: list[dict[str, str]] = []
            sources: list[tuple[Path, str]] = [(report_path, "report.json"), (markdown_path, "report.md")]
            published_candidates: list[tuple[Path, dict[str, Any]]] = []
            if selected is not None:
                candidate_relative = selected["candidate_artifact"]
                candidate_path = run_dir / candidate_relative
                candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
                published_candidates.append((candidate_path, candidate))
                for evaluation in selected["evaluation_artifacts"]:
                    evaluation_rel, evaluation_path = run_relative_path(
                        run_dir, evaluation["path"], "published evaluation path"
                    )
                    canonical_evaluation = compute_evaluation(
                        load_json(evaluation_path), manifest, run_dir
                    )
                    sources.append((evaluation_path, evaluation_rel))
                    raw_rel, raw_path = run_relative_path(
                        run_dir,
                        canonical_evaluation["raw_response_path"],
                        "published evaluation raw response",
                    )
                    sources.append((raw_path, raw_rel))
            else:
                for item in report.get("strongest_candidates", []):
                    candidate_path = run_dir / item["artifact"]
                    candidate = validate_candidate(load_json(candidate_path), manifest, run_dir)
                    published_candidates.append((candidate_path, candidate))
            for candidate_path, candidate in published_candidates:
                candidate_relative = candidate_path.relative_to(run_dir).as_posix()
                sources.append((candidate_path, candidate_relative))
                for research_path, _ in lineage_research_records(
                    run_dir, manifest, candidate, required=False
                ):
                    sources.append((research_path, research_path.relative_to(run_dir).as_posix()))
                export_root = run_dir / "exports" / candidate["candidate_id"]
                if candidate["stage"] == "frozen" and export_root.exists():
                    _external_identity(run_dir, manifest, candidate["candidate_id"])
                for name in ("holdout_packet.md", "response_schema.json"):
                    export_path = export_root / name
                    if export_path.is_file():
                        sources.append((export_path, export_path.relative_to(run_dir).as_posix()))
                for receipt_path, receipt, _ in import_receipts:
                    receipt_parts = receipt_path.relative_to(run_dir).parts
                    if receipt["candidate_id"] != candidate["candidate_id"] or receipt_parts[2] != f"v{candidate['version']}":
                        continue
                    sources.append((receipt_path, receipt_path.relative_to(run_dir).as_posix()))
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
                digest = write_immutable(destination / relative, data, root=destination)
                copied.append({"path": relative, "sha256": digest})
            history_path = knowledge_dir / "history_index.jsonl"
            entries: list[dict[str, Any]] = []
            if history_path.exists():
                for line_number, line in enumerate(history_path.read_text(encoding="utf-8").splitlines(), start=1):
                    if not line.strip():
                        raise InputError(f"blank line in history index at {line_number}")
                    entry = expect_object(parse_json(line, source=f"{history_path}:{line_number}"), "history entry")
                    entries.append(entry)
            existing = [entry for entry in entries if entry.get("run_id") == state["run_id"]]
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
                else report.get("no_qualifier_reason")
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
                "record_type": "opportunity_outcome_v1",
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
            }, "published opportunity history entry", exact_keys=OUTCOME_HISTORY_KEYS)
            if existing and existing != [history_entry]:
                raise ConflictError("knowledge history contains a conflicting run entry")
            if not existing:
                entries.append(history_entry)
                history_data = "".join(
                    json.dumps(entry, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
                    for entry in entries
                ).encode("utf-8")
                atomic_write(history_path, history_data, root=knowledge_dir)
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
            return {
                "run_id": state["run_id"],
                "run_status": state["run_status"],
                "outcome_dir": str(destination),
                "history": str(history_path),
                "artifacts": copied,
                "idempotent": bool(existing),
            }


def validate_artifact(run_dir: Path, input_path: Path, kind: str) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    if kind == "candidate":
        candidate = validate_candidate(load_json(input_path), manifest, run_dir)
        return {
            "valid": True,
            "kind": kind,
            "candidate_id": candidate["candidate_id"],
            "version": candidate["version"],
            "canonical_path": candidate_relpath(candidate["candidate_id"], candidate["version"]),
        }
    if kind == "evaluation":
        evaluation = compute_evaluation(load_json(input_path), manifest, run_dir)
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
    validate_generic_input(input_path, kind)
    return {"valid": True, "kind": kind, "input": str(input_path), "stage": state["stage"]}


def status_run(run_dir: Path, full_json: bool) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    if full_json:
        return {"manifest": manifest, "state": state}
    counts = {status: 0 for status in sorted(JOB_STATUSES)}
    for stage_jobs in state["jobs"].values():
        for job in stage_jobs.values():
            counts[job["status"]] += 1
    return {
        "run_id": state["run_id"],
        "stage": state["stage"],
        "run_status": state["run_status"],
        "current_stage_blockers": current_stage_blockers(state) if state["stage"] != "complete" else [],
        "job_counts": counts,
    }


def check_run(run_dir: Path, config_path: Path | None = None) -> dict[str, Any]:
    manifest, state = load_run(run_dir)
    events, finalized_event = require_event_state_match(run_dir, state, manifest)
    if state["stage"] != "complete" and (
        (run_dir / "final" / "report.json").exists() or (run_dir / "report.md").exists()
    ):
        raise InputError("active run contains unreconciled finalization artifacts")
    checked: list[str] = ["manifest.json", "state.json", "events.jsonl"]
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
    for _, candidate in stored_candidates:
        if candidate["stage"] == "frozen":
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
        for _, candidate in latest_candidates_for_stage(run_dir, manifest, "frozen"):
            _external_identity(run_dir, manifest, candidate["candidate_id"])
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
        if not current_path.is_file() or sha256_file(current_path) != pinned_hash:
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
    return {
        "valid": True,
        "config": str(config_path),
        "schema_version": config["schema_version"],
        "rubric_id": config["rubric_id"],
        "rubric_sha256": digest,
        "factor_count": len(factors),
        "weight_total": decimal_json(sum((weight for _, weight in factors), Decimal(0))),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="workflow config path")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR, help="run storage directory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("new", help="create a new immutable run manifest")

    status = subparsers.add_parser("status", help="show run status")
    status.add_argument("run")
    status.add_argument("--json", action="store_true", help="include complete manifest and state")

    resume = subparsers.add_parser("resume", help="recover interrupted jobs and list eligible retries")
    resume.add_argument("run")

    job = subparsers.add_parser("job", help="start, complete, or fail one mechanical job")
    job.add_argument("run")
    job.add_argument("job_id")
    job.add_argument("action", choices=("start", "complete", "fail"))
    job.add_argument("--stage", choices=STAGES)
    job.add_argument("--input", type=Path)
    job.add_argument("--kind", choices=("candidate", "research", "evaluation", "generic"))
    job.add_argument("--error")

    validate = subparsers.add_parser("validate", help="validate an artifact without storing it")
    validate.add_argument("run")
    validate.add_argument("--input", type=Path, required=True)
    validate.add_argument("--kind", choices=("candidate", "research", "evaluation", "generic"), required=True)

    dedup = subparsers.add_parser("dedup", help="deduplicate discovery candidates by structural fingerprint")
    dedup.add_argument("run")

    advance = subparsers.add_parser("advance", help="advance after all current-stage jobs are terminal")
    advance.add_argument("run")

    export = subparsers.add_parser("export-external", help="write a deterministic external holdout packet")
    export.add_argument("run")
    export.add_argument("candidate_id")

    import_parser = subparsers.add_parser("import-external", help="preserve and import one external response")
    import_parser.add_argument("run")
    import_parser.add_argument("candidate_id")
    import_parser.add_argument("raw_response", type=Path)

    finalize = subparsers.add_parser("finalize", help="apply native and binding external score gates")
    finalize.add_argument("run")
    finalize.add_argument("--no-qualifier-reason")
    finalize.add_argument("--best-candidate")

    publish = subparsers.add_parser("publish", help="publish any terminal outcome idempotently")
    publish.add_argument("run")

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
    if args.command == "new":
        emit(make_run(config_path, runs_dir))
        return 0
    if args.command == "check" and args.run is None:
        emit(check_environment(config_path))
        return 0
    run_dir = resolve_run(runs_dir, args.run)
    if args.command == "status":
        emit(status_run(run_dir, args.json))
        return 0
    if args.command == "resume":
        emit(resume_run(run_dir))
        return 0
    if args.command == "job":
        if args.action == "start":
            if args.input is not None or args.kind is not None or args.error is not None:
                raise InputError("job start accepts only optional --stage")
            emit(start_job(run_dir, args.job_id, args.stage))
            return 0
        if args.stage is not None:
            raise InputError("--stage is valid only for job start")
        if args.action == "complete":
            if args.input is None or args.kind is None or args.error is not None:
                raise InputError("job complete requires --input and --kind, and does not accept --error")
            emit(complete_job(run_dir, args.job_id, args.input.resolve(), args.kind))
            return 0
        if args.error is None or args.input is not None or args.kind is not None:
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
    if args.command == "import-external":
        emit(import_external(run_dir, args.candidate_id, args.raw_response.resolve()))
        return 0
    if args.command == "finalize":
        result, code = finalize_run(run_dir, args.no_qualifier_reason, args.best_candidate)
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
