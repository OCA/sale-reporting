# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(env):
    env["product.product"]._action_recalculate_all_weekly_sold_delivered()
