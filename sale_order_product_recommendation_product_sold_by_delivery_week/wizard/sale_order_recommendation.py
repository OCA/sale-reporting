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
        _format_weekly_string = self.env["product.product"]._format_weekly_string
        self.weekly_sold_delivered_shown = False
        products = self.mapped("product_id").filtered(lambda x: x.type != "service")
        common_partner = self.wizard_id.order_id.partner_id.commercial_partner_id
        products_weekly = products.with_context(
            weekly_partner_id=common_partner.id,
        )._weekly_sold_delivered()
        for line in self.filtered(lambda x: x.product_id.type != "service"):
            line.weekly_sold_delivered_shown = _format_weekly_string(
                products_weekly.get(line.product_id, False)
            )
