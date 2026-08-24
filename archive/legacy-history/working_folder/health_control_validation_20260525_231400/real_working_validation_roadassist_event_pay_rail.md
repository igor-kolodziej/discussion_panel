# Real Working-Chat Validation: RoadAssist Event Pay Rail

Date: 2026-05-31 Europe/Warsaw

Prompt file:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_roadassist_event_pay_rail.txt`

Simulated file:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_328_roadassist_event_pay_rail.md`

## Gate Result

- Simulated score: **88.1 / 100**
- Working-chat Zero To One score: **77 / 100**
- Required working-chat score: **>=85**
- Gate decision: **FAIL**

No fresh-chat validation was submitted.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and did not include internal scoring caps, evaluator instructions, working-chat language, fresh-chat language, or gate language. Browser composer verification before send:

- `cleanStart: true`
- `includesIdea: true`
- `hasForbidden: false`
- prompt length in composer: about 9,580 characters

## Zero To One Summary

Zero To One scored the idea **77 / 100**. It accepted the core pain: roadside/towing contractors can lose money through evidence-based invoice rejections, holds, underpayments, chargebacks, storage-day disputes, distance disputes, and correction loops. It said the strongest version is not another dispatch tool but a payor-specific invoice acceptance rail for contractors with a named insurer, assistance-network, fleet, or leasing payor.

The score stayed below gate because the idea is too close to existing roadside/towing dispatch and field-service software. The evaluator cited existing platforms with GPS tracking, mobile driver apps, photos, job status, signatures, dispatching, invoicing, and reporting. The wedge only survives if it is narrowly positioned around reducing rejections for a named payor workflow.

## Strongest Objections Captured

1. Existing towing/roadside platforms already capture dispatch, GPS, mobile workflow, photos, status, signatures, billing, invoicing, and reporting.
2. Payors may force their own app, portal fields, photos, timestamps, service codes, and upload routes.
3. Driver adoption is difficult; missed live photos/signatures/timestamps cannot be reconstructed later.
4. Many rejections are valid: wrong tariff, missed authorization, uncovered policy, unapproved extra service, late submission, inflated storage, excessive distance, wrong service code, or dispatch mismatch.
5. Value per event may be too low if manual QA, WhatsApp chasing, OCR, and invoice-line correction are frequent.
6. Towing and roadside contractors may be low-margin and chaotic, making setup-fee conversion hard.
7. Payor cooperation is uncertain; payors may communicate only through established portals.
8. The business can become generic field-service software if it builds dispatch, routing, GPS, billing, and invoicing.
9. Vehicle plates, locations, customer/driver signoffs, photos, job IDs, invoices, and storage records create privacy and fraud-control burden.
10. Large assistance networks can mandate their own evidence app if the issue is large.

## Evaluator's Better Version

Best beachhead:

**Roadside/towing contractors with 300+ monthly insurer/assistance/fleet jobs and one named payor causing repeated evidence-based invoice rejections or underpayments.**

Accept only cases where the contractor can show:

- named payor;
- job volume;
- recent rejection, hold, chargeback, correction, or underpayment examples;
- payor evidence requirements;
- driver adoption owner;
- invoice-line mapping;
- prepaid 30-day pilot fee;
- before/after rejection baseline.

Reject:

- low-volume contractors;
- general dispatch needs;
- no evidence of payor rejections;
- personal-injury or accident-liability cases;
- storage/legal disputes;
- fraud flags;
- no driver adoption commitment;
- cases where payor requires its own app exclusively.

## POC Correction

The evaluator said proof should focus on before/after rejection reduction:

- 1-2 contractors;
- 1 named payor workflow each;
- 100-200 live events captured;
- 50-100 payor-ready packets;
- baseline rejection/underpayment rate documented;
- 2-3 payor or contractor acceptance outcomes;
- 15,000-45,000 PLN collected.

Six-month proof:

- 5-10 contractors or 2-3 contractor groups;
- 1,500-5,000 events captured;
- 1,000+ packets submitted;
- 2-3 payor-specific playbooks;
- 100,000-300,000 PLN revenue;
- demonstrated rejection/chargeback reduction for at least two payor workflows;
- gross margin above 60%.

## Gate Decision

Fail. Working score is below `>=85`; do not fresh-validate.

## Lesson

Live event rails still fail when existing vertical software already claims most of the capture layer. Future event/payment candidates need a stronger control point than field evidence capture, or a domain where incumbent systems cannot already impose the same workflow.
