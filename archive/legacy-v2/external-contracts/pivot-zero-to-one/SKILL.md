---
name: pivot-zero-to-one
description: Transform weak or impermissibly structured business candidates into disciplined, lawful structural pivots using an evaluator's diagnosis and objections. Use when asked to pivot, materially improve, rescue, reshape, find lawful alternatives, or find stronger versions of an evaluated idea. Preserve the valuable economic mechanism while changing broken economics, payer, ownership, financing, distribution, licensing, geography, risk allocation, defensibility, or business shape. Do not score, validate, or generate unrelated ideas.
---

# Pivot Zero-to-One

Create structural revisions from a candidate and its evaluation. Do not score the revisions.

## Load live context

Read these files completely before pivoting:

1. `/Users/igor/Desktop/discussion_panel/Personalities/ZeroToOne.txt`
2. `/Users/igor/Desktop/discussion_panel/PERSONALITY_SITUATION.md`
3. `/Users/igor/Desktop/discussion_panel/COMMUNICATION_AND_GENERAL_RULES.md`
4. `/Users/igor/Desktop/discussion_panel/prompts/NEW_IDEA_AGENT_PROMPT.md`

Require both the original candidate and an evaluator diagnosis containing objections or weaknesses. If the evaluation is missing, ask the user to run `$evaluate-zero-to-one`; do not silently combine the roles.

A pivoter is not an independent judge. It must not later evaluate or panel the exact pivot it produced. Return the pivot to a fresh `$evaluate-zero-to-one` agent, and use fresh independent simulated judges if it advances.

## Diagnose the pivot boundary

Extract:

- the strongest evidence-backed or explicitly plausible insight worth preserving;
- the primary failure mechanism;
- the buyer, pain, willingness-to-pay, margin, CAC, payback, retention, trust, authority, channel, resource-access, and defensibility assumptions implicated by that failure;
- any decisive evaluator objection and any business shape that must not be repeated;
- each consequential constraint classified as `LAW / BINDING RULE`, `SOFT INDUSTRY NORM`, `ASSUMED CONVENTION`, `REPUTATIONAL EXPECTATION`, `TECHNICAL LIMITATION`, or `ECONOMIC LIMITATION`.

Treat the evaluator's verdict as judgment, not market evidence. Preserve an insight only when it remains useful after the objection is accepted. Split mixed constraints and do not elevate a norm, convention, or reputational expectation into binding law.

## Produce disciplined pivots

Create 1–3 pivots. Prefer one strong pivot over padded variants.

Each pivot must materially change at least one broken structural dimension. Deliberately test payer, economic buyer, asset ownership, financing, distribution, licensing, geography, risk allocation, value capture, painful event, delivery model, trust mechanism, authority, scarce resource, and defensibility mechanism. A workaround must improve the opportunity under the complete 11-factor framework rather than merely relabeling the weakness.

When a candidate contains illegal conduct, deception, coercion, or exploitation that creates serious harm:

1. isolate the lawful economic mechanism worth preserving;
2. remove the prohibited implementation element;
3. attempt a lawful, safer structure using different rights, roles, contracts, counterparties, risk allocation, or value capture;
4. produce no pivot when the prohibited element is indispensable to the value proposition.

Do not reject a lawful pivot merely because it remains controversial or reputationally unusual. Treat those factors only through concrete commercial effects. Do not rely on:

- cosmetic renaming or feature changes;
- the same buyer and trust mechanism with different wording;
- unspecified partnerships or speculative access;
- generic consulting, dashboards, CRMs, or AI wrappers;
- service-heavy delivery without a path to a compounding product, data, workflow, distribution, or transaction advantage;
- an advantage incumbents can cheaply buy or reproduce without a credible compounding response;
- pivots that solve novelty but not margins, CAC, payback, retention, or willingness to pay.

Keep every pivot realistic for the founder's time, capital, location, and distribution preferences, accounting for competent use of AI, contractors, advisors, and hiring. Do not assume AI replaces credentials, relationships, physical operations, regulatory requirements, or tacit knowledge. Include the fastest credible first-customer proof, expected time, capital exposure, and critical dependencies as execution evidence rather than a separate feasibility gate.

Explicitly assess a credible path to at least 5 million PLN of founder net worth inside business model and economics. Model customers or volume, pricing, margins, debt and capital needs, founder ownership and dilution, reinvestment, business value or cumulative distributions, and timing without double-counting. While the founder remains employed, use 95% reinvestment of after-tax distributable cash in conservative and expected scenarios, allow 100% in strong success, and cap optional distributions at 5%. Founder Wealth is an important target, not a hard gate. Label new factual claims as hypotheses requiring research.

Do not apply validation scores. Preserve the downstream constants for routing only: framework ID `holistic-11-v1`; the lower of two fresh independent simulated scores strictly `>8.3`; then working-chat and fresh-chat scores each `>=8.2` on the exact pivot.

## Output each pivot

```markdown
# Zero-to-One Pivot: {name}

## Preserved Insight
## Original Rule and Constraint Classification
## Structural Change
## Circumvention Design
## Lawful-Structure Check
## Target Niche and Buyer
## Painful Event and Willingness to Pay
## Value and Profit Wedge
## Domination Wedge
## Acquisition Channel
## Defensibility and Access Mechanism
## Cold Start and Resource Bootstrap
## Expansion Path
## Founder Wealth Assessment
## First-Customer Validation and Execution Plan
## Minimum People Stack
## Principal Risk
## Residual Rule, Reputation, Technical, and Economic Risks
## First Disconfirming Test
## Evidence Preserved
## New Hypotheses
## Why This Is Not the Original Failure Shape
```

End with a concise comparison explaining which pivot should return to `$evaluate-zero-to-one` first and why. This is a prioritization judgment, not a score or validation.

Only the main agent may write a canonical pivot artifact. When acting as a subagent, return bounded pivot findings to the main agent without writing files. When acting as the main agent and the user supplies an originating run-folder path, write each pivot as `pivot_<slug>_YYYYMMDD_HHMMSS.md` inside that folder; otherwise return the pivots in the response only. Never write to `ideas/`, create `CONFIRMED_IDEA_*`, contact the real Zero to One chatbot, run simulated panels, assign scores, or claim validation.
