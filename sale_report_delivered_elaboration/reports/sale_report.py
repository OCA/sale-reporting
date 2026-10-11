# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReportDeliverd(models.Model):
    _inherit = "sale.report.delivered"

    elaboration_cost = fields.Float("Elaboration cost", readonly=True)

    def _select(self):
        select_str = super()._select()
        select_str += """
            , sum(signed_qty * unsigned_elaboration_cost) AS elaboration_cost
        """
        return select_str

    def _sub_select(self):
        sub_select_str = super()._sub_select()
        sub_select_str += """
            , COALESCE(sm.product_uom_qty, 0.0) * sol.elaboration_cost_price /
                CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0
                    ELSE s.currency_rate END as unsigned_elaboration_cost
        """
        return sub_select_str
