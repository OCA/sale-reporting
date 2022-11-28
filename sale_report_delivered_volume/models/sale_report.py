# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    volume_delivered = fields.Float(digits="Volume")

    def _select_sale(self, fields=None):
        select_str = super()._select_sale(fields=fields)
        select_str += """
        , CASE
            WHEN l.product_id IS NOT NULL THEN sum(
                p.volume * l.qty_delivered / u.factor * u2.factor
            )
            ELSE 0
            END as volume_delivered
        """
        return select_str
