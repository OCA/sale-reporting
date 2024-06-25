# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale layout category hide detail",
    "summary": "Hide details for sections in sale orders and invoices for "
    "reports and customer portal",
    "version": "16.0.1.1.1",
    "category": "Sales Management",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["sale_management"],
    "data": [
        "views/account_move_view.xml",
        "views/invoice_report_templates.xml",
        "views/sale_views.xml",
        "views/sale_order_report_templates.xml",
        "views/sale_portal_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sale_layout_category_hide_detail/static/src/js/**",
            "sale_layout_category_hide_detail/static/src/xml/*.xml",
        ],
    },
    "application": False,
    "installable": True,
}
