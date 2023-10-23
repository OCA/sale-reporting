# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    price_subtotal_delivered = fields.Float(string="Untaxed Total Delivered")
    weight_delivered = fields.Float("Gross Weight Delivered")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        select_str_price = """
            sum(
                CASE WHEN l.price_subtotal <> 0
                    THEN (l.price_subtotal / l.product_uom_qty)
                    ELSE l.price_reduce
                END
                * l.qty_delivered)
        """
        select_str_weight = """
            sum(p.weight * l.qty_delivered / u.factor * u2.factor)
        """
        res.update(
            {
                "price_subtotal_delivered": select_str_price,
                "weight_delivered": select_str_weight,
            }
        )
        return res
