# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    volume_delivered = fields.Float(digits="Volume")

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        select_str_volume_delivered = """
           CASE
            WHEN l.product_id IS NOT NULL THEN sum(
                p.volume * l.qty_delivered / u.factor * u2.factor
            )
            ELSE 0
            END
        """
        res.update(
            {
                "volume_delivered": select_str_volume_delivered,
            }
        )
        return res
