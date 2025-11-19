# Cashier Flows

## Goals
- Move customers through checkout quickly with minimal friction.
- Maintain price accuracy, inventory integrity, and payment compliance.
- Surface alerts for loyalty, age restrictions, and payment issues so the cashier never leaves the customer unattended.

## Personas & Preconditions
- **Primary persona:** Front-line cashier with touch-based register, barcode scanner, cash drawer, and card terminal.
- **Secondary persona:** Lead cashier who can approve overrides and manage cash drawer reconciliation.
- **System prerequisites:**
  - Shift assignment created in workforce module with float amount recorded.
  - Product catalog synced locally with price/version timestamp.
  - Hardware heartbeat < 60 seconds; degraded devices trigger banner before shift start.

## Happy Path Flow
1. **Start transaction**
   - Tap "New Sale" and system opens an empty cart with default store location and register ID.
   - Cashier optionally scans badge or enters PIN to tie the sale to their shift for accountability.
2. **Add items**
   - Scan barcodes or search by name/SKU with autocomplete fed by top-selling items for the store.
   - Grid buttons surface fast-sellers and custom-priced items; layout is configurable per store.
   - Weight-based items prompt for scale input and record raw + net weight for compliance audits.
3. **Apply modifiers**
   - Discounts: manual percent/amount, promotion codes, or loyalty auto-application with guardrails (max 40% unless override role present).
   - Taxes: default from product tax code; override prompt requires manager PIN and captures reason code.
   - Notes: gift receipt flag, curbside instructions, fulfillment routing tag.
4. **Accept payment**
   - Present tender options (card, cash, split, gift, store credit, external financing).
   - Card payments: display device readiness, EMV/Ctless prompts, collect signature/PIN when required, and only pass the tokenized authorization payload to the payments API while the raw network data remains within the payment microservice.
   - Cash payments: show change due, log denomination breakdown, and update drawer variance tracker.
5. **Finalize sale**
   - Offer receipt via print, email, or SMS and log preference to customer profile.
   - Trigger loyalty enrollment if customer not recognized; capture email/phone inline.
   - Fire webhooks for inventory decrement, tax journal entry, and accounting export queues.

## Exception & Recovery Flows
- **Price check:** hold transaction, open price check modal linked to inventory data, and optionally push result back to the cart.
- **Void line item:** require manager PIN; voided SKU recorded with timestamp, cashier ID, and reason.
- **Return/exchange:** switch to return mode, scan receipt or search transactions, validate tender eligibility, restock items, and issue refund in original tender when possible.
- **Offline mode:** capture card payments for deferred auth (tokenized & encrypted), restrict high-risk tenders (gift cards), and queue sync events; UI watermark shows "Offline".
- **Partial fulfillment:** allow split shipments or pickup/delivery combos; each fulfillment leg has its own status and inventory reservation.

## Supporting Services & Telemetry
- **Transaction record:** transaction ID, cashier ID, register ID, timestamp, customer identifier, and channel.
- **Line items:** SKU, quantity, modifiers, tax breakdown, fulfillment leg, and reference to pricing rule applied.
- **Payment events:** tender type, authorization ID, masked PAN, AVS/CVV results, capture status, and reversal references.
- **Device health metrics:** scanner latency, terminal firmware, network strength, offline duration.
- **Audit log:** every override, void, and refund with role + justification for compliance.

## Success Metrics
- Average transaction time < 90 seconds for orders < 5 items.
- Drawer variance < $2 per shift.
- 99.5% of transactions synced to backend within 2 minutes, even after offline recovery.
- < 0.5% manual price overrides per 1,000 transactions (monitors catalog quality).
