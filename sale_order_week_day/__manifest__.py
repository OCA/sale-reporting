# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Day of Week",
    "summary": "Filter/group Sale Orders by Day of Week",
    "version": "14.0.1.0.0",
    "author": "PyTech, Odoo Community Association (OCA)",
    "maintainers": [
        "SirPyTech",
    ],
    "website": "https://github.com/OCA/sale-reporting",
    "license": "AGPL-3",
    "depends": [
        "base_week_day",
        "sale",
    ],
    "data": [
        "views/sale_order_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
