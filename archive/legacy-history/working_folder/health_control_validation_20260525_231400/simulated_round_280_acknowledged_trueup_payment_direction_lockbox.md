# Simulated Round 280: Acknowledged True-Up Payment-Direction Lockbox

Date: 2026-05-30 Europe/Warsaw

Real browser gate: working Zero To One `>=85`, fresh Zero To One `>=85`.

## Search Frame

Recent recovery mandates failed when the target cash was disputed, platform-controlled, internally recoverable by normal AP/AR teams, or tied to ambiguous operations. Round 275 came closest at `83/100` by accepting only customer-acknowledged SaaS/API true-up receivables, but the evaluator still treated the remaining work as ordinary AR/procurement follow-up.

This round tests whether the control point becomes strong enough when the startup accepts only cases with external customer acknowledgement plus signed payment-direction / AP release authority before material work begins. The proof is not a report and not an underbilling analysis. It is a named customer payment released against a signed true-up, PO, invoice, or AP acknowledgement.

## Raw Candidate Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day proof | First acquisition | Economics | Copy risk | Why incumbents cannot copy before control is secured | Initial cap |
|---:|---|---|---|---|---|---|---|---|---|---:|
| 1 | Acknowledged SaaS true-up payment-direction lockbox | B2B SaaS/API/data vendors | customer accepted true-up but AP/procurement payment is stuck | vendor mandate, customer AP acknowledgement, signed payment-direction or release file, invoice/PO thread | 3 mandates, 1 payment released | CFO/RevOps/billing migration partners | setup + 3-8% success | AR/RevOps/fractional CFOs | exact external acknowledgement, release file, and fee right are controlled | 88.4 |
| 2 | Customer-approved minimum-commit shortfall collection | SaaS vendors | annual commit shortfall accepted | amendment/order form/payment direction | 2 paid cases | CFOs | success fee | AR teams | exact accepted shortfall | 85.0 |
| 3 | SaaS vendor-master blocker cure | SaaS vendors | enterprise cannot pay because vendor profile/PO/entity mismatch | AP ticket and vendor-master evidence | one AP payment | controllers | fixed fee | AP internal | weak, ordinary admin | 78 |
| 4 | Contracted data-feed true-up release | data vendors | customer accepted usage data but PO blocked | data statement and AP acknowledgement | one payment | data CFOs | success | billing teams | exact customer thread | 86 |
| 5 | Annual software-support co-term invoice release | software vendors | renewal true-up accepted but PO not issued | renewal quote, AP/procurement thread | one payment | resellers | fee | partner ops | too ordinary renewal ops | 77 |
| 6 | Customer-approved service-credit netting release | SaaS vendors | credits agreed, net invoice stuck | netting statement | one paid invoice | CFOs | fee | AR teams | messy customer relationship | 75 |
| 7 | Enterprise marketplace private-offer AP release | SaaS vendors | customer accepted private offer but marketplace payout stuck | marketplace order, AP ticket | one payment | marketplace ops | success | cloud marketplaces | platform incumbents | 72 |
| 8 | Annual API overage PO release | API vendors | overage statement accepted, PO missing | PO request, usage statement | one payment | API CFOs | 3-8% | billing ops | exact case | 84 |
| 9 | Customer-signed invoice split/entity correction | SaaS vendors | invoice to wrong entity, buyer accepts correction | AP ticket | one payment | controllers | fixed fee | ordinary AR | not hard enough | 76 |
| 10 | Usage-priced embedded-finance fee release | fintech infra vendors | bank/customer accepts fees but risk/procurement holds PO | AP and legal approval | one payment | fintech CFOs | success | finance ops | regulated/trust-heavy | 72 |
| 11 | Cloud consumption resale underbilling release | MSPs/resellers | customer accepted cloud usage true-up | billing exports and AP acknowledgement | one payment | MSP CFOs | success | MSP FinOps | FinOps incumbents | 79 |
| 12 | Ad-tech data-volume true-up release | adtech vendors | buyer accepted log volume fee | signed usage statement | one payment | adtech ops | success | RevOps | customer trust risk | 80 |
| 13 | Wholesale telecom CDR true-up release | small telcos | partner accepted CDR reconciliation | CDR statement and payment direction | one payment | telco finance | success | telco specialists | too specialized | 80 |
| 14 | IoT fleet subscription true-up release | IoT vendors | device count overage accepted | device register and AP ticket | one payment | IoT CFOs | success | AR teams | logs may be weak | 80 |
| 15 | Seat-expansion true-up release | SaaS vendors | customer admits users exceeded seats | seat export and PO | payment | RevOps | success | customer success | relationship blowback | 78 |
| 16 | Enterprise data-room access-fee release | data vendors | paid access accepted, procurement stuck | order form and AP | payment | CFOs | fee | AR | too generic | 75 |
| 17 | License audit settlement release | software vendors | customer settled license audit, payment delayed | settlement and invoice | payment | vendor finance | success | legal/license-audit firms | legal-adjacent | 70 |
| 18 | SaaS reseller pass-through true-up release | resellers | end customer approved, vendor invoice stuck | reseller/end-customer docs | payment | resellers | fee | resellers internal | margin thin | 74 |
| 19 | Data vendor bank-detail revalidation release | data vendors | AP blocked by payee mismatch | AP ticket | payment | AR teams | fixed | VOP/AP tools | ordinary admin | 72 |
| 20 | Enterprise proof-of-delivery AR release | B2B suppliers | customer accepts delivery, PO/GRN missing | GRN/AP ticket | payment | CFOs | fee | AP/AR teams | generic | 68 |
| 21 | Milestone SaaS implementation payment release | SaaS vendors | customer accepted milestone, invoice stuck | acceptance certificate | payment | implementation leads | success | PM/AR teams | service dispute risk | 74 |
| 22 | Enterprise API SLA penalty netting release | API vendors | net amount agreed, payment stuck | AP/netting memo | payment | CFOs | fee | legal/AR | too legal | 70 |
| 23 | Partner-sold SaaS true-up payment release | ISV partners | partner/customer accepted true-up | triparty acknowledgement | payment | partners | fee | partner ops | messy attribution | 78 |
| 24 | Annual data-indexing excess-fee release | data/search vendors | customer accepted index volume fee | usage statement | payment | RevOps | success | billing teams | narrow subset | 82 |
| 25 | API invoice tax/VAT correction release | SaaS vendors | AP agrees corrected invoice needed | corrected invoice | payment | accountants | fixed | tax/accounting | tax advice risk | 70 |
| 26 | Customer-signed renewal uplift release | SaaS vendors | uplift accepted, PO delayed | renewal agreement and AP thread | payment | customer success | success | ordinary CS | not enough | 76 |
| 27 | Debtor-confirmed service-bureau overage release | payroll/HR SaaS | customer accepted employees/transactions true-up | customer statement | payment | CFOs | fee | HR/payroll ops | sensitive data | 77 |
| 28 | Enterprise AI inference true-up release | AI API vendors | buyer accepted token/inference statement | usage logs and AP acknowledgement | payment | AI vendors | success | billing tools | logs/relationship risk | 82 |
| 29 | Payment-direction addendum for clean receivables | B2B SaaS | debtor agrees to pay named invoice by date | signed addendum | payment | CFOs | success | AR teams | exact debtor signoff | 84 |
| 30 | Accepted audit-adjustment invoice release | SaaS/data vendors | customer audit accepted true-up | audit file and invoice | payment | CFOs | fee | audit/legal | too close to audit settlements | 73 |
| 31 | Customer-approved arrears payment plan setup | SaaS vendors | customer accepted arrears but needs plan | payment plan | first installment | CFOs | fee | collections | debt collection-adjacent | 65 |
| 32 | Channel-customer co-sell receivable release | SaaS vendor/channel | buyer accepted co-sell invoice | customer/channel/AP acknowledgement | payment | channels | fee | partner ops | attribution disputes | 73 |

## Finalists And Strict Simulated Scores

| Rank | Idea | Simulated score | Advance? | Reason |
|---:|---|---:|---|---|
| 1 | Acknowledged True-Up Payment-Direction Lockbox | 88.4 | Yes | Strengthens the Round 275 near-pass by requiring an external customer/AP acknowledgement and payment-direction/release file before work; first proof is payment movement, not analysis. |
| 2 | Contracted Data-Feed True-Up Release | 86.0 | No | Cleaner than generic SaaS, but still a subset and below simulation gate. |
| 3 | Customer-Approved Minimum-Commit Shortfall Collection | 85.0 | No | Too close to ordinary AR unless bundled into lead. |
| 4 | API Overage PO Release | 84.0 | No | Good but not clearly stronger than Round 275. |
| 5 | Enterprise AI Inference True-Up Release | 82.0 | No | Timely but sensitive logs and disputed metrics cap it. |
| 6 | Data-Indexing Excess-Fee Release | 82.0 | No | Narrow but not strong enough. |

## Lead Candidate

### Acknowledged True-Up Payment-Direction Lockbox

Internal simulated score: **88.4 / 100**

### Why It Clears Simulation

- It uses the strongest recent near-pass but adds a harder external control point: customer/AP acknowledgement and payment-direction or release authority tied to a named invoice before the startup spends real time.
- It excludes surprise underbilling, disputed usage, license audits, old debt, and ambiguous contract interpretation.
- The buyer's proof is not a memo. The proof is released cash, a paid invoice, or a debtor-confirmed payment date against an accepted true-up.
- Payment direction / AP release file creates a better attribution trail than ordinary AR cleanup.
- Capital needs are low; the first POC can be manual with secure evidence handling and fixed no-go rules.

### Internal Objections

- Competent CFO, AR, RevOps, customer-success, and billing-platform teams should often handle this internally.
- Enterprise AP blockers may be ordinary vendor-master, PO, tax, budget, legal-entity, or procurement admin.
- Customer acknowledgement may not equal willingness to prioritize cash payment.
- Success-fee attribution may still be disputed if the receivable would have paid anyway.
- Cold acquisition is difficult; the likely channel is billing migration partners, usage-billing consultants, fractional CFOs, and RevOps operators, who can internalize.
- It only deserves the score if the prompt is disciplined: no disputed usage, no relationship-damaging backbilling, no legal collection, no generic RevOps consulting.

### Gate Decision

Advance to working Zero To One validation. This is materially different from Round 275 because the control point is not just an acknowledged true-up receivable; it is a debtor/customer AP release file plus payment-direction or payment-date acknowledgement that creates externally evidenced cash movement.
