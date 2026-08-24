# Published Outcomes

`outcomes/<run-id>/` is created only by `python3 scripts/opportunity.py publish` from a finalized terminal run. It contains `report.json`, its derived `report.md`, and canonical lineage research for the preserved candidates. A completed holdout also preserves its selected frozen candidate and binding evaluations; an early closure preserves its strongest latest-stage candidates. Artifact paths stay run-relative, and publication provenance is appended to `knowledge/history_index.jsonl`.

Publication represents one of two honest outcomes:

- a score-qualified candidate labeled exactly `score-qualified under holistic-11; not empirically market-validated`; or
- a non-confirmation or contested report that preserves the selected candidate, binding score limiters, failed work, and unresolved evidence without a qualification label.

Do not create, rename, or edit a published outcome to imply qualification. Do not translate archived scores into the current rubric or promote a candidate from working evaluations. Empirical market validation, build approval, and capital commitment remain separate decisions.

Finalize first, inspect `runs/<run-id>/final/report.json` and `report.md`, then publish the terminal result:

```text
python3 scripts/opportunity.py finalize <run-id>
python3 scripts/opportunity.py publish <run-id>
```

The source run under `runs/<utc-run-id>/` remains the auditable record. Its compact
`opportunity_outcome_v1` history row is an active publication record with outcome,
report, rubric, selected-candidate, score, fingerprint, and terminal-decision
provenance. Legacy `idea` and `run` rows use the separate byte-preserved archive
provenance contract documented in `archive/README.md`.
