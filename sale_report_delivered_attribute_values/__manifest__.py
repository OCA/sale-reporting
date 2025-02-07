# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Sale Report Delivered - Attribute Values",
    "summary": "Allow to view Attribute values of Lines on Sale Report Delivered",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide", "rafaelbn"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "sale_report_delivered",
        "sale_order_line_product_attribute_values",
    ],
    "data": [
        "views/sale_report_delivered_views.xml",
    ],
}
