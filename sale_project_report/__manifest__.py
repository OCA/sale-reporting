# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Project Report",
    "summary": """This module allows to display project name on sale report and in
    portal""",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "maintainers": ["rousseldenis"],
    "depends": [
        "sale",
        "project",
        "sale_project",
    ],
    "data": [
        "report/report_order_document.xml",
        "report/report_invoice_document.xml",
        "views/sale_portal.xml",
    ],
}
