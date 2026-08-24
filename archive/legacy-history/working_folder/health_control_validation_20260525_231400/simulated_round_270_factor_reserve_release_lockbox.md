# Simulated Round 270: FactorReserve Settled-Debtor Holdback Release Lockbox

Date: 2026-05-30 Europe/Warsaw

Real browser gates for this search: working Zero To One `>=85`, fresh Zero To One `>=85`.

## Search Frame

Round 269 failed because the buyer would have to confront its own customers to recover underbilled usage revenue. Round 270 returns to a cleaner cash-control pattern: money already collected by a third-party finance provider, where the buyer is asking for release of its own matured reserve or holdback balance rather than billing a commercial customer.

The candidate is deliberately narrow. It rejects disputed factoring debt, legal collection, factoring advances, PSP reserves, insolvency claims, and any file where the factor has not already collected the underlying debtor payments or issued a usable reserve/settlement ledger.

## Raw Candidate Control Table

| # | Raw candidate | Buyer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | First acquisition mechanism | Economics | Copy risk | Why not service/report/app/broker |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | Settled factoring reserve release | SMEs using factoring | Factor collected debtor payments but reserve/holdback remains unreleased | Signed mandate, factor ledger, debtor-payment evidence, release request | 3 mandates, 2 factor acknowledgements, 1 release | Factoring brokers/accountants | 5k-12k setup + 8-15% of released cash | Factors/brokers/accountants | Controls named cash release file |
| 2 | Invoice-discounting blocked-account release | SMEs with invoice discounting | Blocked account balance not swept back | Bank/factor statements and sweep proof | Mandate, sweep request, bank acknowledgement | CFO/accountant channels | Success fee | Banks/accountants | Cash movement |
| 3 | Factoring over-reserve true-up | Exporters/transport firms | Reserve percentage kept after old invoices cleared | Reserve schedule and debtor ledger | Mandate, factor correction | Factoring brokers | Medium | Factors | Cash release |
| 4 | Recourse-window expiry release | SMEs | Recourse period expired but holdback not freed | Contract window, debtor payment, no dispute notice | Mandate, expiry proof, release | Accountants | Medium | Brokers | Cash release |
| 5 | Factoring settlement statement cleanup | SMEs | Final settlement shows unexplained deductions | Factor statement line challenge | Mandate, itemized correction | Accountants | Medium | Accountants | Specific credit memo |
| 6 | Supplier-finance early-pay fee reversal | Suppliers | Dynamic-discount fee charged despite wrong terms | Portal and remittance evidence | Mandate, buyer/funder correction | AR teams | Medium | Treasury vendors | Cash credit |
| 7 | Trade-credit insurer premium true-up | Exporters | Exposure lower than declared | Policy exposure ledger | Mandate, insurer credit | Brokers | Medium | Brokers | Cash credit, but insurance boundary |
| 8 | Leasing security deposit release | SMEs | Lease ended, deposit not returned | Lease ledger and closing statement | Mandate, lessor acknowledgement | Leasing brokers | Medium | Lessors/lawyers | Cash release |
| 9 | Equipment-finance overpayment refund | SMEs | Payoff quote/auto debit caused overpayment | Lessor ledger | Mandate, refund case | Accountants | Low-medium | Lessors | Cash refund |
| 10 | Merchant acquirer reserve release | Ecommerce merchants | Reserve matured after chargeback window | PSP ledger | Mandate, PSP case | Payment consultants | Medium | Payment consultants | Prior PSP failure |
| 11 | Marketplace payout hold release | Sellers | KYBC/KYC payout hold | Platform evidence | Mandate, payout case | Agencies | Medium | Agencies | Prior marketplace failure |
| 12 | Supplier rebate accrual release | Distributors | Earned rebate unpaid | Rebate agreement, sales ledger | Mandate, vendor acknowledgement | Channel accountants | Medium-high | Vendor teams | Prior failure |
| 13 | Distributor price-protection credit | Resellers | Vendor announces price drop, credit missed | Inventory snapshot, vendor policy | Mandate, credit memo | Distributor reps | Medium | Distributors | Cash credit |
| 14 | Deal-registration margin credit | IT resellers | Registered deal paid at wrong tier | Portal registration, invoice | Mandate, vendor correction | Channel partners | Medium | Vendor teams | Cash credit |
| 15 | MDF claim release | MSPs/VARs | Vendor-funded marketing claim unpaid | MDF approval and proof | Mandate, vendor claim | Distributor reps | Medium | Prior failure | Cash claim |
| 16 | Warranty labor credit release | Installers | OEM accepted RMA but labor credit missing | RMA, serial, return proof | Mandate, credit memo | Installer accountants | Medium | Prior failure | Cash credit |
| 17 | OTA virtual-card recovery | Hotels | OTA remittance mismatch | PMS/OTA statements | Mandate, claim | Revenue managers | Medium | Hotel consultants | Prior likely weak |
| 18 | Freight credit recovery | Importers | Carrier/forwarder credit due | BOL/invoice/claim | Mandate, credit | Freight auditors | Medium | Incumbents | Prior weak |
| 19 | Cloud marketplace remittance recovery | SaaS vendors | Private-offer payout mismatch | Marketplace reports | Mandate, support case | ISV channels | Medium | Marketplace ops | Prior weak |
| 20 | Customer underbilling true-up | SaaS/API vendors | Contracted usage not billed | Contract/logs/invoice | Mandate, corrected invoice | CFOs | High | RevOps | Round 269 failed |
| 21 | Construction retention release | Subcontractors | Warranty period ended | Contract/handover/defect proof | Mandate, release payment | Accountants | High | Lawyers | Prior weak |
| 22 | Public bid-security return | Suppliers | Tender security not returned | Tender docs and bank payment | Mandate, authority acknowledgement | Tender consultants | Medium | Lawyers/procurement | Cash release |
| 23 | Performance bond fee/closure release | Contractors | Bond remains live after acceptance | Beneficiary letter | Mandate, bank release | Guarantee brokers | Medium | Brokers | Prior weak |
| 24 | Pallet-pool deposit release | Manufacturers | Pallet deposits not reconciled | Pool statements | Mandate, deposit credit | Logistics accountants | Medium | Pool systems | Prior weak |
| 25 | Tooling title/final payment release | Manufacturers | Customer tooling payment withheld | Tool title and acceptance docs | Mandate, payment | Manufacturing brokers | Medium | Buyers/suppliers | Prior weak |
| 26 | LC discrepancy payment release | Exporters | Bank discrepancy blocks payment | LC/document set | Mandate, bank/buyer waiver | Forwarders | Medium-high | Banks/forwarders | Prior weak |
| 27 | Insurance admitted-claim evidence completion | SMEs | Insurer admits claim but wants final docs | Claim number and doc list | Mandate, payout | Brokers | Medium | Brokers | Insurance boundary |
| 28 | Utility deposit refund after closure | SMEs | Account closed, deposit unreturned | Utility final statement | Mandate, refund | Accountants | Low | Brokers | Prior weak |
| 29 | SaaS vendor credit balance refund | SMEs | Vendor account has unused credit | Vendor ledger | Mandate, refund | CFOs | Low-medium | SaaS spend tools | Cash refund |
| 30 | Telecom credit balance refund | SMEs | Closed account/unapplied cash | Telecom bills | Mandate, refund | Telecom brokers | Low | Brokers | Cash refund |
| 31 | EPR fee overpayment correction | Producers/importers | Wrong packaging fee basis | EPR declarations | Mandate, PRO credit | Compliance firms | Medium | Consultants | Regulatory/data |
| 32 | Customs post-clearance refund | Importers | Overpaid duty | Customs file | Mandate, authority claim | Customs brokers | Medium | Regulated brokers | Legal/tax boundary |
| 33 | Grant reimbursement release | Beneficiaries | Approved grant costs awaiting draw | Grant portal and invoices | Mandate, draw request | Grant consultants | Medium | Consultants | Prior weak |
| 34 | DRS operator settlement recovery | Retailers | Deposit-return variance | POS/RVM/operator statement | Mandate, operator correction | Retail accountants | Medium | POS/RVM owners | Prior weak |
| 35 | Card settlement defect cure | Merchants | Filed settlement payment blocked | Official defect notice | Mandate, cure packet | US accountants | Medium | Trust/legal | Prior weak |
| 36 | FIFA training reward recovery | Clubs | Clearing-house payment event | Club mandate and EPP record | Mandate, FCH case | Sports lawyers | Medium | Lawyers/FIFA | Prior weak |
| 37 | Royalty statement underpayment | Small licensors | Statement short-paid | Royalty agreement/statement | Mandate, publisher correction | Agents/accountants | Medium | Lawyers/agents | Legal/dispute risk |
| 38 | Franchise marketing fund true-up | Franchisees | Fund unused or overcharged | Franchise statement | Mandate, refund | Franchise accountants | Medium | Lawyers | Legal risk |
| 39 | Public works invoice certification release | Contractors | Certified invoice stuck at treasury | Certificate and payment queue | Mandate, AP escalation | Project accountants | Medium | Admin teams | Relationship/legal |
| 40 | Supplier portal onboarding payment hold release | B2B vendors | Enterprise invoice held for master-data issue | AP ticket, bank/tax/COI evidence | Mandate, payment release | AR/accountants | Medium | AR teams | Generic admin risk |

## Finalists

| Candidate | Simulated score | Advance? | Reason |
|---|---:|---|---|
| FactorReserve Settled-Debtor Holdback Release Lockbox | 88.0 | Yes | Best current-cash control point: factor has already collected debtor payments, the reserve ledger exists, and the output is a factor acknowledgement/payment rather than a report. |
| Invoice-discounting blocked-account release | 86.4 | No | Similar but bank workflows are more opaque and likely handled by existing treasury/admin staff. |
| Recourse-window expiry release | 86.0 | No | Strong subcase, but less complete than the broader reserve-lockbox frame. |
| Distributor price-protection credit | 84.7 | No | Cash-linked but too close to channel admin and rebate workflows that already failed. |
| Supplier portal payment-hold release | 82.5 | No | Cash is real, but ordinary AR/admin teams can handle most cases. |

## Candidate Advanced To Real Validation

Idea name: FactorReserve Settled-Debtor Holdback Release Lockbox

One-sentence thesis: recover matured factoring reserves and invoice-discounting holdbacks for SMEs only after the factor has already collected the underlying debtor payments and the contract/ledger supports release.

Exact buyer: Polish and CEE SMEs with 5-100 million PLN annual revenue using factoring, invoice discounting, recourse factoring, export factoring, or debtor-finance products, especially transport, staffing, wholesale, light manufacturing, and export suppliers with many invoices and weak back-office reconciliation.

Acute trigger: The SME has cash tied in a factor reserve, holdback, blocked account, recourse buffer, dispute reserve, or final settlement balance after debtor payments have already arrived, invoices aged out, or the contract release window has passed, but the balance is not being swept back because the factor ledger, debtor payments, deductions, disputes, and releases are not reconciled.

Control point: Signed limited recovery mandate over named reserve balances; factoring agreement; factor portal exports or monthly statements; debtor payment confirmations; invoice list; recourse/dispute-window expiry evidence; deductions schedule; release request; factor acknowledgement, credit note, settlement statement, bank transfer, or written no-go.

60-day proof:

- Three signed mandates over named factoring reserve ledgers.
- 150-400 invoices screened.
- At least 500,000 PLN in reserve/holdback balances reconciled.
- Two written factor acknowledgements or corrected settlement statements.
- One released payment or scheduled sweep above 75,000 PLN.
- 25,000-75,000 PLN collected or invoiced by the startup from setup and success fees.

6-month POC:

- 15-30 SME mandates.
- 2,000-6,000 invoice lines reconciled.
- 4,000,000-12,000,000 PLN in reserve/holdback balances reviewed.
- 1,000,000-3,500,000 PLN released, acknowledged, scheduled, or written off with a clear no-go.
- 250,000-650,000 PLN startup revenue.
- Gross margin above 65% after reconciliation contractors, accountant review, secure document handling, and channel commissions.

First acquisition mechanism: Source cases through factoring brokers, SME accountants, export-finance advisers, restructuring advisers, CFO-as-a-service providers, and trade-credit insurance brokers. Ask only for cases where the SME has factor statements, debtor-payment evidence, and a suspected matured reserve above 75,000 PLN. Do not cold-solicit distressed merchants or buy receivables.

Economics: Charge 4,000-12,000 PLN for a screened reserve ledger plus 8-15% of actually released, credited, swept, or factor-acknowledged cash, with success fees paid from the recovered balance. Reject files below 75,000 PLN candidate release, files with missing factor statements, and files where the factor has a live debtor dispute, fraud concern, chargeback, tax offset, insolvency issue, or legal setoff.

Copy risk: Factoring brokers, factors, accountants, finance consultants, and larger AR/AP recovery firms can copy. The defense is narrow factor-specific settlement playbooks, channel access to neglected SME ledgers, secure intake, repeat knowledge of reserve-release wording and evidence standards, and signed current mandates over specific balances before a generic consultant sees the file.

Why this is not a service/report/app/dashboard/database/marketplace/broker: The unit is a named cash release file with a factor acknowledgement, settlement correction, bank sweep, or written no-go. The startup is not selling analytics, software, introductions, or a reconciliation report; it only gets paid when a specific reserve balance is released, credited, scheduled, or definitively closed.

Boundaries:

- No receivables purchase, lending, factoring, debt collection, litigation, legal advice, tax advice, or aggressive threats.
- No cases where debtor payment has not arrived, debtor disputes are active, the factor alleges fraud or sanctions risk, or contract interpretation requires counsel before a basic release request can be made.
- SME counsel/accountant approves any disputed contractual point.
- The startup never holds client funds and never changes debtor payment directions.
- Reject PSP/acquirer reserve holds, marketplace payout holds, insolvency dividend claims, and consumer merchant cases.

Duplicate risk:

- Not Amazon Vendor Central, 3PL, Retail OTIF, BSP ADM, PSP reserve, marketplace KYBC, supplier rebate, grant draw, construction retention, lease deposit, or commercial deposit recovery.
- The distinctive control point is a factor-held reserve or invoice-discounting holdback after the factor has already received debtor cash and the SME can show the release ledger.

## Internal Simulation Score

Simulated score: **88.0 / 100**

Rationale:

- The buyer seeks return of its own cash from a finance provider, not new billing against a customer.
- The accepted file starts with factor statements and debtor-payment evidence, reducing speculative recovery.
- Ticket size can be large enough for a success fee and quick payback.
- The proof artifact is cash movement or factor acknowledgement, not a memo.
- The main weaknesses are factor discretion, broker/accountant copy risk, legal-boundary risk, and the chance that clean releases are already handled internally. It passes simulation only because the accepted case boundary is narrow and the first proof requires factor acknowledgement or actual sweep.

## Internal Kill Criteria

Kill if:

- Fewer than 20% of screened SME ledgers contain a reserve balance above 75,000 PLN that is both matured and document-clean.
- Factors refuse to acknowledge third-party-prepared release files even when the SME signs.
- Average time to factor acknowledgement exceeds 45 days.
- More than 30% of accepted files become legal, fraud, debtor-dispute, insolvency, or contract-interpretation matters.
- Accountants/factoring brokers internalize the workflow after one checklist.
- Gross margin falls below 60% after reconciliation labor and channel commissions.

## Decision

Advance to working-chat Zero To One validation because simulated score is strictly above 87 and the first proof is a signed mandate over named, factor-held cash converted into acknowledgement or release.
