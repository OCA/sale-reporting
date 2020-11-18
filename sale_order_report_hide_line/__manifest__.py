# Copyright (C) 2020 Radovan Skolnik
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hide sale order lines from the PDF report if the unit price is 0",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Radovan Skolnik, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": ["sale"],
    "data": ["views/sale_views.xml", "views/sale_report_templates.xml"],
    "installable": True,
    "license": "AGPL-3",
    "development_status": "Beta",
    "maintainers": ["Rad0van"],
}
