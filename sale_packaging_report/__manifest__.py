# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Sale Packaging Report",
    "summary": "Packaging data in sale reports",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["yajo"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale"],
    "data": [
        "report/sale_report_view.xml",
        "views/report_sale_order.xml",
    ],
}
