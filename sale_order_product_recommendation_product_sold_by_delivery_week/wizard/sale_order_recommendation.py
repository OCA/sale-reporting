# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderRecommendationLine(models.TransientModel):
    _inherit = "sale.order.recommendation.line"

    qty_available = fields.Float(
        "Qty. On Hand", related="product_id.qty_available", readonly=True
    )
    weekly_sold_delivered_shown = fields.Char(
        string="Weekly Sold",
        compute="_compute_weekly_sold_delivered_shown",
    )

    @api.depends("product_id")
    def _compute_weekly_sold_delivered_shown(self):
        """Compute dinamically in the view"""
        self.weekly_sold_delivered_shown = False
        common_partner = self.wizard_id.order_id.partner_id.commercial_partner_id
        weekly_map = self.mapped("product_id")._weekly_sold_delivered_shown_map(
            common_partner
        )
        for line in self:
            line.weekly_sold_delivered_shown = weekly_map.get(line.product_id, False)
