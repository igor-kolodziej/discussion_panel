# History And Holdout Integrity

Read this reference when using prior runs, checking novelty, selecting a finalist, exporting to independent judges, importing responses, or interpreting qualification.

## Delayed History

Initial discovery is fresh. Do not load historical candidates, archived scores, failure summaries, or old verdicts into scouts. After a fresh pool exists, use:

- `knowledge/failure_patterns.md` for recurring structural failure modes; and
- only relevant rows from `knowledge/history_index.jsonl` for provenance and overlap.

The active history is digest-only. `legacy_run_digest_v1` rows preserve run state and omissions; `legacy_candidate_v1` rows preserve supported candidate fingerprints, original evaluation roles, raw score strings, and recovery provenance. `opportunity_outcome_v1` rows point to current published outcomes. Raw pre-cleanup evidence is available only through the checkpoint named in the index metadata and is not an active workflow input.

Historical scores retain their original rubric label and comparison semantics. Never normalize, translate, average, promote, or present them as current calibration, current candidates, or held-out evaluations.

Compare the six canonical fingerprint fields before semantic similarity. Reject cosmetic variants that preserve the same customer, trigger, paid event, offer, distribution, and compounding mechanism. Keep a historical variant only when it makes a material structural change and states which prior objections it resolves.

History is for novelty checks and adversarial memory after generation. It is not training text for producing another version of the repository's dominant idea family.

## Development Versus Holdout

Working evaluators diagnose candidates and can guide the bounded redesign stage. Their scores and conclusions cannot confirm a candidate.

Before final evaluation:

1. Validate and freeze each exact finalist version and evidence set.
2. For every frozen candidate, call `export-external` to generate one clean holdout packet bound to the immutable founder and evaluator snapshots and the canonical research records resolved through its lineage. Use that identical packet for both native judges; external submission is optional.
3. Use two fresh independent native judges. Do not reuse a generator, researcher, working evaluator, redesigner, or a judge exposed to another result.
4. Give each judge only the packet: frozen candidate, full canonical lineage research, the run's immutable founder and evaluator snapshots, and the requested response contract. Do not invent a divergent compressed profile.
5. Withhold the desired score, configured rule, rankings, selection rationale, working scores, previous conclusions, other judges' outputs, and archived comparisons.

Do not revise the candidate against a holdout and then count the same conversation as independent confirmation. A changed candidate is a new version and must follow the configured evaluation path.

## Binding Imports

Record the required native judgments as separate canonical evaluation jobs. External judgment is optional; if used, store every complete response unchanged and import each separately. Parser or schema failure is visible and resumable; it is never permission to infer a score. Do not discard an adverse result, cherry-pick a sentence, average in working judgments, or rerun until favorable.

Final qualification is computed only by the CLI from the canonical config, the required native holdouts, and any binding external imports. The native holdout floor controls candidate ranking; an imported external result may contest or reject but never boost that ranking or compensate for a native miss. If a candidate qualifies, use the exact label `score-qualified under holistic-11; not empirically market-validated`. This label describes evaluator performance, not customer demand, market validation, permission to spend, or guaranteed business success.
