# Final Integrity Check

## Verdict

- **Routing and candidate-identity integrity:** PASS.
- **Shadow isolation and strict structural audit:** PASS.
- **Native strict structural audit of the live root:** FAIL; not certified.
- **Approval and validation-path integrity:** PASS.
- **Confirmed-idea gate:** NOT REACHED.

This split verdict is deliberate. The run does not convert a semantic check into a native structural pass.

## Protection And Freeze Pins

| Anchor | SHA-256 pin | Recheck |
|---|---|---|
| Initial live protection anchor | `c1a6bfe07cb96ec2b0ac089251ed7f0b4f74ec2cbcf4e51df0e07f21b066913c` | exact file digest matches |
| Initial live freeze seal | `55e9dd757b019c710b435106304d1a9e907059aa0cef24135342ff49f1c2c39f` | exact file digest and all six candidate digests match |
| Shadow protection anchor | `4abdcb16e9b1b52223a70caa924b0ecfc31edaa78ace15ad5851fed84ca057fe` | exact file digest matches |
| Shadow freeze seal | `6a3f31492e1d2bb4cee6564bb4ad009497a03cd15f0fe06a1aa8243fbde7d2d5` | exact file digest and all six shadow-candidate digests match |
| Wave 2 live freeze seal | `20243633fd6d458c33946bc3d1d7e66febbce3d14c72344d3bbf904fe79bd682` | exact file digest and all six regenerated-candidate digests match |

The Wave 2 seal uses `zt1-regeneration-freeze-seal-v1` because the native auditor has no multi-wave candidate namespace under one run directory. Wave 2 candidates use `wave2_candidate_*.md` so they do not collide with or retroactively invalidate the initial externally sealed `finalist_*.md` set.

## Shadow Isolation

- Shadow manifest: `shadow_only: true`, `validation_eligible: false`.
- Shadow native strict audit: `PASS`, 0 findings.
- Shadow resources reconcile exactly at 300 queries, 1,834,232 uncached input tokens, 205,820 output tokens, 73.3333 wall minutes and maximum concurrency 3.
- An exact search for `SFIN-*`, every shadow candidate title and `shadow_finalist_*` across initial live candidates, live Level-2 dossiers, live context packets, Wave 2 generation, Wave 2 frozen candidates and advisory artifacts returned zero matches.
- No shadow candidate was promoted, substituted, reordered, rewritten, evaluated, panel-scored, sent to a chatbot or used to influence regeneration.

## Live Candidate Identity And Routing

- Initial six live finalist hashes still match the pre-shadow external seal.
- Wave 2 fixed the same six fact-closure candidates selected by the isolated masked selector; no reserve replaced them after closure.
- All six Wave 2 evaluator packets used the exact frozen hashes in the Wave 2 seal.
- Every Wave 2 evaluator was fresh and isolated. No evaluator saw another candidate, prior evaluation, score threshold, historical rejection rhetoric, shadow artifact or validator feedback.
- All twelve live advisory diagnoses across both waves were `decision-critical research`; none was a `strong opportunity`.
- Canonical routing therefore sent zero candidates to simulated judging. No simulated score exists.
- The simulated precondition for a real Zero to One chat was never reached. No working or fresh chatbot chat was opened.
- No pivot agent was invoked because the dominant issue was unavailable private evidence, not a bounded structural repair that could be evaluated without recycling feedback.

## Approval Boundary

No customer, owner, installer, MSP, law firm, auditor, engineer, insurer, MSSP, processor, carrier, debtor, developer, regulator, broker, registry or chatbot was contacted. No contract, option, mandate, authorization, filing, registration, quote request, purchase, capital transfer, account change or external commitment was made.

The validation path, thresholds and external-action gates were not changed. Every proposed resolving test is recorded as approval-gated and remains unexecuted.

## Native Live Audit Failure

The exact native strict report is retained as `10_live_native_audit_report.json`. It reports `FAIL` with 164 errors and 5 unknowns. Two categories must be distinguished:

### Genuine live provenance/telemetry deficiencies

- Run-level resource totals are zero while agent records calculate 527,450 uncached input tokens, 113,951 output tokens and 48 unique typed query events.
- Creative and Level-2 query allocations are declared but their reciprocal typed query/source/tool events are absent.
- Forty-two source events point to evidence IDs missing from the native ledger.
- The file-read and tool-event completeness flags are false.
- One anti-overmerge packet records a `/tmp` input outside the run directory.
- Four agent elapsed values are rounded inconsistently with their timestamp intervals.
- The live run record remains `frozen` and lacks a typed end timestamp, so completion invariants cannot be certified.

These are not repaired retroactively because exact historical events and timestamps were not retained; inventing them would be worse than an explicit failure.

### Auditor/schema incompatibility with the requested live-plus-shadow layout

- The native auditor interprets `matched_pilot: true` as requiring `matched_baseline` agents, even though the canonical contract defines this root as routing-enabled `audited_funnel` with a separate matched `archipelago_lite_shadow` child.
- It recursively includes the child shadow finalists in the live freeze artifact set.
- It consequently labels legitimate live downstream advisory files as forbidden non-routing artifacts.
- Its allocation-stage enum rejects several stages that its own agent-stage enum accepts.

Changing the frozen live manifest to `matched_pilot: false`, changing live agents to non-routing, moving shadow data, suppressing downstream artifacts or issuing a replacement historical seal would alter or conceal the registered workflow. Those changes were not made.

## Auditor Self-Test

The auditor's own self-test suite was run after final evaluation: **82 tests passed, 0 failed**. This confirms the tool executed correctly; it does not override the live run's failed conformance result.

## Confirmed-Idea Check

No exact candidate reached an official lower simulated score, working-chat score or fresh-chat score. No `CONFIRMED_IDEA_20260822_*.md` file exists or was created. Older confirmed-idea files were left untouched.

