# Simulated Round 181: FieldAction Serial Reimbursement Queue

Date: 2026-05-29

Working folder: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/`

## Recovery Logic From Round 180

Round 180 failed because ordinary warranty/RMA credit recovery still depends on claim windows, technical eligibility, missing return proof, and low per-line economics. The better recovery shape is a payor-defined field action, service campaign, recall remedy, or serial-numbered retrofit program where the manufacturer/distributor has already announced the eligible serial population, remedy, and reimbursement route. The startup should not argue warranty coverage. It should control a named reimbursement queue that should already be payable if serials, job proof, and submission windows are clean.

## Raw Candidate Sweep

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day proof | Acquisition | Economics | Copy risk | Why incumbent cannot copy exact case | Why not service/report/app/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | FieldAction serial reimbursement queue | installers/distributors | official service campaign credits unpaid | signed mandate, serial list, campaign notice, job proof, portal/status | 5 queues, 250k PLN eligible, first 50k credit | installer/distributor outreach | fixed screen + success | OEMs/admins | exact serial queue and mandate | recovered credits |
| 2 | PV inverter field-action labor credit | PV installers | OEM campaign window closing | serial/job proof | 100 serials, first credit | PV groups | good if campaign live | OEM portals | exact install base | recovery |
| 3 | EV charger service-campaign credit desk | EV installers/CPOs | charger campaign labor unpaid | campaign IDs, OCPP/job proof | 50 chargers | charger installers | medium | CPO/OEM teams | exact station IDs | recovery |
| 4 | Heat-pump compressor campaign queue | HVAC installers | manufacturer retrofit program | serial/job/RMA proof | 40 units | HVAC groups | medium | distributors | exact serials | recovery |
| 5 | Commercial refrigeration controller campaign | refrigeration service firms | controller board campaign | serial/job proof | 25 units | service firms | medium | wholesalers | exact accounts | recovery |
| 6 | Fire-alarm panel field-action credit | fire/security firms | firmware/board campaign | serial/customer proof | 30 panels | integrators | medium | authorized servicers | exact cases | recovery |
| 7 | Access-control lock campaign credits | security installers | smart lock/controller recall | serial/job proof | 50 locks | integrators | low-medium | OEMs | exact customer base | recovery |
| 8 | Barcode scanner battery recall credit | warehouse IT resellers | recall reimbursements | serial/return proof | 100 units | resellers | low-medium | OEMs | exact serial ledger | recovery |
| 9 | Industrial drive retrofit campaign | maintenance firms | VFD/drive service bulletin | serial/job proof | 20 drives | maintenance firms | high but technical | OEM service | exact serials | recovery |
| 10 | UPS battery module service campaign | UPS service firms | module replacement reimbursement | serial/job proof | 30 modules | electrical firms | medium | OEM service | exact accounts | recovery |
| 11 | BESS rack firmware/retrofit credits | BESS installers | battery campaign | serial/telemetry proof | 20 racks | storage installers | high risk/technical | OEMs | exact sites | recovery |
| 12 | HVAC refrigerant valve service bulletin | HVAC firms | valve campaign | serial/job proof | 50 units | HVAC groups | medium | wholesalers | exact queues | recovery |
| 13 | Retail POS terminal recall credits | retail IT installers | terminal campaign | serial/return proof | 100 terminals | POS installers | low | payment processors | exact terminal IDs | payment-provider risk |
| 14 | Industrial printer field-action credits | coding/marking service firms | printer board/nozzle campaign | serial/job proof | 20 units | service firms | medium | OEMs | exact serials | recovery |
| 15 | Telecom router firmware campaign credits | telco installers | security field action | serial/job proof | 100 routers | telco installers | low-medium | MSPs | exact accounts | recovery |
| 16 | Forklift battery campaign credits | forklift service | battery safety/firmware campaign | serial/job proof | 20 batteries | service firms | medium | dealers | exact serials | safety risk |
| 17 | Gate/door automation campaign credits | access installers | controller/safety campaign | serial/job proof | 40 units | installers | medium | OEMs | exact sites | recovery |
| 18 | Appliance B2B service campaign credits | service firms | OEM campaign labor unpaid | job IDs | 200 jobs | service firms | low | OEM portals | exact job queue | low ticket |
| 19 | Medical equipment field-action credits | med servicers | device campaign | serial/job proof | reject | med channels | regulated | OEMs | exact cases | reject health |
| 20 | Vehicle fleet recall reimbursement queue | fleet workshops | recall labor admin | VIN/job proof | 100 VINs | workshops | low | dealers | exact VINs | OEM/dealer owns |
| 21 | Agricultural machinery campaign credits | agri dealers | retrofit campaign | serial/job proof | 20 machines | dealers | medium | OEM dealers | exact serials | provider dependency |
| 22 | Water pump campaign credits | pump service firms | pump retrofit | serial/job proof | 30 pumps | industrial service | medium | distributors | exact accounts | recovery |
| 23 | Lighting driver field-action credits | electrical contractors | LED driver campaign | serial/job proof | 100 fixtures | contractors | low-medium | wholesalers | exact project | recovery |
| 24 | Elevator component campaign credits | elevator firms | safety retrofit | reject | elevator firms | regulated | OEMs | exact jobs | reject liability |
| 25 | Lab equipment service campaign credits | lab servicers | module campaign | reject | lab service | regulated-ish | OEMs | exact serials | reject specialist |
| 26 | Commercial kitchen equipment campaign credits | service firms | board/burner campaign | serial/job proof | 25 units | service networks | medium | OEM service | exact cases | recovery |
| 27 | Solar optimizer field action | PV installers | optimizer batch campaign | serial/roof job proof | 100 optimizers | PV groups | medium | distributors | exact serial list | recovery |
| 28 | Industrial sensor recall credit | automation integrators | sensor batch replacement | serial/job proof | 100 sensors | integrators | low-medium | OEMs | exact queue | recovery |
| 29 | Printer/copy service campaign | office equipment dealers | campaign labor unpaid | machine IDs | 100 jobs | dealers | low | OEM portals | exact queue | low ticket |
| 30 | Pool pump/sauna controller campaign | installers | campaign credits unpaid | serial/job proof | 30 units | installers | medium-low | distributors | exact queue | seasonal |
| 31 | Cold-room door hardware campaign | refrigeration firms | hardware retrofit | job proof | 20 units | service firms | medium | wholesalers | exact sites | recovery |
| 32 | Industrial charger/rectifier campaign | maintenance firms | charger retrofit | serial/job proof | 20 units | maintenance groups | medium | OEMs | exact serials | recovery |

## Finalist Table

| Finalist | Internal simulated score | Advance? | Reason |
|---|---:|---|---|
| FieldAction Serial Reimbursement Queue | **88.2** | **Yes** | Strongest current-cash control: official campaign, exact serials, signed queue mandate, and first credit memo. Stronger than ordinary RMA because eligibility is payor-defined before intake. |
| PV Inverter Field-Action Labor Credit | 86.5 | No | Good entry niche, but a single vertical can be too campaign-dependent. Use as beachhead inside lead candidate. |
| EV Charger Service-Campaign Credit Desk | 84 | No | Good future vertical, but station/OCPP/procurement evidence can become technical and CPO-owned. |
| Commercial Refrigeration Controller Campaign | 83 | No | Better ticket size, but service networks and wholesalers own the natural workflow. |
| Fire-Alarm Panel Field-Action Credit | 80 | No | Authorized-provider and life-safety boundaries cap it. |
| Industrial Drive Retrofit Campaign | 79 | No | High-ticket, but too technical and OEM-service dependent. |

## Lead Candidate

**FieldAction Serial Reimbursement Queue**

### Buyer

Polish and CEE installers, distributors, service contractors, and small integrators that completed manufacturer/distributor field actions, service campaigns, safety notices, serial-batch remedies, firmware/hardware retrofits, replacement programs, or return campaigns but have not converted eligible serial/job lines into credit memos, account offsets, or labor reimbursements.

### Acute Trigger

The manufacturer or distributor has already announced a program for a named product, serial range, firmware/hardware batch, or installed-base issue. The installer/distributor has serials and work proof, or has already performed the remedy, but the reimbursement window, credit memo, return credit, freight credit, or labor allowance has not been captured before quarter close or campaign expiry.

### Control Point

- signed mandate over one official campaign queue;
- official campaign bulletin, service notice, program email, portal notice, distributor letter, or credit policy;
- eligible serial numbers, installation/customer/site IDs, job dates, remedy performed, photos/screenshots, return labels, shipment proof, invoices, and technician notes;
- payor acknowledgement or portal evidence that the campaign exists and that reimbursement or credit is available if proof is complete;
- submitted reimbursement packet;
- credit memo, account offset, or reimbursement trail;
- founder fee from fixed screen plus recovered-credit success fee.

### 60-Day Proof

1. Five installers/distributors sign mandates over official service-campaign queues.
2. At least 250,000 PLN of campaign-eligible credit or reimbursement face value is documented through campaign notices, account statements, serial/job lists, or portal evidence.
3. Two payor/distributor campaign routes are confirmed in writing.
4. At least 50,000 PLN of credits, account offsets, or reimbursements are recovered or formally approved.
5. At least three buyers pay fixed screened-queue fees before success fees.
6. Cases without official campaign notice, serial eligibility, return/remedy proof, or open submission path are rejected.

### Economics

Charge 2,000-6,000 PLN per screened campaign queue plus 12-25% of actual recovered or approved credit, with a minimum success fee per queue. The buyer pays because the money is tied to a manufacturer-defined program rather than speculative warranty arguing. Gross margin can stay above 65% if the founder accepts only official campaigns with repeatable proof fields and rejects technical disputes.

### Internal Kill Lines

- Kill if more than half the apparent face value lacks official campaign terms or serial eligibility.
- Kill if OEMs/distributors will not accept mandates or require the installer to self-submit every touch.
- Kill if average recoverable value per queue is below 20,000 PLN.
- Kill if most work becomes technical eligibility argument, unsafe-installation review, consumer complaint handling, or litigation.
- Kill if a single OEM/distributor route cannot produce at least three repeatable campaign claims.

## Internal Score Rationale

The idea clears the simulated `>87` gate only because it materially improves on ordinary warranty/RMA recovery:

- campaign eligibility is defined before intake;
- exact serials and payor program notices are the control object;
- proof is recovered credit, not an audit;
- no inventory, client funds, legal claims, or repair work;
- CEE installer/distributor fragmentation may leave enough neglected campaign value;
- one repeated campaign route can compound into payor-specific proof memory.

The main weakness is copy risk: OEMs, distributors, installer admins, and accountants can copy the workflow once visible. The score stays below 90 because defensibility depends on repeated campaign queue access and payor-route memory, not a structural monopoly.

Gate decision: advance to working Zero To One validation.
