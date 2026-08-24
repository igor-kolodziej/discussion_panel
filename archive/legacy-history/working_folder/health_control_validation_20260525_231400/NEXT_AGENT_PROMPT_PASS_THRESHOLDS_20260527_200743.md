# Prompt For Next AI Agent: Confirmed-Idea Search Recovery Handoff

You are taking over a persistent confirmed-idea search in:

`/Users/igor/Desktop/discussion_panel`

Your goal is not to produce interesting ideas. Your goal is to find at least one idea that legitimately passes all gates:

- simulated score strictly `>87`;
- real working-chat Zero To One score `>=82`;
- real fresh-chat Zero To One score `>=82`;
- then write `/Users/igor/Desktop/discussion_panel/ideas/CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md` using a Europe/Warsaw timestamp.

Do not lower the bar. Do not stop with “no idea passed” unless Zero To One/browser access is blocked after following the browser startup flow, tools fail, or the user explicitly stops you.

## Critical User Correction

The user explicitly corrected the validation workflow:

> For future reference, do not give the validation agents the instructions for validations, e.g. “Cap below 85 without a hard control point securable in 6 months. Cap below 87 if CAC, payback, margins, cash conversion, or owner earnings are not credible.”

Therefore:

- Keep internal scoring caps for your own simulation only.
- Do **not** include internal scoring caps, evaluator instructions, or “cap below…” language in Zero To One validation prompts.
- Zero To One prompts should start with only:

```text
Score this business idea 0-100 and include strongest objections.

Founder context: unknown Warsaw solo founder, contractors allowed, max 100,000 PLN, 6-month POC, part-time.
```

Then include the idea fields. Do not add a final “question for scoring” that tells the evaluator how to cap the score.

## Current Browser State

Use `/Users/igor/Desktop/discussion_panel/BROWSER_STARTUP.md` for the browser flow.

At the moment of handoff, the headed gstack browser was healthy and on the working Zero To One chat:

- Browse binary: `/Users/igor/.codex/skills/gstack/browse/dist/browse`
- Working chat URL: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one/c/6a170a7b-0534-83eb-88db-34eb06704eaa`
- Fresh chat direct GPT URL: `https://chatgpt.com/g/g-69fc9f102bb081919a0b72d5daea394f-zero-to-one`

Important: the previous agent filled the working-chat textbox with the Round 108 prompt but was interrupted before clicking Send. When you resume, inspect the browser textbox first. Either:

- submit the existing Round 108 prompt if it is still present and you choose to continue that validation; or
- clear the textbox before sending a new prompt.

Do not accidentally send a stale prompt.

## Required Files To Read First

Read these before generating new candidates:

- `/Users/igor/Desktop/discussion_panel/ideas/CONFIRMED_IDEA_20260511_163033.md`
- `/Users/igor/Desktop/discussion_panel/ideas/CONFIRMED_IDEA_20260511_190013.md`
- `/Users/igor/Desktop/discussion_panel/ideas/CONFIRMED_IDEA_20260511_212329.md`
- `/Users/igor/Desktop/discussion_panel/ideas/confirmed_85s_club/CONFIRMED_IDEA_20260513_155748.md`
- `/Users/igor/Desktop/discussion_panel/ideas/UNCONFIRMED_IDEA_20260526_083609.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/best_rated_idea_characteristics_health_biosignal_rx_adjacent.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/real_working_validation_biowear_agency_ticket_book_buyout.md`
- `/Users/igor/Desktop/discussion_panel/BROWSER_STARTUP.md`

Also read the latest round files:

- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_104_matched_commercial_ff_e_lots.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/real_working_validation_hotelroom_ffe_package_lot_bank.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_105_installed_base_emergency_retainer_books.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/real_working_validation_legacy_line_control_first_call_spares_retainer.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_106_municipal_hazardous_waste_settlement_rails.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/real_working_validation_azbestkpo_all_property_settlement_rail.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_107_platform_inventory_block_case_flows.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/real_working_validation_hazmatblocked_fba_evidence_release_desk.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/simulated_round_108_recovery_claim_payment_mandates.md`
- `/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/zero_to_one_prompt_amazon_vendor_central_recovery_mandate.txt`

## Existing Confirmed Ideas To Avoid Duplicating

These are already confirmed or highly informative:

- **DORA Bank Renewal Evidence Pack**: working/fresh 91/91. Vendor-side regulated-finance evidence response for live DORA/ICT third-party-risk requests.
- **REDBlocked Amazon Connected-Device Evidence Rescue Desk**: latest/fresh 90. Agency-routed Amazon evidence response for connected baby monitors/indoor cameras under RED/CE/GPSR triggers.
- **BioSignal Claim-Risk Diligence Pack**: investor-paid biosignal claim-risk memo for early healthtech diligence.
- **HeritageDoor Suites**: working/fresh 87/87 under the 85s club. Complete matched pre-war interior door suites, controlled before fragmentation.
- **TraceFaktura All-Event Routing Pilot**: working 84, fresh 83 under a lower gate; municipal animal-care all-event invoice evidence rail.
- Other older confirmed themes: BatteryFit, PromoLeak, CBAM Import Continuity Desk, Data Act Machine Data Liberation Desk, GreenTender EPREL Bid Packs, Supplement Stack Safety, HeatQuiet.

Do not duplicate these. A similar idea is only acceptable if the control point, buyer trigger, payment event, and proof artifact are materially different.

## Latest Failure Log And Lessons

### Round 104: HotelRoom FF&E Package Lot Bank

- Simulated: 89
- Working Zero To One: 63
- File: `real_working_validation_hotelroom_ffe_package_lot_bank.md`

Why it failed:

- Used hotel FF&E is not scarce enough.
- Logistics, storage, condition, and buyer fit destroy margin.
- Existing liquidation/FF&E dealers already serve the market.
- The founder becomes a furniture mover/liquidator.

Lesson: stop mining generic physical lots unless the asset is genuinely scarce, coherent, high-margin, and deposit-matched with low logistics drag. HeritageDoor worked because full pre-war door suites are structurally fragmented/destroyed and premium buyers pay for historical continuity. Hotel FF&E did not have that scarcity.

### Round 105: Legacy Line-Control First-Call Spares Retainer

- Simulated: 90
- Working Zero To One: 69
- File: `real_working_validation_legacy_line_control_first_call_spares_retainer.md`

Why it failed:

- Industrial spare incumbents are strong.
- Factories may not pay retainers before failure.
- Compatibility/testing credibility is hard.
- Retiring-technician books are personal and may not transfer.
- Emergency response is not a good part-time-founder fit.

Lesson: even “installed-base + paid retainer + titled spares” is too weak if buyers still search trusted incumbents at the moment of failure. Avoid industrial spares unless the founder controls an already-paid transaction stream.

### Round 106: AzbestKPO All-Property Settlement Rail

- Simulated: 90
- Working Zero To One: 68
- File: `real_working_validation_azbestkpo_all_property_settlement_rail.md`

Why it failed:

- Contractors may already handle settlement with normal admin, BDO exports, photos, and spreadsheets.
- Contractor margins may be thin.
- Gmina payment friction may be weaker than assumed.
- Seasonality and crew capture weaken proof.

Lesson: TraceFaktura-like event rails need very acute payment friction. “Better municipal documentation” is not enough unless there is withheld current cash, mandatory routing, and measurable payment acceptance improvement.

### Round 107: HazmatBlocked FBA Evidence Release Desk

- Simulated: 91
- Working Zero To One: 73
- File: `real_working_validation_hazmatblocked_fba_evidence_release_desk.md`

Why it failed:

- Agencies already solve simple SDS/exemption cases.
- Hard cases require real manufacturer/lab documents outside founder control.
- Amazon outcomes are opaque.
- Reviewer said even good proof only rises to 80-82.

Lesson: do not keep testing evidence-only Amazon desk variants unless the control point includes recovered cash, a signed claim mandate, or a stronger payment stream. REDBlocked passed because the connected-device regulatory trigger and agency case-memory wedge were unusually sharp. Adjacent platform evidence desks are not automatically strong.

### Round 108: Amazon Vendor Central Recovery Mandate

Files already written:

- `simulated_round_108_recovery_claim_payment_mandates.md`
- `zero_to_one_prompt_amazon_vendor_central_recovery_mandate.txt`

Status:

- Prompt was filled into the working Zero To One chat textbox, but the user interrupted before Send.
- It has not been validated yet unless the next agent sends it.

Why this candidate is more promising than the last platform desks:

- It is cash recovery, not evidence-only unblock.
- Hard proof is a signed recovery mandate, live deduction queue, filed disputes, Amazon acknowledgement/credit memo, and first success-fee invoice.
- It still has duplicate risk with PromoLeak, so the prompt distinguishes Amazon Vendor Central 1P deduction workflows from broad retailer promo/deduction leakage.

You may submit Round 108 first, but do not be emotionally attached. If it fails working validation below 82, write `real_working_validation_amazon_vendor_central_recovery_mandate.md` and continue.

## Search Strategy That Should Improve The Odds

The previous agent failed by overestimating:

- physical-lot scarcity;
- route-book transferability;
- generic evidence-desk urgency;
- buyer willingness to pay for “better documentation”;
- preventive retainers before a failure.

The next search should prioritize only candidates where current cash, assigned claims, direct payment direction, or live cases are already controlled.

Ask first:

> What can a solo founder legally control, assign, recover, collect, title, reserve, or route inside 60 days where the first proof is cash movement, not interest?

### Preferred Next Domains

1. **Recovery mandates and assigned claims**
   - Already-deducted, short-paid, overbilled, or platform-held cash.
   - Signed mandate or assignment.
   - Debtor/platform acknowledgement or portal case.
   - First recovered credit/payment inside 60 days.
   - Avoid claims requiring legal practice, tax advice, insurance adjustment authority, or litigation.

2. **Current payment-direction changes**
   - Customer-approved direct billing transfer.
   - Payment lockbox over existing invoices.
   - Seller handoff plus current-month cash before close.
   - Avoid vague goodwill/customer lists.

3. **Platform/portal claim queues with monetary outcomes**
   - Amazon Vendor Central deductions.
   - Retailer shortage/chargeback queues.
   - Freight invoice audit credits.
   - Carrier claims only if debtor acknowledgement and payout path are stronger than the old failed parcel idea.

4. **Buyer-deposit scarce lots only when logistics are trivial**
   - Compact, high-value, serial-numbered lots.
   - Buyer deposit before title transfer.
   - Clear compatibility and return terms.
   - Avoid bulky FF&E, random industrial spares, and generic used equipment.

5. **Agency-routed live cases only where the agency cannot internalize**
   - Must have specialist evidence and clear repeated case memory.
   - Must not depend on third-party source documents the founder cannot influence.
   - Better if success is cash/credit recovered, not only a packet submitted.

## Candidate Ideas Worth Testing After Round 108

Use these as starting points, not as final answers. For every raw candidate, force the table:

- buyer;
- acute trigger;
- transferable control point;
- exactly what is signed/titled/assigned/prepaid within 60 days;
- first acquisition mechanism;
- gross margin and payback logic;
- copy risk;
- why incumbents cannot copy before the founder controls the specific asset/account/case/claim/lot;
- why it is not a service/report/app/dashboard/marketplace/broker.

### A. Stronger Recovery/Cash Candidates

1. **Amazon Vendor Central Recovery Mandate**
   - Already written as Round 108; validate first if not sent.
   - Watch duplicate risk with PromoLeak and incumbents like SupplyPike/Threecolts.

2. **Freight Invoice Credit Recovery Mandate for CEE Importers**
   - Buyer: importers/exporters with many freight invoices.
   - Trigger: demurrage/detention/accessorial/rate errors already charged.
   - Control: signed recovery mandate, invoice/BOL/accessorial data, carrier/forwarder claim submissions, first credit.
   - Risk: freight audit incumbents; weak if only an audit report.

3. **Retailer ASN/OTIF Chargeback Recovery Mandate**
   - Buyer: CPG/beauty/household vendors shipping to specific retailers.
   - Trigger: deductions already taken for ASN, appointment, label, pallet, shortage, or compliance chargebacks.
   - Control: retailer portal access, deduction register, filed disputes, first reversal.
   - Risk: close to PromoLeak; must focus on non-promo operational deductions and actual reversed cash.

4. **3PL Overbilling Recovery Mandate**
   - Buyer: ecommerce brands using outsourced 3PLs.
   - Trigger: storage, pick-pack, return, and special-handling invoices do not match WMS/order evidence.
   - Control: 3PL contract, WMS exports, invoice lines, signed claim mandate, first credit memo.
   - Risk: consultants can copy; must find brands with obvious live credits.

5. **Cloud Marketplace Remittance Recovery Mandate**
   - Buyer: small SaaS vendors selling through AWS/Azure/Google marketplaces.
   - Trigger: private-offer remittance, tax, discount, or payout mismatches.
   - Control: marketplace reports, contract/order evidence, support cases, first credit.
   - Risk: niche and data access; but potentially high-ticket and under-served.

6. **Hotel OTA Commission/Chargeback Recovery Mandate**
   - Buyer: independent hotel groups with Booking/Expedia/OTA statements.
   - Trigger: commission, cancellation/no-show, virtual card, tax/fee or chargeback errors.
   - Control: OTA account exports, PMS reconciliation, filed claims, first credit.
   - Risk: revenue managers already handle many cases.

### B. Payment-Transfer Micro-Acquisitions

7. **Narrow B2B Consumable Route With Customer-Approved Direct Billing**
   - Only if current-month recurring orders and payment direction transfer before close.
   - Examples: printer labels/ribbons for named warehouses; water filters for named Horeca customers; industrial absorbents/PPE for named plants.
   - Avoid if it becomes wholesale distribution from scratch.

8. **Retiring B2B Warranty/Repair Admin Book With First Current-Month Cash**
   - Must not depend on licensed/authorized provider as core value.
   - Seller must transfer phone/domain, customer approvals, current invoices, and payment direction.
   - Avoid fiscal-device/autoclave/calibration shapes that already failed due provider-of-record dependence.

9. **Commercial Cleaning Consumables Reorder Book Buyout**
   - Buyer/payor: B2B sites already buying recurring consumables.
   - Control: customer-approved payment transfer and supplier terms, not just route list.
   - Proof: first-month collected cash before acquisition close.
   - Risk: commodity and low margin unless route density/current cash is real.

### C. Compact Scarce Lots With Deposits

10. **Exact Lease-End POS Terminal/Printer Fleet With Buyer Deposits**
    - Only if MDM/payment data wiped, compatibility bounded, and buyer deposits pre-close.
    - Avoid payment-processing role.

11. **Hotel Safe/Minibar Fleet Deposit Buyout**
    - More compact than FF&E; buyer: serviced apartments/hotels needing identical compact equipment.
    - Risk: still commodity/service/warranty.

12. **Specialized Event/Rental Hardware Lot With Signed Booking Demand**
    - Compact, high-value, upcoming-event rental demand, buyer deposits.
    - Avoid bulky tents/furniture and seasonal low-margin assets.

## Validation Workflow

Use the existing working folder:

`/Users/igor/Desktop/discussion_panel/working_folder/health_control_validation_20260525_231400/`

Continue round numbering:

- Round 108 exists and is pending validation.
- If Round 108 is not used or fails, continue at Round 109.

For each round:

1. Generate 30-50 raw candidates from hard-control categories.
2. Force the control table for every raw candidate.
3. Advance only 4-6 finalists.
4. Apply strict internal caps:
   - internal cap below 82 without concrete 6-month control proof;
   - internal cap below 85 if one vendor contract, equipment purchase, consultant, or hire can copy it;
   - internal cap below 87 if CAC, payback, margins, cash conversion, or owner earnings are weak;
   - internal cap below 87 if dependent on vague partnerships/goodwill/interviews;
   - internal cap below 82 if clinical/legal/patient/regulated-data authority is unresolved.
5. Only real-gate simulated scores strictly `>87`.
6. Write:
   - `simulated_round_NN_<slug>.md`
   - `zero_to_one_prompt_<slug>.txt`
7. Real working-chat validate the exact prompt.
8. If working score `<82`, write `real_working_validation_<slug>.md` and continue.
9. If working score `>=82`, submit the exact same prompt wording to a fresh Zero To One chat and write `real_fresh_validation_<slug>.md`.
10. If both real gates pass, write `/Users/igor/Desktop/discussion_panel/ideas/CONFIRMED_IDEA_YYYYMMDD_HHMMSS.md`.

## Prompt Template For Zero To One

Do not include internal caps. Use:

```text
Score this business idea 0-100 and include strongest objections.

Founder context: unknown Warsaw solo founder, contractors allowed, max 100,000 PLN, 6-month POC, part-time.

Idea name:

One-sentence thesis:

Exact buyer:

Acute trigger:

Control point:

60-day signed/titled/assigned/prepaid proof:

6-month POC:

First acquisition mechanism:

Economics:

Copy risk:

Why incumbents cannot copy before the founder controls the specific asset/account/case/claim/lot/payment stream:

Why it is not a service, report, app, dashboard, database, marketplace, or generic broker:

Boundaries and legal/provider limits:

Duplicate risk against existing confirmed ideas:

Strongest anticipated objections:
```

## Browser Submit Flow

Inspect first:

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse status
/Users/igor/.codex/skills/gstack/browse/dist/browse snapshot -i
```

If browser is stale, follow `/Users/igor/Desktop/discussion_panel/BROWSER_STARTUP.md`.

To submit:

1. Find textbox ref in snapshot.
2. Fill:

```bash
/Users/igor/.codex/skills/gstack/browse/dist/browse fill @TEXTBOX_REF "$(cat /path/to/prompt.txt)"
```

3. Snapshot and find “Send prompt”.
4. Click send.
5. Poll after 30-40 seconds:

```bash
sleep 35; /Users/igor/.codex/skills/gstack/browse/dist/browse text | tail -260
```

6. Save the score and strongest objections in the real validation file.

## Safety And Scope Rules

For Rx, GLP-1, controlled substances, alcohol/drug testing, genetics, EEG, medical workflows, or health data:

- Do not propose direct sale, resale, brokering, advertising, or delivery of prescription or controlled drugs.
- Licensed clinicians/pharmacies/labs remain provider, prescriber, dispenser, lab, and seller of record.
- The startup must not diagnose, prescribe, interpret clinical tests, validate health claims, certify medical devices, or handle patient genetic/health data unless legal/control structure is explicitly solved.
- Avoid consumer-patient trust transfer unless the control point is a legally transferable entity/payment book and current-month cash flow is proven.

Given the recent failures, avoid health/Rx/clinical-adjacent routes unless the hard control point is unusually strong.

## What To Do First

1. Read the required files.
2. Inspect browser textbox for the unsent Round 108 prompt.
3. If Round 108 prompt is still present, submit it to working Zero To One unless you decide it is obviously duplicative of PromoLeak after reading the files.
4. If Round 108 working score is `>=82`, fresh-validate the exact same prompt.
5. If it fails, write the validation file and continue with Round 109 focused on recovery mandates or direct payment-transfer books.

Do not drift back to:

- generic evidence desks;
- physical inventory with bulky logistics;
- route books where the real asset is a licensed provider or trusted technician;
- “we can help with documentation” workflows without current cash blocked or recovered;
- marketplaces, dashboards, dashboards disguised as reports, or brokered introductions.

The winning candidate will probably be ugly and finance/admin-heavy: a signed claim queue, deduction register, recovery mandate, payment direction, current credit memo, or prepaid live case where first cash appears inside the proof window.
