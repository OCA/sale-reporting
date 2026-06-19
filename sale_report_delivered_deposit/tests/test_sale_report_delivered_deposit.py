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
        cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)]
        ).use_customer_deposits = True

    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_deposit(self):
        product_deposit = self._create_product(
            "Test product Deposit", "product", list_price=10, stock_qty=1
        )
        order_deposit = self._create_order(product_deposit, confirm=True)
        self._validate_pickings(order_deposit.picking_ids, 1.0)
        self.env.invalidate_all()
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", order_deposit.ids)]
        )
        self.assertIn(order_deposit, items.mapped("order_id"))
        self.assertIn(order_deposit.picking_ids, items.mapped("picking_id"))
        self.assertIn(product_deposit, items.mapped("product_id"))

    def _test_sale_report_delivered_deposit_read_group(self):
        product_deposit = self._create_product(
            "Test product Deposit",
            "product",
            list_price=10,
            standard_price=3,
            stock_qty=1,
        )
        order_deposit = self._create_order(product_deposit, confirm=True)
        self._validate_pickings(order_deposit.picking_ids, 1.0)
        self.env.invalidate_all()
        res = self.env["sale.report.delivered"].read_group(
            domain=[("order_id", "in", order_deposit.ids)],
            fields=[
                "order_id",
                "margin_percent:sum",
                "price_subtotal:sum",
                "margin:sum",
            ],
            groupby=["order_id"],
        )
        self.assertAlmostEqual(res[0]["margin_percent"], 70.00)

    @users("admin")
    def test_sale_report_delivered_deposit_read_group_admin(self):
        self._test_sale_report_delivered_deposit_read_group()

    @users("test_user-sale_report_delivered")
    def test_sale_report_delivered_deposit_read_group(self):
        self._test_sale_report_delivered_deposit_read_group()
