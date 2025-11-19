# Register Screen Wireframe

```
+--------------------------------------------------------------------------------+
| Header: Store Name            Register #04           Cashier: Maya    14:32    |
| Loyalty Status: Gold (23 visits)        Hardware: ✅ Printer  ✅ Scanner  ⚠️ PIN |
+--------------------------------------------------------------------------------+
| Customer Search [______________]   Loyalty: (Add)      Notes: [_________]       |
+----------------------------------+---------------------------------------------+
| Cart Items                       | Keypad / Quick Add                          |
| -------------------------------- | ------------------------------------------- |
| Qty | Item            | Price    | [7][8][9]  [Disc %] [Disc $] [Tax Override] |
|  1  | Cold Brew        4.50      | [4][5][6]  [Note]    [Gift Rcpt]             |
|  2  | Croissant        3.25      | [1][2][3]  [Custom $] [SKU Search]          |
|  1  | Mug              12.00     | [0][00][.] [Qty x]    [Weight]              |
| -------------------------------- | ------------------------------------------- |
| Subtotal:             $23.75     | Tender Buttons                              |
| Tax:                   $2.14     | [Card] [Cash] [Split] [Gift] [Store Credit] |
| Total:                $25.89     | [External Pay] [Park Cart]                  |
+----------------------------------+---------------------------------------------+
| Footer: Void Item | Return Mode | Save Cart | Parked Carts (3) | Notifications |
+--------------------------------------------------------------------------------+
```

## Interaction Notes
- Header now embeds loyalty + hardware health to reduce context switching.
- Customer search field supports barcode, phone, or loyalty code; results open side drawer.
- Keypad column doubles as action center—buttons morph contextually (e.g., tip entry after total).
- Parked cart pill opens modal with hold duration + cashier owner; managers can reclaim carts.
- Notifications icon surfaces device failures, low paper, or queue alerts sourced from telemetry service.
