# Legacy archive

This directory is the byte-preserving archive created during the agent-native takeover at checkpoint `bac20e3` on 2026-08-24. Archived material is evidence and provenance, not active workflow configuration.

## Contents

- `legacy-history/working_folder/` contains the original run trees.
- `legacy-history/ideas/` contains the original confirmed and unconfirmed idea dossiers.
- `legacy-history/utility-summaries/` contains the original takeover and final-run summaries.
- `legacy-v2/` contains the retired v2 managers, tests, audit anchors, debug memory, browser instructions, prompts, orchestration rules, and failure brain at their former logical subpaths.
- `legacy-v2/external-contracts/` contains exact snapshots of the five external skill, protocol, and auditor files referenced by v2 at migration time.
- `manifest.jsonl` is the file-level provenance ledger.

Nothing historical was deleted as part of the migration. One carried-over Finder cache, `legacy-history/working_folder/.DS_Store`, was intentionally excluded from the manifest and removed after preservation review. Python caches were not moved.

## Manifest contract

Each JSON line has:

- `kind`: `move` for a repository file relocated into this archive, or `external_snapshot` for an external file copied without changing its source;
- `old_path`: the former repository-relative path, or the absolute external source path;
- `new_path`: the repository-relative archive path;
- `size`: the source byte count at migration time;
- `sha256`: the SHA-256 digest of those exact bytes.

The manifest contains 2,436 move records and five external-snapshot records. All 2,441 destinations (23,867,597 bytes total) were independently checked against their recorded sizes and hashes after the move.

## History-index source hashes

`knowledge/history_index.jsonl` uses `sha256-file-v1` for a preserved idea file: SHA-256 over its exact archived bytes.

Preserved run roots use `sha256-tree-v1`. First verify that the archive manifest and raw directory have identical regular-file membership and that every file's size and SHA-256 match. Then:

1. express each file path relative to the run root with POSIX `/` separators;
2. sort those paths by their UTF-8 byte sequence;
3. for each path, append `<lowercase-file-sha256>  <relative-path>\n` encoded as UTF-8; and
4. SHA-256 the concatenated bytes.

An empty directory therefore has the SHA-256 of the empty byte string. Git exports do not materialize empty directories, so a missing archived run root is accepted only when its indexed file count is zero, its tree hash is the empty-tree hash, and no manifest row exists beneath that prefix. Directory hashes are normalized index provenance, not additional file-level manifest rows. A missing normalized fingerprint or business conclusion remains `null` with a reason; it is never reconstructed from a directory name or score.

## Use and restoration

Normal discovery should consult `knowledge/failure_patterns.md` and selected rows from `knowledge/history_index.jsonl` only after a fresh pool has been generated. It should not load this archive wholesale into generation context.

To restore a file, locate its manifest row, copy `new_path` back to `old_path`, and verify both size and SHA-256 before treating the restoration as complete. For `external_snapshot` rows, `old_path` is provenance only: the archived copy is not an instruction to overwrite the current external skill.

Historical verdicts and scores remain evidence from their original evaluator, wording, and threshold. They are not silently converted into the current rubric or acceptance gate.
