# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tools.sql import column_exists, rename_column


def migrate(cr, version):
    if column_exists(cr, "res_company", "amount_option"):
        rename_column(
            cr, "res_company", "amount_option", "multicompany_reporting_amount"
        )
