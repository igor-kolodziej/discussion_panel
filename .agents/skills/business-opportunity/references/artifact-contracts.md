# Artifact Contracts

Read this reference before creating or completing a canonical artifact, recovering state, importing a holdout, or publishing. The CLI and run's immutable config snapshot are authoritative; never hand-edit managed JSON.

## Cohort And Campaign Trees

Each cohort lives at `runs/<utc-run-id>/`:

```text
manifest.json
state.json
events.jsonl
inputs/{founder.md,evaluator.txt,config.json}
discovery/
candidates/<candidate-id>/v<version>.json
portfolio/
  screening-batches.json
  secondary-screening.json
  screening-aggregation.json
  selection.json
  development-decision.json
  version-selection.json
  finalists.json
research/<candidate-id>/v<version>.json
evaluations/<candidate-id>/v<version>/screening-<judge-id>.json
evaluations/<candidate-id>/v<version>/screening-secondary-<judge-id>.json
evaluations/<candidate-id>/v<version>/research-<judge-id>.json
evaluations/<candidate-id>/v<version>/development-<judge-id>.json
development/<candidate-id>/constructor-result.json
holdout/<candidate-id>/v<version>/
exports/<candidate-id>/
final/report.json
report.md
```

`manifest.json` binds the immutable inputs. Configuration is normalized as validated canonical JSON before snapshotting and hashing, so incidental source key order or whitespace does not create drift. `state.json` is validated resumable state, while `events.jsonl` is its append-only transition and failure history. Candidate, research, evaluation, portfolio, development, holdout, and publication records are canonical only after CLI validation.

Each campaign lives at `campaigns/<campaign-id>/` with immutable founder/evaluator snapshots, managed state and events, `briefs/cohort-<N>.json`, and a terminal receipt and report. Every cohort publication writes immutable `outcomes/<run-id>/campaign-metrics.json`, binding all progress metrics to the hashes of the complete published evidence set. Finalization copies the receipt, report, manifest, event log, canonical input snapshots, and continuation briefs to tracked `outcomes/campaigns/<campaign-id>/`. The receipt binds the manifest, cohort reports, and metric receipts. The CLI attaches cohort IDs, records a published cohort idempotently, computes progress, and generates continuation briefs. Do not construct a brief, metric receipt, or campaign receipt by hand.

## Candidate JSON

A candidate is a strict object; extra keys are rejected. Required identity, lineage, and content include:

- `schema_version`, path-safe `candidate_id`, positive `version`, and `parent` naming the immediately preceding version or `null` for the root;
- `stage`: the candidate's current workflow stage;
- `discovery_lane`: one exact slug from the immutable run configuration, preserved by a development child;
- non-empty `title` and `thesis`;
- `fingerprint` with exactly `customer`, `problem_trigger`, `payer_and_paid_event`, `offer_and_business_model`, `distribution_mechanism`, and `compounding_advantage`;
- `structure` with exactly `commercial_archetype`, `control_point`, and `critical_dependency`;
- `critical_control_point`, a strict contract identifying the controlled subject; current owner and launch controller; acquisition instrument; exclusivity, duration, revocability, transferability, and renewal; refusal fallback and replaceability; customer-relationship owner/control; mechanism ownership or dependency; controlled status; lawful founder-access basis; and confidential-employer-resource dependency;
- `commercial_mechanics`, identifying the paid event or measurable loss, payer, budget owner, purchase trigger, renewal event, distribution origin, customer-relationship owner, fully loaded economics, likely incumbent response, and resistance to bundling;
- `structural_signature`, containing controlled commercial-model, control-point, and critical-dependency categories plus normalized descriptors. Controlled categories collapse semantically equivalent industry, geography, and wording variants; `other` retains its normalized descriptor;
- `founder_fit` as a nonempty JSON array of distinct strings, `source_refs`, typed evidence claims, contrary evidence, uncertainties, and risks under the strict CLI contracts; and
- `economics` with pricing, margin basis, acquisition route, payback, retention or repeat, initial capital, founder time, and founder-net-worth path.

Critical-control-point `status` is one of `owned`, `exclusively_contracted`, `durably_contracted`, `replaceable_access`, `externally_controlled`, or `unknown`. Status, mechanism control, customer control, and acquisition terms must agree. Mechanism-first discovery rejects an externally controlled mechanism and requires a stated existing paid event; unknown proof remains valid uncertainty. Its configured founder-access reserve counts only lawful owned/controlled access or operating relationships with no confidential employer dependency.

Candidate files are immutable. Discovery creates an unparented v1 whose stage is `discovery`. Its full commercial core remains unchanged through research. Research, evaluation, shortlist changes, and freeze never create candidate copies.

Every candidate claim contains exactly `claim_id`, `claim_type`, `statement`, `evidence_refs`, and `confidence`. `claim_type` is one of `paid_event_or_measurable_loss`, `payer_and_budget`, `founder_control_point_path`, or `other`. These typed claims give screening and later research explicit evidence to assess; they do not create an eligibility gate. Validation never turns a scalar `founder_fit` into an array or invents a claim, source, or classification; the running candidate job fails visibly and may retry only within the configured mechanical budget.

Only an admitted development redesign may create v2. It must descend directly from the same candidate's v1, declare the exact normalized fingerprint fields and commercial-structure objects changed, change structured economics, and explain the economic effect. Rewording does not count, and later versions are not accepted. A `no_valid_redesign` constructor result leaves v1 as the exact final version. Freeze stores a reference to that exact v1 or v2; it does not create another candidate stage.

## Research JSON

Canonical research at `research/<candidate-id>/v<version>.json` binds `candidate_id`, `candidate_version`, and `candidate_sha256`. It contains strict source records with a bounded `evidence_class`, assessed claims, contrary evidence, unknowns, a critical-control-point assessment, commercial-evidence coverage, and a structured `falsification` map under the configured source limits. At least one source has `stance: "contradicting"`; contrary evidence cannot be an empty list.

`commercial_evidence` contains exactly `buyer_or_paid_event`, `distribution_and_acquisition`, `fully_loaded_unit_economics`, and `rights_control_access_contractibility`. Each item records `status`, `claim_ids`, and `source_ids`. Evidence or inference must bind a matching assessed claim, cited source, and appropriate controlled source class. An explicit `unknown` binds one or more unknown claims and no source IDs; missing private validation is not fatal. `critical_control_point_assessment` uses the same claim/source discipline and one controlled status.

`falsification` contains exactly these keys, each with a nonempty unique list of research claim IDs:

- `control_point_obtainability`;
- `substitutes_and_incumbent_response`;
- `external_dependencies`;
- `willingness_urgency_and_repeat_economics`;
- `cold_start_and_data_moat`; and
- `critical_mechanism_ownership`.

The referenced claims may be evidence, inference, or unknown. Coverage proves the question was addressed, not that the answer is favorable or known.

Every claim is `evidence`, `inference`, or `unknown`; cited references resolve to listed sources. Missing private proof remains unknown. A fatal portfolio disposition requires direct claim evidence and one allowed fatal reason—never a model's generic concern or an absent commitment.

Research is valid only for an exact discovery-v1 reference from the generated immutable `portfolio/selection.json`. Completing work for a different candidate does not silently change the shortlist, and research content never replaces candidate content.

## Evaluator Response And Canonical Evaluation

An evaluator authors one strict JSON response containing exactly:

- `candidate_id`, `candidate_version`, and path-safe `judge_id`;
- every evaluator factor with `name`, `status`, `score`, and `rationale`;
- interaction adjustment and assumptions;
- the required structural-strength, limiter, disconfirming-evidence, highest-value-change, and higher-score-evidence diagnostics.

The response does not contain an authored schema wrapper, evaluation type, rubric identity, weights, total, or qualification. The CLI supplies the phase-specific type (`working_screening`, `working_screening_secondary`, `working_research`, `working_development`, `holdout_native`, or `holdout_external`), binds candidate and rubric hashes, parses weights from the evaluator snapshot, validates exclusions, computes Decimal arithmetic, constrains the interaction and final scale, rounds explicitly, and derives qualification. Revalidating the same response must reproduce the same canonical evaluation.

Every candidate in a generated primary screening batch receives one screening evaluation. All candidates in a batch share one evaluator identity, and that identity cannot appear in another batch. Each triggered secondary set likewise shares one new identity that is fresh from every primary batch and other secondary set. Each selected discovery v1 then receives exactly the configured research working-evaluator coverage. After construction, every configured independent development evaluator assesses both v1 and any v2; the judge set must match across versions and cannot cross lineages or reuse an earlier working role. Constructor IDs are disjoint from development working-judge IDs. Native holdout judge IDs are globally distinct and disjoint from every working judge ID and constructor ID; renaming a reused role is not fresh provenance.

## Portfolio And Development Records

Write these records only with their CLI kinds. All candidate references are strict `{candidate_id, version, candidate_sha256}` objects.

`portfolio/screening-batches.json` is generated when discovery advances. It binds the current dedup-report hash and contains deterministic lane-balanced batches of strict candidate refs. The same candidate appears once, every configured lane contributes equally to each batch, and the union is the configured screening pool. It is never authored by an agent.

After primary coverage, `portfolio/secondary-screening.json` deterministically records every configured close-cutoff set, the primary artifacts and scores used to trigger it, and the cutoff margin. Those internal inputs never appear in `status --secondary-batch`; that view returns only its candidate set and immutable founder/evaluator bindings. Each response uses kind `secondary-evaluation`. Once coverage is complete, `portfolio/screening-aggregation.json` binds every primary and optional secondary artifact plus the configured rule and canonical score. Both generated artifacts and their events are immutable and replay-validated.

After complete screening coverage, the CLI generates `portfolio/selection.json` with exactly:

```text
schema_version
selection_version
calibration
candidate_refs
wildcard_candidate_refs
missing_archetypes
rationale
```

The initial `selection_version` is fixed. `calibration` is retained as a compatibility-shaped, hash-bound record of each screened candidate's own structural fields; its acquisition-evidence value is null. `candidate_refs` are the deterministic top canonical-score prefix from each batch after structural-signature deduplication and same-batch score backfill. `wildcard_candidate_refs` and `missing_archetypes` are empty because neither may alter score advancement. The file is immutable, cannot be agent-authored, and accepts no amendment in the score-bracket workflow.

`portfolio/development-decision.json` uses kind `portfolio-decision` and contains `schema_version` plus `candidate_decisions`. Each decision binds a candidate reference and contains:

- `disposition`: `develop`, `not_selected`, or `fatal`;
- `fatal_reason`: null unless fatal, otherwise `illegality`, `unobtainable_essential_rights`, `impossible_conservative_economics`, or `nondelegable_founder_incompatibility`;
- `fatal_claim_ids`: empty unless fatal and otherwise resolving to direct research evidence; and
- a non-empty `rationale`.

The CLI requires exact research and working-evaluation coverage before accepting the decision and enforces the deterministic score ranking, stable-ID tie break, and configured maximum.

For kind `development-result`, the constructor authors exactly:

```text
schema_version
candidate_id
outcome
constructor_id
rationale
falsification
structural_change
```

`falsification` has the same exact keys as research and each nonempty list references canonical research claim IDs. `structural_change` is null for `no_valid_redesign`. For `redesigned`, it records the dependency changed, resulting control status, control and distribution instruments, customer-relationship owner/control, fully loaded economic effects, incumbent-response defensibility, and supporting research claim IDs. The response contains no candidate hashes or versions. Complete and canonicalize a v2 candidate job first when redesigned. The CLI derives all identity fields from the admitted portfolio decision and canonical candidate state, then stores `development/<candidate-id>/constructor-result.json` with the same `structural_change` plus exactly derived identity fields:

```text
schema_version
candidate_id
base_candidate_version
base_candidate_sha256
outcome
final_candidate_version
final_candidate_sha256
constructor_id
rationale
falsification
structural_change
```

`outcome` is `redesigned` or `no_valid_redesign`. A redesign binds a valid structurally changed child. Preflight that v2 before starting its candidate job: when research establishes external control, the child must change `critical_control_point`, cannot remain `externally_controlled`, and may retain honest `unknown` proof only with a concrete acquisition instrument, launch controller, and refusal fallback. This prospective check prevents an immutable v2 that cannot later satisfy its constructor result. A no-redesign result binds the unchanged final version and explains the failed structural route. Hash identity is therefore stable across validated JSON normalization and cannot be rebound by ambiguous hash-only replacement. Canonical stored hashes remain mandatory and all lineage checks remain strict. Each selected candidate has one accepted constructor result.

When development advances, the CLI first generates `portfolio/version-selection.json`. Each lineage row binds the base ref and every individual evaluation, optional redesign ref and every evaluation, both conservative scores, the selected ref and conservative score, and the deterministic reason. The configured conservative arithmetic is deterministic. A redesign is selected only if its conservative score is strictly higher; equal or lower preserves the base. All artifacts remain immutable.

`portfolio/finalists.json` is then generated from one winning version per lineage. It contains `schema_version` and hash-bound `candidate_refs` to the configured top conservative-score prefix, with stable candidate ID only for exact ties. Both versions of one idea cannot occupy finalist slots. The file is the freeze boundary; no frozen candidate copy exists.

## Writes, Holdouts, And External Imports

Use the CLI for every job lifecycle and canonical write:

```text
python3 scripts/opportunity.py preflight <run-id> --kind <kind>
python3 scripts/opportunity.py preflight <run-id> --kind <kind> --job-id <job-id> --input <file>
python3 scripts/opportunity.py job <run-id> <job-id> start --stage <stage>
python3 scripts/opportunity.py job <run-id> <job-id> complete --input <file> --kind <kind> --preflight-sha256 <digest> --preflight-receipt-sha256 <receipt-digest>
python3 scripts/opportunity.py job <run-id> <job-id> fail --error <message>
python3 scripts/opportunity.py validate <run-id> --input <file> --kind <kind>
```

`preflight` is read-only. Without `--input`, it emits the role's exact skeleton, enums, constraints, and canonical evaluator factor names where applicable. With `--input` and the intended `--job-id`, it invokes the same canonical validator used for completion and returns its first RFC 6901 pointer diagnostic plus the raw input hash, canonical artifact hash, and contextual receipt while leaving the state, event log, and attempt counters unchanged. There is no separately maintained preflight validator. Correct only mechanical schema defects and preserve semantic content. After a successful preflight, start the job and complete it with the same bytes, reported input digest, and reported receipt digest. Structured completion requires both digests; its event stores the full receipt, and `check` rejects missing or inconsistent evidence. `validate` remains the concise authoritative validator for callers that do not need the role contract; it does not replace the preflight-before-start workflow.

Screening evaluators obtain one exact bounded batch with:

```text
python3 scripts/opportunity.py status <run-id> --batch <batch-id>
```

This output includes only that batch's candidate refs and artifacts plus immutable founder and evaluator bindings. Each binding is a repository-relative path and SHA-256, not the snapshot contents. The assigned evaluator must read exactly those two files, verify both hashes, and use their contents; an isolation prompt must expressly permit those reads while prohibiting other repository context. It omits other batches, scores, rankings, portfolio state, unrelated jobs, campaign state, and history.

Triggered secondary evaluators use `status <run-id> --secondary-batch <secondary-batch-id>` plus kind `secondary-evaluation`. They must read and hash-verify the two returned snapshots just like primary evaluators. The view omits the stored primary inputs, cutoff margin, scores, ranks, and rationale. Constructors use `status <run-id> --constructor <candidate-id>`; it exposes only the admitted candidate, its research, founder binding, and response kind. Development judges use `status <run-id> --development-lineage <candidate-id>`; it exposes both lineage versions under one evidence/evaluator context and the configured evaluator count, but no prior score or rank. Every scoped role must read and hash-verify each snapshot binding returned for that role; those bound files are the sole allowed snapshot reads.

Candidate-only researchers obtain their exact bounded context with:

```text
python3 scripts/opportunity.py status <run-id> --candidate <candidate-id>
```

This output includes only the active candidate ref and artifact, immutable founder snapshot binding, expected research path, and that candidate's research status. It omits portfolio metadata, other candidates, rankings, scores, evaluation coverage, unrelated jobs, and campaign state. Broad `status` and `status --json` are supervisor-only in role-separated orchestration.

Validate model output before advancing. For evaluation jobs, transport, parser, schema, or incomplete-output failure becomes a visible failed attempt and may restart only within the configured mechanical budget. Exhaustion remains visible in status and resumable state. A valid low score or adverse judgment completes the job; never retry it for quality. A valid `no_valid_redesign` result is also final for that constructor pass. Never hand-edit the manifest, state, events, frozen inputs, imports, or publication state.

Call `export-external` for each finalist reference. The packet binds the immutable founder and evaluator snapshots, exact referenced candidate, and canonical discovery-v1 research. For each native judge, create a new temporary `.json` destination outside the run and call:

```text
python3 scripts/opportunity.py holdout-assignment <run-id> <candidate-id> --response-destination <fresh-temp.json>
```

The returned object contains exactly `immutable_finalist_packet`, `strict_response_contract`, and `temporary_response_destination`. Give only those values to a freshly launched judge with no inherited repository/workflow context. The judge writes one response and must not load repository instructions, skills, CLI help/status/preflight, history, prior evaluations, rankings, competing candidates, or another judge's output. The main agent then reads the file, performs preflight, and completes the canonical native-holdout job. The CLI rejects a managed-state, non-JSON, missing-parent, or already-used destination. The envelope is mechanically restricted; repository filesystem isolation remains an orchestration guarantee.

External submission is optional. If used, import the complete strict response unchanged. The immutable receipt binds its raw bytes and the derived canonical evaluation. Malformed responses remain rejected and scoreless; every accepted response is binding and cannot be discarded or replaced.

## Terminal Reports And Publication

`finalize` derives `final/report.json` and `report.md` from validated canonical records. Publication copies a self-contained report, portfolio decision, evaluation coverage, selected evidence and candidates, highest working score, terminal stage, holdout results when present, and reopen conditions into `outcomes/<run-id>/`. Rendered reports must not rely on disposable raw-run links.

Terminal meanings are enforced:

- `qualified`: required holdouts and binding imports pass the configured strict rule;
- `no_qualifier`: at least one finalist completed required holdouts but none passed;
- `no_finalist`: research and working-evaluation coverage completed but no finalist reached holdout, leaving official score fields null; and
- `contested`: a binding result prevents confirmation.

Publishing creates `learning-digest.jsonl` with exactly one deterministic compact row for every researched candidate. Each row carries its structural triple, working limiter, disconfirming evidence, disposition, constructor outcome, fresh-evaluation reference and score, holdout objection, and reopen condition where applicable. The compact history row references and hash-binds the digest. Publication is idempotent. A published correction preserves the original outcome in Git history and explicitly states what changed; it never rewrites an old score into a current one.

`quarantine-outcome` is the supported immutable boundary for a current publication later proven procedurally invalid. It leaves the original report and outcome row byte-stable, writes canonical `outcomes/<run-id>/quarantine.json`, and appends an `opportunity_outcome_quarantine_v1` row that binds both the report and sidecar hashes. The command is idempotent only for the same reason and rejects conflicting reuse. Its fixed use class excludes the outcome and learning digest from every business decision while retaining them as workflow-test evidence. A campaign cohort cannot be quarantined independently.

For campaigns, `campaign next` records each published cohort at most once, computes progress from configured score signals under the immutable campaign policy, and either returns a sanitized brief or a terminal action. Free-text archetypes are guidance only and never a progress signal. `campaign finalize` accepts only a deterministic terminal state and writes the receipt and report.

The complete new capability-key set in an immutable config snapshot activates these contracts. Older schema-v3 configs and published schema-v2/v3 artifacts retain their original exact keys, report shapes, hashes, and deterministic validation; no existing run, campaign, outcome, or history row is migrated.
