# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.tools import column_exists, create_column

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    if not column_exists(cr, "sale_order_line", "invoice_date"):
        create_column(cr, "sale_order_line", "invoice_date", "date")
    if not column_exists(cr, "sale_order", "invoice_date"):
        create_column(cr, "sale_order", "invoice_date", "date")
    _logger.info("Initializing computed values for sale_order_line.invoice_date")
    cr.execute(
        """
        WITH sol AS (
            SELECT sol.id AS id, max(move.invoice_date) AS invoice_date
            FROM sale_order_line_invoice_rel rel
            INNER JOIN sale_order_line sol ON rel.order_line_id = sol.id
            INNER JOIN account_move_line aml ON rel.invoice_line_id = aml.id
            INNER JOIN account_move move ON aml.move_id = move.id
            WHERE sol.invoice_status = 'invoiced'
            GROUP BY sol.id
        )
        UPDATE sale_order_line
        SET invoice_date = sol.invoice_date
        FROM sol WHERE sale_order_line.id = sol.id
        """
    )
    _logger.info("Initializing computed values for sale_order.invoice_date")
    cr.execute(
        """
        WITH so AS (
            SELECT so.id AS id, max(sol.invoice_date) AS invoice_date
            FROM sale_order_line sol
            INNER JOIN sale_order so ON sol.order_id = so.id
            WHERE so.invoice_status = 'invoiced' AND sol.invoice_date IS NOT NULL
            GROUP BY so.id
        )
        UPDATE sale_order
        SET invoice_date = so.invoice_date
        FROM so WHERE sale_order.id = so.id
        """
    )
