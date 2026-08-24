# Regeneration Wave 2 — Rule-Structure Analyst

Accessed: 2026-08-22  
Agent: `live-w2-rsa-01`

## W2-RSA-01 — Delegated KSeF issuance desk

- **One-sentence transaction:** A Polish SME grants the service provider scoped KSeF authority to issue structured invoices, return accepted KSeF identifiers, and route exceptions to the client or its accountant.
- **Loss bearer:** The SME whose invoice is delayed, rejected, duplicated, or omitted from receivables.
- **Payer:** The invoicing SME or its accounting office.
- **Beneficiary:** Finance staff, the accounting office, and invoice recipients.
- **Authority holder:** The taxpayer; KSeF expressly permits taxpayer-designated persons and entities, including accounting offices.
- **Distributor:** Accounting offices, vertical ERP implementers, franchise networks, and bookkeeping associations.
- **Information holder:** The SME’s ERP, order system, accountant, and KSeF account.
- **Risk bearer:** The taxpayer retains responsibility for invoice correctness; the provider bears contractual responsibility for authorized transmission and evidence handling.
- **Transaction owner:** The taxpayer, with narrowly delegated operational access.
- **First paid event:** Issuance of the first production invoice batch with returned KSeF identifiers and an exception register.
- **Control/compounding asset:** Revocable KSeF authority plus mappings between orders, invoice schemas, identifiers, corrections, and payment reconciliation.
- **Founder-accessible first proof with capital range:** Implement a manual-assisted connector for one accounting office and three of its clients using existing KSeF tooling; **4,000–12,000 PLN**.
- **Buyer economics / substitute:** Direct costs arise from staff re-entry, interrupted collections, and accountant exception work; substitutes are native ERP modules, manual government applications, and accounting-office labor.
- **Evidence atoms:** KSeF can be used by the taxpayer or a taxpayer-designated person/entity, explicitly including an accounting office; mandatory issuance is phased and small-value transitional exceptions remain through 2026. **Q01/S01**, [official KSeF scope](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/), accessed 2026-08-22.
- **Decision-critical unknowns:** Availability and pricing of adequate ERP integrations; willingness of accounting offices to delegate credentials; liability allocation for source-data errors; support load around corrections and outages.
- **Constraint class:** Delegated system right and government-accepted transaction record.
- **Lawful structure:** Written processing agreement, least-privilege KSeF authorization, client-approved invoicing rules, immutable transmission log, and immediate revocation procedure.
- **Prohibited reliance:** Holding oneself out as the taxpayer, determining VAT treatment, concealing rejected invoices, sharing credentials outside the mandate, or treating a KSeF identifier as proof that the underlying sale is lawful.

## W2-RSA-02 — EUDR primary-operator declaration desk

- **One-sentence transaction:** An in-scope timber, wood-product, coffee, cocoa, cattle, rubber, soy, or palm operator mandates a service desk to assemble lot evidence and submit the applicable due-diligence or simplified declaration under the operator’s authority.
- **Loss bearer:** The operator whose goods cannot lawfully proceed because required evidence or a declaration reference is absent.
- **Payer:** Primary operators, importers, or first placers still subject to submission duties under the amended regime.
- **Beneficiary:** The operator, its buyers, customs intermediaries, and downstream customers needing usable reference data.
- **Authority holder:** The regulated operator; any representative acts only within an express mandate while the operator retains substantive responsibility.
- **Distributor:** Sawmills, timber-accounting firms, customs brokers, commodity cooperatives, and traceability vendors.
- **Information holder:** Producers, landowners, suppliers, customs agents, and the operator’s procurement team.
- **Risk bearer:** The operator bears regulatory and commodity-origin risk; the provider bears contractual custody and submission-process risk.
- **Transaction owner:** The operator placing or exporting the relevant product.
- **First paid event:** Submission of the first client-approved declaration and delivery of its registry reference with a source-evidence bundle.
- **Control/compounding asset:** Reusable plot, supplier, commodity-code, document-provenance, and lot-lineage records.
- **Founder-accessible first proof with capital range:** Assemble one declaration-ready evidence bundle for a Polish timber or furniture supply chain using customer-supplied records and a specialist’s scope confirmation; **8,000–20,000 PLN**.
- **Buyer economics / substitute:** The buyer avoids repeated supplier chasing, shipment holds, and manual lot reconstruction; substitutes are spreadsheets, broker services, enterprise traceability platforms, and internal compliance staff.
- **Evidence atoms:** The 2026 amendment removes submission duties from downstream operators and traders and introduces a simplified declaration route for micro or small primary operators, concentrating the opportunity on actors that retain a filing event. **Q02/S02**, [Commission Implementing Regulation (EU) 2026/1565](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601565), accessed 2026-08-22.
- **Decision-critical unknowns:** Exact client status after the 2026 amendments; commodity and customs-code coverage; data quality at plot level; representative permissions in the live information system; seasonality of declaration volume.
- **Constraint class:** Eligibility-dependent filing right and accepted registry reference.
- **Lawful structure:** Client or counsel fixes applicability; the provider performs evidence administration and authorized submission; every assertion retains provenance and client approval.
- **Prohibited reliance:** Declaring goods deforestation-free without evidence, inventing coordinates, treating downstream buyers as filers when the amended rule relieves them, or impersonating a competent authority.

## W2-RSA-03 — Reserved CBAM declarant capacity

- **One-sentence transaction:** A Polish importer reserves recurring declaration capacity from an authorized indirect customs representative, with the entrant operating the emissions-data workflow and handoff under a three-party contract.
- **Loss bearer:** The importer facing blocked imports, customs disruption, certificate expense, or unsupported embedded-emissions data.
- **Payer:** Importers of covered cement, iron and steel, aluminium, fertilisers, electricity, or hydrogen.
- **Beneficiary:** The importer, customs representative, procurement team, and non-EU supplier.
- **Authority holder:** The authorized CBAM declarant—either the importer or an eligible indirect customs representative.
- **Distributor:** Customs agencies, freight forwarders, trade-finance advisers, chambers of commerce, and metal or fertiliser distributors.
- **Information holder:** Non-EU producers, importers, customs agents, verifiers, and procurement systems.
- **Risk bearer:** The authorized declarant bears declaration duties; the importer bears commercial exposure; the entrant bears contracted data-workflow risk.
- **Transaction owner:** The authorized CBAM declarant.
- **First paid event:** A capacity reservation covering a defined importer and the first covered import, followed by an accepted registry entry.
- **Control/compounding asset:** Contracted declarant capacity, supplier-installation emissions histories, CN-code mappings, and certificate-liability forecasts.
- **Founder-accessible first proof with capital range:** Secure one customs-agency capacity agreement and prepare a supplier-data pack for one Polish importer; **12,000–30,000 PLN**.
- **Buyer economics / substitute:** The importer’s direct exposures include customs continuity, purchased certificates, supplier-data labor, and representative fees; substitutes are self-authorization, customs agencies, consultants, and large trade-compliance suites.
- **Evidence atoms:** The definitive regime applies from 1 January 2026 and imposes authorization, reporting, and certificate purchase/surrender obligations; it covers six named carbon-intensive sectors. **Q03/S03**, [European Commission CBAM portal](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en), accessed 2026-08-22.
- **Decision-critical unknowns:** Customs representatives’ appetite for reserved capacity; collateral and liability requirements; importer volumes above applicable thresholds; verifier availability; quality of producer emissions data.
- **Constraint class:** Authorized declarant status and contracted transaction capacity.
- **Lawful structure:** The authorized declarant owns submissions; the entrant supplies traceable data operations; contracts allocate approval, certificate funding, corrections, and audit access.
- **Prohibited reliance:** Acting as a customs representative without authority, fabricating producer emissions, guaranteeing certificate prices, or describing a registry submission as verification.

## W2-RSA-04 — Stationary-battery passport custodian

- **One-sentence transaction:** A battery importer or manufacturer authorizes a passport custodian to create and maintain the electronic record for each qualifying industrial battery installed by renewable-energy contractors.
- **Loss bearer:** The economic operator unable to demonstrate an accurate, current passport for a battery it places on the market.
- **Payer:** Battery importers, private-label distributors, manufacturers, or energy-storage integrators.
- **Beneficiary:** The payer, installer, asset owner, repairer, second-life operator, and recycler.
- **Authority holder:** The economic operator placing the battery on the market; an authorized data operator may store or process passport data on its behalf.
- **Distributor:** Battery distributors, energy-storage installers, renewable wholesalers, and the founder’s family-access installation firm.
- **Information holder:** Manufacturer, importer, installer, battery-management system, owner, repairer, and recycler.
- **Risk bearer:** The placing operator remains responsible for passport accuracy; the custodian bears contractual availability, integrity, and access-control risk.
- **Transaction owner:** The economic operator placing the battery on the market.
- **First paid event:** Creation and handover of the first live passport at commissioning of a qualifying battery.
- **Control/compounding asset:** Persistent custody mandate, unique battery identities, commissioning history, service events, ownership handoffs, and second-life records.
- **Founder-accessible first proof with capital range:** Use the family-access installer to map one distributor-to-installation data chain and publish passports for a small stationary-battery batch; **6,000–18,000 PLN**.
- **Buyer economics / substitute:** The payer avoids per-installation evidence chasing and later reconstruction for warranty, resale, or recycling; substitutes are OEM portals, spreadsheets, QR-document links, and horizontal DPP vendors.
- **Evidence atoms:** From 18 February 2027, every industrial battery above 2 kWh, every EV battery, and every LMT battery placed on the market or put into service must have a battery passport; covered operators also face long-lived documentation and periodic verification duties. **Q04/S04**, [consolidated Batteries Regulation](https://eur-lex.europa.eu/eli/reg/2023/1542/2025-07-31/eng/), accessed 2026-08-22.
- **Decision-critical unknowns:** Final interoperability rules; OEM willingness to expose BMS data; who pays across importer, distributor, and installer; identifier standards; liability for post-sale updates.
- **Constraint class:** Mandatory persistent electronic record with restricted update rights.
- **Lawful structure:** Passport responsibility stays with the economic operator; the custodian receives explicit storage and update permissions, limits secondary data use, and provides export and continuity rights.
- **Prohibited reliance:** Claiming notified-body status, altering manufacturer data without provenance, selling protected passport data, or presenting a passport as proof of full product conformity.

## W2-RSA-05 — Certified-installer acceptance at heat-pump checkout

- **One-sentence transaction:** A seller of non-hermetically sealed F-gas equipment pays for a checkout control that binds each sale to an accepting certified installer and retains the required evidence.
- **Loss bearer:** The equipment seller unable to identify the certified undertaking that will install the sold equipment.
- **Payer:** Heat-pump, refrigeration, and air-conditioning wholesalers or online sellers.
- **Beneficiary:** Seller, certified installer, purchaser, equipment operator, and regulator.
- **Authority holder:** The seller owns the sales record; the certified undertaking owns its certification and installation acceptance.
- **Distributor:** HVAC wholesalers, e-commerce platforms, manufacturer dealer networks, and certified installation firms.
- **Information holder:** Seller, buyer, equipment distributor, certification holder, and installer.
- **Risk bearer:** The seller bears sales-record duties; the installer bears certified-work duties; the service bears identity-matching and evidence-retention risk.
- **Transaction owner:** The equipment seller.
- **First paid event:** A completed equipment order paired with a verified installer acceptance and archived record.
- **Control/compounding asset:** A permissioned directory of certification holders, installer acceptance records, equipment-sale links, and repeat seller integrations.
- **Founder-accessible first proof with capital range:** Integrate a manual acceptance link into one regional seller’s checkout and recruit certified installers through the family-access renewable firm; **8,000–25,000 PLN**.
- **Buyer economics / substitute:** Sellers otherwise incur manual certificate collection, abandoned orders, and five-year record administration; substitutes are email attachments, declaration checkboxes, internal call-centre verification, and distributor portals.
- **Evidence atoms:** Sellers of specified non-hermetically sealed equipment must retain records of the equipment sold and the certified undertaking that will install it for at least five years; suppliers also retain certificate-linked purchaser records. **Q05/S05**, [F-gas Regulation](https://eur-lex.europa.eu/eli/reg/2024/573/2024-02-20/eng), accessed 2026-08-22.
- **Decision-critical unknowns:** Polish certificate-registry access; seller interpretation of acceptable evidence; chargeback responsibility when installers withdraw; equipment categories in scope; installer acquisition cost.
- **Constraint class:** Certification-gated transaction acceptance and five-year evidence duty.
- **Lawful structure:** Verify certification from an authoritative source where available, capture explicit installer acceptance, preserve timestamps, and leave technical installation decisions to certified parties.
- **Prohibited reliance:** Treating a buyer checkbox as certification, dispatching unqualified labor, falsifying certificate numbers, or performing regulated F-gas work without certification.

## W2-RSA-06 — Construction-product passport continuity escrow

- **One-sentence transaction:** A small construction-product manufacturer contracts a passport custodian to host each product passport, preserve update rights, and guarantee an exportable continuity copy after the product leaves active sale.
- **Loss bearer:** The manufacturer whose declaration, technical documentation, or product identity becomes unavailable to clients or authorities.
- **Payer:** Manufacturers and private-label importers of construction products.
- **Beneficiary:** Manufacturer, distributor, contractor, designer, building owner, reuse operator, and market-surveillance authority.
- **Authority holder:** The economic operator responsible for the product passport.
- **Distributor:** Testing laboratories, certification bodies, construction wholesalers, BIM consultancies, and manufacturing associations.
- **Information holder:** Manufacturer, laboratory, notified or technical bodies, importer, and product-information management system.
- **Risk bearer:** The manufacturer remains responsible for accuracy; the custodian bears contracted persistence, access-control, and export risk.
- **Transaction owner:** The manufacturer or other passport-responsible economic operator.
- **First paid event:** Publication and escrow of the first product-family passport and its signed continuity export.
- **Control/compounding asset:** Long-duration hosting mandate, product-type identifiers, documentation lineage, client access history, and links between superseded versions.
- **Founder-accessible first proof with capital range:** Convert one Polish manufacturer’s existing declaration and technical pack into a passport-shaped record with role-based access and an independent backup; **10,000–28,000 PLN**.
- **Buyer economics / substitute:** The buyer exchanges recurring document-request labor and migration risk for durable availability; substitutes are document-management systems, manufacturer websites, BIM libraries, and general DPP platforms.
- **Evidence atoms:** The construction DPP system must support restricted update rights, data integrity, and availability for 25 years after the last product of a type is placed on the market, while the economic operator must make its passport available for at least ten years. **Q06/S06**, [Construction Products Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R3110), accessed 2026-08-22. ESPR also expressly contemplates DPP service providers and restricts their reuse of hosted data. **Q10/S10**, [Ecodesign for Sustainable Products Regulation](https://eur-lex.europa.eu/eli/reg/2024/1781/2024-06-28/eng), accessed 2026-08-22.
- **Decision-critical unknowns:** Product-family implementation calendar; custodian certification requirements; acceptable business-continuity guarantees; storage liability; willingness to pay before product-specific specifications apply.
- **Constraint class:** Mandatory source-of-truth continuity and restricted update authority.
- **Lawful structure:** Data-processing and continuity agreement, named update roles, immutable version lineage, routine export, and no secondary use absent specific consent.
- **Prohibited reliance:** Claiming the passport proves conformity, issuing technical declarations for the manufacturer, suppressing superseded versions, or locking the payer out of its records.

## W2-RSA-07 — KSC registry and incident-evidence operator

- **One-sentence transaction:** A Polish entity already classified by itself or counsel as important or essential authorizes an operator to prepare its KSC registry entry, maintain S46 contact data, and assemble incident evidence for client-approved submission.
- **Loss bearer:** The regulated entity and its management when registration, contact, or incident-reporting duties are missed.
- **Payer:** Medium-sized entities in covered sectors, especially those without a dedicated governance team.
- **Beneficiary:** Management, security staff, legal counsel, CSIRT counterparties, and customers dependent on service continuity.
- **Authority holder:** The entity’s manager or duly authorized person.
- **Distributor:** Regional MSPs, cyber insurers, sector associations, law firms, and IT auditors.
- **Information holder:** Management, IT operations, security tools, vendors, HR, and legal counsel.
- **Risk bearer:** The entity retains statutory responsibility; the operator bears contracted custody, workflow, and deadline-notification risk.
- **Transaction owner:** The regulated entity.
- **First paid event:** Submission of the entity-approved KSC registry dossier and delivery of an evidence receipt.
- **Control/compounding asset:** Authorized registry workflow, current service and contact map, incident chronology schema, and recurring evidence feeds from vendors.
- **Founder-accessible first proof with capital range:** Work with one MSP and one already-classified entity to assemble its registry dataset and S46 operating procedure; **8,000–20,000 PLN**.
- **Buyer economics / substitute:** The buyer avoids management time spent assembling scattered evidence and coordinating multiple vendors; substitutes are internal security teams, law firms, MSSPs, and governance platforms.
- **Evidence atoms:** Poland’s amended KSC regime requires important and essential entities to enter the KSC register and implement an information-security management system; entities meeting the criteria at commencement had a 3 October 2026 registration date. **Q07/S07**, [Polish Ministry of Digital Affairs](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych), accessed 2026-08-22.
- **Decision-critical unknowns:** Delegated S46 access model; sector-specific supervisory practice; which entities were entered ex officio; professional-liability coverage; required availability outside the founder’s working hours.
- **Constraint class:** Statutory registry, delegated filing authority, and recurring incident evidence.
- **Lawful structure:** Applicability is fixed by the client or qualified counsel; the operator handles authorized administration, preserves evidence, and requires client approval for every filing.
- **Prohibited reliance:** Giving unauthorized legal conclusions on scope, suppressing incidents, altering timestamps, submitting without authority, or marketing as a government-approved certifier.

## W2-RSA-08 — High-risk AI deployer log escrow

- **One-sentence transaction:** A deployer of a client-classified high-risk AI system contracts a neutral custodian to retain system-generated logs, human-oversight records, and provider instructions in an access-controlled evidence vault.
- **Loss bearer:** The deployer unable to reconstruct how a consequential AI-supported decision was produced or supervised.
- **Payer:** Employers, recruitment providers, education operators, lenders, insurers, or healthcare organizations deploying covered systems.
- **Beneficiary:** The deployer, affected-person response team, internal audit, data-protection staff, and competent authorities.
- **Authority holder:** The deployer controls logs under its authority; the provider controls logs and documentation remaining on the provider side.
- **Distributor:** AI vendors, DPO consultancies, employment-law firms, sector software integrators, and insurers.
- **Information holder:** AI provider, deployer, identity system, human reviewer, case-management system, and data-protection function.
- **Risk bearer:** Provider and deployer retain their respective regulatory duties; the custodian bears contracted integrity, access, and retention risk.
- **Transaction owner:** The deployer for deployment-side evidence.
- **First paid event:** Ingestion and sealing of the first production log period with a documented human-oversight event.
- **Control/compounding asset:** Durable log custody, provider/deployer schema mappings, decision-to-review linkage, and recurring retention events.
- **Founder-accessible first proof with capital range:** Connect one recruitment or eligibility workflow to immutable storage using synthetic and client-approved production metadata; **6,000–18,000 PLN**.
- **Buyer economics / substitute:** Direct costs include engineer time retrieving vendor logs, manual review records, and dispute reconstruction; substitutes are vendor-native logs, SIEM storage, case-management systems, and governance suites.
- **Evidence atoms:** Providers and deployers of high-risk AI systems must retain automatically generated logs under their control for an appropriate period of at least six months, subject to other applicable law. **Q08/S08**, [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), accessed 2026-08-22.
- **Decision-critical unknowns:** Which client systems are legally high-risk; provider API access; lawful retention under privacy and employment rules; evidence admissibility; buyer preference for existing security tooling.
- **Constraint class:** Mandatory recurring retention event and split information control.
- **Lawful structure:** Client or counsel supplies system classification and retention policy; the custodian minimizes personal data, separates tenants, logs access, and supports deletion when other law requires it.
- **Prohibited reliance:** Classifying systems without authority, retaining personal data indefinitely, claiming logs prove fairness or legality, or modifying records to improve an outcome narrative.

## W2-RSA-09 — DORA contract-register steward

- **One-sentence transaction:** A financial entity gives a register steward recurring contractual rights to ingest ICT agreements, map them to functions and subcontractors, and deliver the prescribed register export.
- **Loss bearer:** The financial entity whose management or supervisor cannot see its ICT dependencies, concentration, termination rights, or contractual gaps.
- **Payer:** Small banks, payment institutions, investment firms, insurers, intermediaries, and other covered financial entities.
- **Beneficiary:** Management body, procurement, operational-risk staff, supervisors, and business-continuity owners.
- **Authority holder:** The financial entity; its management body retains responsibility.
- **Distributor:** Financial-sector law firms, IT auditors, core-system integrators, procurement advisers, and industry associations.
- **Information holder:** Procurement, legal, IT owners, group entities, direct ICT vendors, and subcontractors.
- **Risk bearer:** The financial entity retains DORA responsibility; the steward bears contract-data normalization, change-capture, and export risk.
- **Transaction owner:** The financial entity.
- **First paid event:** Ingestion of the first complete ICT contract population and delivery of a regulator-shaped register export.
- **Control/compounding asset:** Contract-level data rights, stable vendor and function identifiers, subcontractor lineage, renewal dates, and recurring change feeds.
- **Founder-accessible first proof with capital range:** Normalize a small regulated firm’s contracts into the official register structure through a law-firm or IT-auditor channel; **7,000–20,000 PLN**.
- **Buyer economics / substitute:** The buyer pays today through legal review, spreadsheet reconciliation, repeated vendor requests, and governance-platform licenses; substitutes are spreadsheets, GRC tools, consultancies, and internal procurement systems.
- **Evidence atoms:** DORA requires financial entities to maintain and update registers covering all contractual arrangements for ICT services, including entity, sub-consolidated, and consolidated levels; it also requires exit planning and consideration of substitutability and concentration. **Q09/S09**, [Digital Operational Resilience Act](https://eur-lex.europa.eu/eli/reg/2022/2554/oj?uri=CELEX%3A32022R2554), accessed 2026-08-22.
- **Decision-critical unknowns:** Data-access friction across group entities; supervisor-specific submission cadence; incumbent GRC coverage; professional-indemnity requirements; contract confidentiality constraints.
- **Constraint class:** Mandatory source-of-truth register, contractual audit rights, and recurring update event.
- **Lawful structure:** The financial entity owns the register; the steward receives specified contract-data rights, maintains provenance to source agreements, and never substitutes for management approval.
- **Prohibited reliance:** Interpreting contracts as counsel, hiding subcontractors, asserting regulatory completeness without client approval, or using confidential vendor terms for cross-client negotiation.

## W2-RSA-10 — CRA authorized-representative evidence vault

- **One-sentence transaction:** A non-EU manufacturer of connected products appoints an EU-established representative under a written CRA mandate, bundled with ten-year conformity-document custody and authority-response operations.
- **Loss bearer:** The manufacturer or importer whose product lacks an accountable EU contact or retrievable conformity documentation.
- **Payer:** Non-EU manufacturers of software-enabled hardware or standalone software entering the EU market.
- **Beneficiary:** Manufacturer, importer, distributor, market-surveillance authority, and product customers.
- **Authority holder:** The manufacturer grants a written mandate; the representative may perform only specified permitted tasks.
- **Distributor:** Importers, test laboratories, notified bodies, cybersecurity consultancies, contract manufacturers, and marketplace onboarding providers.
- **Information holder:** Manufacturer, developers, component suppliers, laboratory, importer, and vulnerability-response team.
- **Risk bearer:** The manufacturer retains non-delegable product duties; the representative bears responsibility for tasks it accepts; the importer carries its own market-access duties.
- **Transaction owner:** The manufacturer for product compliance; the representative for mandate-defined custody and authority cooperation.
- **First paid event:** Acceptance of a signed representation mandate and custody of the first SKU’s declaration and technical-document index.
- **Control/compounding asset:** EU representation title, durable SKU documentation, manufacturer-component relationships, authority correspondence, and renewal rights across later products.
- **Founder-accessible first proof with capital range:** Form the mandate, insurance, secure evidence vault, and authority-response procedure with specialist counsel, then onboard one low-complexity non-EU manufacturer through an importer; **12,000–35,000 PLN**.
- **Buyer economics / substitute:** The manufacturer avoids establishing an EU entity solely for permitted representative functions and centralizes long-term document retrieval; substitutes are importer-held files, compliance consultancies, testing houses, and established authorized-representative firms.
- **Evidence atoms:** The CRA recognizes an EU-established natural or legal person receiving a written manufacturer mandate; permitted representative tasks include keeping the declaration and technical documentation available for at least ten years and cooperating with market-surveillance authorities. Vulnerability and severe-incident reporting duties apply from 11 September 2026, but core manufacturer obligations excluded from the representative’s mandate remain with the manufacturer. **Q12/S12**, [Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng), accessed 2026-08-22.
- **Decision-critical unknowns:** Insurance and personal-liability exposure; which product classes demand notified-body involvement; non-EU acquisition cost; document-quality remediation burden; precise boundary between permitted representative tasks and non-delegable manufacturer duties.
- **Constraint class:** Written representative title, retained chain of documentation, and restricted mandate.
- **Lawful structure:** Counsel-defined written mandate, clear exclusions for non-delegable duties, secure ten-year custody, authority-response procedure, and contractual termination plus successor handoff.
- **Prohibited reliance:** Acting as a notified body, accepting excluded manufacturer obligations, certifying product security, concealing known vulnerabilities, or claiming that representation itself establishes conformity.

# Query ledger

Exactly 12 distinct web queries were executed.

| Query ID | Query |
|---|---|
| Q01 | `site:podatki.gov.pl KSeF 2026 obowiązkowy terminy uprawnienia certyfikat wystawianie faktur` |
| Q02 | `site:eur-lex.europa.eu EUDR Regulation 2023/1115 due diligence statement authorised representative application 2026` |
| Q03 | `site:taxation-customs.ec.europa.eu CBAM 2026 authorised CBAM declarant indirect customs representative 50 tonnes` |
| Q04 | `site:eur-lex.europa.eu Regulation EU 2023/1542 battery passport due diligence economic operator 2027` |
| Q05 | `site:eur-lex.europa.eu Regulation EU 2024/573 fluorinated greenhouse gases certification records service companies leak checks` |
| Q06 | `site:eur-lex.europa.eu Regulation EU 2024/3110 construction products digital product passport economic operator 2026` |
| Q07 | `site:gov.pl Krajowy System Cyberbezpieczeństwa nowelizacja NIS2 ustawa 2026 obowiązki rejestr podmioty ważne kluczowe` |
| Q08 | `site:eur-lex.europa.eu AI Act Regulation 2024/1689 deployers high-risk logs registration 2 August 2026` |
| Q09 | `site:eur-lex.europa.eu DORA Regulation 2022/2554 register of information ICT third-party contractual arrangements financial entities 2025` |
| Q10 | `site:eur-lex.europa.eu ESPR Regulation 2024/1781 digital product passport service provider registry customs unique operator identifier` |
| Q11 | `site:transport.ec.europa.eu eFTI Regulation 2020/1056 2027 authorities accept electronic freight information certified platform provider` |
| Q12 | `site:eur-lex.europa.eu Cyber Resilience Act Regulation 2024/2847 manufacturer vulnerability reporting conformity 2026 2027` |

# Source ledger

Exactly 12 useful sources were opened.

| Source ID | Source | URL | Accessed |
|---|---|---|---|
| S01 | Polish Ministry of Finance — KSeF mandatory scope | https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/ | 2026-08-22 |
| S02 | Commission Implementing Regulation (EU) 2026/1565 — amended EUDR operation | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ%3AL_202601565 | 2026-08-22 |
| S03 | European Commission — Carbon Border Adjustment Mechanism | https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en | 2026-08-22 |
| S04 | Consolidated Regulation (EU) 2023/1542 — batteries and battery passports | https://eur-lex.europa.eu/eli/reg/2023/1542/2025-07-31/eng/ | 2026-08-22 |
| S05 | Regulation (EU) 2024/573 — fluorinated greenhouse gases | https://eur-lex.europa.eu/eli/reg/2024/573/2024-02-20/eng | 2026-08-22 |
| S06 | Regulation (EU) 2024/3110 — construction products | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R3110 | 2026-08-22 |
| S07 | Polish Ministry of Digital Affairs — amended KSC obligations | https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych | 2026-08-22 |
| S08 | Regulation (EU) 2024/1689 — Artificial Intelligence Act | https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng | 2026-08-22 |
| S09 | Regulation (EU) 2022/2554 — DORA | https://eur-lex.europa.eu/eli/reg/2022/2554/oj?uri=CELEX%3A32022R2554 | 2026-08-22 |
| S10 | Regulation (EU) 2024/1781 — ESPR and digital product passports | https://eur-lex.europa.eu/eli/reg/2024/1781/2024-06-28/eng | 2026-08-22 |
| S11 | European Commission — eFTI Regulation | https://transport.ec.europa.eu/transport-themes/logistics-and-multimodal-transport/efti-regulation_en | 2026-08-22 |
| S12 | Regulation (EU) 2024/2847 — Cyber Resilience Act | https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | 2026-08-22 |
