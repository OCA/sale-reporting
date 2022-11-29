# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class OrderPositionMixin(models.AbstractModel):
    _name = "order.position.mixin"
    _description = "Order position mixin"

    locked_positions = fields.Boolean(compute="_compute_locked_positions")

    @api.depends("state")
    def _compute_locked_positions(self):
        for record in self:
            record.locked_positions = record.state != "draft"

    def action_confirm(self):
        self.recompute_positions()
        return super().action_confirm()

    def action_quotation_send(self):
        self.recompute_positions()
        return super().action_quotation_send()

    def recompute_positions(self):
        return NotImplementedError


class OrderLinePositionMixin(models.AbstractModel):
    _name = "order.line.position.mixin"
    _description = "Order line position mixin"

    position = fields.Integer(readonly=True, index=True, default=False)
    position_formatted = fields.Char(compute="_compute_position_formatted")

    @api.depends("position")
    def _compute_position_formatted(self):
        for record in self:
            record.position_formatted = record._format_position(record.position)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = self._add_next_position_on_new_line(vals_list)
        return super().create(vals_list)

    def unlink(self):
        sales = self.mapped("order_id")
        res = super().unlink()
        for sale in sales:
            sale.recompute_positions()
        return res

    def _add_next_position_on_new_line(self, vals_list):
        """Compute the nex position for the line"""
        return NotImplementedError

    @api.model
    def _format_position(self, position):
        if not position:
            return ""
        return str(position).zfill(3)
