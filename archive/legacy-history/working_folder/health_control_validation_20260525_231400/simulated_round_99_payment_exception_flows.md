# Simulated Round 99: Payment-Regulation Exception / Acknowledged Flow Lanes

Date: 2026-05-27

## Pivot From Round 98

Merchant Center Suspension Release Lane failed working-chat validation at `77 / 100`.

Reason to pivot: the pain and case-flow channel were strong, but the evaluator capped the idea because Google controls the final decision and generic remediation can be copied. This round moves to formal payment-regulation exception flows where release criteria are more defined and the founder can control signed current tickets, customer authorizations, and evidence packets without moving funds.

## Current Source Notes

Official and scheme-level materials show that EU instant payments and Verification of Payee / Verification of Payee-style services are now formal obligations and operational realities for payment service providers:

- Regulation (EU) 2024/886 amending SEPA rules for instant credit transfers: `https://eur-lex.europa.eu/eli/reg/2024/886/oj`
- European Commission instant payments overview: `https://finance.ec.europa.eu/consumer-finance-and-payments/payment-services/instant-payments_en`
- European Payments Council Verification Of Payee Scheme page: `https://www.europeanpaymentscouncil.eu/what-we-do/verification-payee`
- EPC Verification Of Payee Scheme Rulebook page: `https://www.europeanpaymentscouncil.eu/document-library/rulebooks/verification-payee-scheme-rulebook`

The hard-control pattern is not payment execution, factoring, or regulated advice. It is a signed exception-ticket lane from payment bureaus, ERP implementers, PSPs, and corporate treasury/AP teams dealing with beneficiary name/IBAN mismatch cases under verification-of-payee regimes.

## Raw Candidates

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin / payback logic | Copy risk and why incumbents cannot copy before control | Why not wrapper |
|---|---|---|---|---|---|---|---|---|---|
| 1 | VoP Bulk Payment Exception Release Desk | PSPs, payment bureaus, ERP/AP teams with payee-name mismatch exceptions | Bulk payments slowed by no-match/close-match warnings, supplier master data dirty | Signed partner ticket lane, customer authorization, beneficiary confirmation packets, current exception batches | Partner routing, 10-30 prepaid exception batches, customer authorizations | Payment bureaus, ERP integrators, treasury consultants | 2k-15k PLN/batch; >60% margin | Incumbents can build tools, but cannot copy signed current batches and supplier confirmations | Ticket/payment-data lane |
| 2 | Instant Payments PSP Acceptance Evidence Pack | PSP vendors/EMIs implementing instant credit transfers | Regulatory acceptance/testing deadline and bank/PSP onboarding | Test evidence pack, PSP/vendor channel, paid implementation tickets | Prepaid acceptance packs | Core banking/payment vendors | High enterprise fees | Large consultancies and vendors copy | Evidence lane |
| 3 | SEPA Direct Debit Mandate Migration Lockbox | SaaS/gyms/utility billers changing PSPs | Mandate transfer/payment failure | Customer mandate consents, PSP migration file, first collections | Customer-approved mandate transfer, first debit batch | Billing platforms/accountants | Medium | PSPs/payment platforms can copy | Payment book |
| 4 | Corporate Supplier Bank-Account Reverification Book | CFO/AP teams | Payment fraud controls, bank mismatch | Supplier confirmations, AP master-data updates | Customer and supplier confirmations | Accountants/ERP partners | Medium | Generic AP cleanup if no VoP trigger | Data/payment book |
| 5 | Payroll Beneficiary Name Exception Desk | Payroll bureaus/employers | Payroll batches generate beneficiary warnings | Employee authorization, payroll bureau ticket lane | Prepaid current payroll exception batches | Payroll bureaus | High urgency but sensitive data | Payroll providers can do in-house | Ticket lane |
| 6 | EBICS/Host-to-Host Bank File Exception Lane | ERP/treasury teams | Payment files rejected by bank | Bank rejection tickets, ERP partner case flow | Prepaid current rejections | ERP integrators | High ticket | Integrators can copy; technical support | Ticket lane |
| 7 | ISO 20022 Payment Format Migration Release Desk | Corporates/banks | Legacy payment files rejected | ERP/bank case flow, current file errors | Prepaid current migrations | ERP/payment consultants | Medium-high | Crowded migration services | Ticket lane |
| 8 | Sanctions-Screening False Positive Release Pack | Corporates/PSPs | Payments held by screening false positives | Customer/supplier evidence, PSP compliance queue | Prepaid cases | Trade finance/PSP partners | High | Compliance/legal sensitivity | Evidence lane |
| 9 | Payment Fraud Recall Evidence Desk | SMEs hit by authorised push payment fraud | Need recall/escalation evidence | Bank/police/recipient-bank packet | Case authorization | Accountants/legal-adjacent | High pain | Legal/fraud complexity | Case lane |
| 10 | Card Chargeback Representment Current-Case Lane | Hotels/ecommerce/gyms | Chargeback losses | Merchant/acquirer authorization, current disputes | Prepaid current disputes | Acquirers/agencies | Medium | Established tools/services | Case lane |
| 11 | Scheme Fee Overcharge Claim Review | PSPs/merchants | Card/acquirer fees incorrect | Merchant statements, acquirer acknowledgement | Assignment/mandate | Payment consultants | Medium | Data/legal complexity | Claim lane |
| 12 | Marketplace Payout Reserve Release Lane | Sellers | Payouts held | Seller authorization, current cases | Prepaid holds | Ecommerce accountants | High | Platform discretion/fraud risk | Case lane |
| 13 | PSP Onboarding KYC Evidence Pack | SMEs/marketplaces | Payment provider onboarding blocked | Customer docs, PSP case flow | Prepaid onboardings | Agencies/accountants | Medium | KYC/fraud legal risk | Case lane |
| 14 | Bank Account Switch Direct Debit Continuity Desk | SMEs | Bank switch breaks collections | Mandate/payment schedule, bank letters | Customer consents | Accountants | Low-medium | Commodity admin | Payment book |
| 15 | Open Banking API Access Renewal Evidence Pack | Fintechs/TPPs | Bank API access/certificate renewal | TPP certificates, bank ticket flow | Prepaid renewal cases | Fintech consultants | Medium | Technical trust, regulated | Evidence lane |
| 16 | PSD2 SCA Exemption Evidence Lane | Merchants/acquirers | 3DS/SCA exemption declines | Acquirer cases, transaction evidence | Prepaid cases | PSP/acquirer partners | Medium | Acquirers own rail | Evidence lane |
| 17 | Confirmation-of-Payee Supplier Cleanup Book | UK exporters/AP teams | CoP warnings block payments | Supplier confirmations and AP file | Prepaid batches | UK accountants | Medium | Geography/competition | Data book |
| 18 | Bank API Certificate Expiry Rescue Lane | Fintechs/ERPs | Certificates expire, payment flows fail | Current expiry cases, vendor channel | Prepaid cases | Fintech/MSP partners | Medium | Technical narrowness | Case lane |
| 19 | E-invoicing Payment Reference Matching Lane | Corporates | Payment reconciliation errors | Customer data, bank statement mapping | Prepaid batches | ERP/accounting partners | Medium | Generic reconciliation | Data lane |
| 20 | Payment Service Bureau Error-Queue Buyout | Small payment bureaus | Error backlog after regulation changes | Current error queue, customer authorizations, payment split | Prepaid queue access | Retiring/overloaded bureaus | Medium-high | Bureau/provider owns scarce trust | Queue book |
| 21 | Supplier IBAN Fraud Callback Verification Desk | SMEs/AP teams | Vendor bank change fraud risk | Supplier callback evidence, AP approval | Prepaid current changes | Accountants/ERP partners | Medium | Manual service/copyable | Evidence lane |
| 22 | Treasury Beneficiary Master File Remediation Sprint | Mid-market corporates | VoP/CoP warnings create payment delays | Master file export, supplier confirmations | Prepaid sprint | Treasury advisors | Medium | Consulting, no recurring control | Data lane |
| 23 | Bank Payment Investigation Claim Lane | SMEs | SEPA transfer missing/returned | Bank acknowledgment, customer mandate | Prepaid cases | Accountants | Low-medium | Bank ops opaque | Case lane |
| 24 | Cross-Border Payment Trace Packet | Importers/exporters | SWIFT/SEPA funds delayed | Bank trace evidence, supplier/buyer docs | Prepaid current traces | Trade finance advisors | Medium | Bank/provider dependency | Case lane |
| 25 | ERP Vendor Payment Format QA Pack | ERP vendors | Clients' payment exports fail after bank changes | ERP release test cases | Prepaid vendor tickets | ERP vendors | Medium-high | Vendor can hire | Evidence lane |
| 26 | Corporate Card Merchant Descriptor Cleanup Lane | SaaS/ecom | Card declines/chargebacks due descriptor confusion | Acquirer tickets, merchant evidence | Prepaid cases | PSP/acquirer partners | Medium | Acquirer owned | Case lane |
| 27 | Bank Payee Directory Data Correction Lane | PSPs | Beneficiary lookup returns wrong names | Customer/PSP correction tickets | Prepaid corrections | PSP partners | High but regulated/control uncertain | PSP owns directory | Data lane |
| 28 | Payment Batch Cutoff Capacity Desk | Corporates | Time-critical payroll/vendor runs | Reserved bureau support slots | Prepaid capacity | Payment bureaus | Medium | Capacity, not proprietary | Capacity lane |
| 29 | Virtual IBAN Reconciliation Exception Desk | Marketplaces/PSPs | Misallocated virtual-IBAN payments | PSP/accounting case flow | Prepaid cases | PSP/accounting platforms | Medium-high | PSP data access required | Case lane |
| 30 | Refund Batch Failure Release Desk | Ecommerce/accounting teams | Refund file rejected, customers angry | Payment file errors, PSP ticket lane | Prepaid cases | Ecommerce accountants | Medium | Generic ops support | Ticket lane |

## Finalists And Strict Simulated Scores

| Rank | Candidate | Simulated score | Decision | Rationale |
|---|---|---:|---|---|
| 1 | VoP Bulk Payment Exception Release Desk | 90 | Advance | Best fit because regulation creates formal payee-verification workflows, exception volume is likely operationally painful, the founder does not touch funds, and the control point is signed current exception batches plus supplier/customer confirmations. Higher willingness to pay than generic AP cleanup if targeted at payment bureaus/ERP partners with repeated cases. |
| 2 | Instant Payments PSP Acceptance Evidence Pack | 88 | Hold | Enterprise urgency is high, but it may become big-consultancy/vendor implementation work without a channel. |
| 3 | Payroll Beneficiary Name Exception Desk | 88 | Hold | Acute and clear, but payroll/employee data sensitivity and payroll-provider ownership make it harder. |
| 4 | EBICS/Host-to-Host Bank File Exception Lane | 87 | Do not real-gate | Real high-value rejections, but narrower and easier for ERP integrators to copy. |
| 5 | Sanctions-Screening False Positive Release Pack | 86 | Do not real-gate | High urgency but too compliance/legal sensitive. |
| 6 | SEPA Direct Debit Mandate Migration Lockbox | 85 | Do not real-gate | Strong payment-control idea, but more like migration operations and low moat. |

## Advance

Advance **VoP Bulk Payment Exception Release Desk** to real working-chat validation.

## Search Implication

This candidate must be framed as an exception queue and evidence/confirmation lane, not a fintech product:

- no fund custody;
- no regulated payment execution;
- no advice on whether to pay a supplier;
- partner/customer authorizes current exception batches;
- supplier confirmations and master-data corrections are documented;
- fee is paid for resolving a current operational payment block.
