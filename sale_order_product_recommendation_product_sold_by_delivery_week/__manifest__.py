# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product weekly sales hint on sales recommendation wizard",
    "summary": "Adds the weekly sales field to the recommendation wizard",
    "version": "16.0.1.1.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu"],
    "license": "AGPL-3",
    "depends": ["product_sold_by_delivery_week", "sale_order_product_recommendation"],
    "auto_install": True,
    "data": ["wizard/sale_order_recommendation_view.xml"],
}
