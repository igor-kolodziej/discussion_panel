# Simulated Round 242: SWIFT CSP Attestation Evidence Release

Date: 2026-05-30 Europe/Warsaw

Current real gate: working Zero To One `>=85`, fresh Zero To One `>=85`.

Simulation rule: only advance a candidate if simulated score is strictly `>87`. Internal scoring caps are used only here, never in the Zero To One prompt.

## Pivot Logic

The latest data-rights and RED-adjacent variants failed because they lacked a mandatory current cash or network-access gate. SWIFT CSP has a sharper annual gate: all SWIFT users submit annual KYC-SA security attestations, with independent assessment support, and non-attestation can create policy, supervisory, counterparty, and operational risk. This round tests whether a narrow evidence-assembly product for smaller SWIFT users can avoid becoming generic cyber consulting by staying assessor-ready and live-attestation-bound.

## Raw Candidate Control Table

| # | Candidate | Buyer | Acute trigger | Transferable control point | Signed/titled/assigned/prepaid inside 60 days | First acquisition mechanism | Gross margin / payback logic | Copy risk | Why not service/report/app/dashboard/broker |
|---|---|---|---|---|---|---|---|---|---|
| 1 | SwiftBridge CSP Attestation Evidence Sprint | Smaller SWIFT users | Annual KYC-SA attestation/independent assessment window or correspondent request | Signed mandate, BIC/user scope, control-evidence room, assessor handoff, KYC-SA draft support | 2 users, 1 assessor partner, 1 assessor-ready pack | CSP assessors, small banks, EMIs, treasury vendors | 20k-60k PLN; protects network/counterparty access | Big Four/cyber firms/assessors can copy, but exact attestation case controlled | Attestation evidence artifact, not assessment |
| 2 | Correspondent KYC Security Evidence Pack | banks/EMIs | correspondent asks security evidence | request thread/evidence room | paid case | correspondent banking advisers | high | banks/cyber firms | response pack |
| 3 | SWIFT New-Joiner Go-Live Pack | new SWIFT users | must attest before go-live | onboarding scope/evidence | paid case | service bureaus | high | SWIFT consultants | go-live pack |
| 4 | SWIFT Service Bureau Customer Evidence | corporates using bureau | customer asks CSP support | service bureau evidence | paid case | bureaus | medium | bureaus | evidence |
| 5 | KYC-SA Remediation No-Go Desk | SWIFT users | failed controls block submission | gap log | prepaid | assessors | medium | cyber firms | no-go/remediation routing |
| 6 | SWIFT Architecture Scope Map | SWIFT users | unclear architecture type/scope | scoping file | paid | CSP advisers | medium | assessors | narrow artifact |
| 7 | SWIFT Evidence Room Refresh Retainer | SWIFT users | annual refresh | recurring evidence | prepaid | existing clients | medium | cyber firms | refresh artifact |
| 8 | Payment Institution CSP Overflow | EMIs/payment firms | July-Dec deadline | evidence pack | prepaid | fintech advisers | high | cyber firms | pack |
| 9 | Corporate Treasury SWIFT Evidence Pack | large corporates | annual attestation | treasury evidence | prepaid | treasury consultants | medium | treasury/cyber | pack |
| 10 | Securities Broker SWIFT CSP Pack | brokers | attestation/counterparty | evidence pack | prepaid | brokerage IT | medium | cyber firms | pack |
| 11 | Central Securities Depository Supplier Pack | infra vendors | SWIFT/counterparty evidence | evidence | paid | infra advisers | high | specialized consultancies | too regulated |
| 12 | ISO 20022 Evidence Release | banks/corporates | migration/project evidence | project evidence | paid | payment consultants | medium | payment firms | project support |
| 13 | SEPA Instant Payments VoP Evidence | PSPs | VoP go-live | evidence | failed branch | no | no | already failed | reject |
| 14 | PCI TPSP Evidence Pack | payment SaaS | customer asks PCI evidence | evidence | failed branch | no | no | already failed | reject |
| 15 | DORA ICT Supplier Evidence | vendors | bank renewal | confirmed | confirmed | no | no | duplicate | reject |
| 16 | DORA Register Correction Sprint | regulated entities | register correction | evidence | failed | no | no | weak | reject |
| 17 | PSP Reserve Release | merchants | funds held | mandate | failed | no | no | platform | reject |
| 18 | MiCA CASP Bank Evidence | crypto firms | bank/PSP continuity | evidence | failed | no | no | legal/cyber | reject |
| 19 | Fund Transfer Fraud Underwriting Pack | SMEs | insurer asks controls | evidence | failed | no | no | cyber branch | reject |
| 20 | AML Correspondent Questionnaire Pack | small banks | correspondent asks AML | evidence | prepaid | AML consultants | medium | AML firms | legal/compliance |
| 21 | Sanctions Screening Evidence Pack | payment firms | correspondent asks sanctions controls | evidence | prepaid | sanctions advisers | medium | AML firms | legal/sanctions |
| 22 | TMS/Finastra Upgrade Evidence | banks | core payment upgrade | evidence | paid | integrators | medium | vendors | too technical |
| 23 | SWIFT RMA Counterparty Evidence Sprint | SWIFT users | RMA relationship blocked | request/evidence | paid | correspondent advisers | high | banks/cyber | specific gate |
| 24 | SWIFT Control 1.1 Environment Inventory | users | assessor asks inventory | asset inventory | paid | assessors | medium | cyber firms | subartifact |
| 25 | SWIFT MFA Evidence Collection | users | control evidence missing | screenshots/proofs | paid | MSPs | medium | MSPs | remediation drift |
| 26 | SWIFT Backup/DR Evidence Pack | users | control evidence missing | backup/DR artifacts | paid | MSPs | medium | cyber firms | subartifact |
| 27 | SWIFT Supplier Security Evidence | SWIFT users with outsourcers | outsourced environment | supplier evidence | paid | service bureaus | medium | outsourcers | specific |
| 28 | SWIFT KYC-SA Late Submission Rescue | users | deadline near | evidence/action list | prepaid | assessors | high | assessors | emergency pack |
| 29 | SWIFT CSP Board Pack | banks | board/audit committee asks | evidence summary | paid | CFO/CISO | medium | cyber firms | report-ish |
| 30 | Treasury-Bank SWIFT Security Request | corporates | bank asks SWIFT controls | evidence response | paid | treasury consultants | medium | banks | response pack |
| 31 | SWIFT Assessor Slot Prep Desk | certified assessors | assessor needs prepared clients | client evidence room | paid by assessor/client | assessors | medium | assessors hire staff | overflow |
| 32 | CSCF Evidence Change Delta | repeat users | new annual control version | delta pack | prepaid | prior clients | medium | cyber firms | refresh |
| 33 | SWIFT Customer Audit Response | users | supervisor asks attestation evidence | audit file | paid | compliance firms | high | auditors | evidence |
| 34 | KYC-SA Application Upload Support | users | portal submission | upload checklist | paid | SWIFT consultants | low | users/assessors | too admin |
| 35 | SWIFT CSP Evidence Escrow | users | counterparties want visibility | shared evidence room | paid | banks/corporates | medium | GRC platforms | dashboard risk |

## Finalists And Strict Internal Scores

| Rank | Candidate | Internal simulated score | Decision | Rationale |
|---|---|---:|---|---|
| 1 | SwiftBridge CSP Attestation Evidence Sprint | 88.9 | Advance | Mandatory annual SWIFT user attestation, independent assessment support, network/counterparty consequences, high-value regulated buyers, and assessor overflow make this sharper than generic cyber evidence. |
| 2 | SWIFT New-Joiner Go-Live Pack | 86.7 | Do not gate | Strong go-live gate but small, lumpy lead flow and SWIFT consultants/service bureaus sit closest. |
| 3 | SWIFT RMA Counterparty Evidence Sprint | 85.9 | Do not gate | Strong commercial trigger but harder to source repeat cases and may duplicate correspondent banking advisory. |
| 4 | Payment Institution CSP Overflow | 85.5 | Do not gate | Good submarket, but too narrow as standalone unless combined with lead candidate. |
| 5 | SWIFT Assessor Slot Prep Desk | 84.8 | Do not gate | Good channel but risks becoming assessor staffing/overflow service with weak moat. |
| 6 | AML Correspondent Questionnaire Pack | 80.0 | Do not gate | Real buyer pain, but legal/compliance incumbents and broad AML judgment create a cap. |

## Internal Objections Before Real Gate

- Certified SWIFT CSP assessors, Big Four, cyber consultancies, and internal bank security teams are natural owners.
- A non-assessor founder cannot perform the independent assessment or submit truthful attestation decisions.
- Smaller SWIFT users may still be mature enough to buy directly from assessors.
- If underlying controls are missing, the case becomes remediation, not evidence assembly.
- Sensitive SWIFT architecture/security data creates trust friction.
- The buyer pool may be small in Poland/CEE after filtering for users small enough to need help but valuable enough to pay.
- It may look like a DORA/cyber evidence duplicate unless the control object is the annual KYC-SA attestation file and assessor handoff.

## Advance

Advance **SwiftBridge CSP Attestation Evidence Sprint** to working Zero To One validation.

Expected real-score risk: likely `72-82` if the evaluator treats it as cyber consulting or assessor-owned. Possible `85+` only if it credits the mandatory annual SWIFT KYC-SA gate, independent-assessor overflow, and network/counterparty consequences as a structurally stronger live evidence gate than adjacent failed cyber/compliance packs.
