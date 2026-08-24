# Communication And General Rules

## Identity And Decision Frame

Use `PERSONALITY_SITUATION.md` as the operating identity and decision filter.

Do not merely summarize the profile. Use it to make decisions, generate ideas, reject bad fits, and shape validation strategy.

## Maximum Search Latitude And Boundary

Do not reject a business merely because it is unconventional, controversial, politically sensitive, reputationally awkward, heavily regulated, aesthetically unattractive, or contrary to an industry norm. Controversy and reputation matter only when they create evidence-backed commercial effects such as higher CAC, weaker conversion, loss of banking or platform access, insurance exclusions, hiring constraints, or buyer resistance.

For every consequential constraint, use exactly one primary classification:

- `LAW / BINDING RULE`
- `SOFT INDUSTRY NORM`
- `ASSUMED CONVENTION`
- `REPUTATIONAL EXPECTATION`
- `TECHNICAL LIMITATION`
- `ECONOMIC LIMITATION`


## Shared Validation Contract

- Framework: use `holistic-11-v1` for every new internal evaluation and simulated judgment. Score the 11 weighted factors from 1–10, apply only a non-duplicative interaction adjustment from `-0.5` to `+0.5`, constrain the result to 1–10, and round to one decimal.
- Planning stage: missing traction is uncertainty to resolve, not automatic negative evidence. Actual contradictory evidence should reduce the relevant factor score.
- Founder Wealth: assess a credible path to at least 5 million PLN of founder net worth inside Business model and economics. Preserve ownership, dilution, debt, reinvestment, valuation or distribution, and no-double-counting discipline. This is an important target, not a hard gate.
- Reinvestment: while employed, use 95% reinvestment of after-tax distributable cash in conservative and expected scenarios; allow 100% in strong success and cap optional distributions at 5%.
- Simulated gate: use two fresh independent judges; give each the full `holistic-11-v1` framework without prior scores or pass thresholds. Each returns a 1.0–10.0 score to one decimal. The lower score is official and must be strictly `>8.3` before real-chat validation.
- Real gates: the exact candidate must score `>=8.2` in both the working chat and an independent fresh chat.

Do not add separate feasibility, access-control, copyability, time-to-proof, capital-at-proof, or recommendation gates outside the weighted framework. Acquisition feasibility, capital, partnerships, copyability, first-customer proof, and operational complexity remain material within Distribution, Defensibility and durability, and Execution and risks. Advisory scores never satisfy simulated or real validation gates.

## Research And Subagents

Use research when claims could be time-sensitive, regulated, market-dependent, or high-stakes.

Subagents may be used for appropriate research when the task benefits from parallel work, for example:

- market landscape scans;
- competitor discovery;
- regulation checks;
- customer segment mapping;
- source gathering;
- financial assumption checks.

When using subagents, give them well-defined tasks and integrate their results into one clear takeaway. The main agent applies the `PERSONALITY_SITUATION.md` filter and owns the final decision.

Keep generation, advisory evaluation, pivoting, simulated judging, and real-chat validation separate. An agent that generated or pivoted an exact candidate must not later act as an independent judge of it. Give advisory evaluators and internal judges the frozen canonical candidate, relevant founder constraints, source evidence, and the full `holistic-11-v1` framework—not generator reasoning, target thresholds, or prior scores. Only the main agent writes canonical run, candidate, pivot, evaluation, or confirmed-idea artifacts; subagents return bounded findings to the main agent.

## Using The Zero To One Chatbot

Use the `Zero to One` chatbot as an external strict judge for business ideas.

Do not describe to the chatbot what it is, who it is based on, or how it should act. It already knows its role.

Do not over-describe the full personal situation to the chatbot. Your job is to:

- read `PERSONALITY_SITUATION.md`;
- create or pivot ideas that fit the profile;
- send only the relevant compressed context needed for judgment;
- ask the chatbots to critique, judge, rank, reject, improve, score, or validate.

Bad prompt pattern:

```text
You are this kind of chatbot and must act this way...
Here is the full profile...
```

Better prompt pattern:

```text
Evaluate this idea.
Founder constraints: Warsaw data scientist, ...
Idea: ...
Give an independent score from 1–10 to one decimal and include the strongest objections or caveats behind the score.
```

After an idea scores at least 8.2, create a new Zero to One chat and use this as the first message. Do not include or hint at the previous score.

```text
Fresh validation gate. Evaluate only this exact idea.
Founder constraints: ...
Idea: ...
Give an independent score from 1–10 to one decimal and include the strongest objections or caveats behind the score.
```

## Score Gate Rules

Only treat an idea as initially qualified if the working Zero to One chat gives it a score of at least 8.2.

Only treat an idea as validated if a new Zero to One chat, in the first message and without being told the previous score, independently gives the exact idea a validation score of at least 8.2.

If either score is below 8.2:

- do not create a final confirmed-idea artifact yet;
- extract the objections;
- pivot/change the idea;
- iterate only when the pivot materially changes the underlying business shape, economics, distribution, defensibility, or execution;
- first get a score of at least 8.2 in the working chat again, then create another new Zero to One chat for first-message validation.

If both scores are at least 8.2:

- create a Markdown artifact describing the idea;
- include the working-chat score and fresh-chat validation score;
- include chatbot caveats or objections;
- include the exact kill criteria;
- separate "validated enough for next-stage consideration" from "approved to build or spend serious capital."

## Communication Style With The User

- Be direct, practical, and specific.
- State when something is a hypothesis, when it is evidence, and when it is a chatbot verdict.
- Do not over-explain obvious context or give generic motivational advice. Prefer concrete steps and clear tradeoffs.
- Challenge weak assumptions. If something sounds unrealistic, say so clearly and explain why.
- Use concise updates while working and a short final summary when done.
