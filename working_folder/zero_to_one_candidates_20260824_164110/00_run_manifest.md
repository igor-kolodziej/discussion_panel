# V2 Matched Non-Routing Generation Experiment

## Registration

- Run profile: `v2_matched_nonrouting`
- Root scope: `baseline-w01` / `matched_baseline` / `audited_funnel` / `frozen_nonrouting`
- Child scope: `shadow-w01` / `shadow` / `archipelago_lite_shadow` / `frozen_nonrouting`
- Cohort kind: `initial` for both; wave index `1`; no regeneration scope
- Root path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260824_164110`
- Child path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260824_164110/shadow_archipelago_lite`
- External trust path: `/Users/igor/Desktop/discussion_panel/audit_anchors/v2_matched_20260824_164110`
- Registered seed and candidate-order seed: `v2-matched-20260824_164110-2e1793c49609ecd2aa31258b9632902d`
- Model: `gpt-5.6-sol`
- Reasoning setting: `high`
- Root start: `2026-08-24T16:41:25.768295+02:00`
- Root deadline: `2026-08-24T19:41:25.768295+02:00`
- Child declaration time: `2026-08-24T16:41:25.768296+02:00`
- Development contract SHA-256: `521379f9314e7ebc5954265064f594de6716d31cd66ee230d444dc70ffb46aa1`
- Root protection-anchor SHA-256: `9f53fbd3c4271f45a2d23a1c450e482eb160b7b9c75eb7d1e9426d3d287d3fab`
- Child protection-anchor SHA-256: `a897c5932317c8b1740e1eee6f9e85e9e63597a0dd02ff99319a02d1f8181c94`
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

- `incumbent_attacker` / `baseline-gen-ia`: query cap 22; raw IDs 10
- `first_principles_extremist` / `baseline-gen-fpe`: query cap 22; raw IDs 10
- `taboo_space_explorer` / `baseline-gen-tse`: query cap 22; raw IDs 10
- `incentive_hacker` / `baseline-gen-ih`: query cap 21; raw IDs 9
- `rule_structure_analyst` / `baseline-gen-rsa`: query cap 21; raw IDs 9

### Stage timing

- The 180-minute aggregate arm cap and three-agent concurrency cap remain hard. Candidate caps are admission ceilings, not reservations: four Level-2 batches and two closure batches must be scheduled within the remaining run window, and launch must stop if the actual deadline cannot accommodate another batch.

## Deterministic Rules

- Seed order is ascending SHA-256 of UTF-8 bytes `seed|namespace|stable_id`.
- Baseline root rule: remove only indispensable unlawful/seriously harmful shapes or directly falsified indispensable premises; retain reversible economic siblings; then choose 12 Level-2 directions and six closure directions by evidence-supported payer event, founder-accessible first contract, compounding control, and fingerprint diversity, with seed order as the sole tie-break. No numeric scoring.
- Treatment provisional selector returns a complete ordered 48-ID list. Ballot order is `economics_ranker, commercial_ranker, tail_recall_challenger`.
- Treatment fills Level-2 slots as 6 provisional, 3 unique round-robin ballot additions, 1 seeded rejected sentinel, 1 highest unused near-cutoff item, and 1 seeded singleton/underrepresented-island item, using the protocol fallbacks and seed order only.
- Treatment finalist selector returns the exact ordered six closure IDs from twelve masked dossiers; the root copies that order unchanged.
- Runtime tokens come from each candidate agent's own provider `token_count` trace, both during live monitoring and at final admission. Uncached input is exact `input_tokens - cached_input_tokens`; output is exact provider `output_tokens`; elapsed time is an exact integer count of timestamp-derived microseconds. Agent intervals, task identity, web call IDs, returned source URLs, and resources are independently reconciled by the pinned auditor against that same immutable candidate-owned trace.

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
- `context/baseline-level2-02.md`
- `context/baseline-level2-03.md`
- `context/baseline-level2-04.md`
- `context/baseline-level2-05.md`
- `context/baseline-level2-06.md`
- `context/baseline-level2-07.md`
- `context/baseline-level2-08.md`
- `context/baseline-level2-09.md`
- `context/baseline-level2-10.md`
- `context/baseline-level2-11.md`
- `context/baseline-level2-12.md`
- `context/baseline-fact-closure-01.md`
- `context/baseline-fact-closure-02.md`
- `context/baseline-fact-closure-03.md`
- `context/baseline-fact-closure-04.md`
- `context/baseline-fact-closure-05.md`
- `context/baseline-fact-closure-06.md`

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
- `context/shadow-level2-02.md`
- `context/shadow-level2-03.md`
- `context/shadow-level2-04.md`
- `context/shadow-level2-05.md`
- `context/shadow-level2-06.md`
- `context/shadow-level2-07.md`
- `context/shadow-level2-08.md`
- `context/shadow-level2-09.md`
- `context/shadow-level2-10.md`
- `context/shadow-level2-11.md`
- `context/shadow-level2-12.md`
- `context/shadow-finalist-selector-01.md`
- `context/shadow-fact-closure-01.md`
- `context/shadow-fact-closure-02.md`
- `context/shadow-fact-closure-03.md`
- `context/shadow-fact-closure-04.md`
- `context/shadow-fact-closure-05.md`
- `context/shadow-fact-closure-06.md`

Creative and selector packets contain only the applicable closed context classes, neutral founder constraints, safety/legal boundaries, assigned IDs/evidence, caps, and output schema. They exclude downstream frameworks, thresholds, verdicts, detailed prior rhetoric, other agents' conclusions, and unrestricted repository context.

## Non-Routing Boundary

Both arms are irreversibly non-routing, `shadow_only: true`, and `validation_eligible: false`. This run authorizes generation, neutral research, masking, selection, dossier development, closure, freezing, and auditing only. It authorizes no downstream decision workflow, regeneration, outreach, private proof, real chatbot, or confirmation artifact.

## Repository State At Registration

- Branch: `agent/sync-available-files`
- Commit: `a5908aa4497b121dcb6136e83a82aa85f90b29ec`
- Dirty worktree: `true`
- Exact snapshot: `00d_repository_state.txt` (`c58afbace3244b32c2acc0a47ff7b7934ea4abe1bd22a42436585cde601e277c`)
