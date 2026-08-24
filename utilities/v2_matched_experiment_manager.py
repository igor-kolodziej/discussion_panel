#!/usr/bin/env python3
"""Create and maintain the non-routing V2 matched generation experiment.

This helper writes only run-scoped experiment artifacts and independent trust
files.  It never evaluates, validates, pivots, routes, or confirms candidates.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


WORKSPACE = Path("/Users/igor/Desktop/discussion_panel")
WORKING_FOLDER = WORKSPACE / "working_folder"
ANCHOR_ROOT = WORKSPACE / "audit_anchors"
AUDITOR = Path(
    "/Users/igor/.codex/skills/generate-zero-to-one-candidates/scripts/audit_funnel.py"
)
PROTOCOL = Path(
    "/Users/igor/.codex/skills/generate-zero-to-one-candidates/references/blind-search-protocol.md"
)
MODEL = "gpt-5.6-sol"
REASONING = "high"
ROOT_SCOPE_ID = "baseline-w01"
CHILD_SCOPE_ID = "shadow-w01"
CHILD_RELATIVE_PATH = "shadow_archipelago_lite"
LOCAL_TZ = ZoneInfo("Europe/Warsaw")

STAMP_PATTERN = re.compile(r"\A\d{8}_\d{6}\Z")
SEED_PATTERN = re.compile(r"\Av2-matched-[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?\Z")
SEED_MIN_LENGTH = 16
SEED_MAX_LENGTH = 128
SEED_RESERVATION_DIRNAME = ".v2_seed_reservations"
SEED_RESERVATION_SCHEMA = "zt1-v2-seed-reservation-v2"
RUN_REGISTRATION_DIRNAME = ".v2_run_registrations"
RUN_REGISTRATION_SCHEMA = "zt1-v2-run-registration-v1"
REGISTRATION_RECEIPT_SCHEMA = "zt1-v2-matched-registration-receipt-v3"

_JSON_STRING_LITERAL_PATTERN = (
    r'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"'
)
_APPLY_PATCH_LONG_WRAPPER_RE = re.compile(
    r"\A[ \t\r\n]*const[ \t\r\n]+patch[ \t\r\n]*=[ \t\r\n]*"
    rf"(?P<patch_literal>{_JSON_STRING_LITERAL_PATTERN})"
    r"[ \t\r\n]*;[ \t\r\n]*"
    r"const[ \t\r\n]+result[ \t\r\n]*=[ \t\r\n]*"
    r"await[ \t\r\n]+tools[ \t\r\n]*\.[ \t\r\n]*apply_patch[ \t\r\n]*"
    r"\([ \t\r\n]*patch[ \t\r\n]*\)[ \t\r\n]*;[ \t\r\n]*"
    r"text[ \t\r\n]*\([ \t\r\n]*result[ \t\r\n]*\)"
    r"[ \t\r\n]*;[ \t\r\n]*\Z"
)
_APPLY_PATCH_INLINE_AWAIT_WRAPPER_RE = re.compile(
    r"\A[ \t\r\n]*const[ \t\r\n]+patch[ \t\r\n]*=[ \t\r\n]*"
    rf"(?P<patch_literal>{_JSON_STRING_LITERAL_PATTERN})"
    r"[ \t\r\n]*;[ \t\r\n]*"
    r"text[ \t\r\n]*\([ \t\r\n]*"
    r"await[ \t\r\n]+tools[ \t\r\n]*\.[ \t\r\n]*apply_patch[ \t\r\n]*"
    r"\([ \t\r\n]*patch[ \t\r\n]*\)[ \t\r\n]*"
    r"\)[ \t\r\n]*;[ \t\r\n]*\Z"
)
CANONICAL_BOUNDED_RETURN_WRAPPER = """const patch = "<JSON-encoded complete patch beginning with the exact absolute header above>";
const result = await tools.apply_patch(patch);
text(result);"""
_REQUIRED_RETURN_PATH_LINE_RE = re.compile(
    r"(?im)^.*\brequired[ \t]+return[ \t]+path[ \t]*:.*$"
)
_ADD_FILE_INSTRUCTION_LINE_RE = re.compile(
    r"(?m)^.*\*\*\*[ \t]+Add[ \t]+File[ \t]*:.*$"
)
_OUTPUT_PATH_PLACEHOLDER_RE = re.compile(
    r"(?:"
    r"<[^>\r\n]*(?:OUTPUT|RETURN|TARGET|DESTINATION|PATH|FILE)[^>\r\n]*>"
    r"|\{[^}\r\n]*(?:OUTPUT|RETURN|TARGET|DESTINATION|PATH|FILE)[^}\r\n]*\}"
    r"|\$\{?[A-Z0-9_]*(?:OUTPUT|RETURN|TARGET|DESTINATION|PATH|FILE)[A-Z0-9_]*\}?"
    r")",
    re.IGNORECASE,
)
_PATCH_OPERATION_PRESENTATION_RE = re.compile(
    r"(?i)(?:(?:\*|\\\*|&(?:#0*42|#x0*2a|ast);|\u2217|\uff0a)){3}[ \t]+"
)
_RESIDUAL_RETURN_ALTERNATIVE_RE = re.compile(
    r"(?im)^.*(?:"
    r"\b(?:output|return)[ \t]+path\b[ \t]*:"
    r"|\b(?:write|save)[ \t]+(?:path|target|destination)\b[ \t]*:"
    r"|\b(?:write|save)[ \t]+(?:the[ \t]+)?(?:output[ \t]+)?(?:to|at)\b"
    r").*$"
)
_EXEC_COMMAND_PREFIX_RE = re.compile(
    r"\A[ \t\r\n]*const[ \t\r\n]+r[ \t\r\n]*=[ \t\r\n]*"
    r"await[ \t\r\n]+tools[ \t\r\n]*\.[ \t\r\n]*exec_command"
    r"[ \t\r\n]*\([ \t\r\n]*"
)
_EXEC_COMMAND_SUFFIX_RE = re.compile(
    r"[ \t\r\n]*\)[ \t\r\n]*;[ \t\r\n]*"
    r"text[ \t\r\n]*\([ \t\r\n]*r[ \t\r\n]*\.[ \t\r\n]*output"
    r"[ \t\r\n]*\)[ \t\r\n]*;[ \t\r\n]*\Z"
)
_EXEC_COMMAND_WRAPPER_RE = re.compile(
    _EXEC_COMMAND_PREFIX_RE.pattern
    + r"\{[ \t\r\n]*(?:cmd|\"cmd\")[ \t\r\n]*:"
    + rf"[ \t\r\n]*(?P<cmd>{_JSON_STRING_LITERAL_PATTERN})"
    + r"(?:[ \t\r\n]*,[ \t\r\n]*(?:workdir|\"workdir\")"
    + rf"[ \t\r\n]*:[ \t\r\n]*(?P<workdir>{_JSON_STRING_LITERAL_PATTERN}))?"
    + r"(?:[ \t\r\n]*,[ \t\r\n]*\"yield_time_ms\"[ \t\r\n]*:"
    + r"[ \t\r\n]*(?P<yield_time_ms>0|[1-9][0-9]*))?"
    + r"(?:[ \t\r\n]*,[ \t\r\n]*(?:max_output_tokens|\"max_output_tokens\")"
    + r"[ \t\r\n]*:[ \t\r\n]*(?P<max_output_tokens>0|[1-9][0-9]*))?"
    + r"[ \t\r\n]*\}"
    + _EXEC_COMMAND_SUFFIX_RE.pattern.removeprefix(r"\A")
)
_WEB_CALL_PREFIX_PATTERN = (
    r"\A[ \t\r\n]*const[ \t\r\n]+r[ \t\r\n]*=[ \t\r\n]*"
    r"await[ \t\r\n]+tools[ \t\r\n]*\.[ \t\r\n]*web__run"
    r"[ \t\r\n]*\([ \t\r\n]*"
)
_WEB_CALL_SUFFIX_PATTERN = (
    r"[ \t\r\n]*\)[ \t\r\n]*;[ \t\r\n]*"
    r"text[ \t\r\n]*\([ \t\r\n]*"
    r"(?:r|JSON[ \t\r\n]*\.[ \t\r\n]*stringify[ \t\r\n]*"
    r"\([ \t\r\n]*r[ \t\r\n]*\))"
    r"[ \t\r\n]*\)"
    r"[ \t\r\n]*;?[ \t\r\n]*\Z"
)
_WEB_SEARCH_WRAPPER_RE = re.compile(
    _WEB_CALL_PREFIX_PATTERN
    + r"\{[ \t\r\n]*(?:search_query|\"search_query\")[ \t\r\n]*:"
    + r"[ \t\r\n]*\[[ \t\r\n]*\{[ \t\r\n]*(?:q|\"q\")"
    + r"[ \t\r\n]*:[ \t\r\n]*"
    + rf"(?P<query>{_JSON_STRING_LITERAL_PATTERN})"
    + r"[ \t\r\n]*\}[ \t\r\n]*\][ \t\r\n]*,[ \t\r\n]*"
    + r"(?:response_length|\"response_length\")[ \t\r\n]*:"
    + rf"[ \t\r\n]*(?P<length>{_JSON_STRING_LITERAL_PATTERN})"
    + r"[ \t\r\n]*\}"
    + _WEB_CALL_SUFFIX_PATTERN
)
_WEB_OPEN_WRAPPER_RE = re.compile(
    _WEB_CALL_PREFIX_PATTERN
    + r"\{[ \t\r\n]*(?:open|\"open\")[ \t\r\n]*:"
    + r"[ \t\r\n]*\[[ \t\r\n]*\{[ \t\r\n]*(?:ref_id|\"ref_id\")"
    + r"[ \t\r\n]*:[ \t\r\n]*"
    + rf"(?P<ref_id>{_JSON_STRING_LITERAL_PATTERN})"
    + r"[ \t\r\n]*\}[ \t\r\n]*\][ \t\r\n]*,[ \t\r\n]*"
    + r"(?:response_length|\"response_length\")[ \t\r\n]*:"
    + rf"[ \t\r\n]*(?P<length>{_JSON_STRING_LITERAL_PATTERN})"
    + r"[ \t\r\n]*\}"
    + _WEB_CALL_SUFFIX_PATTERN
)

FIXED_PATHS = {
    "founder-profile": WORKSPACE / "PERSONALITY_SITUATION.md",
    "success-safety-contract": WORKSPACE / "COMMUNICATION_AND_GENERAL_RULES.md",
    "goal": WORKSPACE / "prompts/NEW_IDEA_GOAL.md",
    "validator": WORKSPACE / "Personalities/ZeroToOne.txt",
    "orchestration-prompt": WORKSPACE / "prompts/NEW_IDEA_AGENT_PROMPT.md",
    "generator-skill": Path(
        "/Users/igor/.codex/skills/generate-zero-to-one-candidates/SKILL.md"
    ),
    "evaluator-skill": Path(
        "/Users/igor/.codex/skills/evaluate-zero-to-one/SKILL.md"
    ),
    "pivot-skill": Path(
        "/Users/igor/.codex/skills/pivot-zero-to-one/SKILL.md"
    ),
}

WORKFLOW_PATHS = {
    "audit-funnel": AUDITOR,
    "blind-search-protocol": PROTOCOL,
    "v2-candidate-development": WORKSPACE / "utilities/v2_candidate_development.py",
    "v2-matched-experiment-manager": Path(__file__).resolve(),
}

BASELINE_ROLES = [
    "taboo_space_explorer",
    "incentive_hacker",
    "incumbent_attacker",
    "rule_structure_analyst",
    "first_principles_extremist",
]

BASELINE_AGENT_IDS = {
    "taboo_space_explorer": "baseline-gen-tse",
    "incentive_hacker": "baseline-gen-ih",
    "incumbent_attacker": "baseline-gen-ia",
    "rule_structure_analyst": "baseline-gen-rsa",
    "first_principles_extremist": "baseline-gen-fpe",
}

SHADOW_SCOUTS = [
    ("customer_workarounds", "shadow-scout-cw"),
    ("spend_procurement", "shadow-scout-sp"),
    ("operational_failure", "shadow-scout-of"),
    ("incumbent_economics_channels", "shadow-scout-iec"),
    ("technical_scientific_change", "shadow-scout-tsc"),
    ("rules_finance_assets_transitions", "shadow-scout-rfat"),
]

BASELINE_PACKET_PATHS = [
    *(f"context/{agent_id}.md" for agent_id in BASELINE_AGENT_IDS.values()),
    "context/baseline-history-01.md",
    "context/baseline-cartography-01.md",
    "context/baseline-cluster-audit-01.md",
    "context/baseline-level1-01.md",
    *(f"context/baseline-level2-{index:02d}.md" for index in range(1, 13)),
    *(f"context/baseline-fact-closure-{index:02d}.md" for index in range(1, 7)),
]

SHADOW_PACKET_PATHS = [
    *(f"context/{agent_id}.md" for _, agent_id in SHADOW_SCOUTS),
    "context/shadow-builder-01.md",
    "context/shadow-builder-02.md",
    "context/shadow-builder-03.md",
    "context/shadow-inverter-01.md",
    "context/shadow-inverter-02.md",
    "context/shadow-recombiner-01.md",
    "context/shadow-recombiner-02.md",
    "context/shadow-history-01.md",
    "context/shadow-cartography-01.md",
    "context/shadow-cluster-audit-01.md",
    "context/shadow-level1-01.md",
    "context/shadow-provisional-selector-01.md",
    "context/shadow-commercial-ranker-01.md",
    "context/shadow-economics-ranker-01.md",
    "context/shadow-tail-challenger-01.md",
    *(f"context/shadow-level2-{index:02d}.md" for index in range(1, 13)),
    "context/shadow-finalist-selector-01.md",
    *(f"context/shadow-fact-closure-{index:02d}.md" for index in range(1, 7)),
]

DOSSIER_SECTIONS = [
    "## Customer Loss And Payer Evidence",
    "## Proposed Transaction And Paid Trigger",
    "## Acquisition Route",
    "## Incumbent Substitute And Route-Around",
    "## Unit Economics And Sensitivity",
    "## Control Point Or Compounding Asset",
    "## Execution Dependencies And Cheapest Proof",
    "## Decision-Critical Unknowns And Contradictions",
    "## Evidence And Sources",
]
COUNTED_DOSSIER_KEYS = [
    "customer_loss_and_payer_evidence",
    "proposed_transaction_and_paid_trigger",
    "acquisition_route",
    "incumbent_substitute_and_route_around",
    "unit_economics_and_sensitivity",
    "control_point_or_compounding_asset",
    "execution_dependencies_and_cheapest_proof",
    "decision_critical_unknowns_and_contradictions",
]
DOSSIER_KEYS = [*COUNTED_DOSSIER_KEYS, "evidence_and_sources"]
LEVEL2_CAPS = {
    "uncached_input_tokens": 112_000,
    "output_tokens": 20_000,
    "elapsed_minutes": 15,
}
FACT_CLOSURE_CAPS = {
    "uncached_input_tokens": 96_000,
    "output_tokens": 20_000,
    "elapsed_minutes": 12,
}
DEVELOPMENT_LIVE_STOP_THRESHOLDS = {
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
DEVELOPMENT_METERING_MONITOR = {
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


def now() -> datetime:
    return datetime.now(LOCAL_TZ)


def iso(value: datetime) -> str:
    return value.isoformat(timespec="microseconds")


def json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jsonl_bytes(records: list[dict[str, Any]]) -> bytes:
    return ("\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n").encode(
        "utf-8"
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def read_live_jsonl_prefix(path: Path) -> list[dict[str, Any]]:
    """Parse only newline-terminated records from a concurrently written trace."""
    payload = path.read_bytes()
    if not payload.endswith(b"\n"):
        payload = payload.rsplit(b"\n", 1)[0] if b"\n" in payload else b""
    if not payload:
        return []
    records: list[dict[str, Any]] = []
    for line in payload.decode("utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            if not isinstance(record, dict):
                raise RuntimeError(f"live trace record is not an object: {path}")
            records.append(record)
    return records


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _absolute_lexical(path: Path) -> Path:
    """Return an absolute normalized path without resolving symlinks."""
    return Path(os.path.abspath(os.fspath(path)))


def _configured_boundary(path: Path) -> Path | None:
    target = _absolute_lexical(path)
    for configured in (WORKING_FOLDER, ANCHOR_ROOT):
        boundary = _absolute_lexical(configured)
        try:
            target.relative_to(boundary)
        except ValueError:
            continue
        return boundary
    return None


def _directory_open_flags() -> int:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    return flags


def _safe_parent_descriptor(path: Path, *, create: bool) -> tuple[int, str]:
    """Open a parent without following run-owned symlink components."""
    target = _absolute_lexical(path)
    if target.name in {"", ".", ".."}:
        raise RuntimeError(f"unsafe artifact path: {path}")
    boundary = _configured_boundary(target)
    if boundary is None:
        parent = target.parent
        if create:
            parent.mkdir(parents=True, exist_ok=True)
        if parent.is_symlink() or not parent.is_dir():
            raise RuntimeError(f"artifact parent is missing or unsafe: {parent}")
        return os.open(parent, _directory_open_flags()), target.name

    if boundary.is_symlink() or not boundary.is_dir():
        raise RuntimeError(f"configured artifact root is missing or unsafe: {boundary}")
    try:
        relative_parent = target.parent.relative_to(boundary)
    except ValueError as exc:
        raise RuntimeError(f"artifact path escapes its configured root: {path}") from exc
    descriptor = os.open(boundary, _directory_open_flags())
    try:
        for component in relative_parent.parts:
            if component in {"", ".", ".."}:
                raise RuntimeError(f"artifact path has an unsafe component: {path}")
            if create:
                try:
                    os.mkdir(component, mode=0o700, dir_fd=descriptor)
                except FileExistsError:
                    pass
            next_descriptor = os.open(
                component,
                _directory_open_flags(),
                dir_fd=descriptor,
            )
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor, target.name
    except Exception:
        os.close(descriptor)
        raise


def ensure_safe_directory(path: Path, *, exist_ok: bool = True) -> Path:
    target = _absolute_lexical(path)
    boundary = _configured_boundary(target)
    if boundary == target:
        if not exist_ok:
            raise FileExistsError(target)
        if target.is_symlink() or not target.is_dir():
            raise RuntimeError(f"directory is missing or unsafe: {target}")
        return target
    parent_descriptor, name = _safe_parent_descriptor(target, create=True)
    try:
        try:
            os.mkdir(name, mode=0o700, dir_fd=parent_descriptor)
        except FileExistsError:
            if not exist_ok:
                raise
        child_descriptor = os.open(
            name,
            _directory_open_flags(),
            dir_fd=parent_descriptor,
        )
        os.close(child_descriptor)
    finally:
        os.close(parent_descriptor)
    return target


def write_exclusive(path: Path, data: bytes) -> None:
    parent_descriptor, name = _safe_parent_descriptor(path, create=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(name, flags, 0o600, dir_fd=parent_descriptor)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
    finally:
        os.close(parent_descriptor)


def write_exclusive_or_verify(path: Path, data: bytes) -> None:
    if path.exists() or path.is_symlink():
        _require_safe_file(path, "immutable artifact")
        if path.read_bytes() != data:
            raise RuntimeError(f"existing immutable artifact differs: {path}")
        return
    write_exclusive(path, data)


def write_replace(path: Path, data: bytes) -> None:
    parent_descriptor, name = _safe_parent_descriptor(path, create=False)
    temporary_name = f".{name}.new-{os.getpid()}-{os.urandom(8).hex()}"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    temporary_created = False
    try:
        descriptor = os.open(
            temporary_name,
            flags,
            0o600,
            dir_fd=parent_descriptor,
        )
        temporary_created = True
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        try:
            target_status = os.stat(
                name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            target_status = None
        if target_status is not None and not stat.S_ISREG(target_status.st_mode):
            raise RuntimeError(f"replacement target is unsafe: {path}")
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_descriptor,
            dst_dir_fd=parent_descriptor,
        )
        temporary_created = False
    finally:
        if temporary_created:
            try:
                os.unlink(temporary_name, dir_fd=parent_descriptor)
            except FileNotFoundError:
                pass
        os.close(parent_descriptor)


def validate_stamp(stamp: str) -> str:
    if not isinstance(stamp, str) or STAMP_PATTERN.fullmatch(stamp) is None:
        raise RuntimeError("stamp must be YYYYMMDD_HHMMSS")
    return stamp


def validate_seed(seed: str) -> str:
    if not isinstance(seed, str):
        raise RuntimeError("seed must be an explicit string")
    if not SEED_MIN_LENGTH <= len(seed) <= SEED_MAX_LENGTH:
        raise RuntimeError(
            f"seed length must be between {SEED_MIN_LENGTH} and {SEED_MAX_LENGTH} ASCII characters"
        )
    if SEED_PATTERN.fullmatch(seed) is None:
        raise RuntimeError(
            "seed must match v2-matched-[a-z0-9][a-z0-9_-]*[a-z0-9]"
        )
    return seed


def _require_safe_directory(path: Path, label: str) -> Path:
    target = _absolute_lexical(path)
    boundary = _configured_boundary(target)
    if boundary == target:
        if target.is_symlink() or not target.is_dir():
            raise RuntimeError(f"{label} is missing or unsafe: {path}")
        return target.resolve()
    try:
        parent_descriptor, name = _safe_parent_descriptor(target, create=False)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        raise RuntimeError(f"{label} is missing or unsafe: {path}") from exc
    try:
        descriptor = os.open(
            name,
            _directory_open_flags(),
            dir_fd=parent_descriptor,
        )
        os.close(descriptor)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        raise RuntimeError(f"{label} is missing or unsafe: {path}") from exc
    finally:
        os.close(parent_descriptor)
    return target.resolve()


def _require_safe_file(path: Path, label: str) -> Path:
    target = _absolute_lexical(path)
    try:
        parent_descriptor, name = _safe_parent_descriptor(target, create=False)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        raise RuntimeError(f"{label} is missing or unsafe: {path}") from exc
    try:
        try:
            entry = os.stat(
                name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except (FileNotFoundError, OSError) as exc:
            raise RuntimeError(f"{label} is missing or unsafe: {path}") from exc
        if not stat.S_ISREG(entry.st_mode):
            raise RuntimeError(f"{label} is missing or unsafe: {path}")
    finally:
        os.close(parent_descriptor)
    return target


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    _require_safe_file(path, label)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{label} is unreadable or malformed: {path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{label} is not a JSON object: {path}")
    return payload


def _read_v2_run_record(path: Path) -> dict[str, Any] | None:
    _require_safe_file(path, "canonical run manifest")
    try:
        records = read_jsonl(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"canonical run manifest is unreadable or malformed: {path}") from exc
    if not records or records[0].get("record_type") != "run":
        raise RuntimeError(f"canonical run manifest lacks a first run record: {path}")
    run_record = records[0]
    if run_record.get("schema") != "zt1-generation-run-v2":
        return None
    for field in ("seed", "candidate_order_seed"):
        if not isinstance(run_record.get(field), str) or not run_record[field]:
            raise RuntimeError(f"canonical V2 run record lacks {field}: {path}")
    return run_record


def _canonical_registration_receipts() -> list[Path]:
    anchor_root = _require_safe_directory(ANCHOR_ROOT, "audit-anchor root")
    receipts: list[Path] = []
    for candidate in sorted(anchor_root.iterdir(), key=lambda path: path.name):
        if re.fullmatch(r"v2_matched_\d{8}_\d{6}", candidate.name) is None:
            continue
        if candidate.is_symlink() or not candidate.is_dir():
            raise RuntimeError(f"canonical V2 trust directory is unsafe: {candidate}")
        receipt = candidate / "registration_receipt.json"
        _require_safe_file(receipt, "canonical V2 registration receipt")
        receipts.append(receipt)
    return receipts


def _canonical_v2_run_manifests() -> list[Path]:
    working_root = _require_safe_directory(WORKING_FOLDER, "working-folder root")
    manifests: list[Path] = []
    for candidate in sorted(working_root.iterdir(), key=lambda path: path.name):
        if re.fullmatch(r"zero_to_one_candidates_\d{8}_\d{6}", candidate.name) is None:
            continue
        if candidate.is_symlink() or not candidate.is_dir():
            raise RuntimeError(f"canonical run directory is unsafe: {candidate}")
        child = candidate / CHILD_RELATIVE_PATH
        if child.is_symlink():
            raise RuntimeError(f"canonical child directory is unsafe: {child}")
        if child.exists() and not child.is_dir():
            raise RuntimeError(f"canonical child path is not a directory: {child}")
        for manifest in (
            candidate / "00a_context_and_resource_manifest.jsonl",
            child / "00a_context_and_resource_manifest.jsonl",
        ):
            if manifest.is_symlink():
                raise RuntimeError(f"canonical run manifest is unsafe: {manifest}")
            if manifest.is_file() and _read_v2_run_record(manifest) is not None:
                manifests.append(manifest)
    return manifests


def seed_reservation_path(seed: str) -> Path:
    validated = validate_seed(seed)
    digest = sha256_bytes(validated.encode("utf-8"))
    return ANCHOR_ROOT / SEED_RESERVATION_DIRNAME / f"{digest}.json"


def run_registration_path(stamp: str) -> Path:
    validated_stamp = validate_stamp(stamp)
    run_id = f"zero_to_one_candidates_{validated_stamp}"
    digest = sha256_bytes(run_id.encode("utf-8"))
    return ANCHOR_ROOT / RUN_REGISTRATION_DIRNAME / f"{digest}.json"


@contextlib.contextmanager
def registration_mutex() -> Any:
    """Serialize the dual seed/run reservation transaction."""
    anchor_root = _require_safe_directory(ANCHOR_ROOT, "audit-anchor root")
    lock_path = anchor_root / ".v2_registration.lock"
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _canonical_seed_reservations() -> list[Path]:
    reservation_dir = ANCHOR_ROOT / SEED_RESERVATION_DIRNAME
    if reservation_dir.is_symlink():
        raise RuntimeError(f"seed-reservation directory is unsafe: {reservation_dir}")
    if not reservation_dir.exists():
        return []
    if not reservation_dir.is_dir():
        raise RuntimeError(f"seed-reservation path is not a directory: {reservation_dir}")
    reservations: list[Path] = []
    for candidate in sorted(reservation_dir.iterdir(), key=lambda path: path.name):
        if re.fullmatch(r"[0-9a-f]{64}\.json", candidate.name) is None:
            raise RuntimeError(f"unexpected seed-reservation entry: {candidate}")
        _require_safe_file(candidate, "seed reservation")
        reservations.append(candidate)
    return reservations


def _canonical_run_registrations() -> list[Path]:
    registration_dir = ANCHOR_ROOT / RUN_REGISTRATION_DIRNAME
    if registration_dir.is_symlink():
        raise RuntimeError(f"run-registration directory is unsafe: {registration_dir}")
    if not registration_dir.exists():
        return []
    _require_safe_directory(registration_dir, "run-registration directory")
    registrations: list[Path] = []
    for candidate in sorted(registration_dir.iterdir(), key=lambda path: path.name):
        if re.fullmatch(r"[0-9a-f]{64}\.json", candidate.name) is None:
            raise RuntimeError(f"unexpected run-registration entry: {candidate}")
        _require_safe_file(candidate, "run registration")
        registrations.append(candidate)
    return registrations


def _seed_occurrences() -> list[tuple[Path, str, str]]:
    occurrences: list[tuple[Path, str, str]] = []
    for path in _canonical_registration_receipts():
        receipt = _read_json_object(path, "canonical V2 registration receipt")
        schema = receipt.get("schema")
        if not isinstance(schema, str) or not schema.startswith(
            "zt1-v2-matched-registration-receipt-v"
        ):
            raise RuntimeError(f"canonical V2 registration receipt has an invalid schema: {path}")
        if not isinstance(receipt.get("seed"), str) or not receipt["seed"]:
            raise RuntimeError(f"canonical V2 registration receipt lacks seed: {path}")
        occurrences.append((path, "seed", receipt["seed"]))
        candidate_seed = receipt.get("candidate_order_seed")
        if candidate_seed is not None:
            if not isinstance(candidate_seed, str) or not candidate_seed:
                raise RuntimeError(
                    f"canonical V2 registration receipt has invalid candidate_order_seed: {path}"
                )
            occurrences.append((path, "candidate_order_seed", candidate_seed))
    for path in _canonical_v2_run_manifests():
        run_record = _read_v2_run_record(path)
        if run_record is None:
            continue
        occurrences.extend(
            (path, field, run_record[field])
            for field in ("seed", "candidate_order_seed")
        )
    for path in _canonical_seed_reservations():
        reservation = _read_json_object(path, "seed reservation")
        if reservation.get("schema") not in {
            "zt1-v2-seed-reservation-v1",
            SEED_RESERVATION_SCHEMA,
        }:
            raise RuntimeError(f"seed reservation has an invalid schema: {path}")
        reserved_seed = validate_seed(reservation.get("seed"))
        if (
            reservation.get("candidate_order_seed") != reserved_seed
            or path.name != seed_reservation_path(reserved_seed).name
        ):
            raise RuntimeError(
                f"seed reservation filename or candidate-order seed is inconsistent: {path}"
            )
        for field in ("seed", "candidate_order_seed"):
            if not isinstance(reservation.get(field), str) or not reservation[field]:
                raise RuntimeError(f"seed reservation lacks {field}: {path}")
            occurrences.append((path, field, reservation[field]))
    for path in _canonical_run_registrations():
        registration = _read_json_object(path, "run registration")
        if registration.get("schema") != RUN_REGISTRATION_SCHEMA:
            raise RuntimeError(f"run registration has an invalid schema: {path}")
        run_id = registration.get("run_id")
        if not isinstance(run_id, str):
            raise RuntimeError(f"run registration lacks run_id: {path}")
        match = re.fullmatch(r"zero_to_one_candidates_(\d{8}_\d{6})", run_id)
        if match is None or path.name != run_registration_path(match.group(1)).name:
            raise RuntimeError(
                f"run registration filename does not match its run ID: {path}"
            )
        for field in ("seed", "candidate_order_seed"):
            if not isinstance(registration.get(field), str) or not registration[field]:
                raise RuntimeError(f"run registration lacks {field}: {path}")
            occurrences.append((path, field, registration[field]))
    return occurrences


def assert_seed_unused(seed: str, *, allowed_paths: set[Path] | None = None) -> None:
    validated = validate_seed(seed)
    allowed = {
        path.resolve(strict=False) for path in (allowed_paths if allowed_paths is not None else set())
    }
    conflicts = sorted(
        {
            str(path)
            for path, _field, value in _seed_occurrences()
            if value == validated and path.resolve(strict=False) not in allowed
        }
    )
    if conflicts:
        raise RuntimeError(
            f"seed is already reserved or registered: {validated}; conflicts: {', '.join(conflicts)}"
        )


def _write_durable_exclusive(path: Path, data: bytes, duplicate_message: str) -> str:
    parent_descriptor, name = _safe_parent_descriptor(path, create=False)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        try:
            descriptor = os.open(name, flags, 0o400, dir_fd=parent_descriptor)
        except FileExistsError as exc:
            raise RuntimeError(duplicate_message) from exc
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
                os.fchmod(handle.fileno(), 0o400)
        except Exception:
            # An interrupted immutable reservation remains fail-closed.
            raise
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    return sha256_bytes(data)


def reserve_seed(
    *,
    stamp: str,
    seed: str,
    run_dir: Path,
    child_dir: Path,
    anchor_dir: Path,
    registered_at: str,
) -> tuple[Path, str]:
    validated_stamp = validate_stamp(stamp)
    validated_seed = validate_seed(seed)
    assert_seed_unused(validated_seed)
    reservation_dir = ANCHOR_ROOT / SEED_RESERVATION_DIRNAME
    ensure_safe_directory(reservation_dir)
    reservation_path = seed_reservation_path(validated_seed)
    reservation = {
        "schema": SEED_RESERVATION_SCHEMA,
        "stamp": validated_stamp,
        "run_id": run_dir.name,
        "run_dir": str(run_dir.resolve(strict=False)),
        "child_dir": str(child_dir.resolve(strict=False)),
        "anchor_dir": str(anchor_dir.resolve(strict=False)),
        "seed": validated_seed,
        "candidate_order_seed": validated_seed,
        "registered_at": registered_at,
    }
    data = json_bytes(reservation)
    digest = _write_durable_exclusive(
        reservation_path,
        data,
        f"seed is already reserved or registered: {validated_seed}",
    )
    return reservation_path, digest


def reserve_run_registration(
    *,
    stamp: str,
    seed: str,
    run_dir: Path,
    child_dir: Path,
    anchor_dir: Path,
    registered_at: str,
    seed_reservation_path_value: Path,
    seed_reservation_sha256: str,
) -> tuple[Path, str]:
    validated_stamp = validate_stamp(stamp)
    validated_seed = validate_seed(seed)
    registration_dir = ANCHOR_ROOT / RUN_REGISTRATION_DIRNAME
    ensure_safe_directory(registration_dir)
    path = run_registration_path(validated_stamp)
    registration = {
        "schema": RUN_REGISTRATION_SCHEMA,
        "stamp": validated_stamp,
        "run_id": run_dir.name,
        "run_dir": str(run_dir.resolve(strict=False)),
        "child_dir": str(child_dir.resolve(strict=False)),
        "anchor_dir": str(anchor_dir.resolve(strict=False)),
        "seed": validated_seed,
        "candidate_order_seed": validated_seed,
        "seed_reservation_path": str(seed_reservation_path_value.resolve()),
        "seed_reservation_sha256": seed_reservation_sha256,
        "registered_at": registered_at,
    }
    data = json_bytes(registration)
    digest = _write_durable_exclusive(
        path,
        data,
        f"run ID is already reserved or registered: {run_dir.name}",
    )
    return path, digest


def reserve_registration(
    *,
    stamp: str,
    seed: str,
    run_dir: Path,
    child_dir: Path,
    anchor_dir: Path,
    registered_at: str,
) -> tuple[Path, str, Path, str]:
    """Atomically-enough reserve both the seed identity and canonical run ID."""
    with registration_mutex():
        if run_dir.exists() or run_dir.is_symlink():
            raise RuntimeError(f"run path already exists: {run_dir}")
        if anchor_dir.exists() or anchor_dir.is_symlink():
            raise RuntimeError(f"trust path already exists: {anchor_dir}")
        run_pin = run_registration_path(stamp)
        if run_pin.exists() or run_pin.is_symlink():
            raise RuntimeError(f"run ID is already reserved or registered: {run_dir.name}")
        reservation_path, reservation_digest = reserve_seed(
            stamp=stamp,
            seed=seed,
            run_dir=run_dir,
            child_dir=child_dir,
            anchor_dir=anchor_dir,
            registered_at=registered_at,
        )
        registration_path, registration_digest = reserve_run_registration(
            stamp=stamp,
            seed=seed,
            run_dir=run_dir,
            child_dir=child_dir,
            anchor_dir=anchor_dir,
            registered_at=registered_at,
            seed_reservation_path_value=reservation_path,
            seed_reservation_sha256=reservation_digest,
        )
    return (
        reservation_path,
        reservation_digest,
        registration_path,
        registration_digest,
    )


def _canonical_run_context(run_dir: Path) -> dict[str, Path | str]:
    working_root = _require_safe_directory(WORKING_FOLDER, "working-folder root")
    anchor_root = _require_safe_directory(ANCHOR_ROOT, "audit-anchor root")
    supplied = Path(run_dir)
    supplied_lexical = _absolute_lexical(supplied)
    configured_working_lexical = _absolute_lexical(WORKING_FOLDER)
    if supplied.is_symlink():
        raise RuntimeError(f"run path is a symlink: {supplied}")
    try:
        resolved = supplied.resolve(strict=True)
        relative = resolved.relative_to(working_root)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"run path is outside the canonical working-folder root: {supplied}") from exc
    parts = relative.parts
    if len(parts) == 1:
        root_name = parts[0]
        scope_dir = resolved
        expected_lexical = configured_working_lexical / root_name
    elif len(parts) == 2 and parts[1] == CHILD_RELATIVE_PATH:
        root_name = parts[0]
        scope_dir = resolved
        expected_lexical = configured_working_lexical / root_name / CHILD_RELATIVE_PATH
    else:
        raise RuntimeError(f"run path is not a canonical root or registered child: {supplied}")
    if supplied_lexical != expected_lexical:
        raise RuntimeError(f"run path uses a noncanonical or symlinked prefix: {supplied}")
    match = re.fullmatch(r"zero_to_one_candidates_(\d{8}_\d{6})", root_name)
    if match is None:
        raise RuntimeError(f"run path has a noncanonical run ID: {supplied}")
    root_dir = working_root / root_name
    child_dir = root_dir / CHILD_RELATIVE_PATH
    current = working_root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise RuntimeError(f"run path contains a symlink: {current}")
    anchor_dir = anchor_root / f"v2_matched_{match.group(1)}"
    if anchor_dir.is_symlink() or not anchor_dir.is_dir():
        raise RuntimeError(f"canonical trust path is missing or unsafe: {anchor_dir}")
    return {
        "stamp": match.group(1),
        "root_dir": root_dir,
        "child_dir": child_dir,
        "scope_dir": scope_dir,
        "anchor_dir": anchor_dir,
    }


def _parse_registered_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise RuntimeError(f"{label} is missing")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise RuntimeError(f"{label} is malformed") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RuntimeError(f"{label} must include a UTC offset")
    return parsed


def authenticated_run_seed(run_dir: Path) -> str:
    context = _canonical_run_context(run_dir)
    root_dir = context["root_dir"]
    child_dir = context["child_dir"]
    scope_dir = context["scope_dir"]
    anchor_dir = context["anchor_dir"]
    if not all(isinstance(path, Path) for path in (root_dir, child_dir, scope_dir, anchor_dir)):
        raise RuntimeError("internal canonical path binding failed")
    receipt_path = anchor_dir / "registration_receipt.json"
    receipt = _read_json_object(receipt_path, "registration receipt")
    expected_receipt_fields = {
        "schema",
        "run_id",
        "run_dir",
        "child_dir",
        "anchor_dir",
        "root_scope_id",
        "child_scope_id",
        "seed",
        "candidate_order_seed",
        "model",
        "reasoning_effort",
        "development_contract_sha256",
        "root_protection_anchor_path",
        "root_protection_anchor_sha256",
        "child_protection_anchor_path",
        "child_protection_anchor_sha256",
        "seed_reservation_path",
        "seed_reservation_sha256",
        "run_registration_path",
        "run_registration_sha256",
        "registered_at",
    }
    if receipt.get("schema") != REGISTRATION_RECEIPT_SCHEMA or set(receipt) != expected_receipt_fields:
        raise RuntimeError("registration receipt is absent, legacy, or has a noncanonical schema")
    expected_paths = {
        "run_dir": str(root_dir),
        "child_dir": str(child_dir),
        "anchor_dir": str(anchor_dir),
        "root_protection_anchor_path": str(anchor_dir / "baseline_protection_anchor.json"),
        "child_protection_anchor_path": str(anchor_dir / "shadow_protection_anchor.json"),
    }
    for field, expected in expected_paths.items():
        if receipt.get(field) != expected:
            raise RuntimeError(f"registration receipt {field} does not match its canonical path")
    if (
        receipt.get("run_id") != root_dir.name
        or receipt.get("root_scope_id") != ROOT_SCOPE_ID
        or receipt.get("child_scope_id") != CHILD_SCOPE_ID
        or receipt.get("model") != MODEL
        or receipt.get("reasoning_effort") != REASONING
    ):
        raise RuntimeError("registration receipt identity does not match the registered workflow")
    seed = validate_seed(receipt.get("seed"))
    if receipt.get("candidate_order_seed") != seed:
        raise RuntimeError("registration receipt seed and candidate_order_seed disagree")

    registration_path = run_registration_path(str(context["stamp"]))
    if receipt.get("run_registration_path") != str(registration_path.resolve()):
        raise RuntimeError("registration receipt points to the wrong run registration")
    registration = _read_json_object(registration_path, "run registration")
    expected_registration_fields = {
        "schema",
        "stamp",
        "run_id",
        "run_dir",
        "child_dir",
        "anchor_dir",
        "seed",
        "candidate_order_seed",
        "seed_reservation_path",
        "seed_reservation_sha256",
        "registered_at",
    }
    if (
        registration.get("schema") != RUN_REGISTRATION_SCHEMA
        or set(registration) != expected_registration_fields
    ):
        raise RuntimeError("run registration has a noncanonical schema")
    if receipt.get("run_registration_sha256") != sha256(registration_path):
        raise RuntimeError("run registration bytes do not match the registration receipt")
    for field in (
        "stamp",
        "run_id",
        "run_dir",
        "child_dir",
        "anchor_dir",
        "seed",
        "candidate_order_seed",
        "seed_reservation_path",
        "seed_reservation_sha256",
        "registered_at",
    ):
        expected = context["stamp"] if field == "stamp" else receipt.get(field)
        if registration.get(field) != expected:
            raise RuntimeError(f"run registration and registration receipt disagree on {field}")

    reservation_path = seed_reservation_path(seed)
    if receipt.get("seed_reservation_path") != str(reservation_path.resolve()):
        raise RuntimeError("registration receipt points to the wrong seed reservation")
    reservation = _read_json_object(reservation_path, "seed reservation")
    expected_reservation_fields = {
        "schema",
        "stamp",
        "run_id",
        "run_dir",
        "child_dir",
        "anchor_dir",
        "seed",
        "candidate_order_seed",
        "registered_at",
    }
    if reservation.get("schema") != SEED_RESERVATION_SCHEMA or set(reservation) != expected_reservation_fields:
        raise RuntimeError("seed reservation has a noncanonical schema")
    reservation_digest = sha256(reservation_path)
    if receipt.get("seed_reservation_sha256") != reservation_digest:
        raise RuntimeError("seed reservation bytes do not match the registration receipt")
    for field in (
        "stamp",
        "run_id",
        "run_dir",
        "child_dir",
        "anchor_dir",
        "seed",
        "candidate_order_seed",
        "registered_at",
    ):
        expected = context["stamp"] if field == "stamp" else receipt.get(field)
        if reservation.get(field) != expected:
            raise RuntimeError(f"seed reservation and registration receipt disagree on {field}")

    matching_run_reservations = []
    for candidate in _canonical_seed_reservations():
        candidate_record = _read_json_object(candidate, "seed reservation")
        if (
            candidate_record.get("run_id") == root_dir.name
            or candidate_record.get("run_dir") == str(root_dir)
            or candidate_record.get("anchor_dir") == str(anchor_dir)
        ):
            matching_run_reservations.append(candidate.resolve())
    if matching_run_reservations != [reservation_path.resolve()]:
        raise RuntimeError("registered run must have exactly one canonical seed reservation")
    matching_run_registrations = []
    for candidate in _canonical_run_registrations():
        candidate_record = _read_json_object(candidate, "run registration")
        if (
            candidate_record.get("run_id") == root_dir.name
            or candidate_record.get("run_dir") == str(root_dir)
            or candidate_record.get("anchor_dir") == str(anchor_dir)
        ):
            matching_run_registrations.append(candidate.resolve())
    if matching_run_registrations != [registration_path.resolve()]:
        raise RuntimeError("registered run must have exactly one canonical run registration")

    for required_directory in ("context", "agent_returns", "allocation_precommits"):
        _require_safe_directory(root_dir / required_directory, required_directory)
        scope_candidate = scope_dir / required_directory
        if scope_dir != root_dir and (
            scope_candidate.exists() or scope_candidate.is_symlink()
        ):
            _require_safe_directory(scope_candidate, required_directory)
    for optional_directory in (
        "baseline_fact_closure",
        "baseline_level2",
        "failure_evidence",
        "live_metering",
        "runtime_traces",
        "shadow_fact_closure",
        "shadow_level2",
        "stage_admission_baselines",
        "trace_attestations",
    ):
        candidate = scope_dir / optional_directory
        if candidate.exists() or candidate.is_symlink():
            _require_safe_directory(candidate, optional_directory)

    root_manifest_path = root_dir / "00a_context_and_resource_manifest.jsonl"
    root_run = _read_v2_run_record(root_manifest_path)
    if root_run is None or root_run.get("run_id") != root_dir.name:
        raise RuntimeError("registered root run record is absent or has the wrong run ID")
    for field in ("seed", "candidate_order_seed"):
        if root_run.get(field) != seed:
            raise RuntimeError(f"registration receipt and root run {field} disagree")
    registered_at = _parse_registered_time(receipt.get("registered_at"), "registered_at")
    started_at = _parse_registered_time(root_run.get("started_at"), "root started_at")
    if started_at != registered_at + timedelta(seconds=5):
        raise RuntimeError("registration time is not bound to the root run start")
    declarations = root_run.get("declared_child_scopes")
    if not isinstance(declarations, list) or len(declarations) != 1:
        raise RuntimeError("registered root run lacks its exact child declaration")
    declaration = declarations[0]
    if (
        not isinstance(declaration, dict)
        or declaration.get("scope_id") != CHILD_SCOPE_ID
        or declaration.get("relative_path") != CHILD_RELATIVE_PATH
        or _parse_registered_time(
            declaration.get("registered_at"), "child declaration registered_at"
        )
        != started_at + timedelta(microseconds=1)
    ):
        raise RuntimeError("registered child identity or declaration time is inconsistent")

    if root_run.get("development_contract_path") != "00b_development_contract.json":
        raise RuntimeError("registered development contract path is noncanonical")
    contract_path = root_dir / "00b_development_contract.json"
    _require_safe_file(contract_path, "development contract")
    contract_digest = sha256(contract_path)
    if (
        root_run.get("development_contract_sha256") != contract_digest
        or receipt.get("development_contract_sha256") != contract_digest
    ):
        raise RuntimeError("development contract does not match registration")
    human_manifest_path = root_dir / "00_run_manifest.md"
    _require_safe_file(human_manifest_path, "human run manifest")
    seed_binding_line = f"- Registered seed and candidate-order seed: `{seed}`"
    if human_manifest_path.read_text(encoding="utf-8").count(seed_binding_line) != 1:
        raise RuntimeError("human run manifest seed binding is absent or inconsistent")
    for path_field, digest_field in (
        ("root_protection_anchor_path", "root_protection_anchor_sha256"),
        ("child_protection_anchor_path", "child_protection_anchor_sha256"),
    ):
        protected_path = Path(str(receipt[path_field]))
        _require_safe_file(protected_path, path_field)
        if receipt.get(digest_field) != sha256(protected_path):
            raise RuntimeError(f"{path_field} does not match the registration receipt")

    allowed_paths = {
        receipt_path,
        reservation_path,
        registration_path,
        root_manifest_path,
    }
    child_manifest_path = child_dir / "00a_context_and_resource_manifest.jsonl"
    child_manifest_exists = child_manifest_path.is_file() and not child_manifest_path.is_symlink()
    if child_manifest_path.is_symlink():
        raise RuntimeError("registered child manifest is unsafe")
    if child_manifest_exists:
        child_run = _read_v2_run_record(child_manifest_path)
        if child_run is None or child_run.get("run_id") != child_dir.name:
            raise RuntimeError("registered child run record is absent or has the wrong run ID")
        for field in ("seed", "candidate_order_seed"):
            if child_run.get(field) != seed:
                raise RuntimeError(f"registration receipt and child run {field} disagree")
        allowed_paths.add(child_manifest_path)
    if scope_dir != root_dir and not child_manifest_exists:
        raise RuntimeError("registered child run record is absent")
    assert_seed_unused(seed, allowed_paths=allowed_paths)
    return seed


@contextlib.contextmanager
def authenticated_run_command(run_dir: Path) -> Any:
    """Hold the run-identity pin lock across a complete mutating command."""
    context = _canonical_run_context(run_dir)
    registration_path = run_registration_path(str(context["stamp"]))
    parent_descriptor, name = _safe_parent_descriptor(
        registration_path,
        create=False,
    )
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(name, flags, dir_fd=parent_descriptor)
    finally:
        os.close(parent_descriptor)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield authenticated_run_seed(run_dir)
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def run_authenticated_command(
    run_dir: Path,
    command: Any,
    *args: Any,
) -> None:
    with authenticated_run_command(run_dir):
        command(*args)


def marker_block(path: Path, start: str, end: str) -> bytes:
    data = path.read_bytes()
    start_bytes = start.encode("utf-8")
    end_bytes = end.encode("utf-8")
    if data.count(start_bytes) != 1 or data.count(end_bytes) != 1:
        raise RuntimeError("protected block markers are not unique")
    begin = data.index(start_bytes)
    finish = data.index(end_bytes)
    if finish <= begin:
        raise RuntimeError("protected block markers are reversed")
    return data[begin:finish]


def seeded_order(seed: str, namespace: str, values: list[str]) -> list[str]:
    validated_seed = validate_seed(seed)
    return sorted(
        values,
        key=lambda value: hashlib.sha256(
            f"{validated_seed}|{namespace}|{value}".encode("utf-8")
        ).hexdigest(),
    )


def trace_task_name(run_dir: Path, agent_id: str) -> str:
    """Return the globally unique subagent task identity bound to this run."""
    resolved = run_dir.resolve()
    try:
        run_identity = resolved.relative_to(WORKING_FOLDER.resolve()).as_posix()
    except ValueError:
        # Hermetic tests and external diagnostics still need collision-resistant
        # names even when their directories are outside the production root.
        run_identity = (
            f"{resolved.parent.name}/{resolved.name}/"
            f"{sha256_bytes(str(resolved).encode('utf-8'))[:16]}"
        )
    raw = f"{run_identity}_{agent_id}"
    normalized = re.sub(r"[^a-z0-9_]+", "_", raw.casefold()).strip("_")
    if not normalized:
        raise RuntimeError("cannot derive a run-unique trace task name")
    return normalized


def development_contract() -> dict[str, Any]:
    return {
        "schema": "zt1-development-contract-v2",
        "contract_id": "matched-development-v2",
        "level2_sections": list(DOSSIER_SECTIONS),
        "frozen_sections": list(DOSSIER_SECTIONS),
        "evidence_statuses": [
            "verified",
            "interpreted",
            "counsel-required",
            "unknown",
            "contradicted",
        ],
        "stage_query_caps": {"level2": 12, "fact_closure": 8},
        "aggregate_opportunity": {
            "raw": 48,
            "level2": 12,
            "fact_closure": 6,
            "frozen": 6,
            "discovery_queries": 108,
            "level2_queries": 144,
            "fact_closure_queries": 48,
            "total_queries": 300,
        },
        "candidate_budgets": {
            "level2": dict(LEVEL2_CAPS),
            "fact_closure": dict(FACT_CLOSURE_CAPS),
        },
        "candidate_live_stop_thresholds": {
            stage: dict(thresholds)
            for stage, thresholds in DEVELOPMENT_LIVE_STOP_THRESHOLDS.items()
        },
        "metering_monitor": dict(DEVELOPMENT_METERING_MONITOR),
        "dossier_prose_word_ranges": {
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
        "dossier_measurement": {
            "counted_sections": list(DOSSIER_SECTIONS[:-1]),
            "excluded_material": [
                "title",
                "section_headings",
                "evidence_and_sources",
                "source_ledgers",
                "telemetry",
                "machine_metadata",
            ],
        },
        "fact_closure_schema": {
            "requires_decision_critical_evidence": True,
            "requires_pre_freeze_source_chain": True,
            "replacement_after_closure": False,
        },
        "query_source_opportunity": {
            "query_requires_tool_event": True,
            "query_requires_source_open": True,
            "source_requires_bidirectional_evidence": True,
        },
    }


def protection_inventory(captured_at: datetime) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    files = []
    for path in FIXED_PATHS.values():
        digest = sha256(path)
        files.append(
            {
                "path": str(path),
                "pre_run_sha256": digest,
                "sha256": digest,
                "captured_at": iso(captured_at),
            }
        )
    prompt = FIXED_PATHS["orchestration-prompt"]
    block_digest = sha256_bytes(marker_block(prompt, "## Validation Gates", "## Workflow"))
    blocks = [
        {
            "path": str(prompt),
            "start_marker": "## Validation Gates",
            "end_marker": "## Workflow",
            "pre_run_sha256": block_digest,
            "sha256": block_digest,
            "captured_at": iso(captured_at),
        }
    ]
    return files, blocks


def anchor_payload(
    *, run_dir: Path, scope_id: str, created_at: datetime, contract_digest: str
) -> dict[str, Any]:
    prompt = FIXED_PATHS["orchestration-prompt"]
    block_digest = sha256_bytes(marker_block(prompt, "## Validation Gates", "## Workflow"))
    return {
        "schema": "zt1-protection-anchor-v2",
        "contract_profile": "zt1-fixed-v1",
        "workflow_profile": "zt1-auditor-workflow-v2",
        "workflow_files": [
            {"id": key, "path": str(path), "sha256": sha256(path)}
            for key, path in sorted(WORKFLOW_PATHS.items())
        ],
        "run_id": run_dir.name,
        "scope_id": scope_id,
        "run_dir": str(run_dir.resolve()),
        "development_contract_path": "00b_development_contract.json",
        "development_contract_sha256": contract_digest,
        "created_at": iso(created_at),
        "block_semantics": "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1",
        "files": [
            {"id": key, "path": str(path), "sha256": sha256(path)}
            for key, path in sorted(FIXED_PATHS.items())
        ],
        "blocks": [
            {
                "id": "validation-gates",
                "path": str(prompt),
                "start_marker": "## Validation Gates",
                "end_marker": "## Workflow",
                "sha256": block_digest,
            }
        ],
    }


def human_manifest(
    *,
    seed: str,
    run_dir: Path,
    child_dir: Path,
    anchor_dir: Path,
    root_anchor_digest: str | None,
    child_anchor_digest: str,
    contract_digest: str,
    started_at: datetime,
    deadline: datetime,
    declaration_at: datetime,
) -> str:
    seed = validate_seed(seed)
    ordered_roles = seeded_order(seed, "baseline-discovery-role", BASELINE_ROLES)
    caps = [22, 22, 22, 21, 21]
    outputs = [10, 10, 10, 9, 9]
    role_rows = "\n".join(
        f"- `{role}` / `{BASELINE_AGENT_IDS[role]}`: query cap {cap}; raw IDs {count}"
        for role, cap, count in zip(ordered_roles, caps, outputs)
    )
    ballot_order = seeded_order(
        seed,
        "shadow-ballot-order",
        ["commercial_ranker", "economics_ranker", "tail_recall_challenger"],
    )
    baseline_packets = "\n".join(f"- `{path}`" for path in BASELINE_PACKET_PATHS)
    shadow_packets = "\n".join(f"- `{path}`" for path in SHADOW_PACKET_PATHS)
    root_pin = root_anchor_digest or "PENDING_EXTERNAL_CREATION"
    return f"""# V2 Matched Non-Routing Generation Experiment

## Registration

- Run profile: `v2_matched_nonrouting`
- Root scope: `{ROOT_SCOPE_ID}` / `matched_baseline` / `audited_funnel` / `frozen_nonrouting`
- Child scope: `{CHILD_SCOPE_ID}` / `shadow` / `archipelago_lite_shadow` / `frozen_nonrouting`
- Cohort kind: `initial` for both; wave index `1`; no regeneration scope
- Root path: `{run_dir}`
- Child path: `{child_dir}`
- External trust path: `{anchor_dir}`
- Registered seed and candidate-order seed: `{seed}`
- Model: `{MODEL}`
- Reasoning setting: `{REASONING}`
- Root start: `{iso(started_at)}`
- Root deadline: `{iso(deadline)}`
- Child declaration time: `{iso(declaration_at)}`
- Development contract SHA-256: `{contract_digest}`
- Root protection-anchor SHA-256: `{root_pin}`
- Child protection-anchor SHA-256: `{child_anchor_digest}`
- Results remain withheld until both native audits, trust-bundle audit, parity audit, and composite audit pass.

## Equal Opportunity Contract

- Each arm: 48 raw concepts, 12 Level-2 dossiers, six sealed fact-closure candidates, six frozen finalists.
- Each arm: at most 300 unique queries, 10,000,000 uncached input tokens, 700,000 output tokens, 180 wall minutes, and three concurrent agents.
- Each Level-2 entity: one isolated agent, 12-query opportunity, 112,000 uncached-input-token hard admission cap, 20,000-output-token hard admission cap, 15-minute hard cap, and 900–1,500 counted dossier-prose words across the eight substantive sections in `00b_development_contract.json`, with at least 75 words in each section.
- Each fact-closure entity: one isolated agent, eight-query opportunity, 96,000 uncached-input-token hard admission cap, 20,000-output-token hard admission cap, 12-minute hard cap, no replacement after sealing, and 1,100–1,800 counted frozen-dossier words across those same eight substantive sections, with at least 100 words in each section.
- Discovery opportunity: 108 queries per arm. Baseline uses seeded role caps `22/22/22/21/21`; treatment uses 18 queries for each of six scouts.
- Development runs in batches of at most three. Every development agent owns exactly one candidate, allocation, return, and immutable run-local trace; no resource, source, call, or elapsed-time total is divided after execution.
- Before each batch dispatch, the root starts the pinned blocking controller. It discovers only recent run-scoped traces, retains their direct paths, samples them every second, and exits with the exact collaboration task identities to interrupt at the contract's lower live-stop threshold (Level-2: 92,000/11,000/14 minutes; closure: 76,000/11,000/11 minutes). The root waits on that process result and immediately invokes the collaboration interrupt operation; it does not model-poll the shell every second. The reserve to the hard cap is calibrated above the largest observed provider token-event jump; interrupted agents fail admission and cannot advance the checkpoint.
- Unused query and prose opportunity stays in its original allocation and is logged. No filler queries or prose padding.

### Seeded baseline role permutation

{role_rows}

### Stage timing

- The 180-minute aggregate arm cap and three-agent concurrency cap remain hard. Candidate caps are admission ceilings, not reservations: four Level-2 batches and two closure batches must be scheduled within the remaining run window, and launch must stop if the actual deadline cannot accommodate another batch.

## Deterministic Rules

- Seed order is ascending SHA-256 of UTF-8 bytes `seed|namespace|stable_id`.
- Baseline root rule: remove only indispensable unlawful/seriously harmful shapes or directly falsified indispensable premises; retain reversible economic siblings; then choose 12 Level-2 directions and six closure directions by evidence-supported payer event, founder-accessible first contract, compounding control, and fingerprint diversity, with seed order as the sole tie-break. No numeric scoring.
- Treatment provisional selector returns a complete ordered 48-ID list. Ballot order is `{', '.join(ballot_order)}`.
- Treatment fills Level-2 slots as 6 provisional, 3 unique round-robin ballot additions, 1 seeded rejected sentinel, 1 highest unused near-cutoff item, and 1 seeded singleton/underrepresented-island item, using the protocol fallbacks and seed order only.
- Treatment finalist selector returns the exact ordered six closure IDs from twelve masked dossiers; the root copies that order unchanged.
- Runtime tokens come from each candidate agent's own provider `token_count` trace, both during live monitoring and at final admission. Uncached input is exact `input_tokens - cached_input_tokens`; output is exact provider `output_tokens`; elapsed time is an exact integer count of timestamp-derived microseconds. Agent intervals, task identity, web call IDs, returned source URLs, and resources are independently reconciled by the pinned auditor against that same immutable candidate-owned trace.

## Isolation And Allowlists

Every agent uses `fork_turns: none`, reads exactly one immutable scope-owned packet, and writes one bounded return. Packet bytes are hashed before dispatch. Baseline packets:

{baseline_packets}

Child packets (reserved now; materialized only after `shadow-dispatch: PASS`):

{shadow_packets}

Creative and selector packets contain only the applicable closed context classes, neutral founder constraints, safety/legal boundaries, assigned IDs/evidence, caps, and output schema. They exclude downstream frameworks, thresholds, verdicts, detailed prior rhetoric, other agents' conclusions, and unrestricted repository context.

## Non-Routing Boundary

Both arms are irreversibly non-routing, `shadow_only: true`, and `validation_eligible: false`. This run authorizes generation, neutral research, masking, selection, dossier development, closure, freezing, and auditing only. It authorizes no downstream decision workflow, regeneration, outreach, private proof, real chatbot, or confirmation artifact.
"""


def register(stamp: str, seed: str) -> None:
    stamp = validate_stamp(stamp)
    seed = validate_seed(seed)
    _require_safe_directory(WORKING_FOLDER, "working-folder root")
    _require_safe_directory(ANCHOR_ROOT, "audit-anchor root")
    run_dir = WORKING_FOLDER / f"zero_to_one_candidates_{stamp}"
    child_dir = run_dir / CHILD_RELATIVE_PATH
    anchor_dir = ANCHOR_ROOT / f"v2_matched_{stamp}"
    if run_dir.exists() or run_dir.is_symlink():
        raise RuntimeError(f"run path already exists: {run_dir}")
    if child_dir.exists() or child_dir.is_symlink():
        raise RuntimeError(f"reserved child path already exists: {child_dir}")
    if anchor_dir.exists() or anchor_dir.is_symlink():
        raise RuntimeError(f"trust path already exists: {anchor_dir}")
    anchor_time = now()
    registered_at = iso(anchor_time)
    (
        reservation_path,
        reservation_digest,
        registration_path,
        registration_digest,
    ) = reserve_registration(
        stamp=stamp,
        seed=seed,
        run_dir=run_dir,
        child_dir=child_dir,
        anchor_dir=anchor_dir,
        registered_at=registered_at,
    )
    print(f"RESERVED_SEED={seed}", flush=True)
    ensure_safe_directory(run_dir, exist_ok=False)
    ensure_safe_directory(anchor_dir, exist_ok=False)
    ensure_safe_directory(run_dir / "context", exist_ok=False)
    ensure_safe_directory(run_dir / "agent_returns", exist_ok=False)
    ensure_safe_directory(run_dir / "allocation_precommits", exist_ok=False)

    contract_data = json_bytes(development_contract())
    contract_path = run_dir / "00b_development_contract.json"
    write_exclusive(contract_path, contract_data)
    contract_digest = sha256_bytes(contract_data)

    child_anchor = anchor_payload(
        run_dir=child_dir,
        scope_id=CHILD_SCOPE_ID,
        created_at=anchor_time,
        contract_digest=contract_digest,
    )
    child_anchor_path = anchor_dir / "shadow_protection_anchor.json"
    write_exclusive(child_anchor_path, json_bytes(child_anchor))
    child_anchor_digest = sha256(child_anchor_path)
    write_exclusive(
        anchor_dir / "shadow_protection_anchor.sha256",
        f"{child_anchor_digest}  {child_anchor_path.name}\n".encode("utf-8"),
    )

    started_at = anchor_time + timedelta(seconds=5)
    declaration_at = started_at + timedelta(microseconds=1)
    deadline = started_at + timedelta(minutes=180)
    protected_files, protected_blocks = protection_inventory(anchor_time)
    child_declaration = {
        "scope_id": CHILD_SCOPE_ID,
        "relative_path": CHILD_RELATIVE_PATH,
        "relationship": "shadow_child",
        "run_profile": "v2_matched_nonrouting",
        "mode": "archipelago_lite_shadow",
        "arm": "shadow",
        "routing_state": "frozen_nonrouting",
        "cohort_kind": "initial",
        "manifest_sha256": None,
        "development_contract_sha256": contract_digest,
        "protection_anchor_sha256": child_anchor_digest,
        "freeze_seal_sha256": None,
        "audit_report_path": None,
        "audit_report_sha256": None,
        "audit_status": None,
        "model": MODEL,
        "reasoning_effort": REASONING,
        "registered_at": iso(declaration_at),
        "results_visibility": "withheld",
    }
    run_record = {
        "record_type": "run",
        "schema": "zt1-generation-run-v2",
        "run_id": run_dir.name,
        "scope_id": ROOT_SCOPE_ID,
        "run_profile": "v2_matched_nonrouting",
        "arm": "matched_baseline",
        "mode": "audited_funnel",
        "routing_state": "frozen_nonrouting",
        "cohort_kind": "initial",
        "wave_index": 1,
        "selection_policy": "root_orchestrator",
        "lifecycle_state": "registered",
        "status": "registered",
        "started_at": iso(started_at),
        "deadline_at": iso(deadline),
        "ended_at": None,
        "model": MODEL,
        "reasoning_effort": REASONING,
        "results_visibility": "withheld",
        "seed": seed,
        "candidate_order_seed": seed,
        "development_contract_path": contract_path.name,
        "development_contract_sha256": contract_digest,
        "parent_scope_id": None,
        "declared_child_scopes": [child_declaration],
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "protected_files": protected_files,
        "protected_blocks": protected_blocks,
        "budgets": {
            "unique_queries": 300,
            "uncached_input_tokens": 10000000,
            "output_tokens": 700000,
            "elapsed_minutes": 180,
            "max_concurrency": 3,
        },
        "resource_totals": {
            "unique_queries": 0,
            "uncached_input_tokens": 0,
            "output_tokens": 0,
            "elapsed_microseconds": 0,
        },
        "matched_pilot": True,
        "shadow_only": True,
        "validation_eligible": False,
        "shadow_can_route_to_validation": False,
    }
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    write_exclusive(manifest_path, jsonl_bytes([run_record]))
    human_path = run_dir / "00_run_manifest.md"
    write_exclusive(
        human_path,
        human_manifest(
            seed=seed,
            run_dir=run_dir,
            child_dir=child_dir,
            anchor_dir=anchor_dir,
            root_anchor_digest=None,
            child_anchor_digest=child_anchor_digest,
            contract_digest=contract_digest,
            started_at=started_at,
            deadline=deadline,
            declaration_at=declaration_at,
        ).encode("utf-8"),
    )

    root_anchor_path = anchor_dir / "baseline_protection_anchor.json"
    result = subprocess.run(
        [
            sys.executable,
            str(AUDITOR),
            str(run_dir),
            "--create-protection-anchor",
            str(root_anchor_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"PROTECTION_ANCHOR_SHA256=([0-9a-f]{64})", result.stdout)
    if match is None:
        raise RuntimeError(f"auditor did not return a root anchor pin: {result.stdout!r}")
    root_anchor_digest = match.group(1)
    if sha256(root_anchor_path) != root_anchor_digest:
        raise RuntimeError("root anchor printout and bytes disagree")
    write_exclusive(
        anchor_dir / "baseline_protection_anchor.sha256",
        f"{root_anchor_digest}  {root_anchor_path.name}\n".encode("utf-8"),
    )
    write_replace(
        human_path,
        human_manifest(
            seed=seed,
            run_dir=run_dir,
            child_dir=child_dir,
            anchor_dir=anchor_dir,
            root_anchor_digest=root_anchor_digest,
            child_anchor_digest=child_anchor_digest,
            contract_digest=contract_digest,
            started_at=started_at,
            deadline=deadline,
            declaration_at=declaration_at,
        ).encode("utf-8"),
    )
    receipt = {
        "schema": REGISTRATION_RECEIPT_SCHEMA,
        "run_id": run_dir.name,
        "run_dir": str(run_dir.resolve()),
        "child_dir": str(child_dir.resolve(strict=False)),
        "anchor_dir": str(anchor_dir.resolve()),
        "root_scope_id": ROOT_SCOPE_ID,
        "child_scope_id": CHILD_SCOPE_ID,
        "seed": seed,
        "candidate_order_seed": seed,
        "model": MODEL,
        "reasoning_effort": REASONING,
        "development_contract_sha256": contract_digest,
        "root_protection_anchor_path": str(root_anchor_path.resolve()),
        "root_protection_anchor_sha256": root_anchor_digest,
        "child_protection_anchor_path": str(child_anchor_path.resolve()),
        "child_protection_anchor_sha256": child_anchor_digest,
        "seed_reservation_path": str(reservation_path.resolve()),
        "seed_reservation_sha256": reservation_digest,
        "run_registration_path": str(registration_path.resolve()),
        "run_registration_sha256": registration_digest,
        "registered_at": registered_at,
    }
    receipt_path = anchor_dir / "registration_receipt.json"
    write_exclusive(receipt_path, json_bytes(receipt))
    print(json.dumps(receipt, indent=2, sort_keys=True))


def elapsed_microseconds(start: datetime, end: datetime) -> int:
    """Return exact integral active time without a float round-trip."""
    delta = end.astimezone(timezone.utc) - start.astimezone(timezone.utc)
    return (
        delta.days * 86_400_000_000
        + delta.seconds * 1_000_000
        + delta.microseconds
    )


def record_registered(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    if len(records) != 1 or records[0].get("record_type") != "run":
        raise RuntimeError("registration checkpoint requires a manifest containing only its run record")
    run_record = records[0]
    started_at = datetime.fromisoformat(run_record["started_at"])
    deadline = datetime.fromisoformat(run_record["deadline_at"])
    occurred_at = now()
    if occurred_at <= started_at or occurred_at >= deadline:
        raise RuntimeError("registration checkpoint time is outside the pre-registered run window")

    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    state_path = run_dir / "00d_repository_state.txt"
    state_text = (
        f"captured_at: {iso(occurred_at)}\n"
        f"branch: {branch}\n"
        f"commit: {commit}\n"
        f"dirty: {'true' if status else 'false'}\n"
        "status_porcelain_v1:\n"
        f"{status}"
    )
    write_exclusive(state_path, state_text.encode("utf-8"))
    human_path = run_dir / "00_run_manifest.md"
    human = human_path.read_text(encoding="utf-8")
    human += (
        "\n## Repository State At Registration\n\n"
        f"- Branch: `{branch}`\n"
        f"- Commit: `{commit}`\n"
        f"- Dirty worktree: `{'true' if status else 'false'}`\n"
        f"- Exact snapshot: `{state_path.name}` (`{sha256(state_path)}`)\n"
    )
    write_replace(human_path, human.encode("utf-8"))

    totals = {
        "unique_queries": 0,
        "uncached_input_tokens": 0,
        "output_tokens": 0,
        "elapsed_microseconds": elapsed_microseconds(started_at, occurred_at),
    }
    run_record["resource_totals"] = dict(totals)
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-01-registered",
        "state": "registered",
        "predecessor_id": None,
        "occurred_at": iso(occurred_at),
        "completed_agent_ids": [],
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": "00_run_manifest.md", "sha256": sha256(human_path)},
            {"path": "00b_development_contract.json", "sha256": sha256(run_dir / "00b_development_contract.json")},
            {"path": state_path.name, "sha256": sha256(state_path)},
        ],
    }
    write_replace(manifest_path, jsonl_bytes([run_record, checkpoint]))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def baseline_role_assignments(seed: str) -> list[dict[str, Any]]:
    ordered_roles = seeded_order(seed, "baseline-discovery-role", BASELINE_ROLES)
    caps = [22, 22, 22, 21, 21]
    counts = [10, 10, 10, 9, 9]
    cursor = 1
    assignments: list[dict[str, Any]] = []
    evidence_cursor = 1
    query_cursor = 1
    for role, cap, count in zip(ordered_roles, caps, counts):
        raw_ids = [f"RAW-{index:03d}" for index in range(cursor, cursor + count)]
        midpoint = (len(raw_ids) + 1) // 2
        evidence_ids = [
            f"EV-B-DISC-{evidence_cursor:03d}",
            f"EV-B-DISC-{evidence_cursor + 1:03d}",
        ]
        query_ids = [f"Q-B-{index:04d}" for index in range(query_cursor, query_cursor + 4)]
        assignments.append(
            {
                "role": role,
                "agent_id": BASELINE_AGENT_IDS[role],
                "raw_ids": raw_ids,
                "query_cap": cap,
                "evidence_groups": [
                    {"evidence_id": evidence_ids[0], "entity_ids": raw_ids[:midpoint]},
                    {"evidence_id": evidence_ids[1], "entity_ids": raw_ids[midpoint:]},
                ],
                "query_ids": query_ids,
            }
        )
        cursor += count
        evidence_cursor += 2
        query_cursor += 4
    return assignments


def role_brief(role: str) -> str:
    briefs = {
        "taboo_space_explorer": "Search lawful, commercially real markets avoided because they are boring, regulated, low-status, awkward, or politically sensitive. Awkwardness is a discovery lens, never a reason to retain a concept.",
        "incentive_hacker": "Map mismatches among payer, beneficiary, loss bearer, information holder, risk bearer, authority holder, distributor, and transaction owner; build lawful concepts around a concrete paid event.",
        "incumbent_attacker": "Look for excessive pricing, cross-subsidy, weak service, slow operations, channel conflict, fragmented supply, or route-around gaps that an unknown entrant can reach.",
        "rule_structure_analyst": "Separate binding rules from soft norms, assumptions, reputation, technical limits, and economics; use current transitions and enforcement points without treating regulation alone as buyer demand.",
        "first_principles_extremist": "Work backward from a paid outcome using unconventional but lawful ownership, financing, geography, labour, licensing, data, supply, or distribution structures.",
    }
    return briefs[role]


def prepare_baseline_generation(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    if (run_dir / CHILD_RELATIVE_PATH).exists():
        raise RuntimeError("child directory materialized before baseline freeze")
    assignments = baseline_role_assignments(seed)
    launch_records: list[dict[str, Any]] = []
    for assignment in assignments:
        agent_id = assignment["agent_id"]
        packet_path = run_dir / "context" / f"{agent_id}.md"
        output_path = run_dir / "agent_returns" / f"{agent_id}.json"
        allocation_id = f"ALLOC-B-DISC-{agent_id.rsplit('-', 1)[-1].upper()}"
        created_at = now()
        evidence_lines = "\n".join(
            f"- `{group['evidence_id']}` applies to `{', '.join(group['entity_ids'])}`."
            for group in assignment["evidence_groups"]
        )
        packet = f"""# Immutable Generation Packet

## Identity And Allocation

- Scope: `{ROOT_SCOPE_ID}`
- Arm: `matched_baseline`
- Stage: `generation`
- Agent ID: `{agent_id}`
- Role: `{assignment['role']}`
- Model: `{MODEL}`
- Reasoning: `{REASONING}`
- Seed: `{seed}`
- Allocation ID: `{allocation_id}`
- Query cap: `{assignment['query_cap']}`; use exactly four calls: two search calls and one opened result for each search. Leave the remainder unused.
- Assigned and required output IDs: `{', '.join(assignment['raw_ids'])}`
- Required return path: `{output_path}`

## Founder Constraints

Warsaw data scientist employed full time; at most five focused hours daily; about 100,000 PLN personally available and another 100,000 PLN only for an unusually clear case. Strong AI/data/neuroscience/finance fluency, a medical-student partner, and a family renewable-installation firm near Ostrow Wielkopolski. Avoid camera-led distribution and constant high-energy networking. Prefer part-time proof, controlled downside, repeatable demand, scalable assets, and a plausible path to 5 million PLN of founder net worth without double counting.

## Safety And Legal Boundary

Generate only lawful structures. Reject indispensable deception, coercion, exploitation, privacy abuse, evasion, or serious harm. Classify each key constraint as one of: LAW / BINDING RULE; SOFT INDUSTRY NORM; ASSUMED CONVENTION; REPUTATIONAL EXPECTATION; TECHNICAL LIMITATION; ECONOMIC LIMITATION. Unsupported public facts remain explicit unknowns.

## Role Assignment

{role_brief(assignment['role'])}

Search broadly across sectors. Generate economically distinct concepts, not title variants. Each concept needs a named customer loss, payer and paid trigger, transaction owner, acquisition route, and possible compounding asset. Do not rank or select concepts. Do not read any other file or use any inherited repository material.

## Evidence Assignment

Run two genuinely different, time-sensitive public-evidence searches. For each, open exactly one useful result. Use the first evidence chain for the first entity group and the second chain for the second group:

{evidence_lines}

Prefer direct customer, procurement, operational, incumbent, technical, or official evidence according to the role. Record contradiction and uncertainty honestly. A public source may support a problem or mechanism; it does not prove willingness to pay unless it actually shows budget or payment.

## Required Return Schema

Create exactly one valid UTF-8 JSON object at the required return path. Do not create or read any other file.

{bounded_return_instruction(output_path, run_dir)}

The object must have exactly these top-level keys:

`agent_id`, `role`, `assigned_ids`, `output_ids`, `queries`, `concepts`, `files_read`.

- `agent_id`, `role`, `assigned_ids`, and `output_ids` must exactly match this packet and preserve ID order.
- `files_read` is exactly `["context/{agent_id}.md"]`.
- `queries` contains exactly two objects, in tool-call order, each with: `search_text`, `opened_url`, `source_title`, `source_date` (or null), `evidence_id`, `entity_ids`, `proposition`, `status`, `contradiction`, and `cheapest_resolving_test`.
- `concepts` contains exactly one object per assigned raw ID with: `raw_id`, `title`, `one_sentence_thesis`, `customer`, `loss_event`, `payer`, `beneficiary`, `authority_holder`, `distributor`, `risk_bearer`, `transaction_owner`, `first_paid_event`, `acquisition_route`, `compounding_asset`, `mechanism_class`, `evidence_id`, `hypotheses` (array), `constraint_class`, and `prohibited_reliance` (null or a precise statement).
- Every concept's `evidence_id` is the assigned evidence ID for its entity group.
- Keep every concept concise but concrete. Do not include numeric merit ratings, downstream framework language, or another concept author's conclusions.
"""
        write_exclusive(packet_path, packet.encode("utf-8"))
        assert_bounded_return_packet(packet_path, output_path, run_dir)
        precommit = {
            "schema": "zt1-allocation-precommit-v1",
            "scope_id": ROOT_SCOPE_ID,
            "arm": "matched_baseline",
            "stage": "generation",
            "agent_id": agent_id,
            "role": assignment["role"],
            "seed": seed,
            "allocation_id": allocation_id,
            "entity_ids": assignment["raw_ids"],
            "assigned_ids": assignment["raw_ids"],
            "output_ids": assignment["raw_ids"],
            "query_cap": assignment["query_cap"],
            "planned_used_queries": 4,
            "query_ids": assignment["query_ids"],
            "evidence_groups": assignment["evidence_groups"],
            "created_at": iso(created_at),
            "metering_basis": "trace_derived_exact",
            "packet_path": str(packet_path.relative_to(run_dir)),
            "packet_sha256": sha256(packet_path),
            "output_path": str(output_path.relative_to(run_dir)),
            "model": MODEL,
            "reasoning_effort": REASONING,
            "trace_task_name": trace_task_name(run_dir, agent_id),
        }
        precommit_path = run_dir / "allocation_precommits" / f"{allocation_id}.json"
        write_exclusive(precommit_path, json_bytes(precommit))
        assert_bounded_return_precommit(
            packet_path,
            output_path,
            run_dir,
            precommit_path,
            expected_agent_id=agent_id,
            expected_stage="generation",
        )
        launch_records.append(
            {
                "agent_id": agent_id,
                "role": assignment["role"],
                "packet_path": str(packet_path),
                "packet_sha256": sha256(packet_path),
                "output_path": str(output_path),
                "allocation_precommit_path": str(precommit_path),
                "query_cap": assignment["query_cap"],
                "assigned_ids": assignment["raw_ids"],
                "task_name": trace_task_name(run_dir, agent_id),
            }
        )
    launch_path = run_dir / "baseline_generation_launch.json"
    write_exclusive(
        launch_path,
        json_bytes(
            {
                "schema": "zt1-baseline-generation-launch-v1",
                "seed": seed,
                "model": MODEL,
                "reasoning_effort": REASONING,
                "max_concurrency": 3,
                "agents": launch_records,
            }
        ),
    )
    print(str(launch_path))


def find_trace_paths(
    task_names: list[str], *, created_after: datetime | None = None
) -> dict[str, Path | None]:
    """Resolve globally unique subagent traces in one bounded session scan."""
    requested = set(task_names)
    if len(requested) != len(task_names) or any(
        not isinstance(value, str) or not value for value in task_names
    ):
        raise RuntimeError("trace lookup requires unique nonempty task names")
    session_root = Path("/Users/igor/.codex/sessions")
    matches: dict[str, list[Path]] = {task_name: [] for task_name in task_names}
    if created_after is None:
        candidates = session_root.glob("**/*.jsonl")
    else:
        if created_after.tzinfo is None:
            raise RuntimeError("recent trace discovery requires an offset-aware creation time")
        dates = {
            (created_after.astimezone(timezone.utc) + timedelta(days=offset)).date()
            for offset in (-1, 0, 1)
        } | {
            (created_after.astimezone(LOCAL_TZ) + timedelta(days=offset)).date()
            for offset in (-1, 0, 1)
        }
        candidates = (
            path
            for date in sorted(dates)
            for path in (
                session_root
                / f"{date.year:04d}"
                / f"{date.month:02d}"
                / f"{date.day:02d}"
            ).glob("*.jsonl")
        )
    minimum_mtime = (
        created_after.timestamp() - 60 if created_after is not None else None
    )
    for path in candidates:
        try:
            if minimum_mtime is not None and path.stat().st_mtime < minimum_mtime:
                continue
            with path.open("r", encoding="utf-8") as handle:
                first_line = handle.readline()
            first_record = json.loads(first_line)
            source = first_record.get("payload", {}).get("source", {})
            subagent = source.get("subagent", {}) if isinstance(source, dict) else {}
            thread_spawn = (
                subagent.get("thread_spawn", {}) if isinstance(subagent, dict) else {}
            )
            agent_path = thread_spawn.get("agent_path") if isinstance(thread_spawn, dict) else None
            if first_record.get("type") == "session_meta" and isinstance(agent_path, str):
                candidate = agent_path.removeprefix("/root/")
                if candidate in requested and agent_path == f"/root/{candidate}":
                    matches[candidate].append(path)
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
    resolved: dict[str, Path | None] = {}
    for task_name, paths in matches.items():
        if len(paths) > 1:
            raise RuntimeError(f"expected one runtime trace for {task_name}, found {paths}")
        resolved[task_name] = paths[0] if paths else None
    return resolved


def find_trace_path(task_name: str) -> Path | None:
    """Resolve one globally unique subagent trace without interpreting usage."""
    return find_trace_paths([task_name])[task_name]


def _partial_trace_usage_at_path(task_name: str, trace_path: Path | None) -> dict[str, Any]:
    if trace_path is None:
        measured_at = now()
        return {
            "status": "not_started",
            "trace_path": None,
            "measured_at": iso(measured_at),
            "uncached_input_tokens": 0,
            "output_tokens": 0,
            "elapsed_microseconds": 0,
        }
    records = read_live_jsonl_prefix(trace_path)
    starts = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "task_started"
    ]
    ends = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "task_complete"
    ]
    token_records = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "token_count"
    ]
    if not starts:
        if ends or token_records:
            raise RuntimeError(
                f"partial runtime trace for {task_name} records usage or completion before task start"
            )
        measured_at = now()
        return {
            "status": "not_started",
            "trace_path": str(trace_path),
            "measured_at": iso(measured_at),
            "uncached_input_tokens": 0,
            "output_tokens": 0,
            "elapsed_microseconds": 0,
        }
    if len(starts) != 1 or len(ends) > 1:
        raise RuntimeError(f"partial runtime trace for {task_name} has invalid task boundaries")
    start = parse_timestamp(starts[0]["timestamp"]).astimezone(LOCAL_TZ)
    measured_at = (
        parse_timestamp(ends[0]["timestamp"]).astimezone(LOCAL_TZ)
        if ends
        else now()
    )
    uncached = 0
    output = 0
    if token_records:
        usage = token_records[-1].get("payload", {}).get("info", {}).get(
            "total_token_usage", {}
        )
        input_tokens = usage.get("input_tokens")
        cached_input_tokens = usage.get("cached_input_tokens")
        output_tokens = usage.get("output_tokens")
        if any(
            not isinstance(value, int) or isinstance(value, bool) or value < 0
            for value in (input_tokens, cached_input_tokens, output_tokens)
        ):
            raise RuntimeError(f"partial runtime trace for {task_name} has invalid token types")
        uncached = input_tokens - cached_input_tokens
        output = output_tokens
        if uncached < 0:
            raise RuntimeError(f"partial runtime trace for {task_name} has impossible cached usage")
    return {
        "status": "complete" if ends else "running",
        "trace_path": str(trace_path),
        "measured_at": iso(measured_at),
        "uncached_input_tokens": uncached,
        "output_tokens": output,
        "elapsed_microseconds": elapsed_microseconds(start, measured_at),
    }


def partial_trace_usages_from_paths(
    task_paths: dict[str, Path | None],
) -> dict[str, dict[str, Any]]:
    """Read live provider counters from already-resolved candidate traces."""
    if any(not isinstance(task_name, str) or not task_name for task_name in task_paths):
        raise RuntimeError("partial trace usage requires nonempty task identities")
    return {
        task_name: _partial_trace_usage_at_path(task_name, trace_path)
        for task_name, trace_path in task_paths.items()
    }


def partial_trace_usages(task_names: list[str]) -> dict[str, dict[str, Any]]:
    """Read one batch's latest provider meter events after a single trace scan."""
    paths = find_trace_paths(task_names)
    return partial_trace_usages_from_paths(paths)


def partial_trace_usage(task_name: str) -> dict[str, Any]:
    """Read the latest provider meter event for one running candidate agent."""
    return partial_trace_usages([task_name])[task_name]


def _parse_trace_at_path(task_name: str, trace_path: Path) -> dict[str, Any]:
    """Parse one already-resolved immutable runtime trace."""
    records = read_jsonl(trace_path)
    session_records = [record for record in records if record.get("type") == "session_meta"]
    if len(session_records) != 1:
        raise RuntimeError(f"runtime trace for {task_name} lacks one exact session record")
    source = session_records[0].get("payload", {}).get("source", {})
    subagent = source.get("subagent", {}) if isinstance(source, dict) else {}
    thread_spawn = subagent.get("thread_spawn", {}) if isinstance(subagent, dict) else {}
    if thread_spawn.get("agent_path") != f"/root/{task_name}":
        raise RuntimeError(f"runtime trace identity does not match {task_name}")
    starts = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "task_started"
    ]
    ends = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "task_complete"
    ]
    contexts = [record for record in records if record.get("type") == "turn_context"]
    token_records = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "token_count"
    ]
    if len(starts) != 1 or len(ends) != 1 or len(contexts) != 1 or not token_records:
        raise RuntimeError(f"runtime trace for {task_name} lacks exact task/context/token records")
    usage = token_records[-1]["payload"]["info"]["total_token_usage"]
    uncached = int(usage["input_tokens"]) - int(usage["cached_input_tokens"])
    if uncached < 0:
        raise RuntimeError(f"runtime trace for {task_name} reports impossible cached usage")
    context = contexts[0]["payload"]
    if context.get("model") != MODEL or context.get("effort") != REASONING:
        raise RuntimeError(f"runtime model/effort drift for {task_name}")

    custom_calls = [
        record
        for record in records
        if record.get("type") == "response_item"
        and record.get("payload", {}).get("type") == "custom_tool_call"
    ]
    custom_output_records = [
        record
        for record in records
        if record.get("type") == "response_item"
        and record.get("payload", {}).get("type") == "custom_tool_call_output"
    ]
    call_ids = [call.get("payload", {}).get("call_id") for call in custom_calls]
    output_ids = [record.get("payload", {}).get("call_id") for record in custom_output_records]
    if (
        any(not isinstance(call_id, str) or not call_id for call_id in call_ids + output_ids)
        or len(call_ids) != len(set(call_ids))
        or len(output_ids) != len(set(output_ids))
    ):
        raise RuntimeError(f"runtime trace for {task_name} has invalid or duplicate tool call IDs")
    custom_outputs = {
        record["payload"]["call_id"]: record for record in custom_output_records
    }
    file_change_events = [
        record
        for record in records
        if record.get("type") == "event_msg"
        and record.get("payload", {}).get("type") == "item_completed"
        and record.get("payload", {}).get("item", {}).get("type") == "FileChange"
    ]
    web_calls = []
    for record in custom_calls:
        if _outer_tool_call_kind(record) == "web__run":
            _decode_strict_web_call(record)
            web_calls.append(record)
    for call in web_calls:
        if call["payload"].get("call_id") not in custom_outputs:
            raise RuntimeError(f"web call lacks output in runtime trace for {task_name}")
    return {
        "trace_path": trace_path,
        "trace_sha256": sha256(trace_path),
        "started_at": starts[0]["timestamp"],
        "ended_at": ends[0]["timestamp"],
        "model": context["model"],
        "reasoning_effort": context["effort"],
        "uncached_input_tokens": uncached,
        "output_tokens": int(usage["output_tokens"]),
        "cached_input_tokens": int(usage["cached_input_tokens"]),
        "input_tokens": int(usage["input_tokens"]),
        "web_calls": web_calls,
        "custom_outputs": custom_outputs,
        "custom_calls": custom_calls,
        "file_change_events": file_change_events,
    }


def parse_trace(task_name: str) -> dict[str, Any]:
    trace_path = find_trace_path(task_name)
    if trace_path is None:
        raise RuntimeError(f"expected one runtime trace for {task_name}, found none")
    return _parse_trace_at_path(task_name, trace_path)


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def timestamp_from_epoch(value: float) -> str:
    return iso(datetime.fromtimestamp(value, tz=ZoneInfo("UTC")).astimezone(LOCAL_TZ))


def normalize_query_from_call(call: dict[str, Any], opened_url: str) -> str:
    raw = str(call["payload"]["input"])
    query_match = re.search(r'(?:"q"|\bq)\s*:\s*"((?:\\.|[^"\\])*)"', raw)
    if query_match is not None:
        return json.loads(f'"{query_match.group(1)}"')
    if re.search(r'(?:"open"|\bopen)\s*:', raw):
        return f"open {opened_url}"
    raise RuntimeError("research tool call is neither a search nor an open")


def call_output_contains_url(trace: dict[str, Any], call_id: str, url: str) -> bool:
    """Prove the declared source URL was present in that exact tool result."""
    output_record = trace["custom_outputs"].get(call_id)
    if output_record is None or not isinstance(url, str) or not url.strip():
        return False
    payload = output_record.get("payload", {}).get("output")

    def strings(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return [text for item in value for text in strings(item)]
        if isinstance(value, dict):
            return [text for item in value.values() for text in strings(item)]
        return []

    return any(url in value for value in strings(payload))


def call_source_time(trace: dict[str, Any], call_id: str) -> str:
    output_record = trace["custom_outputs"].get(call_id)
    if output_record is None:
        raise RuntimeError(f"missing output record for {call_id}")
    return iso(parse_timestamp(output_record["timestamp"]).astimezone(LOCAL_TZ))


class ApplyPatchTraceEncodingError(RuntimeError):
    """The runtime trace does not use an approved apply-patch representation."""


def _outer_tool_call_kind(call: dict[str, Any]) -> str | None:
    payload = call.get("payload", {})
    raw = payload.get("input")
    if payload.get("name") == "apply_patch":
        return "apply_patch"
    if not isinstance(raw, str):
        return None
    if raw.startswith("*** Begin Patch\n") or re.match(
        r"\A[ \t\r\n]*const[ \t\r\n]+patch\b", raw
    ):
        return "apply_patch"
    if _EXEC_COMMAND_PREFIX_RE.match(raw) is not None:
        return "exec_command"
    if re.match(_WEB_CALL_PREFIX_PATTERN, raw) is not None:
        return "web__run"
    if "apply_patch" in raw:
        return "apply_patch"
    if "exec_command" in raw:
        return "exec_command"
    if "web__run" in raw:
        return "web__run"
    return None


def _is_apply_patch_call(call: dict[str, Any]) -> bool:
    return _outer_tool_call_kind(call) == "apply_patch"


def _decode_strict_web_call(call: dict[str, Any]) -> str:
    raw = call.get("payload", {}).get("input")
    if not isinstance(raw, str):
        raise RuntimeError("web tool call input is not text")
    search_match = _WEB_SEARCH_WRAPPER_RE.fullmatch(raw)
    open_match = _WEB_OPEN_WRAPPER_RE.fullmatch(raw)
    match = search_match or open_match
    if match is None:
        raise RuntimeError(
            "web tool call is not an exact single search/open wrapper; nested or extra statements are forbidden"
        )
    try:
        response_length = json.loads(match.group("length"))
        value = json.loads(
            match.group("query") if search_match is not None else match.group("ref_id")
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError("web tool wrapper contains malformed JSON string literals") from exc
    if response_length not in {"short", "medium", "long"}:
        raise RuntimeError("web tool wrapper has an unsupported response length")
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError("web tool wrapper has an empty search/open value")
    return "search" if search_match is not None else "open"


def _decode_bounded_exec_command(call: dict[str, Any], packet_path: Path) -> str:
    raw = call.get("payload", {}).get("input")
    if not isinstance(raw, str):
        raise RuntimeError(
            f"agent packet read is not a machine-parseable bounded command: {packet_path}"
        )
    wrapper_match = _EXEC_COMMAND_WRAPPER_RE.fullmatch(raw)
    if wrapper_match is None:
        raise RuntimeError(
            f"agent packet read uses an unsupported wrapper or nested statement: {packet_path}"
        )
    try:
        command = json.loads(wrapper_match.group("cmd"))
        workdir_literal = wrapper_match.group("workdir")
        workdir = json.loads(workdir_literal) if workdir_literal is not None else None
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"agent packet read arguments are malformed: {packet_path}") from exc
    if workdir is not None and workdir != str(WORKSPACE):
        raise RuntimeError(f"agent packet read uses an unapproved working directory: {packet_path}")
    for group, label, minimum, maximum in (
        ("yield_time_ms", "yield-time-ms", 250, 30_000),
        ("max_output_tokens", "max-output-tokens", 1, 1_000_000),
    ):
        raw_value = wrapper_match.group(group)
        if raw_value is not None and not minimum <= int(raw_value) <= maximum:
            raise RuntimeError(f"agent packet read uses an invalid {label}: {packet_path}")
    if not isinstance(command, str):
        raise RuntimeError(f"agent packet read command is malformed: {packet_path}")
    allowed_read = re.fullmatch(
        r"sed -n '[0-9]+,[0-9]+p' " + re.escape(str(packet_path)), command
    )
    if allowed_read is None:
        raise RuntimeError(
            f"agent packet read must be one exact bounded sed command for {packet_path}"
        )
    return command


def _canonical_expected_output_path(output_path: Path) -> Path:
    expected = Path(output_path)
    if not expected.is_absolute() or os.path.normpath(str(expected)) != str(expected):
        raise RuntimeError(f"bounded return path is not an absolute canonical path: {expected}")
    if unicodedata.normalize("NFC", str(expected)) != str(expected):
        raise RuntimeError(f"bounded return path is not in canonical Unicode form: {expected!r}")
    forbidden_unicode_categories = {"Cc", "Cf", "Cs", "Zl", "Zp"}
    if any(
        unicodedata.category(character) in forbidden_unicode_categories
        for character in str(expected)
    ):
        raise RuntimeError(
            f"bounded return path contains a control or format character: {expected!r}"
        )
    return expected


def _require_exact_existing_path_spelling(path: Path, label: str) -> None:
    """Reject case/normalization aliases on filesystems that resolve them."""
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        try:
            if current.name not in os.listdir(current.parent):
                raise RuntimeError(
                    f"{label} uses an alternate filesystem spelling: {current}"
                )
        except OSError as exc:
            raise RuntimeError(f"{label} spelling cannot be verified: {current}") from exc


def _canonical_run_owned_return_path(output_path: Path, run_dir: Path) -> Path:
    """Bind a canonical output path to one run's direct agent_returns directory."""
    run_root = Path(run_dir)
    if not run_root.is_absolute() or os.path.normpath(str(run_root)) != str(run_root):
        raise RuntimeError(f"bounded return run path is not absolute and canonical: {run_root}")
    if unicodedata.normalize("NFC", str(run_root)) != str(run_root) or any(
        unicodedata.category(character) in {"Cc", "Cf", "Cs", "Zl", "Zp"}
        for character in str(run_root)
    ):
        raise RuntimeError(f"bounded return run path spelling is not canonical: {run_root!r}")
    try:
        if not run_root.is_dir() or run_root.resolve(strict=True) != run_root:
            raise RuntimeError(f"bounded return run path is missing or symlinked: {run_root}")
        _require_exact_existing_path_spelling(run_root, "bounded return run path")
    except OSError as exc:
        raise RuntimeError(f"bounded return run path is missing or symlinked: {run_root}") from exc

    expected = _canonical_expected_output_path(output_path)
    return_dir = run_root / "agent_returns"
    if expected.parent != return_dir:
        raise RuntimeError(
            f"bounded return path is outside the run-owned agent_returns directory: {expected}"
        )
    try:
        if (
            return_dir.is_symlink()
            or not return_dir.is_dir()
            or return_dir.resolve(strict=True) != return_dir
        ):
            raise RuntimeError(
                f"bounded return directory is missing or symlinked: {return_dir}"
            )
        _require_exact_existing_path_spelling(
            return_dir, "bounded return directory"
        )
    except OSError as exc:
        raise RuntimeError(
            f"bounded return directory is missing or symlinked: {return_dir}"
        ) from exc

    current = Path(expected.anchor)
    for part in expected.parts[1:]:
        current /= part
        if current.is_symlink():
            raise RuntimeError(f"bounded return path contains a symlink: {current}")
        if current == expected:
            if current.exists():
                raise RuntimeError(
                    f"bounded Add File target already exists or aliases an existing path: {expected}"
                )
            continue
        if not current.is_dir():
            raise RuntimeError(f"bounded return path component is missing or unsafe: {current}")
    try:
        if expected.resolve(strict=False) != expected:
            raise RuntimeError(f"bounded return path contains an alias or symlink: {expected}")
    except OSError as exc:
        raise RuntimeError(f"bounded return path cannot be resolved safely: {expected}") from exc
    return expected


def bounded_return_instruction(output_path: Path, run_dir: Path) -> str:
    """Render the sole path-bound bounded-write instruction for one packet."""
    expected = _canonical_run_owned_return_path(output_path, run_dir)
    return f"""The decoded patch must use this exact absolute header:

```text
*** Begin Patch
*** Add File: {expected}
```

Relative paths, workspace-relative paths, `..`, aliases, symlinks, alternate spellings, and any other file operation are forbidden.

Use this wrapper exactly:

```javascript
{CANONICAL_BOUNDED_RETURN_WRAPPER}
```"""


def assert_bounded_return_packet(
    packet_path: Path, output_path: Path, run_dir: Path
) -> str:
    """Fail closed unless an immutable packet has one exact path-bound instruction."""
    run_root = Path(run_dir)
    expected = _canonical_run_owned_return_path(output_path, run_root)
    packet = Path(packet_path)
    if (
        not packet.is_absolute()
        or os.path.normpath(str(packet)) != str(packet)
        or packet.parent != run_root / "context"
    ):
        raise RuntimeError(f"bounded return packet path is not canonical and run-owned: {packet}")
    if unicodedata.normalize("NFC", str(packet)) != str(packet):
        raise RuntimeError(f"bounded return packet path is not in canonical Unicode form: {packet}")
    parent_descriptor: int | None = None
    descriptor: int | None = None
    try:
        parent_descriptor, packet_name = _safe_parent_descriptor(packet, create=False)
        if packet_name not in os.listdir(parent_descriptor):
            raise RuntimeError(
                f"bounded return packet path uses an alternate filesystem spelling: {packet}"
            )
        descriptor = os.open(
            packet_name,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_descriptor,
        )
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(
                f"bounded return packet is not one immutable run-owned regular file: {packet}"
            )
        if packet.resolve(strict=True) != packet:
            raise RuntimeError(f"bounded return packet path contains an alias or symlink: {packet}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            != (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        ):
            raise RuntimeError(f"bounded return packet changed while being verified: {packet}")
        packet_bytes = b"".join(chunks)
        packet_text = packet_bytes.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise RuntimeError(f"bounded return packet is unreadable: {packet}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if parent_descriptor is not None:
            os.close(parent_descriptor)

    expected_declaration = f"- Required return path: `{expected}`"
    declaration_lines = _REQUIRED_RETURN_PATH_LINE_RE.findall(packet_text)
    if declaration_lines != [expected_declaration]:
        raise RuntimeError(
            f"bounded return packet must declare exactly one matching absolute return path: {packet}"
        )

    expected_add_file = f"*** Add File: {expected}"
    add_file_lines = _ADD_FILE_INSTRUCTION_LINE_RE.findall(packet_text)
    if add_file_lines != [expected_add_file]:
        raise RuntimeError(
            f"bounded return packet must contain exactly one matching absolute Add File header: {packet}"
        )
    operation_lines = [
        line
        for line in packet_text.splitlines()
        if _PATCH_OPERATION_PRESENTATION_RE.search(line) is not None
    ]
    if operation_lines != ["*** Begin Patch", expected_add_file]:
        raise RuntimeError(
            f"bounded return packet contains an alternate or duplicate patch operation: {packet}"
        )

    expected_instruction = bounded_return_instruction(expected, run_root)
    if packet_text.count(expected_instruction) != 1:
        raise RuntimeError(
            f"bounded return packet must contain exactly one canonical path-bound instruction: {packet}"
        )
    if (
        packet_text.count(CANONICAL_BOUNDED_RETURN_WRAPPER) != 1
        or packet_text.count('const patch = "') != 1
        or packet_text.count("apply_patch") != 1
        or packet_text.count("text(result);") != 1
    ):
        raise RuntimeError(
            f"bounded return packet must contain exactly one canonical long-form wrapper: {packet}"
        )
    if _OUTPUT_PATH_PLACEHOLDER_RE.search(packet_text) is not None:
        raise RuntimeError(f"bounded return packet contains an output-path placeholder: {packet}")
    residual_text = packet_text.replace(expected_instruction, "").replace(
        expected_declaration, ""
    )
    if (
        "agent_returns/" in residual_text
        or _RESIDUAL_RETURN_ALTERNATIVE_RE.search(residual_text) is not None
    ):
        raise RuntimeError(
            f"bounded return packet contains a second or alternate return path: {packet}"
        )
    residual_text = residual_text.replace(str(expected), "")
    forbidden_relative_spellings = {
        expected.relative_to(run_root).as_posix(),
        expected.relative_to(run_root.parent).as_posix(),
    }
    try:
        forbidden_relative_spellings.add(expected.relative_to(WORKSPACE).as_posix())
    except ValueError:
        pass
    if any(spelling and spelling in residual_text for spelling in forbidden_relative_spellings):
        raise RuntimeError(
            f"bounded return packet contains a relative or workspace-relative alternative: {packet}"
        )
    return sha256_bytes(packet_bytes)


def assert_bounded_return_precommit(
    packet_path: Path,
    output_path: Path,
    run_dir: Path,
    precommit_path: Path,
    *,
    expected_agent_id: str,
    expected_stage: str,
) -> dict[str, Any]:
    """Recheck one deterministic packet/precommit pair at dispatch authorization."""
    run_root = Path(run_dir)
    packet = Path(packet_path)
    output = Path(output_path)
    precommit_file = Path(precommit_path)
    packet_digest = assert_bounded_return_packet(packet, output, run_root)
    if (
        not precommit_file.is_absolute()
        or os.path.normpath(str(precommit_file)) != str(precommit_file)
        or precommit_file.parent != run_root / "allocation_precommits"
        or unicodedata.normalize("NFC", str(precommit_file)) != str(precommit_file)
    ):
        raise RuntimeError(
            f"bounded return precommit path is not canonical and run-owned: {precommit_file}"
        )
    _require_safe_file(precommit_file, "bounded return allocation precommit")
    try:
        precommit_status = precommit_file.stat(follow_symlinks=False)
        if (
            precommit_status.st_nlink != 1
            or precommit_file.resolve(strict=True) != precommit_file
            or precommit_file.name not in os.listdir(precommit_file.parent)
        ):
            raise RuntimeError(
                f"bounded return allocation precommit is aliased: {precommit_file}"
            )
    except OSError as exc:
        raise RuntimeError(
            f"bounded return allocation precommit is unsafe: {precommit_file}"
        ) from exc
    precommit = _read_json_object(
        precommit_file, "bounded return allocation precommit"
    )
    expected_packet_relative = packet.relative_to(run_root).as_posix()
    expected_output_relative = output.relative_to(run_root).as_posix()
    if (
        precommit.get("schema")
        not in {"zt1-allocation-precommit-v1", "zt1-candidate-allocation-precommit-v2"}
        or precommit.get("agent_id") != expected_agent_id
        or precommit.get("stage") != expected_stage
        or precommit.get("packet_path") != expected_packet_relative
        or precommit.get("output_path") != expected_output_relative
        or precommit.get("packet_sha256") != packet_digest
    ):
        raise RuntimeError(
            "bounded return dispatch identity, paths, or immutable packet hash "
            f"differ from precommit: {precommit_file}"
        )
    return precommit


def _parse_single_add_file_patch(patch: str, expected: Path) -> bytes:
    if "\r" in patch:
        raise ApplyPatchTraceEncodingError(
            f"unsupported apply_patch trace encoding for {expected}: patch must use LF newlines"
        )
    body = patch[:-1] if patch.endswith("\n") else patch
    lines = body.split("\n")
    begin = "*** Begin Patch"
    end = "*** End Patch"
    add_prefix = "*** Add File: "
    add_headers = [line for line in lines if line.startswith(add_prefix)]
    if lines.count(begin) != 1 or lines.count(end) != 1 or len(add_headers) != 1:
        raise RuntimeError(
            f"bounded apply_patch must contain exactly one begin, add-file, and end header: {expected}"
        )

    target = add_headers[0][len(add_prefix) :]
    target_segments = target.split("/")
    if (
        not Path(target).is_absolute()
        or any(segment in {".", ".."} for segment in target_segments)
        or os.path.normpath(target) != target
    ):
        raise RuntimeError(f"bounded apply_patch target is not canonical: {target!r}")
    if target != str(expected):
        raise RuntimeError(
            f"bounded apply_patch target does not equal expected canonical path: {expected}"
        )

    operation_headers = [line for line in lines if line.startswith("*** ")]
    expected_headers = [begin, f"{add_prefix}{expected}", end]
    if operation_headers != expected_headers or lines[:2] != expected_headers[:2] or lines[-1] != end:
        raise RuntimeError(
            f"bounded apply_patch contains an unsupported update, delete, move, or alternate operation: {expected}"
        )

    added_lines = lines[2:-1]
    if any(not line.startswith("+") for line in added_lines):
        raise RuntimeError(f"bounded add-file patch contains a non-add content line: {expected}")
    added_text = "\n".join(line[1:] for line in added_lines)
    if added_lines:
        added_text += "\n"
    try:
        return added_text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ApplyPatchTraceEncodingError(
            f"unsupported apply_patch trace encoding for {expected}: decoded patch is not UTF-8"
        ) from exc


def _decode_apply_patch_call(call: dict[str, Any], expected: Path) -> tuple[bytes, str]:
    raw = call.get("payload", {}).get("input")
    if not isinstance(raw, str):
        raise ApplyPatchTraceEncodingError(
            f"unsupported apply_patch trace encoding for {expected}: tool input is not text"
        )

    wrapper_match = _APPLY_PATCH_LONG_WRAPPER_RE.fullmatch(raw)
    if wrapper_match is None:
        wrapper_match = _APPLY_PATCH_INLINE_AWAIT_WRAPPER_RE.fullmatch(raw)
    if wrapper_match is not None:
        literal = wrapper_match.group("patch_literal")
        try:
            patch = json.loads(literal)
        except json.JSONDecodeError as exc:
            raise ApplyPatchTraceEncodingError(
                f"unsupported apply_patch trace encoding for {expected}: malformed JSON string literal"
            ) from exc
        if not isinstance(patch, str):
            raise ApplyPatchTraceEncodingError(
                f"unsupported apply_patch trace encoding for {expected}: patch literal is not text"
            )
        representation = "json-string-wrapper"
    elif raw.startswith("*** Begin Patch\n"):
        patch = raw
        representation = "legacy-raw-patch"
    else:
        raise ApplyPatchTraceEncodingError(
            f"unsupported apply_patch trace encoding for {expected}: expected one of the two exact JSON-string wrappers or strict raw patch"
        )
    return _parse_single_add_file_patch(patch, expected), representation


def _record_ordinal(record: dict[str, Any], label: str, expected: Path) -> int:
    ordinal = record.get("ordinal")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool):
        raise RuntimeError(f"{label} lacks an exact runtime ordinal for {expected}")
    return ordinal


def _corresponding_file_change_event(
    trace: dict[str, Any],
    call: dict[str, Any],
    expected: Path,
    added_bytes: bytes,
) -> dict[str, Any]:
    call_id = call.get("payload", {}).get("call_id")
    if not isinstance(call_id, str) or not call_id:
        raise RuntimeError(f"apply_patch call lacks an exact call ID for {expected}")
    output_record = trace.get("custom_outputs", {}).get(call_id)
    if output_record is None:
        raise RuntimeError(f"apply_patch call lacks corresponding custom-tool output for {expected}")
    if call.get("payload", {}).get("status") != "completed":
        raise RuntimeError(f"apply_patch call did not complete for {expected}")

    call_ordinal = _record_ordinal(call, "apply_patch call", expected)
    output_ordinal = _record_ordinal(output_record, "apply_patch custom-tool output", expected)
    file_change_events = trace.get("file_change_events")
    if not isinstance(file_change_events, list) or len(file_change_events) != 1:
        raise RuntimeError(
            f"apply_patch trace must contain exactly one FileChange tool result for {expected}"
        )
    event = file_change_events[0]
    event_ordinal = _record_ordinal(event, "apply_patch FileChange result", expected)
    if not call_ordinal < event_ordinal < output_ordinal:
        raise RuntimeError(f"apply_patch FileChange result is not paired with its call for {expected}")

    call_turn = call.get("payload", {}).get(
        "internal_chat_message_metadata_passthrough", {}
    ).get("turn_id")
    output_turn = output_record.get("payload", {}).get(
        "internal_chat_message_metadata_passthrough", {}
    ).get("turn_id")
    event_turn = event.get("payload", {}).get("turn_id")
    if not isinstance(call_turn, str) or not call_turn or not (call_turn == event_turn == output_turn):
        raise RuntimeError(f"apply_patch call/result turn identity mismatch for {expected}")

    item = event.get("payload", {}).get("item", {})
    changes = item.get("changes")
    if (
        item.get("type") != "FileChange"
        or item.get("status") != "completed"
        or not isinstance(changes, dict)
        or list(changes) != [str(expected)]
    ):
        raise RuntimeError(
            f"apply_patch tool result does not attest one added expected path: {expected}"
        )
    change = changes[str(expected)]
    if (
        not isinstance(change, dict)
        or set(change) != {"type", "content"}
        or change.get("type") != "add"
        or not isinstance(change.get("content"), str)
    ):
        raise RuntimeError(f"apply_patch tool result is not one file creation for {expected}")
    try:
        result_bytes = change["content"].encode("utf-8")
    except UnicodeEncodeError as exc:
        raise RuntimeError(f"apply_patch tool result content is not UTF-8 for {expected}") from exc
    if result_bytes != added_bytes:
        raise RuntimeError(f"apply_patch patch bytes and tool result differ for {expected}")
    if (
        item.get("stdout")
        != f"Success. Updated the following files:\nA {expected}\n"
        or item.get("stderr") != ""
    ):
        raise RuntimeError(f"apply_patch tool output path/status mismatch for {expected}")
    timestamp = event.get("timestamp")
    if not isinstance(timestamp, str):
        raise RuntimeError(f"apply_patch FileChange result lacks a timestamp for {expected}")
    try:
        parse_timestamp(timestamp)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"apply_patch FileChange result has an invalid timestamp for {expected}") from exc
    return event


def _verify_resulting_added_file(expected: Path, added_bytes: bytes) -> None:
    current = Path(expected.anchor)
    for part in expected.parts[1:]:
        current /= part
        try:
            component_stat = current.lstat()
        except OSError as exc:
            raise RuntimeError(f"bounded return file or path component is missing: {expected}") from exc
        if stat.S_ISLNK(component_stat.st_mode):
            raise RuntimeError(f"bounded return path contains a symlink: {current}")
        try:
            if current.name not in os.listdir(current.parent):
                raise RuntimeError(
                    f"bounded return path uses an alternate filesystem spelling: {current}"
                )
        except OSError as exc:
            raise RuntimeError(
                f"bounded return path spelling cannot be verified: {current}"
            ) from exc
        if current != expected and not stat.S_ISDIR(component_stat.st_mode):
            raise RuntimeError(f"bounded return path component is not a directory: {current}")
    target_stat = expected.lstat()
    if not stat.S_ISREG(target_stat.st_mode):
        raise RuntimeError(f"bounded return is not a regular file: {expected}")
    if target_stat.st_nlink != 1:
        raise RuntimeError(f"bounded return is a hard-link alias: {expected}")
    try:
        if expected.resolve(strict=True) != expected:
            raise RuntimeError(f"bounded return does not resolve to its canonical path: {expected}")
        descriptor = os.open(expected, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise RuntimeError(f"bounded return cannot be opened without following links: {expected}") from exc
    try:
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode):
            raise RuntimeError(f"bounded return is not a regular opened file: {expected}")
        if (
            opened_stat.st_nlink != 1
            or (opened_stat.st_dev, opened_stat.st_ino)
            != (target_stat.st_dev, target_stat.st_ino)
        ):
            raise RuntimeError(f"bounded return opened through an alias or race: {expected}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
    finally:
        os.close(descriptor)
    if b"".join(chunks) != added_bytes:
        raise RuntimeError(f"apply_patch bytes differ from resulting file: {expected}")


def verify_single_bounded_apply_patch(
    trace: dict[str, Any], output_path: Path
) -> dict[str, Any]:
    """Decode and attest the trace's sole exact bounded add-file operation."""
    expected = _canonical_expected_output_path(output_path)
    write_calls = [call for call in trace.get("custom_calls", []) if _is_apply_patch_call(call)]
    if len(write_calls) != 1:
        raise RuntimeError(
            f"agent must make exactly one machine-recognizable bounded apply_patch call: {expected}"
        )
    call = write_calls[0]
    added_bytes, representation = _decode_apply_patch_call(call, expected)
    event = _corresponding_file_change_event(trace, call, expected, added_bytes)
    _verify_resulting_added_file(expected, added_bytes)
    return {
        "call_id": call["payload"]["call_id"],
        "representation": representation,
        "path": str(expected),
        "added_sha256": hashlib.sha256(added_bytes).hexdigest(),
        "completed_at": event["timestamp"],
    }


def apply_patch_completion_time(trace: dict[str, Any], output_path: Path) -> str:
    attestation = verify_single_bounded_apply_patch(trace, output_path)
    return iso(parse_timestamp(attestation["completed_at"]).astimezone(LOCAL_TZ))


def assert_single_packet_read(trace: dict[str, Any], packet_path: Path, output_path: Path) -> None:
    write_attestation = verify_single_bounded_apply_patch(trace, output_path)
    write_call_id = write_attestation["call_id"]
    read_calls: list[dict[str, Any]] = []
    write_calls: list[dict[str, Any]] = []
    web_calls: list[dict[str, Any]] = []
    undeclared_calls: list[dict[str, Any]] = []
    for call in trace["custom_calls"]:
        call_id = call.get("payload", {}).get("call_id")
        if call_id == write_call_id:
            write_calls.append(call)
            continue
        kind = _outer_tool_call_kind(call)
        if kind == "exec_command":
            _decode_bounded_exec_command(call, packet_path)
            read_calls.append(call)
        elif kind == "web__run":
            _decode_strict_web_call(call)
            web_calls.append(call)
        else:
            undeclared_calls.append(call)
    if len(read_calls) != 1:
        raise RuntimeError(f"agent read outside its one allowlisted packet: {packet_path}")
    if len(write_calls) != 1:
        raise RuntimeError(f"agent did not preserve one bounded return path: {output_path}")
    if undeclared_calls:
        raise RuntimeError(f"agent used an undeclared non-research tool while handling {packet_path}")


def concept_markdown(concept: dict[str, Any], creator_agent_id: str) -> str:
    hypotheses = "; ".join(concept["hypotheses"])
    prohibited = concept["prohibited_reliance"] or "None identified in this raw hypothesis."
    return f"""### {concept['raw_id']} — {concept['title']}

- Creator agent: `{creator_agent_id}`
- One-sentence thesis: {concept['one_sentence_thesis']}
- Customer / loss: {concept['customer']} / {concept['loss_event']}
- Payer / beneficiary: {concept['payer']} / {concept['beneficiary']}
- Authority / distributor: {concept['authority_holder']} / {concept['distributor']}
- Risk bearer / transaction owner: {concept['risk_bearer']} / {concept['transaction_owner']}
- First paid event: {concept['first_paid_event']}
- Acquisition route: {concept['acquisition_route']}
- Possible compounding asset: {concept['compounding_asset']}
- Mechanism class: {concept['mechanism_class']}
- Evidence ID: `{concept['evidence_id']}`
- Constraint class: `{concept['constraint_class']}`
- Hypotheses: {hypotheses}
- Prohibited reliance: {prohibited}
"""


def integrate_baseline_generation(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    launch = json.loads((run_dir / "baseline_generation_launch.json").read_text(encoding="utf-8"))
    if launch.get("seed") != seed:
        raise RuntimeError("baseline generation launch seed differs from registration")
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    checkpoints = [record for record in records if record.get("record_type") == "checkpoint"]
    if [checkpoint.get("state") for checkpoint in checkpoints] != ["registered"]:
        raise RuntimeError("baseline generation integration requires only the registered checkpoint")
    run_record = records[0]
    all_concepts: dict[str, tuple[dict[str, Any], str]] = {}
    pending_evidence: list[dict[str, Any]] = []
    research_entries: list[str] = []
    new_manifest_records: list[dict[str, Any]] = []
    trace_dir = run_dir / "trace_attestations"
    ensure_safe_directory(trace_dir)
    source_cursor = 1
    for launch_agent in launch["agents"]:
        agent_id = launch_agent["agent_id"]
        task_name = trace_task_name(run_dir, agent_id)
        output_path = Path(launch_agent["output_path"])
        packet_path = Path(launch_agent["packet_path"])
        precommit_path = Path(launch_agent["allocation_precommit_path"])
        output = json.loads(output_path.read_text(encoding="utf-8"))
        precommit = json.loads(precommit_path.read_text(encoding="utf-8"))
        if precommit.get("seed") != seed:
            raise RuntimeError(f"baseline generation precommit seed differs for {agent_id}")
        expected_top = {
            "agent_id",
            "role",
            "assigned_ids",
            "output_ids",
            "queries",
            "concepts",
            "files_read",
        }
        if set(output) != expected_top:
            raise RuntimeError(f"{agent_id} return uses an unexpected schema")
        if (
            output["agent_id"] != agent_id
            or output["role"] != launch_agent["role"]
            or output["assigned_ids"] != precommit["assigned_ids"]
            or output["output_ids"] != precommit["output_ids"]
            or output["files_read"] != [precommit["packet_path"]]
            or len(output["queries"]) != 2
            or len(output["concepts"]) != len(precommit["output_ids"])
        ):
            raise RuntimeError(f"{agent_id} return does not reconcile its immutable assignment")
        if [concept.get("raw_id") for concept in output["concepts"]] != precommit["output_ids"]:
            raise RuntimeError(f"{agent_id} concept order/IDs drifted")
        trace = parse_trace(task_name)
        if len(trace["web_calls"]) != 4:
            raise RuntimeError(f"{agent_id} used {len(trace['web_calls'])} web calls instead of four")
        assert_single_packet_read(trace, packet_path, output_path)
        start = parse_timestamp(trace["started_at"]).astimezone(LOCAL_TZ)
        end = parse_timestamp(trace["ended_at"]).astimezone(LOCAL_TZ)
        allocation_created = datetime.fromisoformat(precommit["created_at"])
        if not allocation_created < start < end:
            raise RuntimeError(f"{agent_id} allocation/agent chronology is invalid")
        resources = {
            "uncached_input_tokens": trace["uncached_input_tokens"],
            "output_tokens": trace["output_tokens"],
            "elapsed_microseconds": elapsed_microseconds(start, end),
        }
        context_rel = precommit["packet_path"]
        new_manifest_records.append(
            {
                "record_type": "agent",
                "scope_id": ROOT_SCOPE_ID,
                "agent_id": agent_id,
                "arm": "matched_baseline",
                "stage": "generation",
                "role": output["role"],
                "fork_turns": "none",
                "context_classes": ["founder_constraints", "safety_legal", "neutral_evidence"],
                "context_files": [{"path": context_rel, "sha256": precommit["packet_sha256"]}],
                "allowlisted_files": [context_rel],
                "files_read": [context_rel],
                "model": trace["model"],
                "reasoning_effort": trace["reasoning_effort"],
                "metering_basis": "trace_derived_exact",
                "started_at": iso(start),
                "ended_at": iso(end),
                "resources": resources,
                "assigned_ids": output["assigned_ids"],
                "output_ids": output["output_ids"],
            }
        )
        allocation_id = precommit["allocation_id"]
        new_manifest_records.append(
            {
                "record_type": "allocation",
                "scope_id": ROOT_SCOPE_ID,
                "allocation_id": allocation_id,
                "agent_id": agent_id,
                "arm": "matched_baseline",
                "stage": "generation",
                "entity_ids": precommit["entity_ids"],
                "created_at": precommit["created_at"],
                "metering_basis": "trace_derived_exact",
                "resources": resources,
                "query_cap": precommit["query_cap"],
                "used_unique_queries": 4,
                "unused_queries": precommit["query_cap"] - 4,
            }
        )
        evidence_recorded_at = apply_patch_completion_time(trace, output_path)
        trace_calls: list[dict[str, Any]] = []
        for logical_index, query_info in enumerate(output["queries"]):
            group = precommit["evidence_groups"][logical_index]
            if (
                query_info["evidence_id"] != group["evidence_id"]
                or query_info["entity_ids"] != group["entity_ids"]
            ):
                raise RuntimeError(f"{agent_id} evidence group drifted")
            evidence_source_ids: list[str] = []
            for pair_offset in range(2):
                call = trace["web_calls"][logical_index * 2 + pair_offset]
                query_id = precommit["query_ids"][logical_index * 2 + pair_offset]
                call_id = call["payload"]["call_id"]
                call_meta = call["payload"].get("internal_chat_message_metadata_passthrough", {})
                create_time = call_meta.get("create_time")
                if not isinstance(create_time, (int, float)):
                    raise RuntimeError(f"{agent_id} web call lacks exact create_time")
                query_text = normalize_query_from_call(call, query_info["opened_url"])
                query_at = timestamp_from_epoch(float(create_time))
                tool_at = iso(parse_timestamp(call["timestamp"]).astimezone(LOCAL_TZ))
                source_at = call_source_time(trace, call_id)
                source_id = f"SRC-B-{source_cursor:04d}"
                source_cursor += 1
                evidence_source_ids.append(source_id)
                new_manifest_records.extend(
                    [
                        {
                            "record_type": "query",
                            "scope_id": ROOT_SCOPE_ID,
                            "query_id": query_id,
                            "allocation_id": allocation_id,
                            "agent_id": agent_id,
                            "arm": "matched_baseline",
                            "stage": "generation",
                            "query": " ".join(query_text.split()),
                            "entity_ids": group["entity_ids"],
                            "occurred_at": query_at,
                        },
                        {
                            "record_type": "tool_event",
                            "scope_id": ROOT_SCOPE_ID,
                            "call_id": call_id,
                            "query_id": query_id,
                            "allocation_id": allocation_id,
                            "agent_id": agent_id,
                            "arm": "matched_baseline",
                            "stage": "generation",
                            "tool": "web_search",
                            "event_type": "tool_call",
                            "occurred_at": tool_at,
                        },
                        {
                            "record_type": "source_open",
                            "scope_id": ROOT_SCOPE_ID,
                            "source_event_id": source_id,
                            "query_id": query_id,
                            "call_id": call_id,
                            "allocation_id": allocation_id,
                            "agent_id": agent_id,
                            "arm": "matched_baseline",
                            "stage": "generation",
                            "url": query_info["opened_url"],
                            "entity_ids": group["entity_ids"],
                            "evidence_ids": [group["evidence_id"]],
                            "occurred_at": source_at,
                        },
                    ]
                )
                trace_calls.append(
                    {
                        "query_id": query_id,
                        "call_id": call_id,
                        "source_event_id": source_id,
                        "query_occurred_at": query_at,
                        "tool_occurred_at": tool_at,
                        "source_occurred_at": source_at,
                    }
                )
            pending_evidence.append(
                {
                    "record_type": "evidence",
                    "scope_id": ROOT_SCOPE_ID,
                    "arm": "matched_baseline",
                    "stage": "generation",
                    "allocation_id": allocation_id,
                    "agent_id": agent_id,
                    "evidence_id": group["evidence_id"],
                    "direction_id": None,
                    "entity_ids": group["entity_ids"],
                    "source_event_ids": evidence_source_ids,
                    "recorded_at": evidence_recorded_at,
                    "decision_critical": False,
                    "status": "interpreted",
                    "proposition": query_info["proposition"],
                    "source": query_info["opened_url"],
                    "source_date": query_info["source_date"],
                    "cheapest_resolving_test": query_info["cheapest_resolving_test"],
                }
            )
            research_entries.append(
                f"## {group['evidence_id']}\n\n"
                f"- Agent / allocation: `{agent_id}` / `{allocation_id}`\n"
                f"- Entities: `{', '.join(group['entity_ids'])}`\n"
                f"- Proposition: {query_info['proposition']}\n"
                f"- Status: `interpreted`\n"
                f"- Source: {query_info['source_title']} — {query_info['opened_url']}\n"
                f"- Source date: {query_info['source_date'] or 'unknown'}\n"
                f"- Contradiction: {query_info['contradiction']}\n"
                f"- Recorded at: `{evidence_recorded_at}`\n"
                f"- Cheapest resolving test: {query_info['cheapest_resolving_test']}\n"
                f"- Source events: `{', '.join(evidence_source_ids)}`\n"
            )
        for concept in output["concepts"]:
            raw_id = concept["raw_id"]
            if raw_id in all_concepts:
                raise RuntimeError(f"duplicate raw concept ID {raw_id}")
            all_concepts[raw_id] = (concept, agent_id)
        attestation = {
            "schema": "zt1-runtime-trace-attestation-v1",
            "agent_id": agent_id,
            "trace_path": str(trace["trace_path"]),
            "trace_sha256": trace["trace_sha256"],
            "model": trace["model"],
            "reasoning_effort": trace["reasoning_effort"],
            "started_at": iso(start),
            "ended_at": iso(end),
            "input_tokens": trace["input_tokens"],
            "cached_input_tokens": trace["cached_input_tokens"],
            "uncached_input_tokens": trace["uncached_input_tokens"],
            "output_tokens": trace["output_tokens"],
            "web_calls": trace_calls,
            "packet_path": context_rel,
            "packet_sha256": precommit["packet_sha256"],
            "return_path": str(output_path.relative_to(run_dir)),
            "return_sha256": sha256(output_path),
        }
        write_exclusive_or_verify(trace_dir / f"{agent_id}.json", json_bytes(attestation))

    expected_raw_ids = [f"RAW-{index:03d}" for index in range(1, 49)]
    if sorted(all_concepts) != expected_raw_ids:
        raise RuntimeError("baseline raw pool does not contain exactly RAW-001 through RAW-048")
    raw_pool = "# Audited Funnel Baseline Raw Pool\n\n"
    raw_pool += "Unscored generation-only hypotheses. IDs are immutable.\n\n"
    raw_pool += "\n".join(
        concept_markdown(all_concepts[raw_id][0], all_concepts[raw_id][1])
        for raw_id in expected_raw_ids
    )
    raw_pool_path = run_dir / "02a_raw_pool.md"
    write_exclusive(raw_pool_path, raw_pool.encode("utf-8"))
    research_path = run_dir / "03_research_and_sources.md"
    write_exclusive(
        research_path,
        ("# Baseline Research And Sources\n\n" + "\n".join(research_entries)).encode("utf-8"),
    )
    pending_path = run_dir / "baseline_discovery_evidence_pending.json"
    write_exclusive(pending_path, json_bytes({"evidence": pending_evidence}))

    records.extend(new_manifest_records)
    checkpoint_at = now()
    latest_agent_end = max(
        parse_timestamp(record["ended_at"])
        for record in new_manifest_records
        if record.get("record_type") == "agent"
    )
    if checkpoint_at.astimezone(ZoneInfo("UTC")) <= latest_agent_end.astimezone(ZoneInfo("UTC")):
        raise RuntimeError("raw-frozen checkpoint does not follow every generation agent")
    run_start = datetime.fromisoformat(run_record["started_at"])
    agents = [record for record in records if record.get("record_type") == "agent"]
    query_records = [record for record in records if record.get("record_type") == "query"]
    totals = {
        "unique_queries": len({" ".join(record["query"].casefold().split()) for record in query_records}),
        "uncached_input_tokens": sum(int(record["resources"]["uncached_input_tokens"]) for record in agents),
        "output_tokens": sum(int(record["resources"]["output_tokens"]) for record in agents),
        "elapsed_microseconds": elapsed_microseconds(run_start, checkpoint_at),
    }
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-02-raw_frozen",
        "state": "raw_frozen",
        "predecessor_id": "CP-baseline-w01-01-registered",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in agents),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": raw_pool_path.name, "sha256": sha256(raw_pool_path)},
            {"path": research_path.name, "sha256": sha256(research_path)},
            {"path": pending_path.name, "sha256": sha256(pending_path)},
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "raw_frozen"
    run_record.pop("status", None)
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def prepare_baseline_history(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    prior_path = WORKING_FOLDER / "zero_to_one_candidates_20260822_110713" / "01b_history_fingerprints.md"
    bullet_lines = [
        line
        for line in prior_path.read_text(encoding="utf-8").splitlines()
        if re.match(r"^- `HIST-\d{3}` — ", line)
    ]
    if len(bullet_lines) != 28:
        raise RuntimeError("bounded neutral history source no longer contains the expected 28 fingerprints")
    packet_path = run_dir / "context" / "baseline-history-01.md"
    output_path = run_dir / "agent_returns" / "baseline-history-01.md"
    packet = f"""# Immutable Neutral History Packet

## Identity

- Scope: `{ROOT_SCOPE_ID}`
- Arm: `matched_baseline`
- Stage: `history_compressor`
- Agent ID: `baseline-history-01`
- Role: `neutral_history_compressor`
- Model: `{MODEL}`
- Reasoning: `{REASONING}`
- Seed: `{seed}`
- Query cap: `0`
- Required return path: `{output_path}`
- Source artifact: `{prior_path}`
- Source SHA-256: `{sha256(prior_path)}`

Read no other file. Do not browse. Do not create ideas, merge current concepts, choose concepts, or make merit judgments. Normalize only the supplied historical shapes. Preserve status as `confirmed`, `unvalidated`, `rejected`, or `unknown` and preserve source artifact IDs. Remove colorful rhetoric and any recommendations.

## Supplied Neutral Fingerprints

{chr(10).join(bullet_lines)}

## Required Return

Write one Markdown file at the required return path.

{bounded_return_instruction(output_path, run_dir)}

Start with `# Neutral Historical Fingerprints`. Emit exactly 28 numbered fingerprint bullets. Each bullet must preserve: stable ID; customer; loss event; payer; solution primitive; transaction unit or paid trigger; acquisition route; possible compounding asset; status; source artifact ID. Add no other sections or conclusions.
"""
    write_exclusive(packet_path, packet.encode("utf-8"))
    assert_bounded_return_packet(packet_path, output_path, run_dir)
    precommit = {
        "schema": "zt1-allocation-precommit-v1",
        "scope_id": ROOT_SCOPE_ID,
        "arm": "matched_baseline",
        "stage": "history_compressor",
        "agent_id": "baseline-history-01",
        "role": "neutral_history_compressor",
        "seed": seed,
        "allocation_id": "ALLOC-B-ZERO-HISTORY-01",
        "entity_ids": ["RAW-001"],
        "assigned_ids": ["RAW-001"],
        "output_ids": ["RAW-001"],
        "query_cap": 0,
        "planned_used_queries": 0,
        "created_at": iso(now()),
        "metering_basis": "trace_derived_exact",
        "packet_path": str(packet_path.relative_to(run_dir)),
        "packet_sha256": sha256(packet_path),
        "output_path": str(output_path.relative_to(run_dir)),
        "model": MODEL,
        "reasoning_effort": REASONING,
    }
    precommit_path = run_dir / "allocation_precommits" / "ALLOC-B-ZERO-HISTORY-01.json"
    write_exclusive(precommit_path, json_bytes(precommit))
    assert_bounded_return_precommit(
        packet_path,
        output_path,
        run_dir,
        precommit_path,
        expected_agent_id="baseline-history-01",
        expected_stage="history_compressor",
    )
    print(json.dumps({"packet_path": str(packet_path), "output_path": str(output_path), "task_name": trace_task_name(run_dir, "baseline-history-01")}, indent=2))


def integrate_zero_query_agent(
    *,
    run_dir: Path,
    task_name: str,
    agent_id: str,
    role: str,
    stage: str,
    packet_rel: str,
    output_rel: str,
    precommit_rel: str,
    context_classes: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    seed = authenticated_run_seed(run_dir)
    packet_path = run_dir / packet_rel
    output_path = run_dir / output_rel
    precommit = json.loads((run_dir / precommit_rel).read_text(encoding="utf-8"))
    if precommit.get("seed") != seed:
        raise RuntimeError(f"zero-query precommit seed differs for {agent_id}")
    expected_task_name = trace_task_name(run_dir, agent_id)
    if task_name != expected_task_name:
        raise RuntimeError(
            f"zero-query integration task must be run-unique: {expected_task_name}"
        )
    trace = parse_trace(expected_task_name)
    if trace["web_calls"]:
        raise RuntimeError(f"zero-query agent {agent_id} used web research")
    assert_single_packet_read(trace, packet_path, output_path)
    start = parse_timestamp(trace["started_at"]).astimezone(LOCAL_TZ)
    end = parse_timestamp(trace["ended_at"]).astimezone(LOCAL_TZ)
    if not datetime.fromisoformat(precommit["created_at"]) < start < end:
        raise RuntimeError(f"zero-query agent chronology is invalid for {agent_id}")
    resources = {
        "uncached_input_tokens": trace["uncached_input_tokens"],
        "output_tokens": trace["output_tokens"],
        "elapsed_microseconds": elapsed_microseconds(start, end),
    }
    agent = {
        "record_type": "agent",
        "scope_id": ROOT_SCOPE_ID,
        "agent_id": agent_id,
        "arm": "matched_baseline",
        "stage": stage,
        "role": role,
        "fork_turns": "none",
        "context_classes": context_classes,
        "context_files": [{"path": packet_rel, "sha256": precommit["packet_sha256"]}],
        "allowlisted_files": [packet_rel],
        "files_read": [packet_rel],
        "model": trace["model"],
        "reasoning_effort": trace["reasoning_effort"],
        "metering_basis": "trace_derived_exact",
        "started_at": iso(start),
        "ended_at": iso(end),
        "resources": resources,
        "assigned_ids": precommit["assigned_ids"],
        "output_ids": precommit["output_ids"],
    }
    allocation = {
        "record_type": "allocation",
        "scope_id": ROOT_SCOPE_ID,
        "allocation_id": precommit["allocation_id"],
        "agent_id": agent_id,
        "arm": "matched_baseline",
        "stage": stage,
        "entity_ids": precommit["entity_ids"],
        "created_at": precommit["created_at"],
        "metering_basis": "trace_derived_exact",
        "resources": resources,
        "query_cap": 0,
        "used_unique_queries": 0,
        "unused_queries": 0,
    }
    attestation = {
        "schema": "zt1-runtime-trace-attestation-v1",
        "agent_id": agent_id,
        "trace_path": str(trace["trace_path"]),
        "trace_sha256": trace["trace_sha256"],
        "model": trace["model"],
        "reasoning_effort": trace["reasoning_effort"],
        "started_at": iso(start),
        "ended_at": iso(end),
        "input_tokens": trace["input_tokens"],
        "cached_input_tokens": trace["cached_input_tokens"],
        "uncached_input_tokens": trace["uncached_input_tokens"],
        "output_tokens": trace["output_tokens"],
        "web_calls": [],
        "packet_path": packet_rel,
        "packet_sha256": precommit["packet_sha256"],
        "return_path": output_rel,
        "return_sha256": sha256(output_path),
    }
    return agent, allocation, attestation


def checkpoint_resource_totals(records: list[dict[str, Any]], run_start: datetime, at: datetime) -> dict[str, Any]:
    agents = [record for record in records if record.get("record_type") == "agent"]
    queries = [record for record in records if record.get("record_type") == "query"]
    return {
        "unique_queries": len({" ".join(record["query"].casefold().split()) for record in queries}),
        "uncached_input_tokens": sum(int(record["resources"]["uncached_input_tokens"]) for record in agents),
        "output_tokens": sum(int(record["resources"]["output_tokens"]) for record in agents),
        "elapsed_microseconds": elapsed_microseconds(run_start, at),
    }


def parse_history_fingerprints(path: Path) -> list[str]:
    required_fields = (
        "customer:",
        "loss event:",
        "payer:",
        "solution primitive:",
        "transaction unit or paid trigger:",
        "acquisition route:",
        "possible compounding asset:",
        "status:",
        "source artifact ID:",
    )
    fingerprints: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(?:- |\d+\. )(`(HIST-\d{3})` — .+)$", line)
        if not match:
            continue
        fingerprint_id = match.group(2)
        if fingerprint_id in fingerprints:
            raise RuntimeError(f"duplicate neutral history fingerprint: {fingerprint_id}")
        normalized = f"- {match.group(1)}"
        if any(field not in normalized for field in required_fields):
            raise RuntimeError(f"neutral history fingerprint lacks a required field: {fingerprint_id}")
        fingerprints[fingerprint_id] = normalized
    expected_ids = [f"HIST-{index:03d}" for index in range(1, 29)]
    if sorted(fingerprints) != expected_ids:
        raise RuntimeError("history compressor did not return the exact HIST-001 through HIST-028 set")
    return [fingerprints[fingerprint_id] for fingerprint_id in expected_ids]


def integrate_baseline_history(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    checkpoint_states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if checkpoint_states != ["registered", "raw_frozen"]:
        raise RuntimeError("history integration requires the exact registered -> raw_frozen prefix")
    agent, allocation, attestation = integrate_zero_query_agent(
        run_dir=run_dir,
        task_name=trace_task_name(run_dir, "baseline-history-01"),
        agent_id="baseline-history-01",
        role="neutral_history_compressor",
        stage="history_compressor",
        packet_rel="context/baseline-history-01.md",
        output_rel="agent_returns/baseline-history-01.md",
        precommit_rel="allocation_precommits/ALLOC-B-ZERO-HISTORY-01.json",
        context_classes=["history"],
    )
    raw_return = run_dir / "agent_returns" / "baseline-history-01.md"
    fingerprint_lines = parse_history_fingerprints(raw_return)
    canonical_path = run_dir / "01b_history_fingerprints.md"
    canonical = (
        "# Neutral Historical Fingerprints\n\n"
        "Comparison evidence only; no current concept is automatically excluded.\n\n"
        + "\n".join(fingerprint_lines)
        + "\n"
    )
    write_exclusive(canonical_path, canonical.encode("utf-8"))
    write_exclusive(
        run_dir / "trace_attestations" / "baseline-history-01.json",
        json_bytes(attestation),
    )
    records.extend([agent, allocation])
    checkpoint_at = now()
    if checkpoint_at <= datetime.fromisoformat(agent["ended_at"]):
        raise RuntimeError("history checkpoint does not follow its agent")
    run_record = records[0]
    totals = checkpoint_resource_totals(
        records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at
    )
    previous_agents = [
        record["agent_id"] for record in records if record.get("record_type") == "agent"
    ]
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-03-history_frozen",
        "state": "history_frozen",
        "predecessor_id": "CP-baseline-w01-02-raw_frozen",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(previous_agents),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": canonical_path.name, "sha256": sha256(canonical_path)},
            {"path": str(raw_return.relative_to(run_dir)), "sha256": sha256(raw_return)},
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "history_frozen"
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def baseline_raw_sections(run_dir: Path) -> list[tuple[str, str]]:
    text_value = (run_dir / "02a_raw_pool.md").read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^### (RAW-\d{3}) — .+$", text_value))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text_value)
        section = text_value[match.start() : end].strip()
        section = re.sub(r"(?m)^- Creator agent:.*\n", "", section)
        sections.append((match.group(1), section))
    expected = [f"RAW-{index:03d}" for index in range(1, 49)]
    if [raw_id for raw_id, _ in sections] != expected:
        raise RuntimeError("baseline raw pool no longer contains the exact RAW-001 through RAW-048 sequence")
    return sections


def prepare_baseline_cartography(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    records = read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen"]:
        raise RuntimeError("cartography preparation requires the exact history_frozen prefix")
    raw_sections = baseline_raw_sections(run_dir)
    history_text = (run_dir / "01b_history_fingerprints.md").read_text(encoding="utf-8")
    packet_path = run_dir / "context" / "baseline-cartography-01.md"
    output_path = run_dir / "agent_returns" / "baseline-cartography-01.json"
    packet = f"""# Immutable Baseline Semantic-Cartography Packet

## Identity And Boundary

- Scope: `{ROOT_SCOPE_ID}`
- Arm: `matched_baseline`
- Stage: `cartography`
- Agent ID: `baseline-cartography-01`
- Role: `semantic_cartographer`
- Model: `{MODEL}`
- Reasoning: `{REASONING}`
- Query cap: `0`
- Required return path: `{output_path}`
- Seed: `{seed}`

{bounded_return_instruction(output_path, run_dir)}

Read no other file. Do not browse. Do not rank merit, choose a research cohort, evaluate, validate, pivot, promote, regenerate, propose outreach, or execute a proof. The raw cards below have creator identity removed. Historical fingerprints are comparison evidence only and never automatic exclusions.

Create exactly 16 reversible economic directions `DIR-001` through `DIR-016`. Map every `RAW-001` through `RAW-048` exactly once. Compare on customer/loss event, payer/budget, paid trigger, transaction owner, acquisition route, and compounding asset. Preserve a distinct sibling whenever payer, paid trigger, transaction owner, or route materially differs. Use `retained` for a direction's representative, `merged` only for genuinely same-field variants, and `unresolved` when a sibling remains distinct inside the broader direction. Do not use `rejected` unless indispensability is plainly unlawful, seriously harmful, or directly contradicted by supplied evidence.

Return one JSON object using exactly this shape:

```json
{{
  "directions": [
    {{
      "direction_id": "DIR-001",
      "title": "neutral descriptive title",
      "customer_loss": "...",
      "payer_budget": "...",
      "paid_trigger": "...",
      "transaction_owner": "...",
      "acquisition_route": "...",
      "compounding_asset": "...",
      "raw_ids": ["RAW-001"],
      "nearest_history_ids": ["HIST-001"],
      "history_overlap_note": "neutral comparison",
      "disagreements": ["explicit unresolved field mismatch, or none"]
    }}
  ],
  "mappings": [
    {{
      "raw_id": "RAW-001",
      "direction_id": "DIR-001",
      "cluster_id": "CL-001",
      "disposition": "retained",
      "reason": "field-by-field rationale covering payer, paid trigger, owner, route, and any preserved mismatch"
    }}
  ],
  "effective_concept_count": 48,
  "method_note": "short non-merit description"
}}
```

Use each `DIR-NNN` exactly once in `directions`; every direction must have at least one mapped raw member and exactly one `retained` representative. Cluster IDs are reversible labels and need not equal direction IDs. Every `raw_ids` list must be exactly reciprocal with `mappings`. `nearest_history_ids` may be empty but may contain only `HIST-001` through `HIST-028`. `effective_concept_count` counts economically distinct shapes after only genuine same-field merges. Add no other top-level or direction/mapping fields.

## Author-Stripped Raw Cards

{chr(10).join(section for _, section in raw_sections)}

## Neutral Historical Fingerprints

{history_text}
"""
    write_exclusive(packet_path, packet.encode("utf-8"))
    assert_bounded_return_packet(packet_path, output_path, run_dir)
    raw_ids = [raw_id for raw_id, _ in raw_sections]
    precommit = {
        "schema": "zt1-allocation-precommit-v1",
        "scope_id": ROOT_SCOPE_ID,
        "arm": "matched_baseline",
        "stage": "cartography",
        "agent_id": "baseline-cartography-01",
        "role": "semantic_cartographer",
        "seed": seed,
        "allocation_id": "ALLOC-B-ZERO-CARTOGRAPHY-01",
        "entity_ids": raw_ids,
        "assigned_ids": raw_ids,
        "output_ids": raw_ids,
        "query_cap": 0,
        "planned_used_queries": 0,
        "created_at": iso(now()),
        "metering_basis": "trace_derived_exact",
        "packet_path": str(packet_path.relative_to(run_dir)),
        "packet_sha256": sha256(packet_path),
        "output_path": str(output_path.relative_to(run_dir)),
        "model": MODEL,
        "reasoning_effort": REASONING,
    }
    precommit_path = run_dir / "allocation_precommits" / "ALLOC-B-ZERO-CARTOGRAPHY-01.json"
    write_exclusive(precommit_path, json_bytes(precommit))
    assert_bounded_return_precommit(
        packet_path,
        output_path,
        run_dir,
        precommit_path,
        expected_agent_id="baseline-cartography-01",
        expected_stage="cartography",
    )
    print(json.dumps({"packet_path": str(packet_path), "output_path": str(output_path), "task_name": trace_task_name(run_dir, "baseline-cartography-01")}, indent=2))


def validate_baseline_cartography(payload: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(payload, dict) or set(payload) != {
        "directions", "mappings", "effective_concept_count", "method_note"
    }:
        raise RuntimeError("cartography return has an invalid top-level schema")
    directions = payload.get("directions")
    mappings = payload.get("mappings")
    if not isinstance(directions, list) or not isinstance(mappings, list):
        raise RuntimeError("cartography directions and mappings must be lists")
    if len(directions) != 16 or len(mappings) != 48:
        raise RuntimeError("cartography must return exactly 16 directions and 48 mappings")
    direction_fields = {
        "direction_id", "title", "customer_loss", "payer_budget", "paid_trigger",
        "transaction_owner", "acquisition_route", "compounding_asset", "raw_ids",
        "nearest_history_ids", "history_overlap_note", "disagreements",
    }
    mapping_fields = {"raw_id", "direction_id", "cluster_id", "disposition", "reason"}
    expected_directions = [f"DIR-{index:03d}" for index in range(1, 17)]
    expected_raw = [f"RAW-{index:03d}" for index in range(1, 49)]
    expected_history = {f"HIST-{index:03d}" for index in range(1, 29)}
    if sorted(item.get("direction_id") for item in directions if isinstance(item, dict)) != expected_directions:
        raise RuntimeError("cartography direction IDs are not exactly DIR-001 through DIR-016")
    if sorted(item.get("raw_id") for item in mappings if isinstance(item, dict)) != expected_raw:
        raise RuntimeError("cartography mapping IDs are not exactly RAW-001 through RAW-048")
    mapping_by_raw: dict[str, dict[str, Any]] = {}
    for item in mappings:
        if not isinstance(item, dict) or set(item) != mapping_fields:
            raise RuntimeError("cartography mapping uses an invalid schema")
        if item["direction_id"] not in expected_directions:
            raise RuntimeError(f"unknown mapping direction: {item['direction_id']}")
        if item["disposition"] not in {"retained", "merged", "unresolved", "rejected"}:
            raise RuntimeError(f"invalid mapping disposition: {item['raw_id']}")
        if not isinstance(item["cluster_id"], str) or not item["cluster_id"].strip():
            raise RuntimeError(f"missing cluster ID: {item['raw_id']}")
        if not isinstance(item["reason"], str) or not item["reason"].strip():
            raise RuntimeError(f"missing mapping rationale: {item['raw_id']}")
        mapping_by_raw[item["raw_id"]] = item
    seen_members: list[str] = []
    for direction in directions:
        if not isinstance(direction, dict) or set(direction) != direction_fields:
            raise RuntimeError("cartography direction uses an invalid schema")
        for field in direction_fields - {"raw_ids", "nearest_history_ids", "disagreements"}:
            if not isinstance(direction[field], str) or not direction[field].strip():
                raise RuntimeError(f"direction {direction.get('direction_id')} lacks {field}")
        raw_ids = direction["raw_ids"]
        history_ids = direction["nearest_history_ids"]
        disagreements = direction["disagreements"]
        if not isinstance(raw_ids, list) or not raw_ids or len(raw_ids) != len(set(raw_ids)):
            raise RuntimeError(f"direction {direction['direction_id']} has invalid raw_ids")
        if not isinstance(history_ids, list) or len(history_ids) != len(set(history_ids)) or not set(history_ids).issubset(expected_history):
            raise RuntimeError(f"direction {direction['direction_id']} has invalid history IDs")
        if not isinstance(disagreements, list) or any(not isinstance(value, str) for value in disagreements):
            raise RuntimeError(f"direction {direction['direction_id']} has invalid disagreements")
        reciprocal = sorted(
            raw_id for raw_id, mapping in mapping_by_raw.items()
            if mapping["direction_id"] == direction["direction_id"]
        )
        if sorted(raw_ids) != reciprocal:
            raise RuntimeError(f"direction {direction['direction_id']} raw membership is not reciprocal")
        if sum(mapping_by_raw[raw_id]["disposition"] == "retained" for raw_id in raw_ids) != 1:
            raise RuntimeError(f"direction {direction['direction_id']} does not have exactly one retained representative")
        seen_members.extend(raw_ids)
    if sorted(seen_members) != expected_raw:
        raise RuntimeError("cartography direction membership does not partition the raw pool")
    effective_count = payload.get("effective_concept_count")
    if not isinstance(effective_count, int) or isinstance(effective_count, bool) or not 16 <= effective_count <= 48:
        raise RuntimeError("cartography effective concept count is invalid")
    if not isinstance(payload.get("method_note"), str) or not payload["method_note"].strip():
        raise RuntimeError("cartography method note is missing")
    return directions, mappings


def integrate_baseline_cartography(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen"]:
        raise RuntimeError("cartography integration requires the exact history_frozen prefix")
    agent, allocation, attestation = integrate_zero_query_agent(
        run_dir=run_dir,
        task_name=trace_task_name(run_dir, "baseline-cartography-01"),
        agent_id="baseline-cartography-01",
        role="semantic_cartographer",
        stage="cartography",
        packet_rel="context/baseline-cartography-01.md",
        output_rel="agent_returns/baseline-cartography-01.json",
        precommit_rel="allocation_precommits/ALLOC-B-ZERO-CARTOGRAPHY-01.json",
        context_classes=["founder_constraints", "safety_legal", "neutral_evidence"],
    )
    return_path = run_dir / "agent_returns" / "baseline-cartography-01.json"
    directions, mappings = validate_baseline_cartography(
        json.loads(return_path.read_text(encoding="utf-8"))
    )
    creator_by_raw: dict[str, str] = {}
    for record in records:
        if record.get("record_type") == "agent" and record.get("stage") == "generation":
            for raw_id in record["output_ids"]:
                creator_by_raw[raw_id] = record["agent_id"]
    if sorted(creator_by_raw) != [f"RAW-{index:03d}" for index in range(1, 49)]:
        raise RuntimeError("cannot reconcile baseline raw creators")
    canonical_mappings = [
        {
            "record_type": "mapping",
            "raw_id": item["raw_id"],
            "direction_id": item["direction_id"],
            "cluster_id": item["cluster_id"],
            "disposition": item["disposition"],
            "reason": item["reason"],
            "creator_agent_id": creator_by_raw[item["raw_id"]],
        }
        for item in sorted(mappings, key=lambda value: value["raw_id"])
    ]
    direction_by_raw = {item["raw_id"]: item["direction_id"] for item in mappings}
    pending = json.loads(
        (run_dir / "baseline_discovery_evidence_pending.json").read_text(encoding="utf-8")
    )
    evidence_records = pending.get("evidence")
    if not isinstance(evidence_records, list) or len(evidence_records) != 10:
        raise RuntimeError("baseline discovery evidence pending set is not the expected ten records")
    for evidence in evidence_records:
        evidence["direction_id"] = direction_by_raw[evidence["entity_ids"][0]]
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    write_exclusive(ledger_path, jsonl_bytes(canonical_mappings + evidence_records))
    direction_by_id = {item["direction_id"]: item for item in directions}
    funnel_lines = [
        "# Baseline Reversible Economic Directions",
        "",
        "Sixteen unscored directions derived after raw freeze. Historical fingerprints are comparison evidence only.",
        "",
    ]
    for direction_id in sorted(direction_by_id):
        item = direction_by_id[direction_id]
        funnel_lines.extend(
            [
                f"## {direction_id} — {item['title']}",
                "",
                f"- Customer / loss: {item['customer_loss']}",
                f"- Payer / budget: {item['payer_budget']}",
                f"- Paid trigger: {item['paid_trigger']}",
                f"- Transaction owner: {item['transaction_owner']}",
                f"- Acquisition route: {item['acquisition_route']}",
                f"- Compounding asset: {item['compounding_asset']}",
                f"- Raw members: {', '.join(f'`{value}`' for value in item['raw_ids'])}",
                f"- Nearest history: {', '.join(f'`{value}`' for value in item['nearest_history_ids']) if item['nearest_history_ids'] else '`none`'}",
                f"- Historical comparison: {item['history_overlap_note']}",
                f"- Preserved disagreements: {'; '.join(item['disagreements']) if item['disagreements'] else 'none recorded'}",
                "",
            ]
        )
    funnel_path = run_dir / "02_candidate_funnel.md"
    write_exclusive(funnel_path, ("\n".join(funnel_lines).rstrip() + "\n").encode("utf-8"))
    search_map_path = run_dir / "01a_search_space_map.md"
    search_map = """# Baseline Search-Space Map

This is a soft coverage record, not an exhaustion claim.

- Evidence modalities: binding-rule changes, public operational audits, official market and technology reports, and official product or program documentation.
- Creative lenses: rule structure, taboo spaces, incentive redesign, first principles, and incumbent attack.
- Geographic emphasis: Poland and the European Union, with cross-border channels where evidenced.
- Economic fields preserved during cartography: payer, paid trigger, transaction owner, acquisition route, and possible compounding asset.
- Discovery usage: 20 unique tool calls against a registered opportunity of 108; unused opportunity remained unused.
"""
    write_exclusive(search_map_path, search_map.encode("utf-8"))
    write_exclusive(
        run_dir / "trace_attestations" / "baseline-cartography-01.json",
        json_bytes(attestation),
    )
    records.extend([agent, allocation])
    checkpoint_at = now()
    if checkpoint_at <= datetime.fromisoformat(agent["ended_at"]):
        raise RuntimeError("mapped checkpoint does not follow its cartography agent")
    run_record = records[0]
    totals = checkpoint_resource_totals(records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at)
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-04-mapped",
        "state": "mapped",
        "predecessor_id": "CP-baseline-w01-03-history_frozen",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in records if record.get("record_type") == "agent"),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": str(return_path.relative_to(run_dir)), "sha256": sha256(return_path)},
            {"path": funnel_path.name, "sha256": sha256(funnel_path)},
            {"path": search_map_path.name, "sha256": sha256(search_map_path)},
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "mapped"
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def prepare_baseline_cluster_audit(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    records = read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen", "mapped"]:
        raise RuntimeError("cluster-audit preparation requires the exact mapped prefix")
    cartography_path = run_dir / "agent_returns" / "baseline-cartography-01.json"
    directions, mappings = validate_baseline_cartography(
        json.loads(cartography_path.read_text(encoding="utf-8"))
    )
    packet_path = run_dir / "context" / "baseline-cluster-audit-01.md"
    output_path = run_dir / "agent_returns" / "baseline-cluster-audit-01.json"
    packet = f"""# Immutable Baseline Anti-Overmerge Packet

## Identity And Boundary

- Scope: `{ROOT_SCOPE_ID}`
- Arm: `matched_baseline`
- Stage: `cluster_audit`
- Agent ID: `baseline-cluster-audit-01`
- Role: `anti_overmerge_auditor`
- Model: `{MODEL}`
- Reasoning: `{REASONING}`
- Seed: `{seed}`
- Query cap: `0`
- Required return path: `{output_path}`

{bounded_return_instruction(output_path, run_dir)}

Read no other file. Do not browse. Do not rank merit, select, evaluate, validate, pivot, promote, regenerate, propose outreach, or execute a proof. Audit only semantic reversibility.

Challenge every direction with more than three raw members and every mapping currently marked `merged`. Differences in payer, paid trigger, transaction owner, or acquisition route normally remain siblings. You may preserve an overmerged member by changing its disposition to `unresolved`, assigning a more specific cluster ID, and revising its reason. Keep every raw ID and direction ID unchanged. Keep exactly one `retained` representative per direction. Return exact `status: "PASS"` only if all required challenges are covered, every raw remains mapped exactly once, and no mismatch is silently deleted.

Return one JSON object with exactly these keys:

```json
{{
  "status": "PASS",
  "audited_mappings": [
    {{
      "raw_id": "RAW-001",
      "direction_id": "DIR-001",
      "cluster_id": "CL-001",
      "disposition": "retained",
      "reason": "field-level rationale",
      "audit_note": "why the merge is upheld or the sibling is preserved"
    }}
  ],
  "challenged_directions": ["DIR-001"],
  "challenged_merges": ["RAW-002"],
  "effective_concept_count": 48,
  "unresolved_disagreements": ["RAW-NNN — field: concise mismatch"],
  "method_note": "short anti-overmerge method statement"
}}
```

`audited_mappings` must contain all 48 raw IDs exactly once and preserve every original direction ID. `challenged_directions` must contain exactly every supplied direction with more than three members. `challenged_merges` must contain exactly every supplied mapping marked `merged`, whether upheld or changed. Add no other fields.

## Frozen Cartography Return

```json
{json.dumps({'directions': directions, 'mappings': mappings}, indent=2, sort_keys=True)}
```
"""
    write_exclusive(packet_path, packet.encode("utf-8"))
    assert_bounded_return_packet(packet_path, output_path, run_dir)
    raw_ids = [f"RAW-{index:03d}" for index in range(1, 49)]
    precommit = {
        "schema": "zt1-allocation-precommit-v1",
        "scope_id": ROOT_SCOPE_ID,
        "arm": "matched_baseline",
        "stage": "cluster_audit",
        "agent_id": "baseline-cluster-audit-01",
        "role": "anti_overmerge_auditor",
        "seed": seed,
        "allocation_id": "ALLOC-B-ZERO-CLUSTER-01",
        "entity_ids": raw_ids,
        "assigned_ids": raw_ids,
        "output_ids": raw_ids,
        "query_cap": 0,
        "planned_used_queries": 0,
        "created_at": iso(now()),
        "metering_basis": "trace_derived_exact",
        "packet_path": str(packet_path.relative_to(run_dir)),
        "packet_sha256": sha256(packet_path),
        "output_path": str(output_path.relative_to(run_dir)),
        "model": MODEL,
        "reasoning_effort": REASONING,
    }
    precommit_path = run_dir / "allocation_precommits" / "ALLOC-B-ZERO-CLUSTER-01.json"
    write_exclusive(precommit_path, json_bytes(precommit))
    assert_bounded_return_precommit(
        packet_path,
        output_path,
        run_dir,
        precommit_path,
        expected_agent_id="baseline-cluster-audit-01",
        expected_stage="cluster_audit",
    )
    print(json.dumps({"packet_path": str(packet_path), "output_path": str(output_path), "task_name": trace_task_name(run_dir, "baseline-cluster-audit-01")}, indent=2))


def validate_baseline_cluster_audit(run_dir: Path, payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or set(payload) != {
        "status", "audited_mappings", "challenged_directions", "challenged_merges",
        "effective_concept_count", "unresolved_disagreements", "method_note",
    }:
        raise RuntimeError("cluster audit return has an invalid top-level schema")
    if payload.get("status") != "PASS":
        raise RuntimeError("cluster audit did not return exact PASS")
    original = json.loads(
        (run_dir / "agent_returns" / "baseline-cartography-01.json").read_text(encoding="utf-8")
    )
    directions, mappings = validate_baseline_cartography(original)
    original_by_raw = {item["raw_id"]: item for item in mappings}
    audited = payload.get("audited_mappings")
    fields = {"raw_id", "direction_id", "cluster_id", "disposition", "reason", "audit_note"}
    expected_raw = [f"RAW-{index:03d}" for index in range(1, 49)]
    if not isinstance(audited, list) or len(audited) != 48:
        raise RuntimeError("cluster audit must return 48 audited mappings")
    if sorted(item.get("raw_id") for item in audited if isinstance(item, dict)) != expected_raw:
        raise RuntimeError("cluster audit raw IDs are incomplete or duplicated")
    retained_counts: dict[str, int] = {item["direction_id"]: 0 for item in directions}
    for item in audited:
        if not isinstance(item, dict) or set(item) != fields:
            raise RuntimeError("audited mapping uses an invalid schema")
        original_item = original_by_raw[item["raw_id"]]
        if item["direction_id"] != original_item["direction_id"]:
            raise RuntimeError(f"cluster audit changed a frozen direction ID: {item['raw_id']}")
        if item["disposition"] not in {"retained", "merged", "unresolved", "rejected"}:
            raise RuntimeError(f"cluster audit uses invalid disposition: {item['raw_id']}")
        for field in ("cluster_id", "reason", "audit_note"):
            if not isinstance(item[field], str) or not item[field].strip():
                raise RuntimeError(f"cluster audit mapping lacks {field}: {item['raw_id']}")
        retained_counts[item["direction_id"]] += int(item["disposition"] == "retained")
    if any(value != 1 for value in retained_counts.values()):
        raise RuntimeError("cluster audit did not preserve exactly one retained representative per direction")
    expected_challenged_directions = sorted(
        item["direction_id"] for item in directions if len(item["raw_ids"]) > 3
    )
    if payload.get("challenged_directions") != expected_challenged_directions:
        raise RuntimeError("cluster audit did not challenge the exact required large directions")
    expected_challenged_merges = sorted(
        item["raw_id"] for item in mappings if item["disposition"] == "merged"
    )
    if payload.get("challenged_merges") != expected_challenged_merges:
        raise RuntimeError("cluster audit did not challenge every proposed merge")
    effective_count = payload.get("effective_concept_count")
    if not isinstance(effective_count, int) or isinstance(effective_count, bool) or not 16 <= effective_count <= 48:
        raise RuntimeError("cluster audit effective concept count is invalid")
    disagreements = payload.get("unresolved_disagreements")
    if not isinstance(disagreements, list) or any(not isinstance(value, str) for value in disagreements):
        raise RuntimeError("cluster audit unresolved disagreements are invalid")
    if not isinstance(payload.get("method_note"), str) or not payload["method_note"].strip():
        raise RuntimeError("cluster audit method note is missing")
    return audited


def integrate_baseline_cluster_audit(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen", "mapped"]:
        raise RuntimeError("cluster-audit integration requires the exact mapped prefix")
    agent, allocation, attestation = integrate_zero_query_agent(
        run_dir=run_dir,
        task_name=trace_task_name(run_dir, "baseline-cluster-audit-01"),
        agent_id="baseline-cluster-audit-01",
        role="anti_overmerge_auditor",
        stage="cluster_audit",
        packet_rel="context/baseline-cluster-audit-01.md",
        output_rel="agent_returns/baseline-cluster-audit-01.json",
        precommit_rel="allocation_precommits/ALLOC-B-ZERO-CLUSTER-01.json",
        context_classes=["founder_constraints", "safety_legal", "neutral_evidence"],
    )
    return_path = run_dir / "agent_returns" / "baseline-cluster-audit-01.json"
    payload = json.loads(return_path.read_text(encoding="utf-8"))
    audited = validate_baseline_cluster_audit(run_dir, payload)
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    ledger = read_jsonl(ledger_path)
    creator_by_raw = {
        record["raw_id"]: record["creator_agent_id"]
        for record in ledger if record.get("record_type") == "mapping"
    }
    evidence = [record for record in ledger if record.get("record_type") == "evidence"]
    canonical_mappings = [
        {
            "record_type": "mapping",
            "raw_id": item["raw_id"],
            "direction_id": item["direction_id"],
            "cluster_id": item["cluster_id"],
            "disposition": item["disposition"],
            "reason": f"{item['reason']} Anti-overmerge audit: {item['audit_note']}",
            "creator_agent_id": creator_by_raw[item["raw_id"]],
        }
        for item in sorted(audited, key=lambda value: value["raw_id"])
    ]
    write_replace(ledger_path, jsonl_bytes(canonical_mappings + evidence))
    audit_path = run_dir / "02e_cluster_audit.md"
    audit_lines = [
        "# Baseline Anti-Overmerge Audit",
        "",
        "Status: `PASS`",
        "",
        f"- Effective concept count: {payload['effective_concept_count']}",
        f"- Large directions challenged: {', '.join(payload['challenged_directions']) if payload['challenged_directions'] else 'none'}",
        f"- Proposed merges challenged: {', '.join(payload['challenged_merges']) if payload['challenged_merges'] else 'none'}",
        f"- Method: {payload['method_note']}",
        "",
        "## Unresolved Disagreements",
        "",
        *(f"- {value}" for value in payload["unresolved_disagreements"]),
    ]
    if not payload["unresolved_disagreements"]:
        audit_lines.append("- None recorded.")
    write_exclusive(audit_path, ("\n".join(audit_lines).rstrip() + "\n").encode("utf-8"))
    write_exclusive(
        run_dir / "trace_attestations" / "baseline-cluster-audit-01.json",
        json_bytes(attestation),
    )
    records.extend([agent, allocation])
    checkpoint_at = now()
    if checkpoint_at <= datetime.fromisoformat(agent["ended_at"]):
        raise RuntimeError("cluster-audited checkpoint does not follow its agent")
    run_record = records[0]
    totals = checkpoint_resource_totals(records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at)
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-05-cluster_audited",
        "state": "cluster_audited",
        "predecessor_id": "CP-baseline-w01-04-mapped",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in records if record.get("record_type") == "agent"),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": str(return_path.relative_to(run_dir)), "sha256": sha256(return_path)},
            {"path": audit_path.name, "sha256": sha256(audit_path)},
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "cluster_audited"
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def prepare_baseline_level1(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    records = read_jsonl(run_dir / "00a_context_and_resource_manifest.jsonl")
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen", "mapped", "cluster_audited"]:
        raise RuntimeError("Level-1 preparation requires the exact cluster_audited prefix")
    cartography = json.loads(
        (run_dir / "agent_returns" / "baseline-cartography-01.json").read_text(encoding="utf-8")
    )
    directions, _ = validate_baseline_cartography(cartography)
    cluster_payload = json.loads(
        (run_dir / "agent_returns" / "baseline-cluster-audit-01.json").read_text(encoding="utf-8")
    )
    audited = validate_baseline_cluster_audit(run_dir, cluster_payload)
    raw_text = "\n\n".join(section for _, section in baseline_raw_sections(run_dir))
    research_text = (run_dir / "03_research_and_sources.md").read_text(encoding="utf-8")
    packet_path = run_dir / "context" / "baseline-level1-01.md"
    output_path = run_dir / "agent_returns" / "baseline-level1-01.json"
    packet = f"""# Immutable Baseline Equal-Field Level-1 Packet

## Identity And Boundary

- Scope: `{ROOT_SCOPE_ID}`
- Arm: `matched_baseline`
- Stage: `level1`
- Agent ID: `baseline-level1-01`
- Role: `canonicalizer`
- Model: `{MODEL}`
- Reasoning: `{REASONING}`
- Seed: `{seed}`
- Query cap: `0`
- Required return path: `{output_path}`

{bounded_return_instruction(output_path, run_dir)}

Read no other file. Do not browse. Do not rank, select, evaluate, validate, pivot, promote, regenerate, propose outreach, or execute a proof. Normalize each of the 16 audited directions to equal fields and roughly equal detail. Preserve contradictory evidence and unknowns. Sources establish only what they directly support.

Neutral founder constraints: Warsaw data scientist employed full time; at most five focused hours daily; about 100,000 PLN personally available and another 100,000 PLN only for an unusually clear case. Strong AI/data/neuroscience/finance fluency, a medical-student partner, and a family renewable-installation firm near Ostrow Wielkopolski. Avoid camera-led distribution and constant high-energy networking. Prefer part-time proof, controlled downside, repeatable demand, scalable assets, and a plausible path to 5 million PLN of founder net worth without double counting.

Safety/legal boundary: retain only lawful structures. Indispensable deception, coercion, exploitation, privacy abuse, evasion, or serious harm is out of scope. Unsupported public facts remain explicit unknowns.

Return one JSON object with exactly `cards` and `method_note`. `cards` contains exactly one object for every `DIR-001` through `DIR-016`, using exactly these fields:

```json
{{
  "concept_id": "DIR-001",
  "problem_payer_evidence": "...",
  "proposed_transaction_paid_event": "...",
  "current_workaround_and_persistence": "...",
  "initial_acquisition_route": "...",
  "possible_compounding_mechanism": "...",
  "decisive_assumptions_and_contradictions": ["..."],
  "cheapest_falsification": "...",
  "founder_constraint_tension": "...",
  "sources": ["EV-B-DISC-NNN — URL"],
  "explicit_unknowns": ["..."]
}}
```

All narrative string fields must be nonempty; all list fields must be nonempty string lists. Do not include author, creative role, prior status, numeric ratings, or a selection outcome. Add no other fields.

## Audited Directions

```json
{json.dumps(directions, indent=2, sort_keys=True)}
```

## Audited Reversible Mappings

```json
{json.dumps(audited, indent=2, sort_keys=True)}
```

## Author-Stripped Raw Cards

{raw_text}

## Discovery Evidence

{research_text}
"""
    write_exclusive(packet_path, packet.encode("utf-8"))
    assert_bounded_return_packet(packet_path, output_path, run_dir)
    direction_ids = [f"DIR-{index:03d}" for index in range(1, 17)]
    precommit = {
        "schema": "zt1-allocation-precommit-v1",
        "scope_id": ROOT_SCOPE_ID,
        "arm": "matched_baseline",
        "stage": "level1",
        "agent_id": "baseline-level1-01",
        "role": "canonicalizer",
        "seed": seed,
        "allocation_id": "ALLOC-B-ZERO-LEVEL1-01",
        "entity_ids": direction_ids,
        "assigned_ids": direction_ids,
        "output_ids": direction_ids,
        "query_cap": 0,
        "planned_used_queries": 0,
        "created_at": iso(now()),
        "metering_basis": "trace_derived_exact",
        "packet_path": str(packet_path.relative_to(run_dir)),
        "packet_sha256": sha256(packet_path),
        "output_path": str(output_path.relative_to(run_dir)),
        "model": MODEL,
        "reasoning_effort": REASONING,
    }
    precommit_path = run_dir / "allocation_precommits" / "ALLOC-B-ZERO-LEVEL1-01.json"
    write_exclusive(precommit_path, json_bytes(precommit))
    assert_bounded_return_precommit(
        packet_path,
        output_path,
        run_dir,
        precommit_path,
        expected_agent_id="baseline-level1-01",
        expected_stage="level1",
    )
    print(json.dumps({"packet_path": str(packet_path), "output_path": str(output_path), "task_name": trace_task_name(run_dir, "baseline-level1-01")}, indent=2))


def validate_baseline_level1(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or set(payload) != {"cards", "method_note"}:
        raise RuntimeError("Level-1 return has an invalid top-level schema")
    cards = payload.get("cards")
    fields = {
        "concept_id", "problem_payer_evidence", "proposed_transaction_paid_event",
        "current_workaround_and_persistence", "initial_acquisition_route",
        "possible_compounding_mechanism", "decisive_assumptions_and_contradictions",
        "cheapest_falsification", "founder_constraint_tension", "sources", "explicit_unknowns",
    }
    expected = [f"DIR-{index:03d}" for index in range(1, 17)]
    if not isinstance(cards, list) or len(cards) != 16:
        raise RuntimeError("Level-1 return must contain exactly 16 cards")
    if sorted(item.get("concept_id") for item in cards if isinstance(item, dict)) != expected:
        raise RuntimeError("Level-1 card IDs are incomplete or duplicated")
    list_fields = {"decisive_assumptions_and_contradictions", "sources", "explicit_unknowns"}
    for item in cards:
        if not isinstance(item, dict) or set(item) != fields:
            raise RuntimeError("Level-1 card uses an invalid schema")
        for field in fields - list_fields - {"concept_id"}:
            if not isinstance(item[field], str) or not item[field].strip():
                raise RuntimeError(f"Level-1 card {item['concept_id']} lacks {field}")
        for field in list_fields:
            value = item[field]
            if not isinstance(value, list) or not value or any(not isinstance(entry, str) or not entry.strip() for entry in value):
                raise RuntimeError(f"Level-1 card {item['concept_id']} has invalid {field}")
    if not isinstance(payload.get("method_note"), str) or not payload["method_note"].strip():
        raise RuntimeError("Level-1 method note is missing")
    return cards


def seeded_ids(seed: str, namespace: str, ids: list[str]) -> list[str]:
    return seeded_order(seed, namespace, ids)


def integrate_baseline_level1_and_seal(run_dir: Path, selected_ids: list[str]) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != ["registered", "raw_frozen", "history_frozen", "mapped", "cluster_audited"]:
        raise RuntimeError("Level-1 integration requires the exact cluster_audited prefix")
    expected = [f"DIR-{index:03d}" for index in range(1, 17)]
    if len(selected_ids) != 12 or len(set(selected_ids)) != 12 or not set(selected_ids).issubset(expected):
        raise RuntimeError("root selection must contain exactly 12 unique registered direction IDs")
    agent, allocation, attestation = integrate_zero_query_agent(
        run_dir=run_dir,
        task_name=trace_task_name(run_dir, "baseline-level1-01"),
        agent_id="baseline-level1-01",
        role="canonicalizer",
        stage="level1",
        packet_rel="context/baseline-level1-01.md",
        output_rel="agent_returns/baseline-level1-01.json",
        precommit_rel="allocation_precommits/ALLOC-B-ZERO-LEVEL1-01.json",
        context_classes=["founder_constraints", "safety_legal", "neutral_evidence"],
    )
    return_path = run_dir / "agent_returns" / "baseline-level1-01.json"
    payload = json.loads(return_path.read_text(encoding="utf-8"))
    cards = validate_baseline_level1(payload)
    cards_by_id = {item["concept_id"]: item for item in cards}
    level1_path = run_dir / "02_level1_cards.md"
    lines = ["# Baseline Equal-Field Level-1 Cards", "", "Unscored and normalized before root selection.", ""]
    for concept_id in expected:
        item = cards_by_id[concept_id]
        lines.extend(
            [
                f"## {concept_id}", "",
                f"- Problem and payer evidence: {item['problem_payer_evidence']}",
                f"- Proposed transaction and paid event: {item['proposed_transaction_paid_event']}",
                f"- Current workaround and persistence: {item['current_workaround_and_persistence']}",
                f"- Initial acquisition route: {item['initial_acquisition_route']}",
                f"- Possible compounding mechanism: {item['possible_compounding_mechanism']}",
                f"- Decisive assumptions and contradictions: {'; '.join(item['decisive_assumptions_and_contradictions'])}",
                f"- Cheapest falsification: {item['cheapest_falsification']}",
                f"- Founder-constraint tension: {item['founder_constraint_tension']}",
                f"- Sources: {'; '.join(item['sources'])}",
                f"- Explicit unknowns: {'; '.join(item['explicit_unknowns'])}",
                "",
            ]
        )
    write_exclusive(level1_path, ("\n".join(lines).rstrip() + "\n").encode("utf-8"))
    selected_at = now()
    ordered_reserve = seeded_ids(
        seed,
        "baseline-level2-reserve", [concept_id for concept_id in expected if concept_id not in selected_ids]
    )
    selection_payload = {
        "candidate_ids": selected_ids,
        "creator_agent_id": "root-orchestrator",
        "selected_at": iso(selected_at),
        "seed": seed,
        "ordered_reserve": ordered_reserve,
        "decision_rule": "lawful and not directly falsified; then evidence-supported payer event, founder-accessible first contract, compounding control, fingerprint diversity, and seeded tie-break without numeric ratings",
    }
    selection_path = run_dir / "02c_baseline_level2_cohort.json"
    write_exclusive(selection_path, json_bytes(selection_payload))
    write_exclusive(
        run_dir / "trace_attestations" / "baseline-level1-01.json",
        json_bytes(attestation),
    )
    records.extend([agent, allocation])
    checkpoint_at = now()
    if not datetime.fromisoformat(agent["ended_at"]) < selected_at < checkpoint_at:
        raise RuntimeError("Level-2 cohort selection chronology is invalid")
    run_record = records[0]
    totals = checkpoint_resource_totals(records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at)
    checkpoint = {
        "record_type": "checkpoint",
        "checkpoint_id": "CP-baseline-w01-06-level2_cohort_sealed",
        "state": "level2_cohort_sealed",
        "predecessor_id": "CP-baseline-w01-05-cluster_audited",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in records if record.get("record_type") == "agent"),
        "file_read_log_complete": True,
        "tool_event_log_complete": True,
        "resource_totals": totals,
        "artifacts": [
            {"path": str(return_path.relative_to(run_dir)), "sha256": sha256(return_path)},
            {"path": level1_path.name, "sha256": sha256(level1_path)},
            {"path": selection_path.name, "sha256": sha256(selection_path)},
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "level2_cohort_sealed"
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def prepare_baseline_level2(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import prepare_baseline_level2 as prepare_isolated

    prepare_isolated(sys.modules[__name__], run_dir)


def render_dossier(concept_id: str, dossier: dict[str, str], prefix: str) -> str:
    from v2_candidate_development import _render_dossier

    return _render_dossier(sys.modules[__name__], concept_id, dossier, prefix)


def integrate_baseline_level2(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import integrate_baseline_level2 as integrate_isolated

    integrate_isolated(sys.modules[__name__], run_dir)

def seal_baseline_fact_closure(run_dir: Path, selected_ids: list[str]) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    states = [record.get("state") for record in records if record.get("record_type") == "checkpoint"]
    if states != [
        "registered", "raw_frozen", "history_frozen", "mapped", "cluster_audited",
        "level2_cohort_sealed", "level2_complete",
    ]:
        raise RuntimeError("fact-closure sealing requires the exact level2_complete prefix")
    ledger = read_jsonl(run_dir / "02b_raw_to_direction_ledger.jsonl")
    completed_ids = {
        record["concept_id"] for record in ledger
        if record.get("record_type") == "level2" and record.get("development_status") == "complete"
    }
    if len(selected_ids) != 6 or len(set(selected_ids)) != 6 or not set(selected_ids).issubset(completed_ids):
        raise RuntimeError("fact-closure cohort must contain exactly six completed Level-2 IDs")
    selected_at = now()
    payload = {
        "candidate_ids": selected_ids,
        "creator_agent_id": "root-orchestrator",
        "selected_at": iso(selected_at),
        "seed": seed,
    }
    closure_path = run_dir / "02d_fact_closure_candidates.json"
    write_exclusive(closure_path, json_bytes(payload))
    checkpoint_at = now()
    if checkpoint_at <= selected_at:
        raise RuntimeError("fact-closure cohort checkpoint chronology is invalid")
    run_record = records[0]
    run_record["fact_closure_selected_at"] = payload["selected_at"]
    run_record["fact_closure_candidates_file"] = closure_path.name
    run_record["fact_closure_candidates_sha256"] = sha256(closure_path)
    totals = checkpoint_resource_totals(records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at)
    checkpoint = {
        "record_type": "checkpoint", "checkpoint_id": "CP-baseline-w01-08-fact_closure_cohort_sealed",
        "state": "fact_closure_cohort_sealed", "predecessor_id": "CP-baseline-w01-07-level2_complete",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in records if record.get("record_type") == "agent"),
        "file_read_log_complete": True, "tool_event_log_complete": True, "resource_totals": totals,
        "artifacts": [{"path": closure_path.name, "sha256": sha256(closure_path)}],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "fact_closure_cohort_sealed"
    run_record["resource_totals"] = dict(totals)
    write_replace(manifest_path, jsonl_bytes(records))
    print(json.dumps(checkpoint, indent=2, sort_keys=True))


def prepare_baseline_fact_closure(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import prepare_baseline_fact_closure as prepare_isolated

    prepare_isolated(sys.modules[__name__], run_dir)


def integrate_baseline_fact_closure(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import integrate_baseline_fact_closure as integrate_isolated

    integrate_isolated(sys.modules[__name__], run_dir)


def prepare_shadow_level2(
    run_dir: Path, cohort_file: Path, inputs_file: Path
) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import prepare_shadow_level2 as prepare_isolated

    prepare_isolated(
        sys.modules[__name__],
        run_dir,
        cohort_file=cohort_file,
        inputs_file=inputs_file,
    )


def integrate_shadow_level2(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import integrate_shadow_level2 as integrate_isolated

    integrate_isolated(sys.modules[__name__], run_dir)


def prepare_shadow_fact_closure(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import (
        prepare_shadow_fact_closure as prepare_isolated,
    )

    prepare_isolated(sys.modules[__name__], run_dir)


def integrate_shadow_fact_closure(run_dir: Path) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import (
        integrate_shadow_fact_closure as integrate_isolated,
    )

    integrate_isolated(sys.modules[__name__], run_dir)


def meter_development_batch(run_dir: Path, stage: str, batch_index: int) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import meter_batch_snapshot

    snapshot = meter_batch_snapshot(
        sys.modules[__name__],
        run_dir,
        stage=stage,
        batch_index=batch_index,
    )
    print(json.dumps(snapshot, indent=2, sort_keys=True))


def monitor_development_batch(run_dir: Path, stage: str, batch_index: int) -> None:
    authenticated_run_seed(run_dir)
    from v2_candidate_development import monitor_batch

    result = monitor_batch(
        sys.modules[__name__],
        run_dir,
        stage=stage,
        batch_index=batch_index,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


def freeze_baseline(run_dir: Path) -> None:
    seed = authenticated_run_seed(run_dir)
    run_dir = run_dir.resolve()
    manifest_path = run_dir / "00a_context_and_resource_manifest.jsonl"
    records = read_jsonl(manifest_path)
    if [record.get("state") for record in records if record.get("record_type") == "checkpoint"][-1:] != ["closure_complete"]:
        raise RuntimeError("baseline freeze requires the closure_complete prefix")
    closure = json.loads((run_dir / "02d_fact_closure_candidates.json").read_text(encoding="utf-8"))
    if closure.get("seed") != seed:
        raise RuntimeError("sealed fact-closure cohort seed differs from registration")
    selected_ids = closure["candidate_ids"]
    closure_by_id: dict[str, dict[str, Any]] = {}
    for index in range(1, 7):
        output_path = run_dir / "agent_returns" / f"baseline-fact-closure-{index:02d}.json"
        output = json.loads(output_path.read_text(encoding="utf-8"))
        concept_id = output.get("concept_id")
        if not isinstance(concept_id, str) or concept_id in closure_by_id:
            raise RuntimeError("isolated fact-closure returns have invalid candidate ownership")
        closure_by_id[concept_id] = output
    if set(closure_by_id) != set(selected_ids):
        raise RuntimeError("isolated fact-closure returns do not match the sealed cohort")
    contradicted = [
        concept_id
        for concept_id in selected_ids
        if any(
            item.get("status") == "contradicted"
            for item in closure_by_id[concept_id].get("research", [])
        )
    ]
    if contradicted:
        raise RuntimeError(f"cannot freeze directly contradicted indispensable candidates without substitution: {contradicted}")
    ledger_path = run_dir / "02b_raw_to_direction_ledger.jsonl"
    ledger = read_jsonl(ledger_path)
    mappings = [record for record in ledger if record.get("record_type") == "mapping"]
    finalist_records = []
    finalist_artifacts = []
    finalist_payloads: list[tuple[str, Path, bytes]] = []
    for index, concept_id in enumerate(selected_ids, 1):
        source_path = run_dir / "baseline_fact_closure" / f"closure_{concept_id.casefold()}.md"
        finalist_path = run_dir / f"baseline_shadow_finalist_{concept_id.casefold().replace('-', '_')}.md"
        if (
            not source_path.is_file()
            or source_path.is_symlink()
            or finalist_path.exists()
            or finalist_path.is_symlink()
        ):
            raise RuntimeError(f"finalist source/target is missing or unsafe: {concept_id}")
        finalist_payloads.append((concept_id, finalist_path, source_path.read_bytes()))
    frozen_at = now()
    for index, (concept_id, finalist_path, finalist_bytes) in enumerate(finalist_payloads, 1):
        eligible_raw = sorted(
            record["raw_id"] for record in mappings
            if record.get("direction_id") == concept_id and record.get("disposition") in {"retained", "merged"}
        )
        if not eligible_raw:
            raise RuntimeError(f"finalist direction lacks retained or merged raw ancestry: {concept_id}")
        evidence_ids = [
            record["evidence_id"]
            for record in ledger
            if record.get("record_type") == "evidence"
            and record.get("stage") == "fact_closure"
            and record.get("concept_id") == concept_id
        ]
        if not evidence_ids:
            raise RuntimeError(f"finalist lacks candidate-owned closure evidence: {concept_id}")
        finalist_rel = str(finalist_path.relative_to(run_dir))
        finalist_digest = sha256_bytes(finalist_bytes)
        finalist_records.append(
            {
                "record_type": "finalist", "finalist_id": f"FIN-{index:02d}",
                "direction_id": concept_id, "raw_ids": eligible_raw, "evidence_ids": evidence_ids,
                "frozen_at": iso(frozen_at), "arm": "matched_baseline", "shadow_only": True,
                "validation_eligible": False, "artifact_path": finalist_rel, "sha256": finalist_digest,
            }
        )
        finalist_artifacts.append({"path": finalist_rel, "sha256": finalist_digest})
    # All ancestry, evidence, contradiction, source, and target checks finish
    # before the first canonical finalist byte is materialized.
    for _concept_id, finalist_path, finalist_bytes in finalist_payloads:
        write_exclusive(finalist_path, finalist_bytes)
    write_replace(ledger_path, jsonl_bytes(ledger + finalist_records))
    checkpoint_at = now()
    if checkpoint_at <= frozen_at:
        raise RuntimeError("frozen checkpoint does not follow finalist freeze")
    run_record = records[0]
    run_record["live_finalists_frozen_at"] = iso(frozen_at)
    totals = checkpoint_resource_totals(records, datetime.fromisoformat(run_record["started_at"]), checkpoint_at)
    checkpoint = {
        "record_type": "checkpoint", "checkpoint_id": "CP-baseline-w01-10-frozen",
        "state": "frozen", "predecessor_id": "CP-baseline-w01-09-closure_complete",
        "occurred_at": iso(checkpoint_at),
        "completed_agent_ids": sorted(record["agent_id"] for record in records if record.get("record_type") == "agent"),
        "file_read_log_complete": True, "tool_event_log_complete": True, "resource_totals": totals,
        "artifacts": [
            {"path": ledger_path.name, "sha256": sha256(ledger_path)}, *finalist_artifacts,
        ],
    }
    records.append(checkpoint)
    run_record["lifecycle_state"] = "frozen"
    run_record["resource_totals"] = dict(totals)
    manifest_bytes = jsonl_bytes(records)
    write_replace(manifest_path, manifest_bytes)
    snapshot_path = run_dir / "00c_pre_freeze_manifest_snapshot.jsonl"
    write_exclusive(snapshot_path, manifest_bytes)
    print(json.dumps({"checkpoint": checkpoint, "snapshot_sha256": sha256(snapshot_path)}, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("--stamp", required=True)
    register_parser.add_argument("--seed", required=True)
    checkpoint_parser = subparsers.add_parser("record-registered")
    checkpoint_parser.add_argument("run_dir", type=Path)
    generation_parser = subparsers.add_parser("prepare-baseline-generation")
    generation_parser.add_argument("run_dir", type=Path)
    integrate_generation_parser = subparsers.add_parser("integrate-baseline-generation")
    integrate_generation_parser.add_argument("run_dir", type=Path)
    history_parser = subparsers.add_parser("prepare-baseline-history")
    history_parser.add_argument("run_dir", type=Path)
    integrate_history_parser = subparsers.add_parser("integrate-baseline-history")
    integrate_history_parser.add_argument("run_dir", type=Path)
    cartography_parser = subparsers.add_parser("prepare-baseline-cartography")
    cartography_parser.add_argument("run_dir", type=Path)
    integrate_cartography_parser = subparsers.add_parser("integrate-baseline-cartography")
    integrate_cartography_parser.add_argument("run_dir", type=Path)
    cluster_parser = subparsers.add_parser("prepare-baseline-cluster-audit")
    cluster_parser.add_argument("run_dir", type=Path)
    integrate_cluster_parser = subparsers.add_parser("integrate-baseline-cluster-audit")
    integrate_cluster_parser.add_argument("run_dir", type=Path)
    level1_parser = subparsers.add_parser("prepare-baseline-level1")
    level1_parser.add_argument("run_dir", type=Path)
    integrate_level1_parser = subparsers.add_parser("integrate-baseline-level1-and-seal")
    integrate_level1_parser.add_argument("run_dir", type=Path)
    integrate_level1_parser.add_argument("--selected", nargs=12, required=True)
    level2_parser = subparsers.add_parser("prepare-baseline-level2")
    level2_parser.add_argument("run_dir", type=Path)
    integrate_level2_parser = subparsers.add_parser("integrate-baseline-level2")
    integrate_level2_parser.add_argument("run_dir", type=Path)
    seal_closure_parser = subparsers.add_parser("seal-baseline-fact-closure")
    seal_closure_parser.add_argument("run_dir", type=Path)
    seal_closure_parser.add_argument("--selected", nargs=6, required=True)
    fact_closure_parser = subparsers.add_parser("prepare-baseline-fact-closure")
    fact_closure_parser.add_argument("run_dir", type=Path)
    integrate_fact_closure_parser = subparsers.add_parser("integrate-baseline-fact-closure")
    integrate_fact_closure_parser.add_argument("run_dir", type=Path)
    shadow_level2_parser = subparsers.add_parser("prepare-shadow-level2")
    shadow_level2_parser.add_argument("run_dir", type=Path)
    shadow_level2_parser.add_argument("--cohort-file", type=Path, required=True)
    shadow_level2_parser.add_argument("--inputs-file", type=Path, required=True)
    integrate_shadow_level2_parser = subparsers.add_parser("integrate-shadow-level2")
    integrate_shadow_level2_parser.add_argument("run_dir", type=Path)
    shadow_closure_parser = subparsers.add_parser("prepare-shadow-fact-closure")
    shadow_closure_parser.add_argument("run_dir", type=Path)
    integrate_shadow_closure_parser = subparsers.add_parser("integrate-shadow-fact-closure")
    integrate_shadow_closure_parser.add_argument("run_dir", type=Path)
    meter_parser = subparsers.add_parser("meter-development-batch")
    meter_parser.add_argument("run_dir", type=Path)
    meter_parser.add_argument(
        "--stage", choices=("level2", "fact_closure"), required=True
    )
    meter_parser.add_argument("--batch-index", type=int, required=True)
    monitor_parser = subparsers.add_parser("monitor-development-batch")
    monitor_parser.add_argument("run_dir", type=Path)
    monitor_parser.add_argument(
        "--stage", choices=("level2", "fact_closure"), required=True
    )
    monitor_parser.add_argument("--batch-index", type=int, required=True)
    freeze_baseline_parser = subparsers.add_parser("freeze-baseline")
    freeze_baseline_parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    if args.command == "register":
        register(args.stamp, args.seed)
    elif args.command == "record-registered":
        run_authenticated_command(args.run_dir, record_registered, args.run_dir)
    elif args.command == "prepare-baseline-generation":
        run_authenticated_command(
            args.run_dir, prepare_baseline_generation, args.run_dir
        )
    elif args.command == "integrate-baseline-generation":
        run_authenticated_command(
            args.run_dir, integrate_baseline_generation, args.run_dir
        )
    elif args.command == "prepare-baseline-history":
        run_authenticated_command(args.run_dir, prepare_baseline_history, args.run_dir)
    elif args.command == "integrate-baseline-history":
        run_authenticated_command(args.run_dir, integrate_baseline_history, args.run_dir)
    elif args.command == "prepare-baseline-cartography":
        run_authenticated_command(
            args.run_dir, prepare_baseline_cartography, args.run_dir
        )
    elif args.command == "integrate-baseline-cartography":
        run_authenticated_command(
            args.run_dir, integrate_baseline_cartography, args.run_dir
        )
    elif args.command == "prepare-baseline-cluster-audit":
        run_authenticated_command(
            args.run_dir, prepare_baseline_cluster_audit, args.run_dir
        )
    elif args.command == "integrate-baseline-cluster-audit":
        run_authenticated_command(
            args.run_dir, integrate_baseline_cluster_audit, args.run_dir
        )
    elif args.command == "prepare-baseline-level1":
        run_authenticated_command(args.run_dir, prepare_baseline_level1, args.run_dir)
    elif args.command == "integrate-baseline-level1-and-seal":
        run_authenticated_command(
            args.run_dir,
            integrate_baseline_level1_and_seal,
            args.run_dir,
            args.selected,
        )
    elif args.command == "prepare-baseline-level2":
        run_authenticated_command(args.run_dir, prepare_baseline_level2, args.run_dir)
    elif args.command == "integrate-baseline-level2":
        run_authenticated_command(args.run_dir, integrate_baseline_level2, args.run_dir)
    elif args.command == "seal-baseline-fact-closure":
        run_authenticated_command(
            args.run_dir,
            seal_baseline_fact_closure,
            args.run_dir,
            args.selected,
        )
    elif args.command == "prepare-baseline-fact-closure":
        run_authenticated_command(
            args.run_dir, prepare_baseline_fact_closure, args.run_dir
        )
    elif args.command == "integrate-baseline-fact-closure":
        run_authenticated_command(
            args.run_dir, integrate_baseline_fact_closure, args.run_dir
        )
    elif args.command == "prepare-shadow-level2":
        run_authenticated_command(
            args.run_dir,
            prepare_shadow_level2,
            args.run_dir,
            args.cohort_file,
            args.inputs_file,
        )
    elif args.command == "integrate-shadow-level2":
        run_authenticated_command(args.run_dir, integrate_shadow_level2, args.run_dir)
    elif args.command == "prepare-shadow-fact-closure":
        run_authenticated_command(
            args.run_dir, prepare_shadow_fact_closure, args.run_dir
        )
    elif args.command == "integrate-shadow-fact-closure":
        run_authenticated_command(
            args.run_dir, integrate_shadow_fact_closure, args.run_dir
        )
    elif args.command == "meter-development-batch":
        run_authenticated_command(
            args.run_dir,
            meter_development_batch,
            args.run_dir,
            args.stage,
            args.batch_index,
        )
    elif args.command == "monitor-development-batch":
        run_authenticated_command(
            args.run_dir,
            monitor_development_batch,
            args.run_dir,
            args.stage,
            args.batch_index,
        )
    elif args.command == "freeze-baseline":
        run_authenticated_command(args.run_dir, freeze_baseline, args.run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
