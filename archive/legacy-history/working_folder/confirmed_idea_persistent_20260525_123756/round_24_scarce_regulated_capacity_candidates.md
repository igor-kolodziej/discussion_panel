# Round 24: Scarce Regulated Capacity And Emergency Continuity

Created: 2026-05-25

## Pivot Rationale

Rounds 22 and 23 failed because assigned-rights, salvage, and public-auction ideas controlled isolated transactions but did not create privileged repeat flow. Round 24 searches for capacity that can be reserved, stocked, or physically controlled before an urgent regulated transaction occurs.

Filter:

- the buyer must be line-down, shipment-blocked, route-blocked, or legally unable to operate;
- the founder must control stock, dated capacity, inspection slots, or legally usable replacement assets;
- 60-day proof must include prepaid capacity plus customer deposit/cash use;
- reject anything that is only scheduling, advisory, compliance evidence, or generic brokerage.

## Source Anchors

- EU Regulation 2024/573 restricts F-gas use and explicitly preserves exceptions for labelled reclaimed/recycled gases for maintenance/servicing of existing equipment; from 2026, high-GWP gases for AC/heat pumps are prohibited except reclaimed/recycled categories until 2032: https://eur-lex.europa.eu/eli/reg/2024/573/oj/eng
- UDT describes Polish F-gas/SZWO obligations and certification context: https://www.udt.gov.pl/uslugi-udt/szwo-i-f-gazy/o-f-gazach-i-szwo
- The European Labour Authority states that from 2026-07-01 smart tachographs G2V2 are mandatory for light commercial vehicles over 2.5t and up to 3.5t used for international goods transport/cabotage for hire or reward: https://www.ela.europa.eu/assets/lcv2026/index.html?etrans=hr
- PIORIN states that ISPM-15 wood packaging requires heat treatment and an IPPC-approved mark; violations for export wood packaging can be fined: https://www.gov.pl/web/piorin-en/wood-packaging
- COCH provides ATP/FRC testing, GDP mapping, refrigeration-equipment testing, refrigerant analysis, and inspection services, confirming specialized certified capacity around refrigerated transport and cold chain: https://www.coch.pl/en/atp-agreement/
- TDT lists ADR dangerous-goods tanker inspection/technical supervision areas: https://www.tdt.gov.pl/dzialalnosc/dzialalnosc-dozorowa/urzadzenia-podlegajace-dozorowi-technicznemu/urzadzenia-do-transportu-towarow-niebezpiecznych/cysterny-do-przewozu-towarow-niebezpiecznych/
- UDT states that covered technical devices require operating permission and a positive administrative decision before lawful operation; inspection marking alone is not enough: https://www.udt.gov.pl/?Itemid=906&id=914:faq-dozor-techniczny-inspekcja&option=com_content&view=article

## Candidate Set

| # | Candidate | Buyer | Acute trigger | Control point | 2-month proof | First acquisition mechanism | Gross margin / payback logic | Copy risk |
|---:|---|---|---|---|---|---|---|---|
| 1 | Reclaimed High-GWP Refrigerant Emergency Stock | Cold stores, supermarkets, food plants, data centers, HVAC contractors | Leak/repair on legacy refrigeration, AC, or heat-pump equipment; virgin high-GWP service paths restricted and certified emergency supply is scarce | Legally labelled reclaimed refrigerant cylinders, source contracts, lab/purity docs, retained certified F-gas technician/company capacity | Buy compliant limited stock, reserve 2 certified technicians, sell 3 emergency recharge/repair continuity jobs with prepaid deposits | Cold-store and supermarket maintenance managers, HVAC contractors, family OZE/HVAC network | Stock spread plus emergency service margin; high willingness to pay when inventory/food/data uptime is at risk | Medium: incumbents can buy gas, but not if scarce stock and technician slots are locked locally |
| 2 | G2V2 Tachograph Retrofit Slot Bank For 2.5-3.5t International Vans | Courier, express, furniture, event, and cross-border van fleets | 2026-07-01 EU rule makes G2V2 tachographs mandatory for qualifying LCVs; fleets risk losing international route legality | 8-15 tachograph G2V2 kits plus dated installation/calibration slots at authorized workshops | Prepay June workshop capacity, buy kits, sell 10-15 installs with 50% deposits before deadline | Fleets running Poland-Germany/Benelux/Czech routes; transport accountants; route permit consultants | Buy install/kit package, resell deadline-guaranteed slot at premium; payback before install via deposit | Medium-low until deadline passes; after deadline becomes recurring retrofit/expiry pool |
| 3 | ISPM-15 Export Packaging Unblock | Machinery exporters, freight forwarders, warehouses, exporters to UK/US/Asia | Export shipment blocked or rework required because wood packaging lacks valid ISPM-15 treatment/mark | Stock of heat-treated stamped pallets/dunnage/crates plus exclusive emergency kiln/marking capacity from approved facility | Stock near Gdansk/Gdynia or central export zone; sign 3 forwarders; sell same-day repack/re-palletize jobs | Forwarders handling export exceptions, machinery exporters, port/warehouse ops | Emergency stock/repack margin; high when container or shipment delay costs exceed pallet cost | Medium-high: packers can copy, but local stock plus forwarder exception flow matters |
| 4 | ATP-Certified Reefer Vehicle / Inspection Slot Rescue | Food exporters, refrigerated transport SMEs, cold-chain shippers | ATP-valid vehicle/certificate missing or failed; perishable international shipment cannot move | Short lease/options on ATP-valid vehicles/trailers plus reserved certificate/inspection slots | Control 2 certified vehicles or 5 certificate-renewal slots; sell 3 urgent loads/renewals | Food exporters, small reefer carriers, cold-chain brokers | Rush rental/slot margin; payback from perishable delay avoidance | Medium: large carriers compete unless niche geography/equipment is narrow |
| 5 | ADR/TDT Tanker Inspection + Defect-Part Slots | Small fuel/chemical/food-grade tanker operators | Tanker cannot load because inspection, cleaning, gas-free certificate, or defect part is missing | Reserved TDT/ADR inspection/repair windows plus high-failure valves, seals, relief devices, and partner wash/degassing capacity | Pick one tank type, buy top failure parts, reserve workshop/TDT dates, sell 5 urgent recoveries | Small ADR carriers rejected by shippers/terminals; repair shops | 300-1,500 PLN margin per tank event; repeat by fleet cycle | Medium: OEM/service incumbents exist, but parts+slot custody can win neglected tank classes |
| 6 | UDT-Valid Replacement Lift Capacity | Warehouses, factories, contractors, installers | Forklift/scissor lift/telehandler failed inspection or awaits UDT decision; site needs lawful replacement today | One or two niche UDT-current machines with docs, transport, charger, and service records | Lease/buy one niche unit, sell 5 emergency replacement rentals to asset owners waiting on UDT | Cold stores, factories, construction sites, forklift service shops | Emergency rental premium; payback if utilization is high and unit is non-commodity | Medium-high for standard forklifts; stronger for odd specs/underserved geography |

## Finalists Sent To Simulated Scoring Agents

1. Reclaimed High-GWP Refrigerant Emergency Stock
2. G2V2 Tachograph Retrofit Slot Bank For 2.5-3.5t International Vans
3. ISPM-15 Export Packaging Unblock
4. ATP-Certified Reefer Vehicle / Inspection Slot Rescue
5. ADR/TDT Tanker Inspection + Defect-Part Slots
6. UDT-Valid Replacement Lift Capacity

## Initial Read Before Scoring

Reclaimed high-GWP refrigerant and G2V2 tachograph slots are the only candidates that currently look capable of breaking simulated `>87`. They combine near-term regulatory pressure, hard asset/capacity control, and a buyer who pays because operations stop without the asset.

