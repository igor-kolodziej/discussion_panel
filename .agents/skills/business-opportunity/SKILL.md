---
name: business-opportunity
description: Run or resume this repository's founder-fit business opportunity workflow or scored campaign when asked to discover, research, develop, deduplicate, independently evaluate, externally score, finalize, or publish opportunities. Do not use for the separate PromoLeak playbook or casual idea discussion.
---

# Business Opportunity

Operate the repository workflow; do not invent a parallel process. The main agent owns canonical state and delegates bounded, role-separated work. The CLI owns validation, scoring, transitions, campaign patience, imports, and publication.

## Begin Or Resume

1. Read `AGENTS.md`, `config/opportunity-workflow.json`, and current CLI help.
2. Read `PERSONALITY_SITUATION.md` as the founder filter. Load `Personalities/ZeroToOne.txt` only for evaluation, never to shape discovery.
3. Create or resume the requested run or campaign through the CLI. Follow recorded state; never reconstruct it from chat or hand-edit managed files.
4. Read [workflow.md](references/workflow.md) before assigning work or advancing a stage. Read [artifact-contracts.md](references/artifact-contracts.md) before producing a canonical artifact.

## Execute A Cohort

- Keep scouts blind to history, the rubric, target, scores, rankings, verdicts, and one another. Form the fresh pool before delayed history review.
- Record exact fingerprint uniqueness and a separate semantic portfolio audit. Bind the selected research set in the immutable shortlist; use a validated amendment for any substitution.
- Research every shortlisted candidate, distinguish evidence, inference, and unknowns, and apply the narrow fatal-evidence rules. Missing validation remains uncertainty.
- Give every researched candidate its required fresh working evaluation. Research cannot advance or terminate until coverage is exact and complete.
- Let the CLI rank the eligible pool and select the configured development set. Preserve one constructor result per selected candidate: either a structural redesign with changed economics or `no_valid_redesign` with evidence.
- Give each final development version a fresh working evaluation. An earlier version's result does not satisfy the gate.
- Freeze the deterministic top-ranked final versions. Only an all-direct-fatal scored research decision may close `no_finalist`; once development starts, continue its configured top versions to holdout. Export the shared packet, then use fresh context-isolated native holdout judges with distinct role provenance. Follow [history-and-holdout.md](references/history-and-holdout.md). Every valid external import is binding.

## Continue A Campaign

Publish and validate each terminal cohort, then let the CLI determine whether the campaign qualifies, continues, plateaus, or reaches its configured cap. For continuation, give scouts only the generated sanitized gap brief. Do not reveal candidate identities, scores, rankings, qualification rules, selection rationale, or holdout feedback, and do not add unconfigured search loops.

## Keep State Visible

Use `status` before acting and `check` after recovery, import, finalization, or publication. Record every job start, completion, failure, and constructor outcome through the CLI. The CLI records and checks evaluator, constructor, and holdout identities; keep scout and researcher contexts distinct in orchestration. Mechanical retries follow config; quality rejection is not retried.

## Finish

Finalize, inspect the structured report and rendered report, and publish. Terminal semantics are strict:

- `qualified`: required holdouts and any binding external results pass the configured rule;
- `no_qualifier`: at least one finalist completed required holdouts, but none passed;
- `no_finalist`: required working evaluations exist, but no candidate reached holdout, so official scores are null; or
- `contested`: a binding result prevents confirmation.

Preserve strongest-candidate diagnostics and reopen evidence without implying market validation. Never manufacture a score or use `no_qualifier` for a scoreless run.

Do not enter `prompts/PromoLeak/` unless the user explicitly requests that separate playbook.
