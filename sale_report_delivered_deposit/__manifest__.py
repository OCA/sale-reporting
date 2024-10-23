# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Sale Report Delivered - Deposit",
    "summary": "Allow to view Customer Deposits on Sale Report Delivered",
    "version": "16.0.2.0.0",
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
        "stock_customer_deposit",
    ],
    "data": [],
}
