# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    weekly_sold_delivered_catalog_shown = fields.Char(
        string="Weekly Sold for Catalog",
        compute="_compute_weekly_sold_delivered_catalog_shown",
        groups="sales_team.group_sale_salesman",
    )

    def _weekly_sold_delivered_shown_map(self, partner):
        """Return ``{product: formatted weekly string}`` for ``self`` computed
        live and filtered by ``partner`` (its commercial partner). Services are
        skipped."""
        products = self.filtered(lambda p: p.type != "service")
        if not products or not partner:
            return {}
        products_weekly = products.with_context(
            weekly_partner_id=partner.id,
        )._weekly_sold_delivered()
        return {
            product: self._format_weekly_string(products_weekly.get(product, False))
            for product in products
        }

    def _get_catalog_weekly_partner(self):
        """Return the partner to filter the weekly sales by when the product
        catalog is opened from a sale order, so the hint matches the
        recommendation wizard. Empty recordset in any other context."""
        if self.env.context.get("product_catalog_order_model") != "sale.order":
            return self.env["res.partner"]
        order_id = self.env.context.get("product_catalog_order_id")
        if not order_id:
            return self.env["res.partner"]
        order = self.env["sale.order"].browse(order_id).exists()
        return order.partner_id.commercial_partner_id

    @api.depends_context("product_catalog_order_model", "product_catalog_order_id")
    def _compute_weekly_sold_delivered_catalog_shown(self):
        """Live, customer-filtered weekly sales hint that replaces, in the
        product catalog opened from a sale order, the globally stored hint added
        by ``product_sold_by_delivery_week``."""
        self.weekly_sold_delivered_catalog_shown = False
        weekly_map = self._weekly_sold_delivered_shown_map(
            self._get_catalog_weekly_partner()
        )
        for product in self:
            product.weekly_sold_delivered_catalog_shown = weekly_map.get(product, False)
