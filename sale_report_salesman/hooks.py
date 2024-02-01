# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Remove group from the menu 'sale.menu_sale_report'
    menu_sale_report = env.ref("sale.menu_sale_report", raise_if_not_found=False)
    if menu_sale_report:
        groups_to_remove = [
            env.ref("sales_team.group_sale_salesman"),
        ]
        menu_sale_report.write(
            {"groups_id": [(3, group.id) for group in groups_to_remove]}
        )
