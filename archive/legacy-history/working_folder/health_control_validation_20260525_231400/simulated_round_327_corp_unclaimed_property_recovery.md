# Simulated Round 327: Corporate Unclaimed Property Recovery Mandate

Date: 2026-05-31 Europe/Warsaw

## Search Frame

Round 326 failed because a statutory release trigger still relied on incumbent reverse-logistics channels and did not control cash. This round returns to literal found money: public unclaimed-property records where a specific company is named before outreach. The wedge is not "audit your books"; it is "this named government-held property appears to belong to your company, sign a lawful mandate and claim it."

References checked:

- NAUPA explains that official state programs hold and administer unclaimed property, searching/claiming through official programs is free, and third-party finder services are in most cases legal: https://unclaimed.org/can-i-really-search-for-free/
- NAUPA directs claimants to official state programs and notes owners should check states where they have lived or done business: https://unclaimed.org/contact-us-finding-your-unclaimed-property/
- California's State Controller describes investigators/asset locators and states a 10% fee cap for California property: https://www.sco.ca.gov/upd_investigators.html
- New York's official service says unclaimed funds include old accounts, checks, stocks and bonds, and that there is no fee or time limit to claim them: https://www.osc.ny.gov/ouf/index.htm

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day signed/titled/assigned/prepaid proof | Acquisition | Economics | Copy risk | Internal score |
|---:|---|---|---|---|---|---|---|---|---:|
| 1 | Corporate unclaimed-property recovery mandate | CEE corporates named in US/Canada state records | public cash asset already listed | claim-specific finder/authorization package | signed mandate, claim ID, state acknowledgement, first payout | scrape official databases, named outbound | 10-20% success fee, high margin | asset locators | 88.2 |
| 2 | Bankruptcy unclaimed-funds corporate recovery | CEE creditors named in US court unclaimed funds | court-held distribution | claim authorization and court filing package | signed claim, court docket acknowledgement | court lists | high ticket but legal filing | lawyers | 79 |
| 3 | Class-action corporate settlement claim mandate | companies eligible for settlement proceeds | deadline and recoverable settlement | claim package | submitted claim and administrator acceptance | settlement lists | success fee | claim filing firms | 72 |
| 4 | Dormant transfer-agent dividend/share claim | foreign corporate shareholders | old stock/dividend proceeds | transfer-agent claim authority | claim packet accepted | transfer-agent lists | high ticket | asset reunification firms | 76 |
| 5 | Delaware abandoned securities claim sprint | European corporate owners | state-held securities/cash | state claim mandate | claim accepted | Delaware records | fee cap, longer cycle | specialists | 80 |
| 6 | Canadian unclaimed bank balance recovery | Polish companies with old Canadian accounts | dormant account listed | claim authority | Bank of Canada claim receipt | public search | lower volume | finders | 71 |
| 7 | UK dormant asset company claim | CEE entities with UK balances | dormant asset records | claim authority | claim filed | UK searches | opaque search | banks | 62 |
| 8 | Utility deposit refund mandate | closed CEE branches | old supplier deposits | supplier account authority | refund ticket | company closures | small line values | accountants | prior failed |
| 9 | Insurance premium return recovery | companies with cancelled policies | unreturned premium | broker/insurer claim authority | credit memo | policy exports | broker incumbents | prior failed |
| 10 | Merchant processor reserve maturity release | ecommerce merchants | matured reserve | processor case | payout | statements | platform opaque | prior failed |
| 11 | Amazon Vendor Central recovery | vendors | deductions | portal dispute mandate | credit memo | seller agencies | incumbents | prior tested |
| 12 | Retail OTIF chargeback recovery | CPG vendors | deductions | retailer portal access | reversal | agencies | close to PromoLeak | prior failed |
| 13 | 3PL overbilling credit recovery | ecommerce brands | invoice mismatch | WMS/invoice mandate | credit memo | finance teams | consultants copy | prior failed |
| 14 | COD courier remittance recovery | ecommerce sellers | missing COD cash | carrier claim mandate | remittance credit | seller data | small/declining | prior failed |
| 15 | Freight accessorial credit recovery | importers | billed accessorials | carrier claim mandate | credit | invoice data | audit incumbents | 75 |
| 16 | Port demurrage refund sprint | importers | waived/incorrect demurrage | terminal/forwarder claim | credit | customs brokers | brokers own | 70 |
| 17 | Card chargeback representment for B2B | merchants | chargebacks | processor evidence | win | statements | crowded | 66 |
| 18 | Google/Meta ad overbilling refund | agencies | duplicate/tax charges | ad account cases | refund | account exports | agencies own | 64 |
| 19 | Cloud RI resale recovery | AWS users | unused standard reserved instances | marketplace seller listing | sale proceeds | FinOps exports | narrow/declining | 72 |
| 20 | SaaS marketplace payout hold release | app vendors | payout hold | support case mandate | payout | partner forums | platform opaque | 68 |
| 21 | Royalty black-box recovery | music labels | unmatched royalties | CMO claim authority | payout | catalogue search | specialized | 74 |
| 22 | Patent maintenance fee refund recovery | IP owners | duplicate/overpaid fees | office/refund claim | refund | IP invoices | agents own | 58 |
| 23 | Customs duty drawback mandate | exporters/importers | returned/exported goods | broker claim | refund | invoice/customs data | licensed brokers | 69 |
| 24 | VAT split-payment surplus release | Polish SMEs | VAT account cash trapped | tax application | tax-office decision | accountants | tax advice | 63 |
| 25 | Road toll overpayment refund | fleets | misclassified tolls | operator claim | credit | toll exports | prior branch | 70 |
| 26 | Public grant retained payment release | NGOs/SMEs | approved but unpaid tranche | authority response | payout | grant portals | consultants | 67 |
| 27 | Supplier rebate accrual release | distributors | earned rebates unpaid | vendor claim | credit | ERP extracts | supplier/accountant copy | prior failed |
| 28 | OEM core credit recovery | repair networks | uncredited cores | supplier claim | credit | AP data | fresh failed | prior failed |
| 29 | Lease security deposit release | commercial tenants | expired lease | landlord claim | refund | lease data | lawyers/property managers | prior failed |
| 30 | Corporate gift-card breakage recovery | companies | unused stored value | issuer claim | credit | AP/travel data | tiny lines | 52 |
| 31 | Telecom inactive balance refund | closed sites | old prepaid balances | carrier claim | credit | invoices | small | 55 |
| 32 | Court registry deposit recovery | corporates | old case deposit | court claim | court order | court records | legal process | 66 |
| 33 | Insolvency administrator distribution claim | suppliers | distribution notices | claim proof | accepted claim | insolvency bulletins | legal/slow | 65 |
| 34 | Environmental deposit refund | importers | product deposit balances | authority claim | refund | compliance records | legal/small | 58 |
| 35 | Exchange fee/tax reclaim for ADR holders | investors/corporates | withholding/refund | custodian claim | refund | securities records | tax/custody | 60 |
| 36 | Domain/registrar prepaid credit recovery | agencies | old accounts | registrar claim | credit | account lists | tiny | 45 |

## Finalists

| Finalist | Why it advanced | Why it was rejected or kept |
|---|---|---|
| Corporate unclaimed-property recovery mandate | Pre-identifiable public cash asset, neutral state payer, signed claim mandate, no need to manufacture source truth. | Kept. Needs strict corporate-only, high-value-only, lawful-finder-contract-only boundaries. |
| Bankruptcy unclaimed-funds corporate recovery | Similar public cash asset with named creditor. | Rejected because court filings and legal-practice boundaries are heavier. |
| Dormant transfer-agent dividend/share claim | Potentially high value and successor-entity evidence is hard. | Rejected because issuer/transfer-agent workflows and medallion/guarantee requirements are too specialized. |
| Cloud RI resale recovery | Cash recovery from stranded prepaid asset. | Rejected because standard RI resale is narrow/declining and FinOps incumbents own the account data. |
| Royalty black-box recovery | Public/rightsholder matching can reveal money before outreach. | Rejected because music rights expertise, catalog metadata, and CMO processes are too specialist. |

## Selected Candidate

**Idea name:** ClaimFoundry Corporate Unclaimed-Property Recovery Mandate

**Internal simulated score:** 88.2 / 100

## Thesis

A Warsaw solo founder systematically searches official US and Canadian unclaimed-property programs for Polish and CEE corporate legal names, identifies claim records above a strict minimum expected value, signs a lawful claim-specific finder/authorization agreement with the apparent owner, prepares the owner evidence package, tracks state claim IDs, and invoices only after the government or holder pays the company or issues a written payable/approval.

## Why It Clears Simulation

- The founder can find the specific asset before outreach. That lowers CAC and changes the sales motion from speculative consulting to "we found a named claim."
- The payer is usually a state unclaimed-property office or official holder, not a buyer with an economic reason to resist.
- The control point is claim-specific: signed mandate, owner authorization, claim number, state acknowledgement, evidence checklist, and success-fee contract.
- The first proof is not a report: it is a filed claim, state claim ID, approved/payable status, or recovered government payment.
- It can be run part-time if the first wedge is corporate entities only, high listed value only, and no consumer/heir/deceased-estate work.
- It avoids health, tax-advice, litigation, patient data, marketplace, and generic dashboard risk.

## Hard Boundaries

- No individuals, heirs, deceased estates, consumer claims, probate, or family-tracing cases.
- No upfront fee and no custody of recovered funds.
- Company is paid directly by the state/holder; the startup invoices after recovered payment or written payable status.
- Accept only jurisdictions/property types where third-party finder contracts are lawful, with fee limits respected.
- Use a lawyer-reviewed template before first paid contract; if a state requires special investigator forms, registration, notarization, disclosure, or fee caps, comply or reject.
- Reject claims that require legal representation, contested successor ownership, litigation, tax advice, securities transfer advice, or a medallion-signature guarantee process outside an approved provider route.
- Minimum target: public listing or state response implying at least USD 25,000 equivalent expected value, or a bundle of related properties from one company above that threshold.

## 60-Day Proof

- Search 30-50 official state/province programs and MissingMoney/NAUPA-linked sources for 1,000+ Polish/CEE corporate legal names, former names, branches, acquisitions, and English variants.
- Build 40-80 candidate corporate property records with source state, owner name, address/entity match, holder type, property type, and listed range where available.
- Contact 120 CFOs/controllers/general counsels/founders with claim-specific evidence.
- Sign 4-6 claim-specific mandates covering at least USD 200,000 equivalent of listed or expected claim value.
- Submit at least 3 claim packages and obtain at least 2 official claim IDs, acknowledgements, requests for documents, approved/payable statuses, or written no-go decisions.
- Recover or get payable approval for at least one claim, even if small; otherwise continue only if official acknowledgement and document-request conversion is very high.
- Collect the first success fee or signed payable-trigger invoice.

## 6-Month POC

- 25-40 signed corporate mandates.
- USD 1.5-4.0M equivalent in listed/expected claim value under signed mandate.
- 15-25 claims submitted.
- 8-15 official acknowledgements, payable approvals, recovered payments, or clean no-go decisions.
- USD 250,000-900,000 recovered or approved/payable.
- 120,000-500,000 PLN fees invoiced/collected.
- Gross margin above 70% after legal-template review, notary/document costs, entity-record pulls, and contractor research.
- Repeatable state-by-state playbook for acceptable contracts, document packs, company-name/entity-matching, successor evidence, notarization, apostille/translation needs, and claim-status follow-up.

## Economics

Fee model:

- No search fee for the first wedge.
- 10% where state law caps or market norms require it.
- 15-20% only in jurisdictions/property types where lawful and commercially acceptable.
- Minimum success fee: 8,000 PLN equivalent per submitted claim unless bundled.
- Optional fixed document-rebuild fee only after trust is established, credited against success fee.

Costs:

- 5,000-15,000 PLN legal-template and jurisdiction checklist.
- 2,000-8,000 PLN company registry pulls, translations, notarization, apostille, courier, and document retrieval.
- Contractor research for search/name matching and claim status follow-up.

Payback logic:

- A single USD 50,000 recovered claim at 10% yields roughly 20,000 PLN.
- CAC can stay low because outreach is claim-specific and value-led.
- Owner earnings depend on rejecting low-value properties, slow legal-successor cases, and all consumer/heir work.

## Copy Risk

Asset locators, unclaimed-property investigators, law firms, accountants, and corporate-recovery firms can copy the general service. The defensible wedge is pre-identifying cross-border corporate claims others ignore, signing claim-specific mandates before disclosure beyond a partial teaser, and building state-by-state CEE corporate evidence memory. This is a narrow operational advantage, not a software moat.

## Why Incumbents Cannot Copy Before Control

For a specific claim, once the startup has shown a partial record, signed the finder/authorization agreement, prepared the evidence checklist, filed the claim, and obtained a state claim ID or acknowledgement, a later asset locator cannot control that same claim without displacing an already-filed owner authorization. The moat is claim-by-claim speed and precision, not exclusivity over the entire market.

## Why It Is Not a Service, Report, App, Dashboard, Database, Marketplace, or Generic Broker

The startup does not sell an unclaimed-property search report or database access. It accepts only named public property records where a corporation appears to be the owner, signs a claim-specific recovery mandate, prepares the official owner evidence file, submits or coordinates the claim, tracks the state response, and gets paid from actual recovered or approved government-held funds.

## Duplicate-Risk Distinction

This is not PromoLeak, Amazon Vendor Central, retail chargeback, 3PL, OTA, courier COD, OEM core credit, utility deposit, DRS settlement, KSeF, LC discrepancy, PV compensation, DORA, REDBlocked, BioSignal, HeritageDoor, TraceFaktura, CBAM, Data Act, GreenTender, Supplement Stack, HeatQuiet, BatteryFit, or EUDR. The buyer trigger is a pre-identified public government-held property record. The control point is a claim-specific finder/authorization file and official claim ID. The payment event is government/holder return of unclaimed property to the corporate owner.

## Strongest Objections

1. Owners can claim directly for free, and official programs warn claimants that no paid finder is required.
2. Finder fees are capped or regulated in some states, and contracts may require disclosures, forms, timing rules, or registration.
3. Public records often show incomplete values, stale addresses, old names, merged entities, dissolved subsidiaries, or ambiguous owners.
4. Corporate authority evidence can be painful: name changes, acquisitions, signatory authority, tax IDs, officer certificates, board authority, address proof, and notarized/apostilled documents.
5. Claim processing can take months, so 60-day cash recovery is uncertain.
6. Trust friction is high because unclaimed-property finder mail often looks scammy.
7. Asset locators already exist in the US, and some may have better data, mail infrastructure, and state-specific experience.
8. The market may be one-time and episodic rather than recurring.
9. Many high-value claims may be in the US, reducing the Warsaw founder's local advantage unless CEE corporate-name matching is genuinely under-mined.
10. Success-fee collection depends on enforceable contracts and owner willingness to pay after the state pays them directly.

## Kill Criteria

- Fewer than 4 signed mandates from 120 claim-specific outreaches.
- Fewer than 2 official claim IDs/acknowledgements from the first 6 signed mandates.
- No recovered or payable-approved claim within 90 days and no state response pattern showing near-term cash conversion.
- More than 35% of viable candidate claims require legal succession work, securities transfer guarantees, probate, litigation, or state-specific licensing the founder cannot handle.
- Average expected claim value below USD 25,000 after validation.
- Contract enforceability or finder-fee compliance cannot be made clean in the target states.
