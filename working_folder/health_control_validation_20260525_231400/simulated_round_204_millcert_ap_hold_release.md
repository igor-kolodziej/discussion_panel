# Simulated Round 204: MillCert AP Hold Release Desk

Date: 2026-05-30 Europe/Warsaw
Gate: only send to Zero To One if simulated score is strictly above 87.

## Search Frame

Round 204 focused on current unpaid invoice batches where the buyer has written that payment is blocked by a specific traceability/certificate file rather than a commercial dispute. The founder can control a named invoice-release packet, customer acceptance trail, and no-go ledger.

## Raw Candidate Control Table

| # | Candidate | Buyer/payor | Acute trigger | Transferable control point | 60-day proof | Internal cap reason | Sim score |
|---:|---|---|---|---|---|---|---:|
| 1 | MillCert AP hold release desk | metal fabricators, machining, pressure-equipment, rail/energy suppliers | customer AP/QA holds payment over certificates/traceability | invoice-release mandate, customer hold notice, heat/batch map, supplier cert chase file, accepted packet | 8 mandates, 15 invoice batches, 500k PLN accepted/released/no-go | source truth gaps, but current AP acceptance is strong | 89 |
| 2 | Welding doc AP hold release | fabrication shops | customer blocks payment over WPS/WPQR/welder logs/NDT docs | welding/NDT packet | accepted release | engineer/incumbents, legal/safety | 82 |
| 3 | Coating certificate invoice release | coating/finishing suppliers | payment held over coating thickness/CoC | batch certificates | payment release | labs/source truth | 78 |
| 4 | Calibration certificate AP release | industrial service suppliers | customer blocks invoice over calibration evidence | cert file | release | calibration book already failed | 73 |
| 5 | Food CoA invoice release | ingredient suppliers | buyer blocks invoice over CoA/allergen/micro docs | CoA packet | release | food safety/regulated | 72 |
| 6 | Packaging migration certificate release | packaging suppliers | buyer holds invoices over FCM/migration docs | lab/supplier file | release | PPWR/FCM incumbents | 74 |
| 7 | Timber legality certificate invoice release | wood exporters | buyer holds payment over documents | evidence pack | release | EUDR/legal/source truth | 68 |
| 8 | Textile OEKO/GRS certificate AP release | textile suppliers | invoice held over certificates | cert chain | release | certification/licence issues | 71 |
| 9 | Electronics RoHS/REACH CoC invoice release | electronics distributors | invoice held over compliance docs | CoC/test files | release | product compliance incumbents | 69 |
| 10 | Supplier PPAP invoice milestone release | automotive suppliers | milestone held over PPAP file | APQP/PPAP packet | release | IMDS/PPAP failed | 76 |
| 11 | MTC customs release pack | importers | shipment held by customs | MTC/origin evidence | release | customs/legal failed | 72 |
| 12 | Incoming inspection NCR closure release | suppliers | customer withholds payment over NCR | NCR/CAPA evidence | release | quality dispute | 74 |
| 13 | Customer portal vendor-master evidence release | suppliers | payment blocked by vendor onboarding docs | vendor pack | release | AP/admin copyable | 70 |
| 14 | Machine installation acceptance payment pack | machinery integrators | milestone held over SAT/FAT docs | acceptance packet | release | engineering defects | 71 |
| 15 | Maintenance service report invoice release | service firms | invoice held over service proof | report/photos/logs | release | low value/service | 65 |
| 16 | NDT report chase for invoice release | fabrication shops | payment held over NDT reports | NDT files | release | NDT providers own | 75 |
| 17 | Material substitution approval release | suppliers | customer blocks payment over substitution docs | approval file | release | engineering/legal | 67 |
| 18 | Rail component traceability payment release | component suppliers | rail customer holds AP over EN/cert traceability | trace packet | release | high quality/reg safety | 79 |
| 19 | Pressure equipment traceability hold release | PED fabricators | customer holds payment over material/weld records | MDR packet | release | regulatory/safety, engineers | 76 |
| 20 | Energy-component MTC AP release | suppliers to energy projects | invoice held over MTC/CoC | packet | release | strong subset but high spec | 84 |
| 21 | Aerospace certificate AP release | aerospace suppliers | invoice held over CoC/FAI/material certs | AS9100/FAI packet | release | aerospace trust/incumbents | 70 |
| 22 | Building steel CE/DoP invoice release | steel suppliers | contractor holds invoice over DoP/CE | DoP/MTC packet | release | legal/construction disputes | 72 |
| 23 | Lot genealogy rebuild for invoice release | manufacturers | payment held over missing lot genealogy | lot map | release | source truth difficult | 77 |
| 24 | Customer-specific certificate portal release | industrial suppliers | portal rejection blocks payment | portal evidence | release | customer-specific | 73 |
| 25 | Export inspection certificate AP release | exporters | buyer holds payment over SGS/BV/inspection docs | inspection file | release | inspector/bank owns | 67 |
| 26 | Lab CoA payment release for chemicals | chemical distributors | buyer holds invoice over CoA/SDS | CoA/SDS file | release | chemicals compliance | 70 |
| 27 | Rework evidence payment release | industrial suppliers | payment held after rework | rework/NCR evidence | release | true quality disputes | 62 |
| 28 | Paint batch certificate release | coatings suppliers | invoice held over batch docs | CoA/batch map | release | source truth | 72 |
| 29 | Tooling acceptance milestone release | tooling suppliers | final payment held over acceptance docs | acceptance file | release | ToolTitle/legal/engineering | 68 |
| 30 | Readymix test cube payment release | concrete suppliers | payment held over cube results/delivery proof | test/delivery file | release | readymix branch failed | 65 |

## Selected Candidate

**MillCert AP Hold Release Desk**

### Why This Advanced

This is not generic quality consulting. It starts with a written AP/QA payment hold for delivered goods and a named invoice batch. The output is customer acceptance, payment release, partial release, or clean no-go, not an improvement report.

### Control Point

- Supplier mandate over named unpaid invoices and customer hold notice.
- Customer AP/QA request text.
- Heat/batch/lot/serial map from delivered items to invoices and purchase orders.
- Mill test certificates, CoC/CoA, inspection records, NDT reports where already performed, welding/traceability logs where relevant.
- Upstream supplier certificate chase file.
- Customer-ready traceability packet and response matrix.
- Payment release or no-go tracker.

### 60-Day Proof

- 8 prepaid mandates.
- 15 invoice batches above 75,000 PLN each.
- 10 customer acceptances, payment releases, partial releases, or clean no-go outcomes.
- 500,000 PLN+ invoice value accepted/released/formally no-go'd.
- 60,000 PLN+ collected in fees.

### Economics

- 5,000-12,000 PLN triage per invoice batch.
- 12,000-35,000 PLN urgent traceability release file.
- Optional success fee of 2-6% of invoice cash released only where customer hold text and attribution are explicit.
- Gross margin above 65% if missing source truth is no-go'd early and review/chasing is bounded.

### Internal Caps Applied

- Capped below 93 because missing certificates may be impossible to recreate.
- Capped below 91 because industrial quality consultants and internal QA teams can handle some cases.
- Not capped below 87 because the buyer trigger is named unpaid invoices with written AP/QA hold text and acceptance is binary.

## Simulated Zero To One Score

**89 / 100**

Passes the simulated gate because it is strictly above 87.

## Zero To One Prompt File

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_millcert_ap_hold_release.txt`
