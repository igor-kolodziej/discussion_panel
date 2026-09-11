# History, Campaign, And Holdout Integrity

Read this reference when using prior runs, generating a later cohort, checking novelty, freezing a finalist, assigning judges, importing a response, or interpreting qualification.

## Delayed History And Semantic Calibration

Initial discovery is fresh. Do not load historical candidates, failure summaries, scores, or verdicts into scouts. After the fresh pool exists, use `knowledge/failure_patterns.md` and only relevant `knowledge/history_index.jsonl` rows for overlap and adversarial review.

The index is compact memory. Before reading outcome or learning rows, collect every `opportunity_outcome_quarantine_v1` record and exclude its run from business-decision use. The quarantine row itself may be read only to establish that exclusion; its named outcome, candidates, scores, conclusions, and learning digest remain workflow-test evidence and must not inform overlap analysis, research, scoring, ranking, qualification, or campaign progression. Current non-quarantined publication rows reference a hash-bound `learning-digest.jsonl` with one row per researched candidate; later candidate research may load only rows relevant to the already-created fresh score-selected pool. Scouts and screening evaluators never receive it. Legacy rows preserve their original rubric, score string, role, and recovery provenance. Never normalize, average, promote, or present a historical result as a current candidate, working evaluation, or holdout.

Compare exact six-field fingerprints first. Screening-winner deduplication then uses the controlled structural signature. New wording, geography, or industry is not structural novelty when the commercial model, control point, and dependency categories remain the same; normalized descriptors distinguish only the `other` category. Historical overlap may guide later falsification but cannot alter the blinded score-selected shortlist.

Do not create a core-readiness or wildcard eligibility gate. The mechanism-first lane makes lawful control-point acquisition, the current paid event, and the configured founder-access reserve explicit; future-backcast and weak-signal lanes remain independent and may be more speculative. Every candidate is screened, and advancement is score-driven except deterministic semantic deduplication and same-batch backfill. Missing preliminary proof remains uncertainty and should reduce an evaluator's confidence only as the canonical rubric warrants; it is not automatically fatal.

History is delayed adversarial memory, not generation training. PromoLeak and its source dossier are outside this workflow entirely.

## Later Campaign Cohorts

The CLI alone decides whether a published cohort produces another cohort. Use only the `campaign next` action and its generated `briefs/cohort-<N>.json`. Do not prepare a shadow brief from reports or conversation history.

A sanitized brief may identify deficient evaluator factors and copy the shortlist's sanitized `missing_archetypes`. It must not invent a global archetype vocabulary or reveal candidate names or descriptions, raw or rounded scores, deltas, rankings, threshold, shortlist or development rationale, judge feedback, previous verdicts, history rows, or learning-digest content. Scouts remain mutually blind and do not receive the evaluator.

Every later cohort still runs every configured lane to its configured seed budget. The sanitized brief may guide where each lane looks, but it does not collapse mechanism-first, future-backcast, and weak-signal into one shared context or reveal one scout's candidates to another.

Campaign patience is mechanical and score-based. Reworded archetypes, new industry labels, calibration clusters, and missing-archetype labels do not count as progress. Do not stop after one regression, reset progress by editorial judgment, add cohorts past the configured cap, or keep searching after a deterministic stop.

## Working Evaluation Versus Holdout

Working evaluations are mandatory diagnostics for every screening candidate, every researched candidate, and both sides of each admitted original/redesign comparison. They drive the configured score bracket and construction pass but cannot confirm an opportunity.

Before holdout, the main execution agent—not a judge:

1. Validate the hash-bound finalist reference, its deterministic lineage-winning version, discovery-v1 research, constructor result, complete paired development evaluation where a redesign exists, and version-selection receipt.
2. Generate one packet bound to immutable run snapshots and use that same packet for every judge.
3. Create a distinct fresh temporary response destination outside CLI-managed state and obtain `holdout-assignment` for each judge.
4. Launch genuinely fresh native judges isolated from generation, research, working evaluation, construction, the repository workflow context, and one another.
5. Give a judge exactly the assignment's immutable packet, strict response contract, and temporary response destination. It must not load repository instructions, workflow skills, CLI help/status/preflight, history, prior evaluations, rankings, competing candidates, or another judge output.
6. Read the response after the judge stops, perform canonical preflight/import yourself, and ensure judge IDs are globally distinct and disjoint from every working judge ID and constructor ID.

The CLI mechanically constrains the assignment envelope and rejects destinations inside managed run state or already in use. Because native agents share the host filesystem, preventing a judge from independently reading repository files remains an orchestration-only guarantee; use a context-isolated launch and enforce the instruction explicitly.

For a local macOS Codex CLI judge, use the bundled [native-judge launcher](../scripts/launch-native-judge.py). Read it before use. Create a fresh directory with `tempfile.mkdtemp()` and resolve its physical path before generating `holdout-assignment`; the response destination must be directly inside that directory. Save the exact assignment envelope unchanged and run:

```text
python3 .agents/skills/business-opportunity/scripts/launch-native-judge.py <assignment.json> --repo-root <repository-root>
```

The launcher uses one outer operating-system sandbox. It denies repository/worktree contents, global instructions, skills, plugins, sessions, memory, and sibling temporary-directory contents, including `/var` and `/private/var` aliases. It permits writes only inside the judge's directory and to `/dev/null`. Directory metadata remains readable so physical-path resolution can work. Tool shells use a private temporary directory inside the workspace, with login shells and shell snapshots disabled so host startup settings cannot replace that directory. A fresh temporary `CODEX_HOME` holds only that judge's runtime; a temporary read-only route to the existing CLI auth file is removed after execution. Do not copy the runtime auth file or credentials into audit evidence. The CLI receives the exact assignment on stdin, with ephemeral execution, user configuration ignored, project documents and memory injection disabled, and the returned strict response schema. Its `danger-full-access` preset avoids a second nested macOS sandbox; never use that preset without the launcher's outer sandbox. Nesting `workspace-write` inside `sandbox-exec` failed the current host probe with `sandbox_apply: Operation not permitted`.

The native assignment adds explicit types for structured-output compatibility, instructs the judge to write the assigned response file, and binds a deterministic unique judge ID to the run, finalist, and fresh response destination. Exported schemas and immutable packets remain unchanged. Preserve `launch.json`, `sandbox.sb`, `response_schema.json`, events, stderr, the actual judge-written response, and the separate `transport-final.json`. A transport capture alone does not prove that the judge could write its assigned response. Before using the exact launch setup, independently test permitted reads/writes and actual excluded-file reads, including an existing prior judge response through both path spellings; require permission-denied errors, not missing-file errors. Launch judges serially and retain their separate workspaces. On another host, establish and probe an equivalent boundary before starting holdout.

Before any business judgment, verify the exact launch setup with a nonbusiness transport probe using the generated native response schema shape (replace candidate identities and factor labels with harmless probe values while preserving types, nesting, required fields, arrays and bounds): it must create a fresh strict JSON response, receive no repository/global AGENTS or business-skill context, and be unable to read representative excluded files. Inspect its event log for unexpected reads. Preserve the probe evidence; never use a candidate to rehearse or retry the isolation setup. If the available host cannot establish this boundary, keep the holdout unstarted rather than passing development context to a judge.

Do not revise a referenced finalist after feedback and count the same judgment as independent. The active cohort permits a new candidate version only during its admitted development redesign; holdout feedback does not reopen that path.

## Binding Results

Record native judgments as separate canonical jobs. Each valid response is canonicalized deterministically from the same simple JSON contract used for working evaluation. External judgment is optional; if used, preserve and import each complete response independently. Transport, parser, schema, or incomplete-output failure remains visible and scoreless and may consume only the configured mechanical retries. Never retry a valid adverse judgment, infer a missing score, discard an accepted result, substitute a working judgment, or rerun until favorable.

The CLI computes qualification from the immutable config, required native holdouts, and all binding valid external imports. The native lower score controls candidate ranking; an external result may contest or reject but cannot raise the native floor.

Only a fully held-out finalist can produce `qualified`, `no_qualifier`, or `contested`. If no candidate reaches holdout after complete working-evaluation coverage, the cohort is `no_finalist` and its official score is N/A rather than zero. The qualification label describes rubric alignment, not customer demand, empirical market validation, permission to spend, or guaranteed business success.
