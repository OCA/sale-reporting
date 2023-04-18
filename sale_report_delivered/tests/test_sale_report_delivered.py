# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common, new_test_user
from odoo.tests.common import users


class TestSaleReportDeliveredBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.admin = cls.env.ref("base.user_admin")
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": cls.company.currency_id.id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test partner", "property_product_pricelist": cls.pricelist.id}
        )
        cls.user = new_test_user(
            cls.env,
            login="test_user-sale_report_delivered",
            name="test_user-one",
            groups="sales_team.group_sale_manager",
        )
        group_sale_manager = cls.env.ref("sales_team.group_sale_manager")
        group_sale_manager.write({"users": [(4, cls.admin.id)]})

        cls.product = cls.env["product.product"].create(
            {"name": "Test product", "type": "product", "list_price": 10}
        )
        cls._create_stock_quant(cls, cls.product)
        cls.service = cls.env["product.product"].create(
            {"name": "Test service", "type": "service", "list_price": 10}
        )
        cls.order_1 = cls._create_order(cls, cls.product)
        cls.order_2 = cls._create_order(cls, cls.service)
        cls.orders = cls.order_1 + cls.order_2
        cls.orders.action_confirm()
        cls.orders.picking_ids.action_confirm()
        cls.orders.picking_ids.move_ids.write({"quantity_done": 1.0})
        cls.orders.picking_ids.button_validate()

    def _create_stock_quant(self, product):
        res = product.action_update_quantity_on_hand()
        quant_form = Form(
            self.env["stock.quant"].with_context(**res["context"]),
            view="stock.view_stock_quant_tree_inventory_editable",
        )
        quant_form.inventory_quantity = 1
        quant_form.location_id = self.env.ref("stock.stock_location_stock")
        return quant_form.save()

    def _create_order(self, product):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = product
            line_form.product_uom_qty = 1
        return order_form.save()


class TestSaleReportDelivered(TestSaleReportDeliveredBase):
    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_misc(self):
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", self.orders.ids)]
        )
        self.assertIn(self.order_1, items.mapped("order_id"))
        self.assertNotIn(self.order_2, items.mapped("order_id"))
        self.assertIn(self.order_1.picking_ids, items.mapped("picking_id"))
        self.assertIn(self.product, items.mapped("product_id"))
        self.assertNotIn(self.service, items.mapped("product_id"))

    def _test_sale_report_delivered_read_group(self):
        self.product.stock_valuation_layer_ids.value = 1
        res = self.env["sale.report.delivered"].read_group(
            domain=[("order_id", "in", self.orders.ids)],
            fields=[
                "order_id",
                "margin_percent:sum",
                "price_subtotal:sum",
                "margin:sum",
            ],
            groupby=["order_id"],
        )
        self.assertAlmostEqual(res[0]["margin_percent"], 100.00)

    @users("admin")
    def test_sale_report_delivered_read_group_admin(self):
        self._test_sale_report_delivered_read_group()

    @users("test_user-sale_report_delivered")
    def test_sale_report_delivered_read_group(self):
        self._test_sale_report_delivered_read_group()
