# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from datetime import date, timedelta

from odoo import fields
from odoo.tests import TransactionCase


class TestBlanketOrderLinePosition(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_order_obj = cls.env["sale.blanket.order"]
        cls.blanket_order_line_obj = cls.env["sale.blanket.order.line"]
        cls.blanket_order_wiz_obj = cls.env["sale.blanket.order.wizard"]
        cls.so_obj = cls.env["sale.order"]

        cls.payment_term = cls.env.ref("account.account_payment_term_immediate")
        cls.sale_pricelist = cls.env["product.pricelist"].create(
            {"name": "Test Pricelist", "currency_id": cls.env.ref("base.USD").id}
        )

        # UoM
        cls.categ_unit = cls.env.ref("uom.product_uom_categ_unit")
        cls.uom_dozen = cls.env["uom.uom"].create(
            {
                "name": "Test-DozenA",
                "category_id": cls.categ_unit.id,
                "factor_inv": 12,
                "uom_type": "bigger",
                "rounding": 0.001,
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TEST CUSTOMER",
                "property_product_pricelist": cls.sale_pricelist.id,
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Demo",
                "categ_id": cls.env.ref("product.product_category_1").id,
                "standard_price": 35.0,
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "default_code": "PROD_DEL01",
            }
        )
        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Demo 2",
                "categ_id": cls.env.ref("product.product_category_1").id,
                "standard_price": 50.0,
                "type": "consu",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "default_code": "PROD_DEL02",
            }
        )

        cls.tomorrow = date.today() + timedelta(days=1)

        cls.blanket_order = cls.blanket_order_obj.create(
            {
                "partner_id": cls.partner.id,
                "validity_date": fields.Date.to_string(cls.tomorrow),
                "payment_term_id": cls.payment_term.id,
                "pricelist_id": cls.sale_pricelist.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "original_uom_qty": 20.0,
                            "price_unit": 1.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "original_uom_qty": 10.0,
                            "price_unit": 1.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "original_uom_qty": 5.0,
                            "price_unit": 1.0,
                        },
                    ),
                ],
            }
        )

    def test_new_line_position(self):
        """Check that new line created get a new incremental position number."""
        line1 = self.blanket_order.line_ids[0]
        self.assertEqual(line1.position, 1)
        self.assertEqual(line1.position_formatted, "001")
        line2 = self.blanket_order.line_ids[1]
        self.assertEqual(line2.position, 2)
        self.assertEqual(line2.position_formatted, "002")
        line3 = self.blanket_order.line_ids[2]
        self.assertEqual(line3.position, 3)
        self.assertEqual(line3.position_formatted, "003")
        line4 = self.env["sale.blanket.order.line"].create(
            [
                {
                    "order_id": self.blanket_order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "original_uom_qty": 9.0,
                },
            ]
        )
        self.assertEqual(line4.position, 4)
        self.assertEqual(line4.position_formatted, "004")

    def test_unlink_line(self):
        """Check that when line are being removed position are recomputed."""
        self.assertEqual(len(self.blanket_order.line_ids), 3)
        self.blanket_order.line_ids[0].unlink()
        self.assertEqual(len(self.blanket_order.line_ids), 2)
        self.assertEqual(self.blanket_order.line_ids[0].position, 1)

    def test_unlink_no_recompute_line(self):
        """Check that when  parameter disable_sale_position_recompute is True
        and line are being removed position are not recomputed."""
        self.blanket_order.company_id.disable_sale_position_recompute = True
        self.assertEqual(len(self.blanket_order.line_ids), 3)
        self.blanket_order.line_ids[0].unlink()
        self.assertEqual(len(self.blanket_order.line_ids), 2)
        self.assertEqual(self.blanket_order.line_ids[1].position, 3)

    def test_locked_positions(self):
        """Check that when blanket order is open, position are not recomputed."""
        new_line = self.env["sale.blanket.order.line"].create(
            [
                {
                    "order_id": self.blanket_order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "original_uom_qty": 15.0,
                    "price_unit": 1.0,
                },
            ]
        )
        self.assertEqual(new_line.position, 4)
        self.blanket_order.action_confirm()
        self.blanket_order.line_ids[0].unlink()
        self.assertEqual(new_line.position, 4)
