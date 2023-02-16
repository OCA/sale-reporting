The way the positions are computed on the create of `sale.order.line`
record could lead to a performance issue. There is a few improvements
that have been suggested:

Remove it and handle the computation on the write and/or create
method of the `sale.order`.

Have a context key to enable/disable the recomputation.

Do not set any value in the position fields before the sale order lines
are locked (in the current implementation, before sending).
And add a recompute button in the UI.

Set the position values with an SQL query using a `TRIGGER`.
