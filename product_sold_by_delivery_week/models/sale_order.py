# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    weekly_sold_delivered_shown = fields.Char(
        string="Weekly Sold",
        compute="_compute_weekly_sold_delivered_shown",
    )

    def get_partner_for_reporting(self):
        """get partner from line taking into account context parameters"""
        if self.env.context.get("use_delivery_address", False):
            return self.order_id.partner_shipping_id
        return self.order_id.partner_id.commercial_partner_id

    @api.depends("order_id.partner_id", "order_id.warehouse_id", "product_id")
    def _compute_weekly_sold_delivered_shown(self):
        """Compute dinamically in the view"""
        _format_weekly_string = self.env["product.product"]._format_weekly_string
        self.weekly_sold_delivered_shown = False
        partner_products_dic = defaultdict(lambda: self.env["product.product"].browse())
        to_process_lines = self.filtered(
            lambda x: not x.display_type and x.product_id.type != "service"
        )
        # Create dict with products by partner
        for line in to_process_lines:
            partner = line.get_partner_for_reporting()
            partner_products_dic[partner] |= line.product_id
        partner_products_weekly = {}
        # Create dict with partner and product sold delivered info
        for partner, products in partner_products_dic.items():
            partner_products_weekly[partner] = products.with_context(
                weekly_partner_id=partner.id,
            )._weekly_sold_delivered()
        for line in to_process_lines:
            partner = line.get_partner_for_reporting()
            line.weekly_sold_delivered_shown = _format_weekly_string(
                partner_products_weekly[partner].get(line.product_id)
            )
