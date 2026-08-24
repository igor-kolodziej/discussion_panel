---
name: generate-zero-to-one-candidates
description: Generate broad, adversarially sourced, lawful Zero-to-One business finalists with researched economics, defensibility, distribution, execution, and founder-wealth assessments for the discussion_panel founder, including materially improved versions of prior ideas. Use when asked to discover, brainstorm, scout, or create business candidates or finalist briefs across conventional, controversial, regulated, or neglected markets. Generate and research only; do not score, simulate validation, contact the real Zero to One chatbot, or create confirmed-idea artifacts.
---

# Generate Zero-to-One Candidates

Generate an auditable, researched finalist set with maximum permitted search latitude. Do not evaluate it as a panel and do not claim validation.

Default to a fresh cross-sector search. Treat July finalists and all earlier candidates as historical comparison evidence only unless the user explicitly selects one for continuation.

## Non-validator boundary

- Do not change or reinterpret validator criteria, logic, weights, definitions, calibration, thresholds, founder facts, success criteria, or safety/legal boundaries.
- Do not assign scores, invoke `$evaluate-zero-to-one`, invoke `$pivot-zero-to-one`, run simulated panels, contact the real Zero to One chatbot, or create `CONFIRMED_IDEA_*` files.
- Do not change which or how many ideas reach evaluation or validation, validation timing or frequency, downstream gates, feedback reuse, or validation budget without explicit user approval.
- Shadow findings are diagnostics. They cannot alter live routing, the live shortlist, later regeneration prompts, or downstream validation.

## Select and register the generation mode

Record the mode in `00_run_manifest.md` before dispatching agents.

### `audited_funnel`

Use this live default unless the user requests a pre-registered shadow comparison. Preserve the existing funnel ranges:

- 40–60 unscored raw hypotheses;
- 10–20 researched directions;
- 3–6 frozen finalists.

Add complete provenance, reversible clustering, pre-freeze evidence closure, context/resource telemetry, and a shadow-only omission audit. Only the main agent makes live selection decisions.

### `archipelago_lite_shadow`

Use only beside `audited_funnel` as a matched, non-routing discovery treatment. Read [references/blind-search-protocol.md](references/blind-search-protocol.md) completely before creating packets or artifacts for this mode.

The shadow treatment creates 36 evidence-first problem cards, 48 unscored concepts, 12 equal-budget Level-2 dossiers, and six frozen shadow finalists. Store it under `shadow_archipelago_lite/`; prefix finalist artifacts `shadow_finalist_` so live finalist discovery cannot match them. Every shadow artifact must state `shadow_only: true` and `validation_eligible: false`.

Do not send shadow candidates to advisory evaluation, pivoting, simulated panels, or real chats. Promotion or substitution requires explicit approval.

## Load live context

The main agent reads these files completely at the start:

1. `/Users/igor/Desktop/discussion_panel/PERSONALITY_SITUATION.md`
2. `/Users/igor/Desktop/discussion_panel/COMMUNICATION_AND_GENERAL_RULES.md`
3. `/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_AGENT_PROMPT.md`

Do not load `/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt` into creative, clustering, selector, or dossier contexts. It is a downstream validator framework, not a discovery input.

Inspect `/Users/igor/Desktop/discussion_panel/ideas/` and relevant prior funnels under `working_folder/` only after raw live generation. Build neutral fingerprints from previously confirmed, unvalidated, and repeatedly rejected business shapes. Treat history as comparison evidence rather than an automatic exclusion list: a prior shape may return only when the candidate documents a material improvement in customer, wedge, distribution, economics, control point, or timing.

Keep historical discovery bounded:

- Index confirmed ideas by filename, title, thesis, customer, and economic fingerprint; read a full file only for a likely overlap.
- Search manifests, overlap records, final decisions, and relevant candidate funnels before reading detailed historical artifacts.
- Do not recursively load every historical run or simulated review.
- Keep historical scores, evaluator prose, and rejection rhetoric out of creative, clustering, selector, and dossier packets.

## Context isolation and agent roles

The main agent owns orchestration and canonical writes. Subagents return bounded findings only.

- Use `fork_turns:"none"` for every creative, history-compression, clustering, audit, selector, and dossier agent.
- Run at most three subagents concurrently.
- Give each agent one immutable allowlisted context packet with compressed founder facts, applicable safety/legal boundaries, its role, assigned neutral evidence or IDs, resource cap, and output schema.
- Do not give an agent unrestricted repository context, the parent conversation, validator files, factor names or weights, thresholds, scores, evaluator objections, another agent's conclusions, or detailed historical rhetoric.
- Log packet paths and hashes, complete typed context classes, actual files read, exact model identifier/version, reasoning setting, timestamped queries and source opens, tool call IDs, per-entity allocations, uncached input, output, elapsed time, and output IDs. Reconcile the append-only manifest against the run trace before attesting that file-read and tool-event logs are complete.
- For each creative agent, record non-empty `assigned_ids` and `output_ids`; problem cards and concepts record `creator_agent_id`. The ledger and agent records must reconcile exactly so nominal roles cannot stand in for actual outputs.
- An agent that generates or transforms an exact concept cannot later rank, challenge, evaluate, or validate it.
- A fresh isolated provisional shadow selector receives only masked Level-1 cards and the pre-registered main decision rule. It produces the six-item provisional list and ordered reserve; the root orchestrator only writes and hashes that result.
- A second fresh isolated finalist selector receives the twelve masked Level-2 dossiers and chooses the exact six fact-closure candidates. The root seals that cohort; matched shadow mode allows no post-closure replacement.
- In a matched audited-baseline diagnostic, the existing main-agent rule seals six Level-2 direction IDs before fact closure. Those exact six receive eight queries each and either freeze unchanged or make the matched run incomplete; no seventh replacement is permitted.
- In either matched arm, dispatch exactly one isolated Level-2 agent for each of twelve candidates in batches of at most three, then one isolated fact-closure agent for each of six sealed candidates in batches of at most three. Every such agent owns one identical singleton assignment/output, one allocation, one return, one globally unique trace-task identity, and one run-local raw trace. Poll each live candidate trace every second and immediately interrupt its owning agent at the lower contract stop boundary; a crossed boundary fails stage admission. Never divide a multi-candidate agent's aggregate tokens, time, calls, sources, or evidence after execution.
- Rankers receive masked standardized cards with author, island, transformation type, prior status, and provisional selection state removed.

Fail closed when a clean packet cannot be provisioned. Do not repurpose a full-context agent as an independent creative or selector.

## Create the run and artifact ledger

Create `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_YYYYMMDD_HHMMSS/`. Keep live canonical artifacts at the run root and shadow artifacts under `shadow_archipelago_lite/`. Never write generated candidates to `ideas/`.

When a shadow arm exists, mirror its machine-readable `00_run_manifest.md`, `00a_context_and_resource_manifest.jsonl`, `02a_raw_pool.md`, and `02b_raw_to_direction_ledger.jsonl` inside `shadow_archipelago_lite/`. Audit the live root and shadow subfolder separately; the root manifest links both results.

Maintain:

- `00_run_manifest.md` — timestamp, exact baseline, pre-run and post-run content hashes, dirty state, mode, seed, model/effort, founder constraints, resource caps, downstream-contract hashes, and shadow boundary.
- `00a_context_and_resource_manifest.jsonl` — append-only context, read, query, source, tool, protected-contract snapshot, and resource records. Every query links to a typed tool event, opened source, evidence proposition, and affected entity.
- `01_overlap_and_rejections.md` — live historical comparison and material improvements.
- `01a_search_space_map.md` — soft evidence/mechanism coverage; never an exhaustion claim.
- `01b_history_fingerprints.md` — neutral customer/loss/payer/transaction/acquisition/asset fingerprints and status.
- `02_candidate_funnel.md` — 10–20 live directions and decisions.
- `02a_raw_pool.md` — all stable raw IDs and unscored hypotheses. Existing legacy runs may retain `02a_adversarial_raw_pool.md`.
- `02b_raw_to_direction_ledger.jsonl` — exactly one mapping for every raw ID plus evidence and finalist ancestry records.
- `02c_main_provisional_order.json` — in shadow mode, the isolated provisional selector's sealed six IDs, ordered 42-ID reserve, creator agent, freeze timestamp, and seed.
- `02c_shadow_selector_audit.md` — sealed shadow nominations, the pre-unblinding main decision, disagreements, sentinels, and reconciliation.
- `02d_fact_closure_candidates.json` — the isolated finalist selector's exact six-ID closure cohort, creator agent, selection timestamp, and seed.
- `03_research_and_sources.md` — evidence IDs, evidence/hypothesis status, timestamps, contradictions, and direct sources.
- `09_diversity_and_resource_audit.md` — effective fingerprints, overlap, source concentration, selector disagreement, and resource parity.
- `10_integrity_check.md` — audit command/result, exceptions, and protected downstream hashes.
- `finalist_<slug>.md` — 3–6 live finalist briefs.

Before the run starts, create a protection anchor outside the run folder with `audit_funnel.py --create-protection-anchor`, and retain the printed SHA-256 independently rather than copying it only into the mutable run manifest. The fixed `zt1-fixed-v1` profile binds each founder, success, goal, validator, prompt, generator, evaluator, and pivot ID to its exact canonical path; a same-suffix copy elsewhere is not acceptable. After the exact finalists freeze, create a separate external freeze seal with `--create-freeze-seal` and retain its printed SHA-256 independently. The final native audit supplies both files and both independent pins. Manifest-local hashes prove internal consistency only; without both external pins a completed run is `INCOMPLETE`, never a pass.

Before launching a shadow scout, finish and externally seal the live arm. Record the live run's canonical directory and independently retained live freeze-seal digest in the shadow manifest. Audit the shadow arm with `--live-arm-freeze-seal` and `--live-arm-freeze-seal-sha256`; the auditor verifies the sealed live finalist files, exact model/version and reasoning parity, matched flag, and that live sealing preceded every shadow-agent start. A mutable timestamp assertion alone is insufficient.

Use immutable IDs. Renaming never changes identity; a material pivot receives a new ID with parents. Every raw ID must map exactly once to a retained direction, a preserved sibling, or an explicit `rejected` or `unresolved` disposition. Never delete a cluster member.

Every complete Level-2 record binds a unique, non-symlink, nonempty standardized dossier path and content hash, the exact concept ID, required neutral sections, ordered selection/completion timestamps, and typed development status. The standardized dossier covers customer loss and payer evidence, proposed transaction and paid trigger, acquisition route, incumbent substitute and route-around, unit economics and sensitivity, control point or compounding asset, execution dependencies and cheapest proof, decision-critical unknowns and contradictions, and evidence and sources. Count persuasive prose only in the first eight bodies: 900–1,500 words at Level 2 with at least 75 words per section, and 1,100–1,800 words frozen with at least 100 words per section; exclude titles, headings, Evidence And Sources, source ledgers, telemetry, and machine metadata. An early stop is valid only for indispensable illegality/serious harm or a directly falsified premise and cannot enter fact closure or freeze. Every frozen finalist ledger record binds its ID and ancestry to an existing exact dossier path, SHA-256, offset-aware `frozen_at`, cited pre-freeze evidence, and the externally pinned freeze seal. The underlying event chain must satisfy query/tool event <= source open <= evidence record <= freeze, with arm/stage and owning-agent interval consistency. Live finalists explicitly retain `validation_eligible: true`; shadow and matched-baseline finalists set `shadow_only: true` and `validation_eligible: false` and use their non-live filename namespaces. The matched Archipelago arm records six 18-query discovery allocations. The matched audited baseline records five pre-registered discovery allocations, assigned by a seeded role permutation as `22/22/22/21/21`; both record twelve singleton 12-query Level-2 allocations and six singleton eight-query fact-closure allocations. Each matched arm seals its six closure entities before the first closure query. Used and unused queries reconcile within each allocation, unused budget is never reassigned or consumed as filler, and a contradicted sealed candidate makes the matched arm incomplete rather than creating a replacement attempt.

Run `/Users/igor/.codex/skills/generate-zero-to-one-candidates/scripts/audit_funnel.py` with the independently pinned protection anchor and freeze seal before handoff; add the independently pinned live-arm seal when auditing the shadow arm. A downstream evaluator, judge, scorecard, adjudication, pivot, panel, working/fresh/real-chat call or routing artifact recorded anywhere in a shadow/matched manifest or artifact tree is a violation even when its timestamp is later than the declared run end. Validator, threshold, score, or evaluator material inside a non-routing selector, Level-2, or finalist artifact is also a violation.

If a stage admission fails, stop at the last real checkpoint and retain the causal trace and return as evidence. Do not resume that run, backfill telemetry, materialize the child, invent later dossiers or dispositions, or create missing seals. Prefix audits assess only the reachable lifecycle; an absent future artifact is not a separate root cause, while an artifact created before its dispatch boundary is a real error. Record `deadline_at` separately from actual `ended_at`; never use the deadline as an end timestamp.

## Run the audited live funnel

Use all five creative roles in `NEW_IDEA_AGENT_PROMPT.md`, in batches of at most three, with isolated context packets. Create 40–60 meaningfully distinct unscored hypotheses before narrowing. The current mechanism/control-class coverage remains a live baseline diagnostic; do not tell agents that visiting named classes proves search exhaustion.

For every raw hypothesis, record the originating role, mechanism or source mode, loss bearer, payer, beneficiary, authority holder, distributor, risk bearer, transaction owner, first paid event, proposed control or compounding asset, evidence atoms, hypotheses, and any prohibited reliance.

Deduplicate by economic fingerprint—not title or sector—using customer/loss, payer/budget, paid trigger, transaction owner, acquisition route, and compounding asset. Similarity proposes clusters but never deletes inputs. Different payer, paid trigger, transaction owner, or acquisition route normally remains a sibling unless a field-by-field merge rationale establishes economic equivalence.

The main agent freezes and hashes the live finalist IDs and files before dispatching any Archipelago scout or shadow omission auditor. Automatic subagent delivery counts as exposure; sequential dispatch is the safe default unless an isolated coordinator can withhold shadow outputs. The audit may identify omissions but cannot modify live choices.

## Close decision-critical evidence before freeze

Before freezing a finalist, perform bounded research on the assumptions most likely to reverse the decision, including where relevant:

- existence and size of the payer denominator;
- direct budget or willingness-to-pay proxy;
- exact authority, right, access, or contract availability;
- closest substitute and incumbent route-around;
- realistic price, cost, capital, and sensitivity ranges;
- first-customer acquisition path and critical dependencies.

Every consequential record needs an evidence ID, proposition, source and date, `recorded_at`, linked direction, status (`verified`, `interpreted`, `counsel-required`, `unknown`, or `contradicted`), and cheapest resolving test. A public-data gap stays `unknown`; it is not an automatic veto.

The freeze record must cite its decision-critical evidence and have a later `frozen_at` timestamp. Later evidence is a versioned update, never backdated support for the earlier decision.

## Research and develop retained directions

For each retained direction:

1. Reconstruct the target customer's desired outcome, current workaround, priced loss, willingness to pay, and misunderstood tradeoffs.
2. Map who pays, benefits, loses, controls information and distribution, bears risk, holds legal or contractual authority, and owns the transaction.
3. Classify every consequential premise as `LAW / BINDING RULE`, `SOFT INDUSTRY NORM`, `ASSUMED CONVENTION`, `REPUTATIONAL EXPECTATION`, `TECHNICAL LIMITATION`, or `ECONOMIC LIMITATION`. Use primary authority for binding rules and record confidence.
4. Before rejecting a lawful direction for a norm, convention, reputation, technical constraint, or economics, attempt at least one structural circumvention through payer, ownership, financing, distribution, licensing, geography, risk allocation, or value capture.
5. If illegal conduct, deception, coercion, or serious harm is indispensable, reject that implementation; seek a lawful safer structure only when it preserves the valuable mechanism.
6. Identify the first acquisition mechanism and any access, resource, workflow, distribution, data, rights, supply, brand, switching-cost, scale, regulatory, or network advantage. Assess how an unknown founder could secure or prove it.
7. Build conservative, expected-success, and strong-success founder-wealth cases with volume, pricing, revenue, margins, capital and debt, ownership and dilution, reinvestment, business value or cumulative distributions, and timing. Assess the credibility of at least 5 million PLN without double counting.
8. While the founder remains employed, use 95% reinvestment of after-tax distributable cash in conservative and expected cases, allow 100% in strong success, and cap optional distributions at 5%.
9. Define the fastest credible first-customer proof, capital at risk, employment compatibility, and what can be learned before building the full product.
10. Map dependencies across technology, regulation, partnerships, trust, distribution, credentials, relationships, and physical operations. Treat their realistic effects as opportunity evidence, not separate gates.
11. Prefer wedges that generate cash, customer knowledge, reusable assets, proprietary workflow, owned rights, transaction flow, or distribution even if expansion fails.
12. Research time-sensitive market, regulatory, competitive, and economic claims. Balance customer/workaround, spend/procurement, operational, incumbent, technical, and official/regulatory sources; only binding-rule claims require primary authority.
13. Scrutinize generic consulting, generic AI wrappers, dashboards, CRMs, influencer-first distribution, unspecified partnerships, pre-validation capital intensity, superficial foreign copies, and easily copied advantages through their actual effect on demand, economics, distribution, durability, and execution—not a categorical gate.
14. Apply founder fit after divergent generation. Select 3–6 meaningfully distinct live finalists under the current holistic opportunity criteria without assigning scores.

Stop researching a direction when evidence is sufficient to reject it or freeze it. Record unresolved propositions rather than expanding indefinitely.

## Resource and termination discipline

Pre-register per-stage budgets. A fully non-routing matched diagnostic uses these exact machine-enforced aggregate caps separately for an audited-funnel baseline arm and the Archipelago shadow arm: 48 raw concepts, 12 Level-2 dossiers, six frozen finalists, 300 unique queries, 10 million uncached input tokens, 700,000 output tokens, 180 minutes, maximum three concurrent agents, and the same exact model identifier/version and reasoning setting. Its exact per-candidate hard ceilings are 112,000 uncached input tokens, 20,000 output tokens, and 15 minutes at Level 2; 96,000 uncached input tokens, 20,000 output tokens, and 12 minutes at fact closure. Live interruption thresholds are respectively 92,000/11,000/14 minutes and 76,000/11,000/11 minutes. Before each batch, start the pinned blocking controller; it discovers the recent candidate traces once, samples their direct paths every second, and exits with the exact task identities the root must immediately interrupt through the collaboration interrupt operation. Wait on the controller process instead of model-driven one-second polling. Record elapsed use as timestamp-derived integer microseconds; the minute values are caps, not telemetry. Declaring a different cap or monitor boundary fails rather than redefining the experiment. Both matched arms remain `validation_eligible: false`; sending either cohort downstream requires explicit approval. Ordinary live runs retain the 40–60, 10–20, and 3–6 ranges.

Log unused budget; do not transfer it to a favored idea. Do not claim exhaustion from sector, lens, or named mechanism coverage. At the resource boundary report marginal new economic fingerprints, duplicate rate, historical-neighbor rate, unresolved selector disagreement, and uncovered evidence modes. Coverage is diagnostic, not proof of idea quality.

## Write each live finalist brief

Use this structure:

```markdown
# Zero-to-One Candidate: {name}

## One-Sentence Thesis
## Founder Fit
## Customer, Pain, and Current Workaround
## Product Wedge
## Commercial Insight or Market Gap
## Underused Momentum
## Beachhead Market
## Incentive and Power Map
## Business Model and Unit Economics
## First 10 and 100 Customers
## Rule and Constraint Classification
## Lawful-Structure Check
## Constraint-Circumvention Attempts
## Defensibility and Access Mechanism
## Cold Start and Resource Bootstrap
## Distribution Advantage
## Competitive Advantage and Expansion Path
## Poland/EU or Local Adaptation Defense
## Compounding Advantage
## Founder Wealth Assessment
## Reinvestment and Compounding Model
## First-Customer Validation and Execution Plan
## Capital Tranches and Maximum Loss
## Critical Dependency Map
## Full-Time Transition Criteria
## Failure Recovery and Reusable Assets
## Critical Evidence
## Critical Hypotheses
## Kill Criteria
## Budget, Time, and Minimum People Stack
## Research Sources
```

Make the brief complete enough for a downstream evaluator to judge without guessing. Label unsupported numbers and claims as hypotheses. Do not include generation-role identity, shadow-selection status, numeric scores, or validator language.

## Finish

Return a concise list of live finalists, the absolute run-folder path, the Founder Wealth assessment, main execution risk, and strongest unresolved hypothesis for each. Report shadow findings separately when present.

State exactly: `Candidate generation only — not validated.`

Never describe a generated candidate as confirmed, approved, passed, or validated.
