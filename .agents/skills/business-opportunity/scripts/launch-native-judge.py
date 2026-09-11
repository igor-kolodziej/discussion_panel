#!/usr/bin/env python3
"""Launch one packet-only judge inside a fresh macOS filesystem sandbox.

The supervisor supplies the immutable CLI assignment and owns all canonical writes.
This helper does not select candidates, alter responses, or retry judgments.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def sandbox_profile(workspace: Path, repo: Path, codex_home: Path) -> str:
    """Deny excluded contents and all writes outside this judge's workspace."""
    home = Path.home()
    protected = {repo.resolve(), home / ".agents", home / ".claude"}
    listing = subprocess.run(
        ["git", "-C", str(repo), "worktree", "list", "--porcelain"],
        capture_output=True, text=True, check=True,
    )
    protected.update(
        Path(line.removeprefix("worktree ")).resolve()
        for line in listing.stdout.splitlines() if line.startswith("worktree ")
    )
    for parent in {*workspace.parents, home, *home.parents}:
        protected.update(parent / name for name in ("AGENTS.md", "AGENTS.override.md"))
    lines = ["(version 1)", "(allow default)"]
    for path in sorted(protected):
        for spelling in {str(path), str(path.resolve())}:
            lines.append(f"(deny file-read-data (subpath {json.dumps(spelling)}))")
    # Directory metadata must remain available for realpath/auth resolution.
    # Reading directory listings or file contents remains denied. The CLI uses
    # only the existing auth file; its config, skills, sessions and memory are hidden.
    lines.append(
        '(deny file-read-data (require-all '
        f'(subpath {json.dumps(str(codex_home))}) '
        f'(require-not (literal {json.dumps(str(codex_home / "auth.json"))}))))'
    )
    temporary_roots = {workspace.parent, Path("/tmp"), Path("/private/tmp")}
    for root in temporary_roots:
        for spelling in {str(root), str(root).replace("/private/var/", "/var/")}:
            lines.append(
                '(deny file-read-data (require-all '
                f'(subpath {json.dumps(spelling)}) '
                f'(require-not (subpath {json.dumps(str(workspace))}))))'
            )
    lines.append(
        '(deny file-write* (require-all '
        f'(require-not (subpath {json.dumps(str(workspace))})) '
        '(require-not (literal "/dev/null"))))'
    )
    return "\n".join(lines) + "\n"


def launch(assignment_path: Path, repo: Path) -> dict:
    if sys.platform != "darwin":
        raise ValueError("this launcher requires macOS sandbox-exec; use a separately verified host boundary")
    raw = assignment_path.read_bytes()
    assignment = json.loads(raw)
    if set(assignment) != {
        "immutable_finalist_packet", "strict_response_contract", "temporary_response_destination",
    }:
        raise ValueError("assignment must be the exact three-field CLI envelope")
    packet = assignment["immutable_finalist_packet"]
    if hashlib.sha256(packet["content"].encode()).hexdigest() != packet["sha256"]:
        raise ValueError("immutable packet hash mismatch")
    destination = Path(assignment["temporary_response_destination"])
    workspace = destination.parent
    if not destination.is_absolute() or destination != destination.resolve():
        raise ValueError("response destination must use its resolved physical absolute path")
    if workspace.parent != Path(tempfile.gettempdir()).resolve() or not workspace.is_dir():
        raise ValueError("create a fresh directory directly under the system temporary directory")
    if destination.suffix != ".json" or destination.exists() or destination.is_symlink():
        raise ValueError("response destination must be a fresh JSON path")
    runtime_names = {
        "codex-home", "sandbox.sb", "response_schema.json", "events.jsonl",
        "stderr.txt", "transport-final.json", "launch.json",
    }
    if destination.name in runtime_names or any((workspace / name).exists() for name in runtime_names):
        raise ValueError("judge workspace already contains launcher state; use a fresh directory")
    codex = shutil.which("codex")
    if codex is None:
        raise ValueError("Codex CLI is not installed")
    user_codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()
    auth = user_codex_home / "auth.json"
    if not auth.is_file() or auth.is_symlink():
        raise ValueError("an existing regular Codex CLI auth.json is required")
    workspace.chmod(0o700)
    runtime_home = workspace / "codex-home"
    runtime_home.mkdir(mode=0o700)
    profile = workspace / "sandbox.sb"
    profile.write_text(sandbox_profile(workspace, repo, user_codex_home))
    schema = workspace / "response_schema.json"
    schema.write_text(json.dumps(assignment["strict_response_contract"]))
    # A single outer OS sandbox enforces the boundary. Asking Codex to apply a
    # second macOS sandbox makes its tools fail with sandbox_apply EPERM.
    argv = [
        "/usr/bin/sandbox-exec", "-f", str(profile), codex, "exec", "--ephemeral",
        "--ignore-user-config", "--skip-git-repo-check", "-C", str(workspace),
        "-c", "project_doc_max_bytes=0", "-c", "features.memories=false",
        "-c", 'approval_policy="never"', "--sandbox", "danger-full-access",
        "--output-schema", str(schema), "--json", "--color", "never",
        "--output-last-message", str(workspace / "transport-final.json"), "-",
    ]
    receipt = {"argv": argv, "cwd": str(workspace), "assignment_sha256": hashlib.sha256(raw).hexdigest()}
    (workspace / "launch.json").write_text(json.dumps(receipt, indent=2) + "\n")
    env = os.environ.copy()
    env["CODEX_HOME"] = str(runtime_home)
    (runtime_home / "auth.json").symlink_to(auth)
    try:
        with (workspace / "events.jsonl").open("wb") as out, (workspace / "stderr.txt").open("wb") as err:
            result = subprocess.run(argv, cwd=workspace, env=env, input=raw, stdout=out, stderr=err)
        receipt.update(
            exit_code=result.returncode,
            judge_response_written=destination.is_file() and not destination.is_symlink(),
        )
    finally:
        # Do not retain even an auth symlink in evidence copied to the repository.
        (runtime_home / "auth.json").unlink(missing_ok=True)
    (workspace / "launch.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assignment", type=Path)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = launch(args.assignment, args.repo_root.resolve())
        print(json.dumps(result, indent=2))
        raise SystemExit(result["exit_code"] or (0 if result["judge_response_written"] else 2))
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
