# Business Opportunity Workflow

This repository runs evidence-led, founder-specific opportunity campaigns in Codex. Native subagents perform bounded discovery, batch screening, research, construction, and independent judgment. `scripts/opportunity.py` owns deterministic state, validation, score computation, campaign patience, and publication.

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

`campaign next` is the sole continuation decision and brief generator. A continuation brief contains factor gaps and sanitized missing-archetype labels, never candidate identities, scores, rankings, qualification rules, or holdout feedback. The labels can guide later discovery, but they do not count as progress or reset campaign patience. Only the configured score-improvement signals and campaign limits determine continuation. The first cohort has no prior brief. The policy values live only in `config/opportunity-workflow.json`.

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

Before starting any structured-output job, obtain its role-specific contract and preflight the returned file without consuming an attempt:

```text
python3 scripts/opportunity.py preflight <run-id> --kind <kind>
python3 scripts/opportunity.py preflight <run-id> --kind <kind> --job-id <job-id> --input <file> --original-input <preserved-first-response>
python3 scripts/opportunity.py job <run-id> <job-id> start --stage <stage>
python3 scripts/opportunity.py job <run-id> <job-id> complete --kind <kind> --input <file> --preflight-sha256 <digest> --preflight-receipt-sha256 <receipt-digest>
```

Preflight returns the exact JSON skeleton, enums, role-relevant constraints, canonical evaluator factor names where applicable, and the first RFC 6901 pointer error from the same canonical validator used at completion. It never writes run state or consumes an attempt. Preserve the first substantive response outside managed state and supply it through `--original-input` on every input preflight, including after correction; retain the comparison result with that response. Schema corrections must leave claims, scores, rationales, evidence assessments, and other semantic content unchanged. The original author may trim surrounding whitespace from a string; internal content and structure must remain unchanged. A successful input preflight with the intended job ID returns both the raw input digest and a contextual receipt digest. Structured completion requires both; the full receipt is preserved in its lifecycle event and checked against the immutable run, stage, job, kind, input digest, and canonical artifact digest.

Screening evaluators use a role-safe batch view:

```text
python3 scripts/opportunity.py status <run-id> --batch <batch-id>
```

It returns only that lane-balanced batch plus immutable founder and evaluator bindings. It omits other batches, scores, rankings, portfolio state, unrelated jobs, campaign state, and history. Returned artifact and snapshot paths are relative to the run directory. Include that directory in each scoped assignment, and require the role to read and hash-verify each returned snapshot.

When the configured primary cutoff is close, `advance` writes the deterministic secondary plan and remains in calibration. Assign every listed set to a fresh evaluator through the candidate-only view and the `secondary-evaluation` artifact kind:

```text
python3 scripts/opportunity.py status <run-id> --secondary-batch <secondary-batch-id>
python3 scripts/opportunity.py preflight <run-id> --kind secondary-evaluation
```

The scoped view omits primary scores, ranks, cutoff data, and selection rationale. The CLI records and deterministically aggregates the primary and secondary inputs before generating the shortlist.

Candidate-only researchers use the role-safe view instead of broad status:

```text
python3 scripts/opportunity.py status <run-id> --candidate <candidate-id>
```

It returns only that active shortlist ref, its candidate artifact, the immutable founder binding, and its research path/status. It omits other candidates, portfolio rationale, rankings, scores, evaluation coverage, unrelated jobs, and campaign state.

Constructors and development evaluators likewise use bounded contexts:

```text
python3 scripts/opportunity.py status <run-id> --constructor <candidate-id>
python3 scripts/opportunity.py status <run-id> --development-lineage <candidate-id>
```

The constructor view contains the admitted candidate and research but no evaluator, score, rank, or qualification context. The development view contains both immutable lineage versions under the same evidence and evaluator bindings, without prior scores.

The skill drives discovery, exact deduplication, lane-balanced score screening, shortlist binding, research, working evaluation, construction, paired version re-evaluation, exact-reference freeze, and holdout. Relevant deterministic commands include:

```text
python3 scripts/opportunity.py dedup <run-id>
python3 scripts/opportunity.py advance <run-id>
python3 scripts/opportunity.py export-external <run-id> <candidate-id>
python3 scripts/opportunity.py holdout-assignment <run-id> <candidate-id> --response-destination <fresh-temp.json>
python3 scripts/opportunity.py finalize <run-id>
python3 scripts/opportunity.py publish <run-id>
python3 scripts/opportunity.py quarantine-outcome <run-id> --reason-code <code> --reason "<evidence>"
```

For each initial scout, `python3 scripts/opportunity.py scout-contract <run-id> --lane <lane>` returns only its discovery contract, founder binding and an exact-size JSON output schema generated from canonical configuration and the candidate template. Supply that schema to the transport before generation, preserve its first complete response, and preflight each extracted candidate unchanged. The skill includes a macOS bounded-role launcher for this transport; required fields and counts are constrained before submission, while the CLI remains the admission validator. Proposed control rights remain unproven until supported by evidence.

Use `--help` before non-default inputs. Global options precede the subcommand.
For both cohort and campaign finalization, exit code `4` denotes a validated terminal result without a qualifier; it is not an integrity failure. Inspect and publish the emitted result. Input and state conflicts use different exit codes.

The only scoreless active-schema closure is an all-direct-fatal decision after fully scored research:

```text
python3 scripts/opportunity.py finalize <run-id> --no-finalist-reason "<evidence-backed reason>"
```

Once development begins, the deterministic top lineage-winning versions continue through holdout.

## Decision Integrity

Discovery creates an immutable candidate v1. Its commercial core—title, thesis, fingerprint, structure, critical-control-point contract, commercial mechanics, structural signature, and economics—cannot be rewritten during research. Research is stored separately and hash-binds that exact v1. The score-selected shortlist is generated and immutable; it cannot be editorially substituted. Development may create a v2 only after the portfolio decision admits that candidate and only as a declared structural redesign with changed commercial structure and economics.

Exact fingerprint uniqueness and semantic portfolio variety are distinct measurements. Every candidate records a controlled structural signature so equivalent commercial mechanisms collide despite different wording, industries, or geographies; `other` retains a normalized descriptor. The permanent discovery lanes remain orthogonal: mechanism-first begins with realistically obtainable control and an existing paid event; weak-signal begins with an observed purchasing, workaround, pricing, labor-allocation, or transaction change; future-backcast begins with a future operating state missing a physical, contractual, financial, or coordination mechanism. The configured mechanism-first reserve is grounded in lawful founder access or operating relationships and never assumes confidential employer resources.

After exact deduplication, the CLI generates deterministic lane-balanced screening batches. A fresh evaluator scores every candidate in one batch, and evaluator identities cannot cross batches. A configured close cutoff creates a deterministic secondary set around that batch boundary; its fresh evaluator receives candidates only, and the CLI aggregates both scores by the configured canonical rule. The CLI advances the resulting top prefix, deduplicates winners by structural signature, and backfills a removed slot from the next-highest candidate in that same batch. It then generates immutable `portfolio/selection.json`. There is no core/wildcard eligibility gate: future-facing and weak-signal ideas survive through their independent lanes and compete by score like every other idea.

Every researched candidate must have complete canonical working-evaluation coverage. An evaluator authors one strict JSON response containing factor judgments, adjustment, assumptions, and diagnostics. The CLI attaches immutable identity, validates exclusions, applies rubric weights, constrains and rounds the score, and derives qualification. There is no separate authored score wrapper and no model-provided total to reconcile.

The CLI ranks nonfatal research candidates by recomputed working score, using stable candidate ID only for an exact tie. Each selected candidate receives one constructor result. The immutable original and every admitted redesign are then freshly evaluated by the same evaluator within that lineage. A redesign wins only if its fresh score is strictly higher; equal or lower preserves the original. A valid adverse evaluation and a valid `no_valid_redesign` result are completed judgments, not retry triggers. Transport, parsing, schema, or incomplete-output failures use the configured mechanical-attempt budget; exhausted failures remain visible and resumable rather than becoming fabricated scores.

Research separately covers buyer or paid-event evidence, distribution and acquisition, fully loaded unit economics, and rights/control/access/contractibility. Each category binds claims and bounded source classes or records an explicit `unknown`; missing private proof remains uncertainty. Only direct evidence of illegality, unobtainable essential rights, impossible conservative economics, or non-delegable founder incompatibility is a fatal research stop.

Research and construction both carry structured falsification coverage for control-point obtainability, incumbent substitutes and responses, unsigned dependencies, willingness/urgency/repeat economics, cold-start and data-moat formation, and ownership of the critical mechanism. The categories reference research claims and may resolve to evidence, inference, or unknown.

Constructors author a hash-free response. Preflight a proposed v2 before starting its canonical candidate job. When research establishes external control, that preflight requires a changed critical-control structure and rejects a v2 that remains externally controlled; honest `unknown` proof is allowed with a concrete acquisition instrument, launch controller, and refusal fallback. After an optional redesign candidate is canonicalized and stored, the CLI derives the exact base and final identity hashes and validates strict lineage. This removes ambiguous hash-only rebinding without weakening any hash or version gate.

The CLI writes `portfolio/version-selection.json` with one deterministic original-or-redesign winner per lineage. Every configured development evaluator assesses both versions under equivalent conditions; the configured conservative aggregation selects a redesign only when it is strictly higher than the original. `portfolio/finalists.json` then hash-binds the top conservative lineage winners. Both versions of one idea cannot occupy finalist slots, and candidates are not copied into a frozen stage.

For each finalist, the main agent exports and validates one immutable packet, creates a fresh temporary response path outside managed state, and obtains a `holdout-assignment`. A native holdout receives only that packet, the strict response contract, and the temporary destination. It must not load repository instructions, skills, CLI output, history, prior judgments, rankings, competitors, or another judge's output. The main agent alone performs preflight and canonical job completion/import. The CLI restricts the assignment envelope and destination; preventing an independently launched judge from reading repository files remains an orchestration boundary.

## Terminal Results

- `qualified`: the selected referenced finalist passes the configured strict rule; publication labels it as score-qualified, not empirically market-validated.
- `no_qualifier`: at least one finalist completed required holdouts, but none passed.
- `no_finalist`: all required working evaluations exist, but no candidate reached holdout; official score fields are null.
- `contested`: a binding result prevents confirmation.

Published reports include the structured portfolio decision, evaluation coverage, highest working score, terminal stage, holdout evidence where present, and reopen conditions. Publication also creates `learning-digest.jsonl` with one compact row per researched candidate, linking its structural triple, working limiter, disconfirming evidence, disposition, constructor outcome, fresh evaluation, holdout objection, and reopen condition where applicable. The history index row hash-binds and references this digest. Published artifacts do not depend on links into disposable raw-run directories.

If a completed publication is later proven procedurally invalid, `quarantine-outcome` preserves the original report and history row, adds an immutable hash-bound `quarantine.json` sidecar and append-only history row, and marks the run ineligible for business-decision use. Quarantined material is retained only as workflow-test evidence and must be excluded from delayed-history overlap, scoring, ranking, qualification, and campaign progression. A campaign cohort cannot be quarantined independently because doing so would invalidate its campaign ledger.

## Sources Of Truth

- Founder fit: `PERSONALITY_SITUATION.md`
- Evaluator: `Personalities/ZeroToOne.txt`
- Workflow and campaign policy: `config/opportunity-workflow.json`
- Agent workflow: `.agents/skills/business-opportunity/SKILL.md`
- Historical memory: `knowledge/failure_patterns.md` and `knowledge/history_index.jsonl`
- State and schema validation: `scripts/opportunity.py`

Do not copy numeric canonical values into prompts or documentation. `prompts/PromoLeak/` and its preserved dossier are a separate execution playbook and never enter this workflow.

New control-contract behavior is selected by the complete capability-key set in the immutable config snapshot. Older schema-v3 configurations and already published schema-v2/v3 artifacts retain their original validation and report shapes; no stored state is migrated or rewritten.

## Storage And Verification

Keep an active, failed, interrupted, or unpublished `runs/<run-id>/`. After a terminal cohort passes `check` and `publish`, its outcome and history row are canonical and the raw run may be deleted. Campaign state remains until its terminal receipt validates.

```text
python3 scripts/opportunity.py check
python3 -m unittest discover -s tests -v
```

The repository-level check also verifies every tracked outcome, report-to-artifact hashes, binding external raw-response receipts, learning-digest coverage, complete campaign metric evidence sets, any append-only publication-repair boundary, and each immutable outcome-quarantine sidecar/history binding.

Raw pre-cleanup evidence remains recoverable from the Git checkpoint recorded in `knowledge/history_index.jsonl`.
That checkpoint is also the authority for legacy archaeology; mutation uses only the active workflow schema.
