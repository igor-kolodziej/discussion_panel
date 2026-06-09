# Simulated Gate: KSeF Month-End Acceptance Rail

## Exact Candidate Wording
KSeF Month-End Acceptance Rail. A retainer-based operations desk for Polish accounting offices and small ERP integrators whose SME clients use mixed ERPs, sales systems, marketplace exports, and legacy invoicing tools that now must produce FA(3) invoices accepted in KSeF before month-end billing, payment collection, and accounting close. It does not sell a new invoicing app, broad KSeF consulting, or generic XML validation. Accounting offices route only exception batches and client exports that fail, stall, or repeatedly reject in KSeF. The desk ingests rejected/stuck FA(3) XML, KSeF session/UPO/rejection status, client ERP/export samples, buyer/seller NIP/auth context, invoice semantic notes approved by the accountant, and prior accepted examples. It returns corrected XML diffs, exact field/source-system mapping notes, accepted-ready batch package, resubmission checklist, office/client fix card, and if authorized either guides the office through resubmission or submits through the delegated client/accountant path until a KSeF number/UPO or written fix confirmation is obtained. The office adds a client engagement addendum saying KSeF exception batches route through this rail under a defined business-day SLA. Control point: accounting-office routed month-end exception queue, delegated/authorized KSeF submission or resubmission workflow where permitted, accepted KSeF number/UPO as the hard outcome, recurring ERP/vendor error corpus by office/client/source system, and renewal retainer tied to month-end close. Two-month proof: 5 accounting offices or ERP integrators pay retainers; 50 client batches or 500 real invoices processed; at least 90% of fixable cases receive KSeF number/UPO, accepted-ready XML, or accountant-confirmed source fix within one business day; 30k PLN cash collected; at least 3 offices send repeat batches in the second month; 80 recurring error mappings captured. Pricing: 2k-6k PLN/month per office for a defined exception volume plus 150-500 PLN per complex rejected invoice/batch. Hidden insight: KSeF chaos is not only a launch spike; accounting offices become the practical operations owner for clients using messy ERPs and marketplace exports, and they need a shared acceptance rail that converts recurring rejection patterns into accepted invoices without forcing every office to become a KSeF/XML debugging shop.

## Simulated Score
86/100.

## Why It Clears 82
This is stronger than one-off KSeF rejection rescue because it turns the same hard outcome, KSeF number/UPO, into a recurring accounting-office month-end workflow with repeat batches and retained routing. It addresses the prior same-day support caveat by using business-day SLA windows, retainers, and office-level exception queues rather than unlimited ad hoc emergency incidents.

## Strongest Caveats
- Delegated KSeF access and invoice XML data require strict security, DPA, and scope controls.
- Accounting offices may expect ERP vendors to fix problems for free.
- Some rejections reflect substantive invoice/accounting issues and must be approved by the accountant/client.
- ERP vendors and KSeF tooling can absorb common errors over time.
- The desk must show repeat office batches, not just one-off launch chaos.

## Decision
Pass simulated gate. Submit to real working-chat gate.
