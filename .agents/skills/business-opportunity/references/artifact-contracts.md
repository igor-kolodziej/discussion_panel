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
  selection.json
  amendments/v<N>.json
  development-decision.json
research/<candidate-id>/v<version>.json
evaluations/<candidate-id>/v<version>/working-<judge-id>.json
development/<candidate-id>/constructor-result.json
holdout/<candidate-id>/v<version>/
exports/<candidate-id>/
final/report.json
report.md
```

`manifest.json` binds the immutable inputs. `state.json` is validated resumable state, while `events.jsonl` is its append-only transition and failure history. Candidate, research, evaluation, portfolio, development, holdout, and publication records are canonical only after CLI validation.

Each campaign lives at `campaigns/<campaign-id>/` with immutable founder/evaluator snapshots, managed state and events, `briefs/cohort-<N>.json`, and a terminal receipt and report. Every cohort publication writes immutable `outcomes/<run-id>/campaign-metrics.json`, binding all progress metrics to the hashes of the complete published evidence set. Finalization copies the receipt, report, manifest, event log, canonical input snapshots, and continuation briefs to tracked `outcomes/campaigns/<campaign-id>/`. The receipt binds the manifest, cohort reports, and metric receipts. The CLI attaches cohort IDs, records a published cohort idempotently, computes progress, and generates continuation briefs. Do not construct a brief, metric receipt, or campaign receipt by hand.

## Candidate JSON

A candidate is a strict object; extra keys are rejected. Required identity, lineage, and content include:

- `schema_version`, path-safe `candidate_id`, positive `version`, and `parent` naming the immediately preceding version or `null` for the root;
- `stage`: the candidate's current workflow stage;
- non-empty `title` and `thesis`;
- `fingerprint` with exactly `customer`, `problem_trigger`, `payer_and_paid_event`, `offer_and_business_model`, `distribution_mechanism`, and `compounding_advantage`;
- `structure` with exactly `commercial_archetype`, `control_point`, and `critical_dependency`;
- `founder_fit`, `source_refs`, evidence claims, contrary evidence, uncertainties, and risks under the strict CLI contracts; and
- `economics` with pricing, margin basis, acquisition route, payback, retention or repeat, initial capital, founder time, and founder-net-worth path.

Candidate files are immutable. Promotion or structural redesign creates the next version with a parent pointer; it never overwrites the earlier JSON. A redesign must declare the fingerprint changes, change structured economics, and explain the economic effect. Rewording does not count.

Lineage must advance monotonically through the configured stages. A frozen candidate descends through discovery, research, and development. Its final development version must have the configured fresh working-evaluation coverage; an ancestor or another candidate cannot satisfy the gate.

## Research JSON

Canonical research at `research/<candidate-id>/v<version>.json` binds `candidate_id`, `candidate_version`, and `candidate_sha256`. It contains strict source records, assessed claims, contrary evidence, and unknowns under the configured source limits.

Every claim is `evidence`, `inference`, or `unknown`; evidence references resolve to listed sources. Missing private proof remains unknown. A fatal portfolio disposition requires direct claim evidence and one allowed fatal reason—never a model's generic concern.

Research is valid only for an active candidate reference from `portfolio/selection.json` as updated by accepted amendments. Completing work for a different candidate does not silently change the shortlist.

## Evaluation JSON

An authored evaluation contains:

- immutable candidate and rubric identity and hashes;
- path-safe `judge_id` and `evaluation_type` (`working`, `holdout_native`, or `holdout_external`);
- every evaluator factor with a scored or structurally excluded judgment;
- interaction adjustment and assumptions;
- the required structural-strength, limiter, disconfirming-evidence, highest-value-change, and higher-score-evidence diagnostics; and
- run-relative raw-response path and hash.

The CLI parses weights from the evaluator snapshot, validates exclusions, computes Decimal arithmetic, constrains the interaction and final scale, rounds explicitly, and derives qualification. A model-provided total is never trusted.

Each researched candidate version receives exactly the configured working-evaluator coverage. A redesigned or otherwise final development version receives a fresh working evaluation even when an ancestor was evaluated. Constructor IDs are disjoint from development working-judge IDs. Native holdout judge IDs are globally distinct and disjoint from every working judge ID and constructor ID; renaming a reused role is not fresh provenance.

## Portfolio And Development Records

Write these records only with their CLI kinds. All candidate references are strict `{candidate_id, version, candidate_sha256}` objects.

`portfolio/selection.json` uses kind `portfolio-selection` and contains exactly:

```text
schema_version
selection_version
candidate_refs
missing_archetypes
rationale
```

The initial `selection_version` is fixed by the validator. `missing_archetypes` is a unique list of non-empty labels observed as absent in the cohort's semantic audit and may be empty; do not fabricate a global archetype vocabulary. Once recorded, the file is immutable.

Each `portfolio/amendments/v<N>.json` uses kind `portfolio-amendment` and contains exactly:

```text
schema_version
amendment_version
base_selection_sha256
remove_candidate_ref
add_candidate_ref
reason
```

Amendments form the only accepted versioned update path. The CLI validates order, `base_selection_sha256` against the immediately preceding selection or amendment record, the removed active reference, and the added canonical reference.

`portfolio/development-decision.json` uses kind `portfolio-decision` and contains `schema_version` plus `candidate_decisions`. Each decision binds a candidate reference and contains:

- `disposition`: `develop`, `not_selected`, or `fatal`;
- `fatal_reason`: null unless fatal, otherwise `illegality`, `unobtainable_essential_rights`, `impossible_conservative_economics`, or `nondelegable_founder_incompatibility`;
- `fatal_claim_ids`: empty unless fatal and otherwise resolving to direct research evidence; and
- a non-empty `rationale`.

The CLI requires exact research and working-evaluation coverage before accepting the decision and enforces the deterministic development ranking and configured maximum.

`development/<candidate-id>/constructor-result.json` uses kind `development-result` and contains exactly:

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
```

`outcome` is `redesigned` or `no_valid_redesign`. A redesign binds a valid structurally changed child. A no-redesign result binds the unchanged final version and explains the failed structural route. Each selected candidate has one accepted constructor result.

## Writes, Holdouts, And External Imports

Use the CLI for every job lifecycle and canonical write:

```text
python3 scripts/opportunity.py job <run-id> <job-id> start --stage <stage>
python3 scripts/opportunity.py job <run-id> <job-id> complete --input <file> --kind <kind>
python3 scripts/opportunity.py job <run-id> <job-id> fail --error <message>
python3 scripts/opportunity.py validate <run-id> --input <file> --kind <kind>
```

Validate model output before advancing. A malformed artifact becomes a visible failed job, not guessed content. Never hand-edit the manifest, state, events, frozen inputs, imports, or publication state.

Call `export-external` for each frozen finalist. The packet binds the immutable founder and evaluator snapshots, exact frozen candidate, and canonical lineage research. Both native judges receive it unchanged. Preserve each complete native return, then record a distinct canonical evaluation wrapper with its raw binding.

External submission is optional. If used, import the complete response unchanged. Malformed responses remain rejected and scoreless; every accepted response is binding and cannot be discarded or replaced.

## Terminal Reports And Publication

`finalize` derives `final/report.json` and `report.md` from validated canonical records. Publication copies a self-contained report, portfolio decision, evaluation coverage, selected evidence and candidates, highest working score, terminal stage, holdout results when present, and reopen conditions into `outcomes/<run-id>/`. Rendered reports must not rely on disposable raw-run links.

Terminal meanings are enforced:

- `qualified`: required holdouts and binding imports pass the configured strict rule;
- `no_qualifier`: at least one finalist completed required holdouts but none passed;
- `no_finalist`: research and working-evaluation coverage completed but no finalist reached holdout, leaving official score fields null; and
- `contested`: a binding result prevents confirmation.

Publishing appends or corrects one compact history row idempotently. A published correction preserves the original outcome in Git history and explicitly states what changed; it never rewrites an old score into a current one.

For campaigns, `campaign next` records each published cohort at most once, computes progress under the immutable campaign policy, and either returns a sanitized brief or a terminal action. `campaign finalize` accepts only a deterministic terminal state and writes the receipt and report.
