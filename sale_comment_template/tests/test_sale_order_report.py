# Copyright 2017 Simone Rubino - Agile Business Group
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestAccountInvoiceReport(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.ref("base.main_company")
        self.base_comment_model = self.env["base.comment.template"]
        # Create comment related to sale model
        self.sale_obj = self.env.ref("sale.model_sale_order")
        self.sale_before_comment = self._create_comment(self.sale_obj, "before_lines")
        self.sale_after_comment = self._create_comment(self.sale_obj, "after_lines")
        # Create comment related to move model
        self.move_obj = self.env.ref("account.model_account_move")
        self.move_before_comment = self._create_comment(self.move_obj, "before_lines")
        self.move_after_comment = self._create_comment(self.move_obj, "after_lines")
        # Create partner
        self.partner = self.env["res.partner"].create({"name": "Partner Test"})
        self.partner.base_comment_template_ids = [
            (4, self.sale_before_comment.id),
            (4, self.sale_after_comment.id),
            (4, self.move_before_comment.id),
            (4, self.move_after_comment.id),
        ]
        self.product = self.env["product.product"].create(
            {
                "name": "Test product",
                "sale_ok": True,
                "type": "service",
                "list_price": 10,
                "invoice_policy": "order",
            }
        )
        self.sale_order = self._create_sale_order()
        self.sale_order.action_confirm()

    def _create_sale_order(self):
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = self.partner
        with sale_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return sale_form.save()

    def _create_comment(self, model, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company.id,
                "position": position,
                "text": "Text " + position,
                "model_ids": [(6, 0, model.ids)],
            }
        )

    def test_comments_in_sale_order_report(self):
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("sale.report_saleorder")
            ._render_qweb_html(self.sale_order.ids)
        )
        self.assertRegexpMatches(str(res[0]), self.sale_before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.sale_after_comment.text)

    def test_comments_in_generated_invoice(self):
        invoice = self.sale_order._create_invoices()[0]
        self.assertTrue(self.move_before_comment in invoice.comment_template_ids)
        self.assertTrue(self.move_after_comment in invoice.comment_template_ids)
        self.assertFalse(self.sale_before_comment in invoice.comment_template_ids)
        self.assertFalse(self.sale_after_comment in invoice.comment_template_ids)
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("account.report_invoice")
            ._render_qweb_html(invoice.ids)
        )
        self.assertRegexpMatches(str(res[0]), self.move_before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.move_after_comment.text)

    def test_comments_in_sale_order(self):
        self.assertTrue(self.sale_after_comment in self.sale_order.comment_template_ids)
        self.assertTrue(
            self.sale_before_comment in self.sale_order.comment_template_ids
        )
