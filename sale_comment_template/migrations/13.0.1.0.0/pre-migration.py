# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Add temporary table for avoiding the automatic launch of the compute method
    openupgrade.logged_query(
        env.cr, "CREATE TABLE base_comment_template_sale_order_rel (temp int)",
    )
