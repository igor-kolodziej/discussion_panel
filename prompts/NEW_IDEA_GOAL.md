# Goal: Generate One Validated Business Idea

Produce one new confirmed business idea. Save it as `CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md` in `ideas/`. If nothing passes all score gates, produce no file.

## Context (read first)

- `PERSONALITY_SITUATION.md` — founder profile and constraints
- `COMMUNICATION_AND_GENERAL_RULES.md` — ideation rules, validation framework, chatbot usage, score gates, and capital discipline
- `BROWSER_STARTUP.md` — how to open and control the browser
- `Personalities/ZeroToOne.txt` — full `holistic-11-v1` framework for internal judges
- `ideas/` — overlap and learning source; materially improved versions are allowed when the difference and resolved objections are documented
- Full workflow and idea file structure: `prompts/NEW_IDEA_AGENT_PROMPT.md`

## Operating Contract

Run a fresh cross-sector search with maximum permitted latitude. Deliberately inspect unconventional, controversial, politically sensitive, regulated, low-status, incumbent-hostile, and reputationally awkward markets without treating those traits as vetoes. Keep generation separate from evaluation and validation. Classify material constraints as `SOFT INDUSTRY NORM`, `ASSUMED CONVENTION`, `REPUTATIONAL EXPECTATION`, `TECHNICAL LIMITATION`, or `ECONOMIC LIMITATION`.

Use the five independent creative lenses defined in the full prompt: Taboo-Space Explorer, Incentive-Hacker, Incumbent-Attacker, Rule-Structure Analyst, and First-Principles Extremist. No generator or pivoter may later independently judge the same exact candidate, and only the main agent writes canonical artifacts.

Use `holistic-11-v1` for all new internal evaluations and simulated judgments. Treat missing planning-stage traction as uncertainty, not adverse evidence; penalize actual contradictory evidence. Account for realistic AI acceleration without assuming AI replaces credentials, relationships, physical operations, regulation, or tacit knowledge.

Assess a credible path to at least 5 million PLN of founder net worth inside Business model and economics, including ownership, dilution, debt, reinvestment, value or distributions, timing, and no double counting. Founder Wealth is an important target, not a pass/fail gate.

## Validation Gates

### Gate 1 — Simulated Zero To One Panel (score `>8.3`)

Use up to 6 finalists and two fresh independent judges per exact candidate, with up to 3 judges active at once. Give each judge the frozen candidate, relevant founder constraints and source evidence, and the full `holistic-11-v1` framework from `Personalities/ZeroToOne.txt`. Do not reveal prior scores, generator reasoning, or the pass threshold. Each judge returns a 1.0–10.0 score to one decimal plus the strongest objections. The lower score is official and must be strictly `>8.3`.

One orchestration run may use the initial 40–60-hypothesis wave plus at most two regeneration waves. Start another wave only when the rejection record identifies materially untested mechanisms or structural transformations. If no candidate clears the simulated gate after the third wave, or every remaining pivot repeats the same decisive failure, stop with no confirmed artifact; never lower a gate to force an outcome.

### Gate 2 — Real Zero To One Working Chat (score `>=8.2`)

Only after Gate 1. Send the exact idea and compressed founder constraints. Ask only for an independent 1–10 score to one decimal with objections; do not send the internal framework, prior scores, or threshold. If the score is below 8.2, return to evaluation and material pivoting.

### Gate 3 — Real Zero To One Fresh Chat (score `>=8.2`)

Start a new chat. The first message must independently request a 1–10 score to one decimal with objections for the exact idea and compressed founder constraints. Do not reveal or hint at the previous score, internal framework, or threshold. If the score is below 8.2, return to evaluation and material pivoting.

### Chatbot Rules

Never describe to the chatbot what it is or how it should act. Founder context: unknown Warsaw solo founder, contractors allowed, approximately 100,000 PLN available, part-time while employed. Send only the compressed context needed for judgment and the exact idea. Always wait for the full answer. Take the feedback seriously; if you disagree, present strong evidence and discuss it.

## Output

Write the confirmed idea file only when the exact candidate's official lower simulated score is `>8.3` and both real scores are `>=8.2`. Record `holistic-11-v1`, all three decimal scores, objections, and a Founder Wealth assessment without pass/fail language. Use the structure in `prompts/NEW_IDEA_AGENT_PROMPT.md`.
