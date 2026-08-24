# Real Working-Chat Validation: OriginLock Amazon EU/UK COO Restriction Release Desk

Date: 2026-05-31 Europe/Warsaw

Prompt file:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_amazon_coo_restriction_release.txt`

Working chat:

`https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a1acbea-f194-83eb-b868-d5e50d4ceeee`

## Result

- Simulated score: **88.1 / 100**
- Working Zero To One score: **79 / 100**
- Required working gate: **>=85**
- Gate decision: **FAIL**

Do not fresh-validate.

## Prompt Hygiene

The prompt used the clean Zero To One opening:

```text
Score this business idea 0-100 and include strongest objections.
```

The submitted prompt did not include internal scoring caps, evaluator instructions, working-chat language, fresh-chat language, or real-gate language.

Browser composer verification before send:

- `cleanStart: true`
- `includesIdea: true`
- `hasForbidden: false`
- prompt length: about `8,924` characters in the composer

## Zero To One Summary

Zero To One scored the idea **79 / 100**.

It treated the idea as an Amazon-specific listing-risk release desk, not customs-origin advisory. It accepted that the pain is real: Amazon EU/UK requires country-of-origin information at listing/SKU level, and sellers can face blocked new listings, locked edits, compliance notices, or cross-border listing restriction risk when COO is missing.

The evaluator liked the narrowest version:

> "Send the Seller Central COO notice, ASIN/SKU batch, and source documents. We return a truthful SKU-origin ledger, upload file, case chronology, accepted/narrowed status, or no-submit list."

The score stayed below gate because routine COO fixes are often simple bulk-upload work, agencies and VAs can copy the process quickly, and true origin determination can become unsafe customs/legal work.

## Strongest Objections Captured

1. Routine updates are too easy: many cases are just Manage All Inventory edits, inventory reports, or upload-file work.
2. Amazon agencies, catalog VAs, VAT/EPR advisers, compliance firms, and seller-ops teams can copy the workflow quickly.
3. True country-of-origin determination can become customs-law work involving substantial transformation, preferential origin, tariff treatment, or origin-label legality.
4. Source documents may be weak or fail to tie cleanly to exact SKUs, variants, bundles, private-label packaging, or supplier changes.
5. Amazon catalog locks can be frustrating; some rows may require brand-owner paths, delete/relist, or support escalation.
6. Amazon response quality is outside founder control.
7. Enforcement may normalize after sellers update catalogs, reducing urgency.
8. Low-value sellers will use a VA, not pay 8,000-25,000 PLN.
9. Direct acquisition may attract sellers seeking shortcuts or false origin submissions.
10. No-submit decisions are commercially hard because sellers may dislike paying for a refusal to submit unsupported origin data.

## Useful Narrowing From Evaluator

Best beachhead:

Amazon EU/UK account-health and seller-operations agencies with clients receiving COO notices or compliance-dashboard queues across 100-500+ SKU batches.

Accept only cases with:

- written Amazon notice, dashboard flag, case ID, upload queue, or listing restriction risk;
- named ASIN/SKU batch;
- revenue or inventory value at risk;
- seller mandate;
- source documents tied to SKUs;
- agency or seller approval path;
- no-submit authority;
- prepaid fixed fee.

Reject:

- no written Amazon notice;
- generic catalog cleanup;
- low-value SKU rows;
- unsupported origin;
- legally ambiguous origin;
- fake documents;
- sanctions, counterfeit, or product-safety issues;
- preferential-origin or customs-duty questions;
- requests to invent COO.

## POC Correction From Evaluator

60 days:

- 1 agency-routed batch or 2 direct serious batches;
- 100-500 ASIN/SKU rows;
- 50,000 PLN inventory or 100,000 PLN monthly GMV at risk;
- 1 accepted update, narrowed follow-up, restriction avoided/released, or clean no-submit outcome;
- 15,000-60,000 PLN collected.

6 months:

- 6-12 paid batches;
- 1,000-5,000 rows processed;
- 80,000-300,000 PLN revenue;
- 2-3 agency channels;
- 5+ accepted, narrowed, released, or no-submit outcomes;
- gross margin above 60%.

## Gate Decision

Fail. Working score **79 / 100** is below the current real working-chat gate of **>=85**, so this does not advance to fresh validation.

## Lesson

Do not continue Amazon COO variants. The live notice and SKU-level proof are real, but the evaluator capped the idea because routine cases are too easy, agencies/VAs can internalize, and hard cases require customs-origin judgment outside the founder's safe scope.

Future rounds should avoid generic Amazon attribute/compliance cleanup unless the founder controls a stronger paid case book, recovered cash stream, or category-specific proof object that agencies cannot internalize after a few batches.

