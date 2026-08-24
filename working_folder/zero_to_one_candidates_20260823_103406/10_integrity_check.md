# V2 Matched Experiment Failure Receipt

## Outcome

- Experiment status: `FAIL`; stopped at lifecycle prefix `level2_cohort_sealed`.
- Advancement gate: `selection` returned exact status `FAIL` with exit code `1`.
- The baseline Level-2 return was not admitted to the ledger or rendered as dossiers.
- The Archipelago-Lite child directory was never materialized.
- No freeze seal, child trust bundle, native PASS report, composite PASS report, or cohort reveal exists.

## Exact Gate Command

```text
python3 /Users/igor/.codex/skills/generate-zero-to-one-candidates/scripts/audit_funnel.py working_folder/zero_to_one_candidates_20260823_103406 --strict --json --checkpoint selection --protection-anchor audit_anchors/v2_matched_20260823_103406/baseline_protection_anchor.json --protection-anchor-sha256 4f74eccccf4a142df12c233cb89b4a53c1a15e082830a7ffd1d6b0c1f5f26c78
```

## Resource-Exhaustion Stop

- Runtime trace: `/Users/igor/.codex/sessions/2026/08/23/rollout-2026-08-23T11-19-34-01a02deb-0fdd-7d30-9c6d-df62c83ca558.jsonl`
- Trace SHA-256: `323f291999349f7599425f7f07e535f9680ab01c79ccd3639d9f9d6b4626230b`
- Exact input tokens: `1,933,275`; cached input tokens: `1,800,192`; uncached input tokens: `133,083`.
- Exact output tokens: `7,978`.
- Exact active elapsed time: `4.455016666666666` minutes.
- Exact public web calls: `24`.
- Registered deterministic 12-way uncached-input partition: three allocations at `11,091` tokens and nine at `11,090`; every allocation exceeds the `10,000` cap.
- Registered deterministic 12-way output partition: ten allocations at `665` tokens and two at `664`; every allocation exceeds the `500` cap.
- Retrying, discarding the metered attempt, transferring budget, or replacing a candidate is not authorized by the frozen contract.

## Gate Findings

The gate emitted 67 findings:

- Errors: `AGENT_ELAPSED_MISMATCH` ×6; `AGENT_RESOURCE_INVALID` ×9; `CHECKPOINT_BLOCKED` ×1; `CHECKPOINT_STATE_NOT_REACHED` ×1; `CHILD_SCOPE_DECLARATION_INVALID` ×1; `DEVELOPMENT_CONTRACT_OPPORTUNITY_MISMATCH` ×1; `FACT_CLOSURE_COHORT_BINDING_INVALID` ×1; `FACT_CLOSURE_COHORT_COUNT_INVALID` ×1; `FACT_CLOSURE_COHORT_SCHEMA_INVALID` ×1; `FACT_CLOSURE_SELECTION_ORDER_INVALID` ×1; `MATCHED_DISCOVERY_ALLOCATION_SPLIT_INVALID` ×1; `MATCHED_QUERY_OPPORTUNITY_INCOMPLETE` ×2; `RESOURCE_TOTAL_INVALID` ×1; `STAGE_BOUNDARY_RESOURCE_TOTALS_MISMATCH` ×3; `V2_STAGE_ROLE_CARDINALITY_INVALID` ×3.
- Unknowns: `CHILD_TRUST_BUNDLE_MISSING` ×1; `DEVELOPMENT_RESOURCE_TELEMETRY_INCOMPLETE` ×1.
- Warnings: `DISPOSITION_UNRESOLVED` ×32, reflecting deliberately preserved economic siblings.

The resource-field and elapsed findings show that earlier manifest telemetry also used an auditor-incompatible numeric representation. Future-stage, child, trust, closure, and cardinality findings remain unresolved because this run stopped before those boundaries.

## Frozen Evidence State

- Machine manifest SHA-256: `26e206ca65411c396516b79b1ff9ec6ec654451022dff09b950c57f7d3f57ad5`.
- Reversible ledger SHA-256: `6a4675bbf947abc7f64426540ef21bbf3688346cd7438d2dfebe71aeec49ba02`.
- Sealed baseline Level-2 cohort receipt SHA-256: `d2199ed9d2e9fffda1e657d34afb8264d3ba0a793ac34fd80208f5cd1a11e7f9`.
- Unadmitted Level-2 agent return SHA-256: `f0c8443b2f8e490d2f5cfc3a526c9eef4bca70d400e373cd289124b19096fd72`.
- Preliminary, unrevealed diagnostics: 48 raw hypotheses; 16 reversible directions; effective concept count 48; 32 explicit unresolved field disagreements; 45 neutral historical-neighbor links; nine unique opened Level-2 URLs across 12 returned drafts.

## Prohibited Actions

No evaluation, scoring, validation execution, pivot, promotion, regeneration, private proof, external outreach, real-chatbot contact, confirmed-idea artifact, downstream routing, or treatment dispatch occurred.
