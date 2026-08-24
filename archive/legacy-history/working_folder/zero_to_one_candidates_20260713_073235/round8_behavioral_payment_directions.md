# Round 8 — Behavioral Payment and Precommitment Directions

Candidate generation only — not validated. This branch does not score, evaluate, pivot, panel, or confirm ideas.

## Search Thesis

The behavioral insight is real: people and SMEs often do not want more advice after a decision. They want a prior decision to remain binding when temptation, urgency, scope creep, fear or a counterparty's pressure arrives. A commercially useful product must therefore control the actual payment, reserve, deposit or release—not merely send an alert.

This search applied five non-negotiable filters:

1. the paying user or SME directly controls the action being bound;
2. a specific payment/licence route is contractable inside 12 months and 100,000 PLN;
3. paid proof is obtainable inside 180 days and 40,000 PLN while the founder remains employed;
4. the wealth bridge starts from a counted transaction population rather than a broad market value; and
5. the product is rejected if a bank, card issuer, PSP, insurer or counterparty must voluntarily create the missing control, or if an incumbent can reproduce it as one feature.

## Current Payment-Rail Facts

- A Polish small payment institution (MIP) requires KNF registration rather than a full licence. KNF states that a complete application should be entered within three months. An MIP can run payment accounts, transfers, cards/payment instruments, acquiring and money remittance, but cannot provide payment initiation or account-information services. It operates only in Poland, cannot exceed an average €1.5m monthly payment volume, and may hold no more than €2,000 for one user on a payment account. It also needs AML/risk procedures and safeguarded client funds. This is a real bootstrap route, but not a magic route for high-value escrow or open-banking enforcement. [KNF registration](https://www.knf.gov.pl/dla_rynku/procesy_licencyjne/platniczy/MIP/Rejestracja_MIP?articleId=62946&p_id=18), [scope and limits](https://www.knf.gov.pl/dla_rynku/procesy_licencyjne/platniczy/MIP/Dzialalnosc_MIP), [obligations](https://www.knf.gov.pl/dla_rynku/procesy_licencyjne/platniczy/MIP/Podstawowe_obowiazki_MIP)
- A Polish KIP may operate through registered agents, but the agent route begins with a written agreement with an already licensed institution; KNF registration does not force any KIP to accept a startup. [KNF KIP agent rules](https://www.knf.gov.pl/dla_rynku/procesy_licencyjne/platniczy/krajowe_instytucje_platnicze/formy_dzialalnosci)
- Lemonway publishes a B2C marketplace flow in which a consumer pays, the professional seller completes KYB, the regulated PSP safeguards funds, and the platform can hold before payout and control release. Mangopay similarly exposes licensed EMI wallets and third-party marketplace payment flows. These are exact contractable product categories, but production access, underwriting, pricing and use-case acceptance remain discretionary until signed. [Lemonway B2C marketplace](https://documentation.lemonway.com/docs/b2c-marketplacelanding), [Mangopay wallet system](https://docs.mangopay.com/guides/e-wallet-system)
- BGK offers a multi-party escrow account for SMEs and public entities with bank-controlled release conditions. It proves that conditional payment can be purchased for a named B2B transaction, but it does not give a software startup ownership of the payment relationship. [BGK escrow](https://www.bgk.pl/produkty/rachunek-zastrzezony-escrow/)
- Stripe Issuing is available in Poland and provides category, merchant, country, per-transaction and monthly spending controls plus real-time authorization. Cards and program terms remain subject to bank/program approval. The same published capabilities make generic “controlled spend card” ideas easy for incumbents to reproduce. [Stripe availability](https://docs.stripe.com/issuing/global), [spending controls](https://docs.stripe.com/issuing/controls/spending-controls)

## Direction 1 — StakeLine Gambling-Budget Wallet

### Customer point of view

A recreational bettor does not necessarily want permanent abstinence. They want one monthly loss budget that covers every legal operator and cannot be raised during tilt. Operator-by-operator limits are easy to reset or bypass; ordinary bank blocks are all-or-nothing and do not provide a controlled allowance.

### Proposed binding mechanism

The customer prepays a monthly allowance to a dedicated card account. The card works only at legal gambling MCCs, declines after the allowance is consumed, and imposes a 7-day cooling-off period on limit increases. Payouts are swept to a non-gambling bank account and cannot replenish the monthly loss allowance until the next period.

### Payment/control route

An MIP could in principle issue a payment instrument and hold less than €2,000 per customer, or an EMI/BIN sponsor could provide the account and card. Enfuce explicitly advertises BIN sponsorship, gambling-category restrictions and real-time card controls; Stripe also exposes the required controls. Neither source promises consumer gambling-program acceptance to an unknown Polish startup. More importantly, the wallet cannot stop the same user from funding a bookmaker from another bank card or transfer. Binding control would therefore require every other bank/operator to cooperate or the customer to self-enforce exclusivity.

### Current competition and copy test

Revolut already blocks gambling MCC card payments and imposes up to a 48-hour delay when the block is disabled. Starling publishes the same cooling-off behavior. Polish online betting operators must operate responsible-gambling rules. The proposed adjustable budget is narrower than a total block, but it is still a card-control feature using infrastructure already exposed by issuing vendors. [Revolut gambling block](https://help.revolut.com/en-DE/help/profile-and-plan/security-and-personal-data/gambling-block/what-is-gambling-block/), [Starling gambling block](https://help.starlingbank.com/business/topics/debit-card-queries/how-do-i-block-gambling-payments/), [Polish responsible-gambling requirement](https://www.podatki.gov.pl/media/10637/podstawowe-informacje-na-temat-zezwolenia-na-urz%C4%85dzanie-zak%C5%82ad%C3%B3w-wzajemnych-aktualizacja-luty-2025.pdf)

### Counted denominator and wealth screen

The Ministry maintains a list of legal operators, but no official source found in this branch provides the counted annual population of Polish users who use several operators, want a non-zero cross-operator cap, will route all gambling payments through a new card, and will pay a subscription. A wealth case at roughly €60 annual revenue and 25% operating margin needs about 200,000 paying users to create a €10m-plus founder-equity path at ordinary software/payment multiples and retained ownership. That user count is an unsupported behavior denominator, not a conservative share calculation.

### 180-day proof

A waitlist or paid subscription would not prove the binding product. Proof requires a signed issuing/EMI program approval plus live declines across legal gambling merchants, and still would not control external cards or transfers. That existential dependency cannot be cleared by consumer deposits alone inside 40,000 PLN.

### Generation decision

**Rejected.** The key promise—one binding cross-operator budget—is not controlled by the startup. Revolut/Starling already demonstrate the feature-copy risk, while alternative funding rails defeat enforcement.

## Direction 2 — RetrofitVault Milestone Escrow

### Customer point of view

A homeowner fears paying a large deposit to an installer who may disappear, substitute materials or leave the job unfinished. A credible installer fears performing work for a homeowner who later withholds payment. Both want committed funds with staged release, but neither wants the other side to hold unilateral power.

### Proposed binding mechanism

The homeowner funds agreed milestones into a regulated wallet. The installer sees irrevocably committed money; each milestone releases after a time-boxed homeowner approval. A dispute freezes only the contested milestone. The Polish wedge would use fixed heat-pump, insulation and PV/battery milestone templates, including serial numbers, commissioning evidence and subsidy/co-payment separation.

### Payment/control route

Lemonway's published B2C marketplace model exactly matches an individual buyer, professional seller, safeguarded funds and platform-controlled payout. Mangopay is a second licensed-wallet route. The founder's family installation company can provide one willing installer without a speculative partnership, but the PSP must still sign the production platform before customer money moves. An MIP is a poor substitute because a normal project milestone exceeds its €2,000 per-user payment-account ceiling. BGK escrow can prove a named B2B transaction, but its published target and multi-party bank contract do not establish a repeat consumer platform.

### Counted denominator and momentum

NFOŚiGW reports 103,882 buildings with improved energy efficiency in 2025 and 53,594 contracts in the program version running from 31 March 2025 through 3 July 2026. It also reports 6,000 suspect subsidy applications worth about 600m PLN in a fraud review. This is a real, counted Polish transaction population and a trust problem. [Clean Air statistics](https://czystepowietrze.gov.pl/efekty-programu/czyste-powietrze-w-liczbach), [reported abuse](https://czystepowietrze.gov.pl/wazne-komunikaty/naduzycia-w-ppcp)

The program already routes up to 35% prefinancing directly to contractors, requires signed contractor agreements, and uses public operators for higher-support cases. A private wallet can control only the homeowner-funded part; it cannot redirect or condition the public subsidy payment without institutional integration. [Official prefinancing rules](https://czystepowietrze.gov.pl/wez-dofinansowanie/zloz-wniosek/dotacja-z-prefinansowaniem)

### Wealth screen

A paper conservative bridge at a 2% fee requires about 35,000 annual projects at €18,000 average routed value to produce €12.6m revenue. At 20% operating margin, a 6x operating-profit value and roughly 70% founder ownership, founder equity can exceed €10m. The arithmetic is possible, but 35,000 annual projects would mean capturing roughly one-third of the counted Polish annual Clean Air completions or building a multi-country installer network. Country-by-country consumer, payment and renovation rules reset, so this is not yet a non-heroic distribution case.

### 180-day proof

For <=35,000 PLN the founder can obtain a written payment/legal opinion, request two PSP production proposals, build a non-custodial milestone prototype, and charge three unrelated homeowner/installer pairs a 500–1,000 PLN conditional pilot fee. A family-company project may be the first transaction, but at least two unrelated installers are required before calling the channel independent. No customer funds should be held until the licensed PSP signs.

### Current competition and copy test

Renopay, Renno, Revlend and other current products already market regulated or holding-account milestone payments for home renovation; Renno publicly uses a 2% example fee and says European expansion is planned. The Polish subsidy templates and family-company wedge improve reachability, but not the business shape. A foreign product can localize the same workflow through the same PSP. [Renopay](https://www.renopay.co.uk/), [Renno](https://www.renno.pro/?page=homeowner), [Revlend](https://www.revlend.co/)

### Generation decision

**Rejected.** Reachable proof and a counted denominator exist, but the exact milestone-escrow product already exists, the public subsidy payment remains outside startup control, and the wealth path requires a large multi-party installer network with no durable local barrier.

## Direction 3 — WarrantyRetain Funded Workmanship Reserve

### Customer point of view

Milestone escrow protects the homeowner before and during work, then disappears immediately after final release—precisely when latent installation defects begin to appear. A small installer may offer a written warranty but can delay, dispute or become insolvent. The customer wants proof that some money remains available, while a good installer wants a credible signal that distinguishes it from cash-only competitors.

### Proposed binding mechanism

At final payment, the installer contractually routes 5% into a 12-month safeguarded reserve. The reserve is visible to the homeowner and releases automatically if no documented claim exists. A claim freezes the specific reserve; pre-agreed independent inspection or ordinary legal resolution determines release. The installer, not an insurer, funds the promise.

### Payment/control route

A Lemonway/Mangopay professional-seller wallet could retain a share of routed project proceeds. This route is contractable in category, but exact 12-month holding, claim handling and reserve ownership require written PSP approval. MIP's €2,000 per-user account ceiling may fit a single small reserve but becomes restrictive across an installer's concurrent projects. No insurer is needed for the first version, but the platform then bears operational and legal complexity around conflicting claims without providing insurance-grade protection.

### Counted denominator and wealth screen

The same 103,882 Polish energy-renovation completions form a counted top-of-funnel, but there is no count of contractors or customers willing to lock 5% for a year. At €200–250 platform revenue per protected project, 50,000–60,000 annual projects are required for a credible €10m founder-equity bridge under ordinary 20–25% operating margins and retained ownership. That is about half the entire counted Polish annual Clean Air completion flow before filtering for willingness, and country expansion resets warranty law and dispute operations.

### 180-day proof

The family installer could route a reserve for one project, and three independent contractors could pay a setup fee or sign funded-reserve clauses inside 180 days for <=30,000 PLN. This proves willingness only if actual cash is safeguarded by an approved PSP. It does not prove claim economics or contractor retention until at least one full reserve cycle passes.

### Copy and dependency test

Renovation escrow providers can add post-completion retainage as one payout setting. Banks already support conditional escrow agreements, and insurers/bond providers offer stronger risk transfer. The startup's claim workflow does not compound fast enough to overcome those substitutes; each disputed defect still requires costly human/technical judgment.

### Generation decision

**Rejected.** The payer can directly fund the reserve and a pilot is reachable, but wealth requires heroic adoption, disputes scale with revenue, and existing escrow providers can add retainage as one feature.

## Direction 4 — MachineGate FAT/SAT Payment Rail

### Customer point of view

A Polish SME buying a custom machine fears paying large advances before factory acceptance testing (FAT), shipment and site acceptance testing (SAT). The machine builder fears building bespoke equipment for a buyer who later delays acceptance or payment. Both already negotiate milestones, but enforce them through contracts, bank guarantees and manual evidence.

### Proposed binding mechanism

The buyer commits milestone funds to a named escrow; the machine builder receives automatic release on signed FAT, bill of lading and signed SAT evidence, with change orders requiring dual consent. The platform charges per transaction and owns the evidence/release workflow rather than selling a generic project dashboard.

### Payment/control route

BGK's escrow account is a current named-transaction route for SMEs and can control release conditions. Lemonway/Mangopay publish B2B marketplace/payment infrastructure that could later standardize the flow. A first paid project can therefore use bank escrow without the founder holding money. However, the bank owns the actual account and payment control; the startup initially owns only the template and evidence layer unless a PSP platform agreement is signed.

### Counted denominator and wealth screen

GUS reports 87.1bn PLN of non-financial-enterprise capital expenditure in the first half of 2025 and says 76.4% of surveyed enterprises invested; Eurostat PRODCOM records physical volumes and sold values by machinery product. These are useful market values/production counts, but they do **not** count annual Polish/EU custom-machine purchases with staged FAT/SAT payment pain and willingness to use third-party escrow. [GUS investment data](https://ssgk.stat.gov.pl/08.2025/Nak%C5%82ady_inwestycyjne_przedsi%C4%99biorstw_niefinansowych.html), [Eurostat PRODCOM methodology](https://ec.europa.eu/eurostat/cache/metadata/EN/prom_esms.htm)

At a 1% fee on an assumed €250,000 average transaction, approximately 3,600–4,000 annual projects are needed for a founder-wealth bridge after realistic operating margin, valuation and ownership assumptions. Because the eligible transaction count is absent and sales/acceptance are high-touch, that volume cannot be called conservative.

### 180-day proof

Two unrelated machinery buyers could pay 5,000–10,000 PLN setup fees for bank-escrow milestone design inside 180 days and 40,000 PLN. This is reachable alongside employment, but initially resembles transaction consulting. Turning it into owned payment flow requires the additional PSP contract, while disputes still depend on buyer/seller or a costly technical expert.

### Competition and copy test

General B2B escrow platforms already advertise milestone protection for custom manufacturing, equipment and inspection-gated supplier payments. A bank or PSP can reproduce evidence-gated release without a scarce founder asset. [Yala supplier escrow](https://www.useyala.com/product/escrow), [TrustProtect custom manufacturing](https://trustprotect.fr/en/unknown-supplier), [Paynco white-label escrow](https://paynco.com/)

### Generation decision

**Rejected.** Paid proof is reachable, but the branch lacks a counted eligible transaction denominator, initial control belongs to the bank, human acceptance disputes scale, and white-label/general escrow providers already expose the core mechanism.

## Direction 5 — TaxLock SME Revenue Reserve

### Customer point of view

A Polish sole proprietor knows that incoming cash is not all spendable cash. The painful failure is not forecasting; it is spending VAT, PIT or ZUS money during a strong month and discovering the shortage at the due date. The desired product would make the reserve unavailable for ordinary spending while remaining usable for named public obligations.

### Proposed binding mechanism

Customer invoice payments enter a controlled account, an invoicing rule immediately routes VAT and an estimated income/social contribution share to locked pockets, and only tax/ZUS beneficiaries can receive those funds. Increases are immediate; reductions require a cooling-off period or accountant co-approval.

### Payment/control route

MIP registration is a direct Polish route for transfers, accounts and payment instruments, but the €2,000 per-user balance ceiling is too low for many SME tax reserves and MIP cannot use open-banking payment initiation/account-information powers. A KIP/EMI agent contract could lift these constraints, but no institution is required to accept the startup. If customer invoices continue entering their normal bank, the startup cannot bind the reserve.

### Existing statutory control and copy test

Poland's split-payment mechanism already routes the VAT portion of qualifying B2B payments to a special VAT account automatically opened by the bank. Those funds can be used for enumerated taxes and ZUS payments. The e-Tax Office and tax micro-account already provide official payment endpoints. A commercial product may improve PIT/ZUS estimation, but the binding VAT control is statutory and bank-owned; banks/accounting platforms can add the remaining reserve rules. [Official split-payment mechanism](https://www.podatki.gov.pl/podatki-firmowe/vat/poradniki-i-informatory/mechanizm-podzielonej-platnosci-mpp), [VAT-account permitted uses](https://podatki.gov.pl/e-urzad-skarbowy/konto-organizacji/zawiadomienie-zaw-nr), [tax micro-account](https://www.podatki.gov.pl/mikrorachunek-podatkowy)

### Counted denominator and wealth screen

The regulations cover Polish business payments broadly, but this branch found no counted annual population of firms that repeatedly under-reserve non-VAT obligations, will reroute all invoice receipts to a new payment provider and pay enough to support a large company. A plausible software/payment wealth bridge would require roughly 150,000–250,000 paying SMEs at €60–100 annual revenue under ordinary margins and founder ownership. That is an unsupported adoption count, while the statutory VAT account already solves the most enforceable portion at no separate startup fee.

### 180-day proof

The founder could sell a paid cash-flow setup or collect deposits for an account, but that would not prove binding control. A live proof requires completed MIP registration plus a bank safeguarding/transfer account, or a signed KIP/EMI agent agreement. The MIP balance limit then prevents the intended reserve for many customers. The exact product cannot reach representative paid proof inside the cap without changing the control promise.

### Generation decision

**Rejected.** The binding resource is either too small under MIP, controlled by a hoped-for KIP/EMI partner, or already implemented through the statutory bank VAT account. The remainder is an easy bank/accounting feature.

## Branch Conclusion

**No direction from this five-idea behavioral-payment branch qualifies as a finalist.**

The recurring failure is structural, not presentational:

- a gambling cap does not bind other funding rails;
- consumer and B2B escrow require both sides and a discretionary licensed-platform agreement;
- retainage adds human disputes without enough revenue density;
- equipment escrow lacks a counted eligible transaction population and begins as bank-owned consulting; and
- tax locking is constrained by MIP limits and pre-empted by statutory/bank infrastructure.

The useful discovery is narrower: behavioral precommitment can become a control point only when the founder already owns or can directly register the account/instrument **and** the target behavior occurs entirely inside that rail. For high-value, multi-party or cross-account behavior, a user preference is not enough. Future generator work should not revisit these shapes without an already signed issuer/PSP contract, an exclusive distribution rail, or a statutory/contractual requirement that forces the relevant transaction through the startup.

Candidate generation only — not validated.
