# New Business Opportunity

Use `$business-opportunity` to start a new founder-fit opportunity run, or resume the run ID supplied by the user.

Treat these as the only canonical inputs:

- founder constraints: `PERSONALITY_SITUATION.md`
- evaluation framework: `Personalities/ZeroToOne.txt`
- workflow rules, budgets, and qualification logic: `config/opportunity-workflow.json`
- state, artifact contracts, and validation: `scripts/opportunity.py`

Follow `.agents/skills/business-opportunity/SKILL.md`. Keep initial discovery blind to history and scoring, introduce the active historical indexes only at the skill's delayed-dedup stage, and keep development judgment separate from final holdouts. Do not use `prompts/PromoLeak/`; it belongs to a separate execution workflow.

Return the CLI-published terminal outcome, including an explicit non-confirmation or contested report when no candidate qualifies. Never create a confirmed artifact from a working score, lower a configured rule, or hide an interrupted or failed stage.
