# Real Working-Chat Validation: ServiceEntry Pay-Release Desk

Date: 2026-05-31 Europe/Warsaw

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_service_entry_pay_release.txt`

Working chat: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a1acbea-f194-83eb-b868-d5e50d4ceeee`

## Gate Result

- Simulated score: **88.1 / 100**
- Working-chat Zero To One score: **87 / 100**
- Required working-chat score: **>=85**
- Gate decision: **PASS**

Submit the exact same prompt wording to a fresh Zero To One chat.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and contained no internal scoring caps, evaluator instructions, working-chat language, fresh-chat language, or gate language. Browser composer verification before send:

- `cleanStart: true`
- `hasForbidden: false`
- prompt length: about 9,718 characters
- idea name present: `ServiceEntry Pay-Release Desk`

## Zero To One Summary

Zero To One scored the idea **87 / 100** and called it a strong payment-release wedge. It judged the concept materially sharper than the broader SupplierPortal Invoice Release Desk because it targets one specific high-value enterprise AP blocker: a missing or rejected service-entry sheet, goods receipt, work confirmation, completion record, or PO-line acceptance state.

The evaluator accepted that the pain is real in SAP-style service procurement: services are recorded against a PO, and invoice/payment processing can depend on accepted service-entry status. It also accepted the startup's narrower positioning: the invoice is not broadly "unpaid"; it is trapped behind a named internal acceptance state in the buyer's procurement/AP system.

## Strongest Objections Captured

1. Many suppliers should already chase this through project managers, service coordinators, AR staff, or account owners.
2. Some blockers are actually performance disputes, incomplete work, punch-list items, safety documentation, missing reports, unapproved change orders, penalties, or refusal to certify completion.
3. Buyer approvers control the outcome, so the startup can assemble the route and packet but cannot force acceptance.
4. Enterprise AP may ignore third parties, so the desk must work through supplier-authorized channels and registered portal contacts.
5. ERP and portal variation is high across SAP service-entry sheets, Ariba service sheets, Coupa, Oracle, customer-built portals, and email-based loops.
6. Success fees create collections/legal boundary risk unless attribution is explicit.
7. Small invoices do not work; the queue should usually be at least around 150,000 PLN.
8. False completion evidence is a hard risk; the desk must never create, alter, backdate, or imply work completion.
9. Suppliers may internalize once they see the packet, so durability depends on buyer-specific memory, repeat channels, and multi-buyer complexity.
10. It can drift into generic AR outsourcing unless every case starts with written buyer text identifying the specific SES/GR/work-confirmation/acceptance blocker.

## Useful Narrowing

Best beachhead:

- industrial service;
- maintenance;
- field service;
- shutdown work;
- automation;
- engineering;
- facilities suppliers selling to large SAP/Ariba/Coupa/Oracle-using enterprise buyers.

Accept only cases with:

- named enterprise buyer;
- named PO/work order;
- invoice queue above 150,000 PLN preferred;
- written buyer blocker text;
- service-entry, goods-receipt, work-confirmation, or PO-line acceptance issue;
- existing truthful completion evidence;
- customer requester or approver map;
- AP ticket or portal trail;
- prepaid fixed fee.

Reject:

- no written buyer blocker;
- disputed performance;
- missing delivery;
- unresolved site defects;
- price dispute;
- change-order dispute;
- penalty dispute;
- tax/legal issue;
- fraud review;
- buyer insolvency;
- ordinary late payment.

## POC Correction From Evaluator

60 days:

- 4-6 prepaid cases;
- 1,000,000-2,000,000 PLN unpaid invoice value under mandate;
- 3-4 objective outcomes: accepted SES/GR/work confirmation, invoice acceptance, payment schedule, remittance, narrowed follow-up, or clean no-go;
- 50,000-110,000 PLN collected;
- 40%+ rejection log.

6 months:

- 20-45 cases;
- 6,000,000-20,000,000 PLN invoice value under mandate;
- 15-25 objective outcomes;
- 220,000-750,000 PLN revenue;
- 3-5 repeat channels;
- gross margin above 60%.

## Gate Decision

Pass working gate. The working score is **87**, above the required `>=85`. Proceed to fresh validation with the exact same prompt.
