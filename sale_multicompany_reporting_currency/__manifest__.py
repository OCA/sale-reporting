# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Multicompany Reporting Currency",
    "summary": "Adds Amount in multicompany reporting currency to Sale Order",
    "version": "15.0.1.0.2",
    "category": "Sales",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sale", "base_multicompany_reporting_currency"],
    "website": "https://github.com/OCA/sale-reporting",
    "data": [
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "maintainers": ["yankinmax"],
}
