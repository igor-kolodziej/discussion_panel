# W2-L2-004 — Delegated KSeF issuance desk

Research snapshot: **2026-08-22T14:50:45+02:00 (CEST)**  
Scope: delegated issuance of Polish structured invoices; eight distinct queries executed; eight useful sources opened.

## 1. Transaction

A Polish SME grants a service company narrowly scoped KSeF authority. The service company receives client-approved invoice data, converts or maps it to FA(3), performs technical and client-rule checks, transmits it to KSeF, returns the KSeF identifier and UPO, and places rejected or ambiguous documents into an exception register.

The service does **not** decide VAT treatment, establish whether a sale is lawful, or silently change commercial data.

### Operating sequence

1. The taxpayer or accounting office approves the source transaction.
2. An order, ERP export, CSV, or API payload becomes a versioned invoice candidate.
3. The desk checks schema validity, required fields, duplicates, customer-specific rules, and authorization context.
4. It submits the document under delegated `InvoiceWrite` authority.
5. It records the reference number and polls for the final status.
6. On acceptance, it stores the KSeF number, UPO, payload hash, submission time, operator, and source-record link.
7. On rejection, it prevents uncontrolled resubmission and routes a readable exception to the named client or accountant.
8. Corrections require fresh client approval. In offline24, a correction of an offline invoice waits until the original receives its KSeF number.

The Ministry of Finance explicitly allows a taxpayer to authorize an accounting office or another entity, choose the scope, permit further delegation, and later revoke the authority. [KSeF authorization FAQ](https://ksef.podatki.gov.pl/ksef-news/najczestsze-pytania/)

## 2. Verified evidence, interpretation, and unknowns

### Verified

- Delegated entities, including accounting offices, can use KSeF when properly authorized and authenticated. [Mandatory KSeF scope](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/)
- Mandatory issuance began on 1 February 2026 for taxpayers above 200 million PLN of 2024 gross sales and on 1 April 2026 for most remaining taxpayers. Businesses whose monthly invoiced gross sales do not exceed 10,000 PLN can remain outside mandatory issuance through 2026. Receiving through KSeF has been mandatory since 1 February 2026. [Mandatory KSeF scope](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/)
- KSeF supports revocable permissions for accounting offices and, if the taxpayer allows it, downstream delegation to their staff. [KSeF authorization FAQ](https://ksef.podatki.gov.pl/ksef-news/najczestsze-pytania/)
- Offline and outage processing is not merely “retry later.” During a declared outage, submission can be due within seven business days after the outage ends; a total outage has different treatment. Offline corrections can depend on the original invoice first receiving a KSeF number. [Offline24 rules](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/tryb-offline24/)
- The production API exposes authentication, permissions, certificate operations, request limiting, asynchronous references, and retry responses. [Official KSeF API documentation](https://api.ksef.mf.gov.pl/docs/v2/index.html)
- Poland had 2.374 million active non-financial enterprises in 2024; 99.8% were SMEs and 97.2% were microenterprises. [PARP 2026 SME report](https://en.parp.gov.pl/storage/publications/pdf/ROSS_2026___29-04-2026.pdf)
- Native and gateway substitutes can be inexpensive. A January 2026 Comarch price list showed packages from 15 to 600 PLN monthly, depending on system and document volume, with introductory free communication periods. [Comarch KSeF price list, reseller-hosted PDF](https://elte-s.com/wp-content/uploads/2026/01/Cennik_Comarch_KSeF_01.01.2026.pdf)
- One API gateway advertises 100 trial invoices, sub-hour test transmission, production setup in one to two days, corrections, UPOs, webhooks, and 99.5% SLA. These are vendor claims, not independently measured results. [ksef.io](https://ksef.io/)
- A small-business IT seller displays entry prices of 29–219 PLN, while explicitly warning that the displayed prices do not establish license duration or included permissions. [PartsPC cost guide](https://serwis.partspc.pl/blog/ksef-mala-firma-koszt-wdrozenia.php)

### Interpretation

- Pure XML transport is commoditized. The payable product must be the operational desk: source mappings, controlled approval, duplicate protection, returned identifiers, reconciliation, daytime exception handling, and documented responsibility.
- A business already using a well-supported ERP module will generally have little reason to pay 449–999 PLN monthly for transmission alone.
- The strongest initial payer is likely an accounting office or operationally messy SME with several source systems, recurring exceptions, or no internal finance operator.
- Revocable authority improves workflow control but is not durable lock-in. The more persistent asset is the mapping and exception history accumulated around each client.

### Unknown

No selected source quantified:

- Collection delays or staff cost attributable specifically to KSeF rejection and reconciliation.
- The number of firms lacking adequate native ERP support.
- Accounting offices’ willingness to grant entity-level or indirect authority to a specialist.
- Real support hours per client under production conditions.
- Claims frequency, insurability, or customary liability allocation.
- The number and client distribution of Polish accounting offices.
- Independent production reliability for commercial gateways.

## 3. Incentive and power map

| Actor | Controls or supplies | Receives | Incentive and exposure | Practical veto |
|---|---|---|---|---|
| Taxpayer | Authority, source data, invoicing policy, approval | Accepted invoice, KSeF number, evidence | Faster and more reliable issuance; retains exposure to incorrect source and tax data | Can withhold data, approval, or revoke authority |
| Delegated desk | Mapping, validation, transmission, logs, exception queue | Setup and recurring fees | Standardize handling across NIPs; contractual exposure for transmission and security failures | Can reject incomplete or out-of-policy payloads |
| Accounting office | Client relationship, bookkeeping context, sometimes delegated rights | Fewer exceptions and support calls; reseller margin | Wants control without assuming an unclear new liability | Can block distribution or retain the work internally |
| ERP/order-system vendor | Source format and native integration | License and implementation revenue | Can bundle the same transport and status functions | Can make an external desk unnecessary or difficult to integrate |
| Ministry of Finance/KSeF | Authentication, acceptance/rejection, identifier and UPO | Statutory data flow | Enforces system rules; offers no commercial service commitment to the desk | System status and schema determine whether submission succeeds |
| Invoice recipient | Receipt and downstream matching | Structured invoice | Wants correct, timely, reconcilable documents | Can dispute the underlying invoice despite KSeF acceptance |
| Accountant/finance operator | Tax classification and correction decisions | Exception packet and evidence | Avoid re-entry and ambiguity | Must resolve substantive accounting questions |

The taxpayer remains the transaction owner. The desk controls the transmission process only within the granted mandate.

## 4. Payer denominator

The defensible upper bound is the approximately **2.369 million active SMEs** implied by 2.374 million active non-financial enterprises multiplied by the reported 99.8% SME share. This is not a serviceable-customer count.

The usable denominator is:

> In-scope invoice issuers × recurring structured-invoice volume × inadequate native exception handling × willingness to delegate × willingness to pay for managed operations.

Those factors were not quantified by the permitted sources. The scenario volumes below correspond to approximately:

- 220 active NIPs: 0.009% of the SME upper bound.
- 1,000 active NIPs: 0.042%.
- 3,500 active NIPs: 0.148%.

## 5. Pricing, unit economics, and cash timing

### Proposed commercial package

- SME onboarding: **1,500 PLN per NIP**
- Managed issuance: **549 PLN per month per NIP**, including 250 outgoing invoices
- Accounting-office channel: **449 PLN per month per NIP**, with a ten-NIP commitment
- Enhanced workflows or multiple source systems: **999 PLN per month**
- Excess volume: **0.70 PLN per accepted or finally rejected submission**
- Custom ERP mapping: separately quoted

This pricing is for managed responsibility, not API transport. It sits well above low-cost native modules and therefore requires evidence of exception workload or collection risk.

### Standard-client unit model

| Item | PLN/month |
|---|---:|
| Recurring revenue | 519 |
| Gateway, storage, monitoring | 35 |
| Operations: 0.75 hour at 90 PLN | 68 |
| Incident/security reserve | 12 |
| Gross contribution | 404 |
| Gross margin | 78% |

Onboarding at 1,500 PLN is modeled with 700 PLN of mapping, testing, and setup cost, producing 800 PLN of gross contribution. A channel commission of 15% of first-year recurring revenue is approximately 934 PLN. First-year contribution before fixed engineering, sales, and administration is therefore about **4,714 PLN per NIP**.

These are operating assumptions, not observed production costs.

### Cash cycle

- Onboarding is invoiced before production setup.
- Subscription is billed monthly in advance with seven-day terms.
- Gateway, contractor, and support expenditure occurs monthly.
- There is no inventory, but a rejected invoice may delay the client’s receivable without delaying the desk’s own costs.
- Larger accounting offices should post a service deposit or prepay quarterly.
- Retained after-tax cash is included only through balance-sheet cash in the wealth cases; it is not separately added to founder wealth.

## 6. Founder-wealth cases

Common assumptions:

- Values are PLN.
- Revenue includes subscriptions recognized during the stated year plus onboarding for new NIPs.
- Operating expense includes normalized replacement compensation for work that otherwise depends on the founder.
- A 19% effective cash-tax rate is a modeling convention, not tax advice.
- Enterprise values use assumed multiples of exit recurring revenue; no selected source established transaction multiples.
- Founder wealth equals founder ownership of enterprise value plus net cash, less debt, plus distributions actually received.

| Case | Timing and volume | Revenue, margin and operating profit | Capital, ownership and reinvestment | Modeled founder wealth |
|---|---|---|---|---|
| Conservative | Year 5; 180 average and 220 exit NIPs; 70 new setups; 479 PLN blended monthly revenue | 1.14m revenue; 0.80m gross profit at 70%; 0.09m operating profit at 8%; exit ARR 1.265m | 60k founder capital; no debt or dilution; founder remains employed; 95% of after-tax distributable cash retained and optional distributions limited to 5% | 2× ARR = 2.529m enterprise value; 0.15m cash; 0 debt; 100% ownership; 0.02m cumulative distributions: **2.70m** |
| Expected | Year 6; 750 average and 1,000 exit NIPs; 300 new setups; 519 PLN blended monthly revenue | 5.12m revenue; 3.99m gross profit at 78%; 1.13m operating profit at 22%; exit ARR 6.228m | 100k founder capital; 300k revolving debt still outstanding; 10% employee/adviser pool; founder leaves employment after year 3; 95% retained while employed, then 80% retained | 4× ARR = 24.912m enterprise value; 1.2m cash less 0.3m debt; 90% ownership; 0.30m distributions: **23.53m** |
| Strong | Year 7; 2,700 average and 3,500 exit NIPs; 900 new setups; 549 PLN blended monthly revenue | 19.14m revenue; 15.69m gross profit at 82%; 5.74m operating profit at 30%; exit ARR 23.058m | 100k founder capital plus a 2.0m growth-equity round for 20%; no debt at measurement; founder leaves employment after year 2; 100% retained while employed, then 80% retained | 5× ARR = 115.29m enterprise value; 5.0m cash; 80% ownership; 0.50m distributions: **96.73m** |

The larger cases require a staffed operations function and cannot be delivered personally within a five-hour daily founder schedule.

## 7. Acquisition route

The initial route uses the founder’s renewable-installer connection as a design partner, not as privileged distribution.

### First ten customers

1. The seven-person renewable installer.
2. Its accounting office as channel and workflow partner.
3. Two additional clients of that office.
4. Three nearby installers or electrical contractors using comparable order-to-invoice workflows.
5. Three trade or service SMEs referred jointly by the installer and accountant.

The initial message is: “We return every accepted KSeF number to the order record and give your accountant one controlled queue for anything that did not issue.”

### First one hundred

- Five accounting offices contributing 15 NIPs each: 75.
- Two vertical ERP or order-system implementers contributing 7–8 NIPs each: 15.
- Client referrals and adjacent trade networks: 10.

The office channel receives 15% of first-year recurring revenue or a wholesale price. A contractor operations lead becomes necessary before daytime exception response depends on the employed founder.

## 8. Control and compounding asset

The revocable KSeF authorization is operational access, not ownership. The accumulating asset is:

- Versioned mappings from order and ERP fields into FA(3).
- Client-approved invoicing and correction rules.
- Idempotency keys linking source transaction, payload, submission, KSeF number, and UPO.
- A labeled exception corpus by ERP, schema field, client, and resolution.
- Reconciliation history connecting invoices, corrections, and payments.
- Accountant-facing dashboards and multi-client operating routines.
- Measured resolution times and recurring fault patterns.

This can reduce onboarding and support cost as similar clients are added. Clients can still revoke authority and export their records, so retention must come from operational reliability rather than credential captivity.

## 9. Incumbent route-around

- ERP vendors can bundle submission, status retrieval, UPOs, and corrections into existing licenses.
- Comarch’s published packages demonstrate that high-volume KSeF communication can be sold for tens or hundreds of PLN monthly, including prices applicable to accounting offices. [Comarch price list](https://elte-s.com/wp-content/uploads/2026/01/Cennik_Comarch_KSeF_01.01.2026.pdf)
- API gateways advertise rapid implementation, trials, delegated authority, webhooks, and correction support. [ksef.io](https://ksef.io/)
- Low-cost front ends can serve simple single-NIP businesses. [PartsPC cost guide](https://serwis.partspc.pl/blog/ksef-mala-firma-koszt-wdrozenia.php)
- Accounting offices can keep issuance in-house, increase bookkeeping fees, or use a multi-client module.
- Clients can use Ministry tools and manual procedures when invoice volume and complexity are low.
- A vertical implementer can add the return identifier and exception register directly to its own product.

Accordingly, defensible scope begins where native software stops: cross-system approval, monitored exceptions, responsibility allocation, evidence handling, and reconciliation.

## 10. Rules, constraints, and lawful structure

### Classification

- **Delegated system right:** Issuance authority granted and revocable by the taxpayer.
- **Government-accepted record:** The KSeF identifier and UPO evidence acceptance into the system, not the lawfulness of the sale.
- **Binding operational rules:** Mandatory dates, authorization scope, authentication, outage handling, and sequencing of offline corrections.
- **Contractual rules:** Source-data responsibility, approval, SLA, security, incident notification, liability, and record retention.
- **Commercial constraints:** Low-cost native integrations, ERP control of source data, and reluctance to delegate.
- **Founder constraint:** Daytime service must be contractor-operated while the founder remains employed.

### Lawful structure

- Contract through a Polish limited-liability operating company.
- Separate service agreement, processing agreement, security schedule, and authorization matrix.
- Grant only `InvoiceWrite` unless invoice reading is required for an expressly purchased reconciliation function.
- Do not share the taxpayer’s personal signing credentials; grant the provider entity or named operators proper KSeF authority.
- Store private keys in managed key infrastructure, with rotation, access logging, and immediate revocation procedures.
- Require client approval of invoice rules and nominate persons authorized to resolve exceptions.
- Use append-only transmission records containing source hash, payload hash, operator, authorization context, timestamps, response, KSeF number, and UPO.
- Require explicit approval for substantive corrections.
- Exclude tax classification and legal-sale determinations unless separately delivered by an appropriately qualified professional.
- Carry cyber and professional-liability insurance where available, with contract limits that distinguish source-data mistakes from transmission failures.
- Obtain Polish legal review of VAT, data-protection, professional-services, and liability terms before production use.

## 11. Dependencies

- Stable access to the production KSeF API and timely adaptation to schema or authentication changes.
- Valid entity or operator authorization for every NIP.
- Secure certificate issuance, storage, rotation, and revocation.
- Deterministic exports or APIs from each client’s order and ERP systems.
- Named client personnel capable of resolving substantive exceptions.
- Contractor availability for business-hours monitoring.
- A gateway or direct connector supporting idempotency, UPO retrieval, retries, offline modes, and audit export.
- Contract terms and insurance acceptable to accounting-office partners.
- Reliable separation between technical validation and tax judgment.

## 12. Fastest paid proof and capital at risk

Use one accounting office and three of its clients.

- Charge 4,500 PLN total onboarding plus 1,347 PLN monthly at the accounting-office rate.
- Support one repeatable input format and one controlled manual fallback.
- Issue a production batch, return all KSeF identifiers and UPOs, and deliver an exception register.
- Reconcile every source record to accepted, rejected, held-for-client, or cancelled status.
- Operate least-privilege authorization with a tested revocation procedure.

Estimated cash at risk: **4,000–12,000 PLN**:

| Use | PLN |
|---|---:|
| Contract and data-processing review | 1,500–3,500 |
| Connector, mapping and contractor work | 2,000–6,000 |
| Gateway, monitoring and secure key handling | 500–1,500 |
| Contingency and incident rehearsal | 0–1,000 |

Non-cash exposure is approximately 80–120 founder hours. No broad ERP platform, tax engine, or payment-reconciliation product is required for this proof.

## 13. Kill criteria

Stop this implementation if any of the following becomes true:

- The initial accounting-office prospects categorically refuse delegated issuance by a separate provider.
- Their existing ERP already includes equivalent staffed exception resolution and evidence handling without an incremental fee.
- Counsel concludes that source-data and transmission liability cannot be separated contractually or insured on workable terms.
- The connector cannot guarantee idempotent linkage among the source transaction, submitted XML, KSeF number, correction, and UPO.
- Daytime outage and rejection handling cannot be staffed within the founder’s employment constraint and the proposed client price.
- Clients require the desk to make VAT or legal-sale determinations as part of routine issuance.
- Production support becomes bespoke per NIP rather than reusable by ERP or vertical.

## 14. Decision-critical unknowns

1. What fraction of accounting-office clients already receive adequate issuance and exception handling from their ERP?
2. Will an office delegate rights to a specialist entity or insist that only its own personnel hold authority?
3. How many minutes of operator work are required per NIP and per rejected document?
4. Which failures are caused by source-data quality rather than KSeF or connector behavior?
5. Will SMEs pay separately for managed issuance after inexpensive native modules are installed?
6. What liability cap and insurance cover will accounting offices accept?
7. How often do corrections, attachments, foreign-recipient cases, self-billing, and offline modes occur in the chosen vertical?
8. Can a single order-to-FA(3) mapping serve several renewable installers?
9. What are the production uptime and support performance of candidate gateways?
10. Can identifiers and UPOs be returned into incumbent systems without custom work for every client?

## 15. Development status

As of the research timestamp:

- The relevant mandatory KSeF stages are already active.
- Delegated issuance and revocation are supported by the official authorization model.
- Commercial API and ERP substitutes are already available.
- No prototype, production authorization, customer interview, signed office agreement, insurer indication, observed support workload, or paid production batch is evidenced in this packet.
- The next concrete artifact is a three-NIP paid production run with a complete acceptance and exception ledger.

## 16. Query ledger

All queries were executed on **2026-08-22** during the research session ending at **14:50:45 CEST**. The interface did not expose individual per-query seconds.

| ID | Exact query | Result used |
|---|---|---|
| Q01 | `site:ksef.podatki.gov.pl KSeF uprawnienia osoba podmiot biuro rachunkowe nadawanie uprawnień` | S01, S02 |
| Q02 | `site:ksef.podatki.gov.pl obowiązkowy KSeF terminy 2026 2027 10000 zł wykluczenie cyfrowe` | S02 |
| Q03 | `site:ksef.podatki.gov.pl KSeF offline24 awaria identyfikator UPO faktura` | S03 |
| Q04 | `site:gov.pl KSeF API certyfikat limity uprawnienia dokumentacja` | S04 |
| Q05 | `GUS aktywne przedsiębiorstwa Polska liczba mikro małe średnie 2024 raport przedsiębiorczość` | S05 |
| Q06 | `KSeF cennik integracja ERP abonament wysyłka faktur API Polska 2026` | S06, S08 |
| Q07 | `koszt wdrożenia KSeF mała firma biuro rachunkowe badanie 2025` | S07 |
| Q08 | `biura rachunkowe KSeF badanie gotowość klientów 2025 Polska` | No sufficiently robust readiness survey selected; retained as an unknown |

## 17. Source ledger

All sources were opened on **2026-08-22**, before the session-close timestamp **14:50:45 CEST**.

| ID | Source | Type and use |
|---|---|---|
| S01 | [Ministry of Finance: KSeF FAQ](https://ksef.podatki.gov.pl/ksef-news/najczestsze-pytania/) | Primary authority; accounting-office permissions, downstream delegation, revocation |
| S02 | [Ministry of Finance: mandatory KSeF scope](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/) | Primary authority; eligible delegates, commencement dates, temporary small-value exception |
| S03 | [Ministry of Finance: offline24](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/tryb-offline24/) | Primary authority; outage and offline correction workflow |
| S04 | [Ministry of Finance: production API documentation](https://api.ksef.mf.gov.pl/docs/v2/index.html) | Primary technical authority; authentication, permissions, certificates, asynchronous responses and limiting |
| S05 | [PARP: 2026 SME report](https://en.parp.gov.pl/storage/publications/pdf/ROSS_2026___29-04-2026.pdf) | Public market denominator based on GUS data |
| S06 | [ksef.io](https://ksef.io/) | Commercial vendor claims about integration speed, trial, permissions, SLA and feature scope |
| S07 | [PartsPC: small-business KSeF cost guide](https://serwis.partspc.pl/blog/ksef-mala-firma-koszt-wdrozenia.php) | Commercial pricing observation with stated limitations |
| S08 | [Comarch KSeF price list, reseller-hosted](https://elte-s.com/wp-content/uploads/2026/01/Cennik_Comarch_KSeF_01.01.2026.pdf) | Commercial incumbent pricing and introductory free periods; weaker provenance because hosted by a reseller |

## 18. Evidence ledger

| Evidence atom | Source | Status |
|---|---|---|
| Taxpayer can authorize an accounting office or other entity | S01, S02 | Verified |
| Authority can be scoped, delegated onward when permitted, and revoked | S01 | Verified |
| Mandatory issuance dates and temporary 10,000 PLN monthly exception | S02 | Verified |
| Receiving through KSeF mandatory from 1 February 2026 | S02 | Verified |
| Outage and total-outage handling differ | S03 | Verified |
| Offline correction can depend on prior KSeF numbering of the original | S03 | Verified |
| Production API requires authentication and exposes permission/certificate operations | S04 | Verified technical documentation |
| 2.374 million active non-financial firms; SMEs are 99.8% | S05 | Verified public statistic |
| Cheap native and gateway substitutes exist | S06–S08 | Verified as published offers |
| Gateway setup speed and 99.5% SLA | S06 | Vendor claim only |
| Displayed small-business prices of 29–219 PLN | S07 | Commercial observation; license period not established |
| Comarch packages of 15–600 PLN monthly | S08 | Published price list; reseller-hosted |
| SMEs will pay for a staffed delegated desk | None | Unknown |
| Managed issuance reduces collection delays | None | Plausible mechanism, unquantified |
| Accounting offices will accept the proposed liability split | None | Unknown |
| Scenario margins and recurring-revenue multiples | Internal model | Assumptions, not external evidence |
