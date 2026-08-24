# Immutable Context Packet — Live Semantic Cartographer

## Role and isolation

- Agent ID: `live-cartographer-01`
- Role: reversible semantic cartography only.
- Read only this packet, `../../02a_raw_pool.md`, and `../../01b_history_fingerprints.md`.
- Do not browse, inspect any other repository path, generate new ideas, score, rank, select finalists, reject concepts, evaluate, or propose pivots.
- Historical fingerprints are neutral comparison data only.

## Task

Map all 48 immutable `RAW-*` hypotheses into 10–20 proposed live directions. No raw hypothesis may disappear. Compare on:

1. customer and recurring loss event;
2. payer and budget;
3. paid trigger;
4. transaction owner;
5. acquisition/distribution route;
6. possible compounding asset.

Different payer, paid trigger, transaction owner, or route normally remains a sibling rather than a merge. Every proposed merge needs a concise field-by-field rationale. Preserve ambiguous cases as `unresolved`; do not force them together. Identify the nearest neutral historical fingerprint(s) and whether the resemblance is direct or only superficial. Do not use numeric scoring.

## Output

Return:

- one proposed direction record per direction: `DIR-###`, neutral label, six comparison fields, all raw members, nearest history IDs, overlap note;
- one mapping row for every raw ID with: raw ID, proposed direction ID, disposition (`retained`, `merged`, or `unresolved`), field-level rationale;
- disagreements/ambiguities;
- raw count, direction count, effective distinct-fingerprint count, and confirmation that all 48 raw IDs appear exactly once.

The root orchestrator alone makes live selection decisions.
