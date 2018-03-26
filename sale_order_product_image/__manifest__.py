# -*- coding: utf-8 -*-
# © 2018 Exo Software, Lda.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Images on Sales Orders",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "EXO Software, "
              "Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "https://www.exo.pt",
    "category": "Sale",
    "depends": ["sale", "web_tree_image"],
    "data": [
        "views/report_saleorder.xml",
        "views/sale_order_views.xml",
        "views/res_config_views.xml",
    ],
    "demo": [],
    "auto_install": False,
    "installable": True,
}
