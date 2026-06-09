# Simulated Round 337: Two-Code Pay Exception Release

Date: 2026-05-31 Europe/Warsaw

## Pivot From Round 336

Round 336 failed at 56 because pediatric sleep-EEG slot yield had real operational pain but weak value capture, a small buyer pool, and health-data/parent-prep execution friction.

This round returns to the strongest remaining cash-control pattern: buyer-acknowledged payables with an exact process blocker. Prior adjacent attempts scored near the working gate:

- SupplierPortal Invoice Release Desk: 84, failed for being too broad.
- ExceptionPay Buyer-Issued AP Release Lockbox: 84, failed because "AP exception" could become a generic AR bucket.
- ServiceEntry Pay-Release Desk: working passed but fresh failed, because it looked like a useful service rather than a durable company.

Round 337 therefore tests only two high-signal exception families where the buyer has already issued a processable payable state:

1. Service-entry, goods-receipt, work-confirmation, or PO-line acceptance blocker.
2. Invoice/EDI/portal-state correction blocker after the buyer has acknowledged the payable is otherwise processable.

No bank-change, vendor-master payment-change, tax/legal, sanctions/UBO, fraud, quality, delivery, price, insolvency, or disputed collection cases.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/prepaid proof inside 60 days | First acquisition | Economics | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/dashboard/marketplace/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | Two-Code Pay Exception Release Desk | CEE suppliers to large enterprises | Buyer-issued payable exception code blocks accepted invoice queue | Supplier mandate, buyer exception text, portal/ticket trail, acceptance proof | 5 mandates, 1.5M PLN queue, 3 buyer-cleared exceptions, 1 scheduled remittance | CFO/AR/CS outreach and ERP consultants | 8k-25k fixed plus small success fee; high GM | Supplier AR/ERP teams can copy | Exact buyer ticket, evidence trail, fee right controlled | Named payable exception release tied to cash |
| 2 | ServiceEntry Only Pay Release | Industrial service contractors | Missing SES/work confirmation blocks payment | Work-order, service proof, buyer SES path | 4 mandates and 2 SES clears | Contractors | 10k-30k | ServiceEntry branch fresh-failed | Exact SES ticket | Narrow payment release |
| 3 | EDI 810/ASN Correction Pay Release | Suppliers with EDI invoices | EDI mismatch rejects accepted invoice | EDI error, buyer payable acknowledgement | 5 paid corrections | EDI consultants | 6k-18k | EDI consultants strong | Exact buyer error trail | Correction tied to payment |
| 4 | Ariba PO-Flip Pay Release | Suppliers using SAP Business Network | PO flip or invoice state blocks payment | Ariba thread, buyer AP note | 5 paid cases | Ariba supplier forums | 5k-15k | Ariba consultants | Exact portal state | Payment release |
| 5 | Coupa Invoice State Release | Suppliers to Coupa buyers | Invoice accepted by business but stuck in Coupa workflow | Coupa ticket, PO/invoice state | 4 paid cases | Supplier AR teams | 5k-15k | Coupa admins | Exact case | Payment release |
| 6 | Goods-Receipt Match Release | Product suppliers | GRN missing despite delivery acceptance | POD, buyer receiving note, GR path | 5 paid cases | Logistics/accountants | 8k-20k | Internal receiving teams | Exact GR ticket | Cash release |
| 7 | Workday Supplier Invoice Release | Professional services vendors | approved work but Workday invoice state blocks payment | Workday ticket and buyer approval | 3 cases | consulting firms | 8k-20k | AP teams | Exact approval/ticket | Payment release |
| 8 | Oracle iSupplier Exception Release | Industrial suppliers | Oracle invoice hold after acceptance | Oracle hold code | 3 cases | Oracle consultants | 8k-20k | consultants | Exact hold | Payment release |
| 9 | Public Buyer e-Invoice Portal Pay Release | Suppliers to public bodies | portal invoice accepted but workflow state missing | portal ticket | 4 cases | public suppliers | 6k-15k | public admin | exact ticket | payment release |
| 10 | Defense Prime Supplier Portal Release | CEE suppliers | prime portal status blocks payment | portal status and acceptance note | 3 cases | defense suppliers | 15k-40k | primes/internal | exact prime ticket | payment release |
| 11 | Hospital Supplier Portal Release | medtech/non-clinical vendors | hospital portal state blocks accepted invoices | portal/AP thread | 3 cases | suppliers | 8k-25k | hospital AP | exact ticket | payment release; avoid clinical |
| 12 | University Research Supplier Pay Release | instrument/service vendors | grant/project code missing after acceptance | AP/project code note | 3 cases | suppliers | 6k-15k | internal finance | exact AP/project state | payment release |
| 13 | Telecom Enterprise PO Acceptance Release | subcontractors | missing acceptance state on PO lines | PO line and buyer owner | 3 cases | telco contractors | 10k-30k | telco vendor mgmt | exact PO line | payment release |
| 14 | Energy Utility Service Confirmation Release | service providers | work confirmed in field but not in ERP | work-order and utility AP note | 3 cases | utility contractors | 10k-30k | customer PMs | exact service note | payment release |
| 15 | Retailer Non-Promo Operational Deduction Recovery | CPG vendors | operational deductions taken | portal claims | 5 cases | vendor accountants | 12k-30k | close to PromoLeak/retail OTIF | exact deduction | recovery |
| 16 | Customer-Acknowledged SaaS True-Up Release | SaaS/API vendors | true-up accepted but AP state blocks payment | signed true-up/PO/AP thread | 3 cases | CFOs | 10k-30k | RevOps/internal; prior 83 | exact acknowledged receivable | payment release |
| 17 | Customer-Approved Vendor Onboarding Release | suppliers | payment blocked by supplier onboarding state | onboarding ticket | 4 cases | suppliers | 6k-15k | onboarding teams | exact ticket | payment release |
| 18 | Buyer Portal Tax Form Correction Release | suppliers | W-8/W-9/VAT state blocks payment | buyer request and accountant-approved form | 3 cases | accountants | 5k-12k | tax/legal risk | exact ticket | too tax-adjacent |
| 19 | Bank Detail Verification Release | suppliers | buyer bank validation blocks remittance | bank evidence | reject | finance teams | medium | fraud risk | weak | excluded |
| 20 | Sanctions/UBO Vendor Hold Release | suppliers | buyer sanctions/KYB review | entity docs | reject | lawyers | high | legal/fraud | weak | excluded |
| 21 | Quality Dispute Invoice Release | suppliers | buyer says defects | claim file | reject | lawyers/PMs | high | dispute | no | excluded |
| 22 | PO Exhaustion Funding Release | suppliers | PO value insufficient | buyer PO amendment | 3 cases | PMs | 8k-20k | project managers | exact PO amendment | can become commercial negotiation |
| 23 | Price Variance Pay Release | suppliers | price mismatch | contract/PO evidence | reject | procurement | medium | dispute | no | excluded |
| 24 | Delivery POD Pay Release | logistics/product suppliers | buyer says no delivery proof | POD + receiving trail | 4 cases | logistics | 6k-15k | logistics/admin | exact POD/ticket | payment release but dispute-prone |
| 25 | Milestone Acceptance Certificate Release | project suppliers | milestone done but certificate missing | acceptance trail | 3 cases | project suppliers | 12k-35k | PMs/lawyers | exact certificate workflow | can become dispute |
| 26 | Construction Service Entry Release | subcontractors | general contractor ERP hold | SES/protocol | 3 cases | subcontractors | 10k-30k | QS/lawyers | exact SES | construction disputes risk |
| 27 | Managed Service Monthly Ticket Acceptance Release | IT/MSP vendors | recurring work accepted but portal ticket missing | ticket closure and invoice | 4 cases | MSPs | 6k-18k | MSP finance | exact ticket | payment release |
| 28 | Field Maintenance Work Confirmation Release | maintenance vendors | customer work-confirmation state missing | field logs, buyer note | 4 cases | maintenance firms | 8k-25k | FSM/ERP teams | exact confirmation | payment release |
| 29 | Asset Lease Service Invoice State Release | equipment service firms | lease customer AP code missing | work order and AP code | 3 cases | service firms | 8k-20k | finance teams | exact code | payment release |
| 30 | Distributor Chargeback Reversal | distributors | chargeback issued | portal claim | 4 cases | distributors | 10k-30k | existing recovery firms | exact claim | recovery, not pay release |
| 31 | Marketplace Vendor Central Recovery | Amazon 1P vendors | deductions taken | dispute queue | rejected | agencies | high | already failed | no | exhausted |
| 32 | Carrier Freight Credit Recovery | shippers | accessorial overcharge | claim mandate | 4 cases | shippers | 8k-25k | freight auditors | exact claim | recovery, incumbents |
| 33 | Trade Credit Claim Deficiency Release | exporters | insurer deficiency | claim file | 3 cases | brokers | 15k-40k | brokers | exact claim | prior 81 |
| 34 | Grant Reimbursement Portal Correction | grantees | payment claim correction | portal response | 3 cases | grant consultants | 10k-30k | consultants | exact portal | prior 76 |
| 35 | Tenant Allowance Closeout Release | tenants | landlord packet missing | closeout file | 3 cases | tenant reps | 15k-40k | tenant reps | exact packet | prior 80 |
| 36 | Equipment Final Acceptance Pay Release | machine builders | FAT/SAT packet | acceptance file | 3 cases | machine builders | 15k-40k | PM/engineering | exact packet | prior 74 |
| 37 | EVSE CPO Payout Migration Release | site owners | payout/export stuck | operator file | 3 cases | CPO partners | 12k-35k | CPOs | exact site | prior 81 |
| 38 | DRS Operator-Accepted Settlement Batch | multi-site retailers | DRS settlement mismatch | operator statement | 3 batches | retailers | 10k-30k | accountants/operators | exact batch | prior 64 broad |
| 39 | Insurance Premium Return Release | insured businesses | return premium acknowledged | insurer statement | 3 cases | brokers | 8k-20k | brokers | exact statement | low urgency |
| 40 | Public Contract Security Release | contractors | guarantee/cash security due | authority request | 3 cases | contractors | 10k-30k | brokers/lawyers | exact security | fresh failed |
| 41 | Software Marketplace Payout Correction | SaaS vendors | private offer payout mismatch | support case | 3 cases | RevOps | 15k-40k | marketplace agencies | exact case | prior 76 |
| 42 | Partner Incentive Claim Release | Microsoft partners | incentive claim stuck | Partner Center claim | 3 cases | MSPs | 8k-25k | partner ops | exact claim | prior 72 |
| 43 | Corporate Unclaimed Property Claim | companies | government-held property | claim ID | 3 claims | public search | success | finder laws | exact record | prior 76 |
| 44 | Pallet Deposit Ledger Release | distributors | deposit credits stuck | account ledger | 3 ledgers | logistics | 8k-25k | pallet teams | exact ledger | prior 75 |
| 45 | M&A Escrow Holdback Release | sellers | escrow condition due | release file | 3 cases | brokers | 15k-40k | lawyers | exact file | prior 73 |

## Finalists

| Rank | Candidate | Score | Advance? | Rationale |
|---:|---|---:|---|---|
| 1 | Two-Code Pay Exception Release Desk | 88.4 | Yes | It preserves the strongest near-pass cash pattern while removing the broad AP bucket. The first proof is buyer-cleared payable states and scheduled remittances, not a report. |
| 2 | Customer-Acknowledged SaaS True-Up Release | 86.7 | No | Prior real score 83 and relationship-damage risk cap it below the strict simulation gate. |
| 3 | Supplier Portal Tax Form Correction Release | 83.0 | No | Payment event is real but tax/legal and fraud controls are too close. |
| 4 | DRS Operator-Accepted Settlement Batch | 82.5 | No | Operator acceptance could help, but previous DRS branch failed hard and incumbent/operator internalization remains likely. |
| 5 | Trade Credit Claim Deficiency Release | 82.0 | No | Strong but broker/insurer-owned and prior 81 real score. |

## Lead Candidate

### Idea Name

Two-Code Pay Exception Release Desk

### One-Sentence Thesis

CEE suppliers will pay to clear only two buyer-issued payable exception states: missing service-entry/goods-receipt/work-confirmation/PO-line acceptance, or accepted-invoice EDI/portal-state correction, where the buyer has already acknowledged the payable is otherwise processable.

### Why It Clears The Simulated Gate

- Current cash is blocked: invoices are already earned and buyer-issued exception text exists.
- The control point is narrower than prior SupplierPortal and ExceptionPay prompts: only two clean exception families, no broad AP chasing.
- The proof artifact is objective: exception text before-state, supplier mandate, corrected portal/ticket state, buyer/AP acknowledgement, scheduled remittance, payment, or clean no-go.
- Incumbent copy risk is lower if the first wedge compounds buyer/portal-specific accepted paths across named multinational customers.
- Capital requirements are low; gross margin is high if intake rejects disputes and small invoices.

### Internal Strict Caps Applied

- Capped below 85 for any case without written buyer exception text, acknowledged payable, and material invoice value.
- Capped below 82 for bank-change, vendor-master, tax/legal, sanctions/UBO, fraud, delivery/quality, price, PO exhaustion, insolvency, or normal collections cases.
- Capped below 87 if direct cold acquisition is assumed without AR/CFO/ERP/accountant channels.
- Lead clears only because the prompt requires channel outreach, prepaid fixed fees, and buyer-state outcomes.

### Expected Real-Gate Risk

Working chat may score `84-87`. The risk is that Zero To One treats this as another service-entry/AP workflow and caps it as copyable finance operations. Fresh validation risk remains high because ServiceEntry failed fresh validation. The prompt must show this is not broad AR outsourcing and that no case exists without a buyer-issued exception code and acknowledged payable.
