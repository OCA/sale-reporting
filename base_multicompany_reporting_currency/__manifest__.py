# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Base Multicompany Reporting Currency",
    "summary": "Adds the possibility to specify Multicompany Reporting Currency",
    "version": "15.0.1.0.1",
    "category": "Sales",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["base_setup"],
    "website": "https://github.com/OCA/sale-reporting",
    "data": [
        "data/default_multicompany_reporting_currency.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
