# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleReportDelivered(models.Model):
    _inherit = "sale.report.delivered"

    product_brand_id = fields.Many2one(comodel_name="product.brand", string="Brand")

    def _select(self):
        select_str = super()._select()
        select_str += ", sub.product_brand_id"
        return select_str

    def _sub_select(self):
        sub_select_str = super()._sub_select()
        sub_select_str += ", t.product_brand_id as product_brand_id"
        return sub_select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", sub.product_brand_id"
        return group_by_str
