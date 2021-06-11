# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    locked_positions = fields.Boolean(compute="_compute_locked_positions")

    @api.depends("state")
    def _compute_locked_positions(self):
        for record in self:
            record.locked_positions = record.state != "draft"

    def action_quotation_send(self):
        self.recompute_positions()
        return super().action_quotation_send()

    def recompute_positions(self):
        self.ensure_one()
        if self.locked_positions:
            return
        lines = self.order_line.filtered(lambda l: not l.display_type)
        lines.sorted(key=lambda x: x.sequence)
        for position, line in enumerate(lines, start=1):
            line.position = position
