# Round 12 Transaction-Custody Candidate Funnel

Created: 2026-05-25

Round 11 failed because option/title/data rights were still copyable by incumbents with better trust. Round 12 starts from payment, refund, withdrawal, delivery, slot, or escrow custody: the startup must sit in a live transaction path and generate evidence before building software.

## Candidate Set

| # | Candidate | Buyer | Acute trigger | Control point | 60-day proof | First acquisition | Economics | Main copy risk |
|---:|---|---|---|---|---|---|---|---|
| 1 | CODCommit Failed-Delivery Payment Custody | Polish e-commerce sellers with cash-on-delivery / pay-at-pickup failure | Customer did not collect COD parcel; seller faces return cost, dead inventory, wasted courier fee | Merchant routes failed COD orders to startup; customer must pay a small non-refundable redelivery/reservation deposit or convert to prepaid order through startup link before second shipment | 5 merchants, 1,000 failed COD/uncollected orders, 150 recovered with prepaid custody, contribution margin proven | Scrape Allegro/Shopify/Woo stores offering COD; seller forums; cold email with no-integration CSV test | 5-12 PLN per rescued order + 5-10% success fee; SMS/payment cost low; payback immediate | SMS/payment/shipping apps add feature; merchants internalize |
| 2 | WithdrawButton State-Router | EU-facing Shopify/Woo/Magento stores hit by 2026-06-19 withdrawal-button duty | Deadline within weeks; stores need not only a button but order-state/refund/email proof | Store delegates withdrawal endpoint, timestamped receipt, refund-state routing and evidence log to startup | 20 paid stores before deadline, live withdrawal endpoint, 200 test/real withdrawals logged | Reddit/e-commerce dev communities and agency outreach | 299-999 EUR setup + subscription; fast cash | Ecommerce platforms/agencies add plugin |
| 3 | SlotEscrow For Custom Manufacturing | Buyers and small manufacturers of custom metalwork/furniture/signage/CNC | Buyers distrust prepayment; manufacturers need deposits to reserve production | Startup holds buyer deposit and releases by photo/document milestone; supplier gets credible commitment | 10 suppliers, 30 escrowed orders, 1.5-4% fee, no chargebacks | Supplier marketplaces/Polish workshops | High GMV fee, low capital | Payment providers, marketplaces, contract templates |
| 4 | AllegroParts Border Proxy Escrow | EU classic-car/motorcycle/industrial hobby buyers outside Poland | Polish Allegro/OLX sellers do not ship abroad; buyer distrusts transfer | Startup buys domestically, inspects, holds item/title, forwards internationally after buyer payment | 50 transactions, 5k-50k PLN GMV, low dispute rate | Reddit car forums, eBay price arbitrage, SEO | 10-20% fee on high-value parts | Parcel forwarders/proxies |
| 5 | RentSafe Expat Deposit Escrow + Viewing Custody | Incoming foreign tenants/employers | Landlord wants deposit before tenant arrives; tenant fears scam | Startup verifies ownership/viewing and holds deposit until contract/key handoff | 20 escrows, 5 employer/relocation channels | Expat Reddit/Facebook and employers | 300-1000 PLN per transaction | Agencies/legal escrows |
| 6 | PayeeProof Polish VoP Benchmark And Pre-Check | PSPs, fintechs, accounting/payment platforms | SEPA instant Verification of Payee deadline 2027; Polish names/NIP variants cause false positives | Startup owns a rights-cleared benchmark plus API pre-check using consented accounting payment mismatch logs and synthetic edge cases | 2 paid fintech/accounting pilots, 10k named edge cases, false-positive report | Accounting offices and small PSPs | High-margin data/API | PSP vendors build own |

## Best Candidate Before Scoring

**CODCommit Failed-Delivery Payment Custody** has the clearest transaction control and shortest payback:

- The buyer is not buying software or advice; the seller has an already-failed order and lost cash.
- The startup can prove control with a CSV and payment links before integrations.
- The consumer action is small and behavior-changing: a 10-30 PLN redelivery/reservation deposit or conversion to prepaid filters unserious COD buyers.
- The first acquisition mechanism is concrete: target sellers visibly offering COD and complain threads about uncollected parcels; offer a no-integration rescue of recent failed COD orders.
- It does not require carrier partnerships; the merchant retains its courier process, while the startup controls only the commitment/payment step before reshipment.

## Source Anchors

- InPost explains COD as payment at pickup/delivery and explicitly offers COD services in Poland, including through Allegro-related services.
- Polish e-commerce community threads discuss the cost of uncollected parcels and return-to-sender handling for sellers.
- Poczta Polska has warned about unsolicited COD parcels, confirming COD remains a known fraud/commitment problem category.
- Allegro/InPost pages show returns, uncollected parcels, and COD are operationally real in Polish marketplace logistics.
- Reddit/e-commerce discussions repeatedly frame failed delivery and COD as a commitment, fraud, or final-mile blind spot.
