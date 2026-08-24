# Zero-to-One Candidate: SignalChain Sentinel

## One-Sentence Thesis

Build the independent hardware-in-the-loop regression system that tells wearable and digital-biomarker teams whether a firmware, SDK, phone, or cloud release silently changed the physiological signal they ship.

## Founder Fit

The founder can start with public SDKs, affordable devices, edge software, and contract electronics help while remaining employed. The work compounds advanced signal-processing/ML, wearable hardware, real-time HCI infrastructure, proprietary failure data, and relationships with European device engineers. It does not require clinical authority, a clinic, or a finished regulated device during proof.

## Customer, Pain, and Current Workaround

The first buyer is the product/quality leader of a 10–100-person EU wearable OEM or digital-biomarker platform with a raw-data interface and a planned release. The painful event is a firmware, SDK, mobile OS/app, or cloud-pipeline change before release or after an unexplained data-quality regression. Today teams rely on unit tests, spot checks, vendor release notes, and repeated human recordings; those methods rarely verify the complete physical sensor-to-export chain with a known input. A silent units, filtering, timestamp, packet-loss, or metric change can invalidate validation work, corrupt a study, or force an emergency investigation.

## Product Wedge

The first product electrically replays ECG, mechanically replays IMU trajectories, and monitors packet/timestamp behavior through the customer's real sensor, phone, SDK, and cloud export. It generates a machine-readable release fingerprint and a clear diff against the previously accepted version. PPG optical replay is added only after ECG/IMU paid proof. The deliverable is a working regression station and recurring release check, not a compliance memo.

## Commercial Insight or Market Gap

Device companies test components; customers experience a chain. Existing simulators provide signals, while internal scripts usually stop at one device or API. The overlooked buyer need is a persistent external baseline spanning hardware, wireless transmission, phone, SDK, transformations, and cloud output across releases. Independence and cross-vendor comparison matter when an OEM's own update is the suspected cause.

## Underused Momentum

Wearable release frequency, digital endpoints, public SDKs, mandatory EUDAMED modules, and EU lifecycle accuracy/robustness expectations create more change events and more discoverable buyers. The BMJ update study and data-quality literature show that release changes and missingness can affect earlier validation. Regulation is supporting context; the paid event is a concrete release or regression.

## Beachhead Market

European ECG/IMU wearable and digital-biomarker teams exposing raw or near-raw data and operating at least two product/firmware releases per year. Exclude pure consumer brands with no raw access and projects demanding accredited or clinical validation.

## Business Model and Unit Economics

- Hypothesized paid integration: 18,000–30,000 PLN per product line; direct hardware/contract labor 6,000–10,000 PLN; 55–70% contribution margin.
- Hypothesized annual release-monitoring license: 48,000–96,000 PLN per line for scheduled and emergency runs; direct annual labor/hosting/calibration 10,000–22,000 PLN; 70–80% gross margin after adapter maturity.
- Optional on-prem station: 45,000–75,000 PLN with a 45–55% hardware gross margin, always tied to software/calibration.
- Target CAC after channel learning: 12,000–25,000 PLN, recovered on the integration plus first-year contract. This is a hypothesis and a kill metric.

## First 10 and 100 Customers

First 10: build a named list from EUDAMED, POLMED/PARP, CORDIS wearable projects, public SDK repositories, firmware release notes, and authors who disclose device updates. Send technical outbound centered on a published cross-version demonstration; offer one product line and three known-input families with a 40% deposit. Aim for two Polish/CEE referenceable engineering customers and eight European customers without relying on a partner.

First 100: publish anonymized failure-frequency benchmarks, maintain adapters for the most common raw-data devices, sell annual plans through direct technical content and release-note monitoring, and later authorize independent labs/CROs to operate stations under license. Distribution compounds because every adapter and failure pattern shortens the next integration.

## Primary Control Point

Directly owned cross-vendor adapters, replay waveforms, firmware/SDK-specific release fingerprints, failure taxonomy, comparison engine, and longitudinal product-line history. Within 12 months, proof is at least three paid product lines, two repeated release checks, an adapter library, and contracts granting ownership of generic test methods and anonymized failure derivatives. Customer raw data and confidential designs remain theirs.

## Cold Start and Resource Bootstrap

Resource needed: a credible end-to-end fixture and known-input library. Secure it without partnership by buying Movesense/Shimmer-class ECG/IMU devices, two Android phones, an electrical signal source/interface, and a programmable motion jig; use public SDKs and open biosignal waveforms. Spend 22,000–35,000 PLN before paid proof. Publish a reproducible change-detection demo, then require a deposit before buying any customer-specific device or adapter. Before serious capital, prove a known physical input can produce a stable release fingerprint and that one independent buyer pays for a bounded run.

## Distribution Advantage

Target accounts are observable at the moment of change through release notes, public SDK activity, EUDAMED, CORDIS, conference programs, and hiring. This event-driven list is narrower and more efficient than general medtech outbound. Cross-vendor benchmark content earns technical search traffic, while installed regression histories raise switching costs.

## Competitive Advantage and Expansion Path

Start with ECG/IMU release regression; add PPG, EDA, temperature, audio, and multi-device synchronization only when customers fund adapters. Expand from SMEs to CROs and larger device portfolios, then offer fleet-wide release gates and automated equivalence checks. Simulator vendors sell inputs; internal teams see only their own stack; accredited labs are expensive and episodic. The advantage is the accumulated chain-level failure corpus plus continuous workflow integration.

## Poland/EU or Local Adaptation Defense

Poland supplies lower-cost hardware/software talent and a visible medtech base; EU teams face MDR/AI lifecycle documentation and fragmented devices. The product remains an engineering QA system, avoiding claims of accreditation, clinical validation, or conformity approval. A US vendor could enter, but EU data handling, on-prem operation, local-language support, and a head start in European adapters provide a limited—not legal—defense.

## Compounding Advantage

Each integration creates reusable adapters, input waveforms, fault signatures, and a better release-diff model. Each repeated run builds longitudinal switching costs. Aggregate, non-customer-identifying failure patterns improve risk prioritization across the installed base. Hardware revenue seeds software, and software makes the lab less dependent on founder hours.

## Founder Wealth Model

All figures are hypotheses. Business values are equity values net of debt; cumulative founder distributions count only cash actually distributed and are not retained earnings already reflected in equity value.

| Scenario | Scale and pricing | Revenue, margins, capital | Ownership, reinvestment, value | Timing and founder net worth |
|---|---|---|---|---|
| Conservative | Year 8: 75 monitored product lines at 68,000 PLN ARR, 20 integrations at 24,000 PLN, and 8 stations at 55,000 PLN. | 6.02m PLN revenue; 72% gross margin; 28% operating margin (1.69m EBIT). Up to 600k PLN cumulative external capital, primarily non-dilutive/customer-funded; 200k PLN working-capital line. | Founder 86%; 95% of after-tax distributable cash reinvested while employed and no more than 5% optionally distributed; after transition, 1.4m PLN cumulative distributions. At 5.5× EBIT, equity value net of debt is 9.1m PLN; founder share 7.8m. | Paid proof by month 6; 10 lines by year 3; employment exit only after transition gate; Year 8 founder net worth about 9.2m PLN. This case does **not** independently clear 10m and is a downside warning. |
| Expected success | Year 7: 150 monitored lines at 80,000 PLN ARR, 35 integrations at 26,000 PLN, and 12 stations at 60,000 PLN. | 13.63m PLN revenue; 76% gross margin; 37% operating margin (5.04m EBIT). 1.5m PLN cumulative capital; up to 20% dilution; debt below 0.5m. | Founder 80%; 95% reinvestment and at most 5% distribution while employed; 2.0m PLN founder cash distributions after full-time transition. At 5.5× EBIT and net debt deducted, equity value is about 27.2m; founder share 21.8m. | 3 lines year 1; 18 year 2; repeatable channel year 3; Year 7 founder net worth about 23.8m PLN. Passes the wealth gate without an exit. |
| Strong success | Year 7: 400 lines at 100,000 PLN ARR plus 60 integrations/stations worth 5m PLN. | 45m PLN revenue; 80% gross margin; 42% operating margin (18.9m EBIT). Up to 6m PLN growth capital; founder uses 100% of available after-tax cash for reinvestment until scale; 40% dilution. | Founder 60%; no employment-period distribution. At 6× EBIT less 2m net debt, equity value about 111.4m; founder share 66.8m; later distributions excluded from this value. | European channel from year 3; larger portfolios year 5; Year 7 founder net worth about 66.8m PLN. |

Expected success—not strong success—supports the gate. The conservative case misses and therefore becomes a milestone discipline: if 18 recurring lines are not reached by the end of year 2, do not assume the wealth path.

## Reinvestment and Compounding Model

During employment, 95% of distributable after-tax cash in conservative/expected cases purchases adapters, automation, certifications only when customer-funded, and technical sales capacity; optional founder distributions are capped at 5%. Strong success reinvests 100%. Retained cash funds the operating asset and is not separately added to founder net worth. Post-transition distributions occur only after working capital and product road map are funded.

## Reachability and 180-Day Paid-Proof Plan

Days 1–30: build ECG/IMU replay and release-fingerprint demo with public devices; define non-accredited engineering language. Days 31–60: publish the before/after evidence and assemble 100 named release-event accounts. Days 61–120: technical outbound and demonstrations; offer a 18,000–24,000 PLN fixed integration with 40% deposit. Days 121–180: deliver one product line and sell the first repeat release check. Maximum pre-proof founder spend: 35,000 PLN. The work fits five founder-hours/day using one embedded contractor for the jig. It requires one paying buyer, not a clinic, partner, participant cohort, accreditation, or complete sensor family.

## Capital Tranches and Maximum Loss

1. 0–12,000 PLN: device/API feasibility and customer list.
2. Up to 35,000 PLN total: polished ECG/IMU station only after stable replay; this is the hard pre-proof loss cap.
3. Up to 70,000 PLN total only after a paid deposit, successful delivery, and positive contribution margin; add customer-funded adapters.
4. Up to 100,000 PLN only after three independent paying customers and at least one repeat check or documented viable acquisition channel.
5. Family capital excluded until repeatable paid demand and a clear scaling case.

## Critical Dependency Map

- Technical: known-input replay must expose meaningful full-chain changes; directly testable before sale.
- Buyer: product teams must value an external regression baseline; tested by deposit, not interviews alone.
- Access: raw/near-raw API must exist; qualify accounts before selling.
- Liability: remain pre-compliance engineering, with explicit limits; legal review is controllable.
- Control point: contracts must preserve generic methods/failure derivatives; reject work-for-hire terms that erase compounding.
- Distribution: technical event-driven outbound must reach buyers at acceptable CAC; testable with 100 accounts.

## Full-Time Transition Gate

Do not leave employment until there are at least five independent paying customers or contracted recurring lines, positive contribution margin on two delivered integrations, a repeatable acquisition signal, and at least 12 months of personal runway. No single customer may exceed 40% of contracted next-12-month gross profit.

## Failure Recovery and Reusable Assets

If external monitoring demand fails, the hardware station, adapters, waveform library, and regression software can be sold as an internal engineering kit, licensed to a CRO/test lab, or reused for future biosignal R&D. The founder retains embedded, signal-processing, and QA expertise; confidential customer data is not reused.

## Critical Evidence

The BMJ update study documents validation-relevant updates; reviews document algorithm opacity, missingness, and packet-loss risks; device kits are affordable; EUDAMED/POLMED/PARP supply target lists. WhaleTeq proves signal simulators already exist and sets the required differentiation.

## Critical Hypotheses

Buyers will pay an independent small vendor before accredited testing; full-chain diffs produce materially better decisions than internal tests; three device adapters can share enough architecture to achieve 70%+ recurring gross margin; annual release frequency and emergency use support retention; generic derivative rights are acceptable.

## Kill Criteria

Kill or structurally pivot if: fewer than 4 technical calls from 80 qualified release-event accounts; no deposit by day 180; three qualified teams say internal unit tests already cover the physical-to-cloud chain; first integration exceeds 80 founder/contractor hours without reusable adapter code; a buyer requires accreditation/clinical claims before payment; or generic method/failure rights are rejected in two otherwise willing deals.

## Budget, Time, and Minimum People Stack

Pre-proof: 35,000 PLN maximum and about 20–25 founder hours/week. Minimum stack: founder for product/data/sales; 80–120 hours of embedded/electronics contracting; short legal/regulatory copy review. Add a full-time embedded/test engineer only after repeated revenue.

## Research Sources

- [EU MDR](https://eur-lex.europa.eu/legal-content/ENG/ALL/?uri=CELEX%3A32017R0745)
- [AI Act Article 15](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX%3A32024R1689)
- [EUDAMED](https://health.ec.europa.eu/medical-devices-eudamed/overview_en)
- [Wearable update study](https://informatics.bmj.com/content/26/1/e100083)
- [Wearable data-quality review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8294465/)
- [BLE packet-loss research](https://pmc.ncbi.nlm.nih.gov/articles/PMC8533907/)
- [WhaleTeq AECG100](https://www.whaleteq.com/en/product/4/16-health-wearables-testing/view21-aecg100)
- [POLMED](https://polmed.org.pl/izba-polmed-wybrala-nowe-wladze-na-kadencje-2026-2029/)

