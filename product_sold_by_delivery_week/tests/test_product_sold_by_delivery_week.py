# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import TransactionCase


class TestProductSoldByDeliveryWeek(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner for testing",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "detailed_type": "consu",
            }
        )
        cls.product_expense_product = cls.env["product.product"].create(
            {
                "name": "expense product for test",
                "detailed_type": "service",
            }
        )
        cls.product.weekly_sold_delivered = "Sold delivered"
        cls.product_expense_product.weekly_sold_delivered = "Sold delivered service"
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
                            "product_id": cls.product_expense_product.id,
                            "product_uom": cls.product_expense_product.uom_id.id,
                            "product_uom_qty": 3.0,
                        },
                    ),
                ],
            }
        )

    def test_01_check_delivered_message_without_parameters(self):
        """Test the return message deppending on the type of the product."""
        self.assertEqual(self.order.order_line[0].weekly_sold_delivered_shown, "◌◌◌◌◌◌")
        self.assertEqual(self.order.order_line[1].weekly_sold_delivered_shown, False)

    def test_02_check_delivered_message_with_parameters(self):
        """Test the definition of config parameters."""
        self.env["ir.config_parameter"].create(
            {
                "key": "product_sold_by_delivery_week.sold_char",
                "value": "R",
            }
        )
        self.env["ir.config_parameter"].create(
            {
                "key": "product_sold_by_delivery_week.not_sold_char",
                "value": "M",
            }
        )
        self.assertEqual(self.order.order_line[0].weekly_sold_delivered_shown, "MMMMMM")
        self.assertEqual(self.order.order_line[1].weekly_sold_delivered_shown, False)

    def test_03_sale_stock_delivery_partial(self):
        """Test a SO with a product on delivery."""
        # intial order
        self.order.action_confirm()
        self.assertTrue(
            self.order.picking_ids,
            'Sale Stock: no picking created for "invoice on delivery" storable products',
        )
        pick = self.order.picking_ids
        pick.move_ids.write({"quantity_done": 3})
        pick.button_validate()
        for line in pick.move_ids:
            line._action_done()
            self.assertEqual(line.product_id.weekly_sold_delivered, "Sold delivered")
