# Real Working Validation: CPSC eFile Entry Release Desk

## Gate

- Validation agent: Zero To One, GPT-5.5 Thinking / Extended mode
- Chat: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a1a16b0-dee8-83eb-8557-870aaefcd9da`
- Prompt file: `zero_to_one_prompt_cpsc_efile_entry_release.txt`
- Simulated score: `88.2 / 100`
- Real gate: `>=85`
- Working-chat score: `70 / 100`
- Decision: `FAIL`

## Zero To One Verdict

Zero To One judged this stronger than MoCRABlocked because the deadline is harder, the import-entry workflow is more operational, and brokers/3PLs have direct incentive to avoid shipment friction.

It still failed because the founder sits too close to customs and product-safety compliance, while customs brokers, labs, CPSC consultants, and testing firms already own trust, authority, and workflows.

## Strongest Objections Captured

1. Customs brokers and labs already sit closer to the transaction and can absorb the service.
2. Product classification, rule applicability, certificate sufficiency, lab validity, and product-safety judgment can swallow the business.
3. The July 8, 2026 timing spike may fade after brokers, labs, importers, and larger sellers standardize templates.
4. Many sellers will not have the source truth: valid test reports, manufacturer details, production dates, factory addresses, labels, model numbers, and proper CPC/GCC records.
5. The economic buyer may not be the EU seller; importer-of-record authority and broker authorization are critical.
6. Product Registry work should not be oversold because the paid event is broker-ready certificate data for entry.
7. Case economics can collapse into SKU-by-SKU clerical work if label review, supplier chasing, test-report matching, and broker questions are heavy.
8. Brokers may internalize the playbook once repeated cases reveal a standard intake checklist.

## Useful Narrowing From Validator

The best version is:

> Broker-routed CPSC eFiling data rescue desk for EU/CEE sellers with named US shipments and existing source evidence.

POC constraints:

- Start with one product category cluster, not all consumer products.
- Work only through 2-3 brokers, 3PLs, or agencies that already have the importer relationship.
- Accept only cases with existing test reports, product identifiers, label photos, manufacturer details, and broker-supplied entry context.
- Charge `2,000-4,000 PLN` paid triage before packet build.
- Do not touch unresolved classification, testing, lab validity, safety, or legal questions without a named qualified reviewer.
- Continue only if two channels each send at least eight paid cases and at least `40,000 PLN` is collected in the first 60 days.

## Gate Decision

Fails the working-chat real gate. Do not fresh-validate.

## Lesson

Official import-entry artifacts are stronger than marketplace listing packets, but the evaluator still caps them when trusted incumbents control the filing and safety decisions. Avoid more customs/product-safety evidence desks unless the founder controls a paid queue or payment stream that brokers and labs cannot simply internalize.
