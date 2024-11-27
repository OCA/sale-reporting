# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common, new_test_user


class SaleReportSalespersonFromPartner(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
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
            sale_report.order_id,
            self.order,
        )
