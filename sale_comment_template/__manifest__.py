# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Qubiq - Xavier Jiménez
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Comments",
    "summary": "Comments texts templates on Sale documents",
    "version": "11.0.1.2.0",
    "depends": [
        "sale",
        "account_invoice_comment_template",
    ],
    "author": "Camptocamp,"
              "Tecnativa,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "data": [
        "views/sale_order_view.xml",
        'views/base_comment_template_view.xml',
        'views/report_saleorder.xml',
        'security/ir.model.access.csv',
    ],
    "category": "Sale",
    'installable': True,
}
