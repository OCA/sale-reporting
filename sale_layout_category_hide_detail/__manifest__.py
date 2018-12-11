# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale layout category hide detail",
    "summary": "Hide details for sections in sales orders and invoices for "
               "reports and customer portal",
    "version": "11.0.1.0.0",
    "category": "Sales Management",
    "website": "http://github.com/OCA/sale-reporting",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
    ],
    "data": [
        "views/sale_layout_category_view.xml",
        "views/sale_order_report_templates.xml",
        "views/sale_portal_templates.xml",
        "views/invoice_report_templates.xml",
        "views/account_portal_templates.xml",
    ],
    "application": False,
    'installable': True,
}
