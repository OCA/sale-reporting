# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    price_subtotal_delivered = fields.Float(string="Total Price Delivered")

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if fields is None:
            fields = {}
        select_str = """ ,
            sum((l.price_subtotal /
                 coalesce(nullif(l.product_uom_qty, 0), 1)
                ) * l.qty_delivered)
            as price_subtotal_delivered
        """
        fields.update({"price_subtotal_delivered": select_str})
        return super()._query(
            with_clause=with_clause,
            fields=fields,
            groupby=groupby,
            from_clause=from_clause,
        )
