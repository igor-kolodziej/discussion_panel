Create one new, non-redundant confirmed business idea and write it as a timestamped Markdown file in:

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
```

Also you can read existing Markdown files in:

```text
/Users/igor/Desktop/discussion_panel/ideas/
```

## Core Pass Criteria

The confirmed idea must be new, creative and well thought-through. It is the test of how well can you imagine human behavior and real customer needs.

The proposal must solve the cold start problem with a specific initial acquisition mechanism. It must also define a concrete path to secure or prove at least one foundational resource or control point—such as data, inventory, specialized talent, partnerships, rights, workflow access, distribution access, or transaction flow—during max. 12-month POC/POV cycle and under 100,000 PLN. The bootstrap path must state what resource is needed, how it is secured, why an unknown solo founder (optionally with a small team of co-founders or contractors) can secure it under the stated constraints, and what proof can be produced before serious capital is spent.

The solution is non-viable if it depends on unspecified partnerships, or resources that cannot be realistically controlled or tested during the first POC/POV cycle.

## Strategy Bar

Generate broadly first, then filter hard. In the divergent phase, start from secrets, not sectors: look for a non-consensus truth about customers, supply, timing, or power that could support a zero-to-one company. 
The secret to better ideas is understanding what a specific group of people truly wants from the inside, not what outsiders assume they want. Reconstruct that group’s point of view: what outcome they are really trying to secure, what pain, risk, frustration, or loss they are trying to avoid, what tradeoffs they already tolerate, and what others systematically misunderstand about their situation.
Do not be afraid to propose brave, controversial, highly innovative, or category-defining ideas when they reveal a real hidden insight and still survive the control-point and validation gates. Do not restrict ideation to the founder's obvious interests, but final candidates must still satisfy the control-point and validation gates.

### Crucial strategic assumption

Think like Peter Thiel under initial real founder constraints: ask what valuable company almost nobody is building, what important market truth most capable observers miss, and whether that secret can open a domination-oriented beachhead, but assume the founder has at most 100,000 PLN available as the starting capital, no high-profile friends, no privileged introductions, no celebrity/influencer access, and no ability to brute-force trust with status. Prefer overlooked markets, asymmetric distribution, niche dominance, and resource bootstraps that can be started by an unknown founder. Prefer wedges that can reach credible proof with limited capital, then use venture capital, grants, subsidies, public procurement, accelerators, debt, or strategic financing as leverage once the idea has evidence, urgency, or institutional pull.

Do not chase trends just because they are current. AI, crypto, climate, creator tools, marketplaces, or other fashionable categories are valid only when there is a specific hidden insight, unfair local angle, or neglected customer pain. Favor ideas that look strange, narrow, or initially unimportant but become compelling once the hidden bottleneck and path to dominance are made explicit.

Every strong idea must have:

- **Hidden insight:** a specific non-consensus claim about the market that most capable observers would initially doubt, but that explains why a valuable company can exist now.
- **Underused momentum:** existing capital, regulation, budgets, infrastructure, pressure, cultural demand, technical change, supply fragmentation, or institutional pressure that lacks a commercial capture layer.
- **Domination path:** a credible route to becoming hard to replace, hard to copy, and clearly preferred in a specific market.
- **Beachhead:** a narrow first market small enough to dominate but valuable enough to matter.
- **Compounding niche:** knowledge, trust, data, workflows, distribution, partnerships, or brand credibility that let the niche expand outward better than broad competitors can move inward.

Competition is not proof of attractiveness. Seek dominance, not participation.

Foreign-market adaptations are allowed only if Poland or Europe creates real local barriers (like EU preferance or first wins or legal etc). Ask whether local execution can win faster than the original foreign company can enter and adapt. If not, treat it as a weak copy.

Reject generic consulting, generic AI wrappers, dashboards, CRMs, influencer-first ideas, capital-heavy ideas before validation, and ideas with no compounding advantage.

### Control-Point Discipline

If incumbents can copy the core control point through one vendor contract, one equipment purchase, or one internal process change, the idea should be penalized but not automatically killed—cap below 80 unless there is a credible speed, switching-cost, or compounding advantage that makes catch-up hard. Generic partnerships, coordination, and manual sourcing are not valid control points unless they are signed, reserved, prepaid, routed, owned, or provable within 12 months.

## Research (optional)

Use current research for market, regulatory, technical, and financial claims that may have changed. Prefer official/regulatory sources, EU/Polish sources, industry associations, credible company documentation, and market reports.

You may use subagents for focused research. Integrate their findings yourself and apply the founder profile as the final decision filter.

If needed coding required - create scripts in newly created folder (specific for that idea) under utilities/ folder.

## Validation Gates

### Simulated Zero To One Gate

Before contacting the real `Zero to One` chatbot, run an internal simulated Zero To One panel or simulated Zero To One-style review on only up to 6 finalist ideas:

- Spawn up to 6 subagents at one time (one per idea).
- Give each subagent the relevant founder constraints and `/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt` as a system prompt.
- Ask each subagent to score the idea from 0-100 and list the strongest objections or caveats.
- Require each subagent to classify the control point tier and name the strongest copy risk.
- Instruct each subagent to weight profitability, willingness to pay, CAC, margins, payback, retention, and repeatability more heavily than originality. Original ideas with poor economics should score low.
- Instruct each subagent to apply a profitability veto: do not give a high score to an idea only because it is original, defensible, technically interesting, or trend-aligned if it lacks plausible gross margins, repeatable acquisition, willingness to pay, reasonable payback, cash conversion, retention, or meaningful owner earnings.
- Do not tell subagents the desired score or other subagent scores.
- If 2+ subagents identify the same fatal objection, pivot away from that business shape.
- If the idea remains commodity, partner-dependent, trust-heavy, or service-like with no path to a compounding advantage, do not send it to real Zero to One.

The simulated Zero to One score must be strictly greater than 85 before real validation. If the simulated score is 85 or below, use the objections to materially pivot or change the idea, then repeat candidate selection and simulated scoring until a candidate scores greater than 85. Simulated scores do not qualify an idea and never authorize writing the final idea file. They are only a pre-filter for deciding whether real Zero to One validation is worth using.

### Real Zero To One Gates

Use the real `Zero to One` chatbot as the final external judge only after the simulated score is greater than 85.

Do not describe what the chatbot is, who it is based on, or how it should act. Do not paste the full profile; compress only relevant founder constraints.

Ask it to rate the idea from 0-100 and include the strongest objections or caveats behind the score. Do not tell the chatbot how to score, what to cap, or what thresholds to apply. Do not include any internal scoring rules, cap instructions (e.g. "cap below X if…"), evaluation criteria, or validation logic in the prompt. Let it evaluate independently based on the idea and founder constraints alone.

The idea first qualifies only if the real working-chat Zero to One score is at least 82.

After the idea first reaches at least 82, create a new Zero to One chat. In the first message, ask it to independently validate the scored idea from 0-100 and include the strongest objections or caveats behind the score. Do not indicate the previous score in any way.

The idea passes only if the fresh-chat validation score is also at least 82.

If either real score is below 82, pivot away from the business shape or improve it if it has a strong potential of getting score >=82. If a revised version still depends on the same buyer, trust mechanism, authority claim, or speculative resource without a path to long-term dominance, abandon that pattern and generate a different candidate.

More iterations are useful only when they change the underlying business shape or uncover a stronger control point. Do not spend long cycles polishing an idea that remains trust-heavy, service-like, easily replicable, dependent on external acceptance, or unable to prove resource control during the 12-month POC/POV cycle.

### Crucial requirements for chatbot interaction
ALWAYS take into account it's feedback before pivoting/changing the idea, if you don't agree - make sure you have very strong arguments and discuss them with the Zero to One chatbot accordingly.
DO NOT RUSH it's thinking process. NEVER stop it, wait for the full answer.

## Workflow

1. Read required inputs and existing ideas.
2. Generate 10-20 divergent candidate directions before applying caps (take a role of Personalities/ZeroToOne.txt to generate valid, appropriate [as described there] ideas).
3. Create a unique folder in working_folder/ and save up all the utility (summary/organization/research) files that may help you during the whole process. If you decide that some files are not needed, you can delete them. It's role it to help you during the whole process, if it's not helping - do not use it.
4. Identify possible control points for the best candidates.
5. Kill or transform weak candidates.
6. Research only claims needed to assess market, substitutes, regulation, cost, and copy risk. Use subagents for focused research when useful.
7. Select up to 6 finalists (based on the 14 points described in Personalities/ZeroToOne.txt).
8. Run the simulated Zero to One panel or simulated Zero to One-style review.
9. Require the simulated Zero to One score to be `>85`. If it is `<=85`, use objections to materially pivot or improve the idea (you can use the same subagents to help you do that), then repeat candidate selection and simulated scoring (use new subagents for scoring if you used old ones for improving/discussing the ideas) until a candidate scores `>85`.
10. Only after the simulated score is `>85`, contact the real Zero to One chatbot.
11. Require real working-chat Zero to One score `>=82`.
12. Create a fresh Zero to One chat and require independent validation score `>=82`.
13. If either real score is below 82, pivot away from the business shape or improve it if it has a strong potential of getting score >=82.
14. Write the confirmed idea file only if the simulated score is `>85` and both real Zero to One scores are `>=82`. If no idea passes both real gates, do not write an idea file.

## Required Idea File Structure

```markdown
# Confirmed Business Idea

## Idea

## One-Sentence Thesis

## Founder Fit

## Customer And Pain

## Product Wedge

## Hidden Insight Or Market Misunderstanding

## Underused Momentum

## Beachhead Market

## Primary Control Point

### Cold Start & Resource Bootstrapping 

### Unit Economics & Value Capture 

### Distribution Moat 

## Domination Path

## Local Adaptation Defense

## Why This Could Compound

## Validation Plan

## Kill Criteria

## Budget And Time

## 30-Day Execution Plan

## Applicable Non-Refundable Funding (optional)
_If relevant, list specific grants, subsidies, EU programs, public procurement opportunities, or non-refundable funding sources that could accelerate or de-risk the idea. Include program names, eligibility notes, and approximate amounts if known._

## Market Context Checked
```

Include the simulated Zero to One score, final working-chat Zero to One score, fresh-chat validation score, scored idea wording, chatbot caveats or objections, sources used, the primary control point, how the foundational resource can be secured or proven during the 12-month POC/POV cycle, why this is not merely a service/report/dashboard/database/marketplace wrapper.

## Final Response

After writing the file, respond concisely with:

- idea concept;
- absolute path;
- simulated, working-chat, and fresh-chat Zero to One scores, and why the idea passed the simulated `>85` gate and both real 82+ thresholds;

## advice for your success in finding the right idea
Do not self-censor just because an idea challenges convention, sounds uncomfortable, or goes against socially accepted assumptions. The objective here is not social approval or consensus — it is to identify ideas that are actually strong, defensible, and true AND that can pass the Zero to One gates. The greatest ideas for business are often counter-intuitive at the time

If needed enforce this on subagents.