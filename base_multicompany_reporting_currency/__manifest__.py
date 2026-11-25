# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Base Multicompany Reporting Currency",
    "summary": "Adds the possibility to specify Multicompany Reporting Currency",
    "version": "19.0.1.1.0",
    "category": "Sales",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        # Odoo
        "base_setup",
    ],
    "website": "https://github.com/OCA/sale-reporting",
    "data": [
        # Views
        "views/res_config_settings.xml",
    ],
    "installable": True,
}
