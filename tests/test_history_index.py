from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "knowledge/history_index.jsonl"
CHECKPOINT_COMMIT = "8db46d3eef585b696c367f53f4de3aeed9d5f600"
CHECKPOINT_TAG = "pre-cleanup-20260825T080643Z"
FINGERPRINT_FIELDS = [
    "customer",
    "problem_trigger",
    "payer_and_paid_event",
    "offer_and_business_model",
    "distribution_mechanism",
    "compounding_advantage",
]
EXPECTED_CANDIDATES = {
    "zero_to_one_candidates_20260821_002243": 11,
    "zero_to_one_candidates_20260822_110713": 12,
    "zero_to_one_candidates_20260823_103406": 48,
    "zero_to_one_candidates_20260823_235627": 48,
    "zero_to_one_candidates_20260824_111939": 48,
    "zero_to_one_candidates_20260824_164110": 48,
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> tuple[list[str], list[dict]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or any(not line.strip() for line in lines):
        raise AssertionError(f"missing or blank JSONL line in {path}")
    rows = [json.loads(line) for line in lines]
    return lines, rows


class HistoryIndexContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lines, cls.rows = load_jsonl(INDEX_PATH)
        cls.meta = [row for row in cls.rows if row.get("record_type") == "index_meta"]
        cls.run_rows = [
            row for row in cls.rows if row.get("record_type") == "legacy_run_digest_v1"
        ]
        cls.candidates = [
            row for row in cls.rows if row.get("record_type") == "legacy_candidate_v1"
        ]
        cls.outcomes = [
            row for row in cls.rows if row.get("record_type") == "opportunity_outcome_v1"
        ]

    def test_digest_is_compact_canonical_and_complete(self) -> None:
        self.assertLess(INDEX_PATH.stat().st_size, 1_000_000)
        self.assertEqual(len(self.rows), 223)
        self.assertEqual(len(self.meta), 1)
        self.assertEqual(len(self.run_rows), 6)
        self.assertEqual(len(self.candidates), 215)
        self.assertEqual(len(self.outcomes), 1)
        self.assertEqual(
            {row["record_type"] for row in self.rows},
            {
                "index_meta",
                "legacy_run_digest_v1",
                "legacy_candidate_v1",
                "opportunity_outcome_v1",
            },
        )
        for line, row in zip(self.lines, self.rows, strict=True):
            self.assertEqual(
                line,
                json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":")),
            )

    def test_meta_binds_retention_and_recovery(self) -> None:
        meta = self.meta[0]
        self.assertEqual(meta["schema_version"], 3)
        self.assertEqual(meta["history_cutoff_utc"], "2026-07-24T00:00:00Z")
        self.assertEqual(meta["raw_retention"], "digest_only")
        self.assertEqual(meta["checkpoint_commit"], CHECKPOINT_COMMIT)
        self.assertEqual(meta["checkpoint_tag"], CHECKPOINT_TAG)
        self.assertEqual(meta["fingerprint_fields"], FINGERPRINT_FIELDS)
        self.assertIn("never convert", meta["score_policy"])
        self.assertIn("after fresh discovery", meta["read_policy"])
        verification = meta["verification"]
        self.assertEqual(verification["total_rows_including_meta"], len(self.rows))
        self.assertEqual(verification["run_digests"], len(self.run_rows))
        self.assertEqual(verification["candidate_digests"], len(self.candidates))
        self.assertEqual(verification["opportunity_outcomes"], len(self.outcomes))
        self.assertEqual(verification["candidate_counts_by_run"], EXPECTED_CANDIDATES)
        self.assertEqual(verification["checkpoint_run_trees_verified"], 6)
        self.assertEqual(verification["checkpoint_run_tree_files_verified"], 333)
        self.assertEqual(verification["checkpoint_candidate_source_files_verified"], 56)

    def test_run_digests_are_post_cutoff_and_scale_isolated(self) -> None:
        self.assertEqual({row["run_id"] for row in self.run_rows}, set(EXPECTED_CANDIDATES))
        for row in self.run_rows:
            identity = row["run_id"]
            self.assertEqual(row["schema_version"], 3, identity)
            self.assertEqual(row["raw_retention"], "digest_only", identity)
            self.assertEqual(row["candidate_digest_count"], EXPECTED_CANDIDATES[identity])
            self.assertRegex(identity, r"^zero_to_one_candidates_202608(21|22|23|24)_\d{6}$")
            self.assertTrue(row["state_evidence"], identity)
            self.assertTrue(row["candidate_population"], identity)
            self.assertTrue(row["omitted_material"]["reason"], identity)
            source = row["source"]
            self.assertEqual(source["checkpoint_commit"], CHECKPOINT_COMMIT, identity)
            self.assertEqual(source["checkpoint_tag"], CHECKPOINT_TAG, identity)
            self.assertEqual(source["source_hash_algorithm"], "sha256-tree-v1", identity)
            self.assertRegex(source["source_sha256"], r"^[0-9a-f]{64}$", identity)
            self.assertGreater(source["source_file_count"], 0, identity)
            self.assertTrue(
                source["source_path_at_checkpoint"].startswith(
                    "archive/legacy-history/working_folder/"
                ),
                identity,
            )
            for key in ("terminal_objection", "reopen_condition"):
                if row[key] is None:
                    self.assertTrue(row[f"{key}_reason"], (identity, key))

        by_id = {row["run_id"]: row for row in self.run_rows}
        self.assertEqual(by_id["zero_to_one_candidates_20260821_002243"]["score_scale"], "/100")
        self.assertEqual(by_id["zero_to_one_candidates_20260822_110713"]["score_scale"], "/10")
        for run_id in list(EXPECTED_CANDIDATES)[2:]:
            self.assertIsNone(by_id[run_id]["framework_id"])
            self.assertIsNone(by_id[run_id]["score_scale"])
            self.assertTrue(by_id[run_id]["framework_reason"])
            self.assertTrue(by_id[run_id]["score_scale_reason"])

    def test_candidate_digests_are_structured_and_provenance_bound(self) -> None:
        counts = Counter(row["run_id"] for row in self.candidates)
        self.assertEqual(dict(counts), EXPECTED_CANDIDATES)
        identities = [row["candidate_id"] for row in self.candidates]
        self.assertEqual(len(identities), len(set(identities)))

        for row in self.candidates:
            identity = row["candidate_id"]
            self.assertEqual(row["schema_version"], 3, identity)
            self.assertEqual(row["raw_retention"], "digest_only", identity)
            self.assertEqual(
                identity,
                f"legacy:{row['run_id']}:{row['source_candidate_id'].lower()}",
            )
            self.assertTrue(row["title"], identity)
            self.assertEqual(set(row["fingerprint"]), set(FINGERPRINT_FIELDS), identity)
            values = list(row["fingerprint"].values())
            self.assertTrue(all(isinstance(value, str) and value.strip() for value in values), identity)
            self.assertGreaterEqual(len(set(values)), 4, identity)
            self.assertEqual(set(row["fingerprint_source_locators"]), set(FINGERPRINT_FIELDS))
            self.assertTrue(all(row["fingerprint_source_locators"].values()), identity)

            self.assertTrue(row["sources"], identity)
            for source in row["sources"]:
                self.assertEqual(source["checkpoint_commit"], CHECKPOINT_COMMIT, identity)
                self.assertEqual(source["checkpoint_tag"], CHECKPOINT_TAG, identity)
                self.assertEqual(source["source_hash_algorithm"], "sha256-file-v1", identity)
                self.assertRegex(source["source_sha256"], r"^[0-9a-f]{64}$", identity)
                self.assertTrue(source["source_path_at_checkpoint"].startswith("archive/"), identity)
                self.assertTrue(source["locator"], identity)

            score_evidence = row["score_evidence"]
            self.assertIsInstance(score_evidence, list, identity)
            for score in score_evidence:
                self.assertIsInstance(score["raw"], str, identity)
                self.assertTrue(score["raw"], identity)
                self.assertTrue(score["source_locator"], identity)
            if score_evidence:
                self.assertEqual(row["evaluation_type"], "legacy_advisory", identity)
                self.assertIsInstance(row["framework_id"], str, identity)
                self.assertIsInstance(row["score_scale"], str, identity)
                self.assertNotIn("official_score", row, identity)
            else:
                self.assertIsNone(row["evaluation_type"], identity)
                self.assertIsNone(row["framework_id"], identity)
                self.assertIsNone(row["score_scale"], identity)
                self.assertTrue(row["framework_reason"], identity)
                self.assertTrue(row["score_scale_reason"], identity)

            for key in ("terminal_objection", "reopen_condition"):
                if row[key] is None:
                    self.assertTrue(row[f"{key}_reason"], (identity, key))

    def test_native_outcome_remains_bound_to_published_files(self) -> None:
        row = self.outcomes[0]
        self.assertEqual(set(row), OUTCOME_FIELDS)
        self.assertEqual(row["score_scale"], "/10")
        self.assertEqual(row["run_status"], "no_qualifier")
        self.assertIsNone(row["official_score"])
        self.assertIsNone(row["qualification_label"])
        self.assertRegex(row["rubric_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(row["report_sha256"], r"^[0-9a-f]{64}$")
        outcome = ROOT / row["outcome_path"]
        self.assertTrue(outcome.is_dir())
        self.assertEqual(sha256_file(outcome / "report.json"), row["report_sha256"])
        candidate = outcome / row["source_candidate_path"]
        self.assertTrue(candidate.is_file())
        self.assertEqual(sha256_file(candidate), row["source_candidate_sha256"])
        self.assertEqual(set(row["selected_fingerprint"]), set(FINGERPRINT_FIELDS))

    def test_obsolete_archive_contract_is_absent(self) -> None:
        text = INDEX_PATH.read_text(encoding="utf-8")
        self.assertNotIn('\"record_type\":\"idea\"', text)
        self.assertNotIn('\"record_type\":\"run\"', text)
        self.assertNotIn('\"archive_path\"', text)
        self.assertNotIn('\"source_hash_manifest\"', text)
        for row in self.rows:
            self.assertFalse(re.search(r'/(Users|home)/', json.dumps(row)))

    def test_promoleak_dependency_is_preserved_outside_discovery_history(self) -> None:
        dossier = ROOT / "ideas/CONFIRMED_IDEA_20260511_113716.md"
        self.assertTrue(dossier.is_file())
        self.assertEqual(
            sha256_file(dossier),
            "996d87ecec0bc11814ecd6ff72f0291a6a6e6786c04bb7712ae8184df29d3c84",
        )
        self.assertFalse(
            any(
                row.get("record_type") == "legacy_candidate_v1"
                and row.get("title") == "PromoLeak Recovery Desk"
                for row in self.rows
            )
        )


if __name__ == "__main__":
    unittest.main()
