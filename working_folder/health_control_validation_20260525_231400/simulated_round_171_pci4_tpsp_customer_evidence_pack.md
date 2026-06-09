# Simulated Round 171: PCI4 TPSP Customer Evidence Pack

Date: 2026-05-29
Real gate: working Zero To One >=85, fresh Zero To One >=85
Simulation gate: strictly >87

## Source Checks

- PCI DSS v4.0.1 is the active PCI DSS version and the v4 future-dated requirements are now in scope for assessments.
- PCI DSS v4 includes third-party service provider duties around supporting customer PCI compliance, including written responsibility acknowledgment and information on which PCI DSS requirements are the responsibility of the TPSP, the customer, or shared.
- Public PCI practitioner discussions repeatedly point to v4 responsibility matrices, service-provider evidence, AOC scope, and payment-page script requirements as active friction for merchants, QSAs, and third-party providers.

## 34 Raw Candidates Forced Through Hard-Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | Internal score/cap reason |
|---|---|---|---|---|---|---|
| 1 | PCI4 TPSP Customer Evidence Pack | SaaS/payment-adjacent vendors | merchant customer QSA/acquirer evidence blocker | live customer request + vendor evidence packet | customer/QSA acceptance, renewal or assessment unblock | 89.5: DORA-like vendor-side evidence pressure with live buyer gate |
| 2 | SWIFT CSP Assessor-Ready Evidence Pack | small SWIFT users/service bureaus | annual KYC-SA attestation | assessor-scoped evidence room | assessor acceptance | 84: regulated-bank trust and cyber incumbent pressure |
| 3 | SEPA VoP Sponsor-Bank Readiness Pack | payment fintechs | sponsor bank VOP readiness request | test results and EPC evidence | sponsor signoff | 82: payments expertise, narrow buyer |
| 4 | KSeF ERP Vendor Buyer Evidence Pack | Polish ERP/invoicing SaaS | customer procurement KSeF readiness blocker | buyer questionnaire + test evidence | customer acceptance | 81: KSeF variants already underperformed |
| 5 | French PDP Vendor Connection Pack | ERP vendors selling in France | French e-invoicing PDP readiness | PDP proof packet | buyer signoff | 79: geographic/language/local incumbent risk |
| 6 | SOC2 Customer Security Addendum Pack | small SaaS vendors | enterprise customer renewal | customer questionnaire | renewal signoff | 76: generic security evidence |
| 7 | ISO27001 Supplier Control Pack | B2B SaaS vendors | customer procurement | evidence response | acceptance | 73: mature consulting market |
| 8 | NIS2 Supplier Evidence Pack | ICT suppliers | customer NIS2 questionnaire | evidence pack | customer response | 78: similar variants failed |
| 9 | EU AI Act Procurement Evidence Pack | AI SaaS vendors | buyer AI Act request | risk/classification packet | buyer acceptance | 76: AI branch fatigue |
| 10 | CRA Vulnerability Policy Customer Pack | embedded software vendors | buyer asks for CRA reporting proof | CVD policy and incident route | buyer acceptance | 77: not yet enough live cash |
| 11 | App Store Privacy Nutrition Release Pack | app publishers | App Review privacy block | evidence response | app approval | 72: platform evidence desk |
| 12 | Google Play Data Safety Evidence Pack | app publishers | policy rejection | evidence response | app approval | 70: agencies and simple admin |
| 13 | Google Cloud Marketplace Security Pack | SaaS vendors | listing/procurement security review | response packet | listing approval | 79: AppExchange-like prior fail |
| 14 | Microsoft Commercial Marketplace Pack | SaaS vendors | marketplace listing blocker | evidence packet | listing approval | 77: incumbents and generic security |
| 15 | Vendor Risk Cyber Insurance Pack | SaaS vendors | insurance renewal request | evidence packet | quote/bind | 76: cyber insurance variant failed |
| 16 | Bank Account KYB Evidence Pack | ecommerce/fintech merchants | account/payout hold | KYB packet | release | 74: trust, legal, platform opacity |
| 17 | Stripe Connect Platform TPSP Pack | platforms | connected account compliance | platform docs | approval | 72: platform-specific and copyable |
| 18 | FedRAMP Customer Package Extractor | US gov SaaS vendors | agency procurement | inherited controls packet | buyer acceptance | 74: US public-sector/incumbent |
| 19 | CMMC Supplier Evidence Pack | defense suppliers | prime contractor gate | evidence packet | prime acceptance | 73: US defense/C3PAO trust |
| 20 | HIPAA BAA Security Packet | health SaaS vendors | buyer security review | evidence response | buyer acceptance | 70: health/legal |
| 21 | FERPA/EdTech Student Data Pack | edtech vendors | school procurement | privacy/security evidence | buyer acceptance | 72: generic procurement |
| 22 | Accessibility VPAT Procurement Pack | SaaS vendors | EAA/VPAT buyer gate | VPAT/evidence | buyer acceptance | 77: EAA failed |
| 23 | Anti-Slavery Supplier Evidence Pack | manufacturers | enterprise ESG gate | supplier proof | buyer acceptance | 68: generic reports |
| 24 | Battery Passport Supplier Pack | battery importers | customer asks DPP proof | data packet | buyer acceptance | 76: BatteryFit duplicate risk |
| 25 | EPREL Retailer SKU Evidence Pack | appliance suppliers | retailer asks EPREL | EPREL data | buyer acceptance | 73: GreenTender/EPREL duplicate |
| 26 | PSD2 SCA Evidence Pack | payment vendors | acquirer/customer request | SCA evidence | acceptance | 74: old/mature |
| 27 | Open Banking TPP Evidence Pack | fintechs | bank partner onboarding | consent/security evidence | signoff | 76: regulated/partner heavy |
| 28 | AML Vendor Model Evidence Pack | regtech vendors | bank model validation | model evidence | customer acceptance | 78: bank-side consultants |
| 29 | Ledger SOC Bridge Letter Pack | SaaS vendors | year-end audit request | bridge letter/evidence | auditor acceptance | 71: accountants/auditors |
| 30 | Data Processing Addendum Rescue Pack | SaaS vendors | procurement legal block | DPA map | signoff | 68: legal generic |
| 31 | Vendor Subprocessor Delta Pack | SaaS vendors | renewal review | subprocessor evidence | acceptance | 72: too generic |
| 32 | Pen-Test Exception Evidence Pack | SaaS vendors | customer asks pen test | issue triage | acceptance | 73: common security consulting |
| 33 | Payment Page Script Control Pack | merchants/agencies | PCI 6.4.3/11.6.1 blocker | script inventory and control proof | QSA acceptance | 82: stronger but merchant-side, QSAs own |
| 34 | Contact-Center PCI Call Recording Pack | call centers | PCI v4 assessment | DTMF/pause/resume evidence | QSA acceptance | 80: incumbent PCI assessors |

## Finalists

| Finalist | Internal score | Why advanced | Why not winner |
|---|---:|---|---|
| PCI4 TPSP Customer Evidence Pack | 89.5 | Live customer/QSA/acquirer evidence requests pressure vendors, not merchants; clear artifact; high renewal/procurement stakes; close to proven DORA pattern but different regulation and buyer. | QSAs/PCI consultants can copy; must avoid claiming certification. |
| SWIFT CSP Assessor-Ready Evidence Pack | 84 | Strong annual external gate. | More regulated, more cyber-assessor dependent. |
| SEPA VoP Sponsor-Bank Readiness Pack | 82 | Real payments infrastructure gate. | Payment scheme expertise and sponsor-bank trust are hard. |
| KSeF ERP Vendor Buyer Evidence Pack | 81 | Local Warsaw advantage and current mandate. | KSeF variants already underperformed; ERP integrators/accountants internalize. |
| Payment Page Script Control Pack | 82 | Specific PCI v4 pain around payment scripts. | Merchant-side/QSA-owned; less vendor-side leverage. |

## Chosen Candidate

Idea name: PCI4 TPSP Customer Evidence Pack

One-sentence thesis: Turn live PCI DSS v4.0.1 third-party service provider evidence requests from merchant customers, QSAs, and acquirers into buyer-ready responsibility matrices, written acknowledgments, scope notes, and evidence packets for SaaS and payment-adjacent vendors whose renewals or procurements are blocked.

Exact buyer: 20-250 person SaaS, ecommerce infrastructure, booking, ticketing, subscription billing, payment orchestration, call-center payment, hosted checkout, iframe/widget, loyalty, and order-management vendors that touch, redirect, host, script, support, or can affect a merchant customer's cardholder data environment but do not have a mature PCI evidence function.

Acute trigger: A merchant customer, QSA, acquiring bank, payment facilitator, or enterprise procurement team asks the vendor for PCI DSS v4.0.1 TPSP evidence before completing a merchant SAQ/ROC, contract renewal, procurement approval, or payment-flow launch. The request often asks for AOC scope, written responsibility acknowledgment, responsibility matrix, service-provider status, evidence for requirements managed by the TPSP, payment-page script responsibility, incident/contact process, and customer/TPSP shared controls.

Control point: The live customer/QSA/acquirer request, the vendor's existing contracts and technical/security evidence, and a fixed-scope response packet that maps exactly which PCI DSS requirements are vendor, customer, shared, out of scope, or require QSA review. The startup controls the response workflow and accepted wording for a live commercial blocker, not a generic PCI readiness report.

60-day signed/titled/assigned/prepaid proof:

- Three vendors sign fixed-fee packs tied to live customer/QSA/acquirer evidence requests.
- At least five real request threads are assigned under NDA, with customer deadline and renewal/procurement/payment-flow value recorded.
- Two packets receive explicit customer, QSA, acquirer, or procurement acceptance, or a written "this resolves our TPSP evidence request" response.
- First partner referral from a PCI consultant/QSA who does not want low-margin evidence collation.
- First renewal/procurement/payment-flow release is attributed to the packet.

6-month POC:

- Build a target list of 80 vendors whose products can affect merchant checkout or cardholder-data environments but are unlikely to have a polished PCI v4 TPSP evidence function.
- Sell 10-15 packs at 10,000-28,000 PLN each.
- Build a private request-to-evidence library: responsibility-matrix rows, QSA objections, customer wording, AOC scope explanations, 12.9.1 written acknowledgments, 12.9.2 support artifacts, 12.8.4/12.8.5 customer information, payment-page script responsibility, service-provider vs non-service-provider boundary, and "unsafe to answer without QSA/legal review" flags.
- Convert 3-5 vendors into annual evidence refresh retainers before their merchant customers' next PCI cycle.

Economics:

- Fixed fee: 10,000-28,000 PLN per live TPSP customer evidence pack, based on number of customer requests, scope complexity, and urgency.
- Annual refresh: 6,000-14,000 PLN for updated responsibility matrix, AOC/scope note refresh, customer FAQ, and changed-since-last-cycle memo.
- Partner margin: 20-30 percent for PCI consultants, QSAs, fractional CISOs, payment agencies, and payment integration firms that refer work outside their desired scope.
- Delivery cost: founder evidence mapping plus 1-3 hours of paid PCI reviewer/QSA-adjacent issue spotting on flagged sections; no formal PCI assessment or certification.
- Gross margin target: 60-75 percent after reviewer and partner fees.
- Buyer payback: one saved enterprise merchant renewal, payment-flow launch, or QSA assessment delay can justify the fee.

Copy risk:

QSAs, PCI consultants, GRC platforms, and security consultants can copy the artifact set. The wedge is speed and side selection: the first buyer is the vendor being chased by several merchants/QSAs, not the merchant doing its own assessment. Incumbents tend to sell formal assessments, broad PCI programs, or merchant-side advisory; this product is a narrow customer-facing evidence response for live third-party requests.

Why incumbents cannot copy before the founder controls the specific asset/account/case/claim/lot/payment stream:

Once the vendor signs the engagement and assigns the live customer/QSA request threads, the founder controls the evidence intake, response chronology, QSA/customer objection log, and accepted wording for that commercial blocker. A QSA or consultant can copy the method later, but not the already-assigned request threads, customer deadlines, or accepted packet memory.

Why it is not a service, report, app, dashboard, database, marketplace, or generic broker:

The paid artifact is a buyer-ready response pack for a live customer/QSA/acquirer request: responsibility matrix, written responsibility acknowledgment, evidence index, safe-answer pack, customer FAQ, and escalation notes. It is sold only when a real commercial blocker exists. It is not certification, a formal assessment, ongoing consulting, a dashboard, or a brokered introduction.

Boundaries and legal/provider limits:

- The startup does not claim the vendor is PCI compliant, issue an AOC, act as QSA, perform a ROC/SAQ, or provide legal advice.
- Existing QSA, acquirer, customer assessor, and vendor counsel remain decision-makers for PCI scope, compliance status, contractual acknowledgments, and formal attestation.
- The packet separates answerable now, QSA review needed, legal review needed, technical remediation needed, and unsafe-to-answer items.
- Paid PCI reviewer input is issue spotting only unless a properly qualified partner is separately engaged by the vendor.

Duplicate risk:

Not DORA Bank Renewal Evidence Pack: the gate is PCI DSS v4.0.1 TPSP customer evidence, not regulated-finance DORA/ICT supplier risk. Not PromoLeak: this is not retailer deduction recovery. Not REDBlocked: no Amazon product compliance. The commercial mechanism is similar to DORA in that it is vendor-side evidence pressure, but the buyer trigger, artifact, counterparty, and proof are materially different.

Strongest anticipated objections:

- This may be too close to generic security/compliance consulting unless the live QSA/customer request is mandatory for every engagement.
- QSAs and PCI consultants may already provide responsibility matrices and customer evidence packs.
- Vendors with enough merchant customers may already have PCI AOCs, trust portals, or GRC teams.
- Vendors without enough merchant customers may not pay 10,000-28,000 PLN.
- PCI scope is subtle; wrong wording can create liability or overclaim compliance.
- Customer/QSA acceptance may depend on technical controls the founder cannot create.
- Some buyers will need a formal SAQ/ROC or remediation project, not an evidence response pack.

## Internal Score

Simulated score: 89.5

Reason for passing simulation gate: This most closely resembles the best confirmed evidence-pack pattern while avoiding direct duplication. The pressure comes from live customer/QSA/acquirer requests, the vendor has a commercial blocker, the artifact is concrete, buyer payback is tied to renewal/procurement/payment launch, and the founder can validate quickly without becoming a QSA. The main risk is PCI incumbent copy and scope/liability, which keeps it below 91.

Gate decision: advance to working Zero To One validation.

## Kill Criteria

- Working score below 85.
- Reviewer says this is generic PCI consulting or QSAs fully own the workflow.
- Reviewer says vendor willingness to pay is weak without full PCI assessment authority.
- Reviewer says customer/QSA acceptance cannot be controlled within 60 days.
