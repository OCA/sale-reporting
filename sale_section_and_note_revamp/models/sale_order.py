# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def calc_order_lines_dependencies(self):
        """Link order lines with their respective siblings"""
        for order in self:
            order.order_line.write(
                {"previous_line_id": False, "next_line_id": False})
            previous_line = self.env["sale.order.line"]
            for order_line in order.order_line.sorted("sequence"):
                order_line.write({"previous_line_id": previous_line.id})
                if previous_line:
                    previous_line.write({"next_line_id": order_line.id})
                previous_line = order_line
