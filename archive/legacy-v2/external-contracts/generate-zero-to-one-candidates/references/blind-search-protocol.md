# Blind Search Protocol

Use this reference for the V2 machine contract of audited-funnel, live-with-shadow, matched non-routing, and regeneration discovery scopes. The Archipelago stages apply only to `archipelago_lite_shadow`; the shared profile, state, isolation, telemetry, protection, and audit rules apply to every V2 scope. This is a non-validator discovery contract. It does not authorize changes to validation eligibility, candidate counts at validation, validation timing, feedback reuse, gates, or budget.

## Non-validator boundary

- Keep the fixed validator, evaluator, success criteria, founder facts, and safety/legal boundaries unchanged.
- The shadow arm must not call an advisory evaluator, pivot skill, simulated judge, working-chat judge, or fresh-chat judge.
- Moving a forbidden call or downstream artifact timestamp past the declared run end does not create approval; its presence anywhere in the non-routing run manifest or artifact tree is a violation.
- The shadow arm must not add, remove, replace, reorder, or rewrite candidates in the live downstream path.
- Do not expose validator files, framework wording, weights, scores, thresholds, objections, rankings, or suggested remedies to discovery, clustering, shadow selection, or dossier agents.
- Treat `unknown` as an evidence status. It is not a veto unless the indispensable implementation is illegal, unsafe, or directly contradicted.
- Any future use of shadow selectors for live routing or any validation of shadow-only candidates requires explicit user approval.

## Normative V2 execution contract

The machine contract for every newly registered run is `zt1-generation-run-v2`. The legacy boolean `matched_pilot` is not an authoritative V2 selector and must not be used to infer routing, arm type, cohort size, selection ownership, artifact scope, or validator eligibility. A V2 run selects exactly one `run_profile` before any discovery agent starts and never changes it in place.

### Required run fields

In the final `00a_context_and_resource_manifest.jsonl`, the first line is the sole `record_type: "run"` record and contains at least the typed fields below. Compatibility mirrors such as `status`, `matched_pilot`, `shadow_only`, and `validation_eligible` may remain during August migration, but they never select a V2 profile or override the authoritative fields.

```json
{
  "record_type": "run",
  "schema": "zt1-generation-run-v2",
  "run_id": "zero_to_one_candidates_...",
  "scope_id": "live-w01",
  "run_profile": "ordinary_audited_funnel",
  "arm": "live",
  "mode": "audited_funnel",
  "routing_state": "enabled",
  "cohort_kind": "initial",
  "wave_index": 1,
  "selection_policy": "root_orchestrator",
  "lifecycle_state": "complete",
  "started_at": "2026-08-22T12:01:00+02:00",
  "deadline_at": "2026-08-22T15:01:00+02:00",
  "ended_at": "2026-08-22T13:30:00+02:00",
  "model": "exact-model-id-and-version",
  "reasoning_effort": "exact-setting",
  "results_visibility": "available",
  "seed": "pre-registered-seed",
  "candidate_order_seed": "pre-registered-seed",
  "development_contract_path": "00b_development_contract.json",
  "development_contract_sha256": "lowercase-sha256-of-raw-file-bytes",
  "parent_scope_id": null,
  "declared_child_scopes": [],
  "file_read_log_complete": true,
  "tool_event_log_complete": true,
  "protected_files": [],
  "protected_blocks": [],
  "budgets": {"unique_queries":300,"uncached_input_tokens":10000000,"output_tokens":700000,"elapsed_minutes":180,"max_concurrency":3},
  "resource_totals": {"unique_queries":120,"uncached_input_tokens":900000,"output_tokens":90000,"elapsed_microseconds":5340000000}
}
```

All enum values are case-sensitive and closed:

- `run_profile` is exactly `ordinary_audited_funnel`, `operational_live_with_shadow`, or `v2_matched_nonrouting`;
- `arm` is exactly `live`, `shadow`, or `matched_baseline`;
- `mode` is exactly `audited_funnel` or `archipelago_lite_shadow`;
- `routing_state` is exactly `enabled` or `frozen_nonrouting`;
- `cohort_kind` is exactly `initial` or `regeneration`;
- `selection_policy` is exactly `root_orchestrator` or `isolated_two_stage`;
- `results_visibility` is `withheld` for a `frozen_nonrouting` scope and `available` for a routing-enabled live scope; later release is represented only by the parent timestamp defined below;
- `lifecycle_state` is exactly the final `state` in the applicable checkpoint chain defined below.

`run_id` and `scope_id` are immutable. `wave_index` is a positive integer; it is `1` for `cohort_kind: "initial"` and at least `2` for `cohort_kind: "regeneration"`. The run record is the final audited summary: `declared_child_scopes`, timestamps, completeness attestations, lifecycle mirror, and resource totals show the completed scope view. The append-only checkpoints remain the authoritative lifecycle and timing source; every summary field must reconcile to them, and the final run record cannot repair missing checkpoints. A run record that omits a required V2 field, uses an unknown enum value, or combines fields outside the allowed profile matrix fails closed.

`deadline_at` is the immutable planned deadline and only bounds execution. It is never evidence that execution ended. Before completion, `ended_at` is null unless the scope actually stops, in which case it is the actual offset-aware stop timestamp at or before the last reachable boundary. For a completed scope, `ended_at` equals the sole terminal `complete` checkpoint's `occurred_at`. The optional migration mirror `completed_at`, when present, equals that same terminal timestamp and is absent or null before completion. No field may invent a second terminal time or expand the event window after sealing.

`routing_state` has these semantics:

- `enabled` means the arm may become eligible for the unchanged downstream route only after its generation lifecycle is complete and its native audit passes. It does not claim evaluation or validation success.
- `frozen_nonrouting` is irreversible. No later checkpoint, timestamp, child run, or artifact rename can make that scope routing-eligible. A new explicitly approved experiment is required.

`cohort_kind` is exactly `initial` or `regeneration`. It describes generation lineage, not validator status.

### Closed run-profile matrix

#### `ordinary_audited_funnel`

- Root or regeneration scope: `arm: "live"`, `mode: "audited_funnel"`, `routing_state: "enabled"`, and `selection_policy: "root_orchestrator"`.
- An initial arm creates 40–60 unscored raw hypotheses, 10–20 researched directions, and 3–6 frozen finalists.
- It has no Archipelago child and makes no matched-parity claim.
- A regeneration arm uses the same ordinary ranges, has its own audit scope and seals, and obeys the regeneration rules below.

#### `operational_live_with_shadow`

- The root initial scope is `arm: "live"`, `mode: "audited_funnel"`, `routing_state: "enabled"`, and `selection_policy: "root_orchestrator"`.
- Its initial comparison cohort contains exactly 48 raw hypotheses, 12 completed Level-2 dossiers selected from 12–20 directions, one sealed six-direction fact-closure cohort, and the same six frozen finalists.
- It declares exactly one `arm: "shadow"` child scope with `run_profile: "operational_live_with_shadow"`, `mode: "archipelago_lite_shadow"`, `routing_state: "frozen_nonrouting"`, `cohort_kind: "initial"`, and `selection_policy: "isolated_two_stage"`.
- The shadow child produces exactly 36 problem cards, 36 direct concepts, six assumption inversions, six recombinations, 48 Level-1 concepts, 12 completed Level-2 dossiers, one sealed six-concept fact-closure cohort, and the same six shadow finalists.
- Only operational-live artifacts may proceed downstream. The shadow child cannot affect the live shortlist, routing, evaluation, regeneration, pivoting, judging, chat validation, or confirmation.
- Any later operational live regeneration is a separate `run_profile: "ordinary_audited_funnel"`, `cohort_kind: "regeneration"` scope outside the matched comparison; it uses the ordinary audited-funnel ranges and cannot declare a shadow child.

#### `v2_matched_nonrouting`

- The root initial scope is `arm: "matched_baseline"`, `mode: "audited_funnel"`, `routing_state: "frozen_nonrouting"`, and `selection_policy: "root_orchestrator"`.
- It creates exactly 48 raw hypotheses, 12 completed Level-2 dossiers selected from 12–20 directions, one sealed six-direction fact-closure cohort, and the same six baseline finalists.
- It declares exactly one `arm: "shadow"` child scope with `run_profile: "v2_matched_nonrouting"`, `mode: "archipelago_lite_shadow"`, `routing_state: "frozen_nonrouting"`, `cohort_kind: "initial"`, and `selection_policy: "isolated_two_stage"`.
- Both arms use the matched development contract and remain non-routing. Neither arm may contain or call an advisory evaluator, pivot, judge, panel, working/fresh/real chat, confirmation step, or regeneration wave.

No other run-profile/arm/mode/routing-state/cohort-kind combination is legal. Every `operational_live_with_shadow` and `v2_matched_nonrouting` root or child is `cohort_kind: "initial"`. Every `cohort_kind: "regeneration"` scope is exactly `ordinary_audited_funnel` / `audited_funnel` / `live` / `enabled` and has no shadow child. In particular, the presence of a shadow child never turns a `live` root into a `matched_baseline`, and `mode: "audited_funnel"` never determines routing state by itself.

### Lifecycle, cohort kind, and routing state

`lifecycle_state` follows one of these exact append-only checkpoint-state chains:

```text
registered -> raw_frozen -> history_frozen -> mapped -> cluster_audited
  -> level2_cohort_sealed -> level2_complete -> fact_closure_cohort_sealed
  -> closure_complete -> frozen -> complete

registered -> problem_cards_frozen -> direct_concepts_frozen
  -> transformations_frozen -> mapped -> level1_frozen
  -> provisional_order_sealed -> ballots_sealed -> level2_cohort_sealed
  -> level2_complete -> fact_closure_cohort_sealed -> closure_complete
  -> frozen -> complete
```

The second chain is required for `arm: "shadow"`; the first is used for audited-funnel scopes. A stopped or resource-exhausted run records the exact valid prefix it reached and audits `INCOMPLETE`; it does not invent a terminal lifecycle enum. A checkpoint audit assesses only that actually reachable prefix. It reports the causal admission or telemetry defect at the stopped stage and does not emit missing future child manifests, trust bundles, closure agents, finalist artifacts, seals, or dispositions as independent root causes. Conversely, any future-stage artifact that exists before its dispatch boundary is a real premature-materialization error. The first checkpoint establishes `registered`; after that, append-only checkpoint records are the sole state source. The final run-record lifecycle value is only a reconciled mirror of the last checkpoint.

`cohort_kind` is immutable. `level2_cohort_sealed`, `fact_closure_cohort_sealed`, and `frozen` checkpoints hash-bind the corresponding artifacts; there is no second cohort-state field. If an indispensable premise of a sealed closure candidate is contradicted, a sealed artifact changes, or an illegal substitution is attempted, the audit fails or remains incomplete at the last valid prefix. After fact-closure cohort sealing, no reserve, seventh candidate, renamed candidate, or new research allocation may replace a cohort member. Finalist freeze requires the exact same cohort and an external freeze seal.

`routing_state` is immutable after registration. An `enabled` scope becomes downstream-eligible only when `lifecycle_state: "complete"`, the `frozen` checkpoint and exact seal reconcile, and its native scope audit is `PASS`; no additional routing-state alias represents readiness. A `frozen_nonrouting` scope remains non-routing forever.

Routing cannot be inferred from filenames, directory placement, a human summary, or `validation_eligible`. Run and finalist compatibility booleans remain explicit and must agree with `routing_state`: enabled live finalists use `shadow_only: false` and `validation_eligible: true`; both non-routing arms use `shadow_only: true` and `validation_eligible: false`. The optional migration mirror `shadow_can_route_to_validation`, whenever present on any V2 run, is exactly `false`; ordinary runs may omit it, and no profile may use it to enable a shadow route.

### Declared child scopes and audit scope

The final parent run record's `declared_child_scopes` is the completed-audit view of every child, including any later regeneration. Every child namespace that this parent may own—including a future regeneration namespace—is pre-registered in the parent run record before the parent's pre-freeze snapshot and seal. Before any child agent starts, the coordinator records the same closed object with future final pins null; its offset-aware `registered_at` must be inside the parent window and strictly earlier than the child's first typed event. A child that was not present in that sealed registration view cannot later be adopted, used to prune parent ownership, or represented as part of the initial run. Existing checkpoint `artifacts` may hash-bind canonical-JSON registration/final snapshots when retained, but no child-specific manifest record type or alternate declaration schema exists. The child object has exactly these keys:

```json
{
  "scope_id": "shadow-w01",
  "relative_path": "shadow_archipelago_lite",
  "relationship": "shadow_child",
  "run_profile": "operational_live_with_shadow",
  "mode": "archipelago_lite_shadow",
  "arm": "shadow",
  "routing_state": "frozen_nonrouting",
  "cohort_kind": "initial",
  "manifest_sha256": "raw-byte-sha256",
  "development_contract_sha256": "same-raw-byte-sha256-as-parent-matched-arm",
  "protection_anchor_sha256": "independently-retained-digest",
  "freeze_seal_sha256": "independently-retained-digest",
  "audit_report_path": "shadow_archipelago_lite/10_native_audit_report.json",
  "audit_report_sha256": "raw-byte-sha256",
  "audit_status": "PASS",
  "model": "exact-model-id-and-version",
  "reasoning_effort": "exact-setting",
  "registered_at": "offset-aware-pre-dispatch-time",
  "results_visibility": "withheld"
}
```

`relationship` is exactly `shadow_child` or `regeneration`; `audit_status` is null before audit and then exactly `PASS`, `FAIL`, or `INCOMPLETE`; `results_visibility` is exactly `withheld` or `available`. A shadow child declares `results_visibility: "withheld"`; a routing-enabled regeneration declares `results_visibility: "available"`.

A pre-dispatch declaration sets final artifacts that do not yet exist—`manifest_sha256`, `freeze_seal_sha256`, `audit_report_path`, `audit_report_sha256`, and `audit_status`—to null. Its `development_contract_sha256` and `protection_anchor_sha256` must already be non-null and independently pinned. Its `registered_at` is inside the parent run window and strictly precedes the child `registered` checkpoint and every other child event. The parent pre-freeze snapshot contains every such declaration. The final run summary repeats the same closed child object with every final-artifact field non-null and the actual audit status. Fields that were non-null at registration must match byte-for-byte; previously null fields are filled exactly once and never revised. The final run record's child object must equal this final view. Composite audit cannot pass unless its `audit_status` is `PASS`. No child-object key may be added, aliased, or omitted. A genuinely later, unplanned regeneration must be a separately audited top-level scope tied to the initial seal; it cannot be retroactively inserted beneath a sealed parent or counted as an initial matched attempt.

In a final declaration, `manifest_sha256` is the raw-byte SHA-256 of the child's complete `00a_context_and_resource_manifest.jsonl` after its final `complete` checkpoint. `audit_report_path` is relative to the canonical parent run directory, begins with the exact `relative_path`, and resolves to a regular non-symlink file in that child scope. The closed trust entry repeats `audit_report_sha256` and `audit_status`, not `audit_report_path`.

The `relative_path` is unique, contains no `..`, resolves inside the canonical parent run directory, and has no symlink in any path component. Parent and child artifact scopes are disjoint. The parent scope audit excludes only fully declared, hash-bound child roots; an arbitrary or unregistered nested directory remains in parent scope and cannot hide an artifact. Each child is audited from its own canonical directory with its own manifest, ledger, protection anchor, freeze seal, and audit report.

After all declared scopes are sealed, create an external, exclusively created, independently digest-pinned `zt1-child-trust-bundle-v2`. Its top-level object has exactly the keys `schema`, `parent_scope_id`, and `children`, with `schema: "zt1-child-trust-bundle-v2"` and one `children` entry for every final child declaration. Each shadow entry has exactly this shape:

```json
{
  "scope_id": "shadow-w01",
  "protection_anchor_path": "/external/path/shadow_protection_anchor.json",
  "protection_anchor_sha256": "independently-retained-digest",
  "freeze_seal_path": "/external/path/shadow_freeze_seal.json",
  "freeze_seal_sha256": "independently-retained-digest",
  "manifest_sha256": "raw-byte-sha256",
  "development_contract_sha256": "raw-byte-sha256",
  "audit_report_sha256": "raw-byte-sha256",
  "audit_status": "PASS",
  "model": "exact-model-id-and-version",
  "reasoning_effort": "exact-setting",
  "results_visibility": "withheld",
  "live_arm_freeze_seal_path": "/external/path/live_freeze_seal.json",
  "live_arm_freeze_seal_sha256": "independently-retained-digest"
}
```

The two `live_arm_freeze_seal_*` fields are required and non-null only for the entry whose declaration has `relationship: "shadow_child"`; a regeneration entry omits both keys. Each trust entry repeats the declaration's exact scope, manifest, development-contract, protection, freeze, audit hash/status, model/effort, and visibility values. `relative_path` and `audit_report_path` remain in the declaration, not the closed trust entry. Every declared child must have `audit_status: "PASS"`, and the parent scope audit must also be `PASS`, before composite status can be `PASS`. A trust bundle cannot repair, replace, or re-sign an earlier anchor or seal.

### Run-scoped context packets

Use `fork_turns:"none"` for every creative, history-compression, cartography, audit, selector, and dossier agent. Run no more than three agents concurrently.

V2 context inventories are closed, not extensible labels. Every non-history agent declares exactly the applicable values from `founder_constraints`, `safety_legal`, and `neutral_evidence`; a history compressor declares exactly `history`. Unknown classes fail. Each `context_files` item has exactly `path` and `sha256`; its path is strict run-relative, regular, non-symlinked in every component, and scope-owned. The unique `allowlisted_files`, `files_read`, and `context_files.path` sets are equal, so an unrecorded read, unread supplied packet, unknown payload key, outside-run path, `/tmp` path, or hash mismatch blocks the next checkpoint. Every packet is content-scanned before dispatch; a filename allowlist alone is never proof of isolation.

Each mode also has a closed stage/role inventory. An audited-funnel scope has exactly five `generation` agents carrying the five registered live creative roles, followed only by the registered history-compressor, cartography, cluster-audit, and Level-1 roles, exactly twelve singleton `level2_researcher` agents, and exactly six singleton `fact_closure_researcher` agents when those lifecycle stages are reached; root-orchestrator selection is not replaced by a hidden selector agent. An Archipelago scope has exactly the six scout roles and the fixed builder, transformer, compressor, cartography, cluster-audit, Level-1, provisional-selector, two selector, challenger, exactly twelve singleton Level-2 agents, one finalist selector, and exactly six singleton fact-closure agents when reachable. Cross-mode stages, extra selector agents, unknown roles, aggregate development agents, and undeclared retry agents fail; a retry keeps the original typed role and identity.

Each agent receives one explicit, immutable packet. Every `context_files`, `allowlisted_files`, and `files_read` path is relative to that scope's canonical run directory, contains no `..`, resolves to a regular non-symlink file inside the scope, and has no symlink in any path component. Absolute paths, `/tmp`, sibling-scope paths, parent-scope paths, undeclared child paths, and paths that escape after canonical resolution are prohibited. Cross-scope material must be copied into a new run-scoped packet, stripped to its allowed neutral content, and hash-bound; agents never read another scope directly.

Record the packet raw-byte SHA-256 before launch. Packet bytes are immutable after launch. The packet manifest records role, arm, allowed and denied inputs, source hashes, exact model identifier/version, exact reasoning setting, assigned IDs, exact query/time/token cap, and launch timestamp. Provisional-selector, ranker, and challenger packet filenames, IDs, order, field completeness, and dossier depth must not reveal source island, transformation type, live-main selection state, or prior status.

Every bounded-return packet uses a path-bound instruction rendered separately from that packet's canonical output path and canonical scope run directory. Before rendering, the manager verifies that the output path is absolute, lexically canonical, and NFC-normalized; is a direct child of the scope-owned `agent_returns` directory; has no symlinked or aliased component; and does not already exist under any filesystem spelling. The packet itself must be an exact-spelling, single-link regular file read through a no-follow descriptor. The rendered packet contains the actual packet-specific absolute path, never a path placeholder, relative path, workspace-relative path, `..`, alias, or alternate spelling.

The path-bound instruction first declares this exact two-line patch header, with the packet's actual canonical absolute path after `*** Add File: `:

```text
*** Begin Patch
*** Add File: the packet-specific canonical absolute output path
```

It then requires this canonical long-form wrapper exactly:

```javascript
const patch = "<JSON-encoded complete patch beginning with the exact absolute header above>";
const result = await tools.apply_patch(patch);
text(result);
```

Immediately before dispatch, the manager or candidate runtime invokes the shared executable dispatch verifier and fails closed unless the immutable packet has exactly one absolute `Required return path` declaration, exactly one literal `*** Add File:` line with the same byte-for-byte path, exactly one canonical long-form wrapper, and no placeholder, relative alternative, second return declaration, second patch header, other file operation, or different path. Packet bytes must still match their precommit hash at that boundary. The verifier derives packet, output, precommit, agent, task, stage, and batch identities from the registered fixed role inventory and deterministic stage ordinal; mutable launch or precommit values are compared with those identities and never choose them. For manually dispatched Archipelago roles, passing this same verifier is a mandatory launch precondition. Parser support for the previously observed inline-await return remains a replay compatibility rule only; newly generated packets request only the canonical long form.

This path-bound rendering and pre-dispatch check is mandatory in Audited Funnel discovery, history compression, cartography, cluster audit, Level-1 normalization, Level-2, and fact closure, and in every Archipelago discovery/scout, direct-builder, inversion, recombination, history, cartography/mapping, cluster-audit, Level-1, provisional-selector, ranker, challenger, Level-2, finalist-selector, and fact-closure return packet.

### Allowed common content

- compressed founder facts and constraints;
- applicable safety and legal boundaries;
- maximum-search-latitude language;
- the role's source or transformation assignment;
- the neutral output schema;
- pre-registered resource caps;
- explicitly assigned problem, concept, or evidence IDs.

### Prohibited creative and selection content

- `Personalities/ZeroToOne.txt` or any validator/evaluator skill;
- validation criteria, factor names, weights, scores, thresholds, pass rates, or rankings;
- advisory, simulated-panel, or real-chat outputs;
- generator reasoning or another agent's conclusions;
- historical rejection rhetoric, proposed pivots, or score-bearing candidate records;
- full parent conversation or unrestricted repository access.

The history compressor is the only discovery-stage role allowed to read historical candidate artifacts. It must emit neutral fingerprints only and must not generate, rank, merge, reject, or select ideas.

Record every file actually read. Fail the integrity check when an agent reads a path outside its allowlist, a recorded hash no longer matches, a context packet is missing, or a prohibited validator/history file reaches a creative or selector stage.

### Development contract and matched parity

Every V2 scope contains the regular non-symlink run-local file `00b_development_contract.json`. It uses schema `zt1-development-contract-v2`; its path and the lowercase SHA-256 of its exact raw bytes appear in the run record as `development_contract_path` and `development_contract_sha256`. The file is created and pinned before the `registered` checkpoint, is never overwritten, and is included in the protection anchor, child declaration, freeze seal, and child trust bundle.

The implemented contract shape is:

```json
{
  "schema": "zt1-development-contract-v2",
  "contract_id": "matched-development-v2",
  "level2_sections": ["## Customer Loss And Payer Evidence","## Proposed Transaction And Paid Trigger","## Acquisition Route","## Incumbent Substitute And Route-Around","## Unit Economics And Sensitivity","## Control Point Or Compounding Asset","## Execution Dependencies And Cheapest Proof","## Decision-Critical Unknowns And Contradictions","## Evidence And Sources"],
  "frozen_sections": ["## Customer Loss And Payer Evidence","## Proposed Transaction And Paid Trigger","## Acquisition Route","## Incumbent Substitute And Route-Around","## Unit Economics And Sensitivity","## Control Point Or Compounding Asset","## Execution Dependencies And Cheapest Proof","## Decision-Critical Unknowns And Contradictions","## Evidence And Sources"],
  "evidence_statuses": ["verified","interpreted","counsel-required","unknown","contradicted"],
  "stage_query_caps": {"level2":12,"fact_closure":8},
  "aggregate_opportunity": {"raw":48,"level2":12,"fact_closure":6,"frozen":6,"discovery_queries":108,"level2_queries":144,"fact_closure_queries":48,"total_queries":300},
  "candidate_budgets": {
    "level2": {"uncached_input_tokens":112000,"output_tokens":20000,"elapsed_minutes":15},
    "fact_closure": {"uncached_input_tokens":96000,"output_tokens":20000,"elapsed_minutes":12}
  },
  "candidate_live_stop_thresholds": {
    "level2": {"uncached_input_tokens":92000,"output_tokens":11000,"elapsed_minutes":14},
    "fact_closure": {"uncached_input_tokens":76000,"output_tokens":11000,"elapsed_minutes":11}
  },
  "metering_monitor": {"poll_interval_milliseconds":1000,"controller":"blocking_direct_trace_monitor","trace_discovery":"recent_scope_scan_then_direct_path","interrupt_channel":"controller_result_to_root_collaboration_interrupt","stop_action":"interrupt_candidate_agent_and_fail_stage_admission","empirical_max_observed_uncached_token_event_jump":16633,"empirical_max_observed_output_token_event_jump":8204,"minimum_uncached_reserve_tokens":20000,"minimum_output_reserve_tokens":9000},
  "dossier_prose_word_ranges": {"level2":{"minimum":900,"maximum":1500,"minimum_per_section":75},"frozen":{"minimum":1100,"maximum":1800,"minimum_per_section":100}},
  "dossier_measurement": {"counted_sections":["## Customer Loss And Payer Evidence","## Proposed Transaction And Paid Trigger","## Acquisition Route","## Incumbent Substitute And Route-Around","## Unit Economics And Sensitivity","## Control Point Or Compounding Asset","## Execution Dependencies And Cheapest Proof","## Decision-Critical Unknowns And Contradictions"],"excluded_material":["title","section_headings","evidence_and_sources","source_ledgers","telemetry","machine_metadata"]},
  "fact_closure_schema": {"requires_decision_critical_evidence":true,"requires_pre_freeze_source_chain":true,"replacement_after_closure":false},
  "query_source_opportunity": {"query_requires_tool_event":true,"query_requires_source_open":true,"source_requires_bidirectional_evidence":true}
}
```

`stage_query_caps` is exactly `level2: 12` and `fact_closure: 8`. `candidate_budgets` has exactly `level2` and `fact_closure`; each stage has exact non-negative integer hard ceilings for `uncached_input_tokens`, `output_tokens`, and `elapsed_minutes`. `candidate_live_stop_thresholds` and `metering_monitor` are also exact. Before dispatching every batch, the blocking controller rechecks that the actual deadline still accommodates that batch, all later batches in the stage, and—at Level 2—the full fact-closure reservation. The root then starts the pinned blocking controller `monitor-development-batch`; the controller discovers only recent run-scoped traces, retains their direct paths, samples those paths every second without rescanning the session tree, and exits as soon as the batch completes or a still-running candidate reaches its lower boundary. The root waits on that controller process and immediately invokes the collaboration interrupt operation for every still-running task in its `abort_batch_task_names` result; `interrupt_task_names` separately identifies the exact threshold-crossing candidates. That controller result is the executable interrupt channel, not a request for the model to perform one-second shell polling. The reserve is larger than the largest observed provider token-event jump. An interrupt fails the stage admission; the higher final ceilings remain fail-closed admission checks. Both section lists are the same exact nine-heading inventory. `evidence_statuses` is exactly the complete typed taxonomy shown, including `unknown`, `contradicted`, and `counsel-required`. `dossier_prose_word_ranges` separately fixes Level-2 and frozen total depth and applies neutral floors of 75 and 100 words, respectively, to each of the first eight section bodies. `dossier_measurement` counts only persuasive bodies in those sections and explicitly excludes title, headings, Evidence And Sources, source ledgers, telemetry, and machine metadata. Structured traces never count as dossier prose. `fact_closure_schema` and `query_source_opportunity` are the exact closed objects shown. Scope/profile metadata may be added only if both matched files remain byte-identical; it is not needed for profile selection, which comes from the run record.

An ordinary or regeneration scope uses `contract_id: "ordinary-development-v2"`, the same implemented field names, and makes no parity claim. Its `aggregate_opportunity` is still a closed object with exactly the eight keys shown above. It records one exact preselected opportunity within the ordinary ranges: 40–60 raw hypotheses, 10–20 Level-2 directions, and 3–6 fact-closure candidates/frozen finalists, with `fact_closure == frozen`. `level2_queries` equals `level2 * 12`, `fact_closure_queries` equals `fact_closure * 8`, `discovery_queries` is the exact non-negative pre-registered discovery capacity, and `total_queries` is their exact sum. Actual cohort counts and allocation caps must reconcile to that object. For the initial comparison pair of `operational_live_with_shadow` or `v2_matched_nonrouting`, both scopes contain byte-identical contract bytes. Their `development_contract_sha256` values, child declaration hashes, and child trust-entry hashes therefore match exactly.

The matched contract fixes the following opportunity before either scope starts:

- 48 raw concepts, 12 Level-2 dossiers, six fact-closure candidates, and six frozen finalists per scope;
- 300 unique-query capacity per scope: 108 discovery, 144 Level-2, and 48 fact closure;
- audited-funnel discovery allocations `22/22/22/21/21`, assigned to the five roles by a pre-registered seeded permutation;
- Archipelago discovery allocations of 18 queries for each of six evidence scouts;
- 12 queries for every Level-2 dossier and eight queries for every sealed fact-closure entity;
- one isolated Level-2 agent per candidate, executed in batches of at most three, for exactly 12 agents and allocations per arm;
- one isolated fact-closure agent per candidate, also executed in batches of at most three, for exactly six agents and allocations per arm;
- 10,000,000 uncached input tokens, 700,000 output tokens, 180 minutes wall time, and maximum concurrency three per scope;
- the exact same model identifier/version and reasoning effort.

Exact opportunity fields, hard and live candidate boundaries, section/status schemas, model, reasoning effort, and concurrency are equality invariants; the 10% rule never relaxes them. Every development agent has singleton and identical `assigned_ids`, `output_ids`, allocation `entity_ids`, and `trace_entity_id`, plus a globally unique `trace_task_name`, its own run-local regular raw trace file, and raw-byte SHA-256. The pinned auditor parses that trace and reconciles task identity, model/effort, exact provider token totals, timestamps, call IDs, query text, and the source URL returned by each exact tool result. Reusing one task or trace, inventing a source URL from return prose, or dividing any multi-entity agent's aggregate resources after execution is not candidate-level proof and fails admission. The protection anchor binds the protocol, auditor, matched-run manager, and isolated candidate-development runtime. Unused query budget remains with its original allocation and is logged. It cannot be transferred or consumed as filler.

#### Budget calibration evidence and headroom

The August 23 failed aggregate Level-2 trace is immutable calibration evidence, not candidate attribution. Its exact provider totals were 133,083 uncached input tokens, 7,978 output tokens, 24 public web calls, and 267.301 seconds; the first token event alone used 10,867 uncached tokens, proving the old 10,000 cap infeasible before useful candidate research. Decomposition of that trace gives 25,502 non-research uncached tokens plus 107,581 across 24 calls. Therefore the direct call-scaled projections are 79,292.5 uncached tokens at twelve calls and 61,362.3333 at eight calls. The 112,000 and 96,000 hard ceilings provide 41.2524% and 56.4479% headroom. Their 92,000 and 76,000 live-stop thresholds retain 16.0255% and 23.8531% headroom over those projections while reserving 20,000 tokens before hard admission.

Same-model, same-reasoning isolated generation traces—not Level-2 observations—used 27,172–44,706 uncached tokens, 5,902–9,470 output tokens, and 2.6426833–4.53015 minutes over four-call turns. Conservatively scaling the slowest full turn gives 13.59045 minutes for twelve calls and 9.0603 minutes for eight, below the 15- and 12-minute ceilings. Across those traces and the failed aggregate trace, the largest observed provider-event jumps were 16,633 uncached tokens and 8,204 output tokens; the live-to-hard reserves are therefore 20,000 and 9,000. The 20,000 output hard ceiling is above the observed same-model maximum of 9,470 while the 11,000 live boundary permits that observed workload to finish. Output calibration remains lower-confidence because no exact isolated deep-dossier Level-2 or closure trace exists; this limitation must be reported. The next fresh run measures legitimate singleton distributions and may motivate a later pre-registered contract version; it may not rewrite caps in place. Maximum development reservation remains bounded at 1,920,000 uncached input tokens, 360,000 output tokens, and 84 batch-wall minutes per arm, within the unchanged equal aggregate arm caps.

Parity metrics are never declared by the run or development contract. The auditor derives exactly these nine metrics from certified manifest, ledger, dossier, and frozen-artifact records: `level2_queries`, `level2_sources`, `fact_closure_queries`, `fact_closure_sources`, `development_input_tokens`, `development_output_tokens`, `development_elapsed_minutes`, `level2_mean_words`, and `frozen_mean_words`. A source metric counts distinct normalized source URLs that participate in a certified reciprocal chain at that stage; reopening one URL under new event IDs does not inflate opportunity. URL normalization case-folds scheme and host, removes fragments and tracking-only query parameters such as `utm_*`, canonicalizes the remaining query ordering, and never treats tracking variants as distinct sources. Parse each derived non-negative value through its exact base-10 representation into arbitrary-precision `Decimal`. With live value `l` and shadow value `s`, compute without intermediate rounding:

```text
denominator = max(abs(Decimal(l)), abs(Decimal(s)))
relative_delta = abs(Decimal(l) - Decimal(s)) / denominator
```

Exactly 10% passes: parity holds when `relative_delta <= Decimal("0.10")`. A delta greater than 10%, non-exact metering, or an absent/zero denominator makes the comparison `INCOMPLETE`. A mismatched development-contract hash, mismatched fixed cap, or unequal exact opportunity field is a `FAIL`, not an incomplete measurement. Perform the test independently for all nine metrics; do not average metrics, round binary floats, substitute declared caps for measured use, or offset an overage with an underage elsewhere. Parity status never changes routing state or candidate merit.

### Stage checkpoints and retries

Every checkpoint is a boundary completion record with exactly these fields:

```json
{"record_type":"checkpoint","checkpoint_id":"CP-02-problem_cards_frozen","state":"problem_cards_frozen","predecessor_id":"CP-01-registered","occurred_at":"2026-08-21T12:22:30+02:00","completed_agent_ids":["scout-01","scout-02","scout-03","scout-04","scout-05","scout-06"],"file_read_log_complete":true,"tool_event_log_complete":true,"resource_totals":{"unique_queries":108,"uncached_input_tokens":720000,"output_tokens":36000,"elapsed_microseconds":1290000000},"artifacts":[{"path":"02b_raw_to_direction_ledger.jsonl","sha256":"raw-byte-sha256"}]}
```

`checkpoint_id` is unique. `predecessor_id` is null only for the first checkpoint and otherwise equals the immediately preceding checkpoint ID. `occurred_at` is offset-aware and strictly later than its predecessor. `completed_agent_ids` is the complete, duplicate-free inventory of agents that ended strictly before the boundary; it may be empty only at `registered`. `artifacts` is nonempty and contains exact run-owned, regular non-symlink relative paths plus raw-byte hashes. The `registered` checkpoint binds at least `00_run_manifest.md` and `00b_development_contract.json`.

Both completeness flags are true at every checkpoint and attest that file-read and tool-event logs are complete through that boundary. `resource_totals` contains exactly cumulative non-negative integers for `unique_queries`, `uncached_input_tokens`, `output_tokens`, and `elapsed_microseconds`. They reconcile all typed queries and completed-agent telemetry through `occurred_at`; elapsed microseconds equal the exact timestamp-derived run duration through that boundary. A checkpoint is not a budget estimate or eventual-completeness promise.

The audited-funnel chain is exactly:

1. `registered` — run manifest and development contract bound before agents;
2. `raw_frozen` — generation agents complete and raw hypotheses freeze;
3. `history_frozen` — neutral history fingerprints freeze;
4. `mapped` — every raw ID has exactly one mapping/disposition;
5. `cluster_audited` — cartography and anti-overmerge audit complete;
6. `level2_cohort_sealed` — the exact Level-2 cohort freezes before its research;
7. `level2_complete` — all selected dossiers and allocations reconcile;
8. `fact_closure_cohort_sealed` — `02d_fact_closure_candidates.json` fixes the closure cohort;
9. `closure_complete` — closure evidence and allocations reconcile without substitution;
10. `frozen` — the same finalist artifacts are fixed and must reconcile to the external freeze seal;
11. `complete` — all scope telemetry and any final child declarations reconcile.

The Archipelago shadow chain is exactly `registered`, `problem_cards_frozen`, `direct_concepts_frozen`, `transformations_frozen`, `mapped`, `level1_frozen`, `provisional_order_sealed`, `ballots_sealed`, `level2_cohort_sealed`, `level2_complete`, `fact_closure_cohort_sealed`, `closure_complete`, `frozen`, `complete`. No other state or reordered/duplicated boundary is legal. `lifecycle_state` equals the final checkpoint `state`; a final audit requires `complete`, while an exact valid prefix is `INCOMPLETE`.

For Archipelago, all problem scouts finish before direct construction/history compression; direct concepts finish before transformation; transformation and history compression both finish before cartography; cartography precedes overmerge audit and Level-1; provisional selection precedes rankers/challenger; all ballots precede Level-2; Level-2 precedes isolated finalist selection; closure selection precedes fact closure; fact closure precedes freeze. Audited-funnel arms omit Archipelago-only checkpoints and enforce generation → history compression → cartography → cluster audit → Level-1 → Level-2, followed by fact closure and freeze. Every predecessor agent must end strictly before every successor agent starts, and the predecessor stage must finish before the successor's reachable checkpoint boundary.

Retries preserve the same assignment, allocation, entity, and output IDs; consume the original resource cap; and record the failed attempt and exact metering. A retry cannot create an extra concept, selector ballot, dossier, closure entity, or validator opportunity. Missing or reversed checkpoints make the run `INCOMPLETE` or `FAIL`; state is never inferred from file modification times.

A failed Level-2 or fact-closure admission stops at the last real sealed checkpoint. The run records an actual `ended_at` plus a manifest-bound `10_{stage}_admission_failure.json`; it does not append a failed checkpoint or synthesize an agent, allocation, dossier, closure cohort, child, snapshot, or seal. The receipt binds the typed primary cause, actual stop time, hash-bound pre-stage manifest and ledger, original precommits/returns, any exact copied causal raw trace bytes, any partially materialized canonical stage artifacts, and any genuinely present future lifecycle artifact. It explicitly records that no telemetry reconstruction occurred. The auditor authenticates that receipt and reports its primary cause; a checkpoint request beyond the stopped prefix does not add absent future artifacts as independent root causes. A stopped run is immutable and cannot be resumed.

`--checkpoint` audits the evidence available immediately before the named advancement; it does not require evidence that can exist only after that advancement. The exact minimum lifecycle boundaries are `level2_complete` before `selection`, `closure_complete` before `freeze`, `frozen` before `shadow-dispatch`, and `complete` before `evaluation`. For an authenticated admission stop, the auditor evaluates the actually reachable prefix and reports the receipt's primary cause without a redundant `CHECKPOINT_STATE_NOT_REACHED`. A checkpoint result permits advancement only when the audit status is exactly `PASS`; both `INCOMPLETE` and `FAIL` block.

`shadow-dispatch` is a special pre-dispatch composite-prefix audit and is valid only for the initial root of `operational_live_with_shadow` or `v2_matched_nonrouting`. The current parent manifest must still be the sealed pre-freeze snapshot view: its checkpoint chain ends at `frozen`; its live development telemetry, read/tool attestations, resource totals, finalist bytes, protection anchor, manifest snapshot, and independently pinned external live freeze seal all reconcile; no agent remains active. The root contains exactly one safely rooted, non-overlapping, pre-registered shadow declaration with the required shadow profile/mode/arm/routing/cohort, exact parent model and effort, byte-identical matched development-contract hash, independently pinned non-null child protection-anchor hash, non-null registration time strictly before the parent `frozen` boundary, and `results_visibility: "withheld"`. The child fields that cannot truthfully exist before execution—`manifest_sha256`, `freeze_seal_sha256`, `audit_report_path`, `audit_report_sha256`, and `audit_status`—remain null.

The pre-dispatch invocation supplies the child's already-created external anchor and independent digest as the paired inputs `--child-protection-anchor` and `--child-protection-anchor-sha256`. Supplying neither, only one, a symlink, an in-run path, non-canonical JSON, or mismatched bytes blocks dispatch; these inputs are rejected outside `--checkpoint shadow-dispatch`. The payload uses the exact closed `zt1-protection-anchor-v2` schema and its digest equals the sealed declaration's `protection_anchor_sha256`. Its `run_id`, `scope_id`, and canonical `run_dir` identify the reserved child; `created_at` is strictly earlier than the declaration's `registered_at`; its development-contract path/hash matches the declaration; and its workflow-file, fixed-contract, and protected Validation Gates block pins all match the required canonical bytes. This check validates the pre-existing external anchor without requiring the not-yet-materialized child contract file.

The pre-dispatch gate neither accepts nor requires a child trust bundle, child freeze seal, child audit report, or child machine manifest. The reserved child directory may contain only preregistration material needed to bind its development contract; a child run record, checkpoint, agent, allocation, query, tool/source event, finalist, final seal, audit report, or other execution artifact before the gate fails. An unsafe, absolute, `..`-containing, overlapping, or symlinked child path fails without reading escaped content. A missing or late declaration, absent or mismatched child-anchor payload or protection/development pin, missing parent seal, incomplete telemetry, active agent, already materialized child execution, or any shadow event at or before the gate blocks dispatch. After dispatch, ordinary final/composite audit rules require the child manifest, child seal, recursive child `PASS`, finalized declaration, and independently pinned child trust bundle; the prefix exception cannot be used to certify or route a completed child.

## Stable identifiers

Use immutable IDs from first creation:

- problem cards: exactly `P-<island>-01` through `06` for each registered island;
- direct concepts: `D-NNN`;
- inversion concepts: `I-NNN`;
- recombination concepts: `X-NNN`;
- economic directions: `DIR-NNN`;
- clusters: `CL-NNN`;
- evidence: `EV-NNNN`;
- finalists: `FIN-NN`.

Renaming a title never changes an ID. A material pivot receives a new concept or direction ID and records its parent. Every raw ID must map exactly once to a direction or to an explicit unresolved/rejected disposition. Never silently delete a cluster member.

## Archipelago-Lite stages

### 1. Six independent evidence scouts

Run two batches of three scouts. Each returns exactly six problem cards and no business solution.

1. `customer_workarounds` / role `evidence_scout_customer_workarounds` — customer language, support forums, repeated manual work, avoidance behavior, and costly improvisation.
2. `spend_procurement` / role `evidence_scout_spend_procurement` — actual budgets, tenders, pricing, chargebacks, claims, purchasing language, and payment evidence.
3. `operational_failure` / role `evidence_scout_operational_failure` — queues, downtime, bottlenecks, lead times, missed service levels, shortages, and recurring loss events.
4. `incumbent_economics_channels` / role `evidence_scout_incumbent_economics_channels` — cross-subsidy, conflicts, commissions, switching, fragmented supply, route-to-market, and procurement authority.
5. `technical_scientific_change` / role `evidence_scout_technical_scientific_change` — capability, accuracy, interoperability, cost, or infrastructure changes that alter what is feasible.
6. `rules_finance_assets_transitions` / role `evidence_scout_rules_finance_assets_transitions` — binding changes, financing discontinuities, stranded assets, and institutional transitions.

Only the sixth scout starts from regulation. Other scouts may record a rule encountered, but may not use regulation as their mandatory search grammar.

Each problem card contains:

- actor and desired outcome;
- observable loss event, frequency, and magnitude status;
- current workaround or substitute;
- payer or budget evidence;
- evidence sources and dates;
- contradictory evidence;
- unresolved unknowns;
- source-island ID.
- creator agent ID and evidence IDs whose `entity_ids` explicitly include that card. At least one linked source-open record must reciprocally name the same card and evidence ID.

Do not include a solution, moat, score, validator term, compulsory control instrument, or founder-wealth arithmetic in a problem card.

### 2. Neutral history compressor

Run only after all 36 problem cards are frozen. For each historical shape, emit:

- customer;
- loss event;
- payer;
- solution primitive;
- transaction unit or paid trigger;
- acquisition route;
- possible compounding asset;
- status: `confirmed`, `unvalidated`, `rejected`, or `unknown`;
- source artifact IDs.

Strip scores, thresholds, evaluator prose, colorful rejection language, and proposed remedies. Preserve unvalidated champions as `unvalidated`; do not recast them as winners or failures.

### 3. Direct concept builders

Use three isolated builders. Give each twelve problem cards and no browsing, history, peer output, or validator context. Produce one direct concept per card, for 36 total.

The three `assigned_ids` lists partition the 36 problem IDs exactly once. Each builder's twelve `output_ids` equal the twelve mapping records carrying its `creator_agent_id`; each direct mapping has exactly one assigned problem parent.

Each concept records:

- parent problem ID;
- buyer, payer, and desired outcome;
- value-capture event;
- delivery primitive;
- initial acquisition route;
- possible compounding asset;
- first falsifiable assumption;
- safety/legal boundary;
- evidence and hypothesis IDs.

Do not require title, exclusivity, options, reserves, custody, or another shared solution grammar.

### 4. Transformation agents

Use four isolated agents after the direct concepts are frozen:

- two assumption-inversion agents, three concepts each;
- two cross-domain recombination agents, three concepts each.

An inversion must name the inverted assumption—payer, owner, timing, channel, transaction unit, geography, financing, liability, or make/buy boundary—and explain the causal benefit and new risk.

A recombination must cite at least two parent problem or direct-concept IDs from nonadjacent evidence islands, identify the economic mechanism transferred, and state where the analogy breaks. Cosmetic renaming does not count.

Each transformer records assigned parent IDs, exactly three output IDs, and `creator_agent_id` on each corresponding mapping. Inversion mappings use a structured `operation` with `dimension`, `assumption`, `causal_benefit`, and `new_risk`. Recombination mappings use `transferred_mechanism` and `analogy_break`; the auditor derives parent islands from the actual ancestry rather than trusting a declared island label.

The 36/6/6 allocation is a first-pilot treatment, not a permanent optimum or finalist quota.

### 5. Reversible semantic cartography

Use one cartographer and one anti-overmerge auditor. Compare concepts using:

- customer and loss event;
- payer and budget;
- paid trigger;
- transaction owner;
- acquisition/distribution route;
- compounding asset.

A similarity model or heuristic may propose neighbors but cannot delete a concept. Different payer, paid trigger, transaction owner, or route normally remains a sibling, not a merge. Every merge needs a field-by-field rationale. The auditor challenges every cluster with more than three members and every proposed merge with a field mismatch.

Report cluster membership, all raw members, nearest historical fingerprints, disagreements, and effective concept count.

### 6. Equal-field Level-1 cards

Normalize all 48 concepts to the same fields and evidence opportunity. Do not impose identical persuasive prose or a numeric score.

Required fields:

- problem and payer evidence;
- proposed transaction and paid event;
- current workaround and why it persists;
- initial acquisition route;
- possible compounding mechanism;
- decisive assumptions and contradictions;
- cheapest falsification;
- founder-constraint tension;
- sources;
- explicit `unknown` fields.

Remove author, island, transformation label, prior status, and selection outcome from masked selector packets.

### 7. Shadow selection

Dispatch two masked rankers and one tail-recall challenger independently:

- Ranker 1: evidence-supported commercial potential.
- Ranker 2: founder-accessible economics and compounding.
- Challenger: high-upside omissions and premature feasibility filtering.

First dispatch one fresh `provisional_selector` with `fork_turns:"none"`. It receives the 48 masked Level-1 cards, neutral founder constraints, and the pre-registered main decision rule—but no validator files or language, scores, thresholds, detailed history, author/island/type labels, or live selections. It returns an ordered 48-ID list. The root writes and hashes the first six as `main_provisional_ids` and the remaining 42 as `ordered_reserve`; it does not reinterpret the order.

Do not average scores, use majority voting, or reveal one output to another role. Lists remain separate. The sealed provisional order must exist before ranker or challenger dispatch; the already-frozen live choices remain unaffected. The `near-cutoff` sentinel comes from that sealed reserve, never from a post-selector choice.

Each ranker and the challenger returns an ordered list of six plus concise evidence and counterevidence. Pre-register a seeded permutation of the three lists. Fill the three selector/challenger Level-2 slots by round-robin through that permutation, taking the next unique candidate not already in the main six. Do not merge or average their judgments.

### 8. Twelve Level-2 dossiers

Allocate the fixed twelve shadow slots as follows:

- six isolated provisional-selector choices (retaining the machine label `main_provisional` for the pre-registered baseline rule);
- up to three unique ranker or challenger nominations;
- one uniformly seeded rejected concept;
- one seeded near-cutoff concept;
- one cluster singleton or concept from an under-selected evidence island.

When categories overlap, fill the vacancy with the next unique pre-ranked candidate from the same category, then the next unique seeded candidate. Never add a thirteenth dossier. Sentinels consume existing shadow slots and add no validation calls.

Define the sampling categories before unblinding:

- `rejected` — omitted from the main six and all three ordered selector/challenger lists; if that set is empty, use the seeded non-main remainder and record the fallback.
- `near-cutoff` — the highest pre-frozen main rank below the main six that is not already selected.
- `singleton` — the seeded candidate from a one-member semantic cluster; if none exists, use a candidate from the evidence island with the fewest Level-2 representatives, breaking ties by seed.

If a selector list supplies fewer than three unique additions, first exhaust the other pre-registered selector lists, then fill from the seeded non-main remainder. After all category-specific fallbacks, any remaining vacancy is filled from the seeded unused concept IDs. Preserve the intended slot category (`selector_or_challenger`, `rejected`, `near_cutoff`, or `singleton`) and record the fallback in a separate `backfill_reason` field. This keeps the machine-checkable category totals at 6/3/1/1/1 while fixing the Level-2 total at 12 without duplicate concepts or extra attempts.

Dispatch twelve fresh isolated Level-2 agents in four batches of at most three. For each batch, start its blocking controller before spawning the agents, wait on the controller rather than manually polling, and interrupt the returned task identities before any later integration. Each agent receives exactly one candidate-owned packet and may use up to twelve useful research calls. Give each dossier identical research opportunity focused on:

- payer denominator and budget/willingness proxy;
- closest substitute and incumbent route-around;
- realistic price, cost, capital, and sensitivity ranges;
- first-customer route;
- critical dependencies;
- exact rights or access claimed;
- contradictory evidence;
- cheapest private proof for public unknowns.

Every Level-2 ledger record binds `selected_at`, `completed_at`, `development_status`, exact dossier path, and SHA-256. `complete` requires a nonempty, non-symlink, concept-ID-bound dossier with the exact standardized headings `Customer Loss And Payer Evidence`, `Proposed Transaction And Paid Trigger`, `Acquisition Route`, `Incumbent Substitute And Route-Around`, `Unit Economics And Sensitivity`, `Control Point Or Compounding Asset`, `Execution Dependencies And Cheapest Proof`, `Decision-Critical Unknowns And Contradictions`, and `Evidence And Sources`; dossier paths and content hashes are unique. The counted persuasive bodies of the first eight sections contain 900–1,500 words total and at least 75 words per section. Completion must follow selection and precede the finalist selector. An `early_stop` is allowed only with `illegal_or_unsafe_indispensability` or `directly_falsified_premise`, cannot enter fact closure or freeze as a finalist, and leaves unused query budget logged rather than transferred.

After Level-2 research, dispatch one fresh isolated `finalist_selector` with `fork_turns:"none"`. It receives the twelve masked Level-2 dossiers, neutral founder constraints, and a pre-registered decision schema—but no validator/history material, selection categories, source-role labels, or root conclusions. It returns an ordered six-ID fact-closure cohort. The root writes and hashes `02d_fact_closure_candidates.json` without changing the order.

Dispatch six fresh isolated fact-closure agents in two batches of at most three. Give each of those exact six candidates capacity for up to eight useful final fact-closure queries and record the evidence timestamps; unused capacity remains logged and must not induce filler. Each frozen dossier uses the same nine-section schema and contains 1,100–1,800 counted persuasive words across the first eight sections, with at least 100 words in each section. Matched shadow mode permits no post-closure substitution: if closure evidence directly contradicts an indispensable premise, mark the run incomplete and do not replace the candidate from an unresearched reserve. Otherwise those same six, and only those six, receive `frozen_at`. The final six remain shadow artifacts only.

## Pre-freeze evidence closure

Before a live or shadow finalist freezes, record bounded research on the most decision-critical assumptions, including where relevant payer existence, denominator, first-contract authority, access/right availability, route-around risk, capital exposure, and a direct budget or willingness proxy.

Every evidence record needs:

- immutable evidence ID;
- linked direction or concept IDs;
- proposition;
- source URL or artifact;
- source date when known;
- `recorded_at` timestamp;
- status: `verified`, `interpreted`, `counsel-required`, `unknown`, or `contradicted`;
- whether it is decision-critical;
- cheapest resolving test.

### Complete causal telemetry chain

Every consequential evidence proposition and every frozen finalist must be reachable through one complete typed chain:

```text
development contract
  -> agent assignment
  -> allocation
  -> query
  -> query tool_event
  -> source_open
  -> evidence
  -> raw/problem ancestry
  -> completed Level-2 dossier
  -> sealed closure cohort
  -> fact-closure evidence
  -> finalist ledger record
  -> external freeze seal
```

The minimum reciprocal keys are:

- `agent.agent_id`, `scope_id`, `arm`, `stage`, `assigned_ids`, `output_ids`, model/effort, interval, exact metering basis, and resources;
- `allocation.allocation_id`, `agent_id`, `scope_id`, `arm`, `stage`, `entity_ids`, `query_cap`, `used_unique_queries`, `unused_queries`, offset-aware `created_at`, exact metering basis, and resources;
- `query.query_id`, `allocation_id`, `agent_id`, `scope_id`, `arm`, `stage`, normalized query text, `entity_ids`, and `occurred_at`;
- `tool_event.call_id`, `query_id`, `allocation_id`, `agent_id`, `scope_id`, `arm`, `stage`, exact tool name, event type, and `occurred_at`; the implemented research vocabulary is exactly `tool: "web_search"` and `event_type: "tool_call"`;
- `source_open.source_event_id`, `query_id`, `call_id`, `allocation_id`, `agent_id`, `scope_id`, `arm`, `stage`, URL, `entity_ids`, `evidence_ids`, and `occurred_at`;
- `evidence.evidence_id`, `source_event_ids`, `allocation_id`, `agent_id`, `scope_id`, `arm`, `stage`, `entity_ids`, direction/concept ID, proposition, status, decision-critical flag, and `recorded_at`;
- Level-2, closure, finalist, and seal records that name the exact upstream IDs and artifact hashes.

Every forward link has a matching reverse link. IDs, scope, stage, allocation, agent, and entity membership must agree at every hop. Required timestamp order is:

```text
allocation created_at < agent start <= query < tool_event < source_open
            < evidence recorded_at <= agent end < applicable completion checkpoint
Level-2 selected_at <= Level-2 evidence <= Level-2 completed_at < level2_complete checkpoint
fact-closure cohort selected_at < first closure query <= closure evidence
            <= finalist frozen_at < seal sealed_at
```

An event owned by an agent must fall inside that agent's exact interval. Every V2 tool event belongs to exactly one known query and allocation; there is no unlinked, neutral, harmless, messaging, external-call, or alternate-tool escape hatch. A source without a typed query and tool event, a query without an allocation, evidence without a reciprocal source, a finalist without decision-critical pre-freeze evidence on its own sealed entity/direction, or any cross-arm/stage mismatch fails. Evidence IDs never count as affected entity IDs and cannot certify their own ancestry. Later evidence is a versioned update and cannot be backdated into the sealed chain. `contradicted` remains valid, explicit development evidence, but contradicted evidence alone cannot satisfy a frozen finalist's decision-critical support requirement; that scope remains `INCOMPLETE` without another qualifying linked proposition. Lack of public evidence remains `unknown`, not an automatic rejection.

### Exact metering and caps

All query and token counters used for V2 completion or parity are exact non-negative integers. Tokens are provider-reported uncached input and output counts from the candidate-owned raw trace. During each development batch the pinned blocking controller writes one snapshot per second from cached direct trace paths, and its process result is the root's interrupt channel. The root waits for that result and immediately interrupts every still-running task named by `abort_batch_task_names`; `interrupt_task_names` records which candidate or candidates actually crossed a threshold. Integration rejects a missing/gapped meter log or any crossed live threshold. The auditor independently replays every snapshot against provider token-event timestamps and exact partial cumulative counters in the final raw traces. Agent, allocation, checkpoint, and run `resources` use exact non-negative integer `elapsed_microseconds`, reconciled without a floating-point round trip to offset-aware start/end timestamps. The contract's `elapsed_minutes` values remain integer caps only. Query totals come from typed query records with matching tool and source events. Maximum concurrency is derived from exact agent intervals using end-before-start ordering for equal timestamps.

Each agent and allocation record declares top-level `metering_basis` as exactly `tool_reported` or `trace_derived_exact`, with `resources` containing exactly `uncached_input_tokens`, `output_tokens`, and `elapsed_microseconds`. Allocation resource sums equal the owning agent resources, and every agent's elapsed value equals its timestamp-derived active duration. For Level-2 and fact closure, equality is direct because each agent owns exactly one allocation and entity; summing or dividing an aggregate multi-entity trace is forbidden. Estimates, reconstructed counters, prose-derived numbers, rounded timestamps, or `unknown` metering cannot support `lifecycle_state: "complete"` or matched parity; the scope is `INCOMPLETE`. Do not replace a missing exact counter with zero.

Run totals must equal the exact sum or specified derivation from their constituent records. `used_unique_queries + unused_queries == query_cap` for every allocation. Normalize query uniqueness by Unicode-preserving case-folding and whitespace collapse. Retries and repeated identical queries consume tool and elapsed budget but count once toward the unique-query cap. No web-query budget is assigned to history compression, concept construction, transformation, clustering, masking, ranking, or selection; those stages still record exact token and elapsed metering with zero query allocations.

The matched caps and deterministic allocations are defined by the byte-identical development contract above. Ordinary audited-funnel caps are pre-registered in its own development contract. A declared cap that differs from the applicable contract is `FAIL`; a missing counter or unreconciled total is `INCOMPLETE`. Neither condition may redefine the run.

Log unused budget; never transfer it to a favored idea. A candidate-specific early stop is permitted only when an indispensable premise is illegal, seriously unsafe, or directly contradicted. It records the typed stop reason and exact unused allocation, cannot enter fact closure or freeze, and cannot be replaced in a matched sealed cohort.

### Audit outcome classification

Classify contract validity separately from telemetry completeness:

- `FAIL` means a native V2 schema or invariant is false: an unknown/aliased field or enum, illegal profile tuple, mismatched development-contract bytes or hash, mismatched fixed cap or exact opportunity, causal-ID contradiction, cross-scope exposure, routing violation, or protection/seal mismatch.
- `INCOMPLETE` means the V2 contract is otherwise compatible but proof is unavailable or development parity is outside its approved completion band: a required checkpoint or reciprocal event is missing, metering is not exact, a required denominator is absent or zero, any measured parity delta is greater than 10%, resource exhaustion occurs, or totals cannot reconcile.
- `PASS` requires every native scope check, every required child audit, all exact metering and parity comparisons, the integration isolation check, and the final trust bundle to pass. One status cannot mask another scope's failure or incompleteness.

Do not label a completed V1 artifact a genuine telemetry failure merely because it lacks fields first required by `zt1-generation-run-v2`. That is a schema/version incompatibility and remains outside native V2 PASS eligibility. A historical replay reports real V1 telemetry failures only where the frozen V1 contract required the missing or contradictory evidence; it never backfills V2 proof.

## Machine-readable audit artifacts

### Externally pinned snapshots

#### V1 identities remain frozen

`zt1-fixed-v1` is a historical composite identity and must never be edited, redefined, or rebaselined. Its legacy IDs remain bound to the exact canonical paths and hashes recorded by each V1 anchor: founder profile, communication/success/safety contract, goal, validator, orchestration prompt, generator skill, evaluator skill, and pivot skill, plus the raw-byte `validation-gates` block from the `## Validation Gates` marker inclusive to the `## Workflow` marker exclusive. A same-suffix copy elsewhere is not a live canonical contract.

V2 does not claim that an evolved whole orchestration prompt or generator skill still matches the V1 whole-file hash. It preserves the immutable founder/validator identities and exact validation-gates block while versioning workflow files separately.

#### `zt1-protection-anchor-v2`

Before `started_at` and the `registered` checkpoint, exclusively create a regular non-symlink external anchor and retain its canonical-JSON SHA-256 independently:

```json
{
  "schema": "zt1-protection-anchor-v2",
  "run_id": "zero_to_one_candidates_...",
  "scope_id": "live-w01",
  "run_dir": "/canonical/scope/path",
  "created_at": "offset-aware-pre-run-time",
  "contract_profile": "zt1-fixed-v1",
  "workflow_profile": "zt1-auditor-workflow-v2",
  "development_contract_path": "00b_development_contract.json",
  "development_contract_sha256": "raw-byte-development-contract-sha256",
  "block_semantics": "raw-bytes,start-inclusive,end-exclusive,unique-markers-v1",
  "files": [
    {"id":"validator","path":"/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt","sha256":"current-exact-hash"},
    {"id":"orchestration-prompt","path":"/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_AGENT_PROMPT.md","sha256":"current-exact-hash"},
    {"id":"generator-skill","path":"/Users/igor/.codex/skills/generate-zero-to-one-candidates/SKILL.md","sha256":"current-exact-hash"}
  ],
  "blocks": [
    {"id":"validation-gates","path":"/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_AGENT_PROMPT.md","start_marker":"## Validation Gates","end_marker":"## Workflow","sha256":"exact-v1-block-hash"}
  ],
  "workflow_files": [
    {"id":"blind-search-protocol","path":"/Users/igor/.codex/skills/generate-zero-to-one-candidates/references/blind-search-protocol.md","sha256":"current-whole-file-hash"},
    {"id":"audit-funnel","path":"/Users/igor/.codex/skills/generate-zero-to-one-candidates/scripts/audit_funnel.py","sha256":"current-whole-file-hash"},
    {"id":"v2-candidate-development","path":"/Users/igor/Desktop/discussion_panel/utilities/v2_candidate_development.py","sha256":"current-whole-file-hash"},
    {"id":"v2-matched-experiment-manager","path":"/Users/igor/Desktop/discussion_panel/utilities/v2_matched_experiment_manager.py","sha256":"current-whole-file-hash"}
  ]
}
```

The anchor is a closed schema. Its top-level keys are exactly those shown; every `files` and `workflow_files` entry has exactly `id`, `path`, and `sha256`; every `blocks` entry has exactly `id`, `path`, `start_marker`, `end_marker`, and `sha256`. Extra routing, eligibility, trust, alias, or extension fields fail even when the altered JSON is re-pinned. The V2 anchor's `files` array uses the complete production fixed-path set, not only the illustrative entries shown. A fresh V2 anchor pins the current prompt and skill bytes for that future run; it does not rewrite the older V1 anchor or claim those whole files still equal their historical hashes. The raw-byte Validation Gates block and unchanged founder/validator files remain protected invariants. `workflow_files` is the exact closed production set `blind-search-protocol`, `audit-funnel`, `v2-candidate-development`, and `v2-matched-experiment-manager` under `zt1-auditor-workflow-v2`; any byte change requires a fresh future-run anchor. `development_contract_path` is the exact run-relative regular non-symlink contract path and its digest equals both the run record and the actual bytes before registration. A historical whole-file mismatch is reported as `SUPERSEDED`, while a changed protected founder/validator file or Validation Gates block is `FAIL`.

Every referenced canonical file is a regular non-symlink at its exact canonical path. The run-local development contract is also a regular non-symlink, resolves inside the scope, and matches the run record. Both the manifest-local pre/post hashes and the external anchor hashes must agree. A later or mutable manifest hash cannot replace the independently pinned anchor.

#### `zt1-freeze-seal-v2`

After the exact finalist cohort freezes, exclusively create and independently pin a V2 seal:

```json
{
  "schema": "zt1-freeze-seal-v2",
  "run_id": "zero_to_one_candidates_...",
  "scope_id": "live-w01",
  "run_dir": "/canonical/scope/path",
  "run_profile": "operational_live_with_shadow",
  "arm": "live",
  "mode": "audited_funnel",
  "routing_state": "enabled",
  "cohort_kind": "initial",
  "wave_index": 1,
  "selection_policy": "root_orchestrator",
  "seed": 20260822,
  "candidate_order_seed": 20260823,
  "parent_scope_id": null,
  "matched_pilot": true,
  "protection_anchor_sha256": "independently-pinned-anchor-digest",
  "development_contract_sha256": "raw-byte-development-contract-sha256",
  "results_visibility": "available",
  "manifest_snapshot_path": "00c_pre_freeze_manifest_snapshot.jsonl",
  "manifest_snapshot_sha256": "raw-byte-pre-freeze-manifest-sha256",
  "model": "exact-model-id-and-version",
  "reasoning_effort": "exact-setting",
  "sealed_at": "offset-aware-in-window-time",
  "finalists": [
    {"finalist_id":"FIN-01","arm":"live","artifact_path":"finalist_example.md","frozen_at":"offset-aware-time","sha256":"exact-file-sha256"}
  ]
}
```

The seal is also a closed schema. Its top-level keys are exactly those shown. `parent_scope_id` is null for a root seal and is the exact owning scope ID for a shadow or regeneration child. A shadow seal additionally has exactly `live_arm_freeze_seal_sha256`; a regeneration seal additionally has exactly `initial_freeze_seal_sha256`. Each finalist entry has exactly `finalist_id`, `arm`, `artifact_path`, `frozen_at`, and `sha256`. Extra routing, eligibility, override, or extension fields fail even when the altered seal is re-pinned. `matched_pilot` is an August migration mirror emitted by the current compatibility layer. It must agree with the typed profile but never selects or overrides `run_profile`, `arm`, or `routing_state`.

Immediately before creating the external seal, exclusively create the run-local regular non-symlink `00c_pre_freeze_manifest_snapshot.jsonl` as a byte-for-byte copy of the scope's then-current `00a_context_and_resource_manifest.jsonl`. It has no JSON wrapper, canonicalization, filtering, or newline conversion. `manifest_snapshot_path` is exactly `00c_pre_freeze_manifest_snapshot.jsonl`; `manifest_snapshot_sha256` is the lowercase SHA-256 of those raw copied bytes. The snapshot is immutable after exclusive creation. The seal binds this snapshot, never the later final machine manifest.

The V2 seal graph is acyclic and has this exact order:

1. Finish the root live finalist bytes and pre-freeze telemetry, copy its current manifest bytes to `00c_pre_freeze_manifest_snapshot.jsonl`, then exclusively create and independently pin the external root live seal.
2. Only after the live seal exists and the pre-dispatch `--checkpoint shadow-dispatch` audit returns `PASS` may a shadow child be dispatched. That gate uses the sealed parent prefix and pre-registered null-finalization child declaration; it occurs before the child machine manifest, child event stream, final audit, or child trust bundle exists. Once dispatched, the shadow run record contains `live_arm_freeze_seal_sha256`; therefore its pre-freeze manifest snapshot pins that live seal. Its external shadow seal repeats the same `live_arm_freeze_seal_sha256`.
3. Finalize and natively audit the child manifest after its seal. The parent final manifest's completed `declared_child_scopes` entry pins the child's final `manifest_sha256`, development-contract hash, protection-anchor hash, freeze-seal hash, and audit-report hash/status.
4. After every child final manifest and native audit is fixed, exclusively create and independently pin the child trust bundle. Its entries pin the child final manifest hashes and external seals; a shadow entry also pins the live-arm seal by `live_arm_freeze_seal_path` and `live_arm_freeze_seal_sha256`.

The snapshot is the complete pre-seal typed manifest view at capture time. It has exactly one run record, a valid native checkpoint prefix through the `frozen` boundary, all research agents/allocations/queries/tool events/source opens, closed metering, truthful file/tool attestations, and reconciled positive resource totals. Its non-run records are a byte-for-byte prefix of the final manifest's non-run records. After the seal, the only records that may append are the narrowly defined terminal integration checkpoint records needed to reach `complete`; they must follow the snapshot prefix, use the required predecessor, occur strictly after the seal and applicable child completion/audit events, and contain no new research telemetry or retroactive artifact claims. No agent, allocation, query, tool, source, evidence, research-stage checkpoint, or backdated event may be appended, dropped, reordered, or rewritten after the seal. The final machine manifest may materialize only the sole run-summary fields explicitly reserved for final integration bookkeeping: terminal timestamps/status mirrors, final resource/completeness mirrors, pre-registered child declarations by filling their null finalization fields once, and an optional reconciled shadow-results release timestamp. All other run identity, selection, wave, lineage, seed, budget, routing, model/effort, contract, and child-registration fields remain byte-identical. The raw snapshot and external seal are never overwritten or reissued. The final manifest is not an input to its own seal, the parent final manifest is not an input to the child seal it names, and the child trust bundle is not an input to any seal it names. No fixed-point hash, mutable re-seal, replacement snapshot, or post-seal telemetry reconstruction is permitted.

For a regeneration, both its run record and freeze seal additionally bind `parent_scope_id` and `initial_freeze_seal_sha256`. Its audit also receives the independently pinned initial live V2 seal payload and digest; self-repeating an invented parent ID or 64-character digest in the regeneration manifest and its own seal is not ancestry proof. A shadow child's run record, pre-freeze snapshot, external seal, and separate trust entry bind the independently pinned live-arm freeze seal. The seal set, closure cohort, ledger set, and scope-local candidate namespace must match exactly. A renamed, missing, extra, duplicated, symlinked, outside-scope, or rewritten candidate fails. The auditor reports only that exact bytes match pinned snapshots; it does not claim that the filesystem or timestamp source is intrinsically immutable.

### Conservative V1 replay

V1 artifacts are evidence, never instructions. Do not mutate a completed V1 run, anchor, freeze seal, digest pin, or audit report; do not issue a replacement historical seal. A V1 replay uses an explicit read-only legacy adapter and may infer semantics only from a non-contradictory closed tuple:

- `mode: audited_funnel`, `matched_pilot: true`, `shadow_only: false`, and `validation_eligible: true`, plus a valid referenced Archipelago child, maps to `operational_live_with_shadow` / `live`;
- `mode: archipelago_lite_shadow`, `matched_pilot: true`, `shadow_only: true`, and `validation_eligible: false` maps to that profile's `shadow` child only when its live-arm reference and seals agree;
- `mode: audited_funnel`, `matched_pilot: true`, `shadow_only: true`, `validation_eligible: false`, matched-baseline arm records, and baseline finalist namespace maps to `v2_matched_nonrouting` / `matched_baseline` semantics for replay only;
- `mode: audited_funnel`, `matched_pilot: false`, live arm records, and live eligibility maps to `ordinary_audited_funnel`.

Any missing or contradictory profile signal yields `PROFILE_AMBIGUOUS`; do not guess. A V1 artifact that is internally coherent but has no V2-only fields is schema/version-incompatible, not profile-ambiguous and not by itself a genuine telemetry failure. Replay normalization changes classification only. It cannot invent missing events, allocation links, evidence records, exact metering, timestamps, file-read attestations, completion state, or isolation proof, and cannot make a V1 scope satisfy V2 parity.

If current workflow files have evolved, verify the old independently pinned V1 anchor and seal plus an exact content-addressed historical bundle of the old bytes. Report the three claims separately: `historical_snapshot_integrity`, `current_validator_compatibility`, and `current_workflow_relation`. A current whole-file prompt, skill, protocol, or auditor mismatch against a V1 anchor is expected workflow evolution and reports `SUPERSEDED`; it does not make a valid old snapshot fail. The separately pinned Validation Gates block and fixed founder/validator identities must still match for `current_validator_compatibility`. The historical bundle cannot stand in for canonical paths in a new run, create a seal, or authorize routing. Preserve any original historical PASS report as immutable; a replay writes a separate report and never overwrites it.

### `00a_context_and_resource_manifest.jsonl`

Write one JSON object per line. The closed V2 `record_type` enum for this manifest is `run`, `checkpoint`, `agent`, `allocation`, `query`, `tool_event`, or `source_open`. The sole `run` record has the required final-summary shape defined above. Checkpoints are the lifecycle source and hash-bind pre-dispatch and final child declaration snapshot artifacts; no separate child registration, finalization, or state-transition record type exists.

The closed shared stage enum for both agent and allocation records is:

```text
problem_discovery, generation, direct_concept, inversion, recombination,
history_compressor, cartography, cluster_audit, level1, provisional_selector,
selector, tail_challenger, level2, finalist_selector, fact_closure, dossier
```

A zero-query stage still uses its exact enum with `query_cap: 0`. Agent and allocation validators use this same enum; there is no narrower allocation-only stage set. Supported event records include:

```json
{"record_type":"checkpoint","checkpoint_id":"CP-02-problem_cards_frozen","state":"problem_cards_frozen","predecessor_id":"CP-01-registered","occurred_at":"2026-08-21T12:20:30+02:00","completed_agent_ids":["scout-01"],"file_read_log_complete":true,"tool_event_log_complete":true,"resource_totals":{"unique_queries":1,"uncached_input_tokens":120000,"output_tokens":6000,"elapsed_microseconds":1170000000},"artifacts":[{"path":"02b_raw_to_direction_ledger.jsonl","sha256":"..."}]}
{"record_type":"agent","agent_id":"scout-01","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","role":"evidence_scout_customer_workarounds","island_id":"customer_workarounds","assigned_ids":["P-customer_workarounds-01","P-customer_workarounds-02","P-customer_workarounds-03","P-customer_workarounds-04","P-customer_workarounds-05","P-customer_workarounds-06"],"output_ids":["P-customer_workarounds-01","P-customer_workarounds-02","P-customer_workarounds-03","P-customer_workarounds-04","P-customer_workarounds-05","P-customer_workarounds-06"],"fork_turns":"none","context_classes":["founder_constraints","safety_legal","neutral_evidence"],"started_at":"2026-08-21T12:01:00+02:00","ended_at":"2026-08-21T12:20:00+02:00","model":"exact-model-id-and-version","reasoning_effort":"exact-setting","metering_basis":"tool_reported","context_files":[{"path":"context/scout-01.md","sha256":"..."}],"allowlisted_files":["context/scout-01.md"],"files_read":["context/scout-01.md"],"resources":{"uncached_input_tokens":120000,"output_tokens":6000,"elapsed_microseconds":1140000000}}
{"record_type":"allocation","allocation_id":"ALLOC-DISC-01","agent_id":"scout-01","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","entity_ids":["P-customer_workarounds-01","P-customer_workarounds-02","P-customer_workarounds-03","P-customer_workarounds-04","P-customer_workarounds-05","P-customer_workarounds-06"],"query_cap":18,"used_unique_queries":1,"unused_queries":17,"created_at":"2026-08-21T12:00:30+02:00","metering_basis":"tool_reported","resources":{"uncached_input_tokens":120000,"output_tokens":6000,"elapsed_microseconds":1140000000}}
{"record_type":"query","query_id":"Q-0001","allocation_id":"ALLOC-DISC-01","agent_id":"scout-01","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","query":"normalized query text","entity_ids":["P-customer_workarounds-01"],"occurred_at":"2026-08-21T12:05:00+02:00"}
{"record_type":"tool_event","call_id":"CALL-0001","query_id":"Q-0001","allocation_id":"ALLOC-DISC-01","agent_id":"scout-01","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","tool":"web_search","event_type":"tool_call","occurred_at":"2026-08-21T12:05:01+02:00"}
{"record_type":"source_open","source_event_id":"SRC-0001","query_id":"Q-0001","call_id":"CALL-0001","allocation_id":"ALLOC-DISC-01","agent_id":"scout-01","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","url":"https://example.test/source","entity_ids":["P-customer_workarounds-01"],"evidence_ids":["EV-0001"],"occurred_at":"2026-08-21T12:05:02+02:00"}
```

Record actual reads, not intended reads. Every delivered context packet appears in the allowlist and `context_files` with its raw-byte hash; every actual read appears in `files_read`. `context_classes` is a complete typed inventory. Each checkpoint attests completeness and reconciles telemetry through its own boundary. Unknown `record_type`, stage, state, arm, or missing reciprocal ID values are invalid.

The sealed `02c_main_provisional_order.json` has this exact shape and partitions all 48 concepts:

```json
{"main_provisional_ids":["D-001","D-002","D-003","D-004","D-005","D-006"],"ordered_reserve":["the remaining 42 unique concept IDs in order"],"creator_agent_id":"provisional-selector-01","frozen_at":"2026-08-21T13:00:00+02:00","seed":"pre-registered-seed"}
```

The sealed `02d_fact_closure_candidates.json` binds the Level-2 decision to the closure budget. In the Archipelago arm it names raw concept IDs created by the isolated finalist selector. In the matched audited baseline it names Level-2 direction IDs sealed by the existing main-agent rule with `creator_agent_id: "root-orchestrator"`:

```json
{"candidate_ids":["D-001","D-002","D-003","D-004","D-005","D-006"],"creator_agent_id":"finalist-selector-01","selected_at":"2026-08-21T13:40:00+02:00","seed":"pre-registered-seed"}
```

### `02b_raw_to_direction_ledger.jsonl`

Supported records:

```json
{"record_type":"problem","problem_id":"P-customer_workarounds-01","source_island":"customer_workarounds","creator_agent_id":"scout-01","evidence_ids":["EV-0001"]}
{"record_type":"mapping","raw_id":"D-001","concept_type":"direct","parent_ids":["P-customer_workarounds-01"],"creator_agent_id":"builder-01","direction_id":"DIR-001","cluster_id":"CL-001","disposition":"retained","reason":"field-level rationale"}
{"record_type":"mapping","raw_id":"I-001","concept_type":"inversion","parent_ids":["D-001"],"creator_agent_id":"inverter-01","operation":{"dimension":"payer","assumption":"...","causal_benefit":"...","new_risk":"..."},"direction_id":"DIR-001","cluster_id":"CL-I-001","disposition":"merged","reason":"field-level rationale"}
{"record_type":"mapping","raw_id":"X-001","concept_type":"recombination","parent_ids":["D-001","D-007"],"creator_agent_id":"recombiner-01","operation":{"transferred_mechanism":"...","analogy_break":"..."},"direction_id":"DIR-007","cluster_id":"CL-X-001","disposition":"merged","reason":"field-level rationale"}
{"record_type":"evidence","evidence_id":"EV-0001","scope_id":"shadow-w01","arm":"shadow","stage":"problem_discovery","allocation_id":"ALLOC-DISC-01","agent_id":"scout-01","direction_id":"DIR-001","entity_ids":["P-customer_workarounds-01"],"source_event_ids":["SRC-0001"],"proposition":"The named payer has a recurring loss and budget proxy.","recorded_at":"2026-08-21T12:05:03+02:00","decision_critical":true,"status":"unknown","source":"03_research_and_sources.md#EV-0001","cheapest_resolving_test":"Obtain one budget-backed buyer commitment."}
{"record_type":"level2","concept_id":"D-001","selection_category":"main_provisional","selected_at":"2026-08-21T13:15:00+02:00","completed_at":"2026-08-21T13:39:00+02:00","development_status":"complete","artifact_path":"shadow_level2/level2_d-001.md","sha256":"lowercase-sha256-of-exact-dossier"}
{"record_type":"finalist","finalist_id":"FIN-01","direction_id":"DIR-001","raw_ids":["D-001"],"evidence_ids":["EV-0001"],"frozen_at":"2026-08-21T14:00:00+02:00","arm":"shadow","shadow_only":true,"validation_eligible":false,"artifact_path":"shadow_candidates/shadow_finalist_candidate_01.md","sha256":"lowercase-sha256-of-exact-frozen-file"}
```

Allowed mapping dispositions are `retained`, `merged`, `rejected`, and `unresolved`. `unresolved` is explicit preservation, not deletion. A finalist must trace through a `retained` or `merged` raw ancestor, cite decision-critical evidence recorded no later than its freeze, and bind to an existing immutable dossier path and exact SHA-256. Two finalist IDs may not point to identical frozen content. Live finalists explicitly set `validation_eligible: true` and use `finalist_*.md`; Archipelago finalists use `shadow_finalist_*.md`; matched-baseline finalists use `baseline_shadow_finalist_*.md`, `shadow_only: true`, and `validation_eligible: false`.

Shadow Level-2 records use exactly six `main_provisional`, three `selector_or_challenger`, one `rejected`, one `near_cutoff`, and one `singleton` selection category. A fallback retains the intended category and adds `backfill_reason`; it does not create a sixth category.

## Regeneration isolation and shadow-result withholding

A regeneration is a new scope, never a reopened directory or mutable extension of an initial scope. Before any regeneration agent starts, the parent declares a child with `relationship: "regeneration"`, `run_profile: "ordinary_audited_funnel"`, `cohort_kind: "regeneration"`, `arm: "live"`, `mode: "audited_funnel"`, `routing_state: "enabled"`, and a unique run-local non-symlink `relative_path`. The regeneration run record uses the next unused `wave_index`, which is at least 2. The child has its own run record, `00b_development_contract.json`, context tree, ledger, protection anchor, freeze seal, audit report, and child trust-bundle entry. Its development contract records an ordinary audited-funnel opportunity and is not used for parity.

The initial scope, its manifest, closure cohort, candidate files, anchors, and seals remain byte-identical. A regeneration cannot append candidates to the initial ledger, issue a replacement seal, reuse an initial allocation or evidence ID, or depend on recursive filename discovery. Scope-local finalist names may repeat standard filename patterns because identity is `(run_id, scope_id, finalist_id, artifact_path, sha256)`, not basename alone.

Every regeneration run record and its freeze seal bind exactly the lineage fields `parent_scope_id` and `initial_freeze_seal_sha256`. The parent ID equals the initial live scope, and the seal hash equals that scope's independently pinned V2 freeze seal. A direct regeneration audit supplies that external initial seal and digest with `--initial-freeze-seal` and `--initial-freeze-seal-sha256`; a composite audit supplies the already pinned parent seal internally. Missing or self-attested ancestry is `INCOMPLETE` or `FAIL`, never `PASS`. Its final child declaration and trust entry bind the regeneration's own manifest, development contract, anchors, audit, model/effort, and `results_visibility: "available"`.

Regeneration packets are freshly constructed inside the regeneration scope. They may use only neutral live generation history that contains no evaluator, advisory, judge/panel, ranking, validator, confirmation, or downstream decision output, and they cannot read parent or sibling paths directly. Every permitted upstream item is copied into a run-scoped packet, stripped to its allowed content, hash-bound in `context_files`, and listed in the agent's allowlist and actual-read log. Any `shadow` or `matched_baseline` ID, title, artifact path, result, semantic recommendation, evaluator/advisory output, validator feedback, ranking, context read, or unrecorded delivery in a regeneration packet is an isolation failure. This proof comes from scoped packet hashes, actual reads, child declarations, and fingerprint scans—not invented run-record aliases.

For `operational_live_with_shadow`, a shadow child may start only after the initial operational-live cohort is externally frozen. Its declaration begins with `results_visibility: "withheld"`. Shadow execution and storage must occur under a separate coordinator that does not deliver outputs to the live decision-maker, or else shadow dispatch is deferred until the live orchestration is terminal and no regeneration or downstream routing decision remains.

Automatic child-agent delivery counts as release. “Not opening,” not quoting IDs, or finding no literal shadow-title match does not prove withholding. The shadow declaration and child trust entry remain `results_visibility: "withheld"`; they are immutable execution-time facts. The parent may set an offset-aware `shadow_results_released_at` only after its lifecycle is `complete`, the child trust bundle is complete, and no later live cohort can be registered. A regeneration whose `started_at` is at or after that timestamp is a failure. Release cannot rewrite a declaration, trust bundle, audit, or routing state, and any later live decision event fails integration isolation.

For `v2_matched_nonrouting`, both arms remain `frozen_nonrouting`, no regeneration exists, and results may be released only after both scope audits and the child trust bundle are complete. Release never changes routing. In every non-routing scope, structured action, route, call, destination, and next-step fields are content-scanned recursively; an instruction such as `send_to_fresh_chat_validator` fails regardless of filename, key alias, or event timestamp.

## Human-readable artifacts

The root scope stores its machine-readable files at its canonical root. Every declared child mirrors the required machine-readable artifacts inside its own declared scope. Audit each scope independently, then run a separate integration audit over the externally pinned child trust bundle. A scope PASS never substitutes for the integration audit, and an integration report never repairs a scope failure.

- `00_run_manifest.md` — protocol, baseline, hashes, seed, budgets, dirty state, and shadow boundary.
- `00a_context_and_resource_manifest.jsonl` — the V2 final run summary plus append-only checkpoint-derived lifecycle, context, allocation, query, tool, source, and metering records.
- `00b_development_contract.json` — immutable `zt1-development-contract-v2` opportunity and parity contract; its raw-byte digest must match the run record, child declaration, seal, and trust bundle.
- `00c_pre_freeze_manifest_snapshot.jsonl` — immutable raw-byte copy of `00a_context_and_resource_manifest.jsonl` taken immediately before the external V2 freeze seal and bound by that seal's snapshot path/hash fields.
- `01a_search_space_map.md` — evidence modalities and soft coverage, not an exhaustion claim.
- `01b_history_fingerprints.md` — neutral fingerprints and status.
- `02a_raw_pool.md` — every immutable raw concept.
- `02c_shadow_selector_audit.md` — sealed selections, provisional-main timestamp, disagreements, sentinels, and reconciliation.
- `02d_fact_closure_candidates.json` — sealed isolated 12-to-6 selection and exact closure cohort.
- `03_research_and_sources.md` — evidence IDs, timestamps, propositions, sources, contradictions, and unknowns.
- `09_diversity_and_resource_audit.md` — effective fingerprints, duplicates, source concentration, selector overlap, and resource parity.
- `10_integrity_check.md` — audit command, result, exceptions, and protected downstream hashes.

Operational-live finalists use scope-local `finalist_<slug>.md`. Archipelago finalists use `shadow_finalist_<slug>.md`. Matched audited-baseline finalists use `baseline_shadow_finalist_<slug>.md`. Every ledger record also carries the explicit routing compatibility fields. Filename namespace is a defense in depth, not the source of routing truth.

The parent audit ignores a child directory only through its exact registered path and finalized manifest hash. The integration audit deliberately scans the declared scope graph, trust bundle, packets, reads, downstream artifacts, and event ordering. It fails if a non-routing ID, artifact, output, or exposure enters an operational-live finalist, regeneration packet, evaluator packet, pivot, panel request, real-chat request, confirmation artifact, or decision context.

V2 final verification requires, for every scope, its independently pinned V2 protection anchor and freeze seal plus the exact development contract. Multi-scope profiles additionally require the independently pinned `zt1-child-trust-bundle-v2`, all child pins, all scope audit-report hashes, and visibility evidence. Trust documents use the specified canonical JSON encoding for their own digests, are regular non-symlink files outside every audited scope, and are exclusively created rather than overwritten. Raw artifact hashes, including the development-contract digest, remain hashes of exact raw bytes.

## Termination

Do not declare search exhaustion because named sectors, lenses, or mechanism classes were visited. Stop on the pre-registered resource boundary and report:

- new economic fingerprints per additional concept batch;
- historical-neighbor rate;
- duplicate rate;
- unresolved selector disagreement;
- uncovered evidence modalities;
- whether a second seeded run is needed.

Coverage and diversity are process diagnostics. Only a separately approved, matched fixed-validator experiment can establish stronger ideas.
