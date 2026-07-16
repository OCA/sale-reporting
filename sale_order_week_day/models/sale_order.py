# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.base_week_day.models.mixin import WEEKDAYS


class SaleOrder(models.Model):
    _inherit = [
        "base_week_day.mixin",
        "sale.order",
    ]
    _name = "sale.order"

    create_date_week_day = fields.Selection(
        selection=WEEKDAYS,
        compute="_compute_create_date_week_day",
        store=True,
        string="Creation Day of Week",
    )
    date_order_week_day = fields.Selection(
        selection=WEEKDAYS,
        compute="_compute_date_order_week_day",
        store=True,
        string="Order Day of Week",
    )

    @api.depends(
        "create_date",
    )
    def _compute_create_date_week_day(self):
        for order in self:
            order.create_date_week_day = order._get_week_day(order.create_date)

    @api.depends(
        "date_order",
    )
    def _compute_date_order_week_day(self):
        for order in self:
            order.date_order_week_day = order._get_week_day(order.date_order)
