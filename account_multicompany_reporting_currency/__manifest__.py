# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Account Multicompany Reporting Currency",
    "summary": "Adds Amount in multicompany reporting currency to Account Moves",
    "version": "16.0.1.0.0",
    "category": "Accounting",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["account", "base_multicompany_reporting_currency"],
    "website": "https://github.com/OCA/sale-reporting",
    "data": ["views/account_move.xml"],
    "maintainers": ["yankinmax", "ivantodorovich"],
    "auto_install": True,
}
