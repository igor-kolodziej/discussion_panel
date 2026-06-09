# Real Working-Chat Validation: FactorableInvoice Acceptance Release Desk

## Gate

- Round: 314
- Simulated score: 88.3
- Working Zero To One score: 83
- Lowered real gate: >=85
- Decision: FAIL

## Prompt Hygiene

- Prompt file: `zero_to_one_prompt_factorable_invoice_acceptance_release.txt`
- `rg` check for forbidden validation/cap language: clean
- Browser composer check before send:
  - clean start: yes
  - idea fields present: yes
  - forbidden validation/cap language: no

## Zero To One Summary

Zero To One saw the written factor/lender deficiency as a useful sharpening device because it proves the invoice is blocked from funding for a specific evidence reason rather than simply unpaid. It still scored the idea 83 because factors already verify invoices, many deficiencies are really credit decisions, and the boundaries around collections, credit brokerage, assignment, and underwriting are fragile.

## Strongest Objections

1. Factors and invoice-finance providers already verify invoices directly with debtors.
2. "Missing evidence" may be a cover for credit limit, concentration cap, debtor history, invoice age, contra/setoff, recourse risk, or underwriting discretion.
3. Debtor AP teams may ignore third parties or require documents directly from the supplier/factor.
4. Assignment-notice issues can become legal if the debtor disputes assignment, payment direction, prohibitions on assignment, or contract terms.
5. Success fees can create regulatory or boundary risk if they look like credit brokerage or collections.
6. The idea overlaps with SupplierPortal Invoice Release unless the written trigger comes from a factor/lender/platform and the outcome is funding eligibility.
7. Suppliers may be cash-stressed and disorganized, lacking PO, delivery, service-entry, GRN, EDI, portal, or debtor-contact evidence.
8. Some factors may reject third-party involvement.
9. Fraud/fake-invoice risk is high in invoice finance; any pressure to make a weak invoice fundable is a hard reject.
10. The desk can degrade into AR outsourcing unless every case starts with a written factor deficiency, named invoice schedule, specific evidence condition, and material funding value.

## Evaluator Advice

The viable beachhead is factoring brokers and invoice-finance advisers serving CEE suppliers with named invoices excluded only because debtor acceptance evidence is missing. Accept only cases with a written factor/lender/platform deficiency, named invoice schedule, invoice value above 150,000 PLN preferred, supplier mandate, debtor acknowledgement path, PO/contract reference, goods receipt/service entry/EDI/portal evidence route, factor submission trail, no-dispute screen, and prepaid fee. Reject debtor disputes, concentration/credit-limit issues, underwriting discretion, insolvency, assignment disputes, tax/legal questions, fraud review, missing delivery proof, customer refusal to acknowledge payable, and generic AR chasing.

## Lesson

Adding a factor gate improved clarity but not enough. The broader invoice-finance and AP-release family remains below the real gate because incumbents already verify receivables and because legal/collections/funding boundaries are fragile. Do not continue finance-release variants unless the control point includes a materially stronger external mandate or owned payment stream.
