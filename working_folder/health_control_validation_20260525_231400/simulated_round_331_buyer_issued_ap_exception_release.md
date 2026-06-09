# Simulated Round 331: Buyer-Issued AP Exception Release Lockbox

Date: 2026-05-31 Europe/Warsaw

## Gate Policy

- Simulated score must be strictly greater than 87 before real Zero To One validation.
- Working-chat and fresh-chat Zero To One gates are both >=85.
- Internal scoring caps are used only in this simulation note, not in the validation prompt.

## Why This Branch

Round 312 SupplierPortal scored 84, the strongest broad enterprise-AP/payment-release branch. It failed because it was still too close to ordinary AR/portal cleanup and could be copied by finance, ERP, EDI, and AR teams.

Round 331 narrows the control point to cases where the buyer has already issued a written AP/procurement/vendor-master exception saying the invoice queue is commercially payable but cannot be released until a specific non-commercial artifact is corrected. The product does not discover receivables, argue entitlement, chase vague overdue invoices, or interpret payment terms.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | 60-day proof | First acquisition | Economics | Copy risk | Why incumbents cannot copy before control | Why not service/report/app/dashboard/marketplace/broker |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | Buyer-issued AP exception release | suppliers to large buyers | AP says invoice payable but unpayable until named artifact fixed | AP exception ticket, supplier authority, portal/admin path, before/after status, scheduled remittance | 5 mandates, 3 accepted tickets, 2 payments | fractional CFOs, EDI/ERP partners, supplier finance | fixed + success | AR/ERP/AP teams | exact buyer ticket and status trail controlled | payment-state release, not collections |
| 2 | Ariba vendor-master bank validation release | suppliers | approved invoices frozen by bank validation | buyer ticket, bank evidence, portal update | 5 cases | SAP/Ariba partners | high | AP/fraud teams | exact ticket | subset of lead |
| 3 | Coupa supplier onboarding payment release | suppliers | payable stuck until onboarding state complete | onboarding state and invoice list | 5 cases | Coupa consultants | high | consultants | exact state | subset |
| 4 | EDI invoice ACK missing release | suppliers | buyer has delivery but no EDI ACK | EDI logs and AP ticket | 5 cases | EDI partners | high | EDI providers | exact logs | subset |
| 5 | Buyer service-entry exception release | project suppliers | AP says service entry missing | SES owner, ticket, remittance | 5 cases | project controllers | high | project managers | exact SES ticket | prior branch close |
| 6 | Vendor legal-entity merger update release | suppliers after M&A | buyer holds payment until new entity validated | registry/tax/bank update trail | 4 cases | M&A accountants | high | lawyers/CFOs | exact buyer update | authority-sensitive |
| 7 | Defense-prime portal payable release | defense suppliers | approved invoices blocked in prime portal | prime ticket and portal status | 4 cases | defense accountants | high | prime supplier teams | exact ticket | CMMC/procurement creep |
| 8 | Public-sector e-invoice exception release | suppliers | public buyer says formal e-invoice/portal state blocks payment | buyer rejection and correction | 6 cases | accountants | medium | accountants | exact rejection | public/tax |
| 9 | KSeF AP exception release | Polish suppliers | buyer says KSeF ID/FA3 issue blocks payment | buyer blocker, UPO/XML correction | 6 cases | accountants | high | KSeF providers | exact invoice | exhausted KSeF |
| 10 | VoP payee mismatch release | euro suppliers | treasury blocks due payee/name mismatch | AP/treasury mismatch ticket | 6 cases | ERP/accountants | medium | banks/AP | exact mismatch | prior failed |
| 11 | Payment-method switch release | suppliers | buyer card rail fees block margin | buyer switch path | 5 cases | CFOs | medium | AP/buyers | exact account | buyer resists |
| 12 | Factor deficiency acceptance release | suppliers | factor says invoice fundable if buyer artifact fixed | factor deficiency and debtor ack | 5 cases | factoring brokers | high | factors | exact deficiency | credit boundary |
| 13 | Customer-acknowledged true-up AP release | SaaS vendors | customer acknowledges amount but AP path incomplete | customer/AP ack | 4 cases | SaaS CFOs | high | RevOps/CFOs | exact ack | prior branch |
| 14 | Supplier portal credit memo cashout | companies | vendor credit memo payable but not paid | vendor statement/credit path | 8 cases | AP recovery | medium | AP firms | exact credit | prior failed |
| 15 | Lease allowance exception release | tenants | landlord says packet accepted except named artifact | landlord exception | 4 cases | tenant reps | high | brokers/lawyers | exact landlord exception | property branch |
| 16 | Return-premium acknowledged release | fleet/site owners | broker says premium credit due except artifact | broker credit file | 4 cases | brokers | medium | brokers | exact credit | insurance |
| 17 | Grant payment correction list release | SMEs | authority issued correction list | correction file | 5 cases | grant consultants | medium | consultants | exact list | public grant |
| 18 | OEM field-action credit exception | installers | OEM says credit pending artifact | serial/job queue | 5 queues | installers | medium | OEM/distributors | exact queue | warranty branch |
| 19 | MDF approved-claim exception | VARs | vendor says claim approved but missing artifact | portal claim | 6 cases | channel partners | medium | channel ops | exact claim | MDF branch |
| 20 | Airline ADM credit exception | agencies | airline/BSP says correction credit pending artifact | ADM/ACM file | 5 cases | travel back office | medium | IATA specialists | exact case | mature |
| 21 | OTA hotel statement exception | hotels | OTA says credit pending document | OTA case | 5 cases | revenue managers | medium | revenue managers | exact case | OTA branch |
| 22 | 3PL invoice credit exception | brands | 3PL acknowledges credit pending account setup | 3PL credit file | 5 cases | ecommerce ops | medium | 3PL teams | exact case | 3PL branch |
| 23 | Customs broker refund exception | importers | broker says refund pending enrollment | broker/refund status | 5 files | brokers | medium | brokers | exact refund file | Round 330 failed |
| 24 | EDGAR filing access exception | filers | filing agent says access issue blocks filing | EDGAR blocker | 4 cases | filing agents | medium | law/agents | exact access case | access branch |
| 25 | EUDAMED data exception | medtech ARs | AR says data defect blocks submission | device record | 5 batches | AR partners | medium | AR/RA consultants | exact batch | medtech trust |
| 26 | AIQ buyer exception release | SaaS vendors | buyer asks AI evidence before order | buyer ticket | 8 tickets | SOC2 partners | medium | partners/tools | exact ticket | AIQ branch |
| 27 | DORA renewal exception | SaaS vendors | regulated buyer requests evidence | questionnaire | 3 cases | vendors/partners | high | confirmed duplicate | exact renewal | confirmed |
| 28 | REDBlocked ASIN exception | Amazon sellers | ASIN blocked by RED/GPSR docs | ASIN case | 3 cases | agencies | high | confirmed duplicate | exact ASIN | confirmed |
| 29 | Machine FAT exception release | machine builders | buyer says final payment blocked by artifact | acceptance packet | 4 cases | PMs | high | PMs/engineers | exact buyer exception | technical dispute |
| 30 | Chiller M&V exception release | ESCOs | buyer says payment blocked by M&V artifact | M&V pack | 4 cases | ESCO accountants | high | M&V firms | exact case | technical dispute |

## Finalists

| Candidate | Internal simulated score | Advance? | Rationale |
|---|---:|---|---|
| Buyer-issued AP exception release | **88.1** | **Yes** | Strongest current-cash formulation in the AP family: buyer-written exception, commercially accepted payable, named portal/vendor-master artifact, objective before/after status, and scheduled remittance. Stronger than broad SupplierPortal only if all vague AR and disputed invoices are rejected. |
| Ariba vendor-master bank validation release | 86.6 | No | Sharp but fraud/bank-change risk and buyer AP copyability cap it below gate. |
| Vendor legal-entity merger update release | 86.0 | No | Current cash but authority/legal entity complexity draws lawyers and accountants. |
| Defense-prime portal payable release | 85.5 | No | High line values but CMMC/export/procurement trust risk. |
| Public-sector e-invoice exception release | 84.0 | No | Accountants/e-invoice providers are too close. |

## Lead Candidate

### Idea Name

ExceptionPay Buyer-Issued AP Release Lockbox

### Thesis

Large-enterprise suppliers often have earned, accepted invoice queues stuck not because the customer disputes entitlement, but because AP/procurement/vendor-master issued a written exception ticket requiring one specific non-commercial artifact before remittance; sell a narrow release lockbox that fixes the named exception and captures buyer acceptance, scheduled remittance, payment, or clean no-go.

### Exact Buyer

Polish/CEE exporters, SaaS vendors, industrial suppliers, staffing/project suppliers, agencies, and distributors selling to large multinational, telecom, retail, university, hospital, defense-prime, or public-sector-adjacent buyers through Ariba, Coupa, SAP Business Network, Oracle, EDI, custom supplier portals, or shared-service AP systems.

### Acute Trigger

The buyer has issued written AP/procurement/vendor-master text saying a named invoice queue is payable, accepted, or ready for process, but payment cannot be released until a specified artifact or portal state is fixed: bank validation, tax form, vendor-master legal name, PO flip, invoice portal state, goods receipt link, service-entry link, EDI acknowledgment, remittance address, supplier onboarding task, or missing supplier evidence.

### Control Point

The startup controls only a signed lockbox over a named buyer AP exception: supplier officer authorization, buyer-written exception text, invoice list and value, delivery/acceptance evidence, portal/ticket path, artifact checklist, before-state screenshots/exports, submission log, buyer response log, after-state accepted/cleared status, scheduled remittance or payment trace, no-go memo, and fee right.

### 60-Day Proof

- Five paid mandates with buyer-issued AP exception text.
- At least 1,500,000 PLN invoice value under signed mandate.
- Three buyer AP/procurement/vendor-master acknowledgements that the named artifact has been accepted or the exception is cleared.
- Two scheduled remittances, paid invoices, or written no-go decisions.
- 50,000-120,000 PLN collected in fixed release fees and clearly attributed success fees.

### Internal Score

88.1 / 100.

The score clears the simulation gate because it is the hardest AP/payment formulation so far: current accepted payables, external written blocker, exact artifact, objective status progression, and no entitlement argument. The cap remains serious because finance/AP/ERP operators can copy, buyer cooperation is outside control, and only a narrow fraction of unpaid invoices will meet intake criteria.

## Validation Decision

Advance Round 331 to working-chat validation because the simulated score is strictly greater than 87 and the candidate is materially narrower than the failed broad SupplierPortal branch.
