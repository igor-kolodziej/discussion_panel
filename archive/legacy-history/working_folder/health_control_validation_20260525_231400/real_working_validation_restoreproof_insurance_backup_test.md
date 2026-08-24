# Real Working Validation: RestoreProof Cyber-Insurance Backup Test Evidence Bench

Date: 2026-05-29
Prompt file: `zero_to_one_prompt_restoreproof_insurance_backup_test.txt`
Working chat: Zero To One, GPT-5.5 Thinking / Extended mode
Gate: working score >=85
Result: FAIL

## Score

68 / 100

## Validation Hygiene

The first RestoreProof submission was invalid because ChatGPT localStorage contained a stale `oai/apps/conversationDrafts` entry with an unrelated brainstorming prompt, which was appended after submission. I stopped that run, cleared the draft store, verified the editor and localStorage contained only the RestoreProof prompt, and resubmitted in a clean Zero To One chat.

The clean run showed only the RestoreProof prompt as the user message. The evaluator produced a score of 68/100. The response body then partially echoed a rewritten prompt, so the detailed objection section was not cleanly emitted, but the failing gate decision is unambiguous.

## Zero To One Diagnosis Captured

The evaluator called the idea a good, sharp wedge but not a high-confidence dominant business. It accepted that backup-restore evidence can appear in cyber-insurance workflows, but did not believe the proposed broker/MSP-routed restore-test bench overcomes incumbent ownership, implementation/no-go frequency, or defensibility issues.

## Strongest Objections Captured

- Brokers and MSPs can often produce backup evidence themselves.
- Many clients will not have a truthful recent backup/restore proof, so cases become remediation or no-go rather than evidence generation.
- Underwriters may still decline, surcharge, exclude ransomware, or request more evidence after a restore artifact.
- Backup-platform access is sensitive and MSPs may refuse an outside reviewer.
- The founder needs credible backup/BCDR contractors immediately.
- Evidence quality varies by platform, restore scope, and underwriter wording.
- Misstatement risk is severe if an insured wants to exaggerate recovery capability.
- The business may remain a narrow white-label service unless broker case blocks repeat and accepted artifact formats compound.

## Gate Decision

Working score 68 is below the current real gate of 85. Do not fresh-validate.

## Search Lesson

Generating a hard artifact rather than packaging evidence is still not enough when the natural channel owner can perform the work, many leads require real remediation, and the end decision remains with an underwriter. Stop retesting cyber-insurance variants without a materially stronger owned payment stream.
