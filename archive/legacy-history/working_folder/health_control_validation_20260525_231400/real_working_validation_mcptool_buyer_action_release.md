# Real Working-Chat Validation: MCPToolFence Buyer Action Release Sprint

Date: 2026-05-30 Europe/Warsaw
Gate: working Zero To One score must be >=85.

## Result

**Working Zero To One score: 73 / 100**

**Gate decision: FAIL**

Round 215 does not advance to fresh-chat validation.

## Submitted Prompt

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_mcptool_buyer_action_release.txt`

The submitted prompt used the clean Zero To One opening and did not include internal caps or evaluator instructions. Composer checks showed no stale `ColoPower`, `Round 214`, or `Amazon Vendor Central` text before submission.

## Zero To One Summary

Zero To One evaluated this as a buyer-action release sprint rather than a generic AI security review. It said the idea is sharper than ordinary AI questionnaire work because tool-using agents and MCP integrations create concrete buyer concerns: unsafe API calls, credential overreach, data writes, repository changes, ticket creation, external messages, audit gaps, and indirect prompt injection.

The idea still failed because sandboxed traces are not formal assurance. The evaluator saw the work as close to AI red teaming, appsec testing, and security review, where established appsec and AI-security firms have more credibility. It also emphasized false-assurance risk, remediation drift, sensitive access, and partner internalization.

## Strongest Objections Captured

- Appsec and AI-security firms are natural incumbents and can offer broader credibility.
- Buyers may still demand formal penetration testing, SOC2 evidence, ISO 42001, DPIA, legal review, AI Act analysis, or product remediation.
- Short sandbox traces can show bounded behavior under scoped conditions, but cannot prove an agent is safe.
- Many cases will need engineering remediation when overbroad credentials, missing audit logs, weak allowlists, or unsafe tool calls are discovered.
- Tool-using agents can cause real side effects, so even sandbox testing needs strict controls.
- Sensitive evidence access is a trust barrier: tool catalogs, API permissions, sandbox credentials, logs, model settings, prompt traces, and customer data-flow details.
- Appsec boutiques and fractional CISOs may internalize the module after several cases.
- MCP tooling is evolving quickly, so evidence formats, buyer concerns, and controls may change faster than the playbook.

## Evaluator's Best Move

The evaluator recommended pursuing only through partners, positioned as:

**White-label MCP/tool-action buyer-release sprint for appsec and SOC2 partners.**

Required POC constraints:

- written buyer blocker text and blocked commercial value above 100,000 PLN;
- sandbox/demo environments only, with explicit written authorization;
- start with read-only or human-approved tool actions;
- AI-security/appsec reviewer on every first case;
- reject production writes, external email, payments, code execution, privileged admin actions, and regulated high-risk workflows;
- continue only if the first 60 days produce six prepaid cases, four partner/buyer progress outcomes, and gross margin above 60%.

## Lesson

Do not continue AI/appsec evidence variants without actual exclusive partner flow, recognized appsec reviewer credibility, or buyer-accepted proof already in hand. A sharper MCP/tool-action artifact still scores only 73 because formal-assurance substitution and incumbent credibility dominate.
