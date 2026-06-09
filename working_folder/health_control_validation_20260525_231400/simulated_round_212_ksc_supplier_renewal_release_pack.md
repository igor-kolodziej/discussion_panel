# Simulated Round 212: KSC Supplier Renewal Release Pack

Date: 2026-05-29 Europe/Warsaw

## Gate Reminder

- Internal simulated score must be strictly above 87 before browser validation.
- Real working-chat Zero To One gate is `>=85`.
- Real fresh-chat Zero To One gate is `>=85`.
- Internal scoring caps remain internal only and are not included in the Zero To One prompt.

## Current External Facts Used

- Poland has implemented NIS2 through the amended National Cybersecurity System Act, with obligations active in 2026.
- Official Polish guidance describes an expanded catalogue of entities subject to cybersecurity obligations.
- Official Polish guidance also describes a registration deadline for covered entities in 2026.
- NIS2 includes supply-chain-security obligations, and in-scope entities are pushing risk-management requirements into direct supplier and service-provider relationships.

References used for internal simulation only:

- `https://www.gov.pl/web/cyfryzacja/nowelizacja-ustawy-o-krajowym-systemie-cyberbezpieczenstwa-ksc---kogo-obejmuje`
- `https://www.gov.pl/web/rozwoj-technologia/sprawdz-czy-twoja-firme-obejmie-obowiazek-wpisu-do-ksc`
- `https://digital-strategy.ec.europa.eu/en/policies/nis2-directive`

## Raw Candidate Sweep

| # | Candidate | Buyer | Acute trigger | Control point inside 60 days | First proof | Main reason not advanced |
|---|---|---|---|---|---|---|
| 1 | KSC Supplier Renewal Release Pack | SME suppliers to Polish NIS2/KSC entities | Non-bank customer renewal, addendum, PO, or onboarding held for supplier-risk evidence | Buyer request, supplier authorization, evidence packet, addendum response, accepted/no-objection trail | Renewal/addendum/PO released | Advanced |
| 2 | KSC Register Entry Sprint | Newly in-scope entities | Registration deadline | Account, classification file, management signoff | Register submission | Too broad and consultant-like |
| 3 | NIS2 Board Evidence Binder | In-scope entities | board wants readiness proof | policies/risk register | board signoff | GRC consulting |
| 4 | NIS2 Incident 24h Reporting Pack | In-scope entities | incident-reporting obligations | incident playbook | drill | MSSPs/lawyers own |
| 5 | High-Risk Supplier Phaseout Desk | Regulated buyers | high-risk supplier exposure | inventory/phaseout plan | approved exception/plan | too political/legal |
| 6 | OT Supplier Security Addendum Response | OT vendors | utility/industrial buyer asks for OT/security clauses | buyer request and response | contract signed | strong but narrower version of #1 |
| 7 | Backup/DR Evidence Release | suppliers | buyer asks for BCP/DR proof | test evidence | buyer approval | too generic |
| 8 | Subprocessor/Subcontractor Notice Pack | SaaS/MSP vendors | buyer asks for supplier chain | inventory/addendum response | buyer approval | DORA-adjacent, weaker |
| 9 | NIS2 MSP Customer Renewal Pack | MSPs | customers ask for NIS2 posture | MSP evidence | renewal | trust/security-remediation heavy |
| 10 | NIS2 Cyber Insurance Evidence Pack | in-scope SMEs | insurer underwriting | evidence pack | quote bound | insurance brokers/cyber firms |
| 11 | DORA Non-Finance Expansion | tech suppliers | DORA customer renewal | evidence pack | renewal | duplicate with confirmed DORA |
| 12 | AI Act Procurement Evidence | AI vendors | enterprise buyer AI Act asks | evidence pack | renewal | prior AI variants weak/early |
| 13 | Accessibility Act Contract Release | e-commerce/SaaS | buyer accessibility hold | VPAT/audit response | order released | incumbents/accessibility agencies |
| 14 | CRA Product Security Pre-File | device/software makers | Cyber Resilience Act prep | SBOM/security file | buyer approval | obligations mostly future |
| 15 | Radio Equipment Cyber Security Release | IoT vendors | RED cybersecurity evidence | test/evidence file | market release | close to REDBlocked |
| 16 | Railway Cyber Supplier Pack | rail suppliers | rail operator asks cyber evidence | response pack | renewal | narrow/trust-heavy |
| 17 | Water Utility Vendor Cyber Pack | control vendors | utility KSC addendum | response pack | PO | included in #1 |
| 18 | Energy Distributor Supplier Pack | field service/software suppliers | energy customer flowdown | response pack | renewal | included in #1 |
| 19 | Waste-Management Supplier Pack | waste logistics/software vendors | municipal/regulatory buyer requests | response pack | renewal | weaker WTP |
| 20 | Postal/Courier Supplier Pack | parcel-tech vendors | courier buyer flowdown | response pack | renewal | included in #1 |
| 21 | KSeF Supplier Security Evidence | ERP providers | invoice platform data/security ask | pack | contract | prior KSeF weak |
| 22 | Sectoral CSIRT Contact Setup | in-scope entities | reporting contact | account/contact file | registration | admin task |
| 23 | NIS2 Management Liability Brief | boards | fines/liability anxiety | memo | paid workshop | advisory |
| 24 | Vulnerability Disclosure Setup | vendors | buyer asks for VDP | policy/contact page | buyer approval | too easily copied |
| 25 | SBOM Buyer Response | software vendors | buyer asks for SBOM | SBOM and vuln process | renewal | crowded tooling |
| 26 | Backup Evidence Test Slots | SMEs | buyer asks last restore | contractor restore test | buyer accepted | IT service, not control |
| 27 | OT Remote Access Exception Release | industrial service vendors | buyer blocks remote access | access policy/MFA/logging pack | access restored | remediation-heavy |
| 28 | Supplier Incident Notice Addendum Desk | vendors | customer sends NIS2 clauses | negotiated response | addendum signed | legal review heavy |
| 29 | NIS2 Training Evidence Pack | suppliers | buyer asks training proof | training logs | buyer accepted | low WTP/commodity |
| 30 | Pen-test Retest Release Pack | vendors | buyer asks remediation proof | retest evidence | buyer accepted | pen-test firms own |
| 31 | Cloud Region Evidence Pack | SaaS vendors | buyer asks data location | cloud evidence | renewal | DORA-like, crowded |
| 32 | Asset Inventory Snapshot Pack | suppliers | customer asks CMDB/process | evidence pack | approval | generic GRC |
| 33 | KSC Supplier Addendum Contract Inbox | law firms/MSSPs | overflow flowdown answers | intake + response | paid cases | agency subcontractor, not business |
| 34 | Industrial Control Supplier Renewal Evidence | small SCADA/PLC vendors | utility/manufacturing buyer asks | accepted evidence | renewal | finalist but included in #1 |
| 35 | NIS2 Bid Evidence Pack | suppliers bidding to in-scope entities | tender asks NIS2 security | bid annex | bid accepted | tender-pack risk |
| 36 | Secure Development Evidence Pack | software vendors | buyer asks SDLC/vuln mgmt | SDLC pack | renewal | tooling/consultants |

## Finalist Comparison

| Finalist | Control strength | Cash/renewal link | Copy risk | 6-month founder fit | Internal score |
|---|---:|---:|---:|---:|---:|
| KSC Supplier Renewal Release Pack | 8 | 9 | 7 | 7 | **88.6** |
| OT Supplier Security Addendum Response | 8 | 8 | 6 | 6 | 84 |
| NIS2 MSP Customer Renewal Pack | 7 | 8 | 5 | 5 | 78 |
| KSC Register Entry Sprint | 5 | 6 | 5 | 7 | 72 |
| Accessibility Act Contract Release | 6 | 7 | 5 | 6 | 72 |
| SBOM Buyer Response | 6 | 7 | 4 | 6 | 70 |

## Selected Candidate

**KSC Supplier Renewal Release Pack**

One-sentence thesis: help small suppliers to Polish NIS2/KSC-covered entities clear live customer renewal, addendum, PO, or onboarding holds by assembling buyer-specific supplier-risk evidence and response language that the customer accepts or marks no-objection.

## Why It Passes Internal Simulation

- Poland's KSC/NIS2 implementation is live and forces supply-chain security into customer/supplier relationships outside regulated finance.
- The payment event is not an abstract compliance milestone; it is a current renewal, addendum, PO, onboarding, remote-access restoration, or supplier-risk approval held by a named customer.
- The founder does not need to remediate cybersecurity; the POC only accepts cases where underlying evidence exists and the gap is evidence assembly, response structure, or buyer-specific language.
- Warsaw location is useful: Polish-language buyer requests, KSC references, local sectors, and non-bank industrial/utility/transport/service suppliers.
- It is materially different from the confirmed DORA bank renewal idea because the buyer side is not financial ICT third-party-risk under DORA; it is Polish NIS2/KSC supply-chain flowdown across essential/important non-bank sectors.
- Case memory can compound across recurring buyer request patterns: incident notice, continuity, access control, backup, subcontractor, vulnerability, high-risk supplier, and management-approval language.

## Internal Cap Check

- Concrete 6-month control proof: yes, prepaid live cases plus accepted/no-objection customer responses and released renewal/addendum/PO.
- Copyable by one consultant or hire: partially, but buyer-specific KSC flowdown memory and urgent response execution are narrower than broad GRC consulting.
- CAC/payback/margins/cash conversion: credible only where at least 100,000 PLN of contract value is at risk and upfront fees are paid.
- Vague partnerships/goodwill/interviews: avoid; require a written customer request and contract consequence.
- Legal/regulated authority: manageable if the startup does not certify compliance, give legal advice, perform security remediation, or handle sensitive production data beyond the packet.

## Simulated Score

**88.6 / 100**

## Simulation Caveats

The idea should be killed if:

- fewer than three prepaid live cases appear in 60 days;
- more than half of qualified cases require real security remediation rather than evidence response;
- customers insist on law-firm, MSSP, ISO auditor, or CISO ownership;
- suppliers will not pay at least 15,000 PLN for a live contract hold;
- accepted/no-objection outcomes cannot be obtained in under 14 business days;
- the market treats KSC/NIS2 supplier flowdowns as ordinary low-fee questionnaire work.

## Browser Validation Decision

Proceed to working-chat Zero To One validation using:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_ksc_supplier_renewal_release_pack.txt`
