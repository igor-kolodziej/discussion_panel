---
name: business-opportunity
description: Run or resume this repository's founder-fit business opportunity workflow when asked to discover, research, develop, deduplicate, independently evaluate, externally score, finalize, or publish an opportunity. Use for end-to-end opportunity runs and recovery from interrupted runs. Do not use for the separate PromoLeak execution playbook or for casual discussion of an idea outside this repository workflow.
---

# Business Opportunity

Operate the repository workflow; do not invent a parallel process. The main agent owns the run and delegates narrow, independent work. Deterministic commands own state transitions, validation, deduplication, external-score imports, and publication.

## Begin Or Resume

1. Read `AGENTS.md`, `config/opportunity-workflow.json`, and the CLI help.
2. Read `PERSONALITY_SITUATION.md` as the founder filter. Read `Personalities/ZeroToOne.txt` only when preparing or performing evaluation, never as discovery-scoring guidance.
3. For a new run, call `python3 scripts/opportunity.py new`. For an existing run, call `status`; call `resume` only when it is active and needs interrupted-job recovery.
4. Follow the stage recorded in `state.json`. Do not reconstruct state from transcripts or hand-edit CLI-managed files.

## Execute The Run

- Begin with the three evidence lanes in [workflow.md](references/workflow.md). Give scouts only their scoped question, relevant founder facts, evidence requirements, and output contract. Do not expose history, rubric, target, rankings, or prior verdicts.
- Preserve returned work through the CLI job contract. The main agent validates and writes canonical artifacts; subagents do not edit the run.
- Form a structurally varied fresh pool before reading history. Then load `knowledge/failure_patterns.md` and only relevant rows from `knowledge/history_index.jsonl`; run the exact six-field fingerprint and configured similarity checks.
- Research material assumptions and distinguish sourced evidence, inference, and unknowns. Run the proxy checks before finalist selection.
- Use the canonical evaluator for working diagnosis. Keep generation, research, working evaluation, redesign, and final judgment role-separated.
- Use one bounded structural-redesign pass during `development` for near-winners. Change the business structure, not merely the prose, and create a new candidate version.
- Treat every configured maximum stage, retry, and candidate budget as a hard stop. Never add adaptive loops or lower qualification rules. When the budget is exhausted before holdout and no current job remains running or retryable, call `python3 scripts/opportunity.py finalize <run-id> --no-qualifier-reason "<reason>"` with a specific evidence-backed reason; when multiple candidates survive at the strongest stage, also pass `--best-candidate <candidate-id>`.
- Freeze each finalist version before final judgment. For every frozen candidate, call `export-external` to generate the required shared packet. After all packets validate, advance to `holdout`, then give each identical packet to two fresh native judges. The command name does not make external submission mandatory. Follow [history-and-holdout.md](references/history-and-holdout.md); every successfully imported valid external score is binding.

## Keep State Visible

Use `status` before acting and `check` after recovery or import. Record job start, completion, or failure with `scripts/opportunity.py`; never silently skip a job or substitute a score. Resume from the last validated transition.

Read [artifact-contracts.md](references/artifact-contracts.md) before writing or importing any run artifact.

## Finish

Call `finalize`, inspect `final/report.json` and `report.md`, then call `publish`. A terminal result must be either:

- a qualifying frozen candidate supported by the required native holdouts and any imported external holdout, labeled `score-qualified under holistic-11; not empirically market-validated`; or
- a published non-confirmation or contested result that preserves the strongest candidates, binding limiters, failed jobs, and unresolved evidence without implying qualification.

Do not enter `prompts/PromoLeak/` unless the user explicitly requests that separate execution playbook.
