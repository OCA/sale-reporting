# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Report Address Grouping",
    "summary": """
        This module allows to better render invoicing and shipping adresses""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "maintainers": ["rousseldenis"],
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "depends": [
        "sale",
    ],
    "data": [
        "report/saleorder_document.xml",
    ],
}
