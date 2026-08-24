# Simulated Round 314: FactorableInvoice Acceptance Release Desk

## Gate Setup

- Simulation gate: strictly >87.
- Real working-chat gate: >=85.
- Real fresh-chat gate: >=85.
- Search branch: current payment/funding release with channel-driven blocker.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute Trigger | 60-Day Control Proof | Internal Score | Decision |
|---|---|---|---|---|---:|---|
| 1 | FactorableInvoice Acceptance Release Desk | CEE suppliers using factoring/invoice finance | Factor rejects named invoices until debtor acceptance, portal status, assignment notice, GRN, or no-dispute check clears | Signed supplier mandate, factor deficiency, debtor portal/AP trail, accepted eligibility, first funded invoice | 88.3 | Advance |
| 2 | Credit-Insurance Limit Release Desk | Exporters with insured receivables | Insurer limit missing or reduced so shipment/order blocked | Broker/insurer request, buyer docs, approved limit | 83.0 | Reject: broker/underwriter control |
| 3 | Purchase-Order Finance Release Desk | Importers/distributors | PO funder blocks draw pending supplier/customer evidence | Funder deficiency, supplier/customer evidence, funded PO | 82.5 | Reject: lender underwriting |
| 4 | Bank Guarantee Release Desk | Contractors/suppliers | Guarantee tied up after acceptance | Acceptance docs, beneficiary release, bank release | 78.5 | Reject: legal/public works overlap |
| 5 | Factoring Reserve Release | Suppliers/factoring clients | Reserve held after debtor payment | Factor statement, payment proof, reserve release | 75.0 | Reject: prior branch failed |
| 6 | Borrowing-Base Draw Deficiency Release | Borrowers with ABL/factor facilities | Draw blocked by AR/inventory exception | Lender deficiency, accepted certificate | 82.0 | Reject: prior branch exhausted |
| 7 | SupplierPortal Invoice Release | Suppliers to enterprises | AP portal state blocks payment | Buyer blocker, portal acceptance, payment | 84.0 | Prior fail, inform #1 |
| 8 | Export Documentary Collection Release | Exporters | Bank/payment blocked by document discrepancy | Bank notice, corrected docs, payment | 78.0 | Reject: trade finance/legal |
| 9 | LC Discrepancy Cure Desk | Exporters | LC docs rejected | Bank discrepancy notice, accepted docs | 74.0 | Reject: already failed branch |
| 10 | Virtual Card Payment Direction Release | Suppliers | Customer forces VCC/portal payment setup | Customer AP instruction, paid invoice | 73.0 | Reject: prior branch failed |
| 11 | Invoice Discounting Eligibility Pack | SMEs | Bank excludes invoices due documentation gaps | Bank letter, invoice docs, included collateral | 84.5 | Merge into #1 |
| 12 | Debtor Confirmation Sprint For Factors | Factoring brokers | Slow debtor verification blocks factor onboarding | Debtor ack, factor onboarding | 86.0 | Merge into #1 as channel |
| 13 | Reverse Factoring Supplier Onboarding Release | Suppliers invited to SCF programs | SCF portal refuses supplier setup | Buyer invite, platform acceptance, first early payment | 86.5 | Related, but more platform-copyable |
| 14 | Dynamic Discounting Release Desk | Suppliers | Buyer early-pay portal setup blocked | Buyer invite, accepted early-pay account | 82.0 | Reject: low pain |
| 15 | Credit-Note Offset To Funding Release | Suppliers | Factor excludes debtor due credit-note mismatch | Reconciliation, debtor/factor acceptance | 82.0 | Reject: narrow accounting |
| 16 | Retention Invoice Factoring Release | Contractors | Factor excludes retention invoice pending certificate | Certificate, factor acceptance | 77.0 | Reject: construction disputes |
| 17 | Public Buyer Invoice Funding Release | Public suppliers | Invoice funder rejects due buyer acceptance proof | Public portal acceptance, funded invoice | 82.5 | Reject: public payment cycle |
| 18 | Marketplace Seller Invoice Finance Release | Platform sellers | Lender rejects payout/invoice proof | Marketplace reports, lender acceptance | 75.0 | Reject: platform finance crowded |
| 19 | Distributor Rebate Receivable Funding Release | Distributors | Factor excludes rebate receivable | Vendor ack, factor acceptance | 76.0 | Reject: rebate branch failed |
| 20 | Debtor Name/Bank Match Funding Release | Exporters | Factor/bank rejects due debtor identity mismatch | Registry docs, debtor ack, funded invoice | 83.0 | Subset only |
| 21 | Contract Assignment Notice Acceptance Desk | Suppliers | Debtor has not acknowledged assignment notice | Notice, debtor ack, factor purchase | 85.0 | Subset of #1 |
| 22 | Goods-Receipt Proof To Factor Desk | Industrial suppliers | Factor excludes invoice until GRN/service entry | GRN/SES evidence, factor acceptance | 85.5 | Strong subset of #1 |
| 23 | EDI Invoice Acceptance To Factor Desk | Manufacturers | Factor excludes invoice until debtor EDI accepted | EDI acceptance, factor funding | 84.5 | Subset |
| 24 | Customer Portal Export For Factoring | Suppliers | Factor requires portal proof of accepted invoice | Portal export, factor acceptance | 85.0 | Subset |
| 25 | Factoring Broker Overflow Desk | Factoring brokers | Broker has approved supplier but cannot clear docs | Broker referral, funded invoice | 86.8 | Acquisition channel |
| 26 | Recourse Buyback Prevention Desk | Factored suppliers | Factor threatens buyback due debtor non-ack | Debtor ack/no-go, avoided buyback | 81.5 | Reject: legal/collections |
| 27 | Invoice Finance KYC Rework Desk | SMEs | Lender onboarding KYC blocks facility | KYC pack, approved facility | 78.0 | Reject: generic lender onboarding |
| 28 | Exporter Debtor Verification File | Exporters | Foreign debtor verification blocks invoice finance | Debtor proof, factor acceptance | 84.0 | Subset |
| 29 | Customer No-Dispute Confirmation Desk | Suppliers | Factor requires no-dispute confirmation | Debtor no-dispute ack, funded invoice | 85.0 | Subset |
| 30 | Assignment of Proceeds Notice Release | Suppliers | Buyer procurement rejects factor assignment | Notice acceptance, funded invoice | 83.0 | Legal boundary |
| 31 | Supply-Chain Finance First-Payment Desk | Suppliers in buyer SCF program | Buyer/SCF platform setup blocks first early payment | SCF account acceptance, first early payment | 84.0 | Potential but lower urgency |
| 32 | Factored Invoice Portal Evidence Room | Suppliers | Factor rejects due mixed debtor portal proofs | Evidence room, accepted invoice | 85.5 | Subset |
| 33 | Cross-Border VAT/Withholding Funding Release | Export suppliers | Factor excludes invoices over tax uncertainty | Tax docs, factor acceptance | 76.0 | Tax boundary |
| 34 | Invoice Finance UBO/AML Repair | SMEs | Factor KYC blocks funding | KYC documents, approved funding | 76.5 | Generic/KYC |
| 35 | Debtor Concentration Exception Release | Suppliers | Factor holds funding due concentration exception | Buyer ack/support, release | 75.5 | Lender underwriting |

## Finalists

1. **FactorableInvoice Acceptance Release Desk**: strongest because the buyer has a specific funder deficiency and a path to cash if the debtor acceptance packet clears.
2. **Goods-Receipt Proof To Factor Desk**: sharp industrial subset around GRN/service-entry evidence.
3. **Contract Assignment Notice Acceptance Desk**: legally sensitive, but useful as a subset when notice wording is already provided by the factor.
4. **Factoring Broker Overflow Desk**: useful channel because brokers see approved suppliers stuck on debtor proof but are not paid to chase enterprise portals.
5. **Reverse Factoring Supplier Onboarding Release**: attractive early-payment angle, but weaker because buyer platform can internalize more.

## Selected Candidate

**FactorableInvoice Acceptance Release Desk**

## Internal Score: 88.3

Why it clears simulation:

- Starts with a current funding event: the supplier has invoices it wants funded and a factor/invoice-finance provider has issued a concrete deficiency.
- Proof is cash movement or financing eligibility: factor-funded invoice, accepted invoice schedule, debtor no-dispute acknowledgement, or clean no-go.
- The channel is clearer than generic AR: factors and brokers can refer cases where the facility exists but named invoices are ineligible because debtor acceptance evidence is missing.
- It keeps the SupplierPortal cash-release insight but narrows intake to third-party factor deficiencies, reducing drift into ordinary collections.
- The startup controls the signed supplier mandate, factor deficiency, debtor portal/AP trail, evidence file, accepted schedule, and first funding proof.

## Internal Concerns

- Factors and brokers may already chase this or require debtor verification themselves.
- Some cases will be real debtor disputes, credit risk, concentration limits, recourse problems, legal assignment issues, or underwriting decisions outside scope.
- Debtor AP teams may ignore third parties.
- Success fees must avoid collection-agency or finance-broker boundaries.
- This is adjacent to prior borrowing-base/factor failures, so distinction must stay narrow: named invoice eligibility and first funded invoice, not reserve release or generic borrower reporting.

## 60-Day Proof Standard

- 5 prepaid cases referred by suppliers, factors, or factoring brokers.
- At least 1,500,000 PLN in invoices rejected or delayed for debtor acceptance, portal proof, GRN/service-entry, assignment notice, no-dispute confirmation, or EDI acceptance.
- 3 factor-accepted invoice schedules, debtor acknowledgements, funded invoices, or clean no-go outcomes.
- 1,000,000 PLN of invoice value made eligible or no-go'd.
- 60,000-120,000 PLN collected.
- Rejection log above 50% for credit risk, disputes, underwriting issues, legal assignment problems, concentration caps, debtor insolvency, tax issues, and generic AR chasing.

## Why This Is Not A Duplicate

- Not BorrowingBase Certificate Book Buyout or Draw-Release Desk: no recurring collateral certificate or lender facility operation.
- Not factor reserve release: no old reserve recovery after debtor payment.
- Not SupplierPortal Invoice Release: the customer AP process matters only because a factor/invoice-finance provider has issued a funding deficiency.
- Not generic AR/collections: debtor acknowledgement and factor eligibility are required.
