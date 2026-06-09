# Simulated Round 94: Municipal / Contracted Event-Billing Rails

Date: 2026-05-27

## Pivot From Round 93

Approved Commercial Insurance Payout Lockbox failed working-chat validation at `59 / 100`.

Reason to pivot: claims finance is either too clean for the founder or too messy/legal. This round pivots to controlled operational event evidence before invoicing, where the founder can own the current-month billing rail instead of reconstructing claims, reports, or evidence after the fact.

## Raw Candidates

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Margin / payback logic | Copy risk and why incumbents cannot copy before control | Why not wrapper |
|---|---|---|---|---|---|---|---|---|---|
| 1 | WinterRoad Event Billing Rail | Small snow/ice road-maintenance contractors billing gminas, schools, facilities | Gmina disputes winter route/time/salt/equipment invoices | Mandatory all-event routing before month-end invoice | Contractor agreement, prepaid month, route/event intake, invoice packet | Target small contractors before winter season | 1k-4k PLN/month + setup; high gross | Fleet software exists; founder controls live current-month event stream for small contractor | Operational event rail |
| 2 | StormTree Emergency Removal Evidence Rail | Municipal tree-removal/emergency contractors | Storm cleanup invoice disputed for time, crew, site, disposal | Live callout/photo/time/disposal evidence stream | Prepaid current storm/on-call case | Arborist contractors | Per-callout + monthly | Contractors can photograph; founder controls packet workflow | Event rail |
| 3 | Pothole Patch Event Evidence Rail | Road repair micro-contractors | Gmina rejects patch quantities/locations | Live location/photo/material ticket stream | Prepaid route/month | Road repair contractors | Per event/monthly | Road asset software exists; small contractors underserved | Event rail |
| 4 | Greenery Maintenance Evidence Rail | Municipal mowing/greenery contractors | Work acceptance disputes across dispersed sites | Site-photo/route/event packet | Prepaid month | Greenery contractors | Monthly | Easy to copy/photos | Event rail |
| 5 | Streetlight Repair Event Rail | Electrical contractors | Repair invoices need pole/time/material proof | Pole-level event ticket stream | Prepaid month/case | Electrical contractors | Monthly/per ticket | Utilities/software; electrician can log | Event rail |
| 6 | Municipal Waste Extra-Pickup Evidence Rail | Waste contractors | Extra pickups/illegal-dump cleanup disputed | Pickup photo/GPS/KPO/invoice packet | Prepaid current cases | Waste firms | Per pickup/monthly | BDO systems/software; compliance risk | Event rail |
| 7 | Drain/Gully Cleaning Evidence Rail | Infrastructure contractors | Gmina questions cleaned drains/locations | Manhole/gully photo/time/sludge evidence | Prepaid route | Drain firms | Monthly/per asset | Easy but route-heavy | Event rail |
| 8 | Public Facility Repair Callout Rail | Maintenance contractors | Facility disputes callout hours/materials | Work order/photo/signoff stream | Prepaid month | Maintenance firms | Monthly | CMMS exists; small contractors underserved | Event rail |
| 9 | Playground Inspection/Repair Evidence Rail | Municipal playground contractors | Repairs need audit-proof photos/parts | Asset-level inspection/repair packet | Prepaid route | Playground maintenance firms | Monthly | Specialized inspectors exist | Event rail |
| 10 | Bus Stop Shelter Repair Rail | Shelter contractors | Damage/repair invoices disputed | Stop-level photo/time/parts packet | Prepaid month | Shelter maintenance firms | Monthly | Simple, low ARPU | Event rail |
| 11 | Road Sign Replacement Evidence Rail | Traffic sign contractors | Missing/damaged sign invoices disputed | Sign-level photo/GPS/material packet | Prepaid current jobs | Traffic contractors | Per job/monthly | Simple/copyable | Event rail |
| 12 | Animal-Carer Event Rail Expansion | Municipal animal contractors | Event invoice rejected | Existing TraceFaktura-like rail | Direct routing | Existing niche | Monthly/per event | Confirmed TraceFaktura duplicate | Operational rail |
| 13 | Cemetery Maintenance Event Rail | Municipal cemetery contractors | Site tasks disputed | Plot/section event evidence | Prepaid month | Cemetery firms | Monthly | Niche, low urgency | Event rail |
| 14 | Public Toilet Service Evidence Rail | Cleaning/maintenance contractors | Service frequency disputes | QR/photo/time packet | Prepaid month | Cleaning firms | Monthly | Commodity checklist tools | Event rail |
| 15 | School Transport Incident Rail | Transport contractors | Trip/absence/incident billing disputes | Live trip/incident evidence | Prepaid month | Transport firms | Monthly | Sensitive child data; avoid | Event rail |
| 16 | Shelter/Social-Service Event Rail | NGOs/contractors | Per-person service invoice disputes | Sensitive beneficiary events | Prepaid | NGOs | Monthly | Sensitive data/high risk | Event rail |
| 17 | Roadside Litter Cleanup Evidence Rail | Contractors | Gmina disputes collected sites/bags | Site/photo/bag evidence | Prepaid month | Cleanup firms | Monthly | Low value | Event rail |
| 18 | Mosquito/Pest Municipal Treatment Rail | Pest contractors | Treatment area/time disputed | Route/GPS/chemical evidence | Prepaid route | Pest firms | Monthly/season | Regulated chemicals/provider risk | Event rail |
| 19 | Flood Pumping Event Evidence Rail | Emergency contractors | Pumping hours/equipment disputed | Live pump/hour/site evidence | Prepaid on-call | Pumping/drain firms | Per emergency | Event episodic | Event rail |
| 20 | Road Sweeping Evidence Rail | Sweeping contractors | Routes/frequency disputed | Route/photo/GPS packet | Prepaid month | Sweeping firms | Monthly | Fleet telemetry/software | Event rail |
| 21 | Snow Salt Inventory-to-Route Ledger | Winter contractors | Salt/sand quantities disputed | Salt lot + route consumption ledger | Prepaid season | Winter contractors | Setup/monthly | Contractors can copy spreadsheet | Ledger |
| 22 | Municipal Construction Change-Order Rail | Small contractors | Extra works rejected at invoice | Live change-order photo/signoff stream | Prepaid project | Public works contractors | Per project | Construction tools/legal | Event rail |
| 23 | Emergency Roof-Tarping Evidence Rail | Property/municipal contractors | Storm emergency repair invoice disputed | Photo/time/material packet | Prepaid cases | Roofing contractors | Per job | Insurance/legal overlap | Event rail |
| 24 | Housing Association Repair Rail | Maintenance firms | HOA disputes callout/materials | Live work-order evidence | Prepaid month | Maintenance firms | Monthly | CMMS/copyable | Event rail |
| 25 | Public EV Charger Maintenance Rail | Charger service firms | Uptime SLA/repair evidence disputed | Charger-level ticket/evidence | Prepaid account | EV charger operators | Monthly | Operators have platforms | Event rail |
| 26 | Traffic-Light Outage Repair Rail | Signal contractors | Outage response/SLA proof needed | Incident/timestamp/evidence | Prepaid month | Signal firms | Monthly | Large incumbents/software | Event rail |
| 27 | Municipal Small-Bridge Inspection Rail | Engineers | Inspection packets disputed | Asset-level evidence | Prepaid cases | Engineers | Per inspection | Professional liability | Evidence |
| 28 | Graffiti Removal Evidence Rail | Cleanup contractors | Site count/quality disputed | Before/after/time packet | Prepaid month | Cleanup firms | Monthly | Easy photos | Event rail |
| 29 | Roadside Animal-Carcass Pickup Rail | Sanitation contractors | Pickup/disposal invoices disputed | Callout/disposal evidence | Prepaid month | Sanitation firms | Monthly | Sensitive but less than animal-care; duplicate-ish | Event rail |
| 30 | Public-Building Snow/Roof-Ice Rail | Facility contractors | Snow/ice removal invoices disputed | Site/time/photo/acceptance packet | Prepaid season | Facility firms | Seasonal | Simple/copyable | Event rail |
| 31 | Emergency Generator Rental Evidence Rail | Contractors | Public facility outage rental hours disputed | Meter/time/location packet | Prepaid rental | Rental firms | Per event | Rental companies have logs | Event rail |
| 32 | Local Road Marking Evidence Rail | Road marking contractors | Meterage/site disputes | GPS/photo/material packet | Prepaid job | Road-marking firms | Per project | Seasonal, measurable | Event rail |

## Finalists And Strict Simulated Scores

| Rank | Candidate | Simulated score | Decision | Rationale |
|---|---|---:|---|---|
| 1 | WinterRoad Event Billing Rail | 89 | Advance | Best non-TraceFaktura municipal event rail: high-value seasonal invoices, dispersed routes, weather-triggered disputes, salt/material/equipment evidence, and current-month operational capture before invoice reconstruction. |
| 2 | Pothole Patch Event Evidence Rail | 88 | Backup | Similar event proof with measurable locations/materials, but may look like ordinary photo/GPS work-order software. |
| 3 | StormTree Emergency Removal Evidence Rail | 87 | Do not real-gate | Good emergency trigger but episodic and arborist channels may be too scattered. |
| 4 | Municipal Waste Extra-Pickup Evidence Rail | 86 | Do not real-gate | Potentially valuable, but BDO/KPO and waste compliance create incumbent and legal complexity. |
| 5 | Drain/Gully Cleaning Evidence Rail | 85 | Do not real-gate | Operationally plausible but less acute and easy to copy. |
| 6 | Municipal Construction Change-Order Rail | 84 | Do not real-gate | Could be valuable but drifts into construction claims/legal disputes. |

## Advance

Advance **WinterRoad Event Billing Rail** to real working-chat validation.

## Duplicate Risk

This is adjacent to the already-confirmed TraceFaktura municipal animal-care evidence rail, but the operational control point changes materially: no animal/patient-like event custody, no shelter/vet records, no adoption/quarantine chain. The controlled stream is winter road-maintenance callouts, routes, vehicles, weather trigger, material usage, equipment hours, and acceptance evidence for seasonal public-infrastructure invoices.
