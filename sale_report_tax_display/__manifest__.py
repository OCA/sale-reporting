# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale report tax display",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Sale",
    "depends": [
        "sale",
        "account",
    ],
    "data": [
        "views/res_partner_views.xml",
        "report/report_invoice.xml",
        "report/ir_actions_report_templates.xml",
    ],
    "website": "https://github.com/OCA/sale-reporting",
    "installable": True,
}
