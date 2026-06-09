# Simulated Round 298: Factor-Confirmed KSeF Funding Release Desk

Date: 2026-05-31 Europe/Warsaw

Gate policy:

- Simulated score must be strictly greater than 87 before real Zero To One validation.
- Working-chat and fresh-chat Zero To One gates are both >=85.
- Internal scoring caps are used only in this simulation note and are not included in Zero To One prompts.

## Why This Round Exists

Round 297, KSeF Payable-Acknowledged Funding Release Desk, passed the working chat at 87 but failed fresh validation at 67. The fresh evaluator's strongest narrowing was explicit: start with factoring/funding-release cases rather than ordinary supplier payment chasing, because factors already think in receivable eligibility, confirmation, reserves, debtor acceptance, and evidence conditions.

This round tests that narrower payment stream. The buyer is no longer a broad supplier with an unpaid invoice. The accepted case must have a written factor, receivables-finance provider, or factoring broker condition saying funding, reserve release, eligibility, or debtor confirmation is blocked by a defined KSeF/AP evidence defect.

The first proof is factor funding, factor reserve release, receivable eligibility restored, debtor confirmation accepted by the factor, or a paid clean no-go. It is not AP chasing and not KSeF support.

## Current Facts Used

- The official KSeF page says mandatory KSeF issuing applies from 1 February 2026 for taxpayers above the 2024 sales threshold of 200m PLN and from 1 April 2026 for most remaining taxpayers, with receiving through KSeF mandatory from 1 February 2026.
- The same official page says KSeF automatically assigns a unique identifying number to issued structured invoices, and that invoices received through KSeF become a core operational artifact.
- FA(3), KSeF numbers, UPO/access evidence, structured invoice receipt, buyer access, and correction routing are therefore live operational evidence points for factors and receivables-finance providers assessing Polish invoice eligibility.

Sources:

- `https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/`
- `https://ksef.podatki.gov.pl/ksef-news/wystawianie-i-otrzymywanie-faktur/`

## 38 Raw Candidates Screened

| # | Candidate | Buyer / payer | Acute trigger | 60-day control proof | Internal score |
|---:|---|---|---|---|---:|
| 1 | Factor-confirmed KSeF funding release | Suppliers using factoring, factoring brokers, receivables-finance providers | Funding, eligibility, confirmation, or reserve release is held by a factor over KSeF/AP evidence | Written factor hold condition, seller mandate, invoice evidence, first funding/release/no-go | 88.8 |
| 2 | Broad KSeF unpaid invoice release | Suppliers | Buyer says KSeF issue blocks AP | Supplier mandate and AP packet | 84 prior |
| 3 | KSeF payable-acknowledged AP release | Suppliers | Buyer says payable but AP evidence blocks payment | Buyer AP acknowledgement | 88.4 prior, fresh failed |
| 4 | KSeF ordinary factoring support | Factoring clients | Factor asks for KSeF docs generally | Upload packet | 82 |
| 5 | KSeF debtor-confirmation sprint | Factoring brokers | Debtor has not confirmed receivable | Debtor response | 83 |
| 6 | KSeF reserve-only release | Suppliers | Factor has been paid but reserve is held pending KSeF proof | Reserve ledger and release | 85 |
| 7 | KSeF public-sector factor release | Contractors | Public debtor KSeF evidence blocks factor | Factor hold notice | 84 |
| 8 | KSeF construction milestone factor release | Subcontractors | Milestone invoice funding blocked | Factor condition and protocol | 84 |
| 9 | KSeF correction-route finance release | Suppliers | Factor needs accepted correction path | Accountant-approved correction | 82 |
| 10 | KSeF buyer-access QR release | Suppliers/factors | Buyer cannot access or confirm invoice | Access proof | 81 |
| 11 | KSeF self-billing finance release | Suppliers | Self-bill or VAT RR evidence blocks funding | Buyer authority | 78 |
| 12 | KSeF attachment-enabled utility invoice funding | Utility/telecom/fuel suppliers | invoice annex evidence blocks receivable sale | Factor approval | 80 |
| 13 | KSeF accounting-office channel desk | Accounting offices | clients have KSeF payment blockers | referral queue | 82 |
| 14 | KSeF ERP integrator overflow desk | ERP integrators | failed invoice batches | fixed batches | 76 |
| 15 | KSeF factoring broker white-label desk | factoring brokers | repeated client evidence blockers | broker-routed paid cases | 86 |
| 16 | VoP payment mismatch release | exporters | buyer bank/vendor-master mismatch | AP mismatch text | 78 prior |
| 17 | Customer-acknowledged true-up release | SaaS vendors | accepted receivable stuck in AP | AP acknowledgement | 84 prior |
| 18 | Factor reserve release unrelated to KSeF | SMEs | paid debtor but reserve held | factor ledger | 75 prior |
| 19 | Credit memo cashout | SMEs | vendor credit exists | refund/offset | 79 prior |
| 20 | Unapplied cash application | suppliers | customer paid but cash unapplied | remittance/cash application | 73 prior |
| 21 | PSP reserve maturity release | merchants | PSP reserve due | PSP release | 70 prior |
| 22 | Cloud marketplace payout release | SaaS vendors | private-offer payout mismatch | support case | 76 prior |
| 23 | Amazon Vendor Central deduction recovery | 1P vendors | deductions taken | Vendor Central disputes | 67 prior |
| 24 | Retail OTIF chargeback recovery | CPG vendors | operational deductions | retailer portal disputes | 76 prior |
| 25 | 3PL overbilling recovery | ecommerce brands | 3PL invoice mismatch | credit memo | 71 prior |
| 26 | Freight detention credit recovery | importers/exporters | accessorial overbilling | carrier credit | 78 internal |
| 27 | OTA hotel settlement recovery | hotel groups | OTA statement mismatch | OTA credit | 76 prior |
| 28 | MDF claim lockbox | MSPs/VARs | approved MDF not claimed | portal reimbursement | 78 prior |
| 29 | Partner incentive claim release | Microsoft partners | stuck incentives | Partner Center case | 72 prior |
| 30 | Fit-out allowance release | tenants | landlord allowance due | landlord packet | 80 prior |
| 31 | Construction retention release | subcontractors | retention due | acceptance and payment | 75 prior |
| 32 | Public guarantee line release | contractors | guarantee collateral tied | bank/beneficiary release | 76 prior |
| 33 | Utility deposit refund | closed sites | deposit due | refund | 74 prior |
| 34 | Supplier rebate accrual release | distributors | rebate earned but unpaid | vendor credit | 76 prior |
| 35 | Approved RMA labor credit recovery | installers | accepted RMA credit | OEM credit | 72 prior |
| 36 | Mill certificate AP hold release | industrial suppliers | payment held on certificates | customer acceptance | 73 prior |
| 37 | LC discrepancy release | exporters | bank discrepancy | amended docs/payment | 74 prior |
| 38 | Debtor-scheduled payment monitoring | SaaS vendors | scheduled payment near close | payment received | 55 prior |

## Finalists

| Candidate | Score | Advance? | Reason |
|---|---:|---|---|
| Factor-confirmed KSeF funding release | 88.8 | Yes | Stronger than Round 297 because the outside finance provider has already identified the funding blocker and can release cash when the exact evidence condition is met. |
| KSeF factoring broker white-label desk | 86 | No | Good channel, but too broad unless tied to factor-confirmed held funding files. |
| KSeF reserve-only release | 85 | No | Strong cash event but too narrow alone; included as one accepted subcase of the selected candidate. |
| Customer-acknowledged true-up release | 84 prior | No | High-water mark for SaaS AR branch but still failed the gate and lacks KSeF/factor-specific external evidence conditions. |
| Freight detention credit recovery | 78 internal | No | Freight-audit incumbents and ordinary credit disputes cap the idea. |

## Selected Candidate

**Factor-Confirmed KSeF Funding Release Desk**

## Internal Simulated Score

Simulated score: **88.8 / 100**

## Internal Rationale

This is the tightest viable KSeF/payment candidate after Round 297's fresh failure because it changes three things:

- The outside counterparty is a factor or receivables-finance provider, not only a buyer AP team.
- The accepted case starts from a written funding, eligibility, debtor-confirmation, or reserve-release hold condition, not a supplier's belief that KSeF is the problem.
- The proof is cash funding, reserve release, eligibility restored, debtor confirmation accepted by the factor, or clean no-go with the factor's reason code.

Why it clears internal simulation:

- The cash path is near-term and objective: advance, reserve, eligibility, or no-go.
- Factoring brokers and receivables-finance providers are plausible channels because they see the hold before accountants or ERP vendors solve it and may not want to staff KSeF/AP exception work.
- The founder can reject broad KSeF support, tax correction, debt collection, ERP implementation, and buyer AP chasing.
- The case memory is narrower and more durable than general KSeF transition support: factor-specific receivable eligibility rules, debtor-confirmation wording, KSeF/UPO/access proof, correction no-go causes, and funding-release evidence.

## Internal Risk Caps

- Would fall below 82 if accepted cases do not begin with written factor/funding-provider hold conditions.
- Would fall below 85 if it becomes generic KSeF support, supplier AP chasing, factoring brokerage, tax/accounting advice, ERP troubleshooting, debt collection, or old unpaid-invoice work.
- Would fall below 87 if factoring brokers and factors simply internalize the workflow or if clean KSeF-only funding blockers are rare after the transition wave.
- It remains capped below 90 because factors, factoring brokers, accountants, KSeF vendors, and ERP integrators are close to the workflow and can copy a broad checklist.

## Real Validation Rationale

This is worth one real validation despite KSeF fatigue because it directly implements the fresh evaluator's suggested stronger form: factor/funding-release cases. If this narrower funding-only version fails below the real gate, the KSeF branch should be considered exhausted unless actual paid factor-routed cases already exist.
