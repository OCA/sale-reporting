# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests.common import users

from odoo.addons.sale_report_delivered.tests.test_sale_report_delivered import (
    TestSaleReportDeliveredBase,
)


class TestSaleReportDeliveredDeposit(TestSaleReportDeliveredBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_deposit = cls.env["product.product"].create(
            {"name": "Test product Deposit", "type": "product", "list_price": 10}
        )
        cls.deposit_wh = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)]
        )
        cls.deposit_wh.use_customer_deposits = True
        cls._create_stock_quant(cls, cls.product_deposit)
        cls.order_deposit = cls._create_order(cls, cls.product_deposit)
        cls.order_deposit.customer_deposit = True
        cls.order_deposit.action_confirm()
        cls.order_deposit.picking_ids.action_confirm()
        cls.order_deposit.picking_ids.move_ids.write({"quantity_done": 1.0})
        cls.order_deposit.picking_ids.button_validate()

    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_deposit(self):
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", self.order_deposit.ids)]
        )
        self.assertIn(self.order_deposit, items.mapped("order_id"))
        self.assertIn(self.order_deposit.picking_ids, items.mapped("picking_id"))
        self.assertIn(self.product_deposit, items.mapped("product_id"))

    def _test_sale_report_delivered_deposit_read_group(self):
        self.product_deposit.stock_valuation_layer_ids.value = 1
        res = self.env["sale.report.delivered"].read_group(
            domain=[("order_id", "in", self.order_deposit.ids)],
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
    def test_sale_report_delivered_deposit_read_group_admin(self):
        self._test_sale_report_delivered_deposit_read_group()

    @users("test_user-sale_report_delivered")
    def test_sale_report_delivered_deposit_read_group(self):
        self._test_sale_report_delivered_deposit_read_group()
