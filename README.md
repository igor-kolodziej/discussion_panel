# Business Opportunity Workflow

This repository runs an evidence-led, founder-specific business-opportunity process in Codex. Native subagents do bounded discovery, research, and independent judgment. `scripts/opportunity.py` keeps the run state deterministic, validated, resumable, and auditable.

The workflow can end honestly without a qualifying opportunity. Two fresh native holdout judges provide the required independent confirmation; working scores are development feedback. External holdouts are optional, but every successfully imported valid external score is binding.

## Start In Codex

Ask Codex:

```text
Use $business-opportunity to start a new opportunity run.
```

To continue an interrupted run, give the run ID:

```text
Use $business-opportunity to resume <run-id>.
```

`prompts/NEW_IDEA_GOAL.md` is a thin compatibility prompt for the same skill.

## Operator Commands

Create a run:

```text
python3 scripts/opportunity.py new
```

The command creates `runs/<utc-run-id>/` and snapshots the canonical founder profile, evaluator, and workflow config. Use the emitted run ID in later commands.

Inspect or resume it:

```text
python3 scripts/opportunity.py status <run-id>
python3 scripts/opportunity.py status <run-id> --json
python3 scripts/opportunity.py resume <run-id>
```

The skill normally drives the remaining state transitions. Useful recovery and validation commands are:

```text
python3 scripts/opportunity.py check <run-id>
python3 scripts/opportunity.py dedup <run-id>
python3 scripts/opportunity.py advance <run-id>
```

If configured limits are exhausted before holdout, first finish or exhaust every current-stage job, then close honestly with a specific evidence-backed reason:

```text
python3 scripts/opportunity.py finalize <run-id> --no-qualifier-reason "<reason>"
```

If more than one candidate exists at the strongest current stage, also pass `--best-candidate <candidate-id>`. This makes the preserved best candidate, primary limiter, contrary evidence, and reopen condition explicit. Non-qualification is still a successful workflow outcome; inspect and publish its reports rather than adding another unconfigured generation loop.

Run any command with `--help` before supplying non-default paths. Global options such as `--config` and `--runs-dir` must precede the subcommand.

## Independent Holdout

After development, the skill freezes each finalist. For every frozen candidate, it generates one evidence packet bound to the run's immutable founder and evaluator snapshots and canonical candidate-lineage research. Two fresh native judges evaluate that same packet independently through normal evaluation jobs. They do not see development scores, rankings, the qualification rule, selection rationale, or each other's output.

Materialize the deterministic packet for each frozen candidate:

```text
python3 scripts/opportunity.py export-external <run-id> <candidate-id>
```

Despite the command name, packet generation is required for native holdout and does not require an external judge. The packet and response contract are written to `runs/<run-id>/exports/<candidate-id>/`.

Use `status` to inspect the holdout job records. The main agent preserves each raw return and records its canonical result with the CLI job contract and `--kind evaluation`; malformed or incomplete results fail visibly rather than becoming scores.

### Optional External Holdout

To add an external browser judge, submit the same packet in a fresh conversation, save the complete raw response, and import it without editing:

```text
python3 scripts/opportunity.py import-external <run-id> <candidate-id> <raw-response-file>
```

External evaluation is optional. A malformed or incomplete response is preserved as a visible rejected import and contributes no score. Every successfully imported valid score is binding, including an adverse one; it cannot be replaced by a working evaluation or selectively ignored.

If holdout feedback causes any candidate change, preserve the failed frozen version and create a new version in a new run with fresh judges. A revised dossier cannot reuse the current run's holdouts.

Finalize after the required native holdouts and any optional external import are complete:

```text
python3 scripts/opportunity.py finalize <run-id>
```

Inspect `runs/<run-id>/final/report.json` and the concise `runs/<run-id>/report.md`, then publish the terminal result:

```text
python3 scripts/opportunity.py publish <run-id>
```

Published results appear under `outcomes/<run-id>/`, including honest non-confirmation and contested outcomes. Only a score-qualified dossier carries the label `score-qualified under holistic-11; not empirically market-validated`.

## Sources Of Truth

- Founder fit: `PERSONALITY_SITUATION.md`
- Evaluator: `Personalities/ZeroToOne.txt`
- Workflow configuration: `config/opportunity-workflow.json`
- Operational workflow: `.agents/skills/business-opportunity/SKILL.md`
- Active historical learning: `knowledge/failure_patterns.md` and `knowledge/history_index.jsonl`
- State, artifact contracts, and validation: `scripts/opportunity.py`

Do not copy their numeric values into another prompt. `prompts/PromoLeak/` is a separate execution playbook and is never loaded by this discovery workflow.

## Archive Boundary

All pre-takeover ideas, runs, managers, prompts, failure receipts, debug evidence, and externally referenced protocol snapshots remain byte-preserved under `archive/`. [`archive/README.md`](archive/README.md) explains rubric generations and restoration; `archive/manifest.jsonl` records each preserved source path, destination, byte size, and SHA-256. Active code never imports from the archive, and historical binary, `/100`, unknown-framework, and current `/10` results are never converted into a shared numeric scale.

## Verification

```text
python3 scripts/opportunity.py check
python3 -m unittest discover -s tests -v
```

See `runs/README.md` for run artifacts and `outcomes/README.md` for publication
semantics. `docs/TAKEOVER_REPORT.md` records the migration and verification;
`docs/LIVE_SMOKE_REPORT.md` records the bounded native rehearsal.
