# W2-L2-014 — Custom-order merchant of record

Research completed on 2026-08-22. The fixed budget was exhausted: exactly eight distinct web queries and eight source-open attempts. No replacement searches or sources were added after two fetch failures.

## Concept boundary

The entrant is the disclosed seller, merchant of record, and prime contractor for a fixed-specification custom-furniture order. It contracts directly with the buyer, subcontracts fabrication and installation, documents approvals, and remains responsible to the buyer for delivery, remedies, refunds, and payment disputes.

Initial scope should be low-complexity indoor furniture for business buyers: storage walls, office cabinetry, reception desks, counters, workbenches, and non-load-bearing fitted furniture. Early orders should exclude integrated electrical equipment, children’s furniture, load-bearing structures, fire-rated assemblies, and medically regulated environments.

## Problem and payer evidence

### Verified

- Polish custom-furniture suppliers publicly use staged payments. NEO Meble states a standard 50% deposit, 40% before dispatch, and 10% after installation. Metr publishes the same 50/40/10 pattern. This establishes commercial precedent for production-funded milestone collection, although not demand for this entrant’s intermediary model. [NEO Meble FAQ](https://neomeble.pl/faq/), [Metr pricing](https://metrmeble.pl/cennik-mebli-na-wymiar?lang=pl)
- Metr’s published 2026 starting prices are 12,000 PLN for kitchens, 6,000 PLN for wardrobes, and 4,000 PLN for bathroom furniture. These are directional consumer price anchors, not transaction averages. [Metr pricing](https://metrmeble.pl/cennik-mebli-na-wymiar?lang=pl)
- A completed 2025 public procurement for fitted educational and office furniture had a financing amount of 114,660.60 PLN. It demonstrates that a single institutional furniture order can be materially larger than a household cabinet order. [e‑Zamówienia notice](https://ezamowienia.gov.pl/mp-client/search/list/ocds-148610-221bc553-46b1-4422-8cf1-35c00f295dac)
- Stripe Poland lists 1.5% + 1 PLN for standard EEA cards, 1.6% + 1 PLN for BLIK, a 90 PLN dispute-received fee, and a further 90 PLN manually-countered fee refundable only when the dispute is won. [Stripe Poland pricing](https://stripe.com/en-pl/pricing)
- Stripe describes the merchant of record as the party shown to the customer that receives payment and bears responsibility for goods, refunds, and disputes. It requires consistent identification across the storefront, checkout, receipt, and statement descriptor. [Stripe merchant-of-record documentation](https://docs.stripe.com/connect/merchant-of-record)

### Interpretation

The entrant can sell three things that an individual workshop may not deliver consistently:

1. One accountable counterparty.
2. A controlled specification and revision process.
3. A funded remedy reserve with substitute-workshop capacity.

The workshop’s benefit is a clearer production package and milestone payments. The buyer’s benefit is remedy capacity beyond a single small workshop.

### Unknown

No source in the fixed packet quantified:

- ambiguous-specification frequency;
- workshop defect or late-delivery rates;
- chargebacks for custom furniture;
- buyer willingness to pay an intermediary margin;
- the number of qualifying Polish end buyers;
- customer-acquisition cost.

## Transaction and incentive/power map

| Stage | Buyer | Entrant | Workshop | Evidence/control |
|---|---|---|---|---|
| Lead and quote | Supplies requirements and budget | Qualifies buyer and selects workshop | Supplies preliminary cost and capacity | Timestamped quote and assumptions |
| Specification | Approves dimensions, materials, finishes, tolerances, access and installation conditions | Owns specification workflow and revision log | Confirms manufacturability and safety | Signed specification version |
| Contract | Contracts only with entrant | Disclosed seller, prime contractor and merchant of record | Signs subcontract with entrant | Matching buyer and workshop scopes |
| Design payment | Pays specification fee/deposit | Receives payment and invoices buyer | Normally unpaid or paid a small measurement fee | Payment record and delivered design milestone |
| Production release | Approves frozen specification | Issues purchase order and releases workshop deposit | Procures materials and fabricates | Signed production-release record |
| Pre-dispatch | Reviews photographs/checklist where appropriate | Collects next milestone and verifies evidence | Completes workshop QA | Photographs, measurements and checklist |
| Delivery/install | Provides access and identifies visible deviations | Coordinates delivery and remains buyer-facing | Delivers and installs safely | Delivery record and snag list |
| Acceptance | Approves, conditionally accepts, or records defects | Controls remediation and final settlement | Corrects allocated workmanship defects | Signed acceptance or exception record |
| Remedy/dispute | Claims against entrant | Refunds, repairs, replaces, or disputes chargeback | Reimburses entrant where subcontract allocation applies | Complete evidence bundle |

Power is deliberately split:

- Buyer controls requirements, production release, and acceptance.
- Workshop controls safe fabrication methods and may reject unsafe instructions.
- Entrant controls the customer contract, money, records, remedy selection, and workshop replacement.
- Entrant cannot contract away mandatory buyer rights or product-safety duties merely by allocating liability to the workshop.

## Payer denominator

### Verified denominator evidence

The GUS 2025 industrial-production dataset reports production quantities and values for enterprises employing at least ten people. Its accessible landing page does not provide an end-buyer count, and the underlying spreadsheet timed out. It therefore cannot serve as the payer denominator. [GUS industrial production 2025](https://stat.gov.pl/obszary-tematyczne/przemysl-budownictwo-srodki-trwale/przemysl/produkcja-wyrobow-przemyslowych-w-2025-r-%2C3%2C23.html)

### Bottom-up operating denominator

For the expected Year-7 case:

- 9.0 million PLN annual revenue;
- 20,000 PLN average order;
- 450 orders per year;
- approximately 300–350 active buyer accounts if accounts average 1.3–1.5 orders annually.

Illustrative funnel assumptions imply:

- At a 25% qualified-quote close rate: 1,800 qualified quotes annually.
- At 40% lead-to-qualified-quote conversion: 4,500 leads annually.
- At 1.25% cold-contact-to-order conversion: approximately 36,000 targeted contacts annually.

Those are planning assumptions, not measured rates. A named-account count by geography and vertical is still required before treating the denominator as known.

## Price, unit economics, and cash timing

All figures below exclude VAT because VAT is treated as pass-through. Tax treatment requires professional confirmation.

### Expected 18,000 PLN order

| Item | PLN | Revenue share |
|---|---:|---:|
| Buyer price | 18,000 | 100% |
| Workshop fabrication | 11,160 | 62% |
| Delivery and installation | 1,080 | 6% |
| Blended payment cost | 180 | 1% |
| Rework/refund reserve | 900 | 5% |
| Gross profit | 4,680 | 26% |
| Acquisition cost assumption | 1,200 | 6.7% |
| Specification, QA and order administration | 600 | 3.3% |
| Order contribution | 2,880 | 16% |

The 1% blended payment assumption requires bank transfer to dominate B2B milestone payments. Putting the entire 18,000 PLN on a standard EEA card would cost approximately 271 PLN at Stripe’s published rate, before any dispute expense.

### Proposed buyer schedule

- 10% on delivery of the initial specification package, credited to the order.
- 40% when the final specification is signed and production is released.
- 40% after documented workshop QA and before dispatch.
- 10% after installation acceptance or an agreed snag-retention period.

### Proposed workshop schedule

- 40% of workshop price at production release.
- 40% after pre-dispatch QA.
- 20% after installation acceptance.

At the expected order:

- Buyer cash after production release: 9,000 PLN.
- Workshop cash paid at that point: 4,464 PLN.
- Buyer cash before dispatch: 16,200 PLN.
- Workshop cash paid before dispatch: 8,928 PLN.

The difference funds coordination and the remedy reserve, but it is not free cash: payment-provider holds, cancellation, transport damage, and rework can consume it.

The specification payment should be earned against an actually delivered design/specification milestone. It should not be described automatically as non-refundable in all circumstances.

## Founder-wealth cases

These are operating models, not forecasts. “Operating profit” is an EBITDA-like proxy for the asset-light prime contractor. Valuation multiples and a 19% tax placeholder are assumptions, not sourced market or tax facts.

Reinvested earnings are not added separately to founder wealth. They are assumed to support the operating result and resulting enterprise value. Only distributions actually paid are added.

### Operating endpoints

| Case | Year-1 orders / AOV | Year-1 revenue | Year-1 gross / operating margin | Year-7 orders / AOV | Year-7 revenue | Year-7 gross / operating margin |
|---|---:|---:|---:|---:|---:|---:|
| Conservative | 18 / 12,000 | 216,000 | 18% / −5% | 180 / 16,000 | 2,880,000 | 20% / 7% |
| Expected | 30 / 15,000 | 450,000 | 23% / 0% | 450 / 20,000 | 9,000,000 | 25% / 15% |
| Strong | 45 / 18,000 | 810,000 | 25% / 2% | 1,200 / 28,000 | 33,600,000 | 29% / 22% |

### Conservative

- Founder capital: 60,000 PLN.
- Debt: none.
- Ownership: 100%.
- Founder remains employed through Year 7.
- Reinvestment: 95% of after-tax distributable profit; optional distributions 5%.
- Positive operating profit accumulated in the model, Years 2–7: 568,935 PLN.
- Cumulative founder distributions: approximately 23,000 PLN.
- Year-7 operating profit: 201,600 PLN.
- Illustrative value: 3.0 × operating profit = 604,800 PLN.
- Founder wealth at Year 7: approximately **628,000 PLN**, comprising business value and distributions.

### Expected

- Founder capital: 100,000 PLN.
- Revolving working-capital facility from Year 4: 300,000 PLN limit; 150,000 PLN assumed drawn at Year 7.
- Ownership: 90% after a 10% employee/adviser pool; no outside equity.
- Founder remains employed through Year 2.
- While employed: 95% reinvestment and 5% optional distributions.
- From Year 3: 85% reinvestment and 15% distribution.
- Year-7 operating profit: 1,350,000 PLN.
- Illustrative enterprise value: 4.5 × operating profit = 6,075,000 PLN.
- Equity value after assumed debt: 5,925,000 PLN.
- Founder’s 90% interest: 5,332,500 PLN.
- Cumulative founder distributions: approximately 430,000 PLN.
- Founder wealth at Year 7: approximately **5.76 million PLN**.

### Strong

- Founder capital: 100,000 PLN.
- Growth capital: 2.0 million PLN outside equity plus a 1.5 million PLN debt facility from Year 3; 500,000 PLN assumed drawn at Year 7.
- Ownership: 75% after 15% outside investors and a 10% employee pool.
- Founder remains employed through Year 1 and reinvests 100% of after-tax distributable cash that year.
- From Year 2: 90% reinvestment and 10% distribution.
- Year-7 operating profit: 7,392,000 PLN.
- Illustrative enterprise value: 6.0 × operating profit = 44,352,000 PLN.
- Equity value after assumed debt: 43,852,000 PLN.
- Founder’s 75% interest: 32,889,000 PLN.
- Cumulative founder distributions: approximately 1.12 million PLN.
- Founder wealth at Year 7: approximately **34.0 million PLN**.

The expected and strong cases require a multi-workshop network, delegated measurement and QA, employed operations staff, and the founder leaving employment. They are not compatible with one person personally supervising every order for five hours per day.

## Acquisition route

1. Begin with regional B2B furniture having repeatable specifications and low safety complexity.
2. Use the family connection to the renewable installer for one genuine paid internal order or a warm introduction—not an artificial testimonial.
3. Approach installers, electricians, HVAC contractors, property managers, clinics, offices, and small retailers with fixed-scope examples.
4. Build entrant-owned location-and-use-case quote pages such as office storage, reception desk, technical-room cabinetry, and fitted workshop storage.
5. Recruit architects and interior designers as referral channels while keeping the buyer contract with the entrant.
6. Use completed-specification examples and response-time commitments in search campaigns; avoid influencer-led acquisition.
7. Delay public procurement until the company has references, working capital, formal tender capability, and capacity for longer payment cycles.

## First ten customers

- Customer 1: the connected renewable installer, only if it has a real need and pays normal commercial consideration.
- Customers 2–4: installer’s suppliers, trade partners, or adjacent technical-service firms.
- Customers 5–7: regional offices, clinics, or retailers sourced by direct outreach.
- Customers 8–10: architect or fit-out referrals.

For each order, retain the original request, every revision, signed production release, workshop quote, QA record, acceptance record, actual margin, delay cause, and remedy cost.

## First one hundred customers

Proposed mix:

- 30 installers and technical-service SMEs;
- 25 offices and clinics;
- 20 retail and hospitality locations;
- 15 property managers and multi-site local businesses;
- 10 institutional buyers after references and tender capability exist.

Operationally, the first hundred require:

- at least three qualified workshops for each common product family;
- a trained external measurement network;
- standard tolerance and access checklists;
- independent pre-dispatch QA for larger orders;
- one order owner accountable from quote through remedy;
- separate reserve accounting rather than treating buyer deposits as profit.

## Control and compounding asset

The defensible asset is not the website or payment flow. It is the structured record joining:

- buyer specification and revisions;
- quoted versus actual workshop cost;
- dimension and tolerance failures;
- delivery and installation evidence;
- workshop lead time, acceptance rate, rework cost, and remedy speed;
- customer reorder patterns;
- reusable component and pricing libraries.

That dataset can improve workshop selection, quotes, reserves, and production-release checks. Access controls, retention rules, and data-protection procedures are required where records contain personal or premises data.

## Incumbent route-around

| Actor | Route-around | Entrant response |
|---|---|---|
| Workshop | Takes repeat buyer direct | Earn repeat business through reserve capacity, faster remedies, consolidated purchasing, and multi-site records |
| Marketplace | Adds custom quotation, staged payment, or buyer protection | Focus on measurement, specification control, acceptance, and physical remedies |
| Fit-out contractor | Bundles furniture into a larger project | Become the accountable furniture subcontractor or serve smaller standalone orders |
| Payment provider | Adds split payment or escrow-like tooling | Preserve value in specification, QA, workshop substitution, and remedy operations |
| Buyer procurement team | Contracts directly with workshops | Provide multi-workshop coverage, standard contracts, consolidated invoicing, and performance history |

A non-circumvention clause may help at the margin, but it is not a durable control asset and its enforceability and scope require legal review.

## Rule and constraint classification

### Binding law

- Under Article 38(1)(3) of Poland’s Consumer Rights Act, the distance/off-premises withdrawal right does not apply to a genuinely non-prefabricated good made to the consumer’s specification or individualized needs. This is not permission for a blanket “all deposits non-refundable” term, and it does not remove rights concerning non-conforming goods. [Polish Consumer Rights Act](https://eli.gov.pl/api/acts/DU/2023/2759/text.html)
- The EU General Product Safety Regulation requires only safe products to be placed or made available on the market. It addresses design, technical characteristics, assembly and installation instructions, manufacturer information, traceability, complaints, corrective action, and distributor checks. [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj?locale=pl)
- Selling under the entrant’s own name or trademark may change its product-safety role. Exact classification requires product-specific legal review.

### Contract and payment-network rules

- Buyer-facing identity, checkout, receipts, statement descriptor, customer service, refunds, and dispute responsibility must consistently identify the merchant of record. [Stripe documentation](https://docs.stripe.com/connect/merchant-of-record)
- Processor underwriting, reserves, permitted fulfilment structure, and ownership/possession rules remain dependencies.
- Workshop agreements must mirror the buyer specification while preserving the workshop’s right to reject unsafe fabrication instructions.

### Operational constraints

- Measurement error.
- Workshop insolvency or non-performance.
- Material substitutions.
- Installation damage and site-readiness disputes.
- Chargeback evidence deadlines.
- Reserve liquidity.
- Founder time while employed.

### Unresolved classifications

- Furniture-specific standards for each product type and use environment.
- Whether the entrant or workshop is the GPSR manufacturer in each branding arrangement.
- Fire, structural, electrical, accessibility, or public-building requirements.
- Product-liability and professional-indemnity insurance availability.
- Exact tax, invoice, and deposit accounting.

No binding Civil Code conclusion is taken from Q2 because the result was not opened within the source budget.

## Lawful structure

- Use a disclosed Polish operating entity as seller, prime contractor, invoice issuer, and merchant of record.
- Identify that entity consistently in the offer, contract, checkout, receipt, complaint process, and statement descriptor.
- Use a buyer specification appendix with dimensions, materials, tolerances, color references, exclusions, access conditions, installation scope, and revision history.
- Obtain a separate signed production release.
- State a fair cancellation schedule tied to work actually performed and irreversible workshop commitments.
- Preserve all mandatory remedies for non-conforming or unsafe goods.
- Sign a workshop subcontract covering the same specification, workmanship allocation, safety documentation, change control, inspection, delivery, rework, indemnity, and evidence obligations.
- Name the true manufacturer and responsible economic operator as required; do not use contractual language to disguise their roles.
- Keep buyer money and the rework reserve visibly separated in management accounting.
- Avoid hidden merchant identity, fabricated acceptance, misleading origin, unfair non-refundable terms, and unsafe substitutions.

## Dependencies

- Payment-provider pre-clearance of the exact disclosed-prime-contractor model.
- Consumer and commercial contract review by Polish counsel.
- Product-safety role and technical-documentation review.
- Product-liability, transit, installation, and professional-indemnity insurance quotations.
- Two or more workshops capable of producing the same first product family.
- Independent measurement and QA contractors.
- Working-capital line after repeatable order economics exist.
- Version-controlled specification and evidence system.
- Accountant confirmation of VAT, deposits, revenue recognition, and workshop invoicing.

## Fastest paid proof and capital at risk

### Paid proof

Within a single narrowly defined B2B product family:

1. Obtain two workshop quotes from the same specification template.
2. Secure payment-provider confirmation before accepting card payments.
3. Sell a 1,500–2,500 PLN specification milestone, credited to a 12,000–20,000 PLN order.
4. Deliver the specification, obtain signed production release, and collect the production milestone.
5. Complete the order and measure actual margin, founder hours, delay, acceptance, and remedy cost.

A paid specification alone proves willingness to pay for design work. Completion without uncontrolled founder time is needed to establish the transaction mechanics.

### Capital at risk

| Item | PLN |
|---|---:|
| Contract and product-role review | 2,000–4,000 |
| Measurement/design contractor | 1,000–2,500 |
| Rework/refund reserve | 5,000–8,000 |
| Buyer acquisition and quote flow | 1,000–2,000 |
| Insurance/admin contingency | 1,000–1,500 |
| Total | **10,000–18,000** |

The first order should be stopped before production if buyer receipts do not cover the workshop deposit plus the protected reserve.

## Kill criteria

Stop new order intake or materially narrow the product set if any of the following occurs:

- No provider will confirm acceptance of the disclosed merchant structure.
- Twenty qualified buyer conversations do not produce three paid specification milestones within eight weeks.
- Ten completed orders fail to sustain 20% gross margin after actual rework and payment losses.
- Rework, refunds, and chargebacks exceed 8% of revenue across the first twenty orders.
- Workshop on-time, specification-conforming acceptance remains below 85%.
- The cash cycle requires more than the available 100,000 PLN before a workable milestone schedule is established.
- The founder must routinely exceed five hours per day before the economics support an operations hire.
- Product-safety or insurance obligations cannot be satisfied within the proposed price.

## Decision-critical unknowns

1. Named, reachable payer count by initial vertical and geography.
2. Paid-search and direct-outreach acquisition cost.
3. Qualified-quote close rate and sales-cycle length.
4. True workshop defect, delay, and insolvency frequency.
5. Rework reserve required by product family.
6. Payment-provider reserve and payout treatment.
7. Chargeback incidence and evidence success.
8. Buyer willingness to contract with an entrant rather than the workshop.
9. Workshop willingness to accept mirrored remedies and final-payment retention.
10. Product-specific standards and GPSR role.
11. Insurance availability and exclusions.
12. Repeat-order frequency and direct-route-around rate.
13. Founder hours per completed order.
14. Sustainable valuation basis for an operational prime contractor.

## Development status

Desk research and financial modeling only. No buyer interviews, paid specifications, workshop contracts, processor underwriting, insurance quotations, live acquisition data, defect data, or completed orders were supplied.

# Query ledger

All queries ran on 2026-08-22 CEST during the research session ending at `2026-08-22T15:01:55+02:00`.

| ID | Exact query | Useful result |
|---|---|---|
| Q1 | `site:eli.gov.pl ustawa prawa konsumenta art. 38 rzecz nieprefabrykowana specyfikacja konsumenta` | S1 |
| Q2 | `site:eli.gov.pl kodeks cywilny umowa o dzieło odbiór wady art. 627 638 podwykonawca` | Search result found, but no source opened or relied upon |
| Q3 | `site:eur-lex.europa.eu Regulation EU 2023/988 furniture distributor obligations economic operator product safety` | S2 |
| Q4 | `site:stat.gov.pl Polska produkcja mebli 2025 liczba przedsiębiorstw wartość sprzedana meble na wymiar` | S3; spreadsheet fetch timed out |
| Q5 | `Polska meble na wymiar cennik zaliczka etapy płatności producent 2026` | S4, S8 |
| Q6 | `site:ezamowienia.gov.pl meble na wymiar zabudowa biurowa wartość zamówienia 2025` | S5 |
| Q7 | `site:stripe.com/en-pl/pricing dispute fee refund original processing fees Poland` | S6 |
| Q8 | `site:stripe.com merchant of record third party payments prohibited payment facilitation custom goods` | S7 |

# Source ledger

| ID | Source | Access mode and timestamp | Use |
|---|---|---|---|
| S1 | [Polish Consumer Rights Act](https://eli.gov.pl/api/acts/DU/2023/2759/text.html) | Direct open; 2026-08-22 CEST | Article 38 custom-goods exception |
| S2 | [Regulation (EU) 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj?locale=pl) | Direct open; 2026-08-22 CEST | General product-safety obligations |
| S3 | [GUS — industrial production in 2025](https://stat.gov.pl/obszary-tematyczne/przemysl-budownictwo-srodki-trwale/przemysl/produkcja-wyrobow-przemyslowych-w-2025-r-%2C3%2C23.html) | Direct open; 2026-08-22 CEST | Dataset scope and denominator limitation |
| S4 | [NEO Meble FAQ](https://neomeble.pl/faq/) | Search extract; direct fetch returned an internal error; 2026-08-22 CEST | 50/40/10 payment schedule |
| S5 | [e‑Zamówienia furniture procurement](https://ezamowienia.gov.pl/mp-client/search/list/ocds-148610-221bc553-46b1-4422-8cf1-35c00f295dac) | Search extract; direct fetch returned an internal error; 2026-08-22 CEST | 114,660.60 PLN institutional order |
| S6 | [Stripe Poland pricing](https://stripe.com/en-pl/pricing) | Direct open; 2026-08-22 CEST | Processing and dispute fees |
| S7 | [Stripe merchant-of-record documentation](https://docs.stripe.com/connect/merchant-of-record) | Direct open; 2026-08-22 CEST | MoR identity and responsibility |
| S8 | [Metr custom-furniture pricing](https://metrmeble.pl/cennik-mebli-na-wymiar?lang=pl) | Search extract; 2026-08-22 CEST | Starting prices and 50/40/10 schedule |

The GUS XLSX download was the fifth source-open attempt and timed out. No spreadsheet figures were used. The remaining three attempts were S5, S6, and S7, bringing the total to eight.

# Evidence ledger

| Evidence | Status | Implication |
|---|---|---|
| E1: Article 38 exception for genuinely individualized, non-prefabricated goods | Verified, primary authority | A qualifying custom good may fall outside the ordinary distance-withdrawal right |
| E2: GPSR safety, traceability, documentation, installation, complaint, and corrective-action duties | Verified, primary authority | The entrant needs product-role analysis and cannot rely solely on workshop indemnity |
| E3: Stripe card, BLIK, and dispute fees | Verified, commercial source | Payment and dispute costs require explicit unit-economics and reserve treatment |
| E4: MoR must be clearly identified and bears refund/dispute responsibility | Verified, payment-network implementation source | Hidden or inconsistent merchant identity is incompatible with the structure |
| E5: 50/40/10 custom-furniture payment precedent | Commercially observed | Customer-funded production milestones are plausible |
| E6: Published 4,000–12,000 PLN starting prices | Commercially observed | A 12,000–20,000 PLN first order is within published category pricing |
| E7: 114,660.60 PLN institutional furniture procurement | Verified from procurement search extract | Larger B2B/institutional orders exist |
| E8: GUS dataset covers manufacturers with at least ten workers | Verified, official source | It does not establish the end-buyer denominator |
| E9: 20–29% gross margins and scenario volumes | Interpretation | Must be tested with live workshop quotes and completed orders |
| E10: Acquisition funnel, valuation multiples, tax placeholder, and founder-wealth outcomes | Interpretation | Planning model only |
| E11: CAC, defect rate, chargeback rate, payer count, repeat rate, insurance, and processor reserves | Unknown | These determine the actual cash requirement and operating shape |
