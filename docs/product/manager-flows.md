# Manager Flows

## Objectives
- Ensure cash control, staffing, and compliance oversight for every shift.
- Provide tools to react to alerts (fraud, hardware failures, KPIs) in real time.
- Deliver reporting snapshots without forcing the manager back to the office PC.

## Daily Routine Flow
1. **Open store**
   - Approve float amounts for each register and confirm safe drop totals.
   - Run hardware diagnostic summary; escalate any offline printers before store open.
2. **Monitor operations**
   - Live dashboard shows sales/hour, open carts, and queue length telemetry from registers.
   - Managers can reassign transactions, park/resume carts, or hop into a register with override PIN.
3. **Overrides & approvals**
   - All price overrides, tax exemptions, voids, and returns require manager MFA and reason code library.
   - Approval modal surfaces transaction context (items, customer, prior issues) before confirmation.
4. **Cash reconciliation**
   - Mid-day blind counts supported for variance monitoring.
   - End-of-day close wizard: prompt for final cash count, gift card activation report, and deposit slip export.
5. **Staff management**
   - Activate/deactivate cashier logins, reset passwords, and transfer shifts between registers.
   - Schedule adherence: register pings manager if cashier idle > 10 minutes during scheduled shift.

## Alerting & Escalations
- **Fraud triggers:** rapid successive refunds, high-value discounts, mismatched tender vs. receipt.
- **Hardware:** printer/journal roll low, payment terminal firmware out-of-date, scanner disconnections.
- **Operational:** inventory count mismatches, offline register > 5 minutes, loyalty enrollment drop.
- Alerts escalate from register banner → manager mobile push → regional notification if unresolved after SLA.

## Data & Audit Requirements
- Every approval event stores manager ID, affected transaction, justification, and latency to respond.
- Cash reconciliation history keeps start float, declared amount, expected amount, and variance notes.
- Manager activity timeline (logins, register hops, approvals) retained for 18 months for compliance.

## Success Metrics
- Close procedure duration < 15 minutes per register.
- Manager response time to P1 alerts < 2 minutes.
- Variance investigations opened within 24 hours 95% of the time.
