# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate_comment_template(cr):
    cr.execute(
        """
        UPDATE sale_order so
        SET comment_template1_id = bct.condition_template_id,
            note1 = bct.text
        FROM base_comment_template bct
        WHERE bct.id = so.condition_template_id
        AND bct.position = 'before_lines'
        """)
    cr.execute(
        """
        UPDATE sale_order so
        SET comment_template2_id = bct.condition_template_id,
            note2 = bct.text
        FROM base_comment_template bct
        WHERE bct.id = so.condition_template_id
        AND bct.position = 'after_lines'
        """)


@openupgrade.migrate()
def migrate(cr, version):
    if openupgrade.column_exists(cr, 'sale_order', 'condition_template_id'):
        migrate_comment_template(cr)
