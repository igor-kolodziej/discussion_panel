# WooRenewal v2 Decision-Critical Research

- Research date: 2026-07-13 CEST
- Success definition for this revision: a credible route to 1,000,000 PLN of recognized annual revenue by Year 5 with at least 25% operating margin.
- This user-defined Revenue Quality Gate replaces the default founder-wealth gate for this run only.

## Evidence Summary

### Official update-channel transfer is real

WordPress.org documents that a plugin has one official owner. For plugins below 10,000 users, the current owner can add the buyer as a committer and transfer ownership from the Advanced screen. Plugins over 10,000 users require a written request from the current owner and may be denied or delayed. This proves the transfer mechanism, not the availability of a seller or the transfer of billing, IP, customer data, domain, or support history.

Source: [WordPress Plugin Handbook — Transferring Your Plugin to a New Owner](https://developer.wordpress.org/plugins/wordpress-org/transferring-your-plugin-to-a-new-owner/)

WordPress.org also permits adoption of abandoned plugins, but requires attempts to contact the owner, a complete code/security update, and review. It offers no guarantee of transfer. Larger or high-risk plugins are less likely to be adopted.

Source: [WordPress Plugin Handbook — Take Over an Existing Plugin](https://developer.wordpress.org/plugins/wordpress-org/take-over-an-existing-plugin/)

### Billing-product transfer is technically supported

Freemius documents product-ownership transfer for product sales/acquisitions and automatically creates a store for a new owner when needed. Its current documentation supports subscriptions, licences, in-dashboard checkout, deployment, updates, VAT/sales-tax handling, and product migration. This proves that a Freemius-hosted commercial rail can transfer technically. It does not prove that an individual seller's contracts, customer data, liabilities, or renewal cohorts transfer cleanly.

Sources:

- [Freemius — Transferring Product Ownership](https://freemius.com/blog/changelog/fixed-bug-in-transferring-product-ownership/)
- [Freemius WordPress Product Documentation](https://freemius.com/help/documentation/wordpress/)
- [Freemius — What the Platform Does](https://freemius.com/help/documentation/selling-with-freemius/so-what-does-freemius-do/)

### Public supply screen

The official WordPress.org Plugin Information API was queried across four WooCommerce-related searches and three result pages per search. After deduplication:

- 903 public plugins were screened;
- 41 independent operational-workflow plugins had 1,000–50,000 active installs and at least 90 days since the latest update;
- zero publicly disclosed all of: 100 paying sites, 75% renewal, support hours, asking price, billing assignment, IP chain, and atomic transfer;
- therefore qualifying affordable supply remains unproved.

Artifacts:

- `woorenewal_public_target_screen.csv` — 903-row screen with public metadata and unknown fields explicitly marked.
- `research_woorenewal_public_target_screen.md` — method, leads, and gate interpretation.
- `screen_woorenewal_targets.mjs` — reproducible official-API collection and ranking.

Official API source: [WordPress.org Plugin Information API](https://api.wordpress.org/plugins/info/1.2/)

### Small-asset sale precedents exist, but are not qualifying proof

1. A January/February 2026 public seller post offered an unnamed WooCommerce bulk editor for USD 6,000. The seller claimed 1,000+ active installs, USD 317 average monthly revenue from the prior two months, zero refunds, zero support tickets, organic WordPress distribution, and inclusion of the WordPress.org slug and Freemius transfer. The history is too short to prove 12-month renewal or 100 paying sites; the seller and product are not independently verified in this research.

   Source: [Reddit — WooCommerce Bulk Editor offered for USD 6,000](https://www.reddit.com/r/micro_saas/comments/1rf68ws/for_sale_woocommerce_bulk_edit_plugin_1000_active/)

2. A 2025 seller post described a WordPress plugin with 4,500+ active installs, USD 2,844.20 annual revenue, 3,000 email subscribers, subscription and lifetime revenue, and one support request every two to three months. The plugin was not named publicly, its price and renewal rate were not disclosed, and WooCommerce relevance was described only as a cross-sell opportunity.

   Source: [Reddit — WordPress plugin business offered for sale](https://www.reddit.com/r/Wordpress/comments/1lujys1/i_am_looking_to_sell_our_wordpress_plugin_business_where_do_i_start/)

3. An ended Flippa listing offered a WooCommerce one-page-checkout bundle with 140+ sales, 190+ active sites, USD 194 monthly profit, 60% margin, and a USD 5,000 asking price. The listing mentioned possible retained seller rights, which would fail WooRenewal's clean-IP/atomic-transfer requirement unless removed. It is a transaction precedent, not a live target.

   Source: [Flippa — WooCommerce checkout plugin bundle](https://flippa.com/11992701-monetized-wordpress-plugin-bundle-woocommerce-one-page-checkout-plugins-powerful-license-manager-140-sales-190-active-sites)

4. A sold Flippa listing for WPSchoolPress showed USD 19 monthly profit, 79% margin, a 3.7× profit multiple, and an USD 830 winning bid. This supports the existence of very small plugin transactions but not WooCommerce fit or the Year-5 growth bridge.

   Source: [Flippa — WPSchoolPress sold listing](https://flippa.com/8001977-wordpress-plugin-business-for-sale-with-active-subscribers)

### Larger successful assets are outside the founder's acquisition envelope

Flippa reports that WPGetAPI reached roughly 6,000 active installs, 500–600 paid users, thousands in monthly recurring revenue, and an approximately 10% free-to-paid conversion before selling for six figures. It took about 18 months of product/support work before the founder left employment. This is evidence that organic WordPress distribution can produce a valuable paid cohort, but it also shows that a proven cohort of the size WooRenewal ultimately needs is likely far above the initial cash cap.

Source: [Flippa — WPGetAPI six-figure sale](https://flippa.com/blog/wordpress-plugin-sells-for-six-figures-on-flippa/)

### Trust has become a stronger acquisition obstacle

The WordPress Plugin Developer FAQ, updated June 30, 2026, explicitly says unsolicited plugin-purchase offers are probably not legitimate, reports that many have harmed users, and advises owners to transfer only to people they have personally vetted and trust. That directly weakens the claim that an unknown first-time buyer can obtain 100 data rooms through cold outreach.

Source: [WordPress Plugin Developer FAQ — Plugin Ownership](https://developer.wordpress.org/plugins/wordpress-org/plugin-developer-faq/)

WordPress.org also prohibits tracking without explicit consent, dashboard hijacking, spam, and installing premium executable code through the free-directory plugin. Therefore an acquisition cannot be monetized by silently collecting merchant data or aggressively pushing unrelated offers through the update channel.

Source: [WordPress Detailed Plugin Guidelines](https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/)

## Economic Reality Check

At a purchase discipline of at most 2.0× verified owner earnings, 28,000 PLN cash buys roughly 14,000 PLN of annual owner earnings in a no-growth case. Even deploying the founder's complete 100,000 PLN after paid proof would buy roughly 50,000 PLN of annual owner earnings at that multiple. Reaching 250,000 PLN operating profit by Year 5 therefore requires substantial organic product growth, unusually favorable seller financing, or both. Acquisition compounding alone does not bridge the target.

The expected Year-5 model requires approximately 1,100 paid accounts at about 910 PLN recognized annual revenue per account. Starting with 100–150 paid accounts implies roughly 50–65% annual account/revenue growth for several years unless a second related asset contributes a meaningful cohort. No public source proves that bridge for a target affordable to this founder.

## Decision

- Public screening requirement: **passed** (903 targets screened).
- Three public acquisition precedents: **found**, but none is a live, independently verified, fully qualifying target.
- Affordable qualifying supply: **not proven**.
- Official update and Freemius ownership transfer mechanics: **proven in principle**.
- Unknown-founder seller trust: **weaker than v1 assumed**.
- 1m PLN/25% Year-5 target: **arithmetically possible but not yet evidence-backed**.

No seller was contacted and no commitment was made.

