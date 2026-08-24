# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def uninstall_hook(env):
    menu_sale_report = env.ref("sale.menu_sale_report", raise_if_not_found=False)
    if menu_sale_report:
        group_salesman = env.ref(
            "sales_team.group_sale_salesman", raise_if_not_found=False
        )
        if group_salesman:
            menu_sale_report.write({"groups_id": [(3, group_salesman.id)]})
