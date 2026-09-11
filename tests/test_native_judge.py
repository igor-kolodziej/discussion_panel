from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "native_judge", ROOT / ".agents/skills/business-opportunity/scripts/launch-native-judge.py",
)
native = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native)
BOUNDED_SPEC = importlib.util.spec_from_file_location(
    "bounded_role", ROOT / ".agents/skills/business-opportunity/scripts/launch-bounded-role.py",
)
bounded = importlib.util.module_from_spec(BOUNDED_SPEC)
BOUNDED_SPEC.loader.exec_module(bounded)


class NativeJudgeBoundaryTests(unittest.TestCase):
    @unittest.skipUnless(sys.platform == "darwin", "macOS launcher boundary")
    def test_bounded_role_can_read_only_its_hash_bound_exception(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            workspace = root / "role"
            workspace.mkdir()
            bound = root / "founder.txt"
            excluded = root / "other-role.json"
            bound.write_text("bounded fixture")
            excluded.write_text("excluded fixture")
            bindings = [{"path": str(bound), "sha256": hashlib.sha256(bound.read_bytes()).hexdigest()}]
            profile = workspace / "sandbox.sb"
            profile.write_text(bounded.bounded_profile(workspace, ROOT, Path.home() / ".codex", bindings))
            script = """from pathlib import Path
import sys
assert Path(sys.argv[1]).read_text() == 'bounded fixture'
for name in sys.argv[2:]:
    try: Path(name).read_bytes()
    except PermissionError: pass
    else: raise AssertionError('excluded read succeeded')
try: Path(sys.argv[1]).write_text('forbidden')
except PermissionError: pass
else: raise AssertionError('bound input write succeeded')
"""
            result = subprocess.run([
                "/usr/bin/sandbox-exec", "-f", str(profile), sys.executable, "-c", script,
                str(bound), str(excluded), str(excluded).replace("/private/var/", "/var/"), str(ROOT / "AGENTS.md"),
            ], cwd=workspace, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            bound.write_text("changed fixture")
            with self.assertRaisesRegex(ValueError, "binding hash mismatch"):
                bounded.bounded_profile(workspace, ROOT, Path.home() / ".codex", bindings)

    @unittest.skipUnless(sys.platform == "darwin", "macOS launcher boundary")
    def test_os_boundary_allows_workspace_and_denies_other_judge_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            workspace = root / "judge"
            previous = root / "previous"
            workspace.mkdir()
            previous.mkdir()
            (workspace / "input.txt").write_text("allowed fixture")
            (previous / "response.json").write_text('{"fixture":true}')
            profile = workspace / "sandbox.sb"
            profile.write_text(native.sandbox_profile(workspace, ROOT, Path.home() / ".codex"))
            paths = [previous / "response.json", Path(str(previous / "response.json").replace("/private/var/", "/var/")), ROOT / "AGENTS.md"]
            self.assertTrue(all(path.is_file() for path in paths))
            script = """import json,sys
from pathlib import Path
p=Path(sys.argv[1]); report={'read':(p/'input.txt').read_text()}
(p/'output.txt').write_text('allowed output'); report['write']=True
denials=[]
for name in sys.argv[2:]:
    try:Path(name).read_bytes(); denials.append(False)
    except PermissionError:denials.append(True)
try:(p.parent/'outside.txt').write_text('forbidden'); report['outside_write_denied']=False
except PermissionError:report['outside_write_denied']=True
report['read_denials']=denials
print(json.dumps(report))
"""
            result = subprocess.run(
                ["/usr/bin/sandbox-exec", "-f", str(profile), sys.executable, "-c", script, str(workspace), *map(str, paths)],
                cwd=workspace, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {
                "read": "allowed fixture", "write": True,
                "outside_write_denied": True, "read_denials": [True, True, True],
            })
            self.assertFalse((root / "outside.txt").exists())

    def test_assignment_hash_is_checked_before_launch(self) -> None:
        if sys.platform != "darwin":
            self.skipTest("macOS launcher")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "assignment.json"
            path.write_text(json.dumps({
                "immutable_finalist_packet": {"content": "harmless", "sha256": "0" * 64},
                "strict_response_contract": {},
                "temporary_response_destination": str(Path(directory) / "response.json"),
            }))
            with self.assertRaisesRegex(ValueError, "packet hash mismatch"):
                native.launch(path, ROOT)


if __name__ == "__main__":
    unittest.main()
