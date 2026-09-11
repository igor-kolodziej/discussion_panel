#!/usr/bin/env python3
"""Run one fresh non-holdout role with exact read bindings and optional structured output.

The supervisor prepares dispatch.txt, allowed-reads.json and (for scouts, required)
response_schema.json in a fresh physical temporary directory. No canonical writes,
response corrections, retries, role selection or business judgments happen here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


SPEC = importlib.util.spec_from_file_location(
    "native_judge", Path(__file__).with_name("launch-native-judge.py")
)
native = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native)


def bounded_profile(workspace: Path, repo: Path, codex_home: Path, bindings: list[dict]) -> str:
    permits = []
    for binding in bindings:
        if set(binding) != {"path", "sha256"}:
            raise ValueError("each read binding requires exactly path and sha256")
        path = Path(binding["path"])
        if not path.is_absolute() or path != path.resolve() or not path.is_file():
            raise ValueError("read bindings must name physical absolute files")
        if hashlib.sha256(path.read_bytes()).hexdigest() != binding["sha256"]:
            raise ValueError(f"read binding hash mismatch: {path}")
        permits.append(f"(require-not (literal {json.dumps(str(path))}))")
    lines = []
    for line in native.sandbox_profile(workspace, repo, codex_home).splitlines():
        prefix = "(deny file-read-data "
        if permits and line.startswith(prefix):
            line = prefix + "(require-all " + line[len(prefix):-1] + " " + " ".join(permits) + "))"
        lines.append(line)
    return "\n".join(lines) + "\n"


def launch(workspace: Path, repo: Path) -> dict:
    if sys.platform != "darwin":
        raise ValueError("this launcher requires macOS sandbox-exec")
    if workspace != workspace.resolve() or workspace.parent != Path(tempfile.gettempdir()).resolve():
        raise ValueError("use a fresh physical directory directly under the system temporary directory")
    required = {"dispatch.txt", "allowed-reads.json"}
    allowed = required | {"response_schema.json"}
    names = {path.name for path in workspace.iterdir()}
    if not required <= names or not names <= allowed or any(path.is_symlink() for path in workspace.iterdir()):
        raise ValueError("workspace must contain only fresh dispatch, read bindings and optional response schema")
    prompt = (workspace / "dispatch.txt").read_bytes()
    bindings = json.loads((workspace / "allowed-reads.json").read_bytes())
    if not isinstance(bindings, list):
        raise ValueError("allowed-reads.json must be an array of file/hash bindings")
    user_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()
    auth = user_home / "auth.json"
    if not auth.is_file() or auth.is_symlink():
        raise ValueError("an existing regular Codex CLI auth.json is required")
    codex = shutil.which("codex")
    if codex is None:
        raise ValueError("Codex CLI is not installed")
    profile_text = bounded_profile(workspace, repo, user_home, bindings)
    workspace.chmod(0o700)
    runtime = workspace / "codex-home"
    runtime.mkdir(mode=0o700)
    shell_options = native.tool_shell_options(workspace)
    profile = workspace / "sandbox.sb"
    profile.write_text(profile_text)
    schema = workspace / "response_schema.json"
    argv = [
        "/usr/bin/sandbox-exec", "-f", str(profile), codex, "--search", "exec",
        "--ephemeral", "--ignore-user-config", "--skip-git-repo-check", "-C", str(workspace),
        "-c", "project_doc_max_bytes=0", "-c", "features.memories=false",
        *shell_options,
        "-c", 'approval_policy="never"', "--sandbox", "danger-full-access",
        *(["--output-schema", str(schema)] if schema.is_file() else []),
        "--json", "--color", "never", "--output-last-message", str(workspace / "response.json"), "-",
    ]
    receipt = {
        "argv": argv, "cwd": str(workspace), "prompt_sha256": hashlib.sha256(prompt).hexdigest(),
        "allowed_reads": bindings,
        "response_schema_sha256": hashlib.sha256(schema.read_bytes()).hexdigest() if schema.is_file() else None,
    }
    (workspace / "launch.json").write_text(json.dumps(receipt, indent=2) + "\n")
    env = os.environ.copy()
    env["CODEX_HOME"] = str(runtime)
    env["PWD"] = str(workspace)
    (runtime / "auth.json").symlink_to(auth)
    try:
        with (workspace / "events.jsonl").open("wb") as out, (workspace / "stderr.txt").open("wb") as err:
            result = subprocess.run(argv, cwd=workspace, env=env, input=prompt, stdout=out, stderr=err)
        response = workspace / "response.json"
        receipt.update(
            exit_code=result.returncode,
            response_sha256=hashlib.sha256(response.read_bytes()).hexdigest() if response.is_file() else None,
        )
    finally:
        (runtime / "auth.json").unlink(missing_ok=True)
    (workspace / "launch.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = launch(args.workspace, args.repo_root.resolve())
        print(json.dumps(result, indent=2))
        raise SystemExit(result["exit_code"] or (0 if result["response_sha256"] else 2))
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
