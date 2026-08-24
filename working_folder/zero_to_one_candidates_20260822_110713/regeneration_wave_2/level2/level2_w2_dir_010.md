# W2-L2-010 — Solar-inverter warranty exchange merchant

**Research date:** 2026-08-22, Europe/Warsaw  
**Concept:** Buy an eligible failed inverter from an installer, immediately supply an owned replacement, and retain the failed unit plus any lawful repair, warranty-replacement, parts, or resale recovery.

## Executive finding

Poland has a large installed base: 1,636,673 renewable micro-installations at year-end 2025, 99.9% of them photovoltaic. This provides the denominator but not the annual exchange demand. [URE](https://ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html)

The transaction is technically possible, but the profitable subset is narrower than “failed inverter”:

- The owner must be free to transfer the unit and relevant warranty rights.
- The manufacturer must either accept the assignee or the recovery must work without a manufacturer claim.
- The unit cannot be subject to a grant-retention restriction.
- It must remain equipment suitable for inspection or repair rather than being handled unlawfully as waste.
- A compatible, grid-compliant replacement must be available quickly and cheaply.
- The installer must value immediate certainty more than the manufacturer’s existing RMA route.

Current manufacturer service can be fast: SolarEdge says it normally dispatches a qualifying replacement within 48 hours; an older Huawei EU warranty document states two to five working days after approval. These routes directly compete with the exchange proposition. [SolarEdge](https://www.solaredge.com/pl/warranty), [Huawei EU warranty](https://solar.huawei.com/~/media/Solar/attachment/pdf/eu/service/warranty/EU_Warranty_conditions.pdf)

Accordingly, the initial product should be a narrowly defined B2B exchange for documented models where the entrant can quote a fixed price, confirm title eligibility, and deliver faster or with less uncertainty than the incumbent route.

## Verified problem and payer evidence

### Verified evidence

- Poland had **1,636,673 micro-installations and nearly 13.9 GW** at the end of 2025; PV represented 99.9%. [URE](https://ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html)
- The EU Joint Research Centre reports an assumed inverter life of approximately **10–15 years**, more failures early and late in life, standard string-inverter warranties commonly around ten years, and possible difficulty finding equivalent form/fit/function after 10–15 years. It also notes that inverter failure does not necessarily require replacement. [JRC](https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/contentype/product_group_documents/1581689975/Draft_Report_Task4%20Master%20REV%20-%20to%20publish.pdf)
- A Polish distributor advertised new inverter prices from **2,890 PLN net to 8,720 PLN net** across selected SolarEdge, Fronius, Huawei, GoodWe, and Solplanet models. These are promotional listings, not confirmed repeatable wholesale terms. [ACTION](https://fotowoltaika.action.pl/oferta-specjalna)
- The cited Huawei terms require fault information, serial number, and purchase receipt. After replacement, the new unit belongs to the customer and the defective unit belongs to Huawei. [Huawei EU warranty](https://solar.huawei.com/~/media/Solar/attachment/pdf/eu/service/warranty/EU_Warranty_conditions.pdf)
- SolarEdge’s Polish offer says a qualifying replacement is normally dispatched within 48 hours. [SolarEdge](https://www.solaredge.com/pl/warranty)

### Interpretation

The payer’s problem is not simply hardware failure. It is the combination of:

1. another site visit;
2. diagnosis and documentation work;
3. uncertain claim acceptance;
4. reputational exposure while the plant is down;
5. replacement-stock financing; and
6. responsibility for compatibility and recommissioning.

The exchange merchant monetizes certainty: a named unit, fixed exchange price, explicit failed-unit credit, and immediate availability. The strongest cases are likely discontinued models, out-of-warranty units, uncertain claims, missing local stock, or installers unwilling to finance and administer recovery.

### Unknowns

No researched source provides Polish annual inverter failure incidence, installer service-call costs, median downtime, installer count, or willingness to pay for exchange. These require transaction-level fieldwork.

## Exact transaction

1. Installer submits model, serial number, fault code, photographs, commissioning date, proof of purchase, system configuration, and grant status.
2. Entrant checks compatibility, title, warranty eligibility, grant restrictions, serial authenticity, and replacement availability.
3. Entrant quotes:

   - owned replacement selling price;
   - failed-unit credit;
   - resulting net exchange invoice;
   - deposit;
   - delivery/collection terms; and
   - conditions that invalidate the credit.

4. Property owner signs title and warranty-right documentation. Installer confirms its authority to remove the unit.
5. Installer pays a reservation deposit.
6. Entrant dispatches or releases an owned replacement.
7. Qualified installer replaces and recommissions the inverter and remains responsible for installation workmanship.
8. At handover, installer pays the balance and transfers physical possession and valid title to the failed unit.
9. Entrant follows one documented recovery path:

   - disclosed warranty claim as legitimate assignee;
   - repair, test, and disclosed refurbished resale;
   - parts recovery;
   - or compliant end-of-life handling.

10. If a warranty replacement is received, the defective unit goes to the manufacturer where the terms require it; the resulting replacement becomes merchant inventory.

## Incentive and power map

| Party | Incentive | Control or power | Principal exposure |
|---|---|---|---|
| PV owner | Restore generation and preserve warranties | Authorizes removal and title transfer | Downtime, grant breach, incompatible replacement |
| Installer | Close service call quickly and protect reputation | Diagnoses, installs, recommissions, influences supplier | Repeat visits and workmanship |
| Exchange merchant | Earn exchange margin plus recovery value | Owns replacement inventory and validly acquired failed units | Title, authenticity, recovery, inventory and price risk |
| Manufacturer | Limit claims to eligible units | Determines warranty acceptance and replacement timing | Contractual warranty cost |
| Distributor | Sell available stock | Controls wholesale availability and credit | Stock and counterparty exposure |
| OSD | Preserve safe grid operation | Applies connection documentation and technical requirements | Grid compliance |
| Grant administrator | Enforce programme durability | Can restrict disposal or sale | Subsidy clawback |
| Repair/refurbishment partner | Earn diagnostic and repair fees | Determines repairability and evidence quality | Workmanship and parts availability |
| End-of-life operator | Lawful disposal/recovery | Required where the unit is waste | Environmental compliance |

## Payer denominator

The national top-level denominator is approximately **1.635 million PV micro-installations**. It is not an annual demand figure.

A useful serviceable denominator is:

> installed compatible units × annual qualifying failures × installer willingness to outsource × transferable-title share × recoverable-unit share

All factors after installed units remain unknown.

For scale context only:

| Mature annual exchanges | Share of 2025 micro-installation base |
|---:|---:|
| 900 | 0.055% |
| 2,500 | 0.153% |
| 6,000 | 0.367% |

The actual payer denominator is the number of installers responsible for legacy service work. That number was not established within the packet’s source budget.

## Price, unit economics, and cash timing

### Illustrative expected transaction, PLN net

| Component | PLN |
|---|---:|
| Replacement price before failed-unit credit | 6,700 |
| Failed-unit credit | (800) |
| Installer’s net exchange invoice | **5,900** |
| Eventual recovery sale/value | 1,300 |
| Recognized economic revenue | **7,200** |
| Replacement acquisition | (4,300) |
| Two-way logistics | (250) |
| Diagnosis and administration | (250) |
| Repair/refurbishment allowance | (400) |
| return, rejection, and warranty reserve | (300) |
| Gross contribution | **1,700** |
| Gross margin | **23.6%** |

This is a planning model, not observed trading history. Recovery can be zero; without recovery the example contributes only 600 PLN before overhead.

### Cash cycle

- Deposit: target 50% of exchange invoice at reservation.
- Replacement purchase: commonly before delivery unless already held.
- Balance: due on collection or installation handover.
- Failed-unit recovery: approximately 15–90 days in the model.
- Peak transaction cash exposure: roughly 2,000–6,000 PLN with a deposit; greater for high-power units or rejected credits.
- Inventory concentration is the central cash risk: model-specific stock may remain unsold while a different model is urgently required.

The cited Huawei document permits warranty transfer to an assignee under stated conditions, but requires documentation and transfers the defective product to Huawei after replacement. It promises delivery only after the claim has been logged, investigated, and approved. [Huawei EU warranty](https://solar.huawei.com/~/media/Solar/attachment/pdf/eu/service/warranty/EU_Warranty_conditions.pdf)

## Founder-wealth cases

These are internally consistent operating cases, not forecasts. Revenue includes exchange invoices and realized recovery sales. Business values exclude operating cash assumed necessary for the stated volume. Founder distributions are added only after being removed from the company; retained earnings are not added again.

| Item | Conservative | Expected | Strong |
|---|---:|---:|---:|
| Annual jobs: Y1 / Y3 / Y7 | 60 / 350 / 900 | 100 / 700 / 2,500 | 120 / 1,500 / 6,000 |
| Y7 revenue/job | 6,400 PLN | 7,200 PLN | 7,800 PLN |
| Y7 revenue | 5.76m PLN | 18.00m PLN | 46.80m PLN |
| Gross margin | 23% | 32% | 38% |
| Y7 gross profit | 1.32m PLN | 5.76m PLN | 17.78m PLN |
| Operating margin | 7% | 15% | 22% |
| Y7 operating profit | 0.40m PLN | 2.70m PLN | 10.30m PLN |
| Founder capital | 100k PLN | 100k PLN | 100k PLN |
| Maximum inventory debt | 250k PLN | 700k PLN | 1.5m PLN |
| New equity | None | None | 1.0m PLN for 10% |
| Founder ownership | 100% | 100% | 90% |
| Illustrative value basis | 2.5× operating profit | 4× operating profit | 5× operating profit |
| Net debt at value date | 150k PLN | 600k PLN | 1.2m PLN |
| Founder business equity | 0.86m PLN | 10.20m PLN | 45.25m PLN |
| Cumulative founder after-tax distributions | 0.05m PLN | 0.75m PLN | 2.00m PLN |
| Founder wealth represented here | **0.91m PLN** | **10.95m PLN** | **47.25m PLN** |
| Timing | End Y8 | End Y7 | End Y7 |

Assumptions:

- Conservative: founder remains employed through Y7; 95% of after-tax distributable cash is reinvested and optional distributions do not exceed 5%.
- Expected: founder remains employed through Y3 and reinvests 95% during that period; after leaving employment, 70% is retained for inventory and expansion.
- Strong: founder remains employed through Y2 and reinvests 100% during that period; afterward 75% is retained.
- Debt is company inventory finance. Personal guarantees are excluded; if required, founder capital at risk rises.
- The value multiples are scenario assumptions, not sourced transaction multiples. A small inventory merchant without proprietary procedures, contracts, or repeat customers may command materially less.
- Tax rates, eligibility for any used-goods VAT treatment, and transaction-specific VAT consequences require Polish accounting advice.

## Acquisition route

The family-accessible renewable installer is the first distribution channel, evidence source, and design partner. The offer should remain B2B and model-specific.

### First ten paying installers

- One family-connected installer supplies the first documented unit and paid reservation.
- Three installers introduced directly by that firm around Ostrów Wielkopolski.
- Three independent service installers reached through regional wholesalers in Kalisz and Poznań.
- Three firms with accumulated legacy service obligations, approached using a one-page model/price/collection sheet.

Each receives a quote only for models already covered by a written recovery procedure.

### First one hundred paying installers

- Fifty in Wielkopolskie and adjacent Lower Silesia through installer referrals and wholesaler-counter introductions.
- Thirty national service firms using insured courier exchange and same-day eligibility decisions.
- Twenty specialists servicing discontinued or orphaned systems.
- Expansion remains limited to models with repeatable acquisition, commissioning, documentation, and recovery histories.

No camera-led or influencer distribution is required. The sales artifact is an availability matrix showing model, compatible replacement, exchange price, deposit, dispatch time, and document checklist.

## Control and compounding asset

The accumulating asset is the combination of:

- replacement and recovered inventory;
- serial-level model and fault history;
- documentation-completeness and claim-acceptance outcomes;
- acquisition, repair, and resale cost by model;
- compatibility and recommissioning procedures;
- installer payment and return performance;
- signed title and failed-unit-credit forms; and
- repeat installer contracts.

The data should progressively improve the failed-unit credit and identify which models merit stocked replacements. Manufacturers and national distributors possess stronger upstream information, so the defensible element is the local transaction history and installer workflow, not fault data alone.

## Incumbent route-around

The main route-arounds are:

1. **Manufacturer advance RMA.** SolarEdge advertises dispatch within 48 hours for qualifying defects; Huawei’s cited document states two to five working days after approval.
2. **Installer self-financing.** The installer buys a replacement at distributor pricing and later keeps any warranty recovery.
3. **Distributor service desk.** A distributor can bundle credit, inventory, and manufacturer access.
4. **Manufacturer-controlled title.** Under the cited Huawei terms, the failed unit becomes Huawei’s property after replacement, preventing a second recovery.
5. **On-site repair.** JRC notes that larger central inverters are commonly repaired on site.
6. **Direct refurbished sourcing.** An installer can buy a used unit without transferring its failed unit.
7. **OEM policy changes.** A manufacturer can restrict assignees, require original invoices, or supply functionally equivalent newer units.

The entrant therefore needs value in cases where standard RMA is unavailable, uncertain, slow in practice, or administratively unattractive—not merely where an inverter has failed.

## Rules and constraints

| Constraint | Classification | Practical treatment |
|---|---|---|
| Safe electrical replacement and recommissioning | Technical/regulatory | Work remains with a properly qualified installer; merchant does not bypass protections. |
| Grid documentation and NC RfG conformity | Regulatory/OSD process | Retain certificates and settings. Obtain OSD confirmation before treating a changed model or parameter set as a simple swap. |
| Warranty transfer and claim evidence | Manufacturer contract | Check current terms by serial/model; use disclosed assignment and genuine documentation only. |
| Defective-unit ownership after RMA | Manufacturer contract/property | Do not claim residual title where the warranty gives the unit to the manufacturer. |
| Mój Prąd durability | Grant condition | Exclude units that must be retained and may not be sold during the applicable period. |
| Equipment versus waste status | Environmental | Record intent and condition; use a compliant end-of-life operator where the unit is waste. |
| Refurbished resale disclosure | Product/commercial law | Sell only accurately described, tested units with traceable serials and written warranty terms. |
| VAT and invoicing | Tax | Use ordinary VAT invoices unless an accountant confirms another treatment. |
| Authenticity | Contract/product safety | Source serial-verified replacements and reject counterfeit or altered units. |

Government connection guidance requires technical documentation, NC RfG evidence, legal-title statements, and an installer statement concerning qualifications and compliance for a micro-installation notification. Whether every like-for-like inverter replacement requires a new notification remains unresolved. [National RES Contact Point](https://www.gov.pl/web/national-contact-point-for-renewable-energy-sources/micro-system-notification)

Mój Prąd guidance states that, for specified programme editions, an replaced inverter must be retained for three or five years after subsidy payment and cannot be sold or discarded during that period. [Mój Prąd FAQ](https://mojprad.gov.pl/faq/)

Official programme guidance also identifies inverters as equipment subject to end-of-life handling rules. It does not, by itself, settle when a particular failed unit becomes legally classified as waste. [Mój Prąd recycling guidance](https://mojprad.gov.pl/obowiazek-recyklingu/)

## Lawful structure

Use a Polish limited-liability operating company with:

- B2B exchange terms;
- VAT invoice for the replacement;
- separate failed-unit purchase/credit line;
- owner and installer representations concerning title, grant status, serial number, and authority;
- assignment only of warranty rights that are legally and contractually transferable;
- manufacturer-specific eligibility checklist;
- qualified installer responsibility for removal, installation, settings, testing, and commissioning;
- no claim submission under another party’s identity;
- no recovery attributed to the merchant until the manufacturer accepts the claimant and chain of title;
- test reports and conspicuous refurbished status for resale;
- compliant waste handoff where repair or reuse is not the documented purpose; and
- product-liability, stock, transit, and errors-and-omissions insurance appropriate to actual activities.

## Dependencies

- Repeated access to failed units with complete documentation.
- Reliable distributor stock and credit.
- Qualified installer partners.
- Manufacturer-specific current warranty terms.
- A repair partner able to issue serial-linked test reports.
- Insured reverse logistics.
- Accountant advice on VAT and inventory recognition.
- Polish counsel on title assignment, consumer-facing resale, grant restrictions, and waste classification.
- Sufficient demand for repaired or warranty-replacement units.
- Model-level compatibility and grid-setting procedures.

## Fastest paid proof and capital at risk

### Paid proof

Within one transaction cycle:

1. Obtain one failed unit record through the family firm without taking title yet.
2. Collect serial, fault code, invoice, commissioning evidence, grant status, and photographs.
3. Source one confirmed compatible replacement.
4. Issue a written exchange quote.
5. Receive a paid reservation deposit.
6. Complete a qualified installation.
7. Execute the title-transfer document and collect the invoice balance.
8. Attempt the pre-declared recovery path and record every cost and elapsed day.

The paid reservation—not a non-binding expression of interest—is the proof event.

### Capital

- Initial operating envelope: **12,000–30,000 PLN**.
- One replacement and logistics: approximately 4,000–10,000 PLN.
- Legal/accounting documents and insurance: approximately 3,000–8,000 PLN.
- Diagnostic, packaging, courier, and contingency: approximately 2,000–5,000 PLN.
- Remaining capacity funds a second unit or covers a rejected recovery.

Do not deploy the founder’s full 100,000 PLN before several completed exchanges establish title validity, true contribution, cash-cycle duration, and recovery demand.

## Kill criteria

Stop adding inventory or new models if any of the following occurs:

- Twenty relevant installer conversations produce fewer than three paid reservations.
- Ten completed exchanges produce average gross contribution below 1,000 PLN after rejected credits, logistics, repair, and warranty losses.
- Standard manufacturer or distributor RMA restores service as fast as the promised exchange for most documented failures.
- Title, grant, or waste restrictions exclude most offered failed units.
- Compatible replacement stock cannot be confirmed before taking deposits.
- Recovery proceeds remain uncollected beyond 90 days in more than one-third of completed cases.
- Warranty rejection or compatibility-related returns consume more than 10% of recognized revenue.
- Working capital reaches 100,000 PLN before achieving twenty completed exchanges per month.
- A qualified installer or insurer will not accept the proposed responsibility split.

## Decision-critical unknowns

1. Current Polish warranty terms for each target model; the Huawei document found is dated 2018.
2. Whether manufacturers accept the merchant as assignee in practice.
3. Actual annual failures by model and installation year.
4. Installer cost of repeat visits and claim administration.
5. Real dispatch-to-recommissioning time under incumbent RMA routes.
6. Current wholesale pricing and stock depth.
7. Whether a specific replacement requires an OSD update or new documentation.
8. Grant-retention prevalence among failed systems.
9. Legal equipment/waste boundary for received failed units.
10. Repair yield, parts availability, and test cost.
11. Demand and lawful warranty terms for refurbished units.
12. Bad-title, counterfeit, and serial-mismatch incidence.
13. Insurer treatment of refurbished inverter sales.
14. Customer credit behavior and deposit acceptance.
15. Appropriate VAT treatment for each recovery path.

## Development status

Research packet completed. No paid reservation, title transfer, completed exchange, recovery outcome, installer cohort, or model-level failure dataset has been observed. Verified evidence currently covers the installed base, advertised replacement pricing, selected manufacturer mechanics, grid-notification documentation, and specific grant/end-of-life constraints.

## Query ledger

Timestamp precision is the access date; the research interface did not expose wall-clock query times. All queries were run on **2026-08-22, Europe/Warsaw**.

| ID | Exact query | Useful result |
|---|---|---|
| Q1 | `Poland photovoltaic installers inverter failure replacement downtime warranty claim market 2025` | URE installed base; adjacent service material |
| Q2 | `Poland installed photovoltaic systems inverter installed base 2025 URE PTPiREE report` | URE year-end 2025 denominator |
| Q3 | `Poland solar inverter replacement price Huawei SUN2000 Fronius Symo SolarEdge commercial distributor PLN` | ACTION net price listings |
| Q4 | `solar inverter failure rate warranty claim replacement downtime Europe study` | JRC lifetime and replacement discussion |
| Q5 | `site:solar.huawei.com Poland SUN2000 warranty terms RMA replacement inverter failed unit` | Huawei EU warranty document |
| Q6 | `site:solaredge.com warranty Europe inverter RMA replacement ownership failed product Poland` | SolarEdge Polish protection/RMA page |
| Q7 | `site:fronius.com Poland inverter warranty service exchange replacement terms` | No source used; returned material did not establish relevant Polish exchange terms |
| Q8 | `Poland official law photovoltaic inverter replacement grid code settings refurbished electrical equipment WEEE sale` | Government connection, grant-retention, and end-of-life guidance |

Exactly eight distinct queries were executed.

## Source ledger

All useful sources accessed **2026-08-22, Europe/Warsaw**.

| ID | Source | Type | Evidence used |
|---|---|---|---|
| S1 | [URE: more than 1.6m micro-installations](https://ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/13173%2CRaport-URE-w-Polsce-mamy-juz-ponad-16-mln-mikroinstalacji-OZE.html) | Regulator | Installed base, PV share, capacity |
| S2 | [ACTION special offer](https://fotowoltaika.action.pl/oferta-specjalna) | Commercial distributor | Advertised net inverter prices |
| S3 | [JRC preparatory report](https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/contentype/product_group_documents/1581689975/Draft_Report_Task4%20Master%20REV%20-%20to%20publish.pdf) | EU technical authority | Lifetime, warranties, repair and replacement observations |
| S4 | [Huawei EU warranty V3.0](https://solar.huawei.com/~/media/Solar/attachment/pdf/eu/service/warranty/EU_Warranty_conditions.pdf) | Manufacturer contract | Transfer, documentation, timing, title, exclusions |
| S5 | [SolarEdge Poland protection package](https://www.solaredge.com/pl/warranty) | Manufacturer commercial terms | Claimed 48-hour qualifying replacement dispatch |
| S6 | [National RES Contact Point: micro-system notification](https://www.gov.pl/web/national-contact-point-for-renewable-energy-sources/micro-system-notification) | Government procedural authority | Qualifications, documentation, NC RfG and title statements |
| S7 | [Mój Prąd FAQ](https://mojprad.gov.pl/faq/) | Official programme guidance | Inverter retention and sale restriction |
| S8 | [Mój Prąd recycling guidance](https://mojprad.gov.pl/obowiazek-recyklingu/) | Official programme guidance | End-of-life obligations covering inverters |

A SolarEdge reimbursement PDF was opened but returned an internal rendering error. It supplied no evidence and is not counted as a useful source.

## Evidence ledger

| Evidence | Status | Source |
|---|---|---|
| 1,636,673 micro-installations at end-2025 | Verified | S1 |
| PV represents 99.9% of micro-installations | Verified | S1 |
| Selected advertised inverter prices span 2,890–8,720 PLN net | Verified promotional snapshot | S2 |
| Inverter life is commonly modeled at 10–15 years | Verified secondary technical synthesis | S3 |
| Failure need not require replacement | Verified technical observation | S3 |
| Equivalent replacements may become difficult after 10–15 years | Verified technical observation | S3 |
| Huawei warranty may transfer to an assignee subject to conditions | Verified for the dated document | S4 |
| Huawei requires fault information, serial number, and purchase receipt | Verified for the dated document | S4 |
| Huawei replacement changes title to the replacement and defective products | Verified for the dated document | S4 |
| Huawei states two-to-five-working-day delivery after claim approval | Verified for the dated document | S4 |
| SolarEdge says qualifying replacements normally dispatch within 48 hours | Verified current website statement | S5 |
| Micro-installation notification documentation includes NC RfG and installer declarations | Verified government guidance | S6 |
| Some Mój Prąd recipients must retain a replaced inverter and may not sell it during durability | Verified programme guidance | S7 |
| Official end-of-life guidance expressly includes inverters | Verified programme guidance | S8 |
| Installer willingness to pay, failure incidence, recovery value, and margins | Unknown; scenario assumptions only | No source |
| Founder-wealth figures and business-value multiples | Interpretation/model | No source |
