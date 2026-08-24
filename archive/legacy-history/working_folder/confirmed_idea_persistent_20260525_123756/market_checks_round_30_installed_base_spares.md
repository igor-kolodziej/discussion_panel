# Round 30 Market And Competition Checks: Installed-Base Spare Custody

Created: 2026-05-25

## Checked Facts

- Siemens' 2025 SIMATIC PCS 7 Remote I/O Upgrade Guideline states that SIMATIC S7-300 / ET 200M availability ran until 1 October 2023, product cancellation takes effect on 1 October 2025, and components are then planned to be available only as spare parts until 1 October 2033. It also notes that one-by-one replacement may be the only option in some brownfield plants where near-continuous production matters.
  - Source: https://cache.industry.siemens.com/dl/files/203/109824203/att_1320236/v1/SIMATIC_PCS_7_Remote_IO_Upgrade_Guideline.pdf

- Siemens support/forum material around S7-300 replacement shows the practical installed-base issue: older plants may have specific CPU, I/O, firmware, Profibus/MPI, or module-version constraints, and direct replacement is not always a simple "buy any newer PLC" decision.
  - Source: https://support.industry.siemens.com/forum/WW/pt/posts/replace-s7-300-cpu-keeping-et200m-rack-i-o/330819/
  - Source: https://support.industry.siemens.com/forum/it/en/post/1185364/

- Polish competitor Gal-Industry already buys and resells industrial automation spare parts, including PLC, HMI, power supplies, and inverters, and publicly specializes in rare or discontinued parts from a Poland/EU warehouse.
  - Source: https://gal-industry.com/

- Polish competitor ADEGIS sells and repairs industrial automation electronics and lists categories such as industrial computers and HMI panels, PLC, frequency converters, drives, servo drives, safety systems, power supplies, and Siemens SIMATIC/SINUMERIK/SIMODRIVE/HMI/SINAMICS/MICROMASTER components.
  - Source: https://shop.adegis.com/
  - Source: https://adegis.com/en/pages/industrial-electronics-sales

- EU Automation publicly offers new, reconditioned, and obsolete automation parts including Siemens SIMATIC S7-200/300, drives, and HMI lines, confirming that generic global obsolete-parts sourcing is an active incumbent category.
  - Source: https://assets.euautomation.com/downloads/guides/Line-Card-us.pdf

- Community discussion in `r/PLC` shows maintenance/automation people still discussing S7-300 obsolescence, stocking spares, using old modules because full retrofit is delayed, and cases where software/protocol/version constraints matter.
  - Source: https://www.reddit.com/r/PLC/comments/1qdicao/siemens_s7300_obsolescence/
  - Source: https://www.reddit.com/r/PLC/comments/11n2aqo/siemens_plc_softwarehardware_requirements/

## Competition Implication

The market already has public obsolete-parts sellers, repair shops, and global sourcing networks. A startup should not pitch "we sell discontinued PLCs/HMIs" as the wedge.

The only stronger version is:

**Line-Down Controls Continuity Retainer**: sell a paid continuity retainer to factories, collect and control their installed-base register, then buy/test/custody exact matching SKUs for the named installed base. This turns customer-side installed-base data plus call-first terms into the control point.

## Why The Control Point Is Different

Generic reseller:

- buys or lists public inventory first;
- waits for stochastic line-down events;
- competes on search, price, stock, warranty, and courier speed;
- can be copied by existing suppliers.

Installed-base custody:

- collects customer-specific asset registers before buying broad inventory;
- uses paid retainers/deposits to fund exact spare purchases;
- controls call-first emergency routing for known SKUs;
- clusters demand across signed local plants;
- builds a proprietary map of "which exact SKU failure stops which line at which plant."

## Remaining Kill Risks

- If plants will not pay at least 1,500-3,000 PLN/month or a setup deposit before an emergency, the model falls back to speculative resale.
- If the founder cannot source exact tested SKUs under budget, the retainer promise is hollow.
- If incumbents can cheaply offer the same installed-base custody to their service customers, copy risk caps the score.
- If liability, returns, wrong diagnosis, firmware mismatch, or travel/support labor consume margins, owner earnings fall below the gate.
- If the first five customers require bespoke plant engineering instead of a standard audit/custody process, the business becomes a local automation service.
