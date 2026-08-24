Create one new business idea and write it as a timestamped Markdown file only if the exact candidate passes every gate. If no candidate passes, create no confirmed-idea file.

```text
/Users/igor/Desktop/discussion_panel/ideas/
```

Use a filename like:

```text
CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md
```

## Required Inputs

Read:

```text
/Users/igor/Desktop/discussion_panel/PERSONALITY_SITUATION.md
/Users/igor/Desktop/discussion_panel/COMMUNICATION_AND_GENERAL_RULES.md
/Users/igor/Desktop/discussion_panel/BROWSER_STARTUP.md
/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt
/Users/igor/Desktop/discussion_panel/TRIED_IDEAS_AND_FAILURES_BRAIN.md
```

Treat this file as the canonical orchestration contract. The skills below implement individual stages; if a shorter summary conflicts with this file, this file controls unless the user explicitly overrides it.

## Maximum-Latitude Search Contract

Optimize for the probability of finding a real, executable, defensible business satisfying every hard criterion—not for conventionality, social approval, a pleasant narrative, or resemblance to a typical startup.

Deliberately search opportunities that are unconventional, controversial, politically sensitive, reputationally awkward, heavily regulated, low-status, aesthetically unattractive, culturally unpopular, incumbent-hostile, or difficult to explain publicly. None of those traits is an automatic rejection criterion. Regulatory complexity may create licensing, information, transition, procurement, compliance, capacity, or transaction moats.

Do not silently relax a hard requirement. Search for legitimate structural ways around apparent trade-offs by changing the payer, economic buyer, asset owner, financing party, licensed role, distribution route, geography, risk allocation, transaction structure, or value-capture mechanism.

Do not automatically discard the broader opportunity space merely because one implementation is prohibited.

## Constraint Classification

For every consequential barrier or assumption, assign exactly one primary class:

- `LAW / BINDING RULE` — a law, licence, binding contract, tender term, court rule, or enforceable programme condition creates a consequence for a named actor.
- `SOFT INDUSTRY NORM` — voluntary standards, regulator guidance, certifications, insurer policies, or customary procurement practices that allow alternatives.
- `ASSUMED CONVENTION` — an asserted requirement such as “buyers always demand this” without authoritative or contractual evidence.
- `REPUTATIONAL EXPECTATION` — criticism, optics, employee resistance, political sensitivity, or credibility concerns.
- `TECHNICAL LIMITATION` — physical performance, accuracy, interoperability, safety, throughput, or reproducibility.
- `ECONOMIC LIMITATION` — price, CAC, labour, capital, loss rate, market size, payback, substitution, or willingness to pay.

Split mixed claims into separate atoms. For each atom record the proposition, affected actor, jurisdiction or contract, trigger, consequence, controller/enforcer, evidence source and date, confidence (`verified`, `interpreted`, `counsel-required`, or `unknown`), and cheapest proof. Use primary authority for binding-law claims. A proposed law, non-transposed directive, voluntary standard, guidance document, or reputational expectation must not be presented as currently binding law.

Before rejecting a direction for a soft norm, convention, reputation, technical constraint, or economic limitation, record at least one concrete circumvention attempt and why it fails.

## Adversarial Creative Roles

Use all five lenses during fresh generation. Run subagents in batches of at most three concurrent agents:

1. **Taboo-Space Explorer** — inspect legitimate markets mainstream brainstorming avoids because they are controversial, boring, regulated, politically sensitive, low-status, or reputationally unusual. Controversy is a discovery lens, not a selection reason.
2. **Incentive-Hacker** — map who pays, benefits, loses, controls distribution and information, bears risk, and holds regulatory or contractual power; build around mismatches.
3. **Incumbent-Attacker** — find excessive pricing, cross-subsidization, poor service, distribution lock-in, outdated operations, regulatory complacency, and conflicts that prevent incumbents from serving the wedge well.
4. **Rule-Structure Analyst** — distinguish binding rules from norms and assumptions, identify transitions and enforcement points, and design structures around the actual rule perimeter.
5. **First-Principles Extremist** — construct the business backward from the hard criteria using unconventional ownership, financing, geography, labour, licensing, partnerships, data, IP, vertical integration, or outsourcing.

Creative agents receive the founder constraints, this latitude contract, and relevant neutral evidence/rule atoms. Do not give them historical scores, desired scores, prior rejection rhetoric, or other agents' conclusions. They generate hypotheses and may identify prohibited reliance, but they do not score, validate, or make the final selection.

## Discovery Modes And Audit Contract

The generator must register one of these modes in `00_run_manifest.md` before any discovery agent is spawned:

- `audited_funnel` — the live default. Preserve the existing 40–60 raw hypotheses, 10–20 researched directions, and 3–6 finalist ranges. Add stable IDs, complete raw-to-direction provenance, reversible semantic clustering, decision-critical evidence before finalist freeze, and context/resource telemetry. Only the main agent makes live selection decisions.
- `archipelago_lite_shadow` — a matched non-validator discovery treatment that may run beside `audited_funnel`. It creates 36 evidence-first problem cards, 48 concepts, 12 equal-budget Level-2 dossiers, and six frozen shadow finalists under the protocol at `/Users/igor/.codex/skills/generate-zero-to-one-candidates/references/blind-search-protocol.md`.

Shadow artifacts must be stored under `shadow_archipelago_lite/`, marked `shadow_only: true` and `validation_eligible: false`, and named so they cannot match the live `finalist_*.md` pattern. They may diagnose omissions but cannot add, remove, replace, reorder, or rewrite live finalists; influence regeneration; or enter advisory evaluation, pivoting, simulated judging, or real-chat validation without explicit user approval.

Live finalist ledger records use `finalist_*.md` and explicitly retain `validation_eligible: true`; this preserves the existing downstream route and does not claim that an idea has passed any advisory or validation gate. A shadow or matched-baseline ID appearing in a live generation packet, regeneration artifact, evaluator packet, pivot, panel, chat, or confirmation artifact is an integrity failure.

Use `fork_turns:"none"` for every creative, history-compression, clustering, provisional shadow-selector, ranker/challenger, and dossier agent, with no more than three concurrent. Give each one an immutable allowlisted packet and log its hash, complete typed context classes, actual files read, exact model identifier/version, reasoning setting, timestamped query/source/tool IDs, per-entity allocations, uncached input, output, elapsed time, and output IDs. Every actual read must be both allowlisted and hashed. Discovery and shadow-selection packets contain compressed founder facts, safety/legal boundaries, neutral evidence, role instructions, resource caps, and output schemas only. They exclude `Personalities/ZeroToOne.txt`, validator/evaluator skills, validation factors or weights, scores, thresholds, prior evaluator language, detailed rejection rhetoric, unrestricted repository context, and other agents' conclusions.

Freeze and hash the live finalist IDs and files before dispatching any Archipelago scout; automatic subagent delivery counts as exposure. Within the shadow arm, a fresh isolated provisional selector receives only masked Level-1 cards and the pre-registered main decision rule, then returns six provisional choices plus an ordered cutoff reserve. The main agent writes and hashes that sealed output before dispatching any shadow ranker or challenger; it does not redo the selection from its validator/history-bearing context. After the twelve Level-2 dossiers are complete, a second fresh isolated selector chooses and orders the exact six fact-closure candidates from masked dossiers. The root only seals that cohort. Matched shadow mode permits no post-closure substitution: the same six freeze or the run is incomplete. Shadow selectors remain diagnostic and separate; do not average their lists or substitute them for the live decision rule.

Every raw ID must map exactly once to a retained direction, preserved sibling, or explicit `rejected` or `unresolved` disposition. Similarity may propose clusters but may not delete members. A finalist freeze must cite decision-critical evidence whose query/tool, source-open, and evidence-record timestamps causally precede the freeze and remain inside their owning agent's interval. Bind every completed Level-2 and finalist dossier to a unique non-symlink path, exact concept ID, required neutral sections, and SHA-256; an early-stopped Level-2 concept cannot enter fact closure or freeze. Public evidence gaps remain explicit `unknown` hypotheses rather than automatic vetoes.

Before run start, create the protocol's external protection anchor outside the working folder and retain its printed SHA-256 independently. Its fixed profile must resolve to the exact canonical founder, success, goal, validator, orchestration, generator, evaluator, and pivot paths; a same-suffix copy is invalid. After finalist freeze, create the separate external freeze seal and independently retain its digest. Before any Archipelago scout starts, independently pin the live arm's freeze seal and bind its run directory and digest into the shadow manifest; the shadow audit must verify live finalist files, exact model/effort parity, and live sealing before shadow dispatch. Final integrity supplies all applicable pinned snapshots; mutable manifest-local hashes or timestamps alone are insufficient. In matched or shadow mode, enforce the exact `300 / 10M / 700k / 180 / 3` query, uncached-input, output, wall-time, and concurrency caps. Enforce the exact six registered evidence-island IDs, reconcile every creative agent's assigned/output IDs with problem/concept `creator_agent_id`, require reciprocal query→source→evidence→entity lineage, and hash-bind all twelve completed Level-2 dossiers. Any downstream evaluator/judge/scorecard/adjudication/pivot/panel/chat call, artifact, or validator-shaped content in the non-routing arm remains prohibited even if timestamped after the declared run end.

## Role And Contamination Controls

- Keep generation, advisory evaluation, pivoting, simulated judging, and real-chat validation separate.
- An agent that generated or pivoted an exact candidate must not later act as an independent evaluator or simulated judge of it.
- An advisory evaluator or internal judge receives the frozen canonical candidate, compressed founder constraints, relevant source evidence, and the full `holistic-11-v1` framework from `Personalities/ZeroToOne.txt`—not generator reasoning, target thresholds, or previous scores.
- Use fresh independent judges after every material pivot.
- Only the main agent deduplicates, applies founder fit, routes stages, and writes canonical run, candidate, pivot, evaluation, panel, or confirmed-idea artifacts. Subagents return bounded findings; they do not write canonical files.
- Generation and validation are different phases: creative agents expand the space before evaluation agents test it.

## Available Zero-to-One Skills

Use these global Codex skills for their distinct responsibilities:

- `$generate-zero-to-one-candidates` (`/Users/igor/.codex/skills/generate-zero-to-one-candidates/SKILL.md`) — use the five adversarial lenses to create 40–60 unscored raw hypotheses across at least eight mechanism/control classes, deduplicate them into 10–20 researched directions, select 3–6 finalist briefs, and create the candidate run folder. Use it at the start and again only when the surviving business shapes are exhausted.
- `$evaluate-zero-to-one` (`/Users/igor/.codex/skills/evaluate-zero-to-one/SKILL.md`) — diagnose and score a candidate without rewriting it. Use it as an advisory pre-screen and after failed panel/chatbot verdicts. Its score is not a simulated or real validation score and never satisfies a gate.
- `$pivot-zero-to-one` (`/Users/igor/.codex/skills/pivot-zero-to-one/SKILL.md`) — materially change a candidate using the evaluator diagnosis and objections. Use it for structural pivots, then return the revised candidate to `$evaluate-zero-to-one` before any new panel.

Keep the roles separate. Do not ask the generator to score, the evaluator to pivot, or the pivoter to validate. Advisory evaluator scores are diagnostic only. Only the independent simulated panel and real Zero to One chats produce gate-eligible scores.

## Core Opportunity Criteria

The confirmed idea must be well thought-through. It is the test of how well can you imagine human behavior and real customer needs.

The proposal must solve the cold start problem with a specific initial acquisition mechanism. It should identify any foundational resource, access, workflow, distribution, data, rights, supply, brand, switching-cost, scale, regulatory, or network advantage and explain how an unknown founder can secure or prove it with realistic time, capital, AI assistance, contractors, advisors, or hiring. Unspecified partnerships, inaccessible resources, heavy capital requirements, long proof cycles, and multiple uncontrolled dependencies are material Distribution, Defensibility, and Execution risks—not separate vetoes.

Unless stated otherwise, treat every candidate as planning-stage. Missing customers, experiments, partnerships, metrics, or technical validation are uncertainty to resolve, not automatic negative evidence. Contradictory market, economic, technical, or regulatory evidence should reduce the relevant judgment.

### Founder Wealth Assessment

Assess a credible path to at least 5 million PLN of founder net worth inside Business model and economics. Founder net worth is founder-owned business equity plus accumulated personal cash and distributions, minus liabilities and excluding the primary residence. This is an important target, not a hard gate.

Use conservative, expected-success, and strong-success scenarios when the detail supports them. Each should state customers or volume, pricing, revenue, gross and operating margin, debt and capital needs, founder ownership and dilution, reinvestment, business value or cumulative distributions, and estimated timing with intermediate milestones. Use 95% reinvestment of after-tax business cash available for distribution in the conservative and expected scenarios while the founder keeps the corporate job; the strong-success scenario may use 100%. Optional founder distributions during employment should not exceed 5%.

Do not double-count retained earnings in both company value and founder cash or distributions. Heroic market share, margins, valuation multiples, ownership, or indefinite one-for-one founder labor should materially weaken the economics assessment without mechanically capping the overall score.

### Execution And First-Customer Evidence

Define the fastest credible path to first-customer evidence, such as a paid pilot, paid discovery engagement, deposit, preorder, purchase order, or budget-backed commitment. State the expected time, capital at risk, work required alongside employment, and critical dependencies. Prefer tests that avoid building the full product before learning, but do not impose a separate deadline, capital veto, or feasibility gate.

Assume competent use of state-of-the-art AI for suitable research, learning, software, analytics, automation, marketing, operations, documentation, and support. Do not assume AI replaces credentials, licensed accountability, relationships, physical operations, regulatory requirements, or tacit knowledge.

## Strategy Bar

In the divergent phase, start from commercially useful insights, not sectors: look for a novel, overlooked, or better-executed understanding of customers, supply, timing, competition, or power that could support a valuable company, including within an established market.
The source of better ideas is understanding what a specific group of people truly wants from the inside, not what outsiders or current providers assume they want. Reconstruct that group’s point of view: what outcome they are really trying to secure, what pain, risk, frustration, or loss they are trying to avoid, what tradeoffs they already tolerate, and where existing offers leave a commercially meaningful gap.
Do not be afraid to propose brave, controversial, innovative, category-defining, or materially improved existing ideas when they reveal a real commercial advantage and score strongly under the full validation framework. Do not restrict ideation to the founder's obvious interests.

### Crucial strategic assumption

Think like Peter Thiel under initial real founder constraints: ask where a valuable market—new or established—contains a concrete, testable gap in price, speed, trust, distribution, specialization, operations, or customer experience, and whether that gap can open a defensible beachhead, but assume the founder has no high-profile friends, no privileged introductions, no celebrity/influencer access, and no ability to brute-force trust with status. Prefer overlooked or poorly served segments, asymmetric distribution, niche leadership, and resource bootstraps that can be started by an unknown founder. Prefer wedges that can reach credible proof with limited capital, then use venture capital, grants, subsidies, public procurement, accelerators, debt, or strategic financing as leverage once the idea has evidence, urgency, or institutional pull.

Do not chase trends just because they are current. AI, crypto, climate, creator tools, marketplaces, or other fashionable categories are valid only when there is a specific commercial insight, unfair local angle, neglected customer pain, or meaningfully better execution. Favor focused ideas that become compelling once the customer gap and path to durable advantage are made explicit.

Every strong idea must have:

- **Commercial insight or market gap:** a specific insight about demand, customer behavior, economics, distribution, operations, or incumbent weakness that can produce measurably better customer behavior or business economics. It may be novel, overlooked, or already known but poorly executed.
- **Underused momentum:** existing capital, regulation, budgets, infrastructure, pressure, cultural demand, technical change, supply fragmentation, or institutional pressure that lacks a commercial capture layer.
- **Competitive advantage and expansion path:** a credible route to becoming hard to replace, hard to copy, and clearly preferred in a specific market.
- **Beachhead:** a narrow first market small enough to dominate but valuable enough to matter.
- **Compounding niche:** knowledge, trust, data, workflows, distribution, partnerships, or brand credibility that let the niche expand outward better than broad competitors can move inward.

The 40–60-hypothesis raw pool must span at least eight materially different mechanism or control classes. Use classes such as title or custody, assigned payment or transaction routing, exclusive rights or licensing, reserved licensed capacity, bounded underwriting or risk transfer, route density or dispatch priority, mandatory source-of-truth or acceptance control, distressed-asset carve-outs, embedded distribution or procurement authority, and controlled supply or offtake. Sector diversity alone does not satisfy this requirement.

For each retained direction, map the loss bearer, payer, beneficiary, authority holder, distributor, information holder, risk bearer, and transaction owner. State the exact first-contract instrument or owned resource that creates control, who owns capital and downside risk, what observable event triggers repeat payment, what rights survive the first delivery, and how an incumbent could copy or route around the wedge.

Competition is acceptable when it is limited, fragmented, weak in the chosen beachhead, or vulnerable to a specific founder advantage. The candidate must show why its advantage can change customer behavior or economics and how the founder can prove it within the stated constraints. Reject markets where overcoming entrenched incumbents would require excessive capital, status, distribution access, or time.

Foreign-market adaptations are allowed when Poland or Europe creates a meaningful local, regulatory, distribution, operational, trust, pricing, or customer-experience advantage, even without a formal barrier. Ask whether local execution or a materially better offer can win a defensible beachhead before the original foreign company can enter and adapt. Reject superficial copies without such an advantage.

Reject generic consulting, generic AI wrappers, dashboards, CRMs, influencer-first ideas, capital-heavy ideas before validation, and ideas with no compounding advantage.

### Defensibility And Access Discipline

Assess how quickly incumbents could reproduce the core advantage through a vendor contract, equipment purchase, hire, partnership, or routine process change. Cheap replication should materially weaken Defensibility and durability unless speed, switching costs, data, distribution, brand, regulation, supply, workflows, scale, or another compounding advantage makes catch-up difficult. Generic partnerships, coordination, and manual sourcing are hypotheses until specific access and repeatability are evidenced; do not apply a separate categorical tier or numerical cap.

## Research

Follow the research and subagent rules in `COMMUNICATION_AND_GENERAL_RULES.md`. Balance customer workarounds and complaints, actual spend and procurement, operational failures, incumbent economics and channels, technical/scientific change, and rules or institutional transitions. Use primary authority for binding-law claims, but do not treat legal or official-source coverage as evidence of willingness to pay.

Document the run in the single generator-created folder under `working_folder/` and its matching concise takeover summary under `utilities/`. In addition to the existing live artifacts, require `00a_context_and_resource_manifest.jsonl`, `01a_search_space_map.md`, `01b_history_fingerprints.md`, `02a_raw_pool.md`, `02b_raw_to_direction_ledger.jsonl`, `02c_main_provisional_order.json` for shadow runs, `02c_shadow_selector_audit.md`, `09_diversity_and_resource_audit.md`, and `10_integrity_check.md`. Preserve legacy `02a_adversarial_raw_pool.md` inputs when replaying an earlier run. Record evidence IDs and timestamps in `03_research_and_sources.md`. Do not write generated candidates directly to `ideas/`.

## Validation Gates

### Simulated Zero To One Gate

Before contacting the real `Zero to One` chatbot, run an internal simulated Zero To One panel or simulated Zero To One-style review on only up to 6 finalist ideas:

- Spawn up to 3 subagents at one time (two per idea).
- Use fresh judges that did not generate, synthesize, evaluate, or pivot the exact candidate.
- Give each subagent the relevant founder constraints, relevant source evidence, the frozen exact candidate, and the full `holistic-11-v1` framework in `/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt`.
- Ask each subagent for a 1.0–10.0 score to one decimal, a short explanation, strong sides, weak sides, and the strongest objections or caveats.
- Do not tell subagents the desired score or other subagent scores.
- Do not give subagents the pass threshold, generator reasoning, or prior evaluations.
- Use the lower of the two independent scores as the exact candidate's official simulated score.
- If both judges identify the same serious objection, preserve it and determine whether it warrants research, a material pivot, or a lower score under the full framework; do not create an extra veto outside the framework.

The simulated Zero to One score must be strictly greater than 8.3 before real validation. If the simulated score is 8.3 or below, use the objections to materially pivot or change the idea, then repeat candidate selection and simulated scoring until a candidate scores greater than 8.3. Simulated scores do not qualify an idea and never authorize writing the final idea file. They are only a pre-filter for deciding whether real Zero to One validation is worth using.

### Real Zero To One Gates

Follow the chatbot interaction and score gate rules in `COMMUNICATION_AND_GENERAL_RULES.md`. Use the real chatbot only after the simulated score is greater than 8.3.

Additionally: ask the real chatbot only for an independent 1–10 score to one decimal and its strongest objections. Do not send the full internal framework or tell the chatbot what score to give, what to cap, or what thresholds apply. Do not include internal weights, scoring rules, evaluation criteria, or validation logic. Let it evaluate independently from the exact idea and compressed founder constraints.

If a revised version still depends on the same buyer, trust mechanism, authority claim, or speculative resource without a path to durable competitive advantage, abandon that pattern and generate a different candidate. Do not spend long cycles polishing an idea that remains trust-heavy, service-like, easily replicable, dependent on external acceptance, or unable to show a credible path to the required access.

### Crucial requirements for chatbot interaction
ALWAYS take into account it's feedback before pivoting/changing the idea, if you don't agree - make sure you have very strong arguments and discuss them with the Zero to One chatbot accordingly.
DO NOT RUSH it's thinking process. NEVER stop it, wait for the full answer.

## Workflow

1. Invoke `$generate-zero-to-one-candidates` in `audited_funnel` mode for a fresh cross-sector search. Adopt its `working_folder/zero_to_one_candidates_*` directory as the working folder for the entire run; do not create a second working folder. Require the 40–60 live unscored hypotheses, all five creative lenses, at least eight mechanism/control classes, `framework: holistic-11-v1`, complete provenance and context/resource artifacts, and pre-freeze decision-critical evidence. If a matched discovery diagnostic is pre-registered, run `archipelago_lite_shadow` in its separate shadow namespace under the same working folder; it cannot alter the live shortlist or downstream route. Create or update a concise matching takeover summary under `utilities/`. Treat the July finalists and all earlier runs as comparison evidence only, not as the starting shortlist.
2. For each finalist, invoke `$evaluate-zero-to-one` as an advisory pre-screen. Use its score, evidence gaps, Founder Wealth assessment, economic weaknesses, execution risks, and objections as preparation; never convert that advisory score into a simulated or real validation score.
3. Route from the complete advisory judgment:
   - a strong opportunity may enter the independent simulated panel;
   - a decision-critical unknown should be researched and re-evaluated;
   - a structural weakness should be handed to `$pivot-zero-to-one`, then re-evaluated by a fresh evaluator;
   - a clearly unattractive or impermissible shape should be discarded rather than cosmetically rewritten.
4. Select at most 6 panel-ready finalists. If none survive, invoke `$generate-zero-to-one-candidates` again with the accumulated overlap and rejection record. Previously confirmed or rejected ideas may be reconsidered only when the candidate documents a material improvement in the customer, wedge, distribution, economics, control point, or timing and explains why the earlier objections no longer apply. Cosmetic renaming, presentation changes, or minor feature additions do not qualify.
5. Run the independent simulated Zero to One panel described above. Do not invoke `$evaluate-zero-to-one` as a panel judge and do not convert its advisory score into a simulated score.
6. Require the simulated Zero to One score to be `>8.3`. If it is `<=8.3`, run `$evaluate-zero-to-one` on the exact candidate together with the panel objections but without disclosing the panel scores or threshold, then use `$pivot-zero-to-one` for a material structural change. Re-evaluate the revision and use new independent subagents for the next simulated panel.
7. Only after the independent simulated score is `>8.3`, contact the real Zero to One chatbot.
8. Follow the real Zero to One gate rules in `COMMUNICATION_AND_GENERAL_RULES.md` (working-chat `>=8.2`, then fresh-chat `>=8.2`).
9. If either real score is below 8.2, preserve the complete chatbot objections and run `$evaluate-zero-to-one` on the objections without disclosing the real score or threshold, then use `$pivot-zero-to-one` or discard the shape. A revised candidate must restart at advisory evaluation and the independent simulated gate before returning to real validation.
10. Write the confirmed idea file only if the exact same idea wording has an official lower simulated score `>8.3`, working-chat score `>=8.2`, and fresh-chat score `>=8.2`. Record `holistic-11-v1` and a Founder Wealth assessment without pass/fail language. If no idea passes all score gates, do not write an idea file.
11. Bound one orchestration run to the initial 40–60-hypothesis wave plus at most two regeneration waves. Start another wave only when the accumulated rejection record identifies materially untested mechanism/control classes or structural transformations. If no candidate is panel-ready after the third wave, or every remaining pivot repeats a fatal mechanism, terminate the run and report that no confirmed idea passed. Never lower a gate, convert an advisory score, or cosmetically polish a repeated shape to force completion.

## Required Idea File Structure

```markdown
# Confirmed Business Idea

## Idea

## One-Sentence Thesis

## Founder Fit

## Customer And Pain

## Product/Project/Idea Wedge

## Commercial Insight Or Market Gap

## Underused Momentum

## Beachhead Market

## Incentive And Power Map

## Rule And Constraint Classification

## Constraint-Circumvention Attempts

## Defensibility And Access Mechanism

### Cold Start & Resource Bootstrapping 

### Unit Economics & Value Capture 

### Distribution Moat 

## Competitive Advantage And Expansion Path

## Local Adaptation Defense

## Why This Could Compound

## Founder Wealth Assessment

## Reinvestment And Compounding Model

## First-Customer Validation And Execution Plan

## Capital Plan And Maximum Loss

## Critical Dependency Map

## Full-Time Transition Criteria

## Failure Recovery And Reusable Assets

## Validation Plan

## Validation Record
_Framework: `holistic-11-v1`; official lower simulated score; working-chat score; fresh-chat score; strongest objections._

## Kill Criteria

## Budget And Time

## 30-Day Execution Plan

## Yearly Execution Plan

## Applicable Non-Refundable Funding (optional)
_If relevant, list specific grants, subsidies, EU programs, public procurement opportunities, or non-refundable funding sources that could accelerate or de-risk the idea. Include program names, eligibility notes, and approximate amounts if known._
```

## Final Response

After writing the file, respond concisely with:

- short idea concept;
- absolute path;
- Founder Wealth assessment and main execution risk;
- simulated, working-chat, and fresh-chat Zero to One scores, and why the exact candidate passed the simulated `>8.3` gate and both real `>=8.2` thresholds under `holistic-11-v1`;

## advice for your success in finding the right idea
Do not self-censor just because an idea challenges convention, sounds uncomfortable, or goes against socially accepted assumptions. The objective here is not social approval or consensus — it is to identify ideas that are actually strong, defensible, and true AND that can pass the Zero to One gates. The greatest ideas for business are often counter-intuitive at the time

If needed enforce this on subagents.
