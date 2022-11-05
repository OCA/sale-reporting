# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import users

from odoo.addons.sale_report_delivered.tests import test_sale_report_delivered


class TestSaleReportDeliveredBrand(
    test_sale_report_delivered.TestSaleReportDeliveredBase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["product.brand"].create({"name": "Test brand"})
        cls.product.product_brand_id = cls.brand
        cls.service.product_brand_id = cls.brand

    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_misc(self):
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", self.orders.ids)]
        )
        self.assertIn(self.brand, items.mapped("product_brand_id"))
