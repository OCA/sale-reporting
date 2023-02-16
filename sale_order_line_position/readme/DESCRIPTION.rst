This module adds an auto computed position on sale order line.
This position number is also printed on the report.

The position can be used to keep track of each line during
the delivery and invoicing of the order with the customer.
This is why there are related modules on `account-invoice-reporting`
and `stock-logisics-reporting`.

The positions are recomputed when the sale order is printed, sent and set to confirm.

The positions are not changed on the line after the order has been confirmed, but if
new line are added they will receive a position number.

An action is also availabled to manually recompute the positions.
