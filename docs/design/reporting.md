# Reporting Screen Wireframe

```
+--------------------------------------------------------------------------------+
| Header: Reporting Hub                 Role: Regional Director | Date: 2025-05-12|
+--------------------------------------------------------------------------------+
| Filters: [Date Range v] [Region v] [Channel v] [Compare to v]                  |
+----------------------+------------------------------+-------------------------+
| KPI Tiles            | Sales Trend                   | Store Leaderboard       |
| -------------------- | ---------------------------- | ----------------------- |
| Net Sales   $482K ▲6%| Graph: Area chart vs. LY     | 1. Downtown     $82K    |
| Avg Basket $18.42 ▲2 | Hover shows promo overlays   | 2. Midtown      $75K    |
| Margin %   54% ▼1    | Toggle: Day/Hour             | 3. Uptown       $61K    |
| Refund Rate1.8%      |                               | 4. Lakeside     $54K    |
+----------------------+------------------------------+-------------------------+
| Exception Feed                              | Export / Subscriptions        |
| ------------------------------------------- | ----------------------------- |
| 08:10  Store 014  Offline >5m               | [Schedule Email] [Download]   |
| 09:20  Register 03 Cash variance $-18       | Latest exports: Sales.csv     |
| 10:05  Tax remittance pending approval      |                   Inventory.csv|
| 10:30  Inventory shrink >3% Store 008       |                               |
+---------------------------------------------+-------------------------------+
| Detail Table (sticky header)                                                v |
| Store | Net Sales | YOY% | Transactions | Margin | Discounts | Alerts        |
| ----- | --------- | ---- | ------------ | ------ | --------- | ------------- |
| 014   | $82,140   | +8%  | 1,230        | 55%    | $4,210    | 1 (offline)   |
| 008   | $73,004   | -2%  | 1,110        | 51%    | $5,900    | 2 (shrink)    |
| ... (virtualized)                                                              |
+--------------------------------------------------------------------------------+
```

## Interaction Notes
- KPI tiles act as filters; clicking "Refund Rate" highlights rows contributing to variance.
- Exception feed is real-time and shareable; clicking opens side drawer with audit trail and resolution workflow.
- Export panel shows latest generated files, plus ability to subscribe managers to recurring deliveries.
- Detail table supports sticky headers, infinite scroll, and CSV copy respecting row-level security.
- Compare-to selector redraws charts + table variance columns (vs. LY, vs. plan, custom baseline).
