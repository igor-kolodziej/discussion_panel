# Goal: Generate One Validated Business Idea

Produce one new, non-redundant confirmed business idea. Save as `CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md` in `ideas/`. If nothing passes all gates, produce no file.

## Context (read first)

- `PERSONALITY_SITUATION.md` — founder profile and constraints
- `COMMUNICATION_AND_GENERAL_RULES.md` — ideation rules, chatbot usage, score gates, capital discipline
- `BROWSER_STARTUP.md` — how to open and control the browser
- `Personalities/ZeroToOne.txt` — system prompt for simulated panels
- `ideas/` — existing ideas (do not duplicate)
- Full workflow and idea file structure: `prompts/NEW_IDEA_AGENT_PROMPT.md`

## Pass/Fail Gates

### Gate 1 — Simulated Zero To One Panel (score > 85)

Up to 6 finalists, one subagent each using `Personalities/ZeroToOne.txt` as system prompt. Each scores 0–100 with objections, control-point tier, copy risk. If 2+ share same fatal objection → pivot. No idea >85 → pivot and re-run. Score >85 necessary but never sufficient.

### Gate 2 — Real Zero To One Working-Chat (score ≥ 82)

Only after Gate 1. Ask for 0–100 with objections. Do not tell the chatbot how to score or what to cap. If <82 → pivot from Gate 1.

### Gate 3 — Real Zero To One Fresh-Chat Validation (score ≥ 82)

New chat. First message: independent 0–100 validation. No hint of previous score. If <82 → pivot from Gate 1.

### Chatbot Rules

Never describe to the chatbot what it is or how it should act. Founder context: unknown Warsaw solo founder, contractors allowed, max 100,000 PLN, 12-month POC, part-time. Send only compressed founder constraints and the idea. Always wait for the full answer — never interrupt. Take its feedback seriously; if you disagree, present strong arguments and discuss.

## Output

Write the confirmed idea file only when simulated >85 AND both real scores ≥82. Structure defined in `prompts/NEW_IDEA_AGENT_PROMPT.md`.
