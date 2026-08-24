# Level-2 D-012 — Cross-Channel Duplicate Payment Gate

## Problem And Payer Evidence

Duplicate controls commonly operate inside one payment system and depend on exact identifiers. SAP’s standard check compares fields such as supplier, currency, amount, reference, and invoice date; Microsoft Dynamics can reject a reused invoice number for the same vendor. These controls can miss altered invoice numbers, duplicate vendor records, and payments split across ERP, procurement-card, expense, and bank channels.

Cross-channel risk is directly documented. Edmonton’s auditor found no process for detecting duplicates across multiple platforms and matched 78,806 procurement-card transactions against other payments, finding six duplicates worth CAD 1,691. A New York City audit similarly warned that lack of integration between procurement cards and the financial system allowed an invoice to be paid twice.

The prevalence is contradictory:

- Palo Alto reported 24 confirmed duplicates, but 17 had already been identified and resolved by staff. The potential duplicates were only 0.1% of average invoice volume and 0.004% of payment value.
- Toronto processed more than 500,000 invoices worth CAD 5.8 billion in nine months. From 20 high-risk pairs, it confirmed two duplicate invoices worth CAD 4,570 and nine incorrect-vendor payments; CAD 43,379 had been recovered.
- Edmonton’s six cross-channel matches represented about 0.008% of the procurement-card transactions examined.
- Some entities report effective controls and no material weakness. This supports the packet’s warning that an organization may have little recoverable risk.

The payer is the controller, head of accounts payable, internal-audit lead, or finance director at an organization with multiple payment channels. A defensible denominator is not “all businesses”: it is organizations able to export at least 12 months of vendor master, ERP invoice/payment, procurement-card, expense, and bank-disbursement data. The public research did not establish how many Polish organizations meet that condition. A practical initial eligibility threshold is 25,000–250,000 annual transactions across at least two independently controlled channels.

Public willingness proxies exist. London City Hall disclosed an annual cost of £15,000 for duplicate-payment software. Hampshire County Council awarded a three-year duplicate-payment audit-software contract worth £157,713. These are public-sector enterprise purchases, not evidence that Polish mid-market firms will buy a batch audit.

The closest substitutes are ERP duplicate checks, spreadsheet matching, vendor-statement reconciliation, internal audit, and contingency-fee recovery auditors. They persist because they use trusted internal data and workflows, require no new processor, and allow finance staff to decide whether a match is a legitimate recurring charge, credit/rebill, split payment, or recoverable duplicate.

## Proposed Transaction

The first paid event is a read-only historical audit:

- Customer supplies 12 months of approved exports.
- The service normalizes vendor identities and screens exact, fuzzy, split, and cross-channel matches.
- Finance receives an evidence packet for each candidate rather than an accusation of fraud.
- The customer alone adjudicates duplicate status, contacts vendors, and decides whether recovery is appropriate.
- The audit closes with documented confirmed value, recoverable value, false-positive burden, reviewer time, and control gaps.

An interpreted planning range is PLN 4,000–20,000 for a historical scan, depending on transaction volume and number of systems. A continuing service could be PLN 1,500–8,000 per month or approximately PLN 0.05–0.20 per screened transaction, with a minimum monthly charge. These are hypotheses anchored only loosely by the two UK public purchases; Polish willingness is unknown.

Sensitivity is dominated by recoverable value and review time. At PLN 5,000 for 100,000 screened transactions, the stated economic premise requires more than PLN 15,000 of recoverable duplicates. The operational premise permits fewer than 100 reviewer hours at one hour per 1,000 transactions, but a viable small engagement likely needs to be materially better—approximately 10–30 total reviewer hours—because recovery work is additional.

A minimal service can be built within approximately PLN 25,000–60,000 before proof: secure file intake, isolated processing, deterministic rules, limited fuzzy matching, audit logging, security documentation, professional advice, and contractor review. A production integration, continuous bank feed, or payment-blocking capability is outside the private-proof scope and could exceed the founder’s budget.

Required access and rights are exact and limited:

- Written authorization from the customer’s finance/data owner.
- Read-only exports of vendor master, invoices, payments, card transactions, expense transactions, and bank disbursements.
- Stable source-system and transaction identifiers, currency, amount, dates, payee details, invoice reference, and reversal/credit indicators.
- No banking credentials, payment initiation, vendor contact, recovery authority, or ability to block payments.
- A processor agreement covering documented instructions, confidentiality, security, subprocessors, retention, deletion/return, incidents, and audit cooperation.
- Contractual confirmation that the customer may provide the records and that outputs remain customer-confidential.
- Counsel review where records contain personal data, employee expenses, sole-trader information, or allegations that could be treated as fraud claims.

## Acquisition Route

The first route is through accounting firms, outsourced CFOs, and internal-audit consultants. The offer is a bounded “12-month cross-channel payment-control scan,” not an autonomous fraud-detection product.

A partner receives:

- A one-page data-readiness checklist.
- A sample finding packet with transaction lineage and neutral language.
- A fixed-scope pilot agreement.
- An optional partner margin or disclosed referral fee.
- A customer-controlled adjudication workbook.
- A deletion certificate after the agreed retention period.

The first customer should already have a trusted adviser, more than one payment channel, and a known export owner. That reduces both trust friction and the risk that the founder becomes responsible for extracting data from a live ERP.

The initial process is:

- Partner identifies one finance leader with 12 months of exportable records.
- A 30-minute readiness call confirms systems, volume, identifiers, and authority.
- The customer exports files to an isolated workspace.
- Screening produces a deliberately narrow candidate set.
- One finance employee adjudicates the candidates in a recorded session.
- The final meeting measures confirmed duplicates, recoverability, time, and reasons for rejection.

Partner acquisition remains unverified. Accountants may view this as outside their recurring work, may prefer incumbent recovery auditors, or may be unwilling to introduce a small processor handling sensitive payment data.

## Decision-Critical Unknowns

**Verified:** Exact-field ERP duplicate controls exist. Cross-platform gaps can occur. Public organizations have purchased dedicated duplicate-payment software. Some audited duplicate and incorrect payments were recovered.

**Interpreted:** Organizations with 25,000–250,000 annual transactions and multiple payment channels are the likely initial payer population. Public UK contract values indicate budget existence but do not establish Polish pricing.

**Unknown:** The Polish payer denominator; duplicate prevalence by organization type; proportion of matches that remain unrecovered; time needed per 1,000 transactions; data completeness; usefulness of fuzzy vendor resolution; partner conversion; renewal demand; acceptable hosting model; and the proposed PLN price ranges.

**Contradicted:** A universal high-risk premise is contradicted by Palo Alto’s very low duplicate value, staff’s prior identification of most cases, Edmonton’s small recovered amount, and entities reporting adequate existing controls. Broad “every company loses 1–2%” marketing claims should not be used without customer-specific evidence.

**Counsel-required:** GDPR roles and lawful basis; treatment of employee and sole-trader data; cross-border hosting; contractual security obligations; professional-liability limitations; wording that distinguishes control exceptions from fraud; retention and evidence preservation; and any contingency fee tied to recovery.

Not every critical premise is verified. In particular, the required combination of recoverable value above three times the audit fee and low reviewer burden is unknown.

The cheapest private proof is one authorized 12-month scan. It should use three separately exported sources if available, suppress low-value candidates, and require finance adjudication. A PLN 2,000–8,000 proof budget is plausible if extraction is customer-operated. Stop conditions are: unusable identifiers, fewer than three credible cross-channel candidates, confirmed recoverable value below three times the proposed fee, or reviewer burden above one hour per 1,000 transactions.

## Evidence And Sources

Dated direct-URL ledger; research accessed 2026-08-22:

- **2018 — Edmonton, Audit of Accounts Payable:** six cross-platform duplicates among 78,806 card transactions; no cross-platform detection process. https://www.edmonton.ca/sites/default/files/public-files/18439_Audit_of_Accounts_Payable.pdf
- **2017-04-25 — Palo Alto, Continuous Monitoring Audit: Payments:** 24 confirmed duplicates; 17 previously resolved; 0.1% of invoices and 0.004% of value. https://www.cityofpaloalto.org/files/assets/public/v/1/city-auditor/z-old-reports/continuous-monitoring-payments-mini-packet-04-25-17.pdf
- **2016 — Toronto, Continuous Controls Monitoring:** more than 500,000 invoices worth CAD 5.8 billion; duplicate/incorrect-payment findings and recoveries. https://www.toronto.ca/legdocs/mmis/2016/au/bgrd/backgroundfile-90683.pdf
- **2025-06 — London City Hall FOI:** £15,000 annual duplicate-payment software cost. https://www.london.gov.uk/who-we-are/governance-and-spending/sharing-our-information/foi-disclosure-log/foi-accounts-payable-software-jun-2025
- **2023-10-26 — Hampshire County Council award:** £157,713 three-year duplicate-payment audit-software contract. https://www.contractsfinder.service.gov.uk/notice/e7084047-4a4f-4bb3-ad62-c76ab15f638c
- **Accessed 2026-08-22 — SAP Help, duplicate invoice check:** standard comparison fields and customization. https://help.sap.com/docs/SUPPORT_CONTENT/fiaccounting/3361878522.html
- **Accessed 2026-08-22 — Microsoft Learn, Payables Management:** configurable duplicate document-number control by vendor. https://learn.microsoft.com/en-us/dynamics-gp/financials/payablesmanagement
- **2005 — NYC Comptroller, procurement-card audit:** integration gap can permit an invoice to be paid through two routes. https://comptroller.nyc.gov/reports/audit-report-on-the-use-of-procurement-cards-by-the-department-of-parks-and-recreation/
- **Accessed 2026-08-22 — ICO, controller–processor contracts:** required processor terms, security, deletion, subprocessors, and audit cooperation. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/contracts-and-liabilities-between-controllers-and-processors-multi/
- **Accessed 2026-08-22 — APQC, AP cost benchmark:** median reported cost of USD 1.36 per invoice line item across a sample of 4,135 companies; not a duplicate-loss benchmark. https://www.apqc.org/resources/benchmarking/open-standards-benchmarking/measures/total-cost-perform-process-process-10

### Query trace

1. `site:gao.gov duplicate payments accounts payable audit vendor invoice`
2. `site:oversight.gov duplicate payments audit accounts payable invoices`
3. `site:nyc.gov comptroller duplicate payments audit accounts payable`
4. `city audit no high risk duplicate payments accounts payable`
5. `site:oracle.com documentation duplicate invoice check invoice number supplier amount date`
6. `site:help.sap.com duplicate invoice check vendor company code currency amount`
7. `site:learn.microsoft.com Dynamics duplicate invoice number accounts payable vendor`
8. `site:gov.uk contract award duplicate payment audit software pricing accounts payable`
9. `site:assets.applytosupply.digitalmarketplace.service.gov.uk duplicate payment recovery pricing percentage recovered`
10. `procurement card accounts payable duplicate payments across systems audit report`
11. `site:ico.org.uk financial data processor data protection controller processor contract security`
12. `accounts payable cost per invoice benchmark 2024 APQC`

