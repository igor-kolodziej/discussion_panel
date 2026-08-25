# Discussion Panel Working Agreement

## Purpose

This repository is an agent-native workflow for discovering, researching, developing, independently evaluating, and preserving founder-fit business opportunities. Codex owns judgment and bounded delegation; deterministic code owns state, validation, scoring, campaign progression, imports, and publication.

## Canonical Sources

- `PERSONALITY_SITUATION.md` is the sole founder profile and decision filter.
- `Personalities/ZeroToOne.txt` is the sole evaluator definition and scoring rubric.
- `config/opportunity-workflow.json` is the sole machine-readable workflow, budget, campaign, and qualification configuration.
- `scripts/opportunity.py` is the supported interface and schema validator.
- `.agents/skills/business-opportunity/SKILL.md` is the active model workflow.
- `knowledge/failure_patterns.md` and `knowledge/history_index.jsonl` are delayed historical memory. Legacy raw material is recoverable from the checkpoint recorded in the index metadata, not from the active tree.

Do not copy rubric weights, founder financial constraints, workflow maxima, campaign thresholds, or the qualification threshold into prompts, skills, or documentation. Read them from their canonical source.

## Workflow Invariants

- Load `$business-opportunity` for an end-to-end run, campaign, or resume. The main agent is the only canonical writer; subagents return bounded work for validation through the CLI.
- Keep fresh discovery blind to history, the evaluator, target score, rankings, previous verdicts, and other scouts. Introduce history only after the fresh pool has been deduplicated.
- Report exact fingerprint uniqueness only as `exact_fingerprint_unique_count`. Separately audit semantic variety using each candidate's commercial archetype, control point, and critical dependency.
- Bind research to an immutable structured shortlist. A substitution requires a validated versioned amendment; never silently research a different candidate.
- Every researched candidate must receive exactly the configured number of canonical working evaluations before research can advance or terminate. Working evaluations diagnose and rank; they never confirm.
- Treat missing validation, conversion, partner commitment, and other absent evidence as uncertainty. A research finding is fatal only when direct evidence establishes illegality, unobtainable essential rights, impossible conservative economics, or a non-delegable founder incompatibility.
- Select development candidates deterministically from recomputed working evaluations using the configured ranking and limit. Preserve one constructor result per selected candidate: either a valid structural redesign with changed economics or explicit `no_valid_redesign` evidence.
- Evaluate the final development version afresh. An ancestor's evaluation cannot satisfy its gate. Freeze the configured deterministic top-ranked prefix; once development begins, low working scores do not bypass holdout.
- Keep discovery, research, working evaluation, construction, and holdout contexts distinct. The CLI mechanically enforces recorded working-evaluator, constructor, and holdout identity separation; scout and researcher context separation remains the main agent's assignment duty. Holdout judges are fresh, isolated from development context and each other, and receive the same packet bound to the frozen candidate and immutable run inputs.
- A candidate is qualified only by the configured strict rule applied to required holdouts and every binding external result. Never lower the rule, retry for a favorable score, or convert a historical score.
- `no_finalist` means evaluation coverage completed but no candidate reached holdout, so official score fields are null. `no_qualifier` requires at least one fully held-out finalist with a non-passing official score. Never use either status to hide incomplete required work.
- Continue campaign cohorts according to the configured minimum, maximum, progress, and plateau rules. Later scouts receive only the CLI-generated sanitized gap brief; never expose candidate identities, scores, rankings, thresholds, selection rationale, or holdout feedback.
- Failed and incomplete work remains visible and resumable. Never manufacture a score, silently skip a job, or hand-edit CLI-managed state.

## PromoLeak Separation

`prompts/PromoLeak/` is the execution playbook for a previously confirmed opportunity. It is not a discovery input, benchmark, historical candidate, or evaluation aid. Do not load, modify, score, or use it from this workflow. Its required dossier is `ideas/CONFIRMED_IDEA_20260511_113716.md`; keep both byte-stable unless the user explicitly requests PromoLeak work.

## Generated And Preserved Files

- `runs/<utc-run-id>/` is CLI-managed resumable cohort state; `campaigns/<campaign-id>/` is CLI-managed cross-cohort state. Do not hand-edit either.
- `outcomes/<run-id>/` contains CLI-published cohort outcomes and corrections. Do not create a confirmed-looking artifact by hand.
- Keep failed, interrupted, or unpublished runs. After a terminal run passes `check` and `publish`, its raw directory is disposable because the published outcome and compact history row are canonical.
- Historical digest records are read-only evidence. Do not rewrite their raw scores, roles, or conclusions or promote them into current artifacts.
- Keep active paths repository-relative.

## Definition Of Done

For workflow or contract changes, run:

```text
python3 scripts/opportunity.py check
python3 -m unittest discover -s tests -v
```

Also exercise the affected command and inspect generated artifacts. A cohort is complete only when it has a validated published terminal outcome; a campaign is complete only when its deterministic stop reason and receipt validate.
