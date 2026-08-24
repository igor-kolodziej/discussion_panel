# W2-L2-005 — KSC registry and incident-evidence operator

**Research timestamp:** 2026-08-22, Europe/Warsaw (CEST)  
**Budget used:** exactly 8 distinct web queries; exactly 8 useful sources opened; no budget transfer.  
**Concept status:** service and workflow design; no paid deployment or customer evidence established in this packet.

## 1. Transaction

A Polish entity whose KSC status has already been determined by its management or qualified counsel authorizes the operator to:

1. assemble and quality-check its Wykaz KSC registration data;
2. prepare an entity-approved registry submission or update;
3. maintain the contact and service map;
4. preserve an auditable incident chronology and supporting evidence; and
5. prepare client-approved materials for submission through S46.

The first paid event is delivery of the approved registry dossier, completed submission workflow and electronic evidence receipt or registration certificate.

The operator does **not** determine whether the client is an essential or important entity, decide whether an event is legally reportable, suppress evidence, alter timestamps or submit without documented authority.

---

## 2. Verified problem and payer evidence

### Verified evidence

- The amended KSC regime requires essential and important entities to enter the KSC register, implement an information-security management system, use S46, maintain contact persons and manage and report incidents. Entities meeting the criteria when the amendment entered into force must register by **3 October 2026** and complete the broader implementation and S46 transition by **3 April 2027**. [Ministry of Digital Affairs — obligations](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych), [Ministry — timetable](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc--najwazniejsze-terminy)

- Registration requires structured entity, activity, size, contact and account-administrator data. The entity normally designates at least two contact persons; a micro or small entity may designate one. [Amending Act, Dz.U. 2026 poz. 252](https://eli.gov.pl/api/acts/DU/2026/252/text/T/D20260252L.pdf), [UKE implementation guidance](https://www.uke.gov.pl/akt/wdrazanie-przepisow-znowelizowanej-ustawy-ksc-przygotowanie-do-realizacji-obowiazkow-przez-podmioty-kluczowe-i-podmioty-wazne%2C682.html)

- Registration, amendment and deletion applications may be handled by a proxy if an electronically signed power of attorney is attached. Registry data covered by Article 7(2)(1–18) must be updated within **14 days** after a change. The registered entity can generate an electronic registration certificate. [Official KSC FAQ](https://cyber.gov.pl/assets/pdf/faq-ksc.pdf)

- For a serious incident, the amended act specifies an early warning within **24 hours**, the serious-incident notification within **72 hours**, requested interim reporting and a final report within one month. The entity must protect documentation from loss, unauthorized access and integrity failure, maintain versions and retain withdrawn security documentation for the statutory period. [Amending Act](https://eli.gov.pl/api/acts/DU/2026/252/text/T/D20260252L.pdf)

- Non-registration and failures connected with Article 9 duties can result in administrative penalties. Management can also face a separate penalty for listed failures, capped in the act by reference to a multiple of remuneration. Statutory responsibility therefore remains with the entity and its management even where preparation is outsourced. [Amending Act](https://eli.gov.pl/api/acts/DU/2026/252/text/T/D20260252L.pdf)

- Outsourcing cybersecurity work is established buyer behavior: KPMG reported that 94% of surveyed organizations outsourced at least one cybersecurity task in 2025, while approximately one quarter outsourced support in responding to cyberattacks. Its survey also reported at least one security incident at 96% of participating organizations. [KPMG Poland Cybersecurity Barometer 2026](https://assets.kpmg.com/content/dam/kpmgsites/pl/pdf/2026/03/Raport-KPMG-w-Polsce-Barometr-cyberbezpiecze%C5%84stwa-2026.pdf.coredownload.inline.pdf)

- A commercial Polish KSC provider advertises a gap audit from **4,900 PLN net**, followed by separate implementation and maintenance services. This establishes a low-end adjacent-service price, not a registry-operations price. [NIS2.org.pl service page](https://nis2.org.pl/)

- A 2026 public procurement notice for KSC/KRI/ISO 27001 work required prior qualifying implementation experience worth at least **40,000 PLN gross**. This shows procurement demand and the experience burden for public buyers, but it is not the awarded price of the proposed service. [e‑Zamówienia notice 2026/BZP 00170086/01](https://ezamowienia.gov.pl/mo-client-board/bzp/notice-details/2026%2FBZP%2000170086%2F01)

### Interpretation

The operational problem is not merely entering data once. The recurring workload is maintaining current contacts and service information, collecting evidence held by several vendors, preserving chronology and coordinating an entity-approved response inside short statutory windows.

The likely payer is a medium-sized regulated entity with an IT manager or outsourced MSP but without a dedicated GRC or incident-governance team. Management has purchasing power because it retains the legal exposure; an IT manager alone may recognize the need but cannot safely authorize filing or legal classification.

### Unknown

No source in the fixed packet established:

- the current number of self-registered entities;
- the number already entered ex officio;
- the number of medium private entities without internal governance staff;
- live sector-by-sector supervisory practice; or
- willingness to pay specifically for registry administration and evidence readiness.

---

## 3. Exact transaction and incentive/power map

| Participant | Provides or controls | Incentive | Power or veto |
|---|---|---|---|
| Entity manager/board | Authority, budget, final approval | Avoid missed duties and management exposure | Signs contract and filing authority; can stop every submission |
| Qualified counsel/client compliance owner | Applicability and legal interpretation | Correct scope and defensible reporting decisions | Controls classification and legal conclusions |
| Client IT/security lead | System map, incident facts, logs and vendor access | Reduce coordination burden | Can withhold or verify technical evidence |
| MSP/MSSP/vendors | Operational telemetry and incident actions | Retain client and limit contractual exposure | Control much of the raw evidence and response timing |
| Operator | Workflow, evidence requests, chronology, registry dossier and reminders | Setup fee, recurring revenue and incident fee | May reject incomplete or unauthorized work; has no statutory decision power |
| Authorized signatory/proxy | Electronic submission authority | Timely, controlled filing | Final filing action |
| CSIRT/sector CSIRT | Receives incident materials and may request more information | National and sector incident response | Determines official response and follow-up |
| Sector authority | Supervision and enforcement | Compliance and service continuity | Inspection, corrective measures and penalties |
| MSP, law firm, auditor or association | Referral and trust transfer | Client retention, referral revenue or wider engagement | Controls access to its client base |
| Cyber insurer | Policy terms and claims handling | Lower incident and evidence risk | Can impose vendor, notification and documentation conditions |

### Transaction sequence

1. Client or counsel supplies written confirmation that applicability and category have already been determined.
2. Client signs the MSA, data-processing terms, scope-specific authority and, where used, electronic power of attorney.
3. Operator issues a structured request covering entity data, activities, size declaration, services, contacts, vendors and account administrator.
4. Client data owners attest to the supplied facts.
5. Operator prepares the registry dossier and exception list.
6. Manager, authorized person or counsel approves the final version.
7. Authorized filing occurs; the receipt and certificate are preserved with timestamps and dossier version.
8. On retainer, the operator runs contact attestations, vendor-evidence checks and 14-day change workflows.
9. During an incident, the operator builds an immutable chronology and draft reporting package. The client and its designated legal/security authority decide classification and approve submission.
10. Evidence receipts, requests from CSIRT and subsequent reports are linked to the chronology.

---

## 4. Payer denominator

### Verified denominator

The researched official sources define covered sectors and size/activity rules, but they do not provide a current count of medium private entities that:

- are already classified;
- were not completely handled by an ex-officio entry;
- lack a dedicated governance team; and
- are willing to outsource this workflow.

A Poland-wide numerical denominator is therefore not asserted.

### Obtainable denominator

The usable denominator should be a named-account list held by distributors, not a speculative count of all Polish businesses.

**First-ten denominator assumption**

- 4 regional distributors;
- 25 already-classified medium clients screened per distributor;
- 100 named prospects;
- 10 paid registry engagements represented in the operating case.

**First-hundred denominator assumption**

- 10 distributors;
- 50 already-classified, relevant clients per distributor;
- 500 named prospects;
- 100 active customers represented in the channel plan.

The denominator excludes organizations still seeking an applicability opinion, banks governed by the separate financial-sector reporting route, public tenders requiring unavailable references and enterprises already served by a mature internal GRC team.

---

## 5. Price, unit economics and cash timing

All prices exclude VAT.

| SKU | Proposed price | Direct delivery cost | Gross profit | Cash timing |
|---|---:|---:|---:|---|
| Registry dossier, filing workflow and receipt | 8,000 PLN | 1,400 PLN | 6,600 PLN / 82.5% | 4,000 at authorization; 4,000 on approved receipt |
| Evidence-readiness maintenance | 2,500 PLN/month | 500 PLN/month | 2,000 PLN / 80% | Quarterly in advance |
| Serious-incident evidence package | 12,000 PLN | 5,000 PLN | 7,000 PLN / 58% | 6,000 mobilization; balance on approved final package |
| Contact or material registry change outside allowance | 1,500 PLN | 300 PLN | 1,200 PLN / 80% | On approval of update |

Referral compensation is modeled as sales expense rather than delivery cost:

- 10% of first-year collected revenue for an originated account;
- paid only after client cash is received;
- no fee on legal classification.

A customer buying setup plus twelve months of maintenance produces:

- revenue: **38,000 PLN**;
- direct delivery cost: **7,400 PLN**;
- gross profit: **30,600 PLN**, or **80.5%**;
- first-year referral expense: **3,800 PLN**;
- contribution before central overhead: **26,800 PLN**.

With one serious-incident package, first-year revenue becomes **50,000 PLN** and direct delivery cost **12,400 PLN**.

These are designed prices. The verified adjacent anchor is a 4,900 PLN gap audit; no registry-operator price was found. The service must therefore demonstrate that its deliverable is operational custody, evidence readiness and approved filing—not a smaller compliance checklist.

---

## 6. Founder-wealth cases

Measurement date: **31 December 2033**, after approximately seven operating years. Revenue is annual revenue at the measurement date, not cumulative revenue.

Valuation multiples, client volumes and margins below are modeling assumptions, not observed market outcomes.

| Item | Conservative | Expected | Strong |
|---|---:|---:|---:|
| Active recurring clients | 120 | 300 | 800 |
| Annual setup engagements | 30 | 80 | 180 |
| Annual incident packages | 12 | 30 | 80 |
| Average annual retainer | 30,000 PLN | 36,000 PLN | 42,000 PLN |
| Setup price | 8,000 PLN | 9,000 PLN | 10,000 PLN |
| Incident price | 12,000 PLN | 15,000 PLN | 18,000 PLN |
| Annual revenue | 3.984m PLN | 11.970m PLN | 36.840m PLN |
| Gross margin | 74% | 78% | 82% |
| Gross profit | 2.948m PLN | 9.337m PLN | 30.209m PLN |
| Operating margin | 18% | 27% | 33% |
| EBITDA | 0.717m PLN | 3.232m PLN | 12.157m PLN |
| Enterprise-value assumption | 3.0× EBITDA | 4.5× EBITDA | 6.0× EBITDA |
| Enterprise value | 2.151m PLN | 14.544m PLN | 72.943m PLN |
| Net debt at measurement | 0 | 0.300m PLN | 1.500m PLN |
| Founder ownership | 100% | 85% | 75% |
| Founder equity value | 2.151m PLN | 12.107m PLN | 53.582m PLN |
| Cumulative after-tax distributable cash | 1.000m PLN | 4.000m PLN | 15.000m PLN |
| Reinvested | 0.950m PLN / 95% | 3.800m PLN / 95% | 15.000m PLN / 100% |
| Gross optional distributions | 0.050m PLN | 0.200m PLN | 0 |
| Approx. founder distributions after 19% dividend tax | 0.041m PLN | 0.162m PLN | 0 |
| Business-derived founder net worth | **2.192m PLN** | **12.269m PLN** | **53.582m PLN** |

### Capital, debt and dilution assumptions

- **Conservative:** 60,000 PLN founder capital; no debt or dilution. Founder remains employed through most of the build and relies on contractors for deadline coverage.
- **Expected:** full 100,000 PLN founder capital; 300,000 PLN working-capital facility; 15% employee/adviser ownership issued by 2029. Founder leaves employment during 2028.
- **Strong:** 100,000 PLN founder capital; up to 1.5m PLN net debt for security operations and channel expansion; 25% total employee and investor dilution. Founder leaves employment during 2027.

Reinvested cash is assumed to fund delivery capacity, software, security and customer acquisition and is already reflected in the operating business. It is **not** added again to equity value. Founder capital is likewise represented by the equity and is not separately added. Only net personal distributions are added to founder equity value.

---

## 7. Acquisition route

### Primary route

1. Regional MSP identifies clients already covered by KSC.
2. Client’s counsel or compliance owner confirms classification.
3. Operator delivers a white-label or co-branded registry/evidence workflow.
4. MSP continues technical service; operator owns the administrative evidence calendar.
5. Counsel retains all legal interpretation.

The seven-person renewable installer near Ostrów Wielkopolski is useful as a warm route into renewable-sector vendors, installers and their MSPs. It should not be described as a regulated customer unless its status has independently been confirmed.

### First ten customers

- 3 from the initial regional MSP;
- 2 from a second MSP serving industrial or logistics firms;
- 2 referred by law firms that do not want continuing evidence operations;
- 2 through a water, waste, energy or industrial association;
- 1 through an IT auditor.

Each receives the same manual, secure registry workflow before automation is built.

### First hundred customers

- 10 channel partners with approximately 50 pre-screened clients each;
- 20% modeled conversion across that named universe;
- vertical templates for energy, water/waste, manufacturing, transport and digital services;
- a partner dashboard showing missing evidence, upcoming attestations and client-approved receipts;
- centralized delivery staff while partners retain the customer relationship.

The founder’s employed-hours limit is handled by scheduled onboarding, standardized evidence requests and paid contractor coverage. No founder-only 24/7 promise is offered.

---

## 8. Control and compounding asset

The durable asset is not access to the government portal. Direct self-registration is available, so portal knowledge alone is easy to route around.

The compounding operating asset consists of:

- current client service and contact maps;
- reusable sector-specific registry schemas;
- signed authority and approval chains;
- timestamped evidence-request and receipt history;
- incident chronology templates;
- recurring evidence feeds from MSPs and vendors;
- observed vendor response times and recurring missing-data patterns;
- change and renewal calendars; and
- integrations that convert MSP telemetry into client-reviewable evidence objects.

Client-specific evidence remains confidential and is not resold. Only reusable schemas, workflow logic and lawfully aggregated operational metadata compound across customers.

---

## 9. Incumbent route-around

| Substitute | Route around the operator | Operator response |
|---|---|---|
| Internal security/GRC team | Completes registration and evidence internally | Concentrate on medium entities without that team |
| Law firm | Adds filing administration to legal advice | Operate as the law firm’s evidence and workflow layer |
| MSP/MSSP | Bundles registry support with technical services | White-label the process and avoid replacing the MSP |
| Governance platform | Adds Polish KSC forms and reminders | Supply managed evidence collection, approvals and vendor coordination |
| Large consultancy | Bundles KSC into a wider SZBI project | Offer narrower fixed-price setup and recurring custody |
| Government self-service | Entity files directly at low cash cost | Sell preparation, maintenance, chronology and receipts rather than portal access |

The most direct route-around is an MSP or law firm copying the checklist. Defensibility therefore depends on secure integrations, evidence history, response workflow and channel contracts—not the form itself.

---

## 10. Rule and constraint classification

### Binding statutory rules

- Client applicability and category arise from the act, not from the operator’s contract.
- Registration is due within six months after meeting the conditions; the commencement cohort has the 3 October 2026 date.
- Registry changes covered by the official FAQ require updating within 14 days.
- Filing must use an accepted electronic signature or seal.
- Contact-person and S46 duties remain the entity’s duties.
- Incident reporting follows the statutory 24-hour, 72-hour and final-report sequence where applicable.
- Security documentation requires controlled access, integrity protection, versioning and retention.
- The entity and its management retain statutory responsibility.

### Delegable administrative rule

Registration, amendment and deletion can be handled by a properly authorized proxy. The published FAQ describes the required electronic power of attorney.

### Operational constraints

- Evidence is fragmented across management, MSPs, tools, vendors, HR and counsel.
- Incident work can require availability outside the founder’s five-hour workday.
- Raw evidence may contain personal, confidential or security-sensitive data.
- Incorrect timestamps or undocumented edits would damage the evidentiary record.
- Public procurement may require prior references unavailable to a new operator.

### Commercial constraints

- Basic registration can be completed directly.
- Buyers may initially prefer a one-time filing.
- Law firms, MSSPs and GRC vendors can extend into the workflow.
- The first engagement must distinguish administration from unauthorized legal advice.

---

## 11. Lawful structure

1. Operate through a Polish limited-liability company with cyber/E&O and professional-liability terms reviewed against the actual scope.
2. Require written client or counsel confirmation of applicability before onboarding.
3. Use separate documents for:
   - master services;
   - data processing;
   - confidentiality and security;
   - registry power of attorney;
   - approved subcontractors;
   - evidence retention/deletion;
   - incident mobilization; and
   - final client approval.
4. Limit registry authority to named actions and named entities.
5. Do not treat registry authority as automatic authority to make incident classifications or submit incident reports.
6. Keep client tenants segregated, encrypt data in transit and at rest, maintain immutable activity logs and use least-privilege access.
7. Preserve original evidence and generate transformed working copies; never overwrite source files or timestamps.
8. Require two-person approval for external submission.
9. Contract a qualified MSSP or incident-response provider for out-of-hours intake.
10. Market the service as authorized administration and evidence operations, never as government certification or legal classification.

---

## 12. Dependencies

- qualified Polish counsel for scope boundaries and client-side classification;
- a live test of proxy registration and account roles;
- written clarification of delegated S46 incident access;
- regional MSP or MSSP distribution;
- 24/7 incident intake supplied by a contractor or partner;
- secure multi-tenant evidence storage and immutable logs;
- electronic signatures, seals and powers of attorney;
- cyber/E&O insurance quotations;
- client data owners willing to attest to source facts;
- accountant confirmation of tax and cash-distribution assumptions;
- sector-specific CSIRT instructions; and
- vendor contracts permitting evidence transfer and retention.

---

## 13. Fastest paid proof and capital at risk

### Paid proof

Within four weeks:

1. One MSP selects one already-classified client.
2. Client counsel supplies the classification confirmation.
3. Operator receives a narrow registry power of attorney and data-processing authority.
4. Operator assembles the Article 7 data, contact map and registry dossier.
5. Client approves and submits, or the authorized proxy submits.
6. Operator delivers the receipt, versioned evidence bundle and an S46/incident operating procedure.
7. Client pays **8,000 PLN net**.

A tabletop exercise should then test whether evidence from the MSP can be converted into a 24-hour warning package and 72-hour report draft without the operator making the legal reporting decision.

### Capital at risk: 8,000–20,000 PLN

Indicative uses:

- counsel review of authority and service terms;
- secure evidence workspace and logging;
- electronic-signature and test administration costs;
- contractor participation in the tabletop exercise;
- insurance quotation and underwriting materials; and
- limited travel and partner onboarding.

No custom platform is necessary before the paid workflow is completed manually.

---

## 14. Kill criteria

Stop the registry-proxy component if the live government workflow cannot support a commercially usable power-of-attorney process.

Remove incident submission from scope if S46 access cannot lawfully or securely be delegated; retain only evidence preparation for submission by the client.

Do not retain raw incident evidence if appropriate insurance, segregation, access logging and breach-response terms cannot be obtained within available capital.

End a distributor relationship if it requires the operator to provide unsigned legal classification opinions, conceal incidents or submit without explicit approval.

Discontinue the recurring-maintenance proposition if buyers consistently purchase only the filing and will not authorize contact checks, evidence feeds or incident-readiness work.

Do not promise out-of-hours response until a named MSSP or incident-response contractor is contractually responsible for intake and escalation.

---

## 15. Decision-critical unknowns

1. Exact S46 account roles and whether a third-party operator can prepare or submit incident materials under delegated authority.
2. Current counts of self-registered and ex-officio-entered entities.
3. Sector-specific differences in supervisory and CSIRT practice.
4. Which registry fields or evidence objects can be accessed through an API.
5. Acceptable cyber/E&O coverage, exclusions and premium.
6. Whether clients will permit recurring evidence feeds from MSP tools.
7. Buyer preference for quarterly maintenance versus one-time filing.
8. Incident frequency and the proportion requiring a serious-incident workflow.
9. Whether insurers require their own notification before or alongside KSC reporting.
10. GDPR roles for mixed evidence containing employee, customer or attacker data.
11. Required retention periods for incident evidence beyond the explicit security-documentation rule.
12. Availability and price of reliable out-of-hours incident coordination.
13. Referral restrictions for law firms, auditors and insurance distributors.
14. Time needed for a new operator to obtain procurement references acceptable to public entities.

---

## 16. Development status

- **Law and public infrastructure:** the amended act is in force; self-registration began in May 2026; new entities could begin S46 use from June 2026.
- **Service:** specified at workflow and unit-economic level only.
- **Product:** no software build is required for the first paid engagement; a secure manual evidence workspace is sufficient.
- **Distribution:** family access provides a regional introduction route, but no partner commitment is evidenced.
- **Customers:** none evidenced in this packet.
- **Insurance and delegated access:** unresolved.
- **Incident operations:** require a contracted out-of-hours provider before being sold as a response-time service.

---

## 17. Query ledger

All queries executed on **2026-08-22 CEST**.

| ID | Exact query | Purpose |
|---|---|---|
| Q01 | `site:gov.pl cyfryzacja nowelizacja KSC obowiązki podmiotów kluczowych ważnych rejestr 3 października 2026 art. 46` | Official obligations and dates |
| Q02 | `site:eli.gov.pl KSC 2026 ustawa krajowym systemie cyberbezpieczeństwa tekst art. 46 rejestr podmiotów kluczowych ważnych` | Binding statutory text |
| Q03 | `site:gov.pl KSC zgłaszanie incydentów 24 72 godziny dowody podmioty kluczowe ważne` | Incident timetable and reporting |
| Q04 | `site:stat.gov.pl Polska przedsiębiorstwa średnie sektory energia transport zdrowie produkcja liczba 2024` | Potential payer denominator |
| Q05 | `site:biznes.gov.pl NIS2 KSC sektory średnie przedsiębiorstwa podmiot ważny kluczowy Polska` | Sector and size interpretation |
| Q06 | `Polska NIS2 KSC zgodność usługa cena audyt wdrożenie cennik 2026` | Commercial price anchors |
| Q07 | `zamówienie publiczne NIS2 KSC audyt wdrożenie cyberbezpieczeństwo wartość PLN` | Procurement spend and requirements |
| Q08 | `Polska MSP partner cyberbezpieczeństwo NIS2 ubezpieczenie cyber raport rynek 2025 2026` | Outsourcing, channels and market behavior |

---

## 18. Source ledger

All sources accessed on **2026-08-22 CEST**.

| ID | Source | Type | Evidence used |
|---|---|---|---|
| S01 | [Ministry — KSC obligations](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---obowiazki-podmiotow-kluczowych-i-waznych) | Primary public authority | Registration, SZBI, S46, contacts and incident duties |
| S02 | [Amending Act, Dz.U. 2026 poz. 252](https://eli.gov.pl/api/acts/DU/2026/252/text/T/D20260252L.pdf) | Binding law | Registry data, contacts, documentation controls, incident deadlines and penalties |
| S03 | [Ministry — implementation timetable](https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc--najwazniejsze-terminy) | Primary public authority | Registration, S46 and audit dates |
| S04 | [UKE implementation guidance](https://www.uke.gov.pl/akt/wdrazanie-przepisow-znowelizowanej-ustawy-ksc-przygotowanie-do-realizacji-obowiazkow-przez-podmioty-kluczowe-i-podmioty-wazne%2C682.html) | Sector authority | Contact-person and S46 implementation detail |
| S05 | [Official KSC FAQ](https://cyber.gov.pl/assets/pdf/faq-ksc.pdf) | Primary implementation guidance | Proxy filings, signatures, ex-officio entries, 14-day updates and certificates |
| S06 | [NIS2.org.pl](https://nis2.org.pl/) | Commercial provider | 4,900 PLN adjacent audit price and service packaging |
| S07 | [e‑Zamówienia notice](https://ezamowienia.gov.pl/mo-client-board/bzp/notice-details/2026%2FBZP%2000170086%2F01) | Procurement source | KSC/NIS2 audit demand and 40,000 PLN prior-experience condition |
| S08 | [KPMG Cybersecurity Barometer 2026](https://assets.kpmg.com/content/dam/kpmgsites/pl/pdf/2026/03/Raport-KPMG-w-Polsce-Barometr-cyberbezpiecze%C5%84stwa-2026.pdf.coredownload.inline.pdf) | Market survey | Incident prevalence, outsourcing behavior and response outsourcing |

---

## 19. Evidence ledger

| Evidence ID | Claim | Source | Classification |
|---|---|---|---|
| E01 | Essential and important entities must register and implement KSC duties | S01, S02 | Verified |
| E02 | Commencement cohort registration date is 3 October 2026 | S01, S03, S05 | Verified |
| E03 | S46 and broader implementation date is 3 April 2027 | S01, S03 | Verified |
| E04 | At least two contact persons are normally required; small/micro entities may use one | S02, S04 | Verified |
| E05 | Registry filings and changes may be made through an electronically authorized proxy | S05 | Verified |
| E06 | Relevant registry changes must be filed within 14 days | S05 | Verified |
| E07 | Serious-incident sequence includes 24-hour, 72-hour and one-month events | S02 | Verified |
| E08 | Security documentation requires access control, integrity, versioning and retention | S02 | Verified |
| E09 | Entity and management exposure remains despite outsourcing | S02 | Verified |
| E10 | Adjacent commercial gap-audit pricing begins at 4,900 PLN net | S06 | Verified commercial offer |
| E11 | Public procurement can require prior work worth at least 40,000 PLN gross | S07 | Verified procurement condition |
| E12 | 94% of KPMG respondents outsourced at least one cybersecurity task | S08 | Verified survey result |
| E13 | Approximately one quarter outsourced cyberattack-response support | S08 | Verified survey result |
| E14 | Registry operations can be sold at 8,000 PLN plus maintenance | Unit model | Interpretation/assumption |
| E15 | Four partners can furnish 100 named prospects for the first-ten campaign | Channel model | Assumption |
| E16 | National medium-entity payer count is currently known | — | Unknown; not established |
| E17 | Delegated S46 incident submission is permitted | — | Unknown; not established |
| E18 | The workflow can produce the modeled margins and 2033 values | Financial cases | Assumption, not observed outcome |
