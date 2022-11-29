This module adds an auto computed position on blanket order line.
This position number is also printed on the report.

The position can be used to keep track of each line during
the sales , the delivery and invoicing of the order with the customer.
This is why it depends on `sale_order_line_position` and there are related modules on:
- `account-invoice-reporting`
- `stock-logisics-reporting`

The positions are recomputed when the blanket order is printed, sent and set to confirm.

The positions are not changed on the line after the blanket order has been confirmed, but if
new line are added they will receive a position number.

An action is also availabled to manually recompute the positions.
