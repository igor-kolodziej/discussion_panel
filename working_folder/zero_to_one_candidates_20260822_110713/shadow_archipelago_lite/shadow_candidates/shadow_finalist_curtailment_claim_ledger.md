# Shadow Finalist SFIN-03 — D-036

Shadow-only diagnostic artifact. It is not eligible for downstream routing and cannot alter the frozen live cohort.

## Frozen Level-2 Dossier

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

## Frozen Fact Closure

# Fact Closure D-036

## Findings

- **verified:** Payers exist: PSE identifies owners of renewable installations that executed non-market redispatch instructions as the parties entitled to seek compensation.
- **unknown:** The payer denominator is not closed. PSE reports 26,020 MW of photovoltaic capacity and 11,175 MW of wind capacity in early 2026, while URE publishes installation registers; neither source identifies the number of curtailed, eligible, economically material, independently purchasing portfolios.
- **verified:** First-contract authority rests with the installation owner, its KRS-authorized representatives, or a properly empowered attorney. PSE permits servicing entities to operate applications, but accepting settlement information requires appropriate representative or attorney authority.
- **interpreted:** Direct commercial willingness has a current proxy: OdzyskOZE publicly offers subscriptions of €119, €699, or €2,325 per month plus a partner-law-firm fee of 5% of recovery.
- **unknown:** OdzyskOZE states that its examples are illustrative and that real case studies will be published only after it has consenting clients; the offer therefore proves a seller’s pricing hypothesis, not purchases, recoveries, or market acceptance.
- **verified:** The incumbent route-around is substantial. Owners can use PSE’s WOZE portal, current Excel forms, correction workflow, settlement information, and complaint process without buying a third-party ledger.
- **unknown:** Public sources do not establish the capital required for repeatable SCADA ingestion, multi-operator normalization, evidence exception handling, or secure portfolio operation.
- **interpreted:** The cheapest remaining proof is document-led rather than integration-led: review ten authorized assets or asset groups using existing PSE forms, notices, meter or SCADA exports, connection agreements, support records, settlements, and correspondence.

## Decision-Critical Evidence

- **verified:** PSE states that compensation is unavailable where the connection agreement does not guarantee firm delivery for balancing-related reasons. Connection-agreement screening must therefore precede onboarding.
- **verified:** Article 13(7) of Regulation (EU) 2019/943 requires compensation for non-market redispatch, subject to the non-firm-delivery exception, based on additional operating cost, foregone net day-ahead revenue, or an appropriate combination where one measure would be unjustifiably low or high.
- **verified:** PSE’s operating rules state that the compensation claim expires if the owner does not apply before 180 days have elapsed from the last day of the month in which the redispatch instruction was executed.
- **verified:** For auction-support treatment, Article 93(18) as implemented in PSE guidance requires notice to the connected operator within 14 days of the instruction. Missing it excludes the reduced energy from the support obligation and the related lost-support-revenue component; it does not extinguish every possible compensation component.
- **verified:** A deficient claim left uncorrected for 14 days may be left without examination, and an owner has 21 days to complain about rejection or settlement information.
- **verified:** WOZE is available to owners and entities servicing them. Its ordinary service roles permit preparing and viewing applications but expressly exclude acceptance of compensation.
- **verified:** PSE requires OSD authorizations and, where applicable, a power of attorney. Acceptance authority must follow KRS representation rules or a sufficient power of attorney.
- **verified:** PSE’s forms accommodate incomplete irradiance or wind data and prescribe averaging when measurements use multiple points or non-15-minute periods. Missing direct measurements are therefore an evidence-quality issue, not automatically a proven lost claim.
- **interpreted:** Direct WOZE access, operator calculation, correction, and complaint workflows mean the ledger must prove value from deadline control, evidence reconciliation, or contestable exceptions rather than merely reproducing public redispatch intervals.
- **contradicted:** A universal eligibility premise is contradicted by the non-firm-connection exception.
- **contradicted:** A claim estimate based only on curtailed MWh multiplied by an average positive wholesale price is contradicted by the governing calculation framework.
- **counsel-required:** Eligibility under individual connection agreements, PPA allocation, support treatment, complaint or litigation strategy, filing authority, outcome-linked fees, and the legal effect of each operator rule require Polish energy counsel.
- **counsel-required:** The amended Polish cybersecurity regime requires entities meeting its sectoral and size criteria to assess registration, information-security, incident, and audit obligations. Whether the ledger provider or a particular generator is covered cannot be inferred from the energy-sector label alone.

## Remaining Unknowns

- **unknown:** The number of portfolios combining actual curtailment, firm-delivery eligibility, material recoverable value, reachable ownership, and willingness to buy monitoring.
- **unknown:** Whether at least 20% of ten authorized portfolios contain a missed deadline, incomplete evidence set, or unreconciled interval with a material consequence confirmed by the owner or counsel.
- **unknown:** The distribution of realized compensation after negative prices, support rules, PPA terms, outages, availability modeling, and operator calculations.
- **unknown:** Whether customers have synchronized notices, SCADA, metering, settlement, forecast, availability, and contractual evidence.
- **unknown:** Whether a common reconciliation method works across OSDs, generation technologies, SCADA vendors, and commercial arrangements.
- **unknown:** Actual customer acceptance of subscription, setup, or outcome-linked pricing.
- **unknown:** Manual exception time and secure operating cost per asset.
- **unknown:** The cheapest proof’s cash requirement; the dossier’s PLN 25,000–60,000 range remains an unverified planning estimate.

## Indispensable-Premise Check

- **unknown:** No located public evidence directly tests the indispensable premise that enough eligible portfolios contain consequential, economically material reconciliation or deadline failures.
- **unknown:** No indispensable premise was directly contradicted in the located public record, but public absence is not affirmative proof.
- **contradicted:** Universal eligibility, automatic recoverability, and mechanical headline-price valuation are directly contradicted; none is indispensable if the service screens connection terms and records uncertain outcomes.
- **interpreted:** The decisive private test remains ten authorized assets or asset groups, with success only where at least 20% show a material consequence confirmed by the owner or qualified counsel.

## Query And Source Trace

- **verified:** 2019-06-05 — Regulation (EU) 2019/943, Article 13: [https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32019R0943](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32019R0943)
- **verified:** Accessed 2026-08-22 — PSE compensation, eligibility, support-notice, evidence, and authority guidance: [https://www.pse.pl/pl_PL/redysponowanie-nierynkowe](https://www.pse.pl/pl_PL/redysponowanie-nierynkowe)
- **verified:** Accessed 2026-08-22 — PSE IRiESP update containing the 180-day expiry, correction, settlement, and complaint rules: [https://www.pse.pl/documents/20182/5316414280/karta_aktualizacji_nr_2_2024_final.pdf/42ad5023-4530-47ab-b419-a6f3bd592437](https://www.pse.pl/documents/20182/5316414280/karta_aktualizacji_nr_2_2024_final.pdf/42ad5023-4530-47ab-b419-a6f3bd592437)
- **verified:** Accessed 2026-08-22 — current PSE application conditions and authorization documents: [https://www.pse.pl/documents/20182/4168830618/Warunki_skladania_Wniosku_o_rekompensate.pdf](https://www.pse.pl/documents/20182/4168830618/Warunki_skladania_Wniosku_o_rekompensate.pdf)
- **verified:** Updated 2026-04-01; accessed 2026-08-22 — WOZE roles and owner/service-provider access: [https://www.pse.pl/WOZE](https://www.pse.pl/WOZE)
- **verified:** 2026-03-10 — PSE correction to calculation rules, applicable to settlements after 2026-03-03: [https://www.pse.pl/-/korekta-zasad-wyliczania-rekompensaty-za-redysponowanie-nierynkowe-instalacji-oze](https://www.pse.pl/-/korekta-zasad-wyliczania-rekompensaty-za-redysponowanie-nierynkowe-instalacji-oze)
- **verified:** Updated 2026-08-06 — URE renewable-installation register through 2026-06-30: [https://ure.gov.pl/pl/oze/potencjal-krajowy-oze/8108%2CInstalacje-odnawialnych-zrodel-energii-stan-na-30-czerwca-2026-r.html](https://ure.gov.pl/pl/oze/potencjal-krajowy-oze/8108%2CInstalacje-odnawialnych-zrodel-energii-stan-na-30-czerwca-2026-r.html)
- **interpreted:** Accessed 2026-08-22 — OdzyskOZE pricing, process, and express absence of real customer case studies: [https://odzyskoze.pl/en/](https://odzyskoze.pl/en/)
- **counsel-required:** 2026-06-05 — Ministry of Digital Affairs summary of amended KSC obligations: [https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych)

1. `site:ure.gov.pl OR site:pse.pl Poland number renewable generators photovoltaic installations redispatch 2025 payer denominator`
2. `site:pse.pl redysponowanie nierynkowe wniosek pełnomocnictwo operator właściciel instalacji rekompensata`
3. `Poland OZE curtailment compensation claims success fee customer case study OdzyskOZE`
4. `site:pse.pl redysponowanie nierynkowe dane pomiarowe SCADA dostęp właściciel operator instrukcja`
5. `site:pse.pl WOZE rekompensata redysponowanie nierynkowe samodzielnie wniosek operator calculation route`
6. `site:gov.pl OR site:ure.gov.pl OZE SCADA cyberbezpieczeństwo NIS2 operator Polska obowiązki 2026`
7. `site:eur-lex.europa.eu 2019/943 Article 13 7 non-market-based redispatching financial compensation exact rule`
8. `site:pse.pl warunki wniosku rekompensata PV FW dokumenty dane pomiarowe cheapest historical audit proof`

