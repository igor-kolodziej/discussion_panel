# Codex-Native Opportunity System Takeover

## Outcome

The repository now uses a repository-local Codex skill and one standard-library Python utility instead of the legacy v2 orchestration experiments. Canonical founder and evaluator files remain unchanged from the pre-takeover checkpoint, unrelated `prompts/PromoLeak/` work remains separate and unchanged, and historical evidence is isolated behind a verified byte-preserving archive boundary.

The replacement is designed to produce one of two honest results: a score-qualified frozen dossier under the configured current rubric, or a durable non-confirmation/contested outcome. It does not promise that a qualifying business exists and does not describe a model score as empirical demand validation.

## Recovery And Archive Boundary

- Branch: `dev/agent-native-takeover`.
- Pre-takeover checkpoint: `bac20e3` (`chore: checkpoint pre-takeover state`).
- Primary archive move: `ff12af0` (`chore: archive legacy opportunity machinery`).
- Archive reconciliation: `c7f8ec4` (`chore: complete legacy archive boundary`).
- Final tracked browser-setup reconciliation: `daf7104` (`chore: reconcile remaining legacy browser setup`).
- Replacement implementation: `4483cb9` (`feat: add resumable Codex-native opportunity workflow`).
- Clean-export empty-tree verification: `8f9d153` (`test: verify empty archived runs in clean exports`).
- Manifest: `archive/manifest.jsonl`.
- Manifest SHA-256: `b3f93cae5150023c5a32af5a6b4caa3d47b3da73bff4d69a974a15e8716b224e`.
- Reconciled destinations: 2,441, comprising 2,436 moved repository files and five external protocol snapshots.
- Reconciled bytes: 23,867,597.
- Verification: every destination size and SHA-256 matches the manifest; every move matches the corresponding blob in checkpoint `bac20e3`; every moved source is absent; all five external snapshots still match their source; no extra legacy-tree file is outside the manifest.

The archive includes the exact latest five unadmitted v2 agent returns as historical evidence. Old binary, `/100`, mixed, unknown, and current `/10` records retain their original framework and scale labels and are never numerically converted. `archive/README.md` documents restoration and provenance.

Generated caches and obsolete session material were removed only after preservation checks: `.playwright-cli/`, Python caches, Finder caches, and the empty tracked file `87`. The two tracked gstack setup examples were archived because they belonged to the retired browser-startup path. Ignored `.gstack` browser profiles, tokens, and sessions were deliberately retained because Git cannot recover their authentication state.

`prompts/PromoLeak/` is byte-identical to checkpoint `bac20e3` and remains outside discovery, calibration, and evaluation.

## Active Architecture

- `AGENTS.md` defines the source hierarchy, role separation, delayed-history rule, holdout integrity, visible failure behavior, and PromoLeak boundary.
- `.agents/skills/business-opportunity/` contains the repository-local operational workflow and focused artifact/history/holdout references.
- `config/opportunity-workflow.json` is the only active machine-readable source for qualification logic and workflow budgets.
- `scripts/opportunity.py` is the only active runtime. It performs deterministic validation, scoring, deduplication, atomic state changes, resumption, imports, finalization, and publication; it does not orchestrate agents.
- `knowledge/history_index.jsonl` is a scale-isolated provenance/fingerprint index over all preserved idea and run roots. Its legacy contract covers 15 idea files and 37 run trees; file and canonical tree hashes reconcile 2,361 constituent run files to the archive manifest. Active published outcomes use a distinct exact record contract rather than pretending to be archived legacy sources.
- `knowledge/failure_patterns.md` is the compact structural-failure catalog used only after blind discovery.
- `runs/` contains ignored resumable local runs; `outcomes/` contains small publishable terminal decisions.

There is no active agent platform, database, browser controller, private Codex-session inspection, wrapper parser, trace anchor, token meter, global mutable skill dependency, or compatibility layer for retired v2 commands. Production code imports only the Python standard library and never imports from `archive/`.

## Deterministic Guarantees

At run creation, the utility parses the canonical evaluator, verifies its factor count and total weight, hashes all canonical sources, and stores immutable founder, evaluator, and config snapshots. Every later command validates those snapshots against the manifest before acting.

Candidate, research, and evaluation records use strict key sets, stage/version lineage, content hashes, and canonical paths. Candidate revisions require the same stable ID and immediately preceding version. The one permitted same-stage development redesign must declare and actually change at least one normalized fingerprint field, update structured economics, and explain the economic effect; a prose-only pivot is rejected. A finalist must preserve one same-ID discovery → research → development → frozen lineage, and its exact development parent must have a canonical working evaluation; unrelated candidate work cannot satisfy its gate. Decision-critical research distinguishes evidence, inference, unknowns, and contrary evidence. Frozen candidates require a numeric nonnegative initial-capital value so the final cash tie-break cannot depend on prose parsing.

Evaluation arithmetic is recomputed with `Decimal`, proportional exclusion renormalization, the canonical interaction range and score constraint, explicit half-up rounding, and the strict configured comparison. Model-supplied totals are rejected when they differ. Working evaluations cannot qualify a candidate. Native holdouts bind to a frozen candidate, canonical packet, distinct structured raw responses, exact rubric snapshot, and two distinct judges. Valid external imports are binding gates; malformed imports remain preserved and visibly rejected without acquiring a score.

State and artifacts are written atomically under scoped, symlink-safe locks. Artifact-first and state-first interruption boundaries are recoverable and idempotent; completed work is not repeated; conflicting immutable content requires a new candidate version; mechanical retries stop at the configured attempt limit. Event projection covers job lifecycle as well as run stages. Packet export and publication repair a missing event after a durable write without duplicating it. Final-report derivation is validated rather than trusted as editable prose. An early non-confirmation with multiple surviving candidates requires an explicit best-candidate choice and carries that candidate's primary limiter, contrary evidence, and reopen condition into publication history.

## Historical Calibration

The representative current-rubric recalibration is recorded in `docs/HISTORICAL_CALIBRATION.md`. It ignored every archived score and label, performed no cross-scale conversion, and produced the directional ordering HeritageDoor, refrigeration-loss monitoring, TraceFaktura, then DSR commissioning. HeritageDoor's physical control point ranked above the service/data-asset patterns, while still failing to establish sufficient inventory turnover and founder-wealth throughput.

The comparison supports recurring-limiter detection, not exact future scores or qualification. Service-created datasets remained weak where partners or incumbents controlled the customer, source data, regulated action, and distribution.

## Native Smoke And Quality Comparison

The bounded native rehearsal is recorded in `docs/LIVE_SMOKE_REPORT.md`. Run
`20260824T180642Z-260b79` exercised initialization, status, resumption, blind
discovery, deduplication, delayed history, research, working evaluation,
same-candidate freezing, two isolated native holdouts, manual external import,
finalization, validation, and idempotent publication.

The working evaluation was 3.5. Fresh holdouts were 3.8 and 3.7, producing an
official native score of 3.7 and the honest terminal status `no_qualifier`. A
deterministic external fixture recomputed exactly at the configured boundary,
remained binding, and was correctly marked unqualified. One deliberately
malformed scout return exhausted the configured retry budget while its raw bytes
and error stayed visible. The completed ignored local run passes `check` with no
source drift.

The three blind smoke seeds were exact-fingerprint unique but all retained the
same broad service/software, partner-distribution, workflow-data structure. The
latest v2 pool contained 48 concepts, about 31–35 distinct commercial
structures, and 39 members of that recurring family. The smoke therefore does
not establish quality improvement; it demonstrates that the replacement makes
structural concentration and negative business evidence visible without losing
workflow integrity.

## Verification

- Archive reconciliation: 2,441 unique destinations, 23,867,597 bytes, zero
  size, hash, checkpoint-blob, source-removal, or external-snapshot errors.
- History reconciliation: 15 idea files and 37 run trees verified; 2,361 run
  files and one empty tree match the manifest and canonical tree-hash contract.
- Deterministic and fault-injection suite: 48 tests pass with warnings treated
  as errors.
- A clean Git export of `8f9d153` passes all 48 tests, configuration/rubric
  validation, Python compilation, repository-skill validation, active-reference
  scans, and a full 2,441-destination archive size/hash/membership audit.
- Python compilation, environment/config check, skill validation, completed-run
  check, and whitespace/diff validation pass.
- Independent adversarial replay found no remaining blockers. It re-tested raw
  and external provenance deletion, shared native raw responses, forged reports,
  candidate-lineage contamination, every state/event failure boundary, publish
  and export event repair, path and lock symlinks, and ambiguous Boolean schema
  versions.
- Active-tree scans find no machine-specific paths, legacy v2 runtime,
  private-session trace dependency, old gate, browser-startup machinery,
  evaluator-weight copy, founder-capital copy, or import from `archive/`.

## Known Limits

- A model score measures alignment with the current planning rubric; it is not proof of demand, product-market fit, or permission to spend.
- Fresh isolated judges reduce obvious leakage and cherry-picking but do not eliminate model subjectivity.
- Historical fingerprint extraction is a structured human interpretation of uneven legacy artifacts; raw archived files remain authoritative.
- Current web and regulatory evidence will age. Decision-critical claims require re-checking in each production run.
- `.gstack` authentication state remains ignored and outside the active architecture by design.
- Quality improvement from the new discovery lanes remains a hypothesis until a larger blind comparison is reviewed; software correctness does not establish business quality.

## First Production Run

In Codex:

```text
Use $business-opportunity to start a new opportunity run.
```

Or initialize directly:

```text
python3 scripts/opportunity.py new
```

Use `status`, `resume`, and `check` with the emitted run ID. The repository skill then owns bounded native-agent dispatch and the CLI owns every canonical write and transition.
