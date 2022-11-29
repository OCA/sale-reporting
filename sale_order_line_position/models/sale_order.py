# Copyright 2021-2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "order.position.mixin"]

    def recompute_positions(self):
        for sale in self:
            if sale.locked_positions or sale.company_id.disable_sale_position_recompute:
                continue
            lines = sale.order_line.filtered(lambda l: not l.display_type)
            lines.sorted(key=lambda x: (x.sequence, x.id))
            for position, line in enumerate(lines, start=1):
                line.position = position
