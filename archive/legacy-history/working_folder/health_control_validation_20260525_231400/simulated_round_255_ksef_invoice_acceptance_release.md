# Simulated Round 255 - KSeF Invoice Acceptance Release

Date: 2026-05-30 Europe/Warsaw
Working folder: `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/`

Real browser gate for this run: working `>=85`, fresh `>=85`.

## Context Read

Recent failures show that generic recovery mandates, portal evidence desks, official-system onboarding, and commodity route books do not pass the real gate. The next candidate must show current cash movement, buyer-side acceptance, and a control point stronger than a checklist.

Poland's KSeF mandatory e-invoicing rollout is live in 2026. Large taxpayers moved first from 1 February 2026 and the wider VAT-registered business population followed from 1 April 2026. The useful wedge is not broad KSeF implementation. The sharper wedge is a live unpaid invoice queue where the seller's invoice is rejected, not found, not matched, or not released by the buyer's AP team because the KSeF number, FA(3) XML, correction, buyer NIP, PO, or acceptance evidence does not line up.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Control point | 60-day proof | Acquisition | Economics | Copy risk | Why incumbent cannot copy before control | Not service/report/app/broker |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KSeF invoice payment release desk | Foreign-owned Polish subsidiaries and CEE suppliers with unpaid Polish B2B invoices | Buyer AP refuses or delays payment because KSeF acceptance/matching is broken | Signed release mandate, unpaid invoice queue, KSeF/UPO/XML/correction evidence, buyer AP acknowledgement | 10-50 invoices accepted and first paid batch | Accountants, KSeF integrators, foreign chambers, CFO groups | 4k-12k PLN sprint plus 1-2% released cash | Accountants/ERP providers | Specific AP queue, buyer contacts, release trail, and cash attribution are controlled case by case | Payment release queue |
| 2 | KSeF correction-note cash unblock | Polish suppliers with rejected correction invoices | Corrections block credit notes, refunds, or month-end payment | Correction queue and buyer AP acceptance log | Buyer accepts corrections and releases payment | Accountants and CFOs | Fixed fee per correction batch | Accountants | Founder controls only if specific correction queue is mandated | Cash unblock |
| 3 | KSeF foreign-vendor registration bridge | Foreign companies needing Polish invoice compliance | New Polish customer refuses non-KSeF invoice | Onboarding checklist, local accountant handoff | First valid invoice issued | Foreign chambers | Setup fee | KSeF SaaS/accountants | Weak: implementation vendors can copy | Implementation, reject |
| 4 | KSeF invoice evidence pack for enterprise vendors | Vendors asked for KSeF readiness evidence in procurement | Buyer onboarding blocked | Evidence pack | Buyer accepts vendor | Integrators | 5k-10k | Consultants | Weak: no cash movement | Evidence pack, reject |
| 5 | KSeF received-invoice archive rescue | SMEs cannot find received invoices in KSeF | Month-end close delayed | Inbox export and matching | Close completed | Accountants | 2k-8k | Accounting software | Weak: software solves | Back-office service |
| 6 | KSeF Offline24 certificate continuity desk | Field sellers need Offline24 fallback | Sales interrupted during outage/field work | Certificate setup and procedure | Certificates issued and first offline invoice uploaded | POS vendors | 3k-8k | POS/ERP vendors | Weak: implementation | Setup service |
| 7 | KSeF AP duplicate-payment recovery | Buyers paid PDF and KSeF duplicate | Duplicate payments found | Recovery mandate | Refund/offset collected | AP teams | Success fee | AP audit firms | Stronger but narrower and after cash leak | Recovery mandate |
| 8 | KSeF buyer NIP mismatch release | Payment stuck due wrong buyer identity or branch mapping | Buyer AP refuses invoice | Invoice queue plus correction evidence | Corrected invoice paid | CFO/accountant | Fixed batch fee | Accountants | Specific queue control | Cash release |
| 9 | KSeF PO-to-UPO payment bridge for construction subcontractors | Subcontractors to large general contractors | Monthly invoice not released | PO, protocol, UPO, AP approval | First payment | Construction finance groups | 5k-15k | Accountants/GC portals | Possible but construction-specific/legal offsets | Payment bridge |
| 10 | KSeF recurring supplier AP lockbox | Recurring service vendors to large Polish customers | Every month invoices get stuck | Standing AP release process | 3 months paid on time | CFOs | Monthly 3k-8k | Accountants | Buyer-specific process memory | Payment route |
| 11 | EAA checkout accessibility procurement pack | Checkout/payment SaaS vendors | Enterprise renewal blocked by EAA accessibility evidence | Live questionnaire and test traces | Buyer accepts pack | Accessibility partners | 8k-20k | Accessibility firms | Weak: incumbents | Evidence pack |
| 12 | EAA bank accessibility release sprint | Banking service vendors | Bank asks for EN 301 549/WCAG evidence | Test evidence and VPAT/ACR | Procurement moves | Banks/consultants | 12k-30k | Accessibility firms | Weak: known market | Evidence pack |
| 13 | Instant Payments VoP release pack | Payment vendors to PSPs | Verification-of-payee evidence blocks bank go-live | Live bank test cases | Go-live accepted | Payment consultants | 15k-40k | Payment specialists | Regulated and trust-heavy | Evidence pack |
| 14 | IBAN/name mismatch payment repair desk | Businesses with legitimate payments blocked by VoP | Payor cannot release payment | Beneficiary evidence and AP approval | Payment released | CFOs | Fee per payment batch | Banks/accountants | Weak: bank process | Payment repair |
| 15 | DSA trader verification payout release | Marketplace sellers with payout holds | Platform trader verification blocks payouts | KYC evidence queue | Payout released | Agencies | Success fee | Marketplace agencies | Similar to prior KYBC, failed | Platform release |
| 16 | DAC7 platform seller tax-info payout release | Sellers with platform payout holds | Missing tax info blocks payout | Platform tax evidence case | Payout released | Seller agencies | Fixed + success | Agencies/accountants | Platform opacity | Platform release |
| 17 | PSP reserve release mandate | Merchants with rolling reserves after termination | Cash held by acquirer | Reserve agreement, reserve ledger | Partial release | Payment consultants | Success fee | Payment lawyers/consultants | Trust/legal risk | Cash recovery |
| 18 | Telecom billing overcharge credit mandate | SMEs overcharged under old telecom contracts | Credits due | Contract/invoice mandate | Credit memo | CFOs | Success fee | Telecom auditors | Incumbents | Recovery |
| 19 | Data-center energy pass-through audit credit | SaaS/hosting tenants | Colo overbills energy/pass-throughs | Contract/meter/invoice queue | Credit memo | CFOs | Success fee | Consultants | Evidence often weak | Recovery |
| 20 | SaaS cloud marketplace remittance recovery | ISVs selling via AWS/Azure/GCP | Private offer payout mismatch | Marketplace reports and support cases | Credit/payment | ISV finance groups | 10-20% success | RevOps consultants | Somewhat niche | Recovery |
| 21 | Ad platform invalid credit recovery | Ecommerce brands overcharged by ads | Invalid/fraudulent spend claims | Ad account logs and cases | Credit | Agencies | Success fee | Agencies/platform opacity | Platform discretion | Recovery |
| 22 | 3PL warehouse overbilling credit mandate | Ecommerce brands | Pick/pack/storage/returns invoice mismatch | Contract, WMS, invoices | Credit memo | Ecommerce CFOs | Success fee | Consultants | Many can copy | Recovery |
| 23 | Carrier accessorial invoice credit mandate | Importers/exporters | Detention/demurrage/accessorial errors | Invoice/BOL/POD queue | Credit | Freight forwarders | Success fee | Freight auditors | Incumbents | Recovery |
| 24 | Pallet deposit return lockbox | Manufacturers/distributors | Pallet pool deposits unreturned | Deposit ledger and customer confirmations | Deposit cash | Logistics CFOs | Success fee | Pallet providers/AP | Prior similar failed | Deposit recovery |
| 25 | Closed-site vendor deposit release | Businesses closing branches | Utility/lease/service deposits unclaimed | Contract/deposit ledger | Deposit cash | Insolvency/accountants | Success fee | Accountants | Prior failed | Deposit recovery |
| 26 | Construction retention release mandate | Subcontractors after defects period | Retention unpaid | Contract/protocol/notice queue | Payment | Subcontractor CFOs | Success fee | Lawyers/claims consultants | Prior failed | Claim |
| 27 | Public grant reimbursement release | SMEs with approved grant costs | Reimbursement held by documentation gap | Grant docs and institution request | Reimbursement | Grant consultants | Fee/success | Grant firms | Prior failed | Claim |
| 28 | Municipal waste settlement release | Contractors with unpaid municipal work | Payment held by missing evidence | Event evidence and invoice queue | Payment | Contractors | Fee | Contractor admin | Prior failed | Evidence rail |
| 29 | FIFA training reward mandate | Clubs owed training rewards | Player transfer payments due | FIFA case | Payment | Clubs | Success | Sports-law firms | Prior failed | Claim |
| 30 | Music neighboring-rights micro-royalty recovery | Small labels/performers | Royalties unclaimed | CMO registration/claim queue | Royalty payment | Music accountants | Success | Royalty admins | Legal/episodic | Claim |
| 31 | App store tax/remittance recovery | Small app publishers | Payout/tax mismatch | Store reports/support case | Credit/payment | Founder groups | Success | RevOps/accountants | Platform discretion | Recovery |
| 32 | Chargeback evidence release for B2B SaaS | SaaS merchants | Stripe disputes/holds | Evidence queue | Cash released | Stripe agencies | Success | Payments consultants | Incumbents | Platform recovery |
| 33 | Hotel OTA commission correction | Hotels | OTA statement errors | OTA claims | Credit | Revenue managers | Success | Existing rev managers | Prior candidate risk | Recovery |
| 34 | Marketplace withheld VAT inventory release | Amazon/EU sellers | Inventory/payout held | VAT/KYC case | Release | Agencies | Fee | Incumbents | Similar prior failed | Platform release |
| 35 | EU public-procurement eForms bid correction desk | Suppliers | Tender submission rejected by eForms mismatch | Live tender docs | Bid accepted | Tender consultants | Fee | Tender firms | Service-like | Bid admin |
| 36 | eDelivery PEPPOL invoice release for EU vendors | Vendors to public sector | Invoice rejected in PEPPOL | Invoice/access point case | Payment | Access points | Fee | Peppol providers | Implementation | Payment release |
| 37 | KSeF public-sector invoice release | Suppliers to Polish public bodies | Invoice/payment stuck | KSeF/UPO/public AP queue | Payment | Public vendors | Fee | Accountants | Could be strong but public payment slow | Payment release |
| 38 | Medical device EUDAMED UDI release | Manufacturers | UDI batch publication blocked | EUDAMED record queue | Batch published | RA consultants | Fee | Prior failed | Regulated/trust-heavy | Evidence |
| 39 | CRA vulnerability reporting readiness | Software vendors | EU buyer asks for CRA reporting evidence | Buyer questionnaire | Buyer accepts | Appsec partners | Fee | Prior failed | Future/consulting | Evidence |
| 40 | NIS2 supplier renewal release | SaaS suppliers | Essential-entity customer asks evidence | Live questionnaire | Renewal moves | Cyber firms | Fee | Prior failed | Evidence pack |

## Finalists And Internal Scores

| Candidate | Internal score | Advance? | Reason |
|---|---:|---|---|
| KSeF invoice payment release desk | 89 | Yes | Live national rollout, current cash blocked, buyer AP acceptance proof, local bilingual wedge, first proof is paid invoice. |
| EAA checkout accessibility procurement pack | 84 | No | Good deadline, but accessibility consultants, tools, and auditors are strong and the artifact is evidence/report-heavy. |
| Instant Payments VoP release pack | 83 | No | Real financial trigger, but regulated-payment trust and bank-vendor incumbents are too strong. |
| Cloud marketplace remittance recovery | 82 | No | Niche cash recovery, but platform discretion and RevOps/accounting copy risk remain high. |
| KSeF public-sector invoice release | 84 | No | Similar trigger, but public payment cycles and procurement admin make cash proof slower. |
| KSeF AP duplicate-payment recovery | 83 | No | Cash recovery is real, but AP-audit incumbents and narrower case volume weaken the wedge. |

## Selected Candidate - 89

### Idea Name

KSeFPay Invoice Acceptance Release Desk

### Exact Buyer

Foreign-owned Polish subsidiaries, CEE suppliers, and Polish B2B vendors selling recurring goods or services to large Polish enterprise buyers where 50,000-500,000 PLN of invoices are unpaid because the buyer's AP team has not accepted, matched, or released the KSeF invoice queue.

Best first buyers:

- foreign-owned entities with Polish VAT/accounting obligations but thin local finance coverage;
- CEE suppliers invoicing Polish large enterprises;
- recurring service, industrial, software, agency, logistics, and maintenance vendors whose month-end cash depends on 5-50 invoice lines;
- sellers already using an accountant or KSeF/ERP provider, but whose problem is cross-party payment acceptance rather than system setup.

### Acute Trigger

The seller has issued or attempted to issue invoices, but cash is stuck because the buyer AP desk rejects, cannot find, cannot match, or will not release payment without clean KSeF references, FA(3) XML/visualization, UPO/official receipt evidence, buyer NIP mapping, PO/GRN/protocol match, correction invoice alignment, or branch/cost-center routing.

This is not "prepare for KSeF." The trigger is "these invoices are not being paid."

### Transferable Control Point

The founder controls a live invoice-release queue under a signed mandate:

- seller authorization to act on the defined invoice batch;
- invoice list with gross value, due dates, buyer entity, buyer AP contact, PO/order/protocol references, KSeF numbers, UPOs, FA(3) XML/visualization, correction references, and bank account confirmation;
- permission to coordinate with the seller's accountant/ERP/KSeF provider, while they remain issuer/accountant of record;
- buyer AP acknowledgement of accepted invoice references or explicit rejection reasons;
- release tracker tying each invoice to buyer acceptance, correction, payment date, and fee attribution.

### 60-Day Signed/Assigned/Prepaid Proof

Within 60 days the founder must obtain:

- 5 signed release mandates covering at least 250,000 PLN of unpaid invoices;
- buyer AP acknowledgement on at least 3 queues;
- at least 20 invoices corrected, matched, accepted, or released;
- at least 100,000 PLN of buyer payments released after intervention;
- at least 20,000 PLN of setup/success fees collected;
- written reasons for every unreleased invoice so invalid cases are excluded from the recovery pool.

### Internal Cap Application

The candidate clears the simulation gate only because the proof is current cash and buyer AP acceptance, not a readiness report. It would be internally capped below 87 if positioned as KSeF implementation, invoice formatting, compliance advice, or generic accounting support. It would also fall below gate if it cannot show that buyers pay for released invoice queues instead of asking existing accountants to handle everything.

### 6-Month POC

Target:

- 20 signed mandates;
- 2,000,000-6,000,000 PLN of candidate invoice value screened;
- 1,000,000-3,000,000 PLN released or accelerated;
- 150,000-400,000 PLN collected fees;
- 5 recurring clients using the desk for a second monthly queue;
- 3 referral sources from accounting firms, KSeF integrators, foreign chambers, or CFO communities;
- gross margin above 70% after contractor bookkeeping/XML review support.

### First Acquisition Mechanism

The first outreach is not to all SMEs. It targets people already seeing payment pain:

1. Polish accounting firms serving foreign-owned clients.
2. KSeF/ERP integrators whose clients blame them for AP delays after implementation.
3. Foreign chambers and CEE business groups.
4. CFO/finance-controller groups at foreign-owned Polish subsidiaries.
5. Direct outbound to suppliers to large Polish buyers using public supplier references and job titles.

Offer:

"If a Polish buyer is holding payment because your KSeF invoice cannot be found, matched, corrected, or accepted, I take the live invoice queue, coordinate with your accountant/ERP provider and buyer AP, and get written acceptance or rejection reasons. Fixed sprint plus success fee on released cash. No tax advice, no accounting-of-record, no KSeF software implementation."

### Economics

Pricing:

- 4,000-12,000 PLN fixed intake/release sprint for a defined invoice queue;
- 1-2% of released invoice value, capped where needed for large queues;
- 2,000-5,000 PLN monthly maintenance for repeat queues after the first success;
- no success fee on invoices where the buyer was already scheduled to pay before intervention unless the release trail shows acceptance after the desk's work.

Cost:

- founder-led coordination, evidence mapping, AP chasing, and release tracker;
- contractor accountant/KSeF operator paid per batch for technical XML/UPO/correction review;
- no software build before repeated queues exist.

Payback:

- buyer recovers fee if one meaningful invoice batch is paid days or weeks earlier;
- for a vendor with 100,000-500,000 PLN stuck, a 6,000-15,000 PLN fee is credible if it releases payroll, VAT, supplier payments, or month-end cash.

### Copy Risk

High but not fatal:

- accountants can fix invoice errors;
- ERP/KSeF vendors can troubleshoot submissions;
- AP automation tools can improve matching;
- CFOs can chase buyers themselves.

The narrow defense is that none of these parties naturally owns the cross-party payment release queue. Accountants often stop at issuance, ERP vendors stop at technical submission, and buyer AP teams stop at rejection codes. The founder's controlled asset is the queue-level release history: buyer-specific AP requirements, accepted correction patterns, KSeF reference mapping, and paid-invoice attribution.

### Why Incumbents Cannot Copy Before Control

They can copy the concept, but not the specific live queue already mandated:

- the seller's signed mandate and sensitive invoice list are case-specific;
- buyer AP contacts and acceptance trail are built from the current queue;
- fee attribution ties to invoice-level release events;
- each accepted queue improves buyer-specific pattern memory;
- accounting/ERP firms may prefer referral fees because they avoid open-ended AP chasing and buyer conflict.

### Why It Is Not A Service, Report, App, Dashboard, Database, Marketplace, Or Generic Broker

It does not sell KSeF readiness, templates, software, dashboards, invoice archiving, tax opinions, or introductions. The commercial unit is a defined unpaid invoice queue. The proof artifact is buyer AP acceptance plus released payment, with invalid/rejected invoices documented and removed.

### Boundaries And Legal/Provider Limits

- The startup does not issue invoices as the seller.
- The startup does not become accounting, tax, legal, payment, or collection provider of record.
- The seller's accountant/ERP/KSeF provider remains responsible for invoice issuance, tax treatment, corrections, and statutory records.
- The buyer decides whether to accept, reject, or pay.
- Disputed commercial claims, debt collection, litigation, tax interpretation, sanctions/KYC issues, and insolvency cases are excluded or routed to licensed advisors.
- The desk only handles operational release of invoices that the seller states are valid and due.

### Duplicate-Risk Distinction

This is distinct from TraceFaktura because it is not a municipal all-event evidence rail. It is also distinct from generic AP audit/recovery because the trigger is Poland's mandatory KSeF acceptance/matching transition and the proof is buyer AP acceptance plus paid invoices. It is not DORA, CBAM, Data Act, REDBlocked, GreenTender, or PromoLeak because the payment event, artifact, buyer trigger, and control point are different.

### Strongest Anticipated Objections

1. Accountants, ERP providers, and KSeF integrators may already solve most cases.
2. Many payment delays may be ordinary buyer cash management disguised as KSeF friction.
3. The founder may not be trusted with sensitive invoices, bank details, and buyer contacts.
4. Buyer AP teams may ignore an outside coordinator.
5. The recoverable fee pool may be too small if invoices are delayed only a few days.
6. The work can become messy, manual, and low-status AP chasing.
7. Invalid invoices, missing POs, tax mistakes, and commercial disputes must be excluded.
8. If 2026 adaptation stabilizes quickly, the window may shrink.
9. A part-time solo founder may struggle to handle urgent month-end queues.
10. Repeatability depends on whether the same buyers and invoice errors recur.

## Decision

Advance KSeFPay Invoice Acceptance Release Desk to real Zero To One validation. It passes the simulation gate at 89 because it is local, immediate, cash-linked, and controlled by a signed invoice-release queue with buyer AP acceptance and paid-invoice proof.
