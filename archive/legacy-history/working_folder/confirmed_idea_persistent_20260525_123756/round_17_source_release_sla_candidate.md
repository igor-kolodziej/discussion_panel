# Round 17 Source-Release And First-Call Restore SLA Candidate

Created: 2026-05-25

## Candidate

### PLC Source-Release & First-Call Restore Exchange

This is a tightened version of the Round 16 near miss. It is not a backup service, an inventory shop, or an automation integrator. It is a transaction rail for releasing, verifying, and escrowing production-control source projects when a small automation integrator, machine builder, or controls technician is retiring, closing, or no longer able to support old customers.

## Buyer

Polish SME factories running older PLC/HMI/SCADA-controlled machines, especially food, packaging, furniture, plastics, metalworking, and local process plants.

## Acute Trigger

- Siemens S7-300/ET200M phase-out and migration planning.
- A production line depends on an old S7/WinCC/Omron/Allen-Bradley project whose editable source is on a retired engineer's laptop.
- PLC upload will not recover full comments/symbols/HMI source or a clean migration package.
- Ransomware, laptop failure, memory-card failure, HMI failure, or migration vendor quote exposes that the factory does not control its own restore state.

## Primary Control Point

A signed tri-party source-release and first-call restore packet:

1. The retiring integrator signs an exclusive 90-day release mandate covering named installations, source-project inventory, emergency phone/domain routing, seller intro, transition support, non-solicit, and earnout.
2. The factory signs customer authorization and pays a source-release/escrow deposit.
3. The company takes encrypted custody of verified source projects, VMs/images, checksums, hardware maps, restore notes, passwords only where lawful, license/dongle register, and emergency contact tree.
4. The factory signs a 12-month first-call restore SLA for the named line or machine.
5. Optional exact-SKU spare procurement is attached only after source/control custody is secured.

## Two-Month Proof Under 100,000 PLN

- Sign 2 exclusive integrator or machine-builder release mandates covering 20-60 named installations.
- Get 5 factories to pay 2,000-8,000 PLN source-release/escrow deposits.
- Verify 3 projects open in the correct STEP7/TIA/WinCC/Omron/other environment with contractor evidence.
- Build 2 complete restore packs with checksum/custody logs, hardware map, VM/software version notes, and access-status map.
- Run 1 customer-observed restore drill or migration-readiness dry run.
- Sign 2 factories to 12-month first-call restore SLAs at 500-1,500 PLN/month.

## Why This Is Stronger Than Round 16

Round 16 looked like source backup plus escrow, which automation firms can copy. This round makes the commercial control point the signed source-release transaction and first-call restore SLA. The founder is not asking factories to trust a stranger with random files; the retiring integrator introduces the customer, the customer authorizes custody, and the buyer pays because the source package becomes a verified operational asset.

## Initial Scoring Hypothesis

This may clear simulated `>87` if the evaluators treat the tri-party release mandate plus first-call SLA as a hard transaction-control point rather than a service workflow. It should still fail if they believe existing automation firms can copy the whole shape with one retiring-integrator contract.
