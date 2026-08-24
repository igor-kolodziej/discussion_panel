# Simulated Round 230: RAGSource Buyer Release Sprint

Date: 2026-05-30 Europe/Warsaw

## Gate Settings

- Real working-chat Zero To One gate: `>=85`
- Real fresh-chat Zero To One gate: `>=85`
- Internal simulation gate: strictly `>87`
- Prompt hygiene: no evaluator cap instructions in the Zero To One prompt

## Why This Branch Exists Despite AI-Security Fatigue

The prior RAG/agent evidence branch produced the closest current working result (`84 / 100`) but then collapsed in stricter thinking validation because the scope was too broad, especially around tool-using agents, false assurance, and general appsec credibility.

Round 230 is materially narrower:

- only read-only RAG or enterprise-search retrieval;
- no tool-using agents;
- no production tests;
- no regulated/high-risk AI;
- no generic questionnaire answers;
- no broad AI red-team promise;
- only written buyer conditions blocking PO, renewal, pilot expansion, or production deployment;
- proof artifact is bounded source-isolation traces plus buyer-release evidence.

## Raw Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day proof | Copy risk / cap note | Internal score |
|---:|---|---|---|---|---|---|---:|
| 1 | RAGSource buyer release sprint | SaaS vendors via appsec/SOC2/fCISO partners | written buyer condition blocks PO/deployment over source isolation | authorized sandbox, source manifest, trace evidence, partner ticket | 6 paid sprints, 4 buyer outcomes | appsec incumbents, but narrower than prior RAGProbe | 88.4 |
| 2 | RAGProbe broad buyer security sprint | SaaS vendors | buyer asks for AI security evidence | test traces | previous near-miss | already failed 84/64 | 84 |
| 3 | RAGModule appsec overflow bench | appsec partners | partner needs annex | white-label module | previous failed | partner internalization | 83 |
| 4 | AIQ partner ticket book | SOC2/fCISO partners | AI questionnaire blocks deal | ticket book | previous failed | template/internalization | 82 |
| 5 | MCP tool-action release sprint | AI SaaS vendors | buyer worried about tool calls | sandbox action traces | previous failed | tool risk/appsec incumbents | 73 |
| 6 | AppExchange retest lane | Salesforce ISVs | failed platform security review | retest packet | 4 cases | incumbents/platform decision | 79 |
| 7 | ConsentGate Entra release | SaaS vendors | Microsoft consent block | app registration evidence | 5 releases | MSPs copy | 74 |
| 8 | KSeF large-invoice release | suppliers | AP hold | buyer AP file | 5 releases | accountants/ERP | 79 |
| 9 | CyberBind subjectivity release | brokers/MSPs | insurance bind subjectivity | underwriter evidence | 6 cases | remediation/misstatement | 82 |
| 10 | BrokerLock subjectivity case book | brokers | repeated cases | broker case book | failed | not hard control | 70 |
| 11 | SENTApparel dispatch gate | wholesalers | SENT shipment release | dispatch mandate | failed 68 | fast normalization/incumbents | 68 |
| 12 | Data Act ag invoice release | ag contractors | invoice disputes | machine logs | 5 released invoices | Data Act duplicate, OEM | 79 |
| 13 | RAGSource source-only partner retainer | partners | repeated source-isolation tickets | prepaid slots | 3 retainers | partner internalization | 80 |
| 14 | RAGSource buyer escrow release | SaaS vendor/buyer | buyer holdback | evidence escrow | 3 holdbacks | escrow/legal/artificial | 72 |
| 15 | AI sandbox fixture kit | AI SaaS vendors | buyer asks for test sandbox | fixture templates | 10 kits | tool/app not hard control | 68 |
| 16 | LLM provider no-training evidence desk | SaaS vendors | buyer asks data use proof | vendor/provider settings | 10 packs | AIQ duplicate/templates | 76 |
| 17 | RAG tenant-label leakage bug bounty | SaaS vendors | buyer asks proof | paid tests | 6 tests | appsec/internal testing | 74 |
| 18 | ISO 42001 pre-audit buyer release | SaaS vendors | buyer asks ISO path | gap pack | 5 packs | consultants/certification | 62 |
| 19 | AI Act Article 50 deployer handoff | AI vendors | transparency/deployer docs | release packet | previous failed | legal/copyable | 78 |
| 20 | RAG legal hold search isolation | legal SaaS | buyer asks data-boundary proof | sandbox traces | 3 cases | legal/sensitive | 69 |
| 21 | Customer-support copilot source-isolation | support SaaS vendors | buyer asks KB boundary proof | source-isolation traces | 5 cases | support platforms internalize | 83 |
| 22 | Document-processing RAG source-isolation | doc AI SaaS | buyer asks document isolation proof | test corpus | 5 cases | broader appsec | 84 |
| 23 | Sales enablement RAG proof | sales SaaS | buyer asks prompt/data proof | trace packet | 5 cases | lower urgency | 75 |
| 24 | Healthcare RAG release | health SaaS | PHI/data segregation | test traces | 3 cases | health data/regulated | 55 |
| 25 | Finance RAG release | fintech/reg-finance | model/data risk | evidence | 3 cases | regulated finance/DORA | 58 |
| 26 | HR RAG release | HR SaaS | buyer bias/data concern | evidence | 3 cases | high-risk HR | 52 |
| 27 | RAG incident no-go triage | SaaS vendors | buyer found leakage | no-go memo | 4 cases | incident/security consulting | 70 |
| 28 | RAG procurement appendix generator | SaaS vendors | AI appendix needed | appendix | 10 packs | report/template | 60 |
| 29 | RAG formal red-team partner | appsec firms | red-team demand | formal report | 3 cases | needs recognized firm | 73 |
| 30 | RAG buyer safe-log export | SaaS vendors | buyer wants logs | log packet | 8 cases | dashboard/app | 65 |
| 31 | Source manifest notarization | SaaS vendors | buyer asks corpus governance | manifest | 10 cases | paper artifact | 58 |
| 32 | RAG data-room evidence transfer | SaaS vendors | buyer asks docs | data room | 10 cases | generic evidence room | 61 |
| 33 | Read-only RAG pilot approval lane | SaaS vendors | buyer holds pilot approval | test traces | 6 pilots | close to candidate | 86 |
| 34 | RAG eval benchmark subscription | SaaS vendors | recurring evals | benchmark | 10 subs | app/service | 70 |
| 35 | RAG source-isolation incident insurance evidence | cyber brokers | underwriter asks RAG controls | evidence | 4 cases | cyberbind duplicate | 76 |
| 36 | RAG partner ticket-book buyout | small appsec partner | current AI tickets | customer transfer | 1 book | seller rare/support/trust | 72 |
| 37 | RAG procurement case finance | SaaS vendors | buyer holdback | finance evidence | 2 cases | financing/legal | 50 |
| 38 | RAG security questionnaire-only lane | SaaS vendors | questionnaire | answers | 10 packs | AIQ duplicate | 62 |
| 39 | RAG source-isolation no-code tool | SaaS vendors | self-test | app | 20 users | dashboard/tool | 57 |
| 40 | AI vendor evidence pack for retail buyers | SaaS vendors | buyer asks AI docs | pack | 8 cases | generic/copy | 67 |

## Selected Candidate

**RAGSource Buyer Release Sprint**

## Simulated Score

**88.4 / 100**

## Internal Scoring Rationale

This is the only AI branch still worth one clean test because it removes the exact elements that made the near-miss fragile:

- written buyer release condition required;
- read-only retrieval only;
- no agent tool actions;
- no production writes;
- no regulated/high-risk use cases;
- partner-routed trust channel;
- narrow source-isolation artifact rather than broad AI security assurance.

The first proof is not "we wrote a better answer"; it is buyer-progress evidence from a bounded test packet tied to a commercial release event.

## Internal Caps Applied

- Cap below 82 if there is no written buyer condition tied to PO, renewal, pilot expansion, or production deployment.
- Cap below 85 if tool-using agents, production tests, regulated workflows, or broad AI red-team claims are included.
- Cap below 87 if the artifact is only a questionnaire or policy answer instead of executable source-isolation traces.
- Cap below 87 if partners do not route repeat cases or if buyer outcomes are not documented.

## Main Risks To Test

1. Appsec and AI-security incumbents may still own credibility.
2. Partners may internalize the recipe.
3. Buyers may still demand formal penetration testing or broader assurance.
4. Sensitive source/log access creates trust friction.
5. Failures often require remediation.
6. Short tests can create false assurance unless scope is tightly bounded.

## Gate Decision

Advance to working-chat Zero To One validation using:

`zero_to_one_prompt_ragsource_buyer_release.txt`
