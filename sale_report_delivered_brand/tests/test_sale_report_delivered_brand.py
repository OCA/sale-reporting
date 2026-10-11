# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import users

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
from odoo.addons.sale_report_delivered.tests import test_sale_report_delivered


class TestSaleReportDeliveredBrand(
    test_sale_report_delivered.TestSaleReportDeliveredBase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.brand = cls.env["product.brand"].create({"name": "Test brand"})

    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_misc(self):
        product = self._create_product("Test product", "consu", stock_qty=1)
        service = self._create_product("Test service", "service")
        product.product_brand_id = self.brand
        service.product_brand_id = self.brand
        order_1 = self._create_order(product, confirm=True)
        order_2 = self._create_order(service, confirm=True)
        orders = order_1 + order_2
        self._validate_pickings(orders.picking_ids, 1.0)
        self.env.invalidate_all()
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", orders.ids)]
        )
        self.assertIn(self.brand, items.mapped("product_brand_id"))
