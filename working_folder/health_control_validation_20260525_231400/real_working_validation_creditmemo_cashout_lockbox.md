# Real Working-Chat Validation: CreditMemo Cash-Out Lockbox

Date: 2026-05-30 Europe/Warsaw

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_creditmemo_cashout_lockbox.txt`

Working chat: Zero To One

## Result

Working Zero To One score: **79 / 100**

Gate decision: **Fail**. The working score is below the current `>=85` real gate. Do not fresh-validate.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and did not include internal scoring caps, evaluator instructions, real-gate language, or working-chat language. The browser composer was verified empty before fill and verified to contain `CreditMemo Cash-Out Lockbox` before submission.

## Zero To One Summary

Zero To One called this a strong cash-release recovery idea with a clean trigger: the vendor has already issued a credit memo, refund notice, unapplied-cash line, or account statement balance. It viewed the idea as safer and more concrete than speculative AP audit or supplier-overbilling claims.

Best framing:

**Cash out acknowledged supplier credits, unapplied balances, refund statements, and closed-account credits for SMEs and PE-backed groups.**

The score stayed at **79** because AP recovery firms and vendor statement reconciliation already exist, many balances will be too small, and many vendors will prefer offsets rather than cash refunds.

## Strongest Objections Captured

1. Vendors may prefer offsets against future purchases rather than cash refunds.
2. Clean balances may be smaller than expected; minimum balance discipline is critical.
3. AP recovery firms already search for duplicate payments, missed vendor credits, unapplied credit memos, overpayments, rebates, pricing errors, and refunds.
4. Some credits are contractually restricted, non-refundable, expired, tied to future purchases, tied to rebate terms, tied to original legal entities, or linked to return/quality disputes.
5. Old legal entities, mergers, wind-downs, and post-acquisition authority can be valuable but messy.
6. Vendor response times can be slow because refunding cash is not a priority.
7. Success-fee attribution can be disputed if AP cleanup was already underway.
8. The business can become low-margin statement chasing if intake accepts vague AP ledgers or missing vendor acknowledgement.
9. CFOs may be embarrassed by messy AP unless pitched as post-close, post-migration, or portfolio cash cleanup.
10. Offset valuation can be contentious unless the buyer specifically approves it.

## Useful Narrowing

Best beachhead:

PE portfolio companies, multi-entity SMEs, ecommerce brands, industrial distributors, and site-closure situations with acknowledged vendor credits above 150,000 PLN total.

Accept only vendor-issued credit memo, vendor statement balance, refund notice, unapplied-cash line, deposit statement, closed-account balance, clear buyer entity authority, no open dispute, and minimum balance threshold.

Reject speculative overbilling claims, contract disputes, tax/customs refunds, vendor insolvency, disputed returns, unclear entity ownership, low-value balances, expired/non-refundable credits, missing vendor acknowledgement, and requests to create or inflate claims.

## Gate Decision

Fail. Do not fresh-validate.

## Lesson For Next Round

Debtor acknowledgement helps, but it still caps below 85 when the workflow is a known AP recovery category and internal/AP-recovery incumbents can copy. The next candidate needs a harder, less obvious control point than "cash out acknowledged credits," ideally one where the founder controls a current payment stream or a scarce live case before the natural incumbent can normalize it.
