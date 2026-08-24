# Anti-Overmerge Audit

## Verdict

**Pass with three required disposition corrections.**

All 15 direction families are defensible as mechanism-level clusters. Material differences among their concepts remain visible through `preserved_sibling` treatment, so no direction split or reassignment is required.

The three `merged_member` records are not field-by-field equivalents and must become preserved siblings.

## Required corrections

| Raw ID | Current mapping | Replacement mapping |
|---|---|---|
| `W2-IHK-04` | `W2-DIR-002` / `merged_member` | `W2-DIR-002` / `preserved_sibling` |
| `W2-RSA-06` | `W2-DIR-006` / `merged_member` | `W2-DIR-006` / `preserved_sibling` |
| `W2-FPE-07` | `W2-DIR-012` / `merged_member` | `W2-DIR-012` / `preserved_sibling` |

No direction IDs or memberships otherwise change.

## Merged-member findings

### `W2-IHK-04` — Rejected

It is not equivalent to lead `W2-IHK-03`.

- Customer/loss: foreign-business VAT write-off versus importer customs-duty overpayment.
- Payer/recovery source: foreign tax authority versus customs authority.
- Paid trigger: jurisdiction-specific VAT refund versus repayment against specified customs entries.
- Transaction owner: country-and-period VAT engagement versus entry-and-ground-specific customs engagement.
- Acquisition route: travel managers, event agencies and accountants versus customs agencies, forwarders and import operators.
- Compounding asset: jurisdictional eligibility and invoice-classification history versus commodity-code, valuation and customs-entry anomaly history.

Retain it within `W2-DIR-002`, but as a distinct sibling.

### `W2-RSA-06` — Rejected

It is not equivalent to lead `W2-RSA-04`.

- Customer/loss: construction-product document continuity versus battery-level passport completeness.
- Payer: construction-product manufacturers and importers versus battery manufacturers, distributors and storage integrators.
- Paid trigger: product-family passport publication plus continuity export versus battery passport creation at commissioning.
- Transaction owner: construction-product passport-responsible operator versus battery-placing economic operator.
- Acquisition route: laboratories, certification bodies, BIM advisers and construction wholesalers versus battery distributors, installers and renewable wholesalers.
- Compounding asset: product-type documentation lineage and superseded versions versus unique battery identities, service events, ownership transfers and second-life records.

Retain it within `W2-DIR-006`, but as a distinct sibling.

### `W2-FPE-07` — Rejected

It is not equivalent to lead `W2-IAT-01`.

- Customer/loss: manual roof-material movement and fragmented access equipment versus tool failure and short-job tool scarcity.
- Payer: both target installation contractors.
- Paid trigger: prepaid complete lifting-cell day versus reserved mixed-brand job pack and deposit.
- Transaction owner: both are entrant-owned equipment rental models.
- Acquisition route: roofing wholesalers and local installer referrals versus renewable-firm and general wholesaler relationships.
- Compounding asset: roof configuration, lifting-cell utilization and reservation history versus serial-level tool demand, failures, deposits and route availability.

The shared rental mechanism supports `W2-DIR-012`, but the materially different equipment cell and loss require sibling preservation.

## ID integrity

- Missing raw IDs: **0**
- Duplicate raw IDs: **0**
- Raw IDs assigned exactly once: **50**
- Family coverage: **10 TSE + 10 IHK + 10 IAT + 10 RSA + 10 FPE**
- All other mappings confirmed: **47**

## Revised counts

- Retained directions: **15**
- `lead`: **14**
- `merged_member`: **0**
- `preserved_sibling`: **35**
- `held_distinct`: **1**
- Total dispositions: **14 + 0 + 35 + 1 = 50**

## Reconciliation

The direction structure remains `W2-DIR-001` through `W2-DIR-015`. Reclassifying the three unsupported merges preserves every raw concept exactly once, keeps all economically material distinctions visible, and leaves the retained-direction count at **15**.
