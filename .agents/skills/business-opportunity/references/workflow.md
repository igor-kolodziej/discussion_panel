# Workflow

Read this reference when starting a cohort or campaign, assigning subagents, advancing a stage, or deciding whether evidence is fatal, a candidate may develop, or a campaign should continue.

## Ownership And Role Isolation

The main agent creates or resumes state with `scripts/opportunity.py` and remains the only canonical writer. Subagents receive bounded assignments with a lane, evidence standard, output contract, and stop condition. Keep scout and researcher contexts distinct by orchestration. The structured records mechanically preserve working-evaluator, constructor, and holdout identities.

Keep generation, research, working evaluation, and construction assignments context-distinct. The CLI enforces that a constructor identity cannot also be a working evaluator and that recorded working-evaluator and constructor identities cannot serve as holdout judges; holdout identities are distinct from one another. Scout and researcher freshness remains an explicit main-agent assignment duty because those records do not claim a mechanically verified actor identity. Do not infer freshness from a renamed output file.

Initial scouts receive relevant founder facts but not historical ideas, failure memory, the evaluator, qualification rule, prior scores, rankings, verdicts, or another scout's work. Campaign continuation does not relax this boundary.

## Discovery, Deduplication, And Portfolio Binding

Run every configured discovery lane before delayed history calibration. Scouts seek evidence of existing spend or loss, constrained operations or transitions, and founder-accessible asymmetries. Require source support for time-sensitive claims, and tag claims as evidence, inference, or unknown.

Each candidate contains the canonical six-field fingerprint and a `structure` object containing exactly:

- `commercial_archetype`: the primary way value is sold and captured;
- `control_point`: the scarce right, workflow position, asset, or relationship the business must control; and
- `critical_dependency`: the external condition whose failure most directly breaks delivery or economics.

Run exact fingerprint deduplication first and report only `exact_fingerprint_unique_count` as exact uniqueness. Lexical similarity remains advisory. Separately audit semantic concentration using `structure`; neither unique wording nor a different industry label proves a distinct commercial structure. Apply the configured semantic portfolio limits and run only the configured bounded gap scout when required.

Load `knowledge/failure_patterns.md` and relevant history rows only after the fresh pool exists. A repeated family may continue only when a material fingerprint or structure change resolves a recorded objection.

Before research, write `portfolio/selection.json` through kind `portfolio-selection`. It binds the selected candidate versions and hashes, selection rationale, and any missing archetypes observed in the semantic audit. The missing list may be empty; do not invent a universal archetype catalog. The selection is immutable. A later substitution, removal, or version change requires the next ordered `portfolio/amendments/vN.json` through kind `portfolio-amendment`; the amendment hash-binds the immediate prior selection record and states the evidence-backed reason. Never replace a selected candidate silently.

## Research And Working Evaluation

Research every active shortlist entry. Test buyer behavior, current spend and workarounds, pricing and unit economics, acquisition, incumbent response, constraints, founder feasibility, and the recurring proxy errors defined by the artifact contract. Keep sourced contrary evidence separate from unknowns.

Missing customer validation, conversion evidence, signed partners, or private operating data is uncertainty, not a fatal finding. Mark a research result fatal only when direct evidence establishes one of these conditions:

- the offer or required conduct is illegal;
- an essential right cannot be obtained;
- conservative unit economics are mathematically impossible; or
- execution requires a non-delegable founder commitment incompatible with the canonical founder profile.

Every researched candidate receives exactly the configured number of canonical working evaluations before the research stage may advance or terminate. Working evaluators receive the immutable candidate, its research, relevant founder constraints, and evaluator snapshot—but not the target, ranking, generator rationale, or another evaluation. The CLI recomputes all totals.

Create `portfolio/development-decision.json` through kind `portfolio-decision`. Rank eligible candidates by recomputed working score, then Economics, Distribution, lower initial cash, and stable candidate ID. Select no more than the configured development maximum. The CLI verifies evaluation coverage before accepting the record; each candidate decision preserves its disposition, rationale, and any direct fatal evidence.

## Construction, Re-evaluation, And Freeze

Give each selected candidate one structural-constructor pass and record `development/<candidate-id>/constructor-result.json` through kind `development-result`. Preserve either:

- a valid new version that changes at least one canonical fingerprint field and structured economics, with the resulting economic effect; or
- `no_valid_redesign`, with the concentrated limiter, attempted structural change, and evidence explaining why no lawful improvement survived.

Do not treat prose polishing as redesign. Preserve the prior version and lineage. Evaluate the final development version afresh even when the constructor preserves the original structure; a parent-version evaluation cannot satisfy the development gate.

Freeze the deterministic highest-ranked final versions up to the configured limit and continue them to holdout. In schema v2, `no_finalist` is available only at scored research when every shortlisted candidate has a validated direct-evidence fatal disposition, so no development candidate exists. Once development begins, the configured top final versions must continue to holdout; a low working score is not an eligibility escape hatch.

## Holdout, Publication, And Campaign Progression

For every frozen finalist, generate one packet bound to the immutable founder and evaluator snapshots, exact candidate version, and canonical lineage research. Give the identical packet independently to the configured fresh native holdout judges. Do not expose the target, working scores, rankings, selection rationale, campaign history, competing candidates, or another judge's output. Valid external evaluations are optional but binding.

After required holdouts and any external import, run `check`, `finalize`, inspect the structured and rendered reports, and `publish`. `no_qualifier` is valid only when at least one finalist completed required holdouts and failed the configured rule. A scoreless completed cohort is `no_finalist`, never `no_qualifier`.

The CLI uses exit code `4` for a validated terminal result without a qualifier. Treat that as an expected business outcome: inspect the emitted report, publish it, and continue or finalize the campaign as directed. Do not confuse it with an input or state-integrity failure.

For an attached campaign, publish and validate the cohort before asking the CLI for the next action. The CLI alone applies the configured cohort minimum, maximum, improvement signals, plateau patience, and immediate qualification stop. A single regression consumes at most one no-progress step and cannot bypass the configured minimum or patience.

When continuation is allowed, pass new scouts only the CLI-generated sanitized gap brief: deficient factor names and missing semantic archetypes. Never add candidate names, scores, score deltas, rankings, thresholds, selection rationale, or holdout feedback. Stop only on qualification, validated plateau, configured cap, or a visible unrecoverable integrity failure.
