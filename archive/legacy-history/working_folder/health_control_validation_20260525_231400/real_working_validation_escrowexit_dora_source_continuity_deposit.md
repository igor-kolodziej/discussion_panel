# Real Working-Chat Validation: EscrowExit DORA Source-Continuity Deposit Pack

Date: 2026-05-30
Gate: working Zero To One score must be >=85

## Score

70 / 100

## Gate Decision

FAIL. The idea does not pass the working-chat real validation gate.

## Exact Prompt File

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_escrowexit_dora_source_continuity_deposit.txt`

The submitted prompt used the clean Zero To One opening and did not include internal cap language or evaluator instructions. The validation was run with Extended/Thinking mode active.

## Zero To One Summary

The evaluator considered this stronger than generic DORA evidence work because it produces a concrete artifact: escrow deposit, build/recovery package, receipt, and buyer proof. It accepted that DORA and ICT third-party-risk pressure can lead banks to ask for exit-continuity or escrow evidence.

The score stayed far below gate because source-code escrow is only one possible continuity mechanism, not a universal DORA requirement. Banks may ask for broader exit testing, contract clauses, step-in rights, BCP/DR, audit rights, and data-return/deletion evidence. Escrow providers, law firms, and DORA advisers also sit closer to the trusted workflow.

## Strongest Objections

1. Banks may not accept a deposit receipt as enough and may demand broader DORA exit/continuity evidence.
2. DORA does not mandate source-code escrow; the business must be buyer-request-led, not regulation-led.
3. Modern SaaS escrow is difficult because source code alone may be useless without IaC, deployment scripts, runbooks, data schemas, operational knowledge, secrets handling, and third-party services.
4. Many vendors will not be deposit-ready because of missing build scripts, undocumented dependencies, contractor IP ambiguity, hardcoded secrets, private packages, fragile deployments, or missing runbooks.
5. Escrow providers can internalize vendor-side deposit packaging.
6. Law firms may own release conditions, beneficiary rights, IP scope, third-party licenses, insolvency triggers, and step-in rights.
7. Handling source code and architecture creates a serious trust burden for an unknown founder.
8. The six-month revenue and case target was too aggressive for a part-time unknown founder.

## Evaluator's Better Narrowing

"DORA-triggered source/build continuity deposit execution for SaaS vendors with regulated-finance buyer blockers."

Recommended POC constraints:

- written buyer request text required;
- blocked commercial value above 150,000 PLN;
- chosen escrow provider or counsel route before technical packaging starts;
- exclude broad DORA remediation, contract negotiation, and major engineering cleanup;
- charge 18,000-35,000 PLN prepaid;
- continue only if 4 of first 6 cases produce escrow-provider acceptance, deposit receipt, buyer acknowledgement, or vendor-accepted no-go.

## Lesson

Harder artifacts help, but DORA-adjacent variants remain capped when they are optional mechanisms inside broader legal/security continuity work. Do not continue DORA variants without a materially stronger owned payment stream or proof that the specific artifact is repeatedly accepted by regulated buyers.

