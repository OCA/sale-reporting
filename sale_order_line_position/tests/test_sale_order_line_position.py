# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SavepointCase


class TestSaleOrderLinePosition(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_9")
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 3.0,
                        },
                    ),
                    (0, 0, {"display_type": "line_section", "name": "Section"}),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 5.0,
                        },
                    ),
                ],
            }
        )

    def test_new_line_position(self):
        """Check that new line created get a new incremental position number."""
        line1 = self.order.order_line[0]
        self.assertEqual(line1.position, 1)
        self.assertEqual(line1.position_formatted, "001")
        line2 = self.order.order_line[1]
        self.assertEqual(line2.position, 0)
        self.assertEqual(line2.position_formatted, "")
        line3 = self.env["sale.order.line"].create(
            [
                {
                    "order_id": self.order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "product_uom_qty": 9.0,
                },
            ]
        )
        self.assertEqual(line3.position, 3)
        self.assertEqual(line3.position_formatted, "003")

    def test_unlink_line(self):
        """Check that when line are being removed position are recomputed."""
        self.order.order_line[0].unlink()
        self.assertEqual(len(self.order.order_line), 2)
        self.assertEqual(self.order.order_line[1].position, 1)

    def test_locked_positions(self):
        """Check that when order is sent, position are not recomputed."""
        new_line = self.env["sale.order.line"].create(
            [
                {
                    "order_id": self.order.id,
                    "product_id": self.product.id,
                    "product_uom": self.product.uom_id.id,
                    "product_uom_qty": 15.0,
                },
            ]
        )
        self.assertEqual(new_line.position, 3)
        self.order.state = "sent"
        self.order.order_line[0].unlink()
        self.assertEqual(new_line.position, 3)
