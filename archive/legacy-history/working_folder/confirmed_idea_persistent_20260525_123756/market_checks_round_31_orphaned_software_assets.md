# Round 31 Market And Competition Checks: Orphaned Software Payment-Flow Assets

Created: 2026-05-25

## Checked Facts

- WordPress.org plugin pages expose public signals useful for acquisition screening: active-install buckets, changelog recency, author profiles, support threads, ratings, and update behavior. WordPress support discussion confirms active-install counts come from update checks against WordPress.org.
  - Source: https://wordpress.org/support/topic/wordpress-plugins-and-active-installations/

- WP Beacon tracks WordPress plugin ownership transfers, dormant-then-reactivated plugin behavior, active installs, and malicious acquisition cases. This confirms that plugin ownership/update-channel transfer is a real control point with serious security implications, not just a generic code purchase.
  - Source: https://wpbeacon.io/
  - Source: https://wpbeacon.io/acquisitions/

- PrestaShop Addons is an official marketplace for modules, including shipping/carrier and payment modules. Its marketplace pages emphasize module support and updates, and show that merchants buy add-ons for operational workflows such as carrier integrations.
  - Source: https://addons.prestashop.com/en/520-shipping-carriers

- PrestaDB indexes more than 1,200 free PrestaShop modules from 600+ developers and explicitly scores maintenance activity, PrestaShop compatibility, documentation, and adoption. This supports the screening thesis: there are many small modules where abandonment/maintenance status is visible.
  - Source: https://prestadb.com/

- Polish/CEE PrestaShop module vendors publicly sell local payment, delivery, InPost parcel locker, DPD, SMS, invoice, and checkout modules with upgrade/support mechanics. This validates the local connector category.
  - Source: https://prestadev.pl/en/prestashop-modules/inpost-parcel-machines-pro-module-for-prestashop.html
  - Source: https://prestaplay.com/en/modules-addons/
  - Source: https://prestashow.pl/platnosci-i-dostawa

- WordPress community discussions highlight practical merchant/site-owner fear around abandoned or removed plugins: directory removal, security issues, and unsupported updates can force users to remove or replace plugins.
  - Source: https://www.reddit.com/r/Wordpress/comments/1tg35t0/plugin_disappeared_from_the_directory_should_i/
  - Source: https://www.reddit.com/r/Wordpress/comments/1n0lnas/over_50_of_plugins_in_the_wordpress_repository/

## Market Implication

This cannot be a "we will build plugins" idea. That is copyable and has weak distribution.

The only potentially defensible wedge is acquisition of an existing narrow software asset with:

- installed base;
- update channel;
- reviews/listing/search history;
- customer support inbox;
- source and release credentials;
- license server;
- renewal/payment flow;
- seller handoff.

## Transferability Caveat

The proof must confirm transferability asset by asset. Some marketplaces, payment accounts, or plugin listings may not be cleanly transferable, and some customers may need re-consent or contract novation.

The simulated and real-gate wording should treat transferability as a kill criterion, not as an assumption.

## Competition Implication

Incumbent agencies and plugin vendors can build substitutes, but they cannot instantly copy the acquired installed update channel or existing customer payment flow. The asset is closer to a micro-acquisition roll-up than a greenfield SaaS.

## Remaining Kill Risks

- No owner with meaningful active paid users will sell under 100,000 PLN or accept an earnout.
- The code is insecure or too poorly written to maintain part-time.
- The marketplace account/listing cannot be transferred.
- Customers churn when ownership changes or reject payment-flow migration.
- The category is too small: acquisition may produce income but not a venture-scale company unless repeat acquisition pipeline is demonstrated.
- A platform/carrier/payment provider releases an official free connector that compresses pricing.
