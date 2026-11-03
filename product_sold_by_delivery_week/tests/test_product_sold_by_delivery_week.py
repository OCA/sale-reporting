# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import TransactionCase, new_test_user

from ..hooks import post_init_hook


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
                "type": "consu",
            }
        )
        cls.product_expense_product = cls.env["product.product"].create(
            {
                "name": "expense product for test",
                "type": "service",
            }
        )
        cls.product.weekly_sold_delivered = "000000"
        cls.product_expense_product.weekly_sold_delivered = "000000"
        # Tests should pass with basic sale and stock access rights
        cls.env = cls.env(
            user=new_test_user(
                cls.env,
                login="test_user",
                groups="stock.group_stock_user,sales_team.group_sale_salesman",
            )
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom_id": cls.product.uom_id.id,
                            "product_uom_qty": 3.0,
                        },
                    ),
                    (0, 0, {"display_type": "line_section", "name": "Section"}),
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_expense_product.id,
                            "product_uom_id": cls.product_expense_product.uom_id.id,
                            "product_uom_qty": 3.0,
                        },
                    ),
                ],
            }
        )

    def test_01_check_delivered_message_without_parameters(self):
        """Test the return message depending on the type of the product."""
        self.assertEqual(self.order.order_line[0].weekly_sold_delivered_shown, "◌◌◌◌◌◌")
        self.assertEqual(self.order.order_line[1].weekly_sold_delivered_shown, False)

    def test_02_check_delivered_message_with_parameters(self):
        """Test the definition of config parameters."""
        self.env["ir.config_parameter"].sudo().create(
            [
                {
                    "key": "product_sold_by_delivery_week.sold_char",
                    "value": "R",
                },
                {
                    "key": "product_sold_by_delivery_week.not_sold_char",
                    "value": "M",
                },
            ]
        )
        self.assertEqual(self.order.order_line[0].weekly_sold_delivered_shown, "MMMMMM")
        self.assertEqual(self.order.order_line[1].weekly_sold_delivered_shown, False)

    def test_03_sale_stock_delivery_partial(self):
        """Test a SO with a product on delivery."""
        # initial order
        self.order.action_confirm()
        self.assertTrue(
            self.order.picking_ids,
            "Sale Stock: no picking created for "
            '"invoice on delivery" storable products',
        )
        pick = self.order.picking_ids
        pick.move_ids.write({"quantity": 3})
        pick.button_validate()
        for line in pick.move_ids:
            line._action_done()
            self.assertEqual(line.product_id.weekly_sold_delivered, "000001")
            self.assertEqual(line.product_id.weekly_sold_delivered_shown, "◌◌◌◌◌●")

        partner_reporting = (
            self.order.order_line[0]
            .with_context(use_delivery_address=True)
            .get_partner_for_reporting()
        )
        self.assertEqual(partner_reporting, self.order.partner_shipping_id)

        self.env[
            "product.product"
        ].sudo()._action_recalculate_all_weekly_sold_delivered()
        weekly_res = (
            self.product.sudo()
            .with_context(weekly_warehouse_id=self.env.ref("stock.warehouse0").id)
            ._weekly_sold_delivered()
        )
        self.assertIn(self.product, weekly_res)

        tmpl = (
            self.env["product.template"].sudo().create({"name": "T", "type": "consu"})
        )
        attr = self.env["product.attribute"].sudo().create({"name": "A"})
        v1 = (
            self.env["product.attribute.value"]
            .sudo()
            .create({"name": "1", "attribute_id": attr.id})
        )
        v2 = (
            self.env["product.attribute.value"]
            .sudo()
            .create({"name": "2", "attribute_id": attr.id})
        )
        self.env["product.template.attribute.line"].sudo().create(
            {
                "product_tmpl_id": tmpl.id,
                "attribute_id": attr.id,
                "value_ids": [(6, 0, [v1.id, v2.id])],
            }
        )
        tmpl.product_variant_ids[0].sudo().weekly_sold_delivered = "01"
        tmpl.product_variant_ids[1].sudo().weekly_sold_delivered = "10"
        self.assertEqual(tmpl.weekly_sold_delivered, "000011")
        self.assertEqual(tmpl.weekly_sold_delivered_shown, "◌◌◌◌●●")

        self.assertTrue(self.product.product_tmpl_id.weekly_sold_delivered)

        tmpl_no_variant = (
            self.env["product.template"]
            .sudo()
            .create({"name": "No Variant", "type": "consu"})
        )
        tmpl_no_variant.product_variant_ids.sudo().action_archive()
        self.assertFalse(tmpl_no_variant.weekly_sold_delivered)

        products_no_company = (
            self.env["product.product"]
            .sudo()
            .search([("company_id", "=", False), ("type", "!=", "service")])
        )
        self.assertTrue(products_no_company)

        products_no_company.sudo().write({"company_id": self.env.company.id})
        self.assertTrue(all(products_no_company.mapped("company_id")))

        empty_company = self.env["res.company"].sudo().create({"name": "Empty"})
        self.assertEqual(empty_company.name, "Empty")

        self.env[
            "product.product"
        ].sudo()._action_recalculate_all_weekly_sold_delivered()
        products_no_company.sudo().write({"company_id": False})
        self.assertFalse(any(products_no_company.mapped("company_id")))

        original_method = type(self.env["product.product"])._weekly_sold_delivered
        type(self.env["product.product"])._weekly_sold_delivered = lambda self: {
            self.env["product.product"]: "000000"
        }
        previous_val = self.product.weekly_sold_delivered
        self.assertTrue(previous_val)
        self.product.sudo()._recalculate_weekly_sold_delivered()
        self.assertEqual(self.product.weekly_sold_delivered, previous_val)
        self.assertNotEqual(self.product.weekly_sold_delivered, "000000")
        type(self.env["product.product"])._weekly_sold_delivered = original_method

    def test_04_post_init_hook(self):
        """Test the post init hook"""
        post_init_hook(self.env)
        self.assertTrue(self.product.weekly_sold_delivered)
