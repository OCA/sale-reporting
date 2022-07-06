# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Sale 0rder Line Position",
    "summary": "Adds position number on sale order line.",
    "version": "15.0.1.1.0",
    "category": "Sales",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/sale-reporting",
    "depends": ["sale"],
    "data": [
        "views/sale_order.xml",
        "views/res_config_settings.xml",
        "report/sale_order_report.xml",
    ],
    "installable": True,
}
