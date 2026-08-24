# Real Working Validation: OrphanMold Last-Run Parts Bank

Date: 2026-05-29

Prompt file: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_orphanmold_last_run_parts_bank.txt`

## Gate

- Simulated score: **91 / 100**
- Working Zero To One score: **70 / 100**
- Required working gate after user update: **>=85**
- Decision: **Fail; do not fresh-validate**

## Evaluator Judgment

Zero To One called the idea a disciplined physical-asset control play and liked the rule that no orphan tooling is purchased unless a buyer has already placed a deposit or conditional PO for a named non-safety part.

It still scored only **70** because tooling ownership, tool condition, sampling, production-partner willingness, and buyer acceptance can become messy fast. The evaluator saw this as worth testing in a narrow form, but not as a clean high-score business.

## Strongest Objections

1. Clean tooling ownership may be rare. Tooling may have been paid for by an OEM, amortized into part price, modified by the molder, inherited from another supplier, or undocumented.
2. Tool condition may destroy economics: wear, corrosion, damaged cavities, missing inserts, obsolete hot runners, cooling blockage, bad ejectors, flash, dimensional drift, unknown maintenance history, or incompatible press requirements.
3. Buyer deposits before first article may be hard to secure because buyers may want material confirmation, dimensional samples, finish/color, fit tests, tolerances, quote, and lead time first.
4. Production partners may not want to run old tools because of machine incompatibility, missing documentation, risky setup, or equipment-damage concerns.
5. Part quality can create rework: material substitution, shrinkage, tolerances, finish, warpage, inserts, clip breakage, fit, and packaging damage.
6. IP/customer rights can be messy even when physical tool possession looks clean.
7. Excluding regulated/safety categories is correct but reduces market size and removes many high-margin scarcity cases.
8. The work can become bespoke manufacturing operations: title review, sample identification, demand verification, production quote, material sourcing, first article, repair, scheduling, QC, shipping, and returns.
9. Incumbents can copy future sourcing. The moat is only transaction-specific after the exact tool and PO are controlled.
10. Tool storage can become a dead-asset trap if the founder starts buying tools speculatively.

## Useful Narrowing If Revisited Later

The evaluator's best version is:

- "Buyer-backed last-run tooling rescue for non-safety legacy parts."
- Proceed only when seller has documented transfer right, buyer is OEM/authorized distributor/lawful part owner, buyer deposits or issues conditional PO, production partner quotes first article and batch, part is non-safety and non-regulated, and tool purchase is contingent on title and production feasibility.

Even with strong proof, the evaluator estimated the score rises only to **77-80**, below the current real gate.

## Prompt Hygiene

The submitted prompt used the clean Zero To One opening and did not include internal scoring caps or evaluator instructions.
