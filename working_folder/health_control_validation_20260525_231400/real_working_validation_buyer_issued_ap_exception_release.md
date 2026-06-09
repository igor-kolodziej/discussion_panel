# Real Working Validation - Round 331

## Candidate

ExceptionPay Buyer-Issued AP Release Lockbox

## Gate

- Simulated score: 88.1
- Working Zero To One score: 84
- Active working gate: >=85
- Decision: FAIL

## Zero To One Summary

Zero To One treated this as a strong payment-release desk and credited the buyer-issued written exception rule. It said the core pain is real: enterprise AP systems frequently block payment because a required workflow state or artifact is missing.

The score stopped at 84 because the prompt remained slightly over-broad. The evaluator said it is weaker than the prior ServiceEntry Pay-Release Desk because "AP exception" can become a generic AR/portal bucket. The best version starts with only two clean exception families.

## Strongest Objections

- It can become generic AR chasing if it accepts vague overdue invoices.
- Many "exceptions" hide delivery disputes, tax errors, sanctions/UBO review, fraud controls, goods-receipt mismatch, bank-change risk, customer cash delay, or buyer-side bureaucracy.
- Buyer AP may ignore third parties, so the startup must operate behind the supplier's authorized billing/procurement contact.
- Bank-validation and vendor-master payment-change cases are dangerous and should be rejected at the start.
- Portal variation across Ariba, Coupa, SAP Business Network, Oracle, EDI, and custom portals can make delivery manual.
- Supplier AR teams, accountants, ERP consultants, EDI consultants, procurement-onboarding specialists, customer-success teams, and buyer AP teams can solve pieces.
- Success-fee attribution is fragile unless before-state exception text and after-state buyer acknowledgement prove causality.
- Small invoices do not work; below 150,000 PLN blocked value the fee is often hard to justify.
- Sensitive invoices, tax forms, bank evidence, company records, portal screenshots, AP tickets, and buyer correspondence create trust friction.
- Suppliers may internalize the workflow after one buyer-specific case.

## Evaluator's Best Narrowing

Start with only:

1. Accepted invoice queues blocked by service-entry, goods-receipt, work-confirmation, or PO-line acceptance.
2. Accepted invoice queues blocked by invoice/EDI/portal-state correction.

Avoid bank-change, vendor-master payment changes, tax/legal uncertainty, sanctions/UBO review, fraud review, buyer insolvency, price disputes, PO exhaustion, quality/performance disputes, and any case where the buyer has not acknowledged a processable payable.

Corrected 60-day proof:

- 4-5 paid mandates.
- 1m-2m PLN invoice value under mandate.
- 3 buyer acknowledgements or exception-cleared outcomes.
- 1-2 scheduled remittances/payments/no-go outcomes.
- 40,000-100,000 PLN collected.

## Gate Decision

Do not fresh-validate. Continue to Round 332 with the narrowed clean exception families only.
