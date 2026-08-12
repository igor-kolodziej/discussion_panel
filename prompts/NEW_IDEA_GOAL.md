# Goal: Generate One Validated Business Idea

Produce one new confirmed business idea. Save as `CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md` in `ideas/`. If nothing passes all gates, produce no file.

## Context (read first)

- `PERSONALITY_SITUATION.md` — founder profile and constraints
- `COMMUNICATION_AND_GENERAL_RULES.md` — ideation rules, chatbot usage, score gates, capital discipline
- `BROWSER_STARTUP.md` — how to open and control the browser
- `Personalities/ZeroToOne.txt` — system prompt for simulated panels
- `ideas/` — overlap and learning source; materially improved versions are allowed when the difference and resolved objections are documented
- Full workflow and idea file structure: `prompts/NEW_IDEA_AGENT_PROMPT.md`

## Pass/Fail Gates

### Gate 0 — Founder Wealth And Reachability

Before simulated scoring, require a credible path to at least 5 million PLN of founder net worth and a credible paid pilot, deposit, preorder, purchase order, paid discovery engagement, or budget-backed commitment within 180 days while risking no more than 40,000 PLN. These are non-compensating gates: failure of either blocks the panel regardless of advisory score.

### Gate 1 — Simulated Zero To One Panel (score > 83)

Up to 6 finalists, two independent subagents per idea using `Personalities/ZeroToOne.txt` as system prompt, with up to 3 subagents active at once. Each scores 0–100 with objections, control-point tier, and copy risk. If 2+ share the same fatal objection → pivot. No idea >83 → pivot and re-run. Score >83 is necessary but never sufficient.

### Gate 2 — Real Zero To One Working-Chat (score ≥ 82)

Only after Gate 1. Ask for 0–100 with objections. Do not tell the chatbot how to score or what to cap. If <82 → pivot from Gate 1.

### Gate 3 — Real Zero To One Fresh-Chat Validation (score ≥ 82)

New chat. First message: independent 0–100 validation. No hint of previous score. If <82 → pivot from Gate 1.

### Chatbot Rules

Never describe to the chatbot what it is or how it should act. Founder context: unknown Warsaw solo founder, contractors allowed, max 100,000 PLN, 12-month POC, part-time. Send only compressed founder constraints and the idea. Always wait for the full answer — never interrupt. Take its feedback seriously; if you disagree, present strong arguments and discuss.

## Output

Write the confirmed idea file only when both Gate 0 requirements pass, simulated >83, and both real scores ≥82. Structure defined in `prompts/NEW_IDEA_AGENT_PROMPT.md`.
