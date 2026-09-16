# Copyright 2025 Tecnativa - Juan Carlos Oñate
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sales Team Invoiced Target Report",
    "version": "19.0.1.0.0",
    "author": "Tecnativa,Odoo Community Association (OCA)",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/sale-reporting",
    "depends": ["sale", "crm"],
    "data": [
        "views/crm_team_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sales_team_invoiced_target_report/static/src/**/*.scss",
        ],
    },
    "installable": True,
}
