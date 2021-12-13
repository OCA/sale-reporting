# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale layout category hide detail",
    "summary": "Hide details for sections in sale orders and invoices for "
    "reports and customer portal",
    "version": "14.0.1.0.0",
    "category": "Sales Management",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sale_management"],
    "data": [
        "views/assets.xml",
        "views/account_move_view.xml",
        "views/invoice_report_templates.xml",
        "views/sale_views.xml",
        "views/sale_order_report_templates.xml",
        "views/sale_portal_templates.xml",
    ],
    "application": False,
    "installable": True,
}
