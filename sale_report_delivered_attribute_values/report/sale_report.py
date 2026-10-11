# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class SaleReportDelivered(models.Model):
    _inherit = "sale.report.delivered"

    sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        readonly=True,
    )

    # This table is not generated here because we are using the original table
    # since the id of this report is the id of the sale order line
    all_product_attribute_value_ids = fields.Many2many(
        related="sale_line_id.all_product_attribute_value_ids",
        relation="sale_order_line_all_product_attribute_value_rel",
        column1="sale_order_line_id",
        column2="product_attribute_value_id",
        readonly=True,
        store=True,  # To allow grouping by this field
    )

    def _select(self):
        """Add sale order line to the select query"""
        res = super()._select()
        res += ", sub.id as sale_line_id"
        return res

    def _group_by(self):
        """Add sale order line to the group by query"""
        res = super()._group_by()
        res += ", sub.id"
        return res
