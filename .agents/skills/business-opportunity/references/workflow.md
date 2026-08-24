# Workflow

Read this reference when starting a run, assigning subagents, advancing a stage, or deciding whether to redesign or stop.

## Preflight And Ownership

The main agent reads the canonical founder profile and configuration, creates or resumes the run with `scripts/opportunity.py`, and remains the only canonical writer. Use bounded subagents for independent evidence gathering or judgment. Each assignment states its lane, scope, evidence standard, output shape, and stopping condition.

Initial scouts may receive relevant founder facts, but must not receive historical ideas, failure memory, the evaluator rubric, the score target, working scores, or another scout's ranking. This prevents imitation and score-shaped generation.

Follow the state sequence recorded by the CLI: `initialized` → `discovery` → `calibration` → `research` → `development` → `frozen` → `holdout` → `complete`. Do not skip or move backward; `resume` recovers interrupted work in the current stage. All configured stage, candidate, and retry maxima are hard limits.

## Fresh Evidence Discovery

Run all three lanes before historical calibration:

- **Mandatory or repeated spend, financial leakage, and costly failure:** locate existing budgets, recurring loss, downtime, claims, disputes, or compulsory workflows with an identifiable paid event.
- **Operational bottlenecks, fragmented assets or supply, specialist scarcity, and market transitions:** locate constrained capacity, coordination failures, stranded or installed assets, broken handoffs, and transitions that change buyer behavior or economics.
- **Founder-accessible asymmetries:** test reachable problems in Poland or CEE and around data or AI, health, finance, and the family renewables ecosystem. Access is evidence to investigate, not a reason to force a sector.

Require sources for time-sensitive or market-dependent claims. Every returned claim is tagged as evidence, inference, or unknown. A scout returns bounded opportunity records rather than persuasive essays.

## Candidate Formation And Delayed History

Create the fresh candidate pool and run its structural deduplication before leaving `discovery`. In `calibration`, read `knowledge/failure_patterns.md` and relevant `knowledge/history_index.jsonl` rows for adversarial review and historical overlap before finalist selection.

Build the exact structural fingerprint from:

- `customer`
- `problem_trigger`
- `payer_and_paid_event`
- `offer_and_business_model`
- `distribution_mechanism`
- `compounding_advantage`

Run `dedup` using the configured exact and approximate rules. A new industry label does not make the same commercial structure novel. A materially improved historical mechanism may continue only when its changed fields and resolved objections are explicit.

The diversity trigger groups the normalized `payer_and_paid_event` and `offer_and_business_model` fields. Distribution is reviewed separately and does not split an otherwise repeated paid-event/business-model structure.

If the dedup report creates the bounded `gap-scout` job, run that one repair within its configured budget and rerun `dedup`. Do not turn a diversity shortfall into open-ended regeneration waves.

## Research And Development Judgment

Research the assumptions most likely to change the decision: paid behavior, purchasing trigger and authority, reachable buyer list, unit economics, distribution incentive and friction, competition, operating requirements, regulation, data rights, and durability.

Before finalist selection, enforce these proxy checks:

- recurring pain is not proof of recurring willingness to pay;
- regulation is not proof of budget or outsourcing;
- naming a partner category is not a distribution mechanism;
- accumulated data is not automatically a moat;
- avoided loss is not automatically capturable revenue;
- an identifiable market is not proof of affordable access; and
- adding software later does not automatically make a service scalable.

Working evaluators receive the immutable current candidate version, relevant founder constraints, evidence, and the canonical evaluator. They do not receive generator rationale, target, rankings, or other evaluations. Their job is to identify the main structural strength, primary limiter, strongest disconfirming evidence, highest-value structural change, and evidence needed to justify improvement.

## Structural Redesign

Use one bounded redesign pass during `development`, only for a near-winner with a concentrated, addressable limiter. Change at least one of the six canonical fingerprint fields, declare the exact changed fields in `redesign.changed_fingerprint_fields`, update at least one structured economics field, and explain the resulting economic effect in `redesign.economic_effect`. Save a new candidate version and preserve the prior one. Rewording does not count.

Honor the configured stage and retry maxima. If evidence invalidates the pool or no candidate survives, finish or exhaust all current-stage jobs, then call `finalize <run-id> --no-qualifier-reason "<reason>"` instead of generating indefinitely. Preserve the strongest latest-stage candidates, evidence, failed jobs, and known limiters for the derived report.

## Freeze, Holdout, And Publish

Validate every finalist artifact and freeze its exact version. For each frozen candidate, call `export-external` to generate one packet bound to the run's immutable `inputs/founder.md` and `inputs/evaluator.txt` snapshots and the canonical research records found along that candidate's lineage; do not create a divergent compressed profile, rubric, or evidence summary. Once every packet validates, advance from `frozen` to `holdout`. Give each identical packet independently to two fresh native judges and record their results through normal evaluation jobs. Submission to an external judge is optional despite the command name; every successfully imported valid external score is binding.

Do not adapt the frozen version in response to a holdout and continue calling that response independent; a changed candidate requires a new version and a new configured evaluation path. After the required native results and any optional external import are complete, run `check`, `finalize`, and inspect `final/report.json` plus `report.md`. Publish every terminal result, including non-confirmation or contested status, while reserving the qualification label for a result that actually earns it.
