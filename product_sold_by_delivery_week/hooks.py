# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(env):
    envs = api.Environment(env.cr, SUPERUSER_ID, {})
    envs["product.product"]._action_recalculate_all_weekly_sold_delivered()
