# Reporting Requirements

## Purpose
Provide near-real-time visibility across sales, inventory, and labor so store and regional leaders can react quickly.

## Stakeholders & Use Cases
- **Store managers:** monitor daily sales vs. targets, margin, and staff performance.
- **Regional leaders:** roll up performance, identify underperforming locations, track promotions.
- **Finance/accounting:** reconcile sales to deposits, ensure tax remittance accuracy.
- **Merchandising:** understand SKU velocity, markdown effectiveness, and stockout risk.

## Core Dashboards
1. **Sales Pulse (intra-day)**
   - Metrics: net sales, transactions/hour, avg basket, discount leakage, tender mix.
   - Filters: store, region, channel, fulfillment type.
   - Visuals: sparkline vs. last week, gauge against goal, leaderboard of top-performing associates.
2. **Inventory Health**
   - Metrics: OH qty, sell-through %, shrink, aging inventory buckets.
   - Alerts: auto email when OH < reorder point or shrink > 2% per week.
   - Data joins: POS sales, purchase orders, cycle counts.
3. **Operational Compliance**
   - Cash variance trend, exception overrides by associate, offline duration per register.
   - Exportable audit package (CSV + PDF) for regulators.
4. **Reporting API feeds**
   - JSON/CSV endpoints for BI tools with pagination + delta tokens.

## Data Model & Refresh Cadence
- Transactions streamed via Kafka topic `pos.txn.completed` within 30 seconds of tender completion.
- Inventory adjustments stream separately with reason codes (sale, return, manual, transfer).
- Labor data pulled hourly from workforce system for sales-per-labor-hour calculations.
- Data warehouse tables partitioned by `business_date` and `store_id`; late-arriving facts allowed up to T+2 days.

## Access & Governance
- Row-level security enforced by store/region membership; regional directors can impersonate store view with audit trail.
- PII (customer emails/phones) masked unless user has CRM role; exports watermark requesting user and timestamp.
- Support saved reports, subscriptions, and anomaly detection thresholds configurable per role.

## Success Metrics
- Dashboards refreshed < 2 minutes behind live transactions.
- 99.9% availability during trading hours.
- Less than 5% of reports require manual Excel manipulation (goal: built-in views cover needs).
