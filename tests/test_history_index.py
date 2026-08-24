from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "knowledge/history_index.jsonl"
MANIFEST_PATH = ROOT / "archive/manifest.jsonl"
FINGERPRINT_FIELDS = {
    "customer",
    "problem_trigger",
    "payer_and_paid_event",
    "offer_and_business_model",
    "distribution_mechanism",
    "compounding_advantage",
}
REQUIRED_PROVENANCE_FIELDS = {
    "original_path",
    "archive_path",
    "source_kind",
    "source_hash_algorithm",
    "source_sha256",
    "source_file_count",
    "source_hash_manifest",
    "source_hash_verified_against_manifest",
    "legacy_label",
    "legacy_state",
    "framework_id",
    "score_scale",
    "fingerprint",
    "terminal_objection",
    "reopen_condition",
}
OUTCOME_FIELDS = {
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


def load_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(not line.strip() for line in lines):
        raise AssertionError(f"blank JSONL line in {path}")
    return [json.loads(line) for line in lines]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_files(path: Path) -> list[Path]:
    candidates = list(path.rglob("*"))
    symlinks = [candidate for candidate in candidates if candidate.is_symlink()]
    if symlinks:
        raise AssertionError(f"symlinks are not valid sha256-tree-v1 members: {symlinks}")
    files = [candidate for candidate in candidates if candidate.is_file()]
    return sorted(files, key=lambda candidate: candidate.relative_to(path).as_posix().encode("utf-8"))


def sha256_tree(path: Path) -> tuple[str, list[Path]]:
    files = tree_files(path)
    records = []
    for candidate in files:
        relative = candidate.relative_to(path).as_posix()
        records.append(f"{sha256_file(candidate)}  {relative}\n")
    return hashlib.sha256("".join(records).encode("utf-8")).hexdigest(), files


class HistoryIndexContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = load_jsonl(INDEX_PATH)
        cls.manifest = load_jsonl(MANIFEST_PATH)
        cls.manifest_by_new = {row["new_path"]: row for row in cls.manifest}

    def test_normalized_contract_and_preserved_counts(self) -> None:
        meta_rows = [row for row in self.rows if row["record_type"] == "index_meta"]
        idea_rows = [row for row in self.rows if row["record_type"] == "idea"]
        run_rows = [row for row in self.rows if row["record_type"] == "run"]
        outcome_rows = [row for row in self.rows if row["record_type"] == "opportunity_outcome_v1"]

        self.assertEqual(len(meta_rows), 1)
        self.assertEqual(len(idea_rows), 15)
        self.assertEqual(len(run_rows), 37)
        self.assertEqual(
            len(self.rows),
            len(meta_rows) + len(idea_rows) + len(run_rows) + len(outcome_rows),
        )
        meta = meta_rows[0]
        self.assertEqual(meta["schema_version"], 2)
        self.assertEqual(set(meta["source_hash_contract"]), {"sha256-file-v1", "sha256-tree-v1"})
        self.assertEqual(set(meta["fingerprint_fields"]), FINGERPRINT_FIELDS)
        self.assertIn("do not normalize, convert", meta["score_policy"])

        identities: set[tuple[str, str]] = set()
        for row in idea_rows + run_rows:
            identity_key = "idea_id" if row["record_type"] == "idea" else "run_id"
            identity = (row["record_type"], row[identity_key])
            self.assertNotIn(identity, identities)
            identities.add(identity)
            self.assertFalse(REQUIRED_PROVENANCE_FIELDS - row.keys(), identity)
            self.assertTrue(row["source_hash_verified_against_manifest"], identity)
            self.assertEqual(row["source_hash_manifest"], "archive/manifest.jsonl")
            self.assertRegex(row["source_sha256"], r"^[0-9a-f]{64}$")
            self.assertIsInstance(row["source_file_count"], int)
            self.assertGreaterEqual(row["source_file_count"], 0)
            for key in ("original_path", "archive_path", "legacy_label", "legacy_state", "framework_id", "score_scale"):
                self.assertIsInstance(row[key], str, (identity, key))
                self.assertTrue(row[key], (identity, key))

            fingerprint = row["fingerprint"]
            if fingerprint is None:
                self.assertIsInstance(row.get("fingerprint_reason"), str, identity)
                self.assertTrue(row["fingerprint_reason"], identity)
            else:
                self.assertEqual(set(fingerprint), FINGERPRINT_FIELDS, identity)
                self.assertTrue(all(isinstance(value, str) and value for value in fingerprint.values()), identity)

            for key in ("terminal_objection", "reopen_condition"):
                value = row[key]
                if value is None:
                    reason = row.get(f"{key}_reason")
                    self.assertIsInstance(reason, str, (identity, key))
                    self.assertTrue(reason, (identity, key))
                else:
                    self.assertIsInstance(value, str, (identity, key))
                    self.assertTrue(value, (identity, key))

            for evidence_key in (
                "normalization_evidence_paths",
                "terminal_objection_sources",
                "reopen_condition_sources",
            ):
                for evidence_path in row.get(evidence_key, []):
                    self.assertTrue((ROOT / evidence_path).is_file(), (identity, evidence_key, evidence_path))

            for score in row.get("score_evidence", []):
                self.assertIsInstance(score.get("raw"), str, identity)
                self.assertTrue(score["raw"], identity)
            for label in row.get("verdict_evidence", []):
                self.assertIsInstance(label, str, identity)
                self.assertTrue(label, identity)

        for row in outcome_rows:
            self.assertEqual(set(row), OUTCOME_FIELDS, row.get("run_id"))
            self.assertEqual(row["score_scale"], "/10")
            for key in (
                "run_id",
                "run_status",
                "rubric_id",
                "rubric_sha256",
                "report_sha256",
                "outcome_path",
            ):
                self.assertIsInstance(row[key], str, (row.get("run_id"), key))
                self.assertTrue(row[key], (row.get("run_id"), key))
            self.assertRegex(row["rubric_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(row["report_sha256"], r"^[0-9a-f]{64}$")
            if row["source_candidate_sha256"] is not None:
                self.assertRegex(row["source_candidate_sha256"], r"^[0-9a-f]{64}$")

    def test_every_source_hash_matches_manifest_and_raw_archive(self) -> None:
        for row in self.rows:
            if row["record_type"] not in {"idea", "run"}:
                continue
            identity = row.get("idea_id") or row["run_id"]
            archive_root = ROOT / row["archive_path"]
            self.assertTrue(archive_root.exists(), identity)

            if row["source_kind"] == "file":
                self.assertEqual(row["source_hash_algorithm"], "sha256-file-v1")
                self.assertEqual(row["source_file_count"], 1)
                digest = sha256_file(archive_root)
                self.assertEqual(digest, row["source_sha256"], identity)
                manifest_row = self.manifest_by_new.get(row["archive_path"])
                self.assertIsNotNone(manifest_row, identity)
                self.assertEqual(manifest_row["old_path"], row["original_path"], identity)
                self.assertEqual(manifest_row["sha256"], digest, identity)
                self.assertEqual(manifest_row["size"], archive_root.stat().st_size, identity)
                continue

            self.assertEqual(row["source_kind"], "directory", identity)
            self.assertEqual(row["source_hash_algorithm"], "sha256-tree-v1", identity)
            digest, files = sha256_tree(archive_root)
            self.assertEqual(digest, row["source_sha256"], identity)
            self.assertEqual(len(files), row["source_file_count"], identity)

            archive_prefix = row["archive_path"] + "/"
            original_prefix = row["original_path"] + "/"
            raw_relpaths = [candidate.relative_to(archive_root).as_posix() for candidate in files]
            manifest_rows = [
                entry for entry in self.manifest if entry.get("new_path", "").startswith(archive_prefix)
            ]
            manifest_rows.sort(key=lambda entry: entry["new_path"][len(archive_prefix):].encode("utf-8"))
            manifest_relpaths = [entry["new_path"][len(archive_prefix):] for entry in manifest_rows]
            self.assertEqual(manifest_relpaths, raw_relpaths, identity)

            for candidate, manifest_row, relative in zip(files, manifest_rows, raw_relpaths, strict=True):
                file_digest = sha256_file(candidate)
                self.assertEqual(manifest_row["old_path"], original_prefix + relative, (identity, relative))
                self.assertEqual(manifest_row["sha256"], file_digest, (identity, relative))
                self.assertEqual(manifest_row["size"], candidate.stat().st_size, (identity, relative))


if __name__ == "__main__":
    unittest.main()
