# Real Working-Chat Validation: SEPA Direct-Debit Collection Rescue Lockbox

Date: 2026-05-31 Europe/Warsaw

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_sepa_mandate_collection_rescue.txt`

Working chat: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a1c1e39-66bc-83eb-8107-6bbfda9ce1fa`

## Gate Result

- Simulated score: **88.3 / 100**
- Working-chat Zero To One score: **61 / 100**
- Required working score: **>=85**
- Gate decision: **FAIL**

Do not fresh-validate.

## Prompt Hygiene

The submitted prompt used the clean required opening and did not include internal scoring caps, evaluator instructions, real-gate language, working-chat language, or fresh-chat language.

Browser composer verification before send:

- Clean start: true.
- Idea name present: true.
- Forbidden scoring-instruction terms: false.
- Textbox was empty before fill.

## Zero To One Summary

Zero To One treated the pain as real: failed SEPA Direct Debit cycles can create immediate cash-flow issues, support tickets, manual collection work, and payer confusion. It agreed the idea is commercially plausible when the problem is a specific technical or process continuity failure such as mandate-reference mapping, creditor-ID migration, PSP shutdown, failed file format, or billing-system cutover.

The score stayed at **61** because the broad version is weaker than AP/payment-release ideas. The buyer pool is narrower than framed, repeatable access to crises is hard, and many failed SEPA Direct Debit collections are not externally rescuable before the next collection run.

## Strongest Objections Captured

1. Many failures are not fixable rescue cases; they are ordinary insufficient funds, cancelled mandates, invalid mandates, debtor refusals, closed accounts, blocked accounts, or payer-side bank issues.
2. The customer can reverse SDD Core payments after settlement, so a first successful batch is not final retained cash.
3. PSPs, banks, billing platforms, accountants, and internal finance teams are natural owners and already have system access and trust.
4. Trust friction is severe because the workflow touches mandate registers, IBANs or bank-account references, payer names, return-code ledgers, collection files, customer notices, PSP acknowledgements, and settlement reports.
5. Re-consent or payer notice work may take longer than the next monthly collection deadline.
6. Success-fee attribution will be disputed if the PSP, internal finance team, or scheduled retry appears to have fixed the batch anyway.
7. The market is less universal than framed; SEPA Direct Debit is not the default recurring consumer payment rail in every target country, especially for many Polish local businesses.
8. Part-time execution is a weak fit for live payment-cycle rescue because the window is operationally unforgiving.
9. Demand is episodic around migrations and incidents, not obviously recurring.
10. The startup has no strong local advantage unless it targets businesses collecting EUR by SEPA Direct Debit in markets where SDD is common.

## Useful Narrowing From Evaluator

Best narrowed version:

**SEPA Mandate Migration Rescue Desk** for businesses with 500-5,000 active SEPA mandates, monthly EUR collections above EUR 50,000, and an active PSP/billing migration or creditor-ID/mandate-reference mapping problem before the next monthly run.

Even that version is an emergency operations niche unless it becomes ongoing collection-quality infrastructure through trusted PSP, billing-platform, accountant, or implementer channels.

## Gate Decision

Fail. Working score **61 / 100** is below the current real working-chat gate of **>=85**.

## Lesson

A current payment stream is not enough if the natural owner is the PSP/bank/billing platform, the founder must borrow urgent trust for sensitive payment data, and most failures are not cleanly fixable by an outside operator. Do not continue direct-debit or payment-file rescue variants unless the founder already controls a trusted channel or a repeated paid migration queue.
