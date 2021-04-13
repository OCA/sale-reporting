# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Product State History",
    "summary": """
        Allows to get a report on products per product state on date""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "category": "Sales",
    "maintainers": ["rousseldenis"],
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "depends": [
        "product_state_history",
        "sale",
        "sales_team",
    ],
    "data": [
        "views/product_state_history.xml",
    ],
}
