# Artifact Contracts

Read this reference before creating a run result, completing a job, importing a holdout response, recovering a run, or publishing an outcome. The CLI's validated contracts and the limits in `config/opportunity-workflow.json` are authoritative; this file explains placement and ownership without copying them.

## Run Tree

Each run lives at `runs/<utc-run-id>/`:

```text
manifest.json
state.json
events.jsonl
inputs/
  founder.md
  evaluator.txt
  config.json
discovery/<job-id>.<ext>
candidates/<candidate-id>/v<version>.json
research/<candidate-id>/v<version>.json
evaluations/<candidate-id>/v<version>/working-<judge-id>.json
holdout/
  jobs/<job-id>.<ext>
  <candidate-id>/v<version>/
    native-<judge-id>.json
    external-<judge-id>.json
    raw/external-<sha256>.txt
    imports/external-<sha256>.json
exports/<candidate-id>/
  holdout_packet.md
  response_schema.json
dedup/
  report.json
artifacts/<stage>/<job-id>.<ext>
final/
  report.json
report.md
```

- `manifest.json` identifies the run and the canonical source snapshots.
- `state.json` is the validated resumable state; it is not a narrative log.
- `events.jsonl` is append-only transition and failure history. Job lifecycle events project to the logical job state; `check` rejects missing or tampered lifecycle events, while the matching interrupted command can reconcile one event-first transition whose state write failed.
- `inputs/` freezes the inputs used by this run. Later canonical edits do not silently change an existing run.
- `discovery/` stores bounded scout returns and their provenance; `dedup/report.json` binds the discovery candidate hashes used for the structural check.
- `candidates/` stores immutable, versioned canonical candidates. A structural change creates a new version.
- `research/` stores sourced evidence and explicit unknowns hash-bound to candidate versions.
- `evaluations/` stores working judgments and their role/provenance, never a confirmation shortcut.
- `holdout/` stores native raw job returns and canonical evaluations plus any optional external raw responses, import records, and canonical evaluations.
- `exports/` contains the canonical shared holdout packets and their response contracts.
- `artifacts/` holds validated generic returns for stages without a stricter canonical path.
- `final/report.json` is the terminal machine record derived from validated candidate and holdout records; `report.md` is its concise human-readable rendering.

`events.jsonl` contains strict records with exactly `sequence`, `at`, `event`, `run_id`, `stage`, `job_id`, and `details`. Sequence values are contiguous in file order; `job_id` may be `null` for a run-level transition and `details` is an object. The CLI rewrites the log atomically when appending and validates the full sequence on read. Never append or repair it manually.

## Candidate JSON

A candidate is a strict object: the ordinary keys below are required and extra keys are rejected, with the single conditional `redesign` field described below.

- `schema_version`: integer matching the run config.
- `candidate_id`: lowercase path-safe slug; `version`: positive integer.
- `parent`: `null` for the first version, otherwise `{candidate_id, version}` naming the same `candidate_id` at exactly the preceding version.
- `stage`: `discovery`, `research`, `development`, or `frozen`.
- `title` and `thesis`: non-empty strings.
- `fingerprint`: object containing exactly `customer`, `problem_trigger`, `payer_and_paid_event`, `offer_and_business_model`, `distribution_mechanism`, and `compounding_advantage`; every value is a non-empty string.
- `founder_fit` and `source_refs`: unique string lists. Source-count limits come from the run config.
- `economics`: object containing exactly `pricing`, `gross_margin_basis`, `acquisition_route`, `payback`, `retention_or_repeat`, `capital_required_pln`, `founder_time`, and `founder_net_worth_path`. Each value is a non-empty string, finite number, or `null` while unknown. A frozen finalist must replace `capital_required_pln` with a finite nonnegative JSON number so the cash tie-break remains deterministic.
- `claims`: list of strict `{claim_id, statement, evidence_refs, confidence}` objects. IDs and statements are non-empty, evidence references are unique strings, and confidence is either a non-empty label or a finite number accepted by the validator.
- `contrary_evidence`, `uncertainties`, and `risks`: unique string lists. Keep disconfirming evidence separate from missing knowledge.
- `redesign`: omitted for ordinary versions. A same-stage development revision must add the strict object `{changed_fingerprint_fields, economic_effect}`. The declared list must exactly match at least one normalized change among the six fingerprint fields, at least one structured economics field must also change, and `economic_effect` must explain the consequence. The field is rejected on every other version.

Candidate files are immutable, and the CLI accepts one only when its `stage` matches the current run stage. Promotion to another stage or any structural redesign creates the next version and points `parent` at the prior version; it never overwrites the earlier JSON.

A lineage begins with discovery at v1, advances without skipping or moving backward, and may repeat a stage only for the bounded development redesign. A frozen version must therefore descend through discovery, research, and development for the same candidate ID. Its exact development parent must have at least one canonical working evaluation before the frozen artifact is accepted or a holdout packet is exported; another candidate's evaluation never satisfies this gate.

## Research JSON

Canonical research lives at `research/<candidate-id>/v<version>.json`. It is a strict object with:

- `schema_version`, `candidate_id`, `candidate_version`, and `candidate_sha256`, bound to the researched candidate artifact;
- `sources`: a list of strict `{source_id, url, title, publisher, published_at, accessed_at, source_type, stance}` objects. Every field is a non-empty string, source IDs are unique, and `stance` is `supporting`, `contradicting`, or `context`;
- `claims`: a list of strict `{claim_id, statement, assessment, evidence_refs}` objects. Claim IDs are unique, `assessment` is `evidence`, `inference`, or `unknown`, and every evidence reference resolves to a listed source ID; and
- unique string lists `contrary_evidence` and `unknowns`.

The configured source limits are enforced. Record an unsupported proposition as inference or unknown, never as evidence. Completing a research job validates the identity binding and writes the canonical path; do not paste later research into an already validated record.

## Evaluation JSON

An authored evaluation has these required keys:

- Identity: `schema_version`, `candidate_id`, `candidate_version`, `candidate_sha256`, `rubric_id`, `rubric_sha256`, and path-safe `judge_id`.
- Role: `evaluation_type`, set to `working`, `holdout_native`, or `holdout_external` as appropriate for the current stage.
- Judgment: `factors`, `interaction_adjustment`, and a unique string list named `assumptions`.
- Diagnostics: non-empty `main_structural_strength`, `primary_score_limiter`, `strongest_disconfirming_evidence`, `highest_value_structural_change`, and `evidence_needed_for_higher_score` strings. These must come from the judge's actual analysis, not a later summarizer.
- Raw binding: run-relative `raw_response_path` and matching `raw_response_sha256`.

`factors` contains exactly one object for every factor parsed from the immutable evaluator snapshot. Each factor has `{name, status, score, rationale}`:

- `status: scored` requires a score on the evaluator scale and a non-empty rationale.
- `status: excluded` requires `score: null` and a specific structural-irrelevance rationale.

Do not ask a model to copy rubric weights or calculate totals. The CLI verifies the candidate, rubric, and raw-response hashes; takes weights from the run snapshot; renormalizes only valid exclusions; and derives `original_weight`, `effective_weight`, `base_score`, `unrounded_score`, `constrained_score`, `final_score`, and `qualified`. If authored input includes a derived value, the CLI accepts it only when it exactly matches its own arithmetic.

For a native judgment, preserve the complete return as a generic holdout artifact first, then point the evaluation JSON at that run-relative raw artifact and hash. The external importer preserves the raw response and injects the immutable candidate, rubric, and raw-response identity fields before applying the same evaluator contract.

## Write Contract

Use the CLI for state-managed writes and transitions:

```text
python3 scripts/opportunity.py job <run-id> <job-id> start --stage <stage>
python3 scripts/opportunity.py job <run-id> <job-id> complete --input <file> --kind <kind>
python3 scripts/opportunity.py job <run-id> <job-id> fail --error <message>
python3 scripts/opportunity.py validate <run-id> --input <file> --kind <kind>
```

Supported kinds are reported by CLI help. Validate model-produced JSON before advancing. The main agent converts bounded subagent returns to the required input; subagents must not edit run state or canonical candidate files directly.

Never hand-edit `manifest.json`, `state.json`, `events.jsonl`, frozen inputs, imported holdout records, or publication state. Preserve raw model and external responses when the contract requires them. A malformed or incomplete artifact becomes a visible failed job, not a guessed value.

## Native And External Holdouts

Each fresh native judge returns the packet's `response_schema.json` judgment body. Preserve that complete body through a distinct generic holdout job, then create the canonical evaluation wrapper with the immutable candidate, rubric, judge, role, raw path, and raw hash fields. Record each wrapper through a distinct holdout-stage job with `--kind evaluation`; role and independence provenance must remain explicit.

Call `export-external` for every frozen candidate. It writes the one `holdout_packet.md` and `response_schema.json` used identically by both required native judges. The packet binds the candidate to the run's exact `inputs/founder.md` and `inputs/evaluator.txt` snapshots and embeds the path, hash, and full canonical research records resolved through its lineage; export fails if no candidate-bound research exists. It must not substitute a separately edited founder, rubric, or evidence summary.

Submitting that packet to an external judge is optional despite the command name. If external evaluation is used, save each complete response to a file and pass that file to `import-external`. Do not clean up, summarize, or merge raw judge responses before import. The CLI preserves and records a malformed response as rejected with no score; every successfully imported valid score is binding.

## Published Outcome

`finalize` writes `final/report.json` and derives `report.md`, including for non-confirmation or contested results. It derives scores, status, selection, evaluator diagnostics, binding limiters, failed or exhausted jobs, preserved candidate and evidence summaries, provenance, and any qualification label from canonical records; never parse the Markdown rendering back into state. Without a reason flag, finalization requires the holdout stage. `--no-qualifier-reason` may close any nonterminal active stage only when its current jobs have no running or retryable work.

`publish` accepts every finalized terminal status. It writes `outcomes/<run-id>/report.json` and `report.md`; preserves the holdout-selected candidate and binding evaluations, or the strongest early-closure candidates; and includes their canonical lineage research at the original run-relative paths. If early closure preserves multiple current-stage candidates, `finalize` requires `--best-candidate <candidate-id>` so the decision record, primary limiter, contrary evidence, and reopen condition bind to an explicit best candidate. It appends a provenance, fingerprint, raw-score, terminal-objection, and reopen-condition row to `knowledge/history_index.jsonl`. Non-confirmation and contested publications remain explicitly unqualified; absence of a qualifying candidate is not a runtime failure.
