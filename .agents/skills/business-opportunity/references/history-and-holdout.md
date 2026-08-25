# History, Campaign, And Holdout Integrity

Read this reference when using prior runs, generating a later cohort, checking novelty, freezing a finalist, assigning judges, importing a response, or interpreting qualification.

## Delayed History And Semantic Novelty

Initial discovery is fresh. Do not load historical candidates, failure summaries, scores, or verdicts into scouts. After the fresh pool exists, use `knowledge/failure_patterns.md` and only relevant `knowledge/history_index.jsonl` rows for overlap and adversarial review.

The index is digest-only. Legacy rows preserve their original rubric, score string, role, and recovery provenance. Never normalize, average, promote, or present a historical result as a current candidate, working evaluation, or holdout.

Compare exact six-field fingerprints first. Separately compare `structure.commercial_archetype`, `structure.control_point`, and `structure.critical_dependency`. New wording, geography, or industry is not semantic novelty when the commercial mechanism and dependency remain the same. Keep a historical variant only when a material structural change resolves a recorded objection.

History is delayed adversarial memory, not generation training. PromoLeak and its source dossier are outside this workflow entirely.

## Later Campaign Cohorts

The CLI alone decides whether a published cohort produces another cohort. Use only the `campaign next` action and its generated `briefs/cohort-<N>.json`. Do not prepare a shadow brief from reports or conversation history.

A sanitized brief may identify deficient evaluator factors and copy the shortlist's observed `missing_archetypes`. It must not invent a global archetype vocabulary or reveal candidate names or descriptions, raw or rounded scores, deltas, rankings, threshold, shortlist or development rationale, judge feedback, or previous verdicts. Scouts remain mutually blind and do not receive the evaluator.

Campaign patience is mechanical. Do not stop after one regression, reset progress by editorial judgment, add cohorts past the configured cap, or keep searching after a deterministic stop.

## Working Evaluation Versus Holdout

Working evaluations are mandatory diagnostics for all researched candidates and again for every final development version. They can drive the configured selection and construction pass, but cannot confirm an opportunity.

Before holdout:

1. Validate the exact finalist version, lineage research, constructor result, and fresh development-version working evaluation.
2. Generate one packet bound to immutable run snapshots and use that same packet for every judge.
3. Use genuinely fresh native judges isolated from generation, research, working evaluation, construction, and one another.
4. Ensure native judge IDs are globally distinct and disjoint from every working judge ID and constructor ID.
5. Give a judge only the packet and response contract. Withhold the desired score, qualification rule, prior scores, rankings, selection rationale, campaign history, competing candidates, other outputs, and archived comparisons.

Do not revise a frozen candidate after feedback and count the same judgment as independent. A changed candidate is a new version in a new permitted evaluation path with fresh judges.

## Binding Results

Record native judgments as separate canonical jobs. External judgment is optional; if used, preserve and import each complete response independently. Parser or schema failure remains visible and scoreless. Never infer a missing score, discard an adverse result, substitute a working judgment, or rerun until favorable.

The CLI computes qualification from the immutable config, required native holdouts, and all binding valid external imports. The native lower score controls candidate ranking; an external result may contest or reject but cannot raise the native floor.

Only a fully held-out finalist can produce `qualified`, `no_qualifier`, or `contested`. If no candidate reaches holdout after complete working-evaluation coverage, the cohort is `no_finalist` and its official score is N/A rather than zero. The qualification label describes rubric alignment, not customer demand, empirical market validation, permission to spend, or guaranteed business success.
