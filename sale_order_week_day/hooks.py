# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api

from odoo.addons.base_week_day.hooks import populate_date_order_week_day


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    populate_date_order_week_day(
        env,
        "sale_order_week_day",
        "sale.order",
        "date_order_week_day",
        "date_order",
    )
    populate_date_order_week_day(
        env,
        "sale_order_week_day",
        "sale.order",
        "create_date_week_day",
        "create_date",
    )
