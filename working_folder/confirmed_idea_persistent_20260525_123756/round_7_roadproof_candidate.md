# Round 7 Candidate: RoadProof Patch Ledger

Date: 2026-05-25 Europe/Warsaw.

## Why This Pivot

Several route-book and micro-acquisition ideas solved cold start but stayed copyable. The strongest confirmed pattern in the archive is different: a contractor-paid live event ledger that captures evidence before the invoice exists, tied to a payment/acceptance event and public-procurement-visible buyers.

This candidate applies that pattern to a different municipal-service vertical with higher event value and less animal-care specificity: small road-maintenance contractors.

## Exact Candidate Wording For Simulated Scoring

**RoadProof Patch Ledger** is a mobile-first invoice-evidence rail for small Polish road-maintenance contractors that perform per-event or call-off pothole patching, pavement repairs, curb/sidewalk fixes, drainage-inlet fixes, road-sign/furniture repairs, roadside mowing/clearing, emergency safety works, or winter-damage repairs for gminas, powiats, housing cooperatives, retail parks, industrial sites, and facility managers.

It does not sell generic construction project management, fleet GPS, public-sector software, or a dashboard. It activates only when the contractor already has a maintenance/call-off contract or repeated work orders where payment depends on defensible location, quantity, material, and acceptance evidence.

Crew leads capture every billable repair event through a WhatsApp/QR/mobile web flow before leaving the site: GPS/location, road/asset identifier, before/after photos, defect class, repair method, dimensions or tonnage, asphalt/cold-mix/material batch or delivery ticket, crew/time, traffic-safety setup where relevant, client work-order number, and acceptance/witness signature or later inspector note. The system hashes/timestamps the event, detects missing fields before month-end, reconciles events to material tickets and work orders, and produces client-specific invoice attachment packets.

Buyer: owner-operated and small Polish road-maintenance contractors serving 2-10 public or institutional clients where month-end invoices depend on many small repair events, photos, measurements, material tickets, and acceptance protocols.

Acute trigger: the contractor loses margin or cash because municipal/facility clients question whether a pothole, patch, sign, drain, or mowing event was completed, whether the invoiced quantity matches reality, whether material tickets support the invoice, or whether month-end photos/notes are too scattered to defend the invoice quickly.

Hidden insight: small road-maintenance contractors do not mainly need another fleet tracker or construction ERP. Their invoice becomes defendable or weak at the roadside, when the crew has one chance to capture photos, location, dimensions, material, and client work-order context. Municipal and facility clients often verify small works after the fact, while contractors reconstruct packets from WhatsApp, paper notes, asphalt tickets, and memory.

Primary control point: a paid, signed all-event-routing mandate inside one contractor's daily workflow for at least two named clients. The pilot contract requires all new eligible billable repairs/call-offs for those clients to be captured through RoadProof first. The second proof is written client-side packet-format acknowledgement, correction, or usable feedback through the contractor's existing client contact. Without all-event routing and client-format feedback, the POC is killed.

2-month proof under 100,000 PLN: build a public-procurement target list of 30-80 qualified contractors; sign one prepaid pilot at 6,000-15,000 PLN covering at least two named clients; capture 50+ repair/maintenance events or 200,000+ PLN invoiced work value; generate two client-specific invoice packets; obtain at least one written client acknowledgement, field correction, or usable packet-format feedback; measure invoice-prep time reduction or reduction in missing evidence; and collect at least 10,000 PLN in pilot/packet fees.

Cold start: use BZP/e-Zamowienia, BIP, Platforma Zakupowa, and municipal/powiat contract award pages to identify contractors with call-off road-maintenance contracts, pothole repair packages, road emergency work, or unit-price maintenance tenders. Outbound references the specific public contract and asks for a prepaid 60-day all-event-routing pilot only if the contractor has evidence/payment pain.

Pricing: 6,000-15,000 PLN 60-day pilot for two clients, then 1,500-5,000 PLN/month per contractor plus per-packet or per-event overage. Larger contractors pay for additional clients/crews.

Why this is not a service/report/dashboard/database/marketplace: RoadProof does not clean old documents or list suppliers. It controls the live event ledger before invoices exist; the ledger becomes the source evidence object for work-order acceptance, invoice attachments, material-ticket reconciliation, and client-specific acceptance memory.

## Initial Strategic Notes

Likely strengths:

- concrete payment/acceptance trigger;
- public procurement exposes target list without privileged access;
- 2-month proof is possible in road-maintenance season;
- mobile/photo/GPS/OCR workflow fits founder skills;
- one contractor can route all events without gmina procurement.

Likely risks:

- close structural adjacency to the existing animal-care TraceFaktura idea;
- civil/road contractors may already use GPS/fleet/photo apps or client inspection systems;
- field crews may resist mobile capture unless extremely lightweight;
- if clients do not question invoices, willingness to pay falls.
