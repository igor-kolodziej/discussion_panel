# Discussion Panel Working Agreement

## Purpose

This repository is an agent-native workflow for discovering, researching, developing, independently evaluating, and preserving founder-fit business opportunities. Keep the active system small: Codex owns judgment and bounded delegation; deterministic code owns state, validation, deduplication, imports, and publication.

## Canonical Sources

- `PERSONALITY_SITUATION.md` is the sole founder profile and decision filter.
- `Personalities/ZeroToOne.txt` is the sole evaluator definition and scoring rubric.
- `config/opportunity-workflow.json` is the sole machine-readable workflow, budget, and qualification configuration.
- `scripts/opportunity.py` is the supported interface and schema validator for run state and artifacts.
- `.agents/skills/business-opportunity/SKILL.md` is the active model workflow.
- `knowledge/failure_patterns.md` and `knowledge/history_index.jsonl` are the active historical learning and provenance indexes. Legacy raw material is not part of the active tree; its recovery checkpoint is recorded in the index metadata.

Do not copy numeric rubric weights, founder financial constraints, or qualification thresholds into prompts, skills, or documentation. Link to the canonical source instead.

## Workflow Invariants

- Load `$business-opportunity` for an end-to-end opportunity run or resume.
- The main agent owns canonical state. Give subagents bounded read-only research or judgment tasks; receive their results before writing through the CLI.
- Fresh discovery scouts must not receive historical ideas, the evaluator rubric, the score target, previous verdicts, or candidate rankings. Introduce history only at the configured delayed-dedup stage.
- Working evaluations diagnose and redesign; they never confirm an opportunity.
- Freeze the exact candidate before final evaluation. Use two fresh native holdout judges as the required confirmation basis, isolate them from development context and each other, and bind their shared packet to the run's immutable `inputs/founder.md` and `inputs/evaluator.txt` snapshots, the frozen candidate, and its canonical lineage research.
- Preserve every optional external response raw. Malformed imports remain visibly rejected and contribute no score; every successfully imported valid score is binding and must not be substituted, reinterpreted, or selectively discarded.
- Never lower a configured qualification rule, add an unconfigured retry loop, or convert an archived score to the current rubric.
- A development redesign must change at least one canonical fingerprint field, update structured economics, and record the resulting economic effect; wording-only revisions are invalid.
- Failed and incomplete runs remain visible and resumable. Never manufacture a score or silently skip a failed job.

## PromoLeak Separation

`prompts/PromoLeak/` is the execution playbook for a previously confirmed opportunity. It is not an idea-discovery input, benchmark, historical candidate, or evaluation aid. Do not load, modify, score, or use it from the business-opportunity workflow. Enter it only when the user explicitly asks to execute that separate opportunity.

Its preserved source dossier is `ideas/CONFIRMED_IDEA_20260511_113716.md`. Keep that dossier and the playbook byte-stable unless the user explicitly requests PromoLeak work.

## Generated And Preserved Files

- `runs/<utc-run-id>/` is CLI-managed, resumable run state. Do not hand-edit `manifest.json`, `state.json`, `events.jsonl`, input snapshots, imported holdouts, or publication events.
- `outcomes/<run-id>/` contains CLI-published outcomes. Do not create a confirmed-looking artifact by hand.
- Keep failed, interrupted, or unpublished runs so they can be resumed. After a terminal run passes `check` and `publish`, its raw run directory is disposable because the published outcome and compact history row are canonical.
- Historical digest records are read-only evidence. Do not rewrite their raw score strings, evaluation roles, or conclusions, and never promote them into current candidate or holdout artifacts.
- Do not hard-code machine-specific paths. Keep active references repository-relative.

## Definition Of Done

For workflow or contract changes, run:

```text
python3 scripts/opportunity.py check
python3 -m unittest discover -s tests -v
```

Also exercise the narrow affected command and inspect its generated artifacts. A business run is complete only when it ends in a validated, published terminal outcome, including an explicit non-confirmation or contested report; interruption, exhaustion, and rejection remain visible.
