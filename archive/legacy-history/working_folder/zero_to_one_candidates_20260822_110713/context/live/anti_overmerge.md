# Immutable Context Packet — Live Anti-Overmerge Auditor

## Role and isolation

- Agent ID: `live-anti-overmerge-01`
- Role: anti-overmerge audit only.
- Read only this packet, `../../02a_raw_pool.md`, and `/tmp/zt1_live_cartographer_20260822.md` (SHA-256 `aff15cb29aa2b4025e910d8447b976392c84742057832f3496aaed7473842727`).
- Do not browse, inspect other files, generate ideas, score, rank, select, reject, evaluate, or pivot.

## Task

Audit the proposed 19-direction reversible map. Challenge:

1. every direction with more than three members;
2. the sole proposed effective merge (`RAW-TSE-05` with `RAW-FPE-04`);
3. every placement where payer, paid trigger, transaction owner, acquisition route, or compounding asset differs;
4. the two unresolved placements;
5. coverage of all 48 raw IDs exactly once.

Different payers, paid triggers, transaction owners, or routes normally require sibling preservation or a split. A direction may be a broad family containing siblings, but must not be misrepresented as one effective fingerprint. Do not delete any raw hypothesis.

## Output

- findings by direction with `accept`, `split`, or `keep_as_family_not_merge`;
- a decision on the proposed effective merge;
- any corrected direction membership proposal;
- effective distinct-fingerprint count after corrections;
- exact coverage confirmation;
- concise integrity exceptions, if any.

The root orchestrator alone makes live selection decisions.
