# Copyright 2016 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleOrderWeight(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order_model = cls.env["sale.order"]
        cls.sale_order_line_model = cls.env["sale.order.line"]
        cls.partner = cls.env.ref("base.res_partner_3")
        cls.product_3 = cls.env.ref("product.product_product_3")
        cls.product_4 = cls.env.ref("product.product_product_4")
        cls.product_5 = cls.env.ref("product.product_product_5")

        order_vals = dict()
        order_vals["partner_id"] = cls.partner.id

        line_data = [
            Command.create(
                {
                    "product_id": cls.product_4.id,
                    "name": "product test 4",
                    "product_uom_qty": 1.0,
                    "product_uom": cls.product_4.uom_id.id,
                    "price_unit": cls.product_4.lst_price,
                },
            ),
            Command.create(
                {
                    "product_id": cls.product_5.id,
                    "name": "product test 5",
                    "product_uom_qty": 2.0,
                    "product_uom": cls.product_5.uom_id.id,
                    "price_unit": cls.product_5.lst_price,
                },
            ),
            Command.create(
                {
                    "product_id": cls.product_3.id,
                    "name": "product test 3",
                    "product_uom_qty": 3.0,
                    "product_uom": cls.product_3.uom_id.id,
                    "price_unit": cls.product_3.lst_price,
                },
            ),
        ]
        order_vals["order_line"] = line_data
        cls.sale_order = cls.sale_order_model.create(order_vals)

    def test_total_weight(self):
        # Change weight
        self.product_3.weight = 2.0  # 3.0
        self.product_4.weight = 10.0  # 1.0
        self.product_5.weight = 1.0  # 2.0
        # check total weight
        self.assertEqual(self.sale_order.total_weight(), 18.0)
