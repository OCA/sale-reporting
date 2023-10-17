# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = ["sale.order.line", "display.line.mixin"]

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.order_id.calc_order_lines_dependencies()
        return res

    def write(self, vals):
        res = super().write(vals)
        if any(fname in vals for fname in ["order_id", "sequence"]):
            self.order_id.calc_order_lines_dependencies()
        return res
