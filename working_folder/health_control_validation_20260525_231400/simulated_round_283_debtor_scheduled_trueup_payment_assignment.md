# Simulated Round 283 - Debtor-Scheduled True-Up Payment Assignment

Date: 2026-05-30 Europe/Warsaw

## Gate Context

- Simulation gate: validate only if simulated score is strictly `>87`.
- Real Zero To One gate after user update: working chat `>=85` and fresh chat `>=85`.
- Round 280 scored `84` because an acknowledged true-up plus payment-direction file was still close to ordinary AR/procurement follow-up.
- Round 281 failed because making the startup reseller/payee-of-record created legal, tax, credit, and payment-services risk.
- Round 282 failed because cash already in the vendor bank still looked like internal finance-ops cleanup.

Round 283 tests a narrower control point: the startup accepts only named enterprise true-up receivables where the debtor/customer has already signed or portal-confirmed the payment route and scheduled payment date before intake. The founder does not discover underbilling, argue entitlement, finance the receivable, serve as reseller, or collect disputed debt.

## Raw Hard-Control Candidate Table

| # | Candidate | Buyer | Acute trigger | Transferable control point inside 60 days | First proof | Main copy risk | Internal disposition |
|---:|---|---|---|---|---|---|---|
| 1 | Debtor-scheduled true-up payment assignment | B2B SaaS/API/data vendors | Customer accepted a true-up and AP has scheduled payment, but vendor needs controlled release follow-through before quarter close | Vendor mandate, debtor/AP signed payment-direction or portal-approved pay-date record, named invoice/PO, no-dispute certificate, fee right | First scheduled payment arrives or written no-go before work expands | CFO/AR/RevOps/fractional finance | Selected |
| 2 | Signed PO payment-date release desk | B2B vendors | PO exists and invoice is approved but payment-cycle date is uncertain | Buyer portal pay-date screenshot and vendor CFO authority | Payment on named date | AR teams | Finalist, less tied to high-value true-up |
| 3 | Debtor-confirmed overage installment release | SaaS/API vendors | Accepted overage is split into installments | Debtor payment-plan acknowledgement | First installment paid | Collections teams | Capped, debt-plan adjacency |
| 4 | Enterprise AP approved-for-payment batch monitor | PE-backed vendors | Multiple invoices approved but not paid | AP portal approved-for-payment list | Batch paid | BPO/AR tools | Too generic |
| 5 | Scheduled supplier rebate cash-in | Distributors | Manufacturer has approved rebate payment date | Vendor portal payment-date confirmation | Rebate cash received | Channel ops | Capped by failed rebate branch |
| 6 | Cloud marketplace customer-accepted private-offer pay-date | SaaS vendors | Customer accepted private offer but payout timing uncertain | Marketplace support case and payment statement | Payout | Marketplace consultants | Failed platform branch |
| 7 | Debtor-signed short-pay cure | Exporters | Customer admits short-pay and schedules balance | Debtor pay-date email and invoice map | Balance paid | AR/accountants | Too broad |
| 8 | Approved milestone payment release | Services vendors | Customer accepted milestone, payment scheduled | Acceptance certificate and AP date | Payment | Project managers | Service dispute risk |
| 9 | Buyer-accepted license expansion true-up | SaaS vendors | Customer admits extra users/modules, payment scheduled | Order form/AP confirmation | Payment | CS/RevOps | Strong subcase |
| 10 | Debtor-confirmed annual minimum-commit shortfall | SaaS/data vendors | Annual commit shortfall accepted and scheduled | Signed true-up statement/payment date | Payment | CFO/AR | Finalist |
| 11 | Scheduled data-usage true-up pay-date | Data vendors | Customer accepted measured usage fee | Usage statement and AP date | Payment | Billing teams | Finalist |
| 12 | Approved invoice awaiting vendor-master switch | SaaS vendors | Debtor approved invoice but new bank/payee validation blocks payment | Debtor AP bank validation confirmation | Payment | AP/vendor-master tools | Capped as ordinary admin |
| 13 | Debtor-signed renewal co-term adjustment | SaaS vendors | Co-term math accepted, payment date scheduled | Amendment/AP date | Payment | Renewals teams | Capped |
| 14 | Acquired-company payment redirection after customer consent | B2B acquirers | Customer must redirect current invoice to buyer | Customer consent/pay-date record | Cash collected | M&A integration | Legal/tax complexity |
| 15 | Customer-confirmed AI/API inference true-up | AI vendors | Token/inference statement accepted and scheduled | Usage acceptance/AP date | Payment | RevOps | Sensitive logs; finalist but narrower market |
| 16 | Enterprise partner pass-through accepted true-up | ISVs/channel partners | End customer and partner accepted delta | Triparty payment date | Payment | Partner ops | Attribution messy |
| 17 | Debtor-scheduled support-renewal uplift | Software vendors | Uplift accepted by customer, date set | AP date/order form | Payment | Renewal teams | Ordinary |
| 18 | Approved audit adjustment payment release | Vendors | Customer audit accepted adjustment | settlement/pay-date | Payment | Legal/audit firms | Legal-adjacent |
| 19 | Accepted payment plan first-date monitor | B2B vendors | Customer accepted arrears plan | Payment-plan doc | First payment | Collections | Debt collection-adjacent |
| 20 | Debtor-scheduled foreign-entity correction | Multinationals | Wrong legal entity fixed and AP date set | correction invoice/AP date | Payment | Controllers | Ordinary finance |
| 21 | Scheduled customer credit offset release | SaaS vendors | Credit and net amount accepted | netting letter/pay-date | Net invoice paid | AR teams | Capped by credit branch |
| 22 | Debtor-approved no-PO invoice exception | Vendors | AP agrees one-off pay without PO | exception approval | Payment | AR/internal | Low defensibility |
| 23 | Buyer-portal approved payment evidence harvest | Vendors | Vendor cannot prove payment scheduled to board/lender | portal record | Internal release | Report-like | Reject |
| 24 | Debtor-signed AP unblock sprint | B2B vendors | AP asks for one missing file before scheduled pay | AP checklist/pay-date | Payment | AR teams | Generic |
| 25 | Scheduled holdback release after SaaS go-live | SaaS vendors | Go-live signed and holdback pay-date set | acceptance/pay-date | Payment | Implementation PMs | Service dispute risk |
| 26 | Debtor-scheduled overage for data clean-room vendors | Data vendors | Usage/seat overage accepted | usage statement/pay-date | Payment | RevOps | Niche finalist |
| 27 | Approved payment with bank-detail revalidation | Vendors | AP confirms amount but bank validation pending | AP validation/pay-date | Payment | VOP/AP tools | Ordinary |
| 28 | Debtor-signed disputed-to-undisputed conversion | Vendors | Dispute resolved and payment date agreed | settlement/pay-date | Payment | lawyers/collections | Too legal |
| 29 | Debtor-scheduled true-up insurance for board close | SaaS vendors | Board/covenant close needs cash by date | pay-date record and CFO mandate | Payment | Finance teams | Same as lead |
| 30 | Debtor-scheduled annual data minimum catch-up | Data/API vendors | Minimum take-or-pay catch-up accepted | customer/AP date | Payment | CFO/AR | Strong subcase |
| 31 | Scheduled enterprise invoice release through outsourced AR partner | AR firms | Partner has paid cases but not enough specialist capacity | partner routing and debtor dates | Payment | partner internalization | Channel but weaker control |
| 32 | Debtor-confirmed usage true-up clean no-go desk | Vendors | Customer accepts amount but payment blockers found | no-go classification | Paid no-go fee | AR teams | Useful boundary, not lead |

## Finalists

| Candidate | Control strength | Speed to cash | Copy resistance before control | Reason not selected |
|---|---:|---:|---:|---|
| Debtor-scheduled true-up payment assignment | 9 | 9 | 6 | Best fit: debtor-side scheduled payment evidence before intake, high value, no platform discretion. |
| Debtor-confirmed annual minimum-commit shortfall | 8 | 8 | 5 | Good, but can feel like collections unless payment date is already scheduled. |
| Scheduled data-usage true-up pay-date | 8 | 8 | 5 | Strong but narrower than all SaaS/API/data accepted true-ups. |
| Signed PO payment-date release desk | 7 | 8 | 4 | Too close to generic approved-invoice follow-up. |
| Customer-confirmed AI/API inference true-up | 8 | 8 | 5 | Timely but sensitive usage logs and AI-specific disputes cap score. |
| Debtor-scheduled overage for data clean-room vendors | 8 | 8 | 5 | Interesting but too small as first wedge. |

## Selected Candidate

**Idea name:** Debtor-Scheduled True-Up Payment Assignment

### Thesis

For B2B SaaS, API, data, and infrastructure vendors, the highest-quality true-up recovery cases are not disputed underbilling cases. They are already accepted true-ups where the enterprise customer or AP/procurement team has signed a payment-direction acknowledgement, approved a portal payment date, or issued a written scheduled-payment confirmation, but the vendor needs a bounded third-party release operator to maintain the file, keep evidence clean, and convert the scheduled payment into cash before quarter close, covenant reporting, acquisition diligence, or board review.

### Control Table

| Field | Forced answer |
|---|---|
| Buyer | 20-500 employee B2B SaaS/API/data/infrastructure vendors with enterprise customers and accepted usage, seat, data-volume, minimum-commit, co-term, or renewal true-up receivables above 150,000 PLN equivalent. |
| Acute trigger | Cash is scheduled and externally acknowledged, but still commercially critical: quarter close, board reporting, lender covenant, acquisition diligence, renewal expansion, or runway pressure depends on receiving one or more named payments on time. |
| Transferable control point | Vendor mandate over named receivable; debtor/AP signed payment-direction acknowledgement or buyer-portal approved-for-payment record with scheduled date; invoice/order form/true-up statement; no-dispute certificate; customer contact path through vendor-approved billing owner; fee right tied to scheduled payment received or documented clean no-go. |
| Signed/titled/assigned/prepaid within 60 days | Three mandates covering 1.5M+ PLN in debtor-scheduled accepted true-ups; each with debtor-side written pay-date or portal approved-for-payment evidence; first 500,000+ PLN cash received or cleanly no-goed; 35,000+ PLN collected in setup/success/no-go fees. |
| First acquisition mechanism | Warm outbound to billing-migration partners, usage-pricing consultants, RevOps firms, fractional SaaS CFOs, SaaS accountants, PE/VC portfolio operators, and enterprise billing implementation partners asking only for "accepted true-ups with customer/AP scheduled payment already in writing." |
| Gross margin and payback logic | 8,000-25,000 PLN fixed setup/no-go fee per named payment file plus 1.5-5% success fee when cash arrives by the scheduled date or after documented AP release action. Contractor cost is secure evidence handling and finance-ops review, not litigation or collections. |
| Copy risk | Internal CFO/AR/RevOps teams, billing migration partners, fractional CFOs, ERP/billing consultants, outsourced AR providers. |
| Why incumbents cannot copy before control | The startup only claims transaction-level control after the vendor signs the mandate and the debtor-side pay-date/payment-direction evidence is already captured in the file. Incumbents can copy the method later, but they cannot retroactively control that named receivable, evidence room, fee right, scheduled-payment trail, and no-go boundary once the file is assigned. |
| Why it is not a service/report/app/dashboard/marketplace/broker | It does not analyze underbilling, sell software, broker buyers, chase old debt, or write a report. It accepts only named debtor-scheduled payment files and produces cash received by the vendor, a dated debtor no-go, or a clean rejection before work expands. |

### Internal Simulation

**Simulated score: 88.1 / 100**

Reasons this clears simulation:

- It tightens the strongest near-pass from Round 280 by requiring debtor-side scheduled-payment evidence before intake.
- It avoids platform discretion, reseller/payee-of-record risk, and generic cash-application cleanup.
- It creates first proof within 60 days: scheduled cash received, fee collected, or clean debtor-side no-go.
- It has high willingness to pay when named cash matters for close, runway, covenant, diligence, or board reporting.
- It is disciplined enough for a part-time founder because it rejects disputed usage, legal collection, old debt, and unclear AP blockers.

Reasons the score stops at 88.1:

- Clean debtor-scheduled cases may be rare.
- Competent CFOs and AR teams should already manage many approved payment files.
- Partners can internalize the workflow after seeing it.
- Success-fee attribution can still be contested unless the baseline scheduled-payment record and startup action log are precise.
- Sensitive contracts, invoices, AP records, customer threads, and usage statements create trust friction.

## Internal Gate Decision

Advance to working-chat validation because the simulated score is strictly `>87` and the control point is materially stronger than prior receivable-release variants: debtor-side scheduled payment evidence is mandatory before the startup accepts the file.
