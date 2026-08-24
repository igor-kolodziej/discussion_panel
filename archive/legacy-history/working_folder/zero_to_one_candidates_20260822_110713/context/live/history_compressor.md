# Immutable Context Packet — Live Neutral History Compressor

## Isolation and role

- Agent ID: `live-history-compressor-01`
- Role: neutral history compressor only.
- Read only this packet. Do not browse, inspect the repository, generate candidates, rank, select, reject, merge, score, or propose pivots.
- Output neutral fingerprints. Strip scores, thresholds, evaluator language, colorful rejection language, and proposed remedies.
- Preserve `unvalidated` as `unvalidated`; do not recast it.

## Output schema

Return one compact record per historical shape with exactly these fields:

1. fingerprint ID (`HIST-001`, sequential)
2. customer
3. loss event
4. payer
5. solution primitive
6. transaction unit or paid trigger
7. acquisition route
8. possible compounding asset
9. status: `confirmed`, `unvalidated`, `rejected`, or `unknown`
10. source artifact IDs

You may consolidate multiple rejected examples only when their customer, loss, payer, paid trigger, route, and compounding mechanism are materially the same. State all source shape names in that record.

## Confirmed and unvalidated source shapes

1. `ideas/CONFIRMED_IDEA_20260511_105542.md` — BatteryFit Retrofit Pack. Small photovoltaic installers pay for qualification of battery, EMS, or heat-storage retrofit opportunities among existing PV customers; event is a retrofit sales decision; installer channel; accumulating retrofit economics/fit records. Status confirmed.
2. `ideas/CONFIRMED_IDEA_20260511_113716.md` — PromoLeak Recovery Desk. Challenger consumer brands pay to recover retailer, marketplace, or distributor deductions; event is a disputed deduction or withheld receivable; route through finance/commercial teams; accumulating deduction patterns and recovery evidence. Status confirmed.
3. `ideas/CONFIRMED_IDEA_20260511_120859.md` — CBAM Import Continuity Desk. Customs brokers and freight forwarders serving SME importers pay for repeated CBAM evidence continuity; event is a covered import flow; broker-first route; accumulating supplier/evidence mappings. Status confirmed.
4. `ideas/CONFIRMED_IDEA_20260511_123619.md` — Data Act Machine Data Liberation Desk. Independent compressed-air service companies and energy auditors pay for access/export support around installed machine data; event is a customer audit or service opportunity; broker-first route; accumulating machine/interface mappings. Status confirmed.
5. `ideas/CONFIRMED_IDEA_20260511_135210.md` — GreenTender EPREL Bid Packs. Lighting distributors/importers pay for product evidence needed in public lighting tenders; event is a tender submission; distributor/tender route; accumulating SKU-to-evidence packs. Status confirmed.
6. `ideas/CONFIRMED_IDEA_20260511_143431.md` — Supplement Stack Safety & Lab-Response Passport. Adults with multiple supplements and recent laboratory results pay for practitioner-reviewed stack/lab response review; event is a review cycle; direct-user/practitioner route; accumulating consented longitudinal records. Status confirmed.
7. `ideas/CONFIRMED_IDEA_20260511_154009.md` — HeatQuiet Noise Risk + Complaint Shield. Heat-pump installers, warranty/distributor channels, property managers, or owners pay around risky outdoor-unit siting or active complaints; event is pre-install siting or complaint resolution; installer/distributor route; accumulating acoustic/site cases. Status confirmed.
8. `ideas/CONFIRMED_IDEA_20260511_163033.md` — BioSignal Claim-Risk Diligence Pack. EU/CEE healthtech investors and programs pay for diligence of wearable and digital-biomarker claims; event is an investment decision; investor/accelerator route; accumulating claim/evidence mappings. Status confirmed.
9. `ideas/CONFIRMED_IDEA_20260511_190013.md` — REDBlocked Amazon Connected-Device Evidence Rescue Desk. Marketplace compliance agencies pay for white-label evidence responses for connected-device sellers; event is an account-health evidence request; agency route; accumulating device/document precedent. Status confirmed.
10. `ideas/CONFIRMED_IDEA_20260511_212329.md` — DORA Bank Renewal Evidence Pack. Software vendors pay for ICT third-party-risk evidence that blocks regulated-finance renewal/procurement; event is a bank evidence request; vendor/security route; accumulating reusable evidence mappings. Status confirmed.
11. `ideas/CONFIRMED_IDEA_20260523_031740.md` — TraceFaktura All-Event Routing Pilot. Polish municipal animal-care contractors pay to route and evidence per-event work; event is each contracted animal-care event; contractor/municipal route; accumulating event evidence and invoice linkage. Status confirmed.
12. `ideas/CONFIRMED_ZERO_TO_ONE_BUSINESS_IDEA.md` — Distributor-backed Heat-Pump Commissioning Passport. Heat-pump distributor/installer channels pay around commissioning and retrofit handoff records; event is a system commissioning; distributor-backed route; accumulating commissioning records. Status confirmed.
13. `ideas/confirmed_85s_club/CONFIRMED_IDEA_20260513_155748.md` — HeritageDoor Suites. Premium renovation buyers pay for complete matched pre-war internal door suites; event is acquisition for a renovation; sourcing through demolition/renovation networks; accumulating controlled matched inventory and provenance. Status confirmed.
14. `ideas/UNCONFIRMED_IDEA_20260512_235132.md` — CarrierProof DPD/DHL Recovery Rail. One Polish ecommerce 3PL would pay for embedded parcel-claims recovery across its merchant base; event is a carrier loss/damage claim; 3PL channel; accumulating claim evidence and recovery patterns. Status unvalidated.
15. `ideas/UNCONFIRMED_IDEA_20260526_083609.md` — BioWear Regulated-Listing Ticket-Book Buyout. A buyer would acquire or option an ecommerce compliance agency ticket book around regulated wearables; event is acquisition plus recurring regulated-listing ticket; agency acquisition route; accumulating customer access, ticket history, and marketplace precedent. Status unvalidated.

## Rejected historical source shapes

Source artifact for every record in this section: `TRIED_IDEAS_AND_FAILURES_BRAIN.md`.

16. Reference phantoms, coupons, fixtures, calibration tiles, artificial media, and repeatable QA rigs sold to wearable, biosignal, robotics, or device developers. Customer loss: uncertain test fidelity or release quality. Payer: engineering/QA labs. Paid trigger: build, test, or release cycle. Route: direct technical sales. Possible asset: test corpus or calibration history. Source shapes include PouchSense, LotBridge, SweatFlux, TonePulse, Interface Matrix, WashWitness, BlindBench, FlexFault, PolyPick, OptiGhost, TactiWear, Haptic Reference Tiles, PAIForge, PulsePhantom Bench. Status rejected.
17. Commodity or custom replacement components for wearables, robotics, PPE, smart garments, research equipment, or discontinued devices. Loss: downtime, incompatibility, or end-of-life supply. Payer: fleet owner, lab, or OEM. Trigger: failure/replacement. Route: direct parts or distributor channel. Possible asset: compatibility library or stocked inventory. Source shapes include DryPin, SmartPod, aftermarket battery rights, Smart-Glasses insert rail, OrphanFinger, TaskSkin, CrashFuse, WashLock, FlexTail, HoloLens Uptime, NeuroPort. Status rejected.
18. Hardware gates, approval terminals, consent beacons, privacy docks, or isolated appliances intended to govern AI/device actions. Loss: unsafe action, recording, or data exposure. Payer: enterprise security/operations. Trigger: consequential action or deployment. Route: security/IT procurement. Possible asset: policy/action records. Source shapes include ActionKey, CommitKey, SpectacleSafe, RoomConsent, AgentCage, Inference Firewall, SmartPPE Privacy Gate. Status rejected.
19. Owned device fleets, matched lots, loaners, swap inventory, or try-before-buy stock. Loss: continuity, uptime, sizing, study compatibility, or migration. Payer: labs, employers, integrators, or users. Trigger: study, failure, fit, or migration. Route: rental/direct/reseller. Possible asset: serialized condition and compatibility history. Source shapes include CohortVault, WearOS Flightcase, StudyContinuity Lots, RingRelay, HapticBridge Poland. Status rejected.
20. Custom assessment, testing, benchmarking, or work-sample services for hiring, AI-assisted operations, or workforce performance. Loss: bad hire or unsafe/ineffective workflow. Payer: employer. Trigger: hire, rollout, requalification, or audit. Route: direct employer sale. Possible asset: performance/outcome dataset. Source shapes include BenchHire Direct, ProofBatch Talent Cell, GownTrace, LedgerTrial, WorkScore Passport. Status rejected.
21. Service-provider or customer-book acquisition combined with an optional technology/data module. Loss: fragmented distribution or renewal access. Payer: acquired clients. Trigger: acquisition and recurring service renewal. Route: seller succession. Possible asset: contracted book, renewal calendar, and cross-sell data. Source shapes include HumanFactor Works. Status rejected.
22. Per-exception, claim, refund, remedy, or bounty recovery rails where an installed platform, employer, carrier, or payer retains the transaction. Loss: denied claim, error, refund, or exception labor. Payer: merchant, employer, vendor, or beneficiary. Trigger: accepted recovery/exception. Route: embedded partner or direct operations. Possible asset: resolution precedents. Source shapes include ExceptionLedger, AgentRemedy Rail, CatchPool AI, parcel recovery variants. Status rejected.
23. Retained-rights human physiological, behavioral, voice, or manipulation datasets. Loss: missing training/validation data. Payer: AI, robotics, media, or device developer. Trigger: collection batch or model cycle. Route: direct technical sales or participant panels. Possible asset: licensed corpus and consent history. Source shapes include Dexterity Rights Foundry, CharacterContinuity Rail, MowaForge-related panels. Status rejected.
24. Direct-user physiological safety, accessibility, self-control, or communication products. Loss: unsafe self-management, inaccessible interaction, or communication failure. Payer: user, stable, employer, or care channel. Trigger: session/use cycle. Route: direct user or sponsor. Possible asset: personalized response history. Source shapes include CueBand Duo, JawKey, TiltLock, StableGuard, SpeechBridge Workline. Status rejected.
25. Scarce-rights or exclusive-media mechanisms attached to venues, equipment, characters, patents, or suppliers. Loss: unavailable distribution/content/resource. Payer: advertiser, buyer, licensee, or integrator. Trigger: campaign, production, or licence. Route: rights acquisition then resale. Possible asset: option/exclusivity portfolio and performance history. Source shapes include GymSignal Media Rail, licensed tactile language, ExoCell, CharacterContinuity Rail. Status rejected.
26. Returns, repair, refurbishment, and diagnostic custody networks. Loss: product downtime, warranty/return cost, or unknown failure. Payer: brand, fleet, or owner. Trigger: return or repair event. Route: brand/repair partner. Possible asset: failure intelligence and custody history. Source shapes include RepairProof, ProbeRevive, PulseReturn Rail, NeuroPort. Status rejected.
27. Compliance, data-portability, or evidence services without a protected channel or mandatory vendor-specific transaction. Loss: blocked market access, regulatory response, or missing evidence. Payer: SME manufacturer/vendor. Trigger: filing, audit, or evidence request. Route: direct compliance sale. Possible asset: evidence mappings. Source shapes include Wearable Data Act Port, PhysioVault, IncidentFreeze, SessionSeal. Status rejected.
28. Service-heavy operational networks whose wealth path depends on many small accounts, repeated manual delivery, or unsupported capture of procurement volume. Loss: missed calls, staffing gaps, route inefficiency, safety process, or maintenance. Payer: SMB/employer/site. Trigger: service event or subscription. Route: cold direct sales. Possible asset: route/customer data. Source shapes include FallbackLine, PAR Rail, HeatReserve CEE and related networks. Status rejected.

## Safety boundary

Do not recommend evasion of law, dumping, deceptive claims, financial misconduct, unauthorized access, or regulated activity without the relevant licensed partner. Do not turn any historical objection into a validator score or decision.
