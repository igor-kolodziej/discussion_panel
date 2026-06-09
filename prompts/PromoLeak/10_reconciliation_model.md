# Reconciliation Model

## Objective
Build the first practical reconciliation model for one brand and one retailer/channel, focused on finding recoverable or preventable leakage.

## Prerequisites
- Documents have been received and organized.
- Extracted tables exist or can be created from source files.
- The audit scope and date range are fixed.
- The goal is leakage detection, not full accounting cleanup.

## Inputs
- Invoices.
- Credit notes.
- Retailer or distributor remittances.
- Promotion agreements and promo calendars.
- Price lists and agreed trade terms.
- Retail-media charges if available.
- Sell-out files if available.
- Extraction workflow and table schema.

## Instructions
1. Normalize document identifiers, dates, retailer/channel names, product names, SKUs, EANs, quantities, net values, VAT, and currencies.
2. Build base tables for invoices, payments/remittances, credit notes/deductions, promo agreements, retail-media charges, price lists, and sell-out.
3. Match deductions to the expected source: promo window, agreed rebate, retail-media campaign, listing fee, logistics/service fee, or unknown charge.
4. Flag leakage categories:
   - duplicated deduction
   - wrong date window
   - unsupported charge
   - price-list mismatch
   - rebate or promo-rate mismatch
   - retail-media charge without evidence
   - remittance short-pay without clear reason
   - promotion that appears contribution-negative
5. Estimate recoverable PLN when evidence supports dispute.
6. Estimate preventable future PLN when mechanics should be renegotiated or stopped.
7. Separate hard findings from hypotheses.
8. Keep formulas and assumptions visible.

## Subagents
- Use one subagent to independently inspect a sample of matched deductions.
- Use one subagent to challenge whether each leakage category is recoverable, preventable, or only informational.
- Use subagents only with permitted document access.

## Output
Return:
- reconciliation table design
- matching logic
- leakage category definitions
- assumption list
- quality checks
- initial finding summary format
