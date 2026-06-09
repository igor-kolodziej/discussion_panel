# Real Working-Chat Validation: StayLedger OTA Settlement Recovery Mandate

Date: 2026-05-29
Gate: working Zero To One score must be >=85

## Score

76 / 100

## Gate Decision

FAIL. The idea does not pass the working-chat real validation gate.

## Exact Prompt File

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_stayledger_ota_settlement_recovery.txt`

## Zero To One Summary

The evaluator called this a credible current-cash recovery mandate with a real reconciliation surface across OTA bookings, PMS folios, virtual cards, commission invoices, cancellations, refunds, acquirer files, and bank/card settlements. It liked the signed recovery mandate, claim IDs, VCC recovery queue, and first-proof-as-cash structure.

The score stayed far below the gate because many apparent leakage items may be valid OTA charges, hotel-caused process failures, PMS mapping issues, missed no-show markings, missed VCC windows, tax/fee setup problems, or front-desk undercollection. Those defects can be operationally useful but may not convert into OTA credits or success-fee recovery.

## Strongest Objections

1. Many suspected errors will be valid OTA commission, cancellation, no-show, refund, tax, or VCC outcomes.
2. Hotels may have caused the leakage through missed no-show markings, wrong VCC charges, expired VCC windows, incorrect folios, or tax/fee misconfiguration.
3. OTA support can be slow and opaque, hurting cash conversion.
4. Revenue managers, controllers, hotel accountants, PMS consultants, channel-manager vendors, and OTA account managers already touch parts of the workflow.
5. Data exports will be messy across OTA, PMS, acquirer, bank, refund, chargeback, and tax/fee systems.
6. Success-fee triggers are hard to define for prevented overpayments.
7. Small hotels may not justify the fee; the first niche needs high OTA volume or multi-property groups.
8. VCC recovery windows may already be missed.
9. Hotels may fear relationship damage with Booking.com, Expedia, Agoda, or other OTAs.
10. The business can become generic hotel finance cleanup unless the mandate rejects PMS cleanup, tax setup, guest disputes, and process-failure repair.

## Evaluator's Best Beachhead

Independent hotels and small groups with high Booking.com, Expedia, and Agoda volume and weak finance operations.

Minimum filters:

- 50+ rooms or a multi-property group;
- OTA gross booking value above 500,000 PLN in the scoped period;
- PMS, OTA, and acquirer exports available;
- a current commission invoice, VCC issue, cancellation/no-show adjustment, refund reversal, or chargeback queue;
- hotel-approved claim drafts;
- no legal, tax, or guest dispute as the main issue.

## POC Pass/Fail Suggested By Evaluator

Continue only if within 60 days:

- 5 mandates are signed;
- at least 1,500 OTA reservations are processed;
- at least 40,000 PLN plausible leakage is identified;
- at least one recovery or invoice reduction is accepted;
- at least 15,000 PLN fees are collected.

By 6 months, continue only if:

- confirmed recovery or prevention exceeds 150,000 PLN;
- at least five hotels or two groups repeat;
- gross margin stays above 60%;
- at least 30% of identified leakage becomes confirmed recovery/prevention;
- data extraction time falls materially after templates stabilize.

If those pass, the evaluator estimated the score rises only to 81-83.

## Lesson

Cash-recovery mandates still fail when the recoverable pool is ambiguous. The next candidate needs a live economic gate where the buyer's current tender, renewal, order, listing, or payment is explicitly blocked by an external requirement, not merely suspected leakage inside messy operations.
