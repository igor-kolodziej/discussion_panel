# Simulated Gate: KSeF Rejection Rescue Desk

## Exact Candidate Wording
AcceptedInvoice KSeF Rejection Rescue Desk for Polish accounting offices and ERP integrators. A same-day diagnostic/fix desk for accountants whose clients' FA(3) XML invoices are rejected or stuck in KSeF after mandatory rollout. It does not sell a new invoicing app. It sits behind accounting offices/ERP consultants as a white-label incident team: accountant uploads rejected XML, UPO/session status/rejection code, client ERP export sample, NIP/role/auth context, and desired invoice semantics; desk returns minimal XML diff/fix instructions, corrected FA(3) package, acceptance checklist, and vendor-specific mapping note. For offices with client authorization it can run test submission or guide accountant to resubmit until a KSeF number/UPO is obtained. Control point: accepted KSeF invoice number/UPO for invoices that cannot be legally issued/payment-collected while rejected; office incident queue routed through desk; proprietary corpus of rejection code -> ERP field -> semantic fix by vendor/industry. Two-month proof: 5 accounting offices/ERP consultants sign paid emergency retainer or incident contract; rescue 100 rejected/stuck invoices from 20 companies; achieve 80 accepted KSeF numbers/UPOs or documented client-side fix confirmations within 24h; collect 25k PLN; capture 50 recurring rejection patterns. Pricing: 300-900 PLN per incident bundle or 2k-6k PLN/month office retainer. Hidden insight: in KSeF rollout, the scarce service is not generic invoicing software but fast translation from opaque FA(3)/semantic rejections into accepted invoices inside accountants' existing systems; accepted UPO is a hard operational event.

## Simulated Score
84/100.

## Why It Clears 82
The control point is stronger than a report or advisory workflow: the outcome is an accepted KSeF invoice number/UPO, and a rejected invoice can block issuance, payment operations, and accounting closure. The wedge is narrow enough for a solo data/process founder because the first product is manual incident rescue, not a full invoicing suite.

## Strongest Caveats
- Competition from ERP/accounting vendors, KSeF validators, and implementation consultants is significant.
- The desk must avoid becoming unauthorized tax/accounting advice; it should fix schema/semantic/export issues and work through the accountant.
- Access to invoice XML and client authorization creates data-security and professional-liability requirements.
- The opportunity is deadline-driven; it must convert from emergency incidents into recurring monitoring and error-corpus leverage.
- Some failures may be ERP vendor bugs that the desk can diagnose but not directly fix.

## Decision
Pass simulated gate. Submit to working-chat gate.
