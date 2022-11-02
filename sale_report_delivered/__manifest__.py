# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Report Delivered",
    "version": "14.0.1.0.0",
    "author": "Tecnativa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "category": "Sales",
    "license": "AGPL-3",
    "depends": ["sale_stock", "sale_margin"],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["sergio-teruel"],
    "data": ["security/ir.model.access.csv", "views/sale_report_delivered_views.xml"],
}
