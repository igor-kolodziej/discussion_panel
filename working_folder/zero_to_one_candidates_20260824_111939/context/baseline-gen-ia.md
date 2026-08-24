# Immutable Generation Packet

## Identity And Allocation

- Scope: `baseline-w01`
- Arm: `matched_baseline`
- Stage: `generation`
- Agent ID: `baseline-gen-ia`
- Role: `incumbent_attacker`
- Model: `gpt-5.6-sol`
- Reasoning: `high`
- Seed: `v2-matched-20260824_111939-2a69f68acefb8c3de519b17edb17c50e`
- Allocation ID: `ALLOC-B-DISC-IA`
- Query cap: `22`; use exactly four calls: two search calls and one opened result for each search. Leave the remainder unused.
- Assigned and required output IDs: `RAW-001, RAW-002, RAW-003, RAW-004, RAW-005, RAW-006, RAW-007, RAW-008, RAW-009, RAW-010`
- Required return path: `/Users/igor/Desktop/discussion_panel/working_folder/zero_to_one_candidates_20260824_111939/agent_returns/baseline-gen-ia.json`

## Founder Constraints

Warsaw data scientist employed full time; at most five focused hours daily; about 100,000 PLN personally available and another 100,000 PLN only for an unusually clear case. Strong AI/data/neuroscience/finance fluency, a medical-student partner, and a family renewable-installation firm near Ostrow Wielkopolski. Avoid camera-led distribution and constant high-energy networking. Prefer part-time proof, controlled downside, repeatable demand, scalable assets, and a plausible path to 5 million PLN of founder net worth without double counting.

## Safety And Legal Boundary

Generate only lawful structures. Reject indispensable deception, coercion, exploitation, privacy abuse, evasion, or serious harm. Classify each key constraint as one of: LAW / BINDING RULE; SOFT INDUSTRY NORM; ASSUMED CONVENTION; REPUTATIONAL EXPECTATION; TECHNICAL LIMITATION; ECONOMIC LIMITATION. Unsupported public facts remain explicit unknowns.

## Role Assignment

Look for excessive pricing, cross-subsidy, weak service, slow operations, channel conflict, fragmented supply, or route-around gaps that an unknown entrant can reach.

Search broadly across sectors. Generate economically distinct concepts, not title variants. Each concept needs a named customer loss, payer and paid trigger, transaction owner, acquisition route, and possible compounding asset. Do not rank or select concepts. Do not read any other file or use any inherited repository material.

## Evidence Assignment

Run two genuinely different, time-sensitive public-evidence searches. For each, open exactly one useful result. Use the first evidence chain for the first entity group and the second chain for the second group:

- `EV-B-DISC-001` applies to `RAW-001, RAW-002, RAW-003, RAW-004, RAW-005`.
- `EV-B-DISC-002` applies to `RAW-006, RAW-007, RAW-008, RAW-009, RAW-010`.

Prefer direct customer, procurement, operational, incumbent, technical, or official evidence according to the role. Record contradiction and uncertainty honestly. A public source may support a problem or mechanism; it does not prove willingness to pay unless it actually shows budget or payment.

## Required Return Schema

Create exactly one valid UTF-8 JSON object at the required return path, using the file-creation patch tool once. Do not create or read any other file. The object must have exactly these top-level keys:

`agent_id`, `role`, `assigned_ids`, `output_ids`, `queries`, `concepts`, `files_read`.

- `agent_id`, `role`, `assigned_ids`, and `output_ids` must exactly match this packet and preserve ID order.
- `files_read` is exactly `["context/baseline-gen-ia.md"]`.
- `queries` contains exactly two objects, in tool-call order, each with: `search_text`, `opened_url`, `source_title`, `source_date` (or null), `evidence_id`, `entity_ids`, `proposition`, `status`, `contradiction`, and `cheapest_resolving_test`.
- `concepts` contains exactly one object per assigned raw ID with: `raw_id`, `title`, `one_sentence_thesis`, `customer`, `loss_event`, `payer`, `beneficiary`, `authority_holder`, `distributor`, `risk_bearer`, `transaction_owner`, `first_paid_event`, `acquisition_route`, `compounding_asset`, `mechanism_class`, `evidence_id`, `hypotheses` (array), `constraint_class`, and `prohibited_reliance` (null or a precise statement).
- Every concept's `evidence_id` is the assigned evidence ID for its entity group.
- Keep every concept concise but concrete. Do not include numeric merit ratings, downstream framework language, or another concept author's conclusions.
