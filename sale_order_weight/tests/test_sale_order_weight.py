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
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test Product 1",
                "type": "consu",
                "lst_price": 100.0,
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Test Product 2",
                "type": "consu",
                "lst_price": 150.0,
            }
        )
        cls.product_3 = cls.env["product.product"].create(
            {
                "name": "Test Product 3",
                "type": "consu",
                "lst_price": 200.0,
            }
        )

        order_vals = dict()
        order_vals["partner_id"] = cls.partner.id

        line_data = [
            Command.create(
                {
                    "product_id": cls.product_2.id,
                    "name": "product test 2",
                    "product_uom_qty": 1.0,
                    "product_uom_id": cls.product_2.uom_id.id,
                    "price_unit": cls.product_2.lst_price,
                },
            ),
            Command.create(
                {
                    "product_id": cls.product_3.id,
                    "name": "product test 3",
                    "product_uom_qty": 2.0,
                    "product_uom_id": cls.product_3.uom_id.id,
                    "price_unit": cls.product_3.lst_price,
                },
            ),
            Command.create(
                {
                    "product_id": cls.product_1.id,
                    "name": "product test 1",
                    "product_uom_qty": 3.0,
                    "product_uom_id": cls.product_1.uom_id.id,
                    "price_unit": cls.product_1.lst_price,
                },
            ),
        ]
        order_vals["order_line"] = line_data
        cls.sale_order = cls.sale_order_model.create(order_vals)

    def test_total_weight(self):
        # Change weight
        self.product_1.weight = 2.0  # 3.0
        self.product_2.weight = 10.0  # 1.0
        self.product_3.weight = 1.0  # 2.0
        # check total weight
        self.assertEqual(self.sale_order.total_weight(), 18.0)
