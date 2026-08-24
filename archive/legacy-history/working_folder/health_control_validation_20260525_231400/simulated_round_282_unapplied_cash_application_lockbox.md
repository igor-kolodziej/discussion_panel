# Simulated Round 282 - UnappliedCash Application Lockbox

## Gate Context

- Simulation gate: validate only if simulated score is strictly >87.
- Real Zero To One gate after user update: working chat >=85 and fresh chat >=85.
- Round 280 failed at 84 because customer-acknowledged true-up receivables still depend on AP/procurement payment action and can be absorbed by CFO/AR/RevOps teams.
- Round 281 failed at 60 because making the startup reseller/payee of record added legal, VAT, credit, and payment-flow risk.
- Round 282 searches for current cash that has already moved but is not yet operationally applied.

## Raw Hard-Control Search Table

| # | Candidate | Buyer | Acute trigger | Transferable control point inside 60 days | First cash proof | Main copy risk | Internal disposition |
|---:|---|---|---|---|---|---|---|
| 1 | Unapplied B2B SaaS cash application lockbox | SaaS/API/data vendors | Customer already paid but cash sits unapplied/suspense | Signed mandate, bank receipt, AR ledger, remittance, invoice tie-out | Cash applied to invoice/account and fee invoice | AR teams, BPO, BlackLine/HighRadius, ERP consultants | Selected |
| 2 | Wrong-entity payment application release | Multi-entity B2B vendors | Payment landed in wrong group entity | Treasury/AR file and controller approval | Reclass/applied cash | Controllers/accountants | Finalist, folded into #1 |
| 3 | Unmatched SWIFT remittance rescue | Exporters | Wire received with missing/garbled references | Bank receipt, invoice, remittance proof | Payment matched | Finance teams | Finalist |
| 4 | Customer overpayment offset direction | SaaS/vendors | Customer overpaid but next invoice unpaid | Customer offset approval and AR application | Offset posted | AP/AR teams | Capped, credit memo branch adjacency |
| 5 | Marketplace payout suspense application | Platform sellers | Payout received but not reconciled to orders | Payout/export ledger | Cash applied | Accountants/platform ops | Capped, platform branches failed |
| 6 | Distributor rebate unapplied cash | Channel partners | Rebate cash received but not mapped | Remittance and partner ledger | Applied cash | Channel ops | Capped |
| 7 | Grant reimbursement cash application | Grant recipients | Grant cash received but costs not mapped | Grant statement and accounting packet | Applied grant cash | Accountants | Capped, grant branch failed |
| 8 | Insurance payout allocation release | Multi-site operators | Insurer paid but proceeds not applied to claim/site/vendor | Claim remittance and ledger | Applied cash | Brokers/adjusters | Capped by insurance authority |
| 9 | Bank lockbox unidentified receipts cleanup | PE-backed groups | Customer wires sit in unidentified receipts | Lockbox report and AR authority | Applied cash | BPO/cash-app tools | Finalist |
| 10 | Debt collection suspense cleanup | Collection agencies | Debtor payments not allocated | Debtor ledger | Applied cash | Regulated collection | Reject |
| 11 | 3PL billing credit application | Ecommerce brands | 3PL credit exists but invoices still open | Credit memo and statement | Credit applied | 3PL ops/accountants | Capped |
| 12 | Carrier refund application | Shippers | Carrier issued refund but not allocated | Remittance/bank/export | Applied cash | Freight audit | Capped |
| 13 | Customer advance-to-invoice conversion | B2B vendors | Prepayment sits as customer advance | Contract/invoice/customer approval | Revenue/cash applied | Controllers | Finalist |
| 14 | Acquired-company old bank receipt cleanup | PE rollups | Receipts in old accounts after carveout | Bank/AR/acquisition docs | Applied cash | Integration teams | Capped by complexity |
| 15 | Remittance advice reconstruction for German buyers | Exporters | Buyer paid but references in PDFs/emails | Buyer remittance + bank | Applied cash | AR/accountants | Finalist |
| 16 | Payment-service provider orphan payout mapping | SaaS/ecommerce | PSP payout batch unmatched | PSP reports | Applied cash | payment ops | Capped, PSP branches failed |
| 17 | Customer credit balance refund mandate | SMEs | Vendor owes refund | Vendor acknowledgement | Refund | CreditMemo failed |
| 18 | Public authority overpayment return | Suppliers | Treasury paid but invoice mismatch | Authority remittance | Applied/refund | Public admin | Capped |
| 19 | Lockbox bank file migration cleanup | B2B vendors | Bank lockbox migration breaks remittance | Bank file and AR ledger | Applied cash | banks/BPO | Finalist |
| 20 | Invoice factoring unapplied debtor payments | Factored SMEs | Debtor paid factor but seller ledger open | factor remittance | Applied cash | factoring ops | Regulated/capped |
| 21 | Subscription prepayment recognition pack | SaaS vendors | Annual prepay not tied to order | order/remittance | Applied cash | finance ops | Capped unless cash blocked |
| 22 | Multi-currency payment matching desk | Exporters/SaaS | FX wires miss invoice totals | bank/remittance/FX evidence | Applied cash | AR teams | Folded into #1 |
| 23 | Acquirer settlement application for B2B platforms | Platforms | Card settlement not mapped to invoices | PSP data | Applied cash | finance tools | Capped |
| 24 | Customer payment recall prevention | Vendors | Customer threatens recall due mismatch | bank/customer/AP proof | Payment retained/applied | AR teams | Capped |
| 25 | ERP customer-master merge cash cleanup | SaaS/vendors | duplicate customer records leave cash open | ERP ledger and customer confirmation | Applied cash | ERP consultants | Folded into #1 |
| 26 | Failed invoice-number reference repair | Exporters | Buyer paid old/wrong invoice number | remittance + invoice map | Applied cash | AR teams | Folded into #1 |
| 27 | Private-equity portfolio unidentified receipts sprint | PE ops | portfolio has legacy unapplied receipts | portfolio mandate | Applied cash | BPO/accountants | Finalist |
| 28 | Utility customer deposit application | Site operators | deposits/credits not mapped | statements | cash applied/refunded | utility auditors | Capped |
| 29 | Telecom wholesale settlement application | VoIP/SMS providers | carrier payments not matched to traffic | CDR/remittance | Applied cash | telecom billing | Capped, CDR branch failed |
| 30 | Paid but suspended-account release | SaaS vendors | service suspended despite payment | bank/remittance/customer proof | account restored/payment applied | support teams | Good sub-use case |
| 31 | Customer-payment evidence room for audit | Vendors | auditors need cash tie-out | bank/AR package | audit acceptance | auditors/accountants | Report-like, reject |
| 32 | AP debit balance conversion | Buyers | vendors have debit balances | statements | cash/offset | AP recovery tools | CreditMemo adjacency |
| 33 | Cross-border invoice legal-entity mismatch application | Vendors | paid legal entity differs from invoice | treasury/legal-entity file | applied/rebilled cash | controllers | Folded into #1 |
| 34 | Bank fees/withholding short-pay application | Exporters | wire short by fees/taxes | bank proof/customer approval | applied net payment | AR/accountants | Capped |
| 35 | Customer portal paid-status correction | Vendors | portal shows paid, ERP shows open | portal/bank/ERP evidence | status corrected | AR teams | Good sub-use case |
| 36 | Cash application overflow bench | CFOs/controllers | month-end close backlog | paid ticket batch | applied receipts | BPO | Too generic unless named cash |

## Finalists

| Candidate | Control strength | Speed to cash | Copy resistance before control | Main reason not selected |
|---|---:|---:|---:|---|
| Wrong-entity payment application release | 8 | 9 | 5 | Too narrow alone; useful as a sub-pattern. |
| Unmatched SWIFT remittance rescue | 8 | 8 | 5 | Strong for exporters but less repeatable than SaaS/API/data vendors with usage/renewal pressure. |
| Bank lockbox unidentified receipts cleanup | 8 | 8 | 5 | Can become generic BPO unless tied to named current accounts and commercial consequences. |
| Customer advance-to-invoice conversion | 8 | 9 | 5 | Often accounting-policy sensitive; better inside broader lockbox with controller approval. |
| Private-equity portfolio unidentified receipts sprint | 7 | 8 | 5 | Good channel but looks like finance-ops cleanup unless each file is named cash with a release event. |
| Unapplied B2B SaaS cash application lockbox | 9 | 9 | 6 | Best: cash already exists, no payment intermediation, proof is ledger application and customer/account release. |

## Selected Candidate

**Idea name:** UnappliedCash Application Lockbox

### Thesis

For B2B SaaS, API, data, and usage-priced vendors, customer cash often lands before finance ops can tie it to the correct invoice, legal entity, customer account, remittance advice, usage statement, or renewal. The startup accepts only named payments that have already arrived in the vendor's bank or lockbox, reconstructs the evidence trail, obtains controller-approved application, and gets paid when cash moves from suspense/unapplied status to a specific invoice/account/revenue-release outcome.

### Control Table

| Field | Forced answer |
|---|---|
| Buyer | 20-500 employee B2B SaaS/API/data/infrastructure vendors and PE-backed multi-entity B2B groups with enterprise wires, ACH/SEPA/SWIFT payments, lockbox receipts, and messy remittance data. |
| Acute trigger | Customer has paid, but the vendor still shows the invoice/account as open, suspended, over-limit, non-renewed, unreconciled, or not revenue-ready because cash is in unidentified receipts, suspense, customer advance, wrong entity, duplicate customer master, wrong invoice reference, FX short-pay, missing remittance, or portal mismatch. |
| Transferable control point | Signed cash-application mandate over named receipt files; vendor bank/lockbox proof; AR aging and ERP ledger extract; customer remittance/AP ticket where available; invoice/order/usage statement; controller-approved application rule; before/after applied-cash evidence; fee right tied to applied cash or clean no-go. |
| Signed/titled/assigned/prepaid within 60 days | Three vendor mandates, at least 1,000,000 PLN equivalent in named unapplied/suspense cash under review, at least 500,000 PLN applied to invoices/accounts or cleanly no-goed, at least one customer account/renewal/license hold released, and 25,000+ PLN collected or invoiced in fixed/application fees. |
| First acquisition mechanism | Outreach to SaaS controllers, CFOs, RevOps, billing-migration firms, NetSuite/Stripe/Chargebee/Maxio consultants, PE operating partners, and fractional CFOs with a narrow ask: "Do you have customer cash already in the bank that is still sitting in unapplied receipts, suspense, or wrong-account status?" |
| Gross margin and payback logic | 5,000-20,000 PLN setup for named receipt batches plus 1-3% of applied cash where attribution is clear. Cash proof arrives faster than receivable collection because the cash is already in the vendor bank/lockbox. Main costs are secure data handling, data cleanup, remittance reconstruction, and controller review. |
| Copy risk | In-house AR/cash-app teams, outsourced finance BPOs, AR automation platforms, NetSuite/ERP consultants, billing consultants, accountants, and RevOps teams. |
| Why incumbents cannot copy before control | The startup controls only the signed named batch: receipt IDs, bank/lockbox evidence, remittance reconstruction, ERP before/after state, customer/AP proof, controller application approval, and fee right. Tools and BPOs can copy future workflow but not the current batch once authority and evidence room are in motion. |
| Why it is not a service/report/app/dashboard/marketplace/broker | It does not sell analytics or reconciliation software. It accepts only named cash already received and produces applied-cash outcomes, customer/account release, clean offset/no-go, and paid fee. |

### Internal Simulation

**Simulated score: 88.2**

Reasons this clears simulation:

- It fixes the Round 280 debtor-control problem: cash has already moved into the vendor's bank/lockbox.
- It avoids the Round 281 payment-intermediary problem: the startup never becomes payee, reseller, escrow, factor, or custodian.
- The first proof is hard and fast: bank receipt before, ledger application after, customer/account release, and fee invoice.
- It has high willingness to pay when unapplied cash blocks renewal, account access, revenue recognition, close, audit, or customer-success status.
- The founder can reject broad AR outsourcing and accept only high-value named cash batches.

Reasons the score does not exceed 88.2:

- Strong in-house and outsourced substitutes exist.
- Many vendors should already have cash-application processes.
- The product can degrade into generic finance-ops cleanup.
- Success fees on already-received cash may face attribution disputes, so fixed fees should dominate.
- Sensitive bank, ERP, customer, and invoice data creates trust friction.

### Internal Gate Decision

Advance to working-chat validation because simulated score is strictly >87 and the control point is materially different from failed receivable-release, reseller, platform-remittance, credit-memo, and generic AR-cleanup branches.
