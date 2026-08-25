# Business Opportunity Workflow

This repository runs evidence-led, founder-specific opportunity campaigns in Codex. Native subagents perform bounded discovery, research, construction, and independent judgment. `scripts/opportunity.py` owns deterministic state, validation, scoring, campaign patience, and publication.

Every researched candidate receives a working score. Working scores guide development but never confirm an opportunity. Final qualification requires fresh native holdouts and any binding external result. A campaign may finish without a qualifier, but it cannot report an unexplained scoreless `no_qualifier`.

## Start In Codex

For the normal multi-cohort workflow, ask:

```text
Use $business-opportunity to start a new scored opportunity campaign.
```

The skill reads the canonical founder profile, evaluator, configuration, and artifact contracts. It keeps discovery blind, uses fresh role-separated subagents, and follows CLI state rather than chat history.

## Campaign Commands

Create a campaign and attach its first cohort:

```text
python3 scripts/opportunity.py campaign new
python3 scripts/opportunity.py new --campaign <campaign-id>
```

Inspect campaign state, obtain the deterministic next action and sanitized brief, or finalize a terminal campaign:

```text
python3 scripts/opportunity.py campaign status <campaign-id>
python3 scripts/opportunity.py campaign next <campaign-id>
python3 scripts/opportunity.py campaign finalize <campaign-id>
```

`campaign next` is the sole continuation decision and brief generator. A continuation brief contains factor gaps and missing semantic archetypes, never candidate identities, scores, rankings, qualification rules, or holdout feedback. The first cohort has no prior brief. The policy values live only in `config/opportunity-workflow.json`.

Campaign state is generated under `campaigns/<campaign-id>/`. Its founder profile, evaluator, and policy are snapshotted for the whole campaign. Each published cohort is recorded idempotently with score coverage and an immutable `campaign-metrics.json` that hash-binds progress metrics to the complete published evidence set. Finalization publishes an auditable bundle to tracked `outcomes/campaigns/<campaign-id>/`: receipt, report, manifest, events, canonical input snapshots, and sanitized continuation briefs.

## Cohort Commands

Create a standalone cohort only when a campaign is not requested:

```text
python3 scripts/opportunity.py new
```

Inspect or recover a cohort:

```text
python3 scripts/opportunity.py status <run-id>
python3 scripts/opportunity.py status <run-id> --json
python3 scripts/opportunity.py resume <run-id>
python3 scripts/opportunity.py check <run-id>
```

The skill drives discovery, deduplication, shortlist binding, research, working evaluation, construction, re-evaluation, freeze, and holdout. Relevant deterministic commands include:

```text
python3 scripts/opportunity.py dedup <run-id>
python3 scripts/opportunity.py advance <run-id>
python3 scripts/opportunity.py export-external <run-id> <candidate-id>
python3 scripts/opportunity.py finalize <run-id>
python3 scripts/opportunity.py publish <run-id>
```

Use `--help` before non-default inputs. Global options precede the subcommand.
For both cohort and campaign finalization, exit code `4` denotes a validated terminal result without a qualifier; it is not an integrity failure. Inspect and publish the emitted result. Input and state conflicts use different exit codes.

The only scoreless schema-v2 closure is an all-direct-fatal decision after fully scored research:

```text
python3 scripts/opportunity.py finalize <run-id> --no-finalist-reason "<evidence-backed reason>"
```

Once development begins, the deterministic top final versions continue through holdout.

## Decision Integrity

Research is bound to immutable `portfolio/selection.json`; substitutions require a chained versioned amendment. Exact fingerprint uniqueness and semantic portfolio variety are distinct measurements. Every candidate also declares its commercial archetype, control point, and critical dependency.

Every researched candidate must have complete canonical working-evaluation coverage. The CLI ranks eligible development candidates by recomputed working score, Economics, Distribution, initial cash, and stable ID. Each selected candidate receives one constructor result and a fresh evaluation of its final development version.

Missing customer proof or partner commitment remains uncertainty. Only direct evidence of illegality, unobtainable essential rights, impossible conservative economics, or non-delegable founder incompatibility is a fatal research stop.

For each frozen finalist, the CLI exports one packet bound to the run's immutable founder and evaluator snapshots, exact candidate version, and lineage research. Fresh native judges receive the same packet independently. Optional external responses use that packet and become binding once validly imported.

## Terminal Results

- `qualified`: the selected frozen candidate passes the configured strict rule; publication labels it as score-qualified, not empirically market-validated.
- `no_qualifier`: at least one finalist completed required holdouts, but none passed.
- `no_finalist`: all required working evaluations exist, but no candidate reached holdout; official score fields are null.
- `contested`: a binding result prevents confirmation.

Published reports include the structured portfolio decision, evaluation coverage, highest working score, terminal stage, holdout evidence where present, and reopen conditions. They do not depend on links into disposable raw-run directories.

## Sources Of Truth

- Founder fit: `PERSONALITY_SITUATION.md`
- Evaluator: `Personalities/ZeroToOne.txt`
- Workflow and campaign policy: `config/opportunity-workflow.json`
- Agent workflow: `.agents/skills/business-opportunity/SKILL.md`
- Historical memory: `knowledge/failure_patterns.md` and `knowledge/history_index.jsonl`
- State and schema validation: `scripts/opportunity.py`

Do not copy numeric canonical values into prompts or documentation. `prompts/PromoLeak/` and its preserved dossier are a separate execution playbook and never enter this workflow.

## Storage And Verification

Keep an active, failed, interrupted, or unpublished `runs/<run-id>/`. After a terminal cohort passes `check` and `publish`, its outcome and history row are canonical and the raw run may be deleted. Campaign state remains until its terminal receipt validates.

```text
python3 scripts/opportunity.py check
python3 -m unittest discover -s tests -v
```

Raw pre-cleanup evidence remains recoverable from the Git checkpoint recorded in `knowledge/history_index.jsonl`.
That checkpoint is also the authority for schema-v1 archaeology; the active workflow creates schema-v2 artifacts.
