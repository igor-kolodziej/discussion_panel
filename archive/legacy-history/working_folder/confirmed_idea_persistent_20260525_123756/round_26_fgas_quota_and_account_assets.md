# Round 26: F-Gas Quota, Authorisation, And Account-Control Assets

Created: 2026-05-25

## Pivot Rationale

Round 24 showed that physical F-gas/refrigerant stock and technician capacity are too copyable by incumbents. The harder asset is not the cylinder; it is the legal right to place HFCs or HFC-containing equipment on the EU market.

Round 26 therefore targets the **F-gas Portal legal-use layer**:

- quota transfers for bulk HFCs;
- authorisations/delegations for pre-charged equipment imports;
- reference-value holder account options;
- verified reporting/admin roles.

## Source Anchors

- The European Commission's F-gas Portal page says the portal manages HFC quotas, authorisations, import/export licensing, and reporting. Transactions such as transferring and authorising quotas must take place in the F-gas Portal, and the portal is connected to customs enforcement: https://climate.ec.europa.eu/eu-action/fluorinated-greenhouse-gases/f-gas-portal_en
- Commission quota-transfer guidance says only producers/importers assigned a reference value can transfer quota allocation; both grantor and beneficiary need valid F-gas Portal registration; transfers are valid only if accepted through the Portal; transferred quota cannot be transferred a second time: https://climate.ec.europa.eu/document/download/5a2e2f6b-02ac-459f-8677-55d3f61ea8f4_en?filename=policy_f-gas_guidance_quota_transfer_f-gas_portal_en.pdf
- Commission F-gas FAQ says quota is required for placing bulk HFCs on the EU market and can be obtained by acquiring it from a quota holder with a reference value; the F-gas Portal matchmaking tool can help contact holders: https://climate.ec.europa.eu/eu-action/fluorinated-greenhouse-gases/faq_en
- The same FAQ says quota authorisations are required for importing pre-charged HFC equipment/products, can be acquired from quota holders only, are not time-bound until used, and delegations occur only in the F-gas Portal: https://climate.ec.europa.eu/eu-action/fluorinated-greenhouse-gases/faq_en
- Commission bulk-HFC obligations say new entrant bulk HFC importers without reference value can no longer authorise quota to equipment importers; reference values are tied to historical placing on the market, and 2026 quota has a mandatory payment of EUR 3/tCO2e: https://climate.ec.europa.eu/eu-action/fluorinated-greenhouse-gases/stakeholder-obligations/f-gases-bulk_en
- The Commission monitors HFC quota-authorisation prices; a 2025 report found quota authorisation purchase prices around the mid-teens EUR/tCO2e, confirming a private economic market exists: https://climate.ec.europa.eu/document/download/91b240c3-013d-4076-8375-64343d220bb8_en?filename=Price+monitoring+Q2_2025.pdf

## Candidate Set

| # | Candidate | Buyer | Acute trigger | Control point | 2-month proof | First acquisition mechanism | Gross margin / payback logic | Copy risk |
|---:|---|---|---|---|---|---|---|---|
| 1 | F-Gas Quota Transfer Lockbox | EU/Polish bulk HFC importers, refrigerant distributors, chemical traders | Importer cannot release/place bulk HFCs without quota; new quota declarations are periodic and 2026 allocation is paid/limited | Exclusive option over named 2026 quota from a reference-value holder, buyer acceptance route in F-gas Portal, escrowed commercial contract | Secure one quota-holder option for 1,000-5,000 tCO2e and one buyer deposit/accepted portal transfer path | F-gas Portal matchmaking, small EU importers with unused quota, HVAC/refrigerant distributors | Spread/success fee per tCO2e; deposit-funded, no inventory; buyer pays because customs/market placement is blocked | Medium: portal matchmaking exists, but optioned quota is locked and cannot be re-transferred after use |
| 2 | F-Gas Authorisation Wallet For Pre-Charged Equipment Importers | Importers of heat pumps, AC units, refrigeration equipment, MDIs with HFCs | Importer needs authorisation/delegation to import pre-charged HFC equipment/products | Exclusive option over quota-holder authorisations/delegations plus buyer-side F-gas registration/admin handoff | Sign one quota-holder authorisation option and one equipment importer paid deposit for a named shipment | Equipment importers, customs brokers, quota holders with reference values | Margin on authorisation spread; high urgency when shipment is held or production order is blocked | Medium: quota holders can sell direct, but buyer admin and shipment timing create transaction custody |
| 3 | F-Gas Reference-Value Holder Micro-Acquisition | Refrigerant distributors, equipment importers, chemical traders | Reference-value holder status and historical allocation cannot be recreated quickly by new entrants | Option/acquire shares of a small EU/Polish company with reference value, F-gas Portal registration, clean reports, and 2026 quota/account history | Sign LOI/option on one clean micro-holder and obtain one written buyer bid for its quota/account utility | Retiring refrigerant importers, dormant chemical traders, accountants, F-gas consultants | Asset resale or annual quota monetization; stronger control than brokerage | Medium-low if clean holder found; high diligence and liability risk |
| 4 | F-Gas Portal Reporting/Auditor Slot Desk | Importers/producers above verification/reporting thresholds | Annual reporting/verification deadlines and F-gas Portal registration burden | Reserved registered auditor/reporting capacity plus delegated admin custody over reporting files | Reserve 3 auditor slots and sell 5 reporting packages | F-gas consultants, auditors, small importers | Fixed fee; low capex | High: compliance service, likely capped |
| 5 | F-Gas Customs Release Rescue For Held Shipments | Importers/customs brokers with HFC or pre-charged equipment held by customs | Shipment lacks F-gas Portal registration/quota/authorisation data | Triangular rescue: buyer mandate, quota/authorisation seller option, customs broker release workflow | One held shipment cleared or buyer pays success fee after accepted transfer/authorisation | Customs brokers, port forwarders, HVAC importers | Success fee from avoided demurrage/rejection | Medium-high: urgent but case-specific; broker can copy |
| 6 | F-Gas Illegal-Supply Replacement Desk | Cold-chain/HVAC buyers offered suspect gas | Buyers need legal replacement source and proof because illegal HFC trade enforcement risk is rising | Pre-vetted legal quota/stock supplier list plus buyer custody over compliant procurement file | One buyer switches from suspect supplier to legal quota-backed purchase | HVAC contractors, cold stores, distributors | Procurement spread or audit fee | High: closer to compliance/procurement service |

## Initial Read Before Scoring

The only candidates that may clear simulated `>87` are:

1. **F-Gas Quota Transfer Lockbox** because the asset is explicitly transferable in the official portal, cannot be recreated by a simple workshop/technician relationship, and directly gates market placement.
2. **F-Gas Reference-Value Holder Micro-Acquisition** because reference value and quota history are grandfathered assets, but acquisition diligence and liability may make it too slow.

