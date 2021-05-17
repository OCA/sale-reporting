# Copyright 2021 Tecnativa - Víctor Martínez
# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Remove temp table and re-create m2m table through ORM method
    openupgrade.logged_query(env.cr, "DROP TABLE base_comment_template_sale_order_rel")
    obj = env["sale.order"]
    obj._fields["comment_template_ids"].update_db(obj, False)
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO base_comment_template_sale_order_rel
        (base_comment_template_id, sale_order_id)
        SELECT so.comment_template1_id, so.id
        FROM sale_order so
        WHERE so.comment_template1_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO base_comment_template_sale_order_rel
        (base_comment_template_id, sale_order_id)
        SELECT so.comment_template2_id, so.id
        FROM sale_order so
        WHERE so.comment_template2_id IS NOT NULL
        ON CONFLICT DO NOTHING
        """,
    )
