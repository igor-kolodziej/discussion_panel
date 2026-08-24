# Generated Runs

`runs/<utc-run-id>/` contains the resumable working state for one opportunity workflow. Create and operate runs with `python3 scripts/opportunity.py`; do not assemble a run directory or edit its state by hand.

The important top-level artifacts are:

- `manifest.json`, `state.json`, and CLI-managed `events.jsonl` for identity, current state, and a contiguous append-only transition history;
- `inputs/` for frozen canonical founder, evaluator, and config snapshots;
- `discovery/`, `research/`, and `evaluations/` for bounded work and provenance;
- `candidates/<candidate-id>/v<version>.json` for immutable candidate versions;
- `exports/` and `holdout/` for clean packets, required native holdout records, and any optional external responses and validated imports; and
- `final/report.json` and its derived `report.md` rendering for the terminal result, including non-confirmation or contested status.

Use these commands to inspect and recover a run:

```text
python3 scripts/opportunity.py status <run-id>
python3 scripts/opportunity.py resume <run-id>
python3 scripts/opportunity.py check <run-id>
```

A failed or interrupted run is retained and resumed from its last validated transition. Do not delete it merely because it did not qualify an opportunity. See `.agents/skills/business-opportunity/references/artifact-contracts.md` for the full placement and write contract.
