# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class BlanketOrder(models.Model):
    _name = "sale.blanket.order"
    _inherit = ["sale.blanket.order", "order.position.mixin"]

    def recompute_positions(self):
        for blanket in self:
            if (
                blanket.locked_positions
                or blanket.company_id.disable_sale_position_recompute
            ):
                continue
            lines = blanket.line_ids.filtered(lambda l: not l.display_type)
            lines.sorted(key=lambda x: (x.sequence, x.id))
            for position, line in enumerate(lines, start=1):
                line.position = position
