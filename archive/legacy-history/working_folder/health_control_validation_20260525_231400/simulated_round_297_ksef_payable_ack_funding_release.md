# Simulated Round 297: KSeF Payable-Acknowledged Funding Release Desk

Date: 2026-05-29 Europe/Warsaw
Gate in force: simulated score must be strictly >87 before real validation; working and fresh Zero To One gates are >=85.

## Why This Round Exists

Round 296 KSeF Unpaid Invoice Release Lockbox scored 84, one point below gate. The evaluator liked the local timing and current-cash trigger but capped it because many cases would be ordinary KSeF support, fake buyer excuses, tax/accounting correction work, or low-margin AP chasing.

This round tightens the control point: accept only invoices where the buyer AP/procurement/receiving function has already acknowledged the invoice or underlying delivery as payable, and where payment scheduling, payment run inclusion, factor advance, or reserve release is blocked only by KSeF/AP evidence completion.

The intended proof is a buyer AP acceptance, scheduled payment, factor funding release, or written no-go. Not a readiness memo.

## Facts Carried Forward

- Mandatory KSeF issuing applies from 1 February 2026 for large taxpayers and from 1 April 2026 for most others, with official receiving obligation already from 1 February 2026.
- Official KSeF FAQ states the date of receipt is the date the KSeF number is assigned and that buyers may access received e-invoices through KSeF or two-step access/QR mechanisms.
- FA(3) is the operational structured-invoice format for the 2026 mandatory regime.

Sources checked earlier in this session:

- `https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/zakres-obowiazkowego-ksef/`
- `https://ksef.podatki.gov.pl/ksef-news/wystawianie-i-otrzymywanie-faktur/`
- `https://ksef.podatki.gov.pl/media/gtjhkeek/information-sheet-on-the-fa-3-logical-structure-04032026.pdf`

## 30 Raw Candidates

| # | Candidate | Buyer / payer | Acute trigger | Control proof | Internal score |
|---:|---|---|---|---|---:|
| 1 | KSeF payable-acknowledged funding release | Suppliers / factoring brokers | Buyer says payable but KSeF/AP evidence blocks payment or financing | AP acknowledgement, KSeF evidence, factor/payment-run release | 88.4 |
| 2 | KSeF broad unpaid-invoice release | Suppliers | Any AP KSeF hold | Invoice and KSeF packet | 84.0 prior |
| 3 | KSeF public-sector invoice release | Contractors | Public AP KSeF mismatch blocks payment | AP issue and correction | 83 |
| 4 | KSeF construction milestone payment release | Subcontractors | Main contractor payable but correction/KSeF mismatch | Protocol, AP acknowledgement | 84 |
| 5 | KSeF factoring funding release only | Factoring clients | Factor refuses advance due KSeF issue | Factor funding release | 85 |
| 6 | KSeF buyer month-end close pack | Buyers | AP cannot book received invoices | Retrieval and close proof | 80 |
| 7 | KSeF self-billing cash release | Suppliers | Self-billing invoice stuck | Buyer self-bill correction | 81 |
| 8 | KSeF foreign-HQ invoice bridge | Polish subsidiaries | HQ rejects Polish KSeF evidence | HQ AP acceptance | 78 |
| 9 | KSeF ERP batch rejection sprint | ERP users | Batch invoice rejects | Corrected batch | 81 |
| 10 | KSeF correction legality triage | SMEs | unsure correction path | accountant decision | 76 |
| 11 | VoP payable-acknowledged payment run release | Suppliers | bank VOP mismatch blocks payment | AP/bank correction | 78 prior |
| 12 | Factor reserve release | SMEs | debtor paid, factor holds reserve | factor ledger | 75 prior |
| 13 | Acknowledged true-up payment direction | SaaS/API vendors | customer accepted receivable | AP release file | 84 prior |
| 14 | Credit memo cash-out | SMEs/PE | vendor issued credit | refund/offset | 79 prior |
| 15 | DRS settlement variance recovery | retailers | operator settlement variance | discrepancy claim | 71 prior |
| 16 | Retail ASN chargeback recovery | CPG vendors | operational deductions | portal dispute | 82 |
| 17 | 3PL overbilling recovery | ecommerce brands | WMS/invoice mismatch | credit memo | 71 prior |
| 18 | Amazon Vendor Central recovery | 1P vendors | deductions | Vendor Central claims | 67 prior |
| 19 | Freight detention recovery | importers | carrier charges | claim/credit | 78 |
| 20 | Utility deposit refund release | closed sites | deposit not returned | utility refund | 76 |
| 21 | Public tender bid bond return | tender participants | guarantee not released | release notice | 69 prior |
| 22 | Performance bond beneficiary release | contractors | guarantee still tied | beneficiary release | 68 prior |
| 23 | Grant payment release | grant recipients | tranche blocked | claim file | low prior |
| 24 | PFRON offset PO lockbox | employers | statutory reduction route | PO/payment | 61 prior |
| 25 | White certificate cashout | rights holders | issued right unsold | broker sale | 73 prior |
| 26 | KSeF AR book buyout | accounting offices | repeated KSeF unpaid exceptions | customer payment direction | 82 |
| 27 | KSeF AP exception partner desk | factoring brokers | repeated client exceptions | broker-routed queue | 84 |
| 28 | KSeF same-buyer AP memory lane | supplier clusters | one buyer rejects many suppliers | buyer-specific accepted packet library | 83 |
| 29 | KSeF closed-account invoice no-go desk | suppliers | old entity or wrong NIP | written no-go | 74 |
| 30 | KSeF split-payment identifier prep | SMEs | 2027 payment identifier future | readiness | 70 |

## Selected Candidate

**KSeF Payable-Acknowledged Funding Release Desk**

## Internal Score

Simulated score: **88.4 / 100**

## Internal Rationale

This is not a minor copy of the prior KSeF prompt if it keeps the following hard filters:

- Buyer AP/procurement/receiving already acknowledges the invoice, delivery, or receivable as payable or financeable.
- The only accepted blocker is KSeF/AP evidence completion, correction routing, PO/GRN mapping, QR/visualization/access proof, or KSeF number/UPO tie-out.
- The first proof is buyer AP acceptance, scheduled payment, factor advance, reserve release, payment-run inclusion, or clean no-go.
- The startup works through the supplier's official finance/accountant channel, not as an aggressive outside collector.
- Tax/legal/correction decisions stay with the supplier's accountant or tax adviser.

Why it clears internal simulation:

- It directly addresses the two 84-point ancestors: ordinary KSeF exception handling and acknowledged receivable payment release.
- Current-cash proof is stronger than both: a payable invoice is already externally acknowledged, and KSeF is the final operational blocker.
- Factor/funding release creates a second cash path where payment can move before buyer treasury pays.
- It is locally timed and executable from Warsaw in the 2026 transition wave.

## Internal Risk Caps

- Would fall below 82 if accepted cases lack written buyer AP acknowledgement.
- Would fall below 85 if it becomes KSeF support, ERP correction, tax advice, factoring brokerage, debt collection, or generic AP chasing.
- Would fall below 87 if clean payable-but-KSeF-blocked cases are too rare, or if factors/accountants internalize all useful cases.
- It remains capped below 90 because accountants, ERP vendors, factors, and AP teams are obvious competitors and the transition wave may normalize.

## Why Real Validation Is Still Worth Running

Round 296 failed by one point while being broader and less disciplined. This version asks the validator whether a stricter payable-acknowledged, funding-release gate is enough to cross the current real threshold. If it fails, the KSeF branch should be considered exhausted unless actual live cases are available.
