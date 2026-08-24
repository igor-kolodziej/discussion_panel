# Simulated Round 296: KSeF Unpaid Invoice Release Lockbox

Date: 2026-05-29 Europe/Warsaw
Gate in force: simulated score must be strictly >87 before real validation; working and fresh Zero To One gates are >=85.

## Current Regulatory / Timing Facts Checked

- The official KSeF site states that mandatory issuing in KSeF applies from 1 February 2026 for taxpayers whose 2024 gross sales exceeded 200 million PLN, and from 1 April 2026 for other taxpayers except the small monthly-sales exemption through the end of 2026.
- The same official page states that receiving invoices through KSeF is mandatory from 1 February 2026.
- The official KSeF FAQ says small taxpayers receiving invoices from large companies after 1 February 2026 can access the invoice through KSeF tools or a two-step access link/QR; it also states that the date of receipt is the date the KSeF number is assigned.
- The official FA(3) information sheet confirms FA(3) structure and operational details around structured invoice issuance, dates, offline/online modes, and KSeF number assignment.

Sources checked:

- `https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/`
- `https://ksef.podatki.gov.pl/ksef-news/wystawianie-i-otrzymywanie-faktur/`
- `https://ksef.podatki.gov.pl/media/gtjhkeek/information-sheet-on-the-fa-3-logical-structure-04032026.pdf`

## 32 Raw Hard-Control Candidates

| # | Candidate | Buyer | Acute trigger | Transferable control / proof | Internal cap reason | Sim score |
|---|---|---|---|---|---|---:|
| 1 | KSeF unpaid invoice release lockbox | Polish B2B suppliers with unpaid invoices | Enterprise AP rejects/holds payment for missing KSeF number, FA(3) issue, buyer access issue, PO/visualization mismatch, or correction | Signed payment-release mandate, exact unpaid invoice, buyer AP rejection, KSeF number/UPO or rejection log, corrected evidence, payment release | Strong current-cash wedge; accountants/ERP copy risk but proof is specific unpaid invoice | 88.6 |
| 2 | KSeF buyer-side input-VAT invoice retrieval desk | Polish buyers missing supplier invoices | Buyer cannot retrieve/identify received KSeF invoices for close | Buyer authorization, invoice retrieval log, matched KSeF IDs | More bookkeeping than cash recovery | 83.5 |
| 3 | KSeF mass correction pack for ERP migration defects | Mid-market ERP users | FA(3) batch rejections block month-end | Rejection exports and corrected batch | ERP vendors/accountants strong | 81.5 |
| 4 | KSeF foreign supplier fixed-establishment invoice routing | Polish groups with foreign branches | Buyer or supplier dispute whether KSeF is required | Exact transaction and tax/legal review route | Tax-advice boundary unresolved | 78.0 |
| 5 | KSeF public-sector vendor payment unblock | Vendors to public entities | Payment held for KSeF/PO mismatch | Invoice, KSeF ID, e-delivery/PO evidence, AP acceptance | Public payment friction real but slow | 84.0 |
| 6 | KSeF construction progress-payment release | Subcontractors | Main contractor holds milestone payment over KSeF/correction mismatch | Contract milestone, invoice, KSeF proof, AP release | Construction disputes can become legal | 84.5 |
| 7 | KSeF self-billing correction release | Suppliers in self-billing arrangements | Buyer self-billing KSeF issue blocks supplier cash | Self-billing agreement, correction, buyer AP acceptance | Niche and tax boundary | 82.0 |
| 8 | PEPPOL/KSeF cross-border invoice acceptance rescue | Exporters/importers | Foreign ERP rejects Polish KSeF visualization/QR evidence | Invoice mapping, buyer AP acceptance | Integration consultants strong | 80.5 |
| 9 | Retail ASN/OTIF chargeback recovery | CPG vendors | Retailer deducts operational chargebacks | Portal access, dispute cases, credit memo | Close to PromoLeak and incumbents | 84.0 |
| 10 | 3PL invoice overbilling recovery mandate | E-commerce brands | 3PL overcharges storage/pick/returns | Contract, WMS exports, credit memo | Consultants can copy; data messy | 82.5 |
| 11 | Freight detention/demurrage recovery mandate | Importers | Carrier/terminal charges already billed | B/L, gate logs, claim, credit | Freight-audit incumbents | 81.5 |
| 12 | Ocean ETS surcharge credit recovery | Importers | Shipping line EU ETS surcharge mismatch | Carrier invoice and credit claim | Too consultant/audit-like | 78.0 |
| 13 | Cloud reseller private-offer payout recovery | SaaS vendors | Marketplace remittance mismatch | Portal reports, case, payout | Already failed adjacent at 76 | 76.0 |
| 14 | OTA commission/virtual-card recovery | Hotels | Booking/Expedia statement mismatch | OTA exports, claim, credit | Revenue managers handle | 79.5 |
| 15 | Utility grid deposit refund release | Businesses | DSO deposit not returned after connection decision | Deposit receipt, DSO acknowledgment, refund | Legal/utility bureaucracy | 78.0 |
| 16 | Security-deposit release for SME lease exits | Tenants | Landlord holds deposit | Lease, handover proof, payment demand | Becomes legal dispute | 74.0 |
| 17 | Public-tender bid bond return desk | Tender losers | Bid bond/guarantee not released | Tender docs, bank guarantee release | Small ticket and legal/procurement | 77.5 |
| 18 | EUDR coffee/cocoa order-release packet | Importers/brands | Customer pauses order pending EUDR DDS/geolocation | Named order, supplier evidence, DDS/no-go | Compliance incumbents, source-truth risk | 85.0 |
| 19 | EUDR wood pallet/customer release packet | Packaging/wood importers | Buyer demands EUDR statement before shipment | Supplier docs and customer acceptance | Too broad; legal/compliance | 82.5 |
| 20 | PPWR packaging EPR fee correction recovery | Packaging importers | EPR invoices/fees mismatched | PRO invoice and credit | Admin consultancies copy | 79.0 |
| 21 | EAA checkout procurement release pack | E-commerce/SaaS vendors | Customer blocks procurement on accessibility | Audit evidence, remediation route | Consultants and tooling strong | 80.0 |
| 22 | NIS2 critical-supplier renewal evidence pack | Vendors to utilities/transport | Critical-entity customer blocks renewal | Live request, evidence room, progress | DORA-like, evidence-only, crowded | 84.5 |
| 23 | CRA/RED firmware security retail order release | Connected-device importers | Retailer asks for cyber evidence | Product evidence and order progress | Close REDBlocked | 82.0 |
| 24 | GPSR responsible-person listing unblock | Consumer product importers | Marketplace/retailer blocks listings | Listing case, responsible-person proof | Product compliance firms copy | 79.0 |
| 25 | Construction retention release mandate | Subcontractors | Retention withheld after acceptance | Contract, acceptance protocol, release invoice | Legal/collections risk | 80.0 |
| 26 | Energy-certificate subsidy payout release | Building owners/installers | Subsidy payment held over evidence | Program case and payment | Grants admin and seasonality | 78.5 |
| 27 | Warranty reserve release for B2B equipment vendors | Vendors | Enterprise holds warranty reserve | Contract, acceptance, release | Negotiation/legal | 77.0 |
| 28 | Customs guarantee discharge evidence pack | Importers | Customs guarantee remains tied to closed procedure | MRN, SAD, discharge evidence | Customs broker/legal boundary | 82.0 |
| 29 | Excise EMCS movement deposit release | Alcohol/fuel/logistics firms | Excise guarantee tied by unresolved movement | EMCS records and release | Regulated/excise risk | 76.0 |
| 30 | Waste BDO invoice payment release | Waste contractors | Customer/municipality blocks invoice over BDO/KPO mismatch | KPO, invoice, acceptance | Similar documentation rail failures | 78.0 |
| 31 | Used medical equipment serial-lot deposit match | Clinics/dealers | Buyer needs exact compact serial-numbered fleet | Title/reservation/deposit | Regulated-device and physical logistics | 76.5 |
| 32 | Lease-end POS terminal fleet deposit buyout | Retailers/resellers | Buyer deposits for exact fleet | Asset title and deposits | Commodity/payment-processing concerns | 75.0 |

## Finalists Considered

1. **KSeF unpaid invoice release lockbox**: strongest because first proof is actual payment release on current unpaid invoices, and the 2026 KSeF transition is live now in Poland.
2. **EUDR coffee/cocoa order-release packet**: good timing, but supplier source-truth, legal/compliance, and traceability-platform incumbents cap it below real validation threshold.
3. **NIS2 critical-supplier renewal evidence pack**: DORA-like but evidence-only and crowded; likely to be marked a line extension of DORA/GRC.
4. **KSeF public-sector vendor payment unblock**: attractive but narrower and slower than the broader AP rejection/payment-release version.
5. **Retail ASN/OTIF chargeback recovery**: monetary outcome, but too close to PromoLeak and existing deduction-recovery incumbents.
6. **Customs guarantee discharge evidence pack**: cash-like release, but customs broker/legal boundary is too strong for a part-time founder.

## Selected Candidate

**KSeF Unpaid Invoice Release Lockbox**

## Internal Scoring

| Area | Score | Notes |
|---|---:|---|
| Customer pain / willingness to pay | 9.0 | Unpaid B2B invoices and buyer AP rejection create immediate cash pain. |
| Business model | 8.5 | Fixed case fees plus small release-linked fee; no inventory or financing. |
| Control point | 9.0 | Exact unpaid invoice, buyer AP rejection, seller authorization, KSeF/UPO/rejection evidence, payment-release thread. |
| 60-day proof | 9.0 | 5-8 cases can be proven by AP acceptance/payment on named invoices. |
| Founder fit | 8.5 | Warsaw founder has local-language/process advantage; contractors/accountants can be used without becoming tax adviser. |
| Distribution | 7.5 | Outbound to SMEs selling to large Polish buyers; accounting offices and ERP implementers can refer exceptions. |
| Copy risk | 7.0 | Accountants, ERP vendors, AP automation tools, and tax advisers can copy the workflow; defense is live unpaid invoice mandate and exception memory. |
| Margin / cash conversion | 8.5 | Prepaid fees, quick cycles, limited contractor cost. |
| Durability | 7.0 | Strongest during 2026 transition; durability depends on recurring invoice exceptions, corrections, buyer portal quirks, and month-end pressure. |
| Legal/provider risk | 7.5 | Must avoid tax advice and certification; focus on evidence coordination and accountant-approved corrections. |

Simulated score: **88.6 / 100**

## Internal Cap Check

- Concrete 6-month control proof: yes, current unpaid invoices, buyer AP rejection, seller mandate, KSeF number/UPO or rejection log, corrected packet, AP payment release.
- One vendor contract/equipment purchase/consultant can copy: partially. Accountants and ERP vendors can copy the generic workflow, but not the exact live unpaid invoice case once authorized. This keeps the score below 90 but not below 87.
- CAC/payback/margins/cash conversion: plausible because seller pays from blocked invoice pain; prepaid fixed fee required.
- Partnerships/goodwill dependence: not primary. Partner referrals help, but direct acquisition can target sellers with live AP rejection text.
- Clinical/legal/regulated authority unresolved: tax/legal boundary exists, but the startup does not provide tax advice, issue invoices as provider of record, or certify VAT compliance; it coordinates evidence and routes tax/legal calls to the seller's accountant/adviser.

## Why This Is Worth Real Validation

This is ugly, local, administrative, and cash-linked. It fits the stronger search pattern better than recent evidence desks because the product starts only after there is a named unpaid invoice and a written buyer AP blocker. The first proof is not a better dashboard or readiness memo; it is an AP acceptance, scheduled payment, actual payment, corrected KSeF submission, or explicit no-go that protects the seller from chasing a bad invoice.

Main risk: Zero To One may view it as temporary KSeF support that accountants, ERP vendors, and AP departments will absorb. The prompt needs to emphasize current unpaid invoices, prepaid mandates, no tax advice, and payment-release outcomes.
