# Copyright 2026 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Sale Report Delivered - Price Compliance",
    "summary": "Allow to view Price Compliance Tiers on Sale Report Delivered",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide", "rafaelbn"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_report_delivered",
        "sale_price_compliance",
    ],
    "data": [
        "views/sale_report_delivered_views.xml",
    ],
}
