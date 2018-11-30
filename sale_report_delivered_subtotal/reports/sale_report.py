# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    price_subtotal_delivered = fields.Float(
        string='Total Price Delivered',
        readonly=True,
    )

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """,
            sum((l.price_subtotal /
                 coalesce(nullif(l.product_uom_qty, 0), 1)
                ) * l.qty_delivered)
            as price_subtotal_delivered
        """
        return select_str
