# Real Working-Chat Validation: FactorReserve Settled-Debtor Holdback Release Lockbox

Date: 2026-05-30 Europe/Warsaw

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_factor_reserve_release_lockbox.txt`

Working chat: Zero To One

## Result

Working Zero To One score: **75 / 100**

Gate decision: **Fail**. The working score is below the current `>=85` real gate. Do not fresh-validate.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and did not include internal scoring caps, evaluator instructions, real-gate language, or working-chat language. The browser composer was verified empty before fill and verified to contain `FactorReserve Settled-Debtor Holdback Release Lockbox` before submission.

## Zero To One Summary

Zero To One treated this as a strong cash-release recovery idea and said the mechanism is real: factors commonly advance part of an invoice and keep the remainder in reserve until debtor payment and settlement conditions allow release. It credited the narrow boundary: only accept cases where debtor payment has arrived or the contractual release window is mature, and where the factor ledger supports a specific release request.

The score stayed at **75** because clean matured reserves may be rare. Factors often auto-release clean balances, and leftover cases may involve valid offsets, recourse exposure, cross-collateral rights, unpaid invoices, fees, disputes, insolvency risk, or contractual setoff rights. The signed mandate controls a file, but not the factor's decision or the broader reserve logic.

## Strongest Objections Captured

1. Clean matured reserves may be rarer than expected because competent factors usually auto-release them.
2. Leftover reserves may be held for valid reasons: unpaid invoices, debtor deductions, recourse exposure, disputes, cross-collateral, fees, interest, tax/legal offsets, or future claims.
3. Factoring contracts may allow broad setoff rights, so debtor payment does not automatically mean reserve release.
4. Recourse factoring may justify portfolio-wide or facility-wide holdbacks even when a named invoice has been paid.
5. Factors may ignore a third-party coordinator and require the SME or registered broker to handle communication.
6. The work can become low-margin reconciliation across partial payments, credit notes, FX, fees, insurance, deductions, and rolling reserves.
7. Factoring brokers and accountants are good channels but can internalize the checklist.
8. Sensitive factoring agreements, debtor lists, invoice ledgers, bank data, and disputes create trust friction for an unknown founder.
9. Distressed SMEs may bring adverse-selection cases involving insolvency, tax arrears, fraud flags, sanctions/export issues, or recourse defaults.
10. Success-fee attribution can be disputed if the factor was already scheduled to sweep the reserve.

## Useful Narrowing

Best beachhead:

SMEs using recourse factoring or invoice discounting with high invoice volume and weak reconciliation, especially transport, staffing, wholesale, light manufacturing, and export suppliers.

Accept only cases with factoring agreement, factor statements or portal exports, named reserve/holdback ledger, debtor payment evidence, invoice list, no active debtor dispute, no fraud/sanctions/insolvency issue, clear authority, and candidate release above 75,000 PLN.

Reject debtor payment not received, live debtor disputes, factor fraud concerns, recourse defaults, tax/legal offsets, insolvency situations, PSP/acquirer reserves, marketplace holds, missing factor statements, and cases requiring legal interpretation before a basic release request.

## Gate Decision

Fail. Do not fresh-validate.

## Lesson For Next Round

Cash held by a finance counterparty is still not enough when the clean cases may already auto-release and the remaining cases are likely valid holdbacks or legal/credit risk. The next candidate needs either a stronger first-party payment direction, a pre-controlled current transaction stream, or a less discretionary counterparty than a factor.
