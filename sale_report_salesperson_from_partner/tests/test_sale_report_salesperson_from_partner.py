# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, new_test_user

from odoo.addons.base.tests.common import BaseCommon


class SaleReportSalespersonFromPartner(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesperson = new_test_user(
            cls.env,
            login="test_salesperson_from_partner",
            groups="sales_team.group_sale_manager",
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "user_id": cls.salesperson.id,
            }
        )
        cls.product = cls.env["product.product"].create({"name": "Test product"})
        cls.order = cls._create_order(cls, cls.product)
        cls.order.action_confirm()

    def _create_order(self, product):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = product
            line_form.product_uom_qty = 1
        return order_form.save()

    def test_sale_report_user_from_partner_id(self):
        sale_report = self.env["sale.report"].search(
            [("user_from_partner_id", "=", self.salesperson.id)], limit=1
        )
        self.assertTrue(sale_report)
        self.assertEqual(
            sale_report.user_from_partner_id,
            self.salesperson,
        )
        self.assertEqual(
            sale_report.order_reference,
            self.order,
        )
