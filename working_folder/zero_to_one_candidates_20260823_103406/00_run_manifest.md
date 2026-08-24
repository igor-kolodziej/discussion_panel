# V2 Matched Non-Routing Generation Experiment

## Registration

- Run profile: `v2_matched_nonrouting`
- Root scope: `baseline-w01` / `matched_baseline` / `audited_funnel` / `frozen_nonrouting`
- Child scope: `shadow-w01` / `shadow` / `archipelago_lite_shadow` / `frozen_nonrouting`
- Cohort kind: `initial` for both; wave index `1`; no regeneration scope
- Root path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260823_103406`
- Child path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260823_103406/shadow_archipelago_lite`
- External trust path: `/Users/igor/Desktop/discussion_panel/audit_anchors/v2_matched_20260823_103406`
- Registered seed and candidate-order seed: `v2-matched-20260823-314159`
- Model: `gpt-5.6-sol`
- Reasoning setting: `high`
- Root start: `2026-08-23T10:34:11.515277+02:00`
- Root deadline: `2026-08-23T13:34:11.515277+02:00`
- Child declaration time: `2026-08-23T10:34:11.515278+02:00`
- Development contract SHA-256: `1495d1b6182ab640bfdaecf74b024b8fd4e934bec47eb8c9a23f212de55750b3`
- Root protection-anchor SHA-256: `4f74eccccf4a142df12c233cb89b4a53c1a15e082830a7ffd1d6b0c1f5f26c78`
- Child protection-anchor SHA-256: `59dd3f478e5f38afdca30c791a0a7d976c436fa04b95b1fbe911579db5a1b028`
- Results remain withheld until both native audits, trust-bundle audit, parity audit, and composite audit pass.

## Equal Opportunity Contract

- Each arm: 48 raw concepts, 12 Level-2 dossiers, six sealed fact-closure candidates, six frozen finalists.
- Each arm: at most 300 unique queries, 10,000,000 uncached input tokens, 700,000 output tokens, 180 wall minutes, and three concurrent agents.
- Each Level-2 entity: 12-query cap, 10,000 uncached-input-token cap, 500-output-token cap, 12-minute cap, 60–220 words, and the five headings in `00b_development_contract.json`.
- Each fact-closure entity: eight-query cap, 10,000 uncached-input-token cap, 500-output-token cap, eight-minute cap, no replacement after sealing, and the same five-heading frozen schema.
- Discovery opportunity: 108 queries per arm. Baseline uses seeded role caps `22/22/22/21/21`; treatment uses 18 queries for each of six scouts.
- Unused budget stays in its original allocation and is logged. No filler queries or prose padding.

### Seeded baseline role permutation

- `rule_structure_analyst` / `baseline-gen-rsa`: query cap 22; raw IDs 10
- `taboo_space_explorer` / `baseline-gen-tse`: query cap 22; raw IDs 10
- `incentive_hacker` / `baseline-gen-ih`: query cap 22; raw IDs 10
- `first_principles_extremist` / `baseline-gen-fpe`: query cap 21; raw IDs 9
- `incumbent_attacker` / `baseline-gen-ia`: query cap 21; raw IDs 9

### Stage wall budgets

- Baseline: discovery 40m; history 10m; cartography/mapping 15m; cluster audit 5m; Level-1 and root selection 10m; Level-2 45m; closure-cohort seal 5m; fact closure 30m; freeze/native audit 20m.
- Treatment: problem discovery 40m; direct construction 15m; transformations/history 15m; cartography/cluster/Level-1 15m; provisional and ballot selection 15m; Level-2 40m; finalist selection/fact closure 25m; freeze/native/composite audit 15m.

## Deterministic Rules

- Seed order is ascending SHA-256 of UTF-8 bytes `seed|namespace|stable_id`.
- Baseline root rule: remove only indispensable unlawful/seriously harmful shapes or directly falsified indispensable premises; retain reversible economic siblings; then choose 12 Level-2 directions and six closure directions by evidence-supported payer event, founder-accessible first contract, compounding control, and fingerprint diversity, with seed order as the sole tie-break. No numeric scoring.
- Treatment provisional selector returns a complete ordered 48-ID list. Ballot order is `commercial_ranker, economics_ranker, tail_recall_challenger`.
- Treatment fills Level-2 slots as 6 provisional, 3 unique round-robin ballot additions, 1 seeded rejected sentinel, 1 highest unused near-cutoff item, and 1 seeded singleton/underrepresented-island item, using the protocol fallbacks and seed order only.
- Treatment finalist selector returns the exact ordered six closure IDs from twelve masked dossiers; the root copies that order unchanged.
- Aggregate runtime tokens come from the final provider `token_count` trace. Uncached input is exact `input_tokens - cached_input_tokens`; output is exact provider `output_tokens`. Multi-entity agent totals are partitioned by stable entity order using integer quotient and first-remainder assignment; sums remain exact. Agent intervals and web call IDs come from the same immutable rollout trace.

## Isolation And Allowlists

Every agent uses `fork_turns: none`, reads exactly one immutable scope-owned packet, and writes one bounded return. Packet bytes are hashed before dispatch. Baseline packets:

- `context/baseline-gen-tse.md`
- `context/baseline-gen-ih.md`
- `context/baseline-gen-ia.md`
- `context/baseline-gen-rsa.md`
- `context/baseline-gen-fpe.md`
- `context/baseline-history-01.md`
- `context/baseline-cartography-01.md`
- `context/baseline-cluster-audit-01.md`
- `context/baseline-level1-01.md`
- `context/baseline-level2-01.md`
- `context/baseline-fact-closure-01.md`

Child packets (reserved now; materialized only after `shadow-dispatch: PASS`):

- `context/shadow-scout-cw.md`
- `context/shadow-scout-sp.md`
- `context/shadow-scout-of.md`
- `context/shadow-scout-iec.md`
- `context/shadow-scout-tsc.md`
- `context/shadow-scout-rfat.md`
- `context/shadow-builder-01.md`
- `context/shadow-builder-02.md`
- `context/shadow-builder-03.md`
- `context/shadow-inverter-01.md`
- `context/shadow-inverter-02.md`
- `context/shadow-recombiner-01.md`
- `context/shadow-recombiner-02.md`
- `context/shadow-history-01.md`
- `context/shadow-cartography-01.md`
- `context/shadow-cluster-audit-01.md`
- `context/shadow-level1-01.md`
- `context/shadow-provisional-selector-01.md`
- `context/shadow-commercial-ranker-01.md`
- `context/shadow-economics-ranker-01.md`
- `context/shadow-tail-challenger-01.md`
- `context/shadow-level2-01.md`
- `context/shadow-finalist-selector-01.md`
- `context/shadow-fact-closure-01.md`

Creative and selector packets contain only the applicable closed context classes, neutral founder constraints, safety/legal boundaries, assigned IDs/evidence, caps, and output schema. They exclude downstream frameworks, thresholds, verdicts, detailed prior rhetoric, other agents' conclusions, and unrestricted repository context.

## Non-Routing Boundary

Both arms are irreversibly non-routing, `shadow_only: true`, and `validation_eligible: false`. This run authorizes generation, neutral research, masking, selection, dossier development, closure, freezing, and auditing only. It authorizes no downstream decision workflow, regeneration, outreach, private proof, real chatbot, or confirmation artifact.

## Repository State At Registration

- Branch: `agent/sync-available-files`
- Commit: `a5908aa4497b121dcb6136e83a82aa85f90b29ec`
- Dirty worktree: `true`
- Exact snapshot: `00d_repository_state.txt` (`670d3da8f3bc1780590f4d78750b8c668095b7ae03bd74d545cbd8cadecbe370`)
