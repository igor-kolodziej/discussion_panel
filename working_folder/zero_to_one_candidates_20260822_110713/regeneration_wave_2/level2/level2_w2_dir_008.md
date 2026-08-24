# W2-L2-008 — Employer-funded expiring appointment capacity

**Agent:** `live-w2-level2-008`  
**Concept:** `W2-IAT-08`  
**Research timestamp:** 2026-08-22 14:58:54 CEST (+0200)  
**Research budget used:** exactly 8 distinct web queries; 8 source-open attempts, of which 6 returned usable content and 2 were technically inaccessible. No files were edited.

## 1. Transaction

The entrant purchases short-dated options on independent providers’ otherwise perishable appointment slots, then sells prepaid packs of same-week appointment credits to employers. Employees voluntarily claim credits and choose among eligible providers.

A practical initial product:

- Employer prepays **2,100 PLN net** for ten credits valid for 30 days.
- Activating a credit exposes appointments occurring in the next seven days.
- Provider receives a **10 PLN option fee per reserved slot** and approximately **123–128 PLN additional payment** when an employee attends.
- The provider may resell an unexercised slot after the contractual release time.
- If the entrant cannot supply a qualifying appointment, it restores or refunds the credit.
- Employee no-shows can consume a credit only under prominent, accepted terms.
- Provider controls assessment, consent, treatment, clinical documentation and whether service is appropriate.
- Employer receives invoices and aggregate utilization only—never symptoms, diagnoses, treatment details or provider notes.

This is a three-contract structure: provider capacity agreement, employer credit-pack agreement, and employee booking/privacy terms.

## 2. Problem and payer evidence

### Verified evidence

Polish employees insured through ZUS generated **42.4 million days of absence from musculoskeletal and connective-tissue conditions in 2025**, representing **17.5%** of sickness-absence days due to an insured person’s own illness. This establishes a large underlying burden, but does not establish that physiotherapy credits reduce absence or that employers will pay for them. [ZUS 2025 sickness-absence report](https://www.zus.pl/documents/10182/39590/Raport%2BAbsencja%2Bchorobowa%2Bw%2B2025%2Broku.pdf/b2b8893f-049d-0782-1787-415168d381b3?t=1775560395351)

A Warsaw provider’s April 2026 price list shows:

- 60-minute first physiotherapy/manual-therapy visit: **200 PLN**
- 45-minute subsequent visit: **180 PLN**
- 30-minute peripheral-joint manual therapy: **140 PLN**
- 60-minute home visit: **250 PLN**

This supports a retail price anchor around 180–200 PLN for ordinary clinic appointments. It does not establish provider willingness to wholesale empty capacity at 128–138 PLN. [Osteomedis price list](https://osteomedis.pl/cennik/)

PZU’s current individual Premium package costs **5,433 PLN per year** and includes 30 rehabilitation procedures plus broad medical services. It is not an employer price and the rehabilitation procedures are not necessarily equivalent to 30 individual physiotherapy visits, but it demonstrates a route around the entrant: employers or employees can purchase integrated annual medical packages. [PZU Zdrowie packages](https://zdrowie.pzu.pl/sklep/pakiety-medyczne?cid=blog-banner)

The supplied packet reports that Booksy charges **145 PLN net monthly**, **35 PLN per additional user**, and an optional Boost fee equal to **45% net of a completed first visit** from an acquired customer. That supports providers’ willingness to pay for booking and acquisition, but not willingness to sign capacity options. [Booksy Biz pricing](https://biz.booksy.com/pl-pl/cennik)

### Interpretation

The employer’s possible economic benefit per redeemed credit is:

> avoided absence hours × loaded hourly employment cost  
> + reduced employee search/waiting time  
> + retention or benefit value  
> − credit price  
> − associated payroll tax and contribution cost

No source in this packet supports a causal claim that a visit avoids a particular number of absence hours. Sales materials should therefore promise access to reserved capacity, not medical outcomes or absence reduction.

The provider’s incentive is incremental income on a slot likely to expire. Its counter-incentives are price dilution, cannibalization of full-price demand, administrative work, employee no-shows and fear that employers or the entrant will interfere with care.

## 3. Payer denominator

The intended payer unit is an **employer site with roughly 20–249 employees located within a practical journey of a provider cluster**, rather than every registered company.

The Warsaw statistical search result reported that entities declaring **10–49 workers represented 2.2%** of registered entities and entities above 49 workers represented **0.5%**. Thus, a preliminary top-of-funnel proxy is **2.7% of Warsaw REGON entities**, before removing:

- inactive or non-employing registrations;
- entities above the desired size;
- public bodies and other slow-procurement organizations;
- employers already offering adequate rehabilitation access;
- sites without enough employees near a provider cluster;
- employers whose payroll treatment makes a 200 PLN credit unattractive.

The underlying GUS PDF could not be extracted during the capped source session, so an exact absolute employer count is not asserted. [Statistics Poland, *Panorama dzielnic Warszawy 2025*](https://warszawa.stat.gov.pl/files/gfx/warszawa/pl/defaultaktualnosci/760/5/26/1/panorama_dzielnic_warszawy_2025v08_internet.pdf)

The operating denominator should be constructed as a named account list:

\[
N_{\text{reachable payers}} =
N_{\text{active 20–249 employee sites}}
\times
\text{provider-cluster coverage}
\times
\text{benefit-fit rate}
\]

The conservative and expected cases require 80 and 350 employer customers respectively. The strong case requires expansion beyond Warsaw rather than relying on a single local denominator.

## 4. Incentive, power and information map

| Actor | Pays/receives | Power retained | Information received | Principal risk |
|---|---|---|---|---|
| Employer | Prepays pack; may incur benefit-related payroll cost | Sets budget, employee eligibility and continuation | Pack balance, aggregate redemption, invoices | Low use, tax cost, employee dissatisfaction |
| Employee | Normally zero copay | Chooses whether to participate, provider and appointment; gives clinical consent | Available services, providers, expiry and cancellation terms | Privacy, unsuitable appointment, lost credit |
| Provider | Receives option and exercise payments | Sole control of assessment, suitability, treatment and clinical record | Booking identity and information needed to provide care | Liability, cannibalization, no-show, administration |
| Entrant | Buys options; receives employer prepayment | Controls commercial inventory, pack ledger, payment and booking channel | Minimum booking, eligibility and redemption data | Unused options, refunds, liquidity, privacy and contract liability |
| Payment/booking processors | Receive processing fees | Only contracted processing functions | Minimum payment or booking fields | Security and service failure |
| Tax, privacy and professional authorities | No transaction payment | Interpret and enforce applicable rules | Records obtainable under law | Reclassification, fines, corrective orders |
| Medical-network incumbents | Receive subscription or package fees | Control their own networks and package design | Member and utilization data under their arrangements | Can bundle or imitate rapid-access capacity |

The entrant must not direct treatment, demand medical notes, reward a particular diagnosis, or let the employer condition employment decisions on utilization.

## 5. Price, unit economics and cash timing

### Proposed pricing

| Pack | Employer price, net | Unit price | Intended use |
|---|---:|---:|---|
| Pilot | 2,100 PLN / 10 credits | 210 PLN | One-month paid proof |
| Standard | 4,000 PLN / 20 credits | 200 PLN | Small employer |
| Larger site | 7,600 PLN / 40 credits | 190 PLN | Dense local site |

Prices exclude any VAT that may become chargeable. The model assumes either recoverable VAT or prices reset to preserve net economics; the actual VAT treatment is unresolved.

### Expected per-redeemed-credit model

| Item | PLN |
|---|---:|
| Average employer price | 205.00 |
| Provider payment for exercised slot, including used-slot option fee | (135.00) |
| Option fees lost on unused capacity at 80% capacity utilization | (2.50) |
| Payment, booking, refund and messaging cost | (6.00) |
| Gross profit | **61.50** |
| Gross margin | **30.0%** |

The 2.50 PLN leakage assumes a 10 PLN option premium and 0.25 unused options per redeemed appointment at 80% utilization. Provider pricing is an operating assumption, not an observed wholesale quote.

At 24 credits per employer per month, expected monthly revenue is **4,920 PLN** and gross profit is approximately **1,476 PLN**. A 3,000 PLN fully loaded employer acquisition cost would be recovered from gross profit in approximately two months, before central operating expenses and churn.

### Cash cycle

1. Employer prepays seven days before the service month.
2. Entrant pays option premiums weekly.
3. Employees claim credits and book released slots.
4. Provider invoices exercised slots weekly or on net-7/net-14 terms.
5. Entrant holds a refund and dispute reserve.
6. Accounting revenue is recognized when the service obligation is satisfied or when an enforceable expiry is reached—not automatically when cash arrives.

Employer prepayment can create positive working capital, but refund rights, VAT, revenue recognition and accumulated provider invoices could reverse it. The entrant should reconcile capacity liabilities and credit liabilities weekly.

## 6. Founder-wealth cases

All figures are nominal PLN. “Operating margin” below means normalized operating/EBITDA margin before financing and company tax. Valuation multiples are planning assumptions, not observed offers. Retained earnings are reflected through operating value and net debt and are not added again to founder wealth.

|  | Conservative, year 5 | Expected, year 6 | Strong, year 8 |
|---|---:|---:|---:|
| Geography | Warsaw | Warsaw metro | Five major Polish metros |
| Employer customers | 80 | 350 | 1,200 |
| Credits/customer/month | 12 | 24 | 32 |
| Annual redeemed credits | 11,520 | 100,800 | 460,800 |
| Average revenue/credit | 195 | 205 | 210 |
| Annual revenue | **2.246m** | **20.664m** | **96.768m** |
| Gross margin | 25% | 30% | 35% |
| Gross profit | 0.562m | 6.199m | 33.869m |
| Operating margin | 3% | 12% | 17% |
| Operating/EBITDA profit | 0.067m | 2.480m | 16.451m |
| Valuation assumption | 3× | 5× | 6× |
| Enterprise value | 0.202m | 12.398m | 98.703m |
| Net debt | 0 | 0.800m | 3.000m |
| Founder ownership | 100% | 75% | 60% |
| Founder company-equity value | 0.202m | 8.699m | 57.422m |
| Cumulative founder distributions | 0.020m | 0.250m | 0 |
| Implied founder wealth | **0.222m** | **8.949m** | **57.422m** |

### Capital, dilution and reinvestment assumptions

**Conservative**

- Founder contributes up to **100,000 PLN**.
- No external equity; no net debt at year 5.
- Cumulative after-tax distributable cash: **0.40m PLN**.
- **0.38m PLN, or 95%,** remains in the company; **0.02m PLN** is distributed.
- The retained amount is already reflected in company operations and net debt.

**Expected**

- Founder contributes **100,000 PLN**.
- Approximately **2.5m PLN** external equity supports hiring, provider-cluster rollout and software.
- Investor ownership plus an employee option pool dilutes the founder to **75%**.
- A working-capital facility reaches 1.5m PLN; net debt at the valuation date is **0.8m PLN**.
- Cumulative after-tax distributable cash: **5.0m PLN**.
- **4.75m PLN, or 95%,** is reinvested; **0.25m PLN** is distributed.
- The retained 4.75m PLN is not separately added to founder wealth.

**Strong**

- Cumulative external equity of approximately **12m PLN**, including an employee pool, leaves the founder with **60%**.
- Debt facilities reach 5m PLN; net debt at year 8 is **3m PLN**.
- Cumulative after-tax distributable cash of approximately **20m PLN** is **100% reinvested**.
- No founder distribution is included.

The expected and strong cases assume the founder leaves employment after repeatable sales and operations exist. While still employed, the operating plan remains limited to roughly five hours per day and uses contractors for legal, payroll, provider onboarding and booking support.

## 7. Acquisition route

The initial route is founder-led, account-based selling to owners, finance leads and HR leads at Warsaw employers with concentrated workforces. Suitable opening segments include professional-service offices, call centres, logistics sites, light manufacturing, trades and employers with visible ergonomic or manual-work exposure.

The offer is not “better healthcare.” It is:

> A prepaid local appointment allowance with specified same-week inventory, no annual medical-package commitment and no clinical information returned to the employer.

Practical acquisition tools:

- named lists of employers within 15–30 minutes of contracted provider clusters;
- direct email, LinkedIn and telephone outreach;
- warm introductions from accountants, payroll bureaux, occupational-safety advisers and local business associations;
- provider referrals to nearby employers;
- employee-benefit brokers after direct economics are established;
- no camera-led or influencer distribution.

The family connection to a seven-person renewable installer can provide workflow interviews and potentially a paid small-company reference, but it should not substitute for a paid Warsaw transaction.

## 8. First ten and first one hundred customers

### First paid proof

Target duration: **14–21 days**.

1. Obtain written price and schedule indications from ten independent providers.
2. Sign option agreements with two providers for a combined 10–20 weekly slots.
3. Prepare employer, employee, privacy and provider terms with Polish counsel.
4. Sell one Warsaw SME a ten-credit pack for **2,100 PLN net**, paid before activation.
5. Run booking manually using opaque eligibility codes and provider-hosted clinical intake.
6. Record claim time, offered slots, booking time, attendance, option losses, refunds and employer renewal intent.

Capital exposed:

| Item | PLN |
|---|---:|
| Provider option fees and capacity deposit | 1,000–4,000 |
| Legal, privacy, tax and contract work | 1,500–6,000 |
| Payments, insurance and simple booking operations | 500–2,000 |
| Total | **3,000–12,000** |

No custom software is required for the first transaction.

### First ten employers

- Operate one or two Warsaw provider clusters.
- Contract approximately 6–8 providers offering around 35 option slots per week.
- Sell ten-credit monthly packs, yielding roughly 100 credits per month.
- Founder remains primary seller and account owner.
- A contractor performs reconciliations and employee support.
- Capture reasons for non-claim, unavailable appointment times, cancellations and provider refusals.

### First one hundred employers

- Expand to approximately 20–30 providers.
- Maintain around 470 option slots per week to support roughly 1,500 monthly redemptions at 80% utilization.
- Standardize provider eligibility, insurance evidence, option release times, no-show handling and invoice reconciliation.
- Add an operations lead and one employer salesperson.
- Introduce broker and payroll-bureau referrals only after the direct contract and support process are stable.
- Provide employers a dashboard limited to pack balance, aggregated use and service-level measures.

## 9. Control and compounding asset

The defensible asset is the combined local liquidity record:

- provider-by-day and provider-by-time capacity curves;
- option prices and provider acceptance history;
- employer demand by location and time window;
- anonymized claim, booking, attendance and cancellation history;
- renewal and pack-sizing history;
- capacity-option contracts and release rights;
- an owned employer and employee booking channel.

The data should improve option purchasing and reduce unused-option leakage. It must not include clinical notes or inferred diagnoses. Raw appointment-level data should have short retention periods, while aggregated capacity statistics can persist under a documented retention policy.

## 10. Incumbent route-around

Incumbents can bypass the entrant in several ways:

- LUX MED, Medicover, PZU Zdrowie or Enel-Med can add rapid rehabilitation access to existing employer contracts.
- Benefit brokers can negotiate direct packages or reimbursement allowances.
- Employers can reimburse employee invoices rather than prebuy capacity.
- Providers can sell corporate vouchers or reserved blocks directly.
- Booksy can add employer-funded credits or provider yield-management tools.
- Employers can buy broad annual medical packages; PZU already bundles rehabilitation into higher packages.
- Providers can simply discount late appointments without granting options.

The entrant’s response is contractual access to fragmented independent-provider inventory, faster local supply deployment, employer-specific pack sizing and data that makes weekly option purchasing more accurate. Exclusivity should be narrow and time-limited; broad provider restrictions would increase cost and legal risk.

## 11. Rule and constraint classification

| Classification | Current position |
|---|---|
| Employment-benefit tax | The tax authority states that employment income includes amounts paid for an employee and free or partly paid benefits. This supports treating employer-funded credits as potentially taxable employee income. Exact treatment depends on allocation and use. [Polish tax portal](https://www.podatki.gov.pl/podatki-osobiste/pit/informacje-podstawowe/co-jest-opodatkowane/dochody-z-pracy) |
| Social contributions | ZUS guidance discusses employer-funded medical packages as employee income subject to pension and disability contributions during work periods. It does not determine every credit design. [ZUS e-files Q&A](https://www.zus.pl/en/firmy/przedsiebiorco-przeczytaj-wazne/e-akta/e-akta-pytania-i-odpowiedzi) |
| Health privacy | Appointment purpose may reveal health information. GDPR Article 9 treatment, the entrant’s lawful basis, controller roles and any DPIA obligation require a Polish privacy memorandum. The official EUR-Lex page was technically inaccessible during extraction. [GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj) |
| Expiry and consumer terms | UOKiK guidance says the seller sets a gift-card validity period and must present it clearly and understandably. Whether an employee beneficiary is a consumer party under this structure remains unresolved. [UOKiK voucher guidance](https://archiwum.uokik.gov.pl/aktualnosci.php?news_id=19140) |
| Professional independence | Provider must remain solely responsible for clinical suitability, consent, treatment and clinical records. Applicable physiotherapist and medical-activity rules were not researched within this packet’s source budget. |
| VAT and invoicing | It is unknown whether the entrant’s option, booking or credit resale qualifies for any medical-service exemption. The financial cases assume net economics unaffected by unrecoverable VAT. |
| Employment relationship | Participation must be voluntary and must not affect employment decisions. Employer access to individual clinical utilization should be prohibited. |
| Contract | Option release, exercise, resale, no-show, refund, service quality, insurance and liability allocation can be addressed contractually, subject to mandatory law. |

## 12. Lawful operating structure

A Polish limited-liability company would act as the nonclinical capacity and payment intermediary.

Required boundaries:

- Provider is an independent professional business with required registrations and professional-liability insurance.
- Provider remains the service party responsible for care.
- Entrant sells appointment-access credits and administers payment; it does not advertise itself as the treating entity.
- Employer buys a commercial pack and defines eligibility without receiving medical data.
- Employee voluntarily claims a credit and separately accepts provider consent and clinical terms.
- Entrant processes only identity, eligibility, contact, location, appointment and redemption data necessary for booking.
- Clinical intake occurs directly with the provider.
- Employer reporting is aggregated and suppresses small groups where re-identification is plausible.
- Provider and entrant controller roles, processors, retention, breach handling and data-subject requests are documented.
- Provider option agreements prohibit clinical steering and employer influence.
- Employee terms state price, expiry, cancellation, no-show, refund, complaint and provider identity clearly.
- A written Polish tax/VAT/payroll memorandum precedes repeat sales.

Prohibited operating methods include outcome guarantees, diagnostic targeting by employers, fake bookings, provider employment misclassification and unauthorized access to clinical information.

## 13. Dependencies

- Independent providers willing to release identifiable weekly capacity at the assumed wholesale economics.
- A tax/payroll structure employers can administer.
- Confirmed VAT and revenue-recognition treatment.
- A legally sufficient basis for booking data that may imply health information.
- Provider professional credentials and insurance verification.
- Employee demand aligning with providers’ genuinely empty times.
- Reliable cancellations, reminders and option-release automation.
- Payments capable of handling employer prepayment and refunds.
- Professional, cyber and intermediary liability insurance.
- Employer procurement and benefit-policy approval.
- Adequate provider density around each employer cluster.
- Founder employment contract permitting the activity.

## 14. Kill criteria

Cease additional deployment spending if any of the following occurs:

- After 30 provider discussions, fewer than six providers will sign cancellable options near **135 PLN all-in per exercised slot**.
- After 100 qualified employer contacts and 20 buyer meetings, fewer than three employers prepay at least **190 PLN per credit**.
- Two operating clusters remain below **60% capacity-option utilization** for eight consecutive weeks.
- Attendee no-shows and late cancellations exceed **25%** despite reminders and clear terms.
- Realized gross margin remains below **20%** across 300 completed appointments.
- Employers’ payroll treatment adds enough employee tax or contributions that three paid pilots decline renewal specifically for that reason.
- Counsel concludes that the necessary structure makes the entrant responsible for clinical provision or creates unrecoverable VAT that removes positive contribution margin.
- The model requires employers to receive individual clinical or inferred-health information.
- Fewer than 70% of the first 20 renewal-eligible employers renew or replace their pack with another paid pack.
- Provider supply is concentrated in low-demand hours that cannot be matched with voluntary employee use.

## 15. Decision-critical unknowns

1. Exact PIT and ZUS treatment when credits are allocated, claimed, redeemed or expire.
2. VAT treatment of option fees, resale credits and booking/intermediation.
3. Whether employees acquire consumer rights directly against the entrant.
4. Which GDPR Article 6 and Article 9 bases apply and whether consent is appropriate in an employment setting.
5. Controller allocation among employer, entrant and provider.
6. Applicability of physiotherapist, medical-activity and referral rules.
7. Provider willingness to accept option premiums and wholesale exercise prices.
8. Distribution of real empty slots by weekday and hour.
9. Employee claim, attendance and repeat-use rates.
10. Employer willingness to pay separately when it already provides a medical package.
11. Whether rapid access influences absence, employee satisfaction or retention.
12. Acceptable expiry, rollover, substitution and refund mechanics.
13. Accounting treatment of unredeemed credits.
14. Direct-employer acquisition cost and annual retention.
15. Integration requirements for provider calendars and existing booking systems.
16. Exact number of reachable Warsaw employer sites after active-employer and geographic filtering.

## 16. Development status

This is a research-stage commercial design. No provider interview, option quote, signed contract, employer meeting, prepaid pack, employee booking, privacy memorandum, tax opinion or live utilization record was supplied or created during this packet. The unit economics, acquisition costs, capacity utilization, retention, financing and valuation multiples are explicit planning assumptions.

## 17. Query ledger

All eight distinct queries were executed on 2026-08-22. The ledger timestamp was recorded at **14:58:54 CEST**; the search backend did not expose individual request clock times.

| ID | Exact query | Purpose | Result used |
|---|---|---|---|
| Q1 | `site:podatki.gov.pl świadczenia pracownicze fizjoterapia pracodawca przychód pracownika podatek` | Employee-benefit PIT treatment | General official rule for free and employer-paid benefits |
| Q2 | `site:zus.pl świadczenia pracownicze fizjoterapia składki pracodawca pakiet medyczny` | Social-contribution treatment | ZUS medical-package example |
| Q3 | `site:uodo.gov.pl dane o zdrowiu rezerwacja wizyty pracodawca pracownik fizjoterapia` | Health-data boundaries | No sufficiently useful UODO result returned |
| Q4 | `site:uokik.gov.pl bon voucher termin ważności zwrot konsument usługi` | Credit expiry and consumer terms | Official voucher-expiry guidance |
| Q5 | `site:stat.gov.pl Warszawa podmioty gospodarki narodowej liczba pracujących 10-49 50-249 2025` | Payer denominator | GUS result with employer-size shares; PDF extraction failed |
| Q6 | `site:zus.pl absencja chorobowa 2025 choroby układu mięśniowo-szkieletowego raport` | Problem magnitude | Official 2025 absence report |
| Q7 | `fizjoterapia Warszawa cennik 2026 wizyta 60 minut cena` | Retail price anchor | Warsaw provider price list |
| Q8 | `pracodawca pakiet medyczny fizjoterapia pracownicy cena Medicover Lux Med PZU 2026` | Incumbent route and package pricing | PZU package containing rehabilitation |

## 18. Source ledger

Access recorded 2026-08-22 14:58:54 CEST.

| ID | Source | Type | Access result | Use |
|---|---|---|---|---|
| S0 | [Booksy Biz pricing](https://biz.booksy.com/pl-pl/cennik) | Commercial primary; packet-supplied | Not reopened; evidence taken from assigned packet | Provider software and acquisition-price anchor |
| S1 | [Polish tax portal—employment income](https://www.podatki.gov.pl/podatki-osobiste/pit/informacje-podstawowe/co-jest-opodatkowane/dochody-z-pracy) | Government authority | Usable | General PIT rule |
| S2 | [ZUS e-files Q&A](https://www.zus.pl/en/firmy/przedsiebiorco-przeczytaj-wazne/e-akta/e-akta-pytania-i-odpowiedzi) | Government authority | Usable | Medical packages and contributions |
| S3 | [GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Primary law | Technical extraction failure | Privacy issue identification only |
| S4 | [UOKiK voucher guidance](https://archiwum.uokik.gov.pl/aktualnosci.php?news_id=19140) | Consumer authority | Search content usable; opened page blocked | Validity disclosure |
| S5 | [GUS Warsaw district panorama](https://warszawa.stat.gov.pl/files/gfx/warszawa/pl/defaultaktualnosci/760/5/26/1/panorama_dzielnic_warszawy_2025v08_internet.pdf) | Official statistics | Technical extraction failure; search snippet usable | Employer-size shares |
| S6 | [ZUS 2025 absence report](https://www.zus.pl/documents/10182/39590/Raport%2BAbsencja%2Bchorobowa%2Bw%2B2025%2Broku.pdf/b2b8893f-049d-0782-1787-415168d381b3?t=1775560395351) | Official statistics | Usable | Absence burden |
| S7 | [Osteomedis price list](https://osteomedis.pl/cennik/) | Provider commercial source | Usable | Warsaw retail pricing |
| S8 | [PZU Zdrowie packages](https://zdrowie.pzu.pl/sklep/pakiety-medyczne?cid=blog-banner) | Incumbent commercial primary | Usable | Package route-around |

## 19. Evidence ledger

| Evidence | Status | Source | Boundary |
|---|---|---|---|
| Musculoskeletal conditions produced 42.4m absence days and 17.5% of own-illness days in 2025 | Verified | S6 | National burden; no causal claim for the product |
| Warsaw physiotherapy prices of 180–200 PLN for ordinary visits | Verified for one provider | S7 | Not a market average |
| PZU Premium costs 5,433 PLN/year and lists 30 rehabilitation procedures | Verified | S8 | Individual rather than employer price; procedures may differ from visits |
| Employer-paid and free benefits may constitute employment income | Verified general rule | S1 | Exact credit treatment unresolved |
| ZUS discusses employer-funded medical packages as income subject to contributions | Verified example | S2 | Structure-specific advice still required |
| Voucher validity is set by the seller and should be clear and understandable | Verified authority guidance | S4 | B2B/employee-party application unresolved |
| Warsaw entities declaring 10–49 workers were 2.2%; above 49 were 0.5% | Search-result evidence | S5 | Exact count and 50–249 subdivision unavailable |
| GDPR health-data restrictions are potentially engaged | Primary-law issue; extraction incomplete | S3 | Legal basis and role allocation unresolved |
| Booksy charges 145 PLN monthly, 35 PLN/additional user and 45% Boost fee on a completed first visit | Packet-supplied evidence | S0 | Not independently reopened |
| Employers will pay 190–210 PLN per credit | Unknown | — | Requires prepaid pilots |
| Providers will accept approximately 128–138 PLN exercised-slot economics | Unknown | — | Requires signed option quotations |
| Capacity utilization can reach 65–88% | Model assumption | — | Requires live weekly inventory |
| Employer credits reduce absence or waiting cost | Unknown | — | No outcome claim should be made |
| 3×–6× enterprise-value multiples and stated dilution | Financing assumptions | — | Not market quotations |
