# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    price_subtotal_delivered = fields.Float(string="Subtotal Delivered")
    weight_delivered = fields.Float("Gross Weight Delivered")

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if fields is None:
            fields = {}
        select_str_price = """ ,
            sum((l.price_subtotal /
                 coalesce(nullif(l.product_uom_qty, 0), 1)
                ) * l.qty_delivered)
            as price_subtotal_delivered
        """
        select_str_weight = """ ,
            sum(p.weight * l.qty_delivered /
                u.factor * u2.factor) as weight_delivered
        """
        fields.update(
            {
                "price_subtotal_delivered": select_str_price,
                "weight_delivered": select_str_weight,
            }
        )
        return super()._query(
            with_clause=with_clause,
            fields=fields,
            groupby=groupby,
            from_clause=from_clause,
        )
