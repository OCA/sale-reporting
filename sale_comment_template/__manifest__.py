# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# Copyright 2018 Qubiq - Xavier Jiménez
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Comments",
    "summary": "Comments texts templates on Sale documents",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Camptocamp, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale",
        "account_comment_template",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/base_comment_template_view.xml",
        "views/report_saleorder.xml",
        "security/ir.model.access.csv",
    ],
}
