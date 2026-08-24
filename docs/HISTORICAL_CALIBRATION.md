# Historical Quality Calibration

This calibration checks whether the current `holistic-11-v1` rubric produces a sensible directional ordering on representative archived opportunities. It is development evidence only: it is not a holdout, a qualification, or a conversion of any historical score.

The reviewer used the current `PERSONALITY_SITUATION.md` and the evaluator snapshot identified by SHA-256 `3460cbf1226930081478cc5b87f8b49c28c6f6b21f037cf5d831b552a8b230cc`, ignored every archived score and label, and rescored the dossiers from their underlying claims. All factors remained applicable, so no weight was excluded or renormalized. Factor weights remain defined only in `Personalities/ZeroToOne.txt` and are intentionally not copied here.

## Results

| Factor | HeritageDoor | TraceFaktura | Refrigeration monitoring | DSR commissioning |
|---|---:|---:|---:|---:|
| Core insight | 8 | 7 | 6 | 6 |
| Customer pain / willingness to pay | 6 | 6 | 7 | 5 |
| Business model / economics | 5 | 4 | 5 | 4 |
| Market / beachhead | 5 | 4 | 5 | 5 |
| Competitive position | 6 | 4 | 4 | 3 |
| Expansion | 6 | 5 | 5 | 5 |
| Defensibility | 6 | 4 | 4 | 3 |
| Strength of advantage | 7 | 6 | 5 | 4 |
| Timing | 5 | 6 | 6 | 7 |
| Distribution | 6 | 5 | 5 | 4 |
| Execution / risks | 5 | 6 | 6 | 5 |
| Deterministic base score | **5.74** | **4.86** | **5.21** | **4.29** |
| Interaction adjustment | **0.0** | **-0.3** | **-0.2** | **-0.2** |
| Final score | **5.7** | **4.6** | **5.0** | **4.1** |

The base scores were recomputed with the canonical evaluator weights and Decimal arithmetic; the displayed final scores apply the listed interaction adjustment and explicit half-up rounding. The factor scores, evaluator hash, base score, adjustment, and final score are sufficient to reproduce the result without creating a second weight source.

The directional ordering is HeritageDoor, refrigeration monitoring, TraceFaktura, then DSR commissioning. HeritageDoor leads because controlled physical inventory is a more credible scarce asset than the service-created datasets in the other dossiers. It still falls far short of qualification because fit-specific demand, turnover, working capital, and the required throughput for founder wealth are not evidenced.

## Candidate Diagnostics

### HeritageDoor

Source: [`archive/legacy-history/ideas/confirmed_85s_club/CONFIRMED_IDEA_20260513_155748.md`](../archive/legacy-history/ideas/confirmed_85s_club/CONFIRMED_IDEA_20260513_155748.md)

- Primary limiter: thin, dimension-specific demand combined with slow, capital-consuming inventory turns; the dossier does not establish throughput compatible with the founder-wealth path.
- Strongest contrary evidence: current marketplace supply includes cheap or free old doors, while established firms can reproduce historical doors. Scarcity therefore has to exist at the matched-suite and exact-fit level, not at the generic old-door level.
- Evidence caveat: no deposits, realized full-suite margins, turnover time, dimension match rate, damage rate, or restoration quotes are present. Marketplace listings are asking prices, not completed sales.
- Current checks: [OLX listings](https://www.olx.pl/budowa-i-remont/drzwi/warszawa/q-drzwi-ze-starej-kamienicy/), [Eurostyl](https://eurostyl.net.pl/en/offer/doors/stylised-and-historical-doors), and [Stolarnia Laskus](https://stolarnialaskus.pl/o-firmie/).

### TraceFaktura

Source: [`archive/legacy-history/ideas/CONFIRMED_IDEA_20260523_031740.md`](../archive/legacy-history/ideas/CONFIRMED_IDEA_20260523_031740.md)

- Primary limiter: payer/beneficiary mismatch. Municipalities and taxpayers benefit from reliable evidence, while a contractor may gain little or lose useful ambiguity by adopting it.
- Strongest contrary evidence: the cited NIK audit describes municipalities paying despite weak reports and incomplete checks. That validates the governance problem but weakens the immediate contractor-side paid consequence.
- Interaction: weak enforcement and adverse contractor incentives reinforce one another, producing the separate negative adjustment.
- Evidence caveat: the qualified buyer count, invoice-delay economics, municipality acceptance, prepaid routing mandates, staff compliance, and reusable data rights remain unknown. The newer KROPiK law strengthens traceability direction but may also standardize part of the identity and event layer.
- Current checks: [NIK audit](https://www.nik.gov.pl/plik/id,30164,vp,33186.pdf), [KROPiK act](https://api.sejm.gov.pl/eli/acts/DU/2026/755/text.pdf), and [entry-into-force record](https://ppiop.rcl.gov.pl/index.php?id_akt_prawny=306110&r=skorowidz/aktprawnydetail).

### Refrigeration-loss monitoring

Source: [`archive/legacy-history/working_folder/zero_to_one_candidates_20260822_110713/finalist_refrigeration_loss_monitoring.md`](../archive/legacy-history/working_folder/zero_to_one_candidates_20260822_110713/finalist_refrigeration_loss_monitoring.md)

- Primary limiter: the certified maintenance partner or incumbent controller vendor commonly owns the customer, telemetry, dispatch, and service contract, and can substitute for or internalize the offer.
- Strongest contrary evidence: Danfoss already markets alarm triage, remote monitoring, repair, and technician dispatch. The highest-loss sites are also likely to be the best-covered sites because leak detection and record obligations increase with refrigerant charge.
- Interaction: the clearest loss-funded return and the strongest incumbent coverage are negatively correlated.
- Evidence caveat: private loss histories, controller access costs, false-positive rates, liability, partner margin, incremental budget, transition rates, and signed data rights are missing.
- Current checks: [Danfoss monitoring](https://www.danfoss.com/en/industries/food-and-beverage/dcs/monitoring-and-management/), [Alsense](https://www.danfoss.com/en-us/products/dcs/monitoring-and-services/alsense-food-retail-iot-cloud-application-for-supermarkets/), [EU Regulation 2024/573](https://eur-lex.europa.eu/eli/reg/2024/573/2024-02-20/eng), and [UDT F-gas requirements](https://www.udt.gov.pl/faq/faq-najczesciej-zadawane-pytania/f-gazy-i-szwo).

### DSR process commissioning

Source: [`archive/legacy-history/working_folder/zero_to_one_candidates_20260822_110713/finalist_dsr_process_commissioning.md`](../archive/legacy-history/working_folder/zero_to_one_candidates_20260822_110713/finalist_dsr_process_commissioning.md)

- Primary limiter: no separate paid transaction is established. An aggregator already captures the flexibility economics and may treat assessment and onboarding as customer acquisition cost.
- Strongest contrary evidence: Enel X advertises no-cost participation, jointly prepares the reduction plan, and reports a large Polish position, directly weakening a generic paid-audit wedge.
- Interaction: the complex processes that most need commissioning also create greater controls cost, safety constraints, and uncertainty in dependable flexibility.
- Evidence caveat: there is no aggregator subcontract, site purchase order, acceptance specification, dependable-kW test, data-rights term, contractor margin, penalty allocation, or durable post-market revenue basis.
- Current checks: [Enel X DSR offer](https://www.enelx.com/pl/pl/demand-side-response), [Enel X market report](https://www.enelx.com/pl/pl/aktualnosci/raport-enelx-dsr-na-rynku), and [URE aggregator register](https://bip.ure.gov.pl/bip/rejestry-i-bazy/wykaz-agregatorow/4713,Wykaz-agregatorow.html).

## Recurring Structural Pattern

TraceFaktura, refrigeration monitoring, and DSR commissioning reproduce the historical service-to-data-asset weakness:

- A customer, certified partner, controller vendor, or aggregator controls the raw data and can restrict reuse.
- Early records are heterogeneous and client-specific, not an exclusive transferable learning asset.
- Service labor produces the data without evidence of product-like delivery costs or compounding retention.
- Incumbents own more observations and stronger distribution, so they can internalize successful workflow logic.
- The founder-wealth path requires customer counts or project throughput well beyond the evidenced beachhead.

HeritageDoor partially escapes the pattern through physical asset ownership, but its database remains an operating aid rather than a solution to sparse demand and inventory turnover.

## Interpretation

This calibration supports expected ordering and recurring-limiter detection, not exact future model scores. The dossiers have unequal freshness and evidence density, and the current sources can change. Any future use should re-check decision-critical claims and preserve these results as `calibration`, never `holdout_native`.
