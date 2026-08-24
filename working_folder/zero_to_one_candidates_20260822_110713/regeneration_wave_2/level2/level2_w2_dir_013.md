# W2-L2-013 — Metered electric drying capacity for grain stores

**Research timestamp:** 2026-08-22T15:01:28+02:00  
**Concept:** A venture-owned modular electric heat-and-airflow unit installed at a grain store, with the venture purchasing electricity through the site’s approved dynamic retail arrangement and invoicing for measured moisture removal per tonne.

## 1. Problem and payer evidence

### Verified evidence

- Poland harvested approximately **35.0 million tonnes of grain in 2024**, including **9.4 million tonnes of maize**. The agriculture ministry also reported grain-storage problems involving pests and fumigation. Grain purchase prices in December 2024 were approximately 938 PLN/t for consumption wheat and 842 PLN/t for maize, making degradation of a stored batch economically material. [MRiRW agricultural-market memorandum](https://www.gov.pl/attachment/7db41037-4c86-4843-9a2c-9aa6c8c9726d)
- Grain above roughly **14.5% moisture is unsuitable for long-term storage without conservation**; excess moisture promotes respiration loss, fungi, microorganisms and storage pests. European farm dryers typically work only **100–1,000 hours annually**, confirming both the problem and the utilization risk. [Grube and Böckelmann, *Key figures for grain drying*](https://www.agricultural-engineering.eu/landtechnik/article/download/2011-66-4-276-281/2011-66-4-276-281-en-pdf/678)
- During the wet 2025 Polish harvest, commercial drying was commonly charged by the **tonne-percentage-point**: 15–25 PLN, most often 15–20 PLN. Loading and unloading were commonly another 8–10 PLN/t. The reported all-in alternative was 50–80 PLN/t for cereals. [WRP commercial drying-price report](https://www.wrp.pl/ceny/ile-kosztuje-suszenie-zboz-i-rzepaku-usluga-w-tym-roku-bardzo-popularna-2666756)
- Polish dynamic-price contracts can use day-ahead prices published at 14:00 on the preceding day, but require remotely read settlement metering. The investigated retail offers added approximately **0.0999–0.149 PLN/kWh** plus possible monthly fees to wholesale prices; actual average customer prices in the reported period exceeded 0.50 PLN/kWh. [URE dynamic-contract analysis](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12692%2CRaporty-i-analizy-URE-w-ubieglym-roku-135-odbiorcow-skorzystalo-z-umow-z-cena-dy.html)
- Negative wholesale prices do occur: on 23 June 2024, Poland recorded seven consecutive negative-price hours, from −30.43 to −88.81 PLN/MWh. These events are evidence of dispatch opportunity, not evidence of a dependable annual electricity cost. [URE negative-price notice](https://www.ure.gov.pl/pl/oze/swiadectwa-pochodzenia/ceny-ujemne/12037%2CWytworcy-energii-z-OZE-po-raz-kolejny-musza-skorygowac-wnioski-o-wydanie-swiadec.html)

### Interpretation

The payer is not buying electricity. It is buying a measurable conversion of wet, storage-unstable grain into grain meeting an agreed moisture range without transporting it to a third-party dryer. The economic comparison is therefore:

> service charge + site handling + crop risk  
> versus external drying + two-way handling/transport + delay + degradation risk.

Large farms, warehouses and cooperatives are the natural payers because they can provide enough batch volume, electrical infrastructure and repeat utilization. Small farms are more likely to be reached through a cooperative or shared store.

### Unverified claims not used

No claim is made that electric heat is inherently cheaper than LPG, gas or biomass, or that negative-price hours will coincide reliably with permissible drying windows.

## 2. Transaction, incentives and power

| Party | Gives | Receives | Incentive | Effective power |
|---|---|---|---|---|
| Grain owner/warehouse | Grain access, site access, batch records, payment | Measured moisture removal and storage stabilization | Avoid degradation, transport and fuel exposure | Can approve the batch and refuse site access |
| Venture | Equipment, dispatch, metering, maintenance and performance obligation | Service fee per tonne-percentage-point | Maximize safe utilization and electricity spread | Owns equipment, software and service contract |
| Site owner | Electrical connection, ventilation interface and hosting area | Hosting consideration or lower drying cost | Monetize existing infrastructure | Controls physical installation and connection |
| Electricity supplier | Retail energy under an approved contract | Energy payment, markup and fees | Sell incremental load | Controls price formula and contractual eligibility |
| Distribution operator | Connection capacity and metering interface | Network charges | Safe grid operation | Can constrain or delay increased connection power |
| Grain-handling operator | Loading, turning, sampling and unloading | Handling charge or internal operating benefit | Protect throughput and grain quality | Controls operational procedures |
| Certified electrician/integrator | Design, protection, installation and acceptance documentation | Installation fee | Repeat farm electrification work | Can block unsafe commissioning |
| Independent sampler/laboratory | Intake and completion moisture records | Testing fee | Neutral measurement | Resolves billing and quality disputes |
| Downstream grain buyer | Acceptance and quality specification | Stable grain | Reliable commodity quality | Can reject grain despite nominal moisture |
| Insurer/lender | Liability or equipment capital | Premium, interest and covenants | Controlled loss exposure | Can limit crops, temperatures or installations |

The venture bears equipment utilization, purchased-energy and agreed drying-performance risk. Grain title stays with the customer. The customer retains disclosed risks arising from pre-existing contamination, immature grain, handling and storage conditions outside the venture’s control.

## 3. Payer denominator

### Verified denominator

- Total Polish grain harvested in 2024: approximately **35.0 million tonnes**.
- Maize: approximately **9.4 million tonnes**.

### Mechanical denominator, not observed demand

If the 9.4 million tonnes of maize required an average seven percentage points of moisture reduction:

\[
9.4m\ tonnes \times 7 = 65.8m\ tonne\text{-}percentage\text{-}points
\]

At 15–20 PLN per tonne-point, that mechanical base corresponds to **987 million–1.316 billion PLN** of drying charges. It is not an estimate of actual obtainable spend because the following are unknown:

- harvested-moisture distribution;
- share already served by owned dryers;
- share stored without artificial drying;
- site power and ventilation compatibility;
- geographic density and timing;
- customers’ willingness to substitute electricity for existing fuels.

KONSIL’s commercial claim of 15,275 silos sold, 900,000 tonnes of associated storage and 15,000 Polish customers demonstrates a reachable equipment-owner channel, but it is neither a national site count nor an independent market statistic. [KONSIL](https://www.konsil.pl/)

## 4. Price, unit economics and cash timing

### Billing unit

One **tonne-point** means reducing the moisture reading of one intake tonne by one percentage point, subject to an agreed sampling protocol. A 100-tonne batch reduced from 19% to 14% produces 500 billable tonne-points.

The contract should specify:

- intake mass source;
- representative sampling locations and frequency;
- meter model, calibration and dispute procedure;
- target moisture range rather than a single exact reading;
- maximum grain and air temperatures;
- treatment of uneven batches and pre-existing damage.

### Energy physics

For one intake tonne reduced from 19% to 14%, the approximate water removed is:

\[
1,000 \times \frac{19-14}{100-14}=58.1\ kg
\]

That is about **11.6 kg of water per tonne-point**.

Published European figures for in-store aeration drying are approximately 0.85 kWh of thermal energy plus 0.3–1.0 kWh of electrical energy per kilogram of moisture removed. With resistance heat replacing thermal fuel, an indicative combined range is therefore approximately **13.4–21.5 kWh per tonne-point**. Crop, maturity, weather and equipment can move specific energy by at least 20%, and poor air distribution can worsen it further. [Grube and Böckelmann](https://www.agricultural-engineering.eu/landtechnik/article/download/2011-66-4-276-281/2011-66-4-276-281-en-pdf/678)

### Modeled operating cases per tonne-point

All prices are net of VAT and exclude grain loading/unloading.

| Input | Conservative | Expected | Strong |
|---|---:|---:|---:|
| Service price | 15.00 PLN | 16.00 PLN | 18.00 PLN |
| Electricity use | 20 kWh | 17 kWh | 14 kWh |
| Weighted all-in electricity cost | 0.50 PLN/kWh | 0.38 PLN/kWh | 0.30 PLN/kWh |
| Electricity expense | 10.00 PLN | 6.46 PLN | 4.20 PLN |
| Field labour, hosting, meter and maintenance | 3.00 PLN | 2.40 PLN | 2.30 PLN |
| Gross contribution | 2.00 PLN | 7.14 PLN | 11.50 PLN |
| Gross margin | 13% | 45% | 64% |

The electricity-cost assumptions include energy, retail markup and variable network charges. They are scenario assumptions, not quoted tariffs. The strong case does not assume that electricity is purchased at negative prices.

### Module capacity

For a 60 kW module:

| Input | Conservative | Expected | Strong |
|---|---:|---:|---:|
| Productive hours/year | 700 | 1,100 | 1,400 |
| Tonne-points/hour | 3.0 | 3.53 | 4.29 |
| Tonne-points/module/year | 2,100 | 3,882 | 6,000 |
| Revenue/module/year | 31,500 PLN | 62,112 PLN | 108,000 PLN |

### Cash timing

- Customer supplies a deposit equal to forecast electricity expense before dispatch.
- Venture pays the supplier/site settlement monthly or under the approved hosting arrangement.
- Completion measurement occurs immediately after the batch.
- Final invoice is due within 7–14 days; disputed moisture value, not the whole invoice, is held back.
- A 200-tonne batch reduced by five points creates 1,000 tonne-points: expected revenue 16,000 PLN and modeled electricity expense about 6,460 PLN.
- Without a deposit, a large fleet creates material peak-season working-capital exposure even though the service cycle is short.

## 5. Founder-wealth cases

These are internally consistent operating scenarios, not forecasts. Year 1 begins with the first paid batch. No grants are assumed.

### Conservative — year 8

- Fleet: 10 modules.
- Annual volume: 21,000 tonne-points.
- Revenue: **315,000 PLN**.
- Gross margin: **13%**.
- Operating margin: **−15%**, approximately −47,000 PLN.
- Capital deployed: **650,000 PLN**.
- Funding: 100,000 PLN founder capital, 250,000 PLN external equity and 300,000 PLN equipment debt.
- Ownership: founder **75%** after dilution.
- Reinvestment: 95% of after-tax distributable cash; none exists in this case.
- Optional distributions: **zero**.
- Year-8 net debt: approximately 250,000 PLN.
- Value: no going-concern value assigned. At 35% equipment recovery, fleet proceeds are approximately 193,000 PLN and do not cover debt.
- Founder business equity value: **zero**.

This case represents insufficient utilization and no economic fleet-scale operation.

### Expected — year 8

- Fleet: 120 modules.
- Annual volume: **465,840 tonne-points**.
- Revenue: **7.45 million PLN**.
- Gross margin: **45%**.
- Operating margin: **22%**.
- EBITDA: approximately **1.64 million PLN**.
- Capital deployed across the period: **10.0 million PLN**.
- Funding: 100,000 PLN founder capital, 2.4 million PLN external equity, 5.0 million PLN cumulative retained after-tax cash and 2.5 million PLN debt raised.
- Year-8 net debt: **1.5 million PLN**.
- Ownership: founder **75%**.
- Reinvestment: **95%** of after-tax distributable cash while the founder remains employed.
- Optional distributions: **zero** in the model.
- Assumed enterprise value: 5× EBITDA = **8.20 million PLN**.
- Equity value after net debt: **6.70 million PLN**.
- Founder share: approximately **5.02 million PLN** in year 8.

Retained earnings are not added separately: they fund the fleet and are reflected only through enterprise value. At 4× EBITDA, the same case produces approximately **3.79 million PLN** of founder equity, showing its dependence on both operating performance and exit pricing.

### Strong — year 8

- Fleet: 240 modules.
- Annual volume: **1.44 million tonne-points**.
- Revenue: **25.92 million PLN**.
- Gross margin: **64%**.
- Operating margin: **34%**.
- EBITDA: approximately **8.81 million PLN**.
- Capital deployed: **18.5 million PLN**.
- Funding: 100,000 PLN founder capital, 4.0 million PLN external equity, 10.4 million PLN cumulative retained after-tax cash and 4.0 million PLN debt raised.
- Year-8 net debt: **3.0 million PLN**.
- Ownership: founder **65%** after equity financing and employee/management dilution.
- Reinvestment: **100%** of after-tax distributable cash.
- Distributions: **zero**.
- Assumed enterprise value: 6× EBITDA = **52.88 million PLN**.
- Equity value after debt: **49.88 million PLN**.
- Founder share: approximately **32.42 million PLN**.

The strong case requires low weighted energy costs, high seasonal utilization, replicable installation and a defensible fleet operator rather than isolated equipment rentals.

## 6. Acquisition route

The family connection to a seven-person renewable installer near Ostrów Wielkopolski provides the initial route without implying privileged procurement status.

Commercial sequence:

1. Installer identifies grain customers with silos, three-phase supply and daytime PV or flexible retail contracts.
2. Venture performs a paid electrical and airflow survey.
3. Customer receives a batch quote in tonne-points, not a savings estimate.
4. A certified electrician connects the module.
5. Independent intake and completion measurements determine the invoice.
6. A one-page batch record becomes the referral artifact.
7. Installer receives a disclosed first-season commission or fixed survey fee.

Founder work can remain within five hours/day if certified installation, physical operation and sampling are contracted. The founder’s work is dispatch logic, pricing, data review, contracting and partner management. No camera-led distribution is required.

### First ten customers

- Customer 1: family-accessible agricultural site; one paid 50–100 tonne batch.
- Customers 2–4: referrals from the renewable installer’s existing farm customers.
- Customers 5–7: referrals from silo, fan and grain-handling technicians.
- Customers 8–10: one cooperative or warehouse relationship supplying multiple stores.

Each must be a paid transaction. Discounting can cover experimental risk, but electricity and field labour should not be given away.

### First one hundred customers

- 1–10: founder-led installations around southern Wielkopolska.
- 11–30: two renewable-installation partners and one grain-equipment service partner.
- 31–60: cooperative and warehouse groups capable of hosting two or more modules.
- 61–100: dealer/service agreements tied to annual pre-harvest electrical surveys.

At expected utilization, 100 one-module sites correspond to approximately 388,200 tonne-points and **6.21 million PLN** of annual revenue at 16 PLN per tonne-point. Actual customer count can be lower if warehouses host several modules.

Modeled scaled acquisition cost is 5,000–10,000 PLN per site, including survey, partner commission and commissioning. This remains an assumption requiring paid-channel evidence.

## 7. Control and compounding asset

The defensible asset is the combination of:

- site-specific connection, airflow and back-pressure maps;
- energy-price and load curves;
- crop, intake-moisture, ambient-condition and drying-response records;
- software that schedules modules against price, weather and promised completion;
- contract rights to use anonymized operating data;
- a movable fleet with standardized connections and spare parts;
- repeat pre-harvest reservations.

Continuous moisture, air-condition and energy recording is important: published engineering work notes that final moisture alone does not reveal energy efficiency or moisture uniformity. [Grube and Böckelmann](https://www.agricultural-engineering.eu/landtechnik/article/download/2011-66-4-276-281/2011-66-4-276-281-en-pdf/678)

## 8. Incumbent route-around

| Route-around | Consequence | Practical response |
|---|---|---|
| Customer buys its own electric heater after one season | Removes repeat service revenue | Multi-year reservation, performance warranty and avoided-capex pricing |
| Renewable installer fabricates a copy | Channel becomes competitor | Partner economics, standardized controls and retained dispatch/data layer |
| Dryer manufacturer adds electric heat and dynamic dispatch | Hardware advantage disappears | Integrate rather than depend on proprietary heater design |
| Customer shifts its load directly under a dynamic contract | Energy-spread value is internalized | Sell verified drying performance and operating responsibility |
| LPG, gas or biomass provider cuts price | Service price is capped | Quote total delivered cost, including transport and handling |
| Warehouse uses ambient aeration and waits | No paid intervention in favorable weather | Target batches with storage or delivery deadlines |

No durable exclusivity is apparent at the hardware level. Contracted sites, operating data, safe integration and dependable peak-season capacity must carry the advantage.

## 9. Rule and constraint classification

| Class | Constraint | Status |
|---|---|---|
| Binding energy rule | Increased demand or altered technical parameters may require new grid-connection conditions | Confirmed by Polish government guidance |
| Binding energy rule | Dynamic pricing requires suitable settlement metering and an eligible supplier product | Confirmed for the reported customer categories; commercial-site eligibility remains site-specific |
| Binding feed rule | Feed operators must protect stored products against contamination and spoilage, maintain hygienic storage and control pests | Confirmed by Regulation (EC) 183/2005 |
| Electrical safety | Heater, fan, protection, cable and emergency-stop integration must be designed and accepted by qualified contractors | Mandatory in practice; exact standards list not researched |
| Product conformity | Venture-owned modules may require conformity documentation for the assembled machine and controls | Exact classification requires specialist review |
| Measurement | Moisture and mass readings determine payment | Contract and legal-metrology treatment remains unresolved |
| Commodity quality | Overheating, uneven drying or contamination can damage food, feed, seed or malting grain | Must be bounded by crop-specific procedures and insurance |
| Physical | Connection headroom, airflow, ambient humidity and grain maturity govern output | Must be measured at each site |
| Commercial | Seasonal utilization and willingness to prepay energy govern cash return | Requires paid operating history |

A request for increased connection power starts with the relevant distribution operator. Connection terms specify equipment, measurement, power and timing; official guidance gives indicative response periods from 21 to 150 days depending on connection group. [Polish government grid-connection guidance](https://www.gov.pl/web/your-europe/how-to-obtain-a-connection-to-the-electricity-grid)

Feed-business operators remain responsible for protecting feed against spoilage and contamination and for maintaining relevant hazard-control records. [Regulation (EC) No 183/2005](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A02005R0183-20190726)

## 10. Lawful structure

A preliminary operating structure is:

- A Polish limited-liability company owns and insures the modules.
- The site remains the grain operator and retains title, handling responsibility and food/feed records.
- The electricity supplier and site approve the retail arrangement, remote meter and incremental load.
- The venture pays or reimburses documented incremental electricity under a written hosting arrangement accepted by the supplier.
- The customer invoice is for **drying service measured in tonne-points**, plus disclosed mobilization or testing—not for resold kWh.
- Certified contractors perform electrical integration and acceptance.
- Contract schedules define crops, temperatures, sampling, exclusions, emergency shutdown and liability caps.
- No undocumented storage-yield, quality-premium or electricity-savings representation is made.

Polish energy counsel must confirm that the electricity-payment and hosting mechanism is not treated as unlicensed electricity resale, particularly if the venture is not the named retail customer.

## 11. Dependencies

1. Written connection-power confirmation for the pilot site.
2. Eligible dynamic or indexed commercial electricity product.
3. Certified 30–60 kW heater/fan integration and protection design.
4. Compatible silo or flat-store airflow and safe exhaust path.
5. Calibrated energy, moisture and mass measurement.
6. Crop-specific temperature and handling procedures.
7. Public-liability, product-liability and equipment insurance.
8. Electricity deposit and short invoice terms.
9. Field technician availability during harvest peaks.
10. Financing that matches a short seasonal revenue window.
11. Data-use rights and cybersecurity for remote dispatch.
12. Independent confirmation of equipment fabrication and production-module cost.

## 12. Fastest paid proof and capital at risk

### Paid proof

- Rent or fabricate one 30–60 kW module.
- Install it at the family-accessible agricultural customer.
- Select a 50–100 tonne batch requiring approximately five moisture points of reduction.
- Charge 15 PLN per tonne-point.
- Expected first invoice: **3,750–7,500 PLN**.
- Independently record intake moisture, completion moisture, mass, energy, ambient conditions and elapsed time.
- Collect an electricity deposit before starting.
- Complete the trial in approximately 6–10 weeks from site approval, conditional on equipment availability and electrical headroom.

### Capital at risk

**35,000–75,000 PLN**, covering rented or fabricated equipment, certified electrical work and independent metering. The amount should be released in stages:

- survey and connection confirmation;
- refundable equipment reservation;
- fabrication/rental;
- commissioning;
- paid batch.

No second module should be ordered solely from an unpaid expression of interest.

## 13. Kill criteria

Stop further fleet investment if any of these conditions persists after controlled paid trials:

- Delivered energy remains above 20 kWh per tonne-point while customers will not pay more than 15 PLN.
- Three of the first five technically suitable sites require uneconomic grid upgrades or cannot safely accept the load.
- Moisture distribution remains materially uneven despite corrected airflow and sampling.
- Independent sampling cannot produce a billing result accepted by both parties.
- Fewer than three of ten qualified sites sign a paid trial before harvest.
- Customers reject electricity deposits and normal payment timing creates unaffordable seasonal working capital.
- Required insurance is unavailable or excludes the principal grain-quality risks.
- Counsel cannot establish a workable energy-purchase arrangement without licensed electricity resale.
- A module cannot reach roughly 700 productive hours across a season and any practicable relocation route.
- Production module cost remains above the cash return supported by two seasons of observed contribution.

## 14. Decision-critical unknowns

- Actual spare connection capacity at candidate sites.
- Commercial dynamic-product eligibility and complete variable delivered-energy cost.
- kWh per tonne-point by crop, intake moisture, weather and store geometry.
- Maximum safe heater power for existing ventilation.
- Annual productive hours and overlap between regional harvest windows.
- Fraction of the 9.4 million tonnes of maize that requires paid artificial drying.
- Customer preference between tonne-point, batch and guaranteed-completion pricing.
- Production-module price, useful life, residual value and maintenance rate.
- Legal-metrology treatment of moisture-based invoicing.
- Food, feed, seed and malting-grain temperature limits.
- Insurer terms and practical liability caps.
- Whether installers and grain-equipment technicians will refer customers under acceptable economics.
- Bad-debt and payment-delay behavior during harvest.
- Buyer acceptance of grain dried using the proposed process.
- Ability to relocate modules without expensive custom reconnection.

## 15. Development status

- Desk research completed.
- No module has been fabricated or rented.
- No site connection capacity has been confirmed.
- No supplier tariff or equipment quote has been obtained.
- No paid customer agreement exists.
- No moisture-removal performance data has been generated.
- No insurance indication or legal opinion has been obtained.
- Capital beyond the founder-accessible pilot range has not been committed.

## 16. Query ledger

All eight queries were executed on 2026-08-22 before ledger closure at 15:01:28 CEST. The research interface did not expose reliable per-query seconds, so none are invented.

| ID | Exact query | Purpose | Result used |
|---|---|---|---|
| Q01 | `site:gov.pl Poland grain harvest 2024 35 million tonnes maize storage pests memorandum` | Grain denominator and storage problem | MRiRW memorandum |
| Q02 | `grain drying energy consumption kWh per tonne per percentage point moisture electric dryer study` | Drying physics | European engineering paper |
| Q03 | `Poland mobile grain dryer price PLN electric heater 30 kW 60 kW` | Equipment pricing | No usable quoted module price found |
| Q04 | `site:ure.gov.pl dynamic electricity price contract remotely read meter Poland day ahead negative prices` | Dynamic contract and price behavior | Two URE sources |
| Q05 | `site:gov.pl site:ure.gov.pl Poland increase electricity connection capacity business distribution operator fee kW conditions` | Connection-power process | Gov.pl connection guidance |
| Q06 | `site:eur-lex.europa.eu grain storage feed hygiene operator responsibility moisture pests regulation 183/2005` | Binding feed-storage duties | Regulation 183/2005 |
| Q07 | `Poland grain dryer rental service price per tonne moisture drying maize LPG 2025` | Commercial service price | WRP price report |
| Q08 | `Poland grain storage farms cooperatives grain equipment dealers market number warehouses silos` | Distribution and installed-base proxy | KONSIL commercial data |

## 17. Useful-source ledger

| ID | Source | Type | Access timestamp | Material evidence |
|---|---|---|---|---|
| S01 | [MRiRW agricultural-market memorandum](https://www.gov.pl/attachment/7db41037-4c86-4843-9a2c-9aa6c8c9726d) | Primary government market source | 2026-08-22 | Grain volume, maize volume, storage problems, commodity prices |
| S02 | [Grube & Böckelmann, *Key figures for grain drying*](https://www.agricultural-engineering.eu/landtechnik/article/download/2011-66-4-276-281/2011-66-4-276-281-en-pdf/678) | Engineering/industry research | 2026-08-22 | Storage moisture, energy requirements, utilization and process variation |
| S03 | [URE dynamic-contract analysis](https://www.ure.gov.pl/pl/urzad/informacje-ogolne/aktualnosci/12692%2CRaporty-i-analizy-URE-w-ubieglym-roku-135-odbiorcow-skorzystalo-z-umow-z-cena-dy.html) | Primary regulator | 2026-08-22 | Metering, day-ahead timing, supplier markup and observed prices |
| S04 | [URE negative-price notice](https://www.ure.gov.pl/pl/oze/swiadectwa-pochodzenia/ceny-ujemne/12037%2CWytworcy-energii-z-OZE-po-raz-kolejny-musza-skorygowac-wnioski-o-wydanie-swiadec.html) | Primary regulator | 2026-08-22 | Negative-price duration and values |
| S05 | [Gov.pl grid-connection guidance](https://www.gov.pl/web/your-europe/how-to-obtain-a-connection-to-the-electricity-grid) | Primary government guidance | 2026-08-22 | Connection conditions, power changes, timing and fees |
| S06 | [Regulation (EC) No 183/2005](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A02005R0183-20190726) | Binding EU law | 2026-08-22 | Feed-storage hygiene, spoilage, pest control and record responsibility |
| S07 | [WRP drying-price report](https://www.wrp.pl/ceny/ile-kosztuje-suszenie-zboz-i-rzepaku-usluga-w-tym-roku-bardzo-popularna-2666756) | Commercial market report | 2026-08-22 | 2025 tonne-point and handling prices |
| S08 | [KONSIL](https://www.konsil.pl/) | Commercial channel source | 2026-08-22 | Silo customers, installed storage proxy and equipment-channel route |

Ontario government and Taylor & Francis pages returned access errors and were excluded from the useful-source ledger.

## 18. Evidence ledger

| Evidence atom | Source | Classification | Use |
|---|---|---|---|
| Poland produced about 35.0 Mt of grain, including 9.4 Mt maize | S01 | Verified | Payer denominator |
| Moist grain creates respiration, fungi and pest risk; about 14.5% supports long storage | S02 | Verified engineering evidence | Problem definition |
| Typical farm dryer use is seasonal, about 100–1,000 hours | S02 | Verified engineering evidence | Utilization risk |
| In-store energy figures imply approximately 13.4–21.5 kWh per tonne-point | S02 plus disclosed conversion | Interpretation | Unit economics |
| Polish 2025 service price was commonly 15–20 PLN per tonne-point | S07 | Commercial observation | Price anchor |
| Day-ahead price is available the preceding afternoon and requires remote settlement metering | S03 | Verified regulatory evidence | Dispatch and dependency |
| Retail markup can materially reduce the wholesale-price opportunity | S03 | Verified regulatory evidence | Electricity-cost caution |
| Seven negative-price hours occurred on 23 June 2024 | S04 | Verified event | Dispatch opportunity only |
| Increased power demand can require new connection conditions | S05 | Verified government guidance | Installation dependency |
| Feed operator retains storage hygiene and pest-control duties | S06 | Binding-law evidence | Responsibility allocation |
| A silo vendor reports 15,000 Polish customers and 900,000 tonnes of storage | S08 | Commercial self-report | Channel proxy only |
| Scenario prices, electricity costs, margins, module counts and valuation multiples | Model assumptions | Unverified | Founder-wealth cases |
