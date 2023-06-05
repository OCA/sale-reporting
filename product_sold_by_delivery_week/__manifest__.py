# Copyright 2021 Tecnativa - David Vidal
# Copyright 2021 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product weekly sales hint",
    "summary": "Adds a field that graphically hints the weekly product sales",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["sale_stock"],
    "data": [
        "data/ir_cron.xml",
        "security/product_sold_by_delivery_week_security.xml",
        "views/product_views.xml",
        "views/sale_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
