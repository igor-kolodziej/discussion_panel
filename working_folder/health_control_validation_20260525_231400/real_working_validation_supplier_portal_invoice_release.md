# Real Working-Chat Validation: SupplierPortal Invoice Release Desk

## Gate

- Round: 312
- Simulated score: 88.2
- Working Zero To One score: 84
- Lowered real gate: >=85
- Decision: FAIL

## Prompt Hygiene

- Prompt file: `zero_to_one_prompt_supplier_portal_invoice_release.txt`
- `rg` check for forbidden validation/cap language: clean
- Browser composer check before send:
  - clean start: yes
  - idea fields present: yes
  - forbidden validation/cap language: no

## Zero To One Summary

Zero To One treated the idea as a cross-portal payment-release desk rather than generic AR outsourcing. It saw strong cash-linked pain because the supplier has already earned the money and large enterprise portals can block PO-flip, invoice submission, invoice acceptance, payment status, vendor onboarding, and customer-specific setup. It scored the idea 84 because the opportunity is practical and commercially attractive, but the moat is not strong enough unless intake stays brutally narrow.

## Strongest Objections

1. The business can become ordinary AR outsourcing if it accepts vague overdue invoices, buyer cash-management delays, weak relationship ownership, or commercial disputes.
2. Supplier finance teams, controllers, AR teams, accountants, customer-success teams, ERP consultants, EDI consultants, and export admins can often solve buyer-portal issues.
3. Buyer AP teams may ignore third parties and only work through authorized supplier contacts or portal tickets.
4. Apparent portal blockers may hide real disputes: PO mismatch, missing goods receipt, service-entry gaps, delivery proof, quality rejection, tax-form issues, bank fraud review, sanctions screening, or buyer insolvency.
5. Portal variation is high across Ariba, SAP Business Network, Coupa, Oracle, custom portals, EDI flows, and AP ticket systems.
6. Success fees risk crossing into collections if the case is not strictly an acknowledged-payable process-state release.
7. Small invoices cannot support the fee; the invoice queue should usually exceed 100,000 PLN.
8. Trust friction is real because the startup would handle bank verification, tax forms, company records, invoices, EDI logs, portal admin rights, and buyer contact trails.
9. Large buyers may still be slow even after the process state clears, so AP acceptance or scheduled remittance may be a more realistic outcome than immediate cash.
10. Consultants can copy the checklist; the defensibility is active case control, turnaround, buyer/portal memory, and partner channels, not a unique method.

## Evaluator Advice

The viable beachhead is CEE suppliers selling to large multinational, industrial, retail, telecom, university, hospital, defense-prime, or public-sector-adjacent customers where payment is blocked by Ariba, Coupa, SAP Business Network, vendor-master, EDI, PO-flip, or AP portal state. Accept only cases with a named customer, written blocker, acknowledged payable, material invoice queue, supplier officer authorization, portal/ticket path, bank/tax/company evidence, and delivery or service acceptance where relevant. Reject normal collections and every disputed or legally ambiguous case.

## Lesson

The current-cash direction is better than evidence-only work, but broad "approved invoice portal release" still caps below the gate because finance, ERP, EDI, and AR operators can copy it and because the work can degrade into collections. Round 313 should keep current cash but add a sharper, less generic control point than enterprise AP process chasing.
