# Simulated Round 261: EVCharge Commissioning Payment Release

Date: 2026-05-30 Europe/Warsaw
Real browser gates: working Zero To One `>=85`, fresh Zero To One `>=85`.
Simulation rule: advance only if simulated score is strictly `>87`.

## Search Frame

Round 261 tests a current-cash infrastructure handover gate. It is not an EV-charging installation company, electrical inspection firm, OCPP platform, dashboard, warranty administrator, or grant consultant. It only activates when an installed commercial EV-charger site has final payment, warranty activation, CPO acceptance, or fleet go-live blocked by missing commissioning/handover evidence.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point inside 60 days | First proof | Internal cap result |
|---:|---|---|---|---|---|---|
| 1 | EVCharge Commissioning Payment Release | EV charger installers, distributors, fleet/CPO project managers | Final payment/warranty/go-live held after installation | Signed site mandate over named chargers, payment holdback, evidence room, accepted release/no-go | Payment release or accepted rework/no-go | Advance |
| 2 | Rooftop PV grid-trip complaint release | PV installers | Customer complaint/grid fault | Complaint file | Already failed branch |
| 3 | BESS warranty commissioning passport | BESS distributors/installers | Warranty/RMA gate | Distributor recognition | Already failed branch |
| 4 | Heat-pump commissioning passport | Heat-pump distributors | Warranty/rebate gate | Distributor recognition | Confirmed old idea; duplicate |
| 5 | EV charger grant reimbursement release | Municipal/CPO projects | Grant drawdown | Grant evidence mandate | Payment | Cap 80: grant/payment rails failed |
| 6 | EV charger MID-meter proof pack | CPOs | Billing go-live blocked | Meter evidence file | Accepted file | Cap 83: narrow subset of #1 |
| 7 | OCPP backend migration release | CPO/fleet | chargers offline after backend change | Site/router/backend logs | Go-live | Cap 84: service/migration drift |
| 8 | Charger warranty RMA recovery | Installers | RMA/labor credits | RMA mandate | Credit memo | Cap 78: warranty recovery branch failed |
| 9 | Depot load-management proof pack | Fleets | depot go-live blocked | Load-test evidence | Go-live | Cap 83: engineering boundary |
| 10 | EV charger permit closeout file | Property owners | occupancy/inspection closeout | permit file | closeout | Cap 76: legal/inspection boundary |
| 11 | Charger uptime SLA evidence desk | CPOs | SLA penalty/payment dispute | telemetry file | settlement | Cap 78: dispute/adjudication |
| 12 | Lease-end charger removal deposit release | Property owners | lease deposit held | site-handover file | deposit release | Cap 74: property/security deposit branch |
| 13 | Roaming/hubject onboarding release | CPOs | roaming go-live blocked | roaming test file | go-live | Cap 82: platform/incumbent owned |
| 14 | Fleet RFID/payment acceptance file | fleets | driver go-live blocked | test logs | accepted | Cap 82: subset of #1 |
| 15 | Charger fire-safety insurer evidence | property owners | policy bind | evidence pack | bind | Cap 74: insurance evidence branch |
| 16 | Public tender charger SKU evidence | distributors | bid blocked | product evidence | bid pack | Cap 73: tender evidence branch |
| 17 | Installer quality ranking book | distributors | preferred status | job evidence | distributor pilot | Cap 83 without signed gate |
| 18 | Charger maintenance route buyout | operators | recurring service book | payment direction | first cash | Cap 75: route/service book |
| 19 | Depot demand-response activation file | fleets | DSR payment gate | meter/baseline file | activation | Cap 80: DSR/aggregator branch |
| 20 | Charger payment-terminal certification file | CPOs | payment acceptance blocked | terminal evidence | go-live | Cap 78: PSP/certification boundary |
| 21 | EVSE serial warranty registration release | installers | warranty not active | serial evidence | warranty activation | Cap 82: subset of #1 |
| 22 | Charger OCPP trace escrow release | CPO/installer | escrow holdback | OCPP/backend evidence | escrow release | Advance as subset of #1 |
| 23 | Multi-site fleet handover lockbox | fleet operators | depot rollout acceptance | payment/warranty mandate | accepted handovers | Advance as #1 beachhead |
| 24 | Charger firmware recall reimbursement | installers | campaign compensation | claim mandate | credit | Cap 76: RMA branch |
| 25 | Charger availability penalty no-go file | CPOs | customer penalty dispute | telemetry file | no-go/rework | Cap 77: dispute consulting |
| 26 | Commercial parking charger settlement file | landlords/CPOs | revenue-share mismatch | settlement mandate | corrected statement | Cap 72: messy settlement |
| 27 | Installer subcontractor payment release file | general contractors | subcontractor payment held | as-built/commissioning file | payment | Advance only if EVSE-specific #1 |
| 28 | Charger backend evidence refresh book | CPOs | annual/fleet reviews | payment book | first cash | Cap 80: ordinary support |
| 29 | Wallbox-to-fleet migration release | installers | fleet acceptance held | migration logs | accepted | Cap 82: subset |
| 30 | EVSE meter seal/reseal packet | operators | billing blocked | meter evidence | accepted | Cap 81: legal metrology boundary |

## Finalists

| Finalist | Simulated score | Why advanced or rejected |
|---|---:|---|
| EVCharge Commissioning Payment Release | 88.3 | Named installed sites, final-payment/warranty/go-live holdback, and OCPP/backend evidence make it harder than generic commissioning. |
| OCPP backend migration release | 84.0 | Strong pain but quickly becomes technical migration support. |
| Charger MID-meter proof pack | 83.0 | Useful but too narrow and metrology-adjacent. |
| Multi-site fleet handover lockbox | 86.0 | Strong if attached to #1, but not separate enough. |
| Roaming onboarding release | 82.0 | Platform-owned and likely handled by CPO tech teams. |

## Selected Candidate

**EVCharge Commissioning Payment Release**

One-sentence thesis:

> Commercial EV charger installations are increasingly paid only after the site is demonstrably backend-visible, load-managed, meter/billing-ready, photographed, tested, and handover-complete; a founder can control named final-payment/warranty/go-live holdbacks by producing buyer-approved release/no-go files for installed sites.

## Internal Gate Review

### Concrete 6-month control proof

Pass. First proof is current cash or an accepted rework/no-go against a named site:

- signed installer/CPO/fleet mandate;
- named installed chargers, serials, site, backend/OCPP target, final-payment or warranty/go-live holdback;
- source evidence from electrical contractor, charger backend, photos, as-built, test sessions, RFID/payment test, load-management notes, and handover checklist;
- buyer-approved release, scheduled payment, warranty activation, go-live, or paid no-go/rework decision.

### CAC, payback, margin, cash conversion

Pass if limited to commercial sites where at least 50,000 PLN of final payment, warranty value, or go-live revenue is at stake. Initial fees can be 4,000-12,000 PLN per small site and 15,000-40,000 PLN for fleet/depot/multi-site handovers, plus success fee only where payment release attribution is documented.

### Copy risk

Conditional pass. Installers, distributors, CPOs, OCPP platforms, and electrical contractors can copy checklists, but the startup controls a named payment holdback and release file once mandated. The wedge is neutral, fast, evidence-focused commissioning closeout for sites already installed and commercially blocked.

### Founder constraints

Pass with boundaries. Contractors handle electrical tests, measurement, safety signoff, repair, OCPP backend changes, payment terminal issues, load-management settings, and metrology/legal questions. The founder coordinates evidence, accepted/rework/no-go status, and buyer response packets.

### Duplicate-risk distinction

It is not HeatQuiet or heat-pump commissioning because the buyer, asset, evidence, and payment gate are EVSE-specific: OCPP/backend visibility, charger serials, RFID/payment test, load management, fleet/CPO go-live, and final-payment release. It is not BESSGuard because charger sites have higher unit volume, clearer backend tests, and smaller safety/engineering scope than commercial batteries.

### Simulated strongest objections

1. Installers and CPOs already have commissioning checklists and OEM portals.
2. Many failures require electrical repair, backend configuration, cellular/router work, charger firmware, load-management tuning, or payment-terminal fixes.
3. A packet cannot force the buyer or CPO to accept the site.
4. Unknown founder trust is weak around final payments and technical evidence.
5. The business may become low-margin project management or punch-list chasing.
6. Some sites need licensed electrical inspection, UDT, fire, metrology, or building closeout decisions outside scope.
7. OEMs and backend providers can automate the evidence.
8. Part-time execution may not fit urgent go-live deadlines.

### Internal Score

**88.3 / 100**

Advance to working-chat Zero To One validation because the simulated score is strictly above 87 and the control point is a named installed-site payment/warranty/go-live holdback with accepted release/no-go proof.
