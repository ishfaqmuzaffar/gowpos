# Inventory Screen Wireframe

```
+--------------------------------------------------------------------------------+
| Header: Inventory Dashboard             Store 014  |  Buyer: L. Chen  |  11:10 |
+--------------------------------------------------------------------------------+
| Filters: [Search SKU/Name__________] [Category v] [Status v] [Location v]      |
+---------------------------+----------------------+-----------------------------+
| Stock Overview            | Replenishment Queue  | Item Detail Panel           |
| ------------------------- | -------------------- | --------------------------- |
| OH Qty    Reorder  ETA    | 1. Espresso Beans    | SKU: 458100                 |
| 12,430    8,000    3 days | 2. Cold Brew Bottles | Name: Cold Brew 12oz 4pk    |
| Shrink: 1.2%              | 3. Ceramic Mugs      | On Hand: 140 (3 locs)       |
| Aging >60d: 3 SKUs        | 4. Syrup Pump        | On Order: 60 (ETA 2 days)   |
| Transfer In: 4            | 5. Gift Box          | Safety Stock: 50            |
| Transfer Out: 2           |                      | Status: BELOW MIN           |
| ------------------------- | -------------------- | --------------------------- |
| Alerts                    | Suggested Actions    | Movement History            |
| - 6 SKUs below min        | [Create PO] [Transfer]| 08:32 Sale -5 (Reg 04)     |
| - 2 cycle counts overdue  | [Mark Down] [Hold]    | 09:10 Return +1 (Reg 03)   |
| - Vendor ASN delayed      |                      | 09:45 Transfer Out -20      |
+---------------------------+----------------------+-----------------------------+
| Footer: [Cycle Count] [Print Shelf Labels] [Export CSV] [Report Issue]         |
+--------------------------------------------------------------------------------+
```

## Interaction Notes
- Left column aggregates KPIs; tapping tiles drills down to filtered item lists.
- Replenishment queue prioritizes items by combined forecast + safety stock breach.
- Item detail panel surfaces context-sensitive actions (create PO, transfer stock, mark down).
- Movement history keeps last 10 adjustments inline; full log opens side drawer with filters.
- Color coding: red = below min, amber = pending review, green = healthy.
