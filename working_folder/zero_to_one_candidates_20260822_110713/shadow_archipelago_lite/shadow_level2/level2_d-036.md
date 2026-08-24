# Level-2 D-036 — Curtailment Claim Ledger

## Problem And Payer Evidence

Polish curtailment exposure is verified. URE reports that in 2024 PSE ordered 597.26 GWh of photovoltaic reduction—up 2,362% year over year—and nearly 125.1 GWh of wind reduction. Most photovoltaic reduction was attributed to national-system balancing rather than network constraints. [URE 2024 redispatch report](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12923%2CRynek-energii-elektrycznej-sprawozdanie-Prezesa-URE-dotyczace-mechanizmow-redysp.html)

PSE states that owners of renewable installations implementing a non-market redispatch instruction have a financial-compensation right under Article 13(7) of Regulation (EU) 2019/943, subject to applicable national rules. PSE also states that, under Article 93(18) of the Polish Renewable Energy Sources Act, a producer generally has 14 days from the instruction to tell the connected operator what portion of reduced energy should count within the auction support system. Missing that notification prevents the reduced energy from counting toward the support obligation and excludes the associated lost support revenue from that part of compensation. [PSE non-market redispatch guidance](https://www.pse.pl/pl_PL/redysponowanie-nierynkowe) [EU Regulation 2019/943](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0943)

The direct payer is an exposed renewable generator, portfolio owner, or asset manager. O&M firms, energy lawyers, PPA advisers, and aggregators are channel partners because they already hold parts of the operational and contractual evidence. PSE reported 26,020 MW of photovoltaic capacity as of February 2026, but total capacity is not a count of exposed, eligible, independently paying portfolios. The payer denominator remains unknown.

A 2026 European Commission country report says Polish curtailment and negative-price frequency have grown, while fair-payment calculation remains unclear. It reports almost 500 GWh of renewable redispatch between June and September 2025, approximately 75% photovoltaic. This is counterevidence to any assumption that public operator intervals translate mechanically into a clear claim amount. [European Commission country report](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52026SC0221)

A direct willingness proxy exists but remains commercially unverified: OdzyskOZE advertises automated Polish claims with a partner-law-firm fee of 5% of amounts recovered. It explicitly labels its examples hypothetical and says it has not yet published real customer case studies. It also states that actual coverage can be low when relevant market prices are negative or near zero. [OdzyskOZE](https://odzyskoze.pl/en/)

The closest substitute is a spreadsheet maintained by the generator, O&M provider, asset manager, trader, or counsel. The incumbent route-around is to ask the O&M provider to reconcile intervals, engage an energy lawyer after a material event, change PPA risk allocation, participate in balancing markets, add storage, or accept the operator’s calculation. Storage and PPA changes address future economics but do not reconstruct past evidence or deadlines.

## Proposed Transaction

The transaction should separate technical monitoring from regulated legal representation:

- Portfolio monitoring and deadline ledger: approximately 1,500–6,000 PLN per month, or 250–750 PLN per monitored asset where data are standardized.
- One-time setup and historical reconciliation: approximately 2,000–8,000 PLN per asset or 8,000–30,000 PLN per heterogeneous portfolio.
- Technical outcome fee: potentially 1–3% of compensation actually accepted or paid, capped and payable only if counsel confirms that the structure is lawful.
- Legal filing, representation, negotiation, and litigation: a separate engagement directly between the customer and qualified counsel.

These ranges are interpreted. The only direct commercial proxy found is a vendor advertising a 5% partner-law-firm success fee; actual Polish customer acceptance and ethical permissibility require confirmation.

The customer-facing ledger should link each operator instruction to asset, interval, instructed reduction, actual generation, modeled available power, metered data, availability/outage status, public operator data, market and settlement prices, support-scheme treatment, PPA treatment, notice deadline, evidence gaps, filing status, operator response, and final amount. It should never label an estimate as an entitlement or booked receivable.

Exact access requires asset-owner authorization; a data-processing and confidentiality agreement; a current grid-connection agreement; operator instructions and correspondence; 15-minute or finer SCADA and meter exports; availability and outage records; production forecasts; balancing and settlement statements; PPA and support-scheme documents; and read-only access using CSV, API, historian replica, or a segregated data room. No control commands should be possible through the monitoring credentials. SCADA cybersecurity architecture, remote-access approval, critical-infrastructure obligations, powers of attorney, filing authority, and legal fee arrangements are counsel-required.

A ten-portfolio historical proof can be performed through O&M firms or counsel, but the lowest-cost version should start with ten assets or asset groups whose owners authorize review. Estimated capital is approximately 25,000–60,000 PLN for secure ingestion, interval reconciliation, counsel validation, and manual review. Production SCADA connectors, deadline operations, and legal workflow could consume 60,000–100,000 PLN before repeatability is known.

Economic sensitivity depends on exposed value, not curtailed MWh alone. Low or negative settlement prices, support-scheme rules, PPA allocation, outages, inaccurate available-power models, and excluded costs can reduce the claim. A subscription of 3,000 PLN per month plus an outcome fee requires recurring preserved value materially above that amount; public national curtailment totals do not demonstrate account-level value.

## Acquisition Route

The first-customer route is a historical one-year review through an O&M firm, energy lawyer, PPA adviser, or local solar operator. The partner should supply ten authorized files representing different asset sizes, grid operators, support arrangements, and PPA structures, without exposing unrelated customer portfolios.

The proof procedure is:

1. Obtain written asset-owner authority and a counsel-approved scope.
2. Inventory every public or customer-recorded redispatch interval.
3. Reconcile operator notices, SCADA, metering, availability, settlement, support, PPA, correspondence, and deadline records.
4. Identify missing notices, unreconciled intervals, unsupported availability assumptions, and missed or approaching deadlines.
5. Have the generator and qualified counsel decide whether each gap has a claim consequence.
6. Record accepted, rejected, uncertain, and time-barred outcomes without filing automatically.

The decisive private test is whether at least 20% of authorized portfolios contain a missed deadline, incomplete evidence set, or unreconciled interval with a material consequence confirmed by the generator or counsel. “Material consequence” must exclude cosmetic documentation errors and speculative headline-price multiplication.

A compounding asset could be a segregated case library mapping operator, asset type, support scheme, PPA structure, interval evidence, calculation treatment, evidence gap, response time, and final outcome. Legal memoranda, customer contracts, SCADA data, and claim strategies must remain customer-confidential unless an explicit reuse right exists.

## Decision-Critical Unknowns

- **Verified:** Polish renewable curtailment rose sharply in 2024.
- **Verified:** Article 13(7) establishes a compensation principle for specified non-market redispatch circumstances.
- **Verified:** PSE publishes a 14-day support-system notification requirement and explains a consequence for missing it.
- **Verified:** PSE and URE publish operator and redispatch information usable in a reconciliation ledger.
- **Interpreted:** O&M firms, energy lawyers, PPA advisers, and asset managers are plausible first-customer channels.
- **Unknown:** The number of exposed and economically reachable paying portfolios.
- **Unknown:** Whether at least 20% of reviewed portfolios contain consequential missed deadlines, incomplete evidence, or unreconciled intervals.
- **Unknown:** Recoverable value per asset after market-price, support, PPA, outage, and availability treatment.
- **Unknown:** Whether one reconciliation method generalizes across operators, SCADA vendors, asset configurations, and commercial contracts.
- **Unknown:** How often asset owners can supply synchronized SCADA, meter, settlement, and correspondence data.
- **Unknown:** Customer acceptance of monitoring, setup, and outcome-linked pricing.
- **Unknown:** The ongoing manual burden of exception review and deadline monitoring.
- **Contradicted:** Curtailment MWh multiplied by an average positive wholesale price is not a reliable claim estimate.
- **Contradicted:** A proposed Energy Law amendment is not enacted law. The government proposal itself describes shortcomings for pay-as-produced PPAs; it must not be applied as current binding treatment until verified in enacted legislation. [Government legislative proposal](https://www.gov.pl/web/premier/projekt-ustawy-o-zmianie-ustawy--prawo-energetyczne2)
- **Contradicted:** Missing the 14-day support notification should not automatically be described as destroying every compensation component; PSE identifies specific support-related consequences.
- **Counsel-required:** Current statutory deadlines beyond the verified 14-day notice, claim eligibility, contestable calculations, PPA allocation, powers of attorney, filing conduct, litigation, SCADA-security obligations, and all outcome-fee structures.

## Evidence And Sources

Dated direct-URL ledger:

- 2025 URE publication, 2026-08-22 accessed — official 2024 redispatch volumes: [https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12923%2CRynek-energii-elektrycznej-sprawozdanie-Prezesa-URE-dotyczace-mechanizmow-redysp.html](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12923%2CRynek-energii-elektrycznej-sprawozdanie-Prezesa-URE-dotyczace-mechanizmow-redysp.html)
- 2026-08-22 accessed — PSE compensation right, 14-day notice, and current operating guidance: [https://www.pse.pl/pl_PL/redysponowanie-nierynkowe](https://www.pse.pl/pl_PL/redysponowanie-nierynkowe)
- 2019-06-05 regulation, 2026-08-22 accessed — Article 13(7), Regulation (EU) 2019/943: [https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0943](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0943)
- 2025 proposal, 2026-08-22 accessed — proposed Polish Energy Law amendment and PPA rationale: [https://www.gov.pl/web/premier/projekt-ustawy-o-zmianie-ustawy--prawo-energetyczne2](https://www.gov.pl/web/premier/projekt-ustawy-o-zmianie-ustawy--prawo-energetyczne2)
- 2026 report, 2026-08-22 accessed — European Commission discussion of curtailment and calculation uncertainty: [https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52026SC0221](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52026SC0221)
- 2026-08-22 accessed — direct commercial offer, data requirements, pricing proxy, and explicit absence of real case studies: [https://odzyskoze.pl/en/](https://odzyskoze.pl/en/)

### Query trace

1. `site:pse.pl curtailment renewable compensation 14 days Poland generator`
2. `site:ure.gov.pl nierynkowe redysponowanie compensation renewable 14 days`
3. `Poland renewable curtailment 2024 GWh official PSE`
4. `Polish Energy Law curtailment compensation claim non-market redispatch`
5. `site:gov.pl Poland curtailment compensation renewable amendment 2025`
6. `site:sejm.gov.pl redysponowanie nierynkowe rekompensata 14 dni`
7. `site:pse.pl rekompensata redysponowanie nierynkowe wniosek`
8. `site:pse.pl curtailment OZE komunikat compensation calculation`
9. `Poland solar curtailment claim law firm PPA compensation`
10. `Poland renewable curtailment SCADA meter data claim process`
11. `Poland curtailment compensation negative prices support scheme`
12. `Poland O&M solar portfolio curtailment reconciliation`

