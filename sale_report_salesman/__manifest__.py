# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Report Salesman",
    "version": "15.0.1.0.0",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "category": "Sales",
    "license": "AGPL-3",
    "data": ["views/menu_views.xml"],
    "depends": ["sale", "sales_team"],
    "installable": True,
    "maintainers": ["carolina.fernandez"],
    "auto_install": True,
    "uninstall_hook": "uninstall_hook",
}
