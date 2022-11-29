# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Blanket 0rder Line Position",
    "summary": "Adds position number on blanket order line.",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/sale-reporting",
    "depends": ["sale_blanket_order", "sale_order_line_position"],
    "data": [
        "views/blanket_order_views.xml",
        "report/templates.xml",
    ],
    "installable": True,
}
