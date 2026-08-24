# Real Working Validation: KSeF Invoice Payment Release Desk

Date: 2026-05-29
Gate: working-chat Zero To One score >=85
Result: FAIL

## Score

79 / 100

## Prompt Validated

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_ksef_invoice_payment_release_desk.txt`

## Evaluator Summary

The evaluator considered this a strong current-cash release idea because it is tied to unpaid AR rather than generic KSeF readiness. It recognized the timing as strong because Poland's mandatory KSeF rollout is active in 2026 and receiving invoices through KSeF is mandatory from 1 February 2026.

The idea still did not clear the gate because many cases can be solved by accountants, ERP providers, or KSeF software vendors, and some apparent KSeF payment holds will actually be buyer bureaucracy, commercial disputes, insolvency, or poor ERP implementation.

## Strongest Objections

1. Accountants and ERP vendors may already solve many cases directly when the blocker is a missing KSeF number, XML export, or correction workflow.
2. Some AP holds will be fake KSeF problems: buyer cash-flow delay, commercial dispute, delivery dispute, quality issue, insolvency, internal bureaucracy, or PO/GRN mismatch unrelated to KSeF.
3. Legal, tax, and accounting boundaries are sensitive because invoice corrections, VAT treatment, KSeF submission, invoice content, and split payment remain official tax/accounting matters.
4. Buyer AP may refuse to engage with an outside coordinator, especially large enterprises, municipalities, and shared-service centers.
5. Some cases will require ERP implementation rather than invoice-batch release, destroying the 4k-18k PLN case economics.
6. Trust and data access are hard because the desk needs invoices, XML, buyer references, PO/GRN data, vendor-master data, bank details, and sometimes contracts or acceptance documents.
7. The pain may fade after the rollout normalizes in 2027 unless the business expands into broader invoice acceptance/payment-release memory.
8. Pricing must be tied to AR value; small invoices will not support the fee.
9. Success fees may be awkward and should not be central to the model.
10. The precise trigger must remain named unpaid AR blocked by buyer AP/KSeF acceptance, not generic readiness or debt collection.

## Gate Decision

Fails the working-chat real gate: 79 is below the required 85.

Do not fresh-validate. Continue at Round 133.
