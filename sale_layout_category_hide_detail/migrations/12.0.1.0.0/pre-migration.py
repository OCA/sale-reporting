# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr, """
        UPDATE sale_order_line sol
        SET show_details = NOT slc.hide_details,
            show_subtotal = slc.subtotal
        FROM sale_layout_category slc
        WHERE slc.id = sol.layout_category_id
            AND display_type = 'line_section'
        """,
    )
    openupgrade.logged_query(
        env.cr, """
        UPDATE account_invoice_line ail
        SET show_details = NOT slc.hide_details,
            show_subtotal = slc.subtotal
        FROM sale_layout_category slc
        WHERE slc.id = ail.layout_category_id
            AND display_type = 'line_section'
        """,
    )
