# Simulated Round 147: TowFaktura Impound Payment Rail

Created: 2026-05-29

Real browser gate: working Zero To One `>=85`, fresh Zero To One `>=85`.

## Search Reasoning

Recent marketplace, EPREL, payment-regulatory, Data Act, and micro-acquisition candidates have been capped. This round returns to the only lower-gate pattern that nearly cleared: municipal all-event payment rails. It avoids duplicating TraceFaktura by changing the buyer, trigger, operational event, and proof artifact.

TraceFaktura: municipal animal-care invoice evidence.

TowFaktura: municipal/police vehicle removal and impound-storage payment acceptance evidence.

## Raw Candidate Sweep

| # | Raw candidate | Buyer / payer | Acute trigger | Transferable control proof | Internal cap |
|---:|---|---|---|---|---:|
| 1 | TowFaktura impound payment rail | Municipal/police towing contractors | Invoices withheld for vehicle removal/storage evidence | Removal order, photos, GPS/time, impound ledger, release/scrap/payment packet | 88 |
| 2 | Disabled student transport ride billing rail | Transport contractors/gminas | Ride invoices disputed | Ride logs/school signoffs/GPS | 83 |
| 3 | Non-emergency patient transport invoice rail | Transport firms | Payment evidence | Health/admin risk | 76 |
| 4 | Snow removal event rail | Winter maintenance contractors | Event invoices disputed | Failed at 64 | 64 |
| 5 | Municipal animal-care event rail | Animal-care contractors/gminas | Invoice evidence | Lower-gate confirmed | Already confirmed |
| 6 | Roadkill/carcass removal billing rail | Municipal contractors | Event evidence | Too close/low volume | 78 |
| 7 | Streetlight repair event rail | Maintenance contractors | Work acceptance | Incumbent CMMS | 72 |
| 8 | Graffiti removal billing rail | Municipal contractors | Photos/protocols | Low-ticket | 70 |
| 9 | Emergency tree removal event rail | Contractors | Storm invoices | Field chaos | 72 |
| 10 | Waste container overflow evidence rail | Waste contractors | Disputed extra pickups | Telematics/incumbents | 72 |
| 11 | Septic/cesspit municipal pickup rail | Contractors | Pickup invoices | Existing BDO/docs | 70 |
| 12 | Parking meter maintenance event rail | Contractors | SLA penalties | Existing systems | 69 |
| 13 | Traffic-sign repair acceptance rail | Contractors | Work acceptance | Existing photos/protocols | 72 |
| 14 | Shelter/vet invoice rail | Contractors | Animal-care payments | Duplicate TraceFaktura | Already confirmed |
| 15 | Readymix pour acceptance ledger | Concrete suppliers | Invoice acceptance | Failed at 68 | 68 |
| 16 | Azbest KPO settlement rail | Asbestos contractors | Settlement | Failed at 68 | 68 |
| 17 | Construction retention release | Contractors | Retention cash | Failed at 67 | 67 |
| 18 | Public grant claim release | Grant recipients | Payment claim | Failed at 76 | 76 |
| 19 | LC payment release | Exporters | LC discrepancy | Failed at 74 | 74 |
| 20 | Municipal sports facility maintenance rail | Contractors | Monthly evidence | Low urgency | 68 |
| 21 | CCTV/alarm response event billing | Security firms | Response invoices | Existing logs | 72 |
| 22 | Elevator rescue call billing rail | Lift firms | Emergency calls | Safety/UDT | 70 |
| 23 | Fire brigade false alarm billing pack | Security/facilities | Cost recovery | Legal/public | 64 |
| 24 | Port truck detention evidence rail | Logistics firms | Detention billing | Freight incumbents | 71 |
| 25 | Waste tire collection settlement rail | Collectors | BDO/payment evidence | Thin margins | 69 |
| 26 | School meal delivery acceptance rail | Caterers | Meal count disputes | Existing signoffs | 70 |
| 27 | Home-care visit invoice rail | Care contractors | Visit evidence | Health/care risk | 72 |
| 28 | Municipal cemetery service billing rail | Contractors | Event records | Low urgency | 67 |
| 29 | Street sweeping GPS billing rail | Contractors | Route proof | Telematics vendors | 70 |
| 30 | Security guard patrol billing rail | Security firms | Patrol proof | Guard-tour systems | 68 |

## Selected Candidate

**TowFaktura Impound Payment Rail**

Internal simulated score: `88 / 100`

## Why It Can Clear Simulation

The candidate advances because the proof artifact is stronger than "better documentation": each paid event starts from an official vehicle-removal order and ends in a payment packet tied to removal, towing, storage days, owner release/payment, abandonment/scrap, or municipal payment.

The first proof is current cash: signed contractor mandate, live municipal/police contract, current unpaid or at-risk invoice batch, event records, and at least one accepted invoice/payment packet.

## Internal Cap Notes

Why not higher:

- Many towing/impound contractors may already have paper/photo workflows.
- Municipal/police procedures and owner-payment rules vary.
- Field capture can be messy, and some cash may be collected from vehicle owners rather than gmina.
- The work can drift into legal disputes, abandoned vehicle disposal, lien/ownership, or public-procurement interpretation.
- It is adjacent to TraceFaktura and must prove a different payment artifact and stronger current-cash friction.

## Required Proof

- Three contractors with active municipal/police towing or impound contracts.
- At least 150 events or 100,000 PLN in unpaid/at-risk invoices reviewed.
- Ten current event packets built from official order, photos, GPS/time, impound entry/exit, tariff, owner payment/release or municipal billing path.
- At least five invoices accepted, corrected, paid, or cleanly no-go'd.
- One contractor submits a second batch.
- Gross margin above 60%.

## Gate Decision

The simulated score is strictly above 87, so write a clean Zero To One prompt and submit to the working chat.
