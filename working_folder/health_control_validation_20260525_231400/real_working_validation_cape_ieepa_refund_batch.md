# Real Working-Chat Validation: CAPE IEEPA Refund Batch Desk

Date: 2026-05-31 Europe/Warsaw

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_cape_ieepa_refund_batch.txt`

Working chat: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a1acbea-f194-83eb-b868-d5e50d4ceeee`

## Result

- Simulated score: **88.2 / 100**
- Working-chat Zero To One score: **82 / 100**
- Required working-chat score: **>=85**
- Gate decision: **FAIL**

Do not fresh-validate. Continue to Round 301.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and did not include internal scoring caps, evaluator instructions, working-chat language, fresh-chat language, or gate language. Browser composer verification before send:

```json
{
  "len": 7743,
  "cleanStart": true,
  "hasIdea": true,
  "hasForbidden": false
}
```

## Validator Summary

Zero To One scored the idea **82 / 100**.

The evaluator accepted that the core workflow is real and timely: CBP launched CAPE Phase 1 inside ACE on 20 April 2026 for IEEPA duty refunds, the refund pool is large, and the work can be operationally batchable.

It also accepted the intended boundary: the startup should prepare entry worklists, CSV batches, exception ledgers, status trackers, and refund reconciliation files while the importer of record or authorized customs broker remains the filer.

The score stayed below gate because the filing relationship, data access, and credibility sit with customs brokers, trade lawyers, freight forwarders, Big Four customs teams, and importers' internal trade teams. The wedge is overflow execution during a refund wave, not a durable defensible company.

## Strongest Objections Captured

1. **Customs brokers already own the filing relationship.** Only importers of record and authorized customs brokers are positioned to submit CAPE declarations through ACE. If the startup looks like unlicensed customs brokerage, it fails.
2. **Phase 1 scope is limited.** CAPE Phase 1 does not cover every refund scenario. Final-liquidation strategy, protests, drawback, reconciliation, and complex cases require later phases or other remedies.
3. **Legal/customs interpretation can creep in fast.** Eligibility, liquidation status, importer rights, protest preservation, and court-order scope can require broker or counsel judgment.
4. **The window may be short.** This is likely a refund-wave business unless it expands into other broker-routed refund/status/reconciliation batch operations.
5. **Data access is a major constraint.** ACE exports, entry numbers, liquidation status, importer identity, ACH refund status, bank setup, and customs records are sensitive.
6. **Brokers may internalize the workflow.** Once the process is learned, brokers can assign junior staff or automate.
7. **Refund attribution can be disputed.** Fixed batch fees should dominate because CBP may issue valid refunds anyway after acceptance.
8. **Public instructions reduce perceived complexity.** The workflow can look simple until entry volume and exceptions pile up.
9. **CEE/EU importer sourcing may be slower than broker sourcing.** Many eligible importers rely entirely on U.S. brokers.
10. **Low-margin data cleanup risk.** Messy entries, missing ACE access, unclear IOR status, ACH failures, and edge cases can turn the desk into customs archaeology.

## Useful Narrowing From Validator

Best beachhead:

- Small and mid-sized U.S. customs brokers serving importers with many IEEPA-duty entries but limited back-office capacity for CAPE screening, CSV preparation, status tracking, and refund reconciliation.

Secondary beachhead:

- CEE/EU brands, distributors, and manufacturers that were U.S. importers of record and paid IEEPA duties but lack internal U.S. customs operations.

Accept only:

- importer or broker authorization;
- named IOR account and entry ranges;
- ACE/exported entry data;
- broker-approved eligibility screen;
- CAPE Phase 1 scope map;
- ACH/ACE refund-readiness status;
- prepaid batch fee;
- authorized filer path;
- status ledger;
- exception/no-go rules.

Reject or route out:

- final-liquidation strategy;
- protest preservation;
- drawback;
- reconciliation entries;
- disputed eligibility;
- unclear IOR authority;
- customs classification issues;
- legal/tariff interpretation;
- refund-rights disputes;
- any case where the startup would file as broker.

## Lesson

Large current cash and official new refund tooling are not enough when licensed incumbents own the filer relationship and can internalize the operational process. Future candidates need the buyer or seller to approve direct payment direction, assigned current cash, or titled scarce assets where the decisive actor is not a licensed incumbent already sitting on the data.
