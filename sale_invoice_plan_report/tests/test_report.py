# Copyright 2026 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.sale.tests import common


@tagged("post_install", "-at_install")
class TestSaleInvoicePlanReport(common.TestSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_a.id,
                "pricelist_id": cls.env.ref("product.list0").id,
                "use_invoice_plan": True,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_a.id,
                            "name": cls.product_a.name,
                            "product_uom_qty": 2.0,
                            "price_unit": 100.0,
                        },
                    ),
                ],
                "invoice_plan_ids": [
                    (
                        0,
                        0,
                        {
                            "installment": 1,
                            "plan_date": "2026-02-23",
                            "invoice_type": "installment",
                            "percent": 50.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "installment": 2,
                            "plan_date": "2026-03-23",
                            "invoice_type": "installment",
                            "percent": 50.0,
                        },
                    ),
                ],
            }
        )

    def _render_report(self, order):
        """Helper to render the sale order report as HTML."""
        report_model = self.env["ir.actions.report"].with_context(
            discard_logo_check=True
        )
        html, _ = report_model._render_qweb_html(
            "sale.action_report_saleorder", order.ids
        )
        if isinstance(html, list):
            html = b"".join(html)
        return html.decode("utf-8")

    def test_sale_order_report_render_smoke(self):
        """Test that the report renders without errors."""
        html = self._render_report(self.sale_order)
        self.assertTrue(html)

    def test_report_contains_invoice_plan_section(self):
        """Test that the invoice plan section appears in the report."""
        html = self._render_report(self.sale_order)
        self.assertIn("Invoice Plan", html)
        self.assertIn("invoice_plan_section", html)

    def test_report_contains_installment_details(self):
        """Test that installment details are displayed correctly."""
        html = self._render_report(self.sale_order)
        self.assertIn("2026", html)
        self.assertIn("50", html)
        self.assertIn("Installment", html)

    def test_report_contains_type_badge(self):
        """Test that installment type badges are rendered."""
        html = self._render_report(self.sale_order)
        self.assertIn("Installment", html)

    def test_report_no_invoice_plan_when_disabled(self):
        """Test that invoice plan section is hidden when not configured."""
        order_no_plan = self.env["sale.order"].create(
            {
                "partner_id": self.partner_a.id,
                "pricelist_id": self.env.ref("product.list0").id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "name": "Test Product",
                            "product_uom_qty": 1.0,
                            "price_unit": 50.0,
                        },
                    ),
                ],
            }
        )
        html = self._render_report(order_no_plan)
        self.assertNotIn("invoice_plan_section", html)
        self.assertNotIn("Invoice Plan", html)

    def test_report_with_advance_and_installments(self):
        """Test report with advance payment and installments."""
        order_with_advance = self.env["sale.order"].create(
            {
                "partner_id": self.partner_a.id,
                "pricelist_id": self.env.ref("product.list0").id,
                "use_invoice_plan": True,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_a.id,
                            "name": "Test Product",
                            "product_uom_qty": 1.0,
                            "price_unit": 1000.0,
                        },
                    ),
                ],
                "invoice_plan_ids": [
                    (
                        0,
                        0,
                        {
                            "installment": 0,
                            "plan_date": "2026-01-15",
                            "invoice_type": "advance",
                            "percent": 50.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "installment": 1,
                            "plan_date": "2026-06-03",
                            "invoice_type": "installment",
                            "percent": 41.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "installment": 2,
                            "plan_date": "2026-07-24",
                            "invoice_type": "installment",
                        },
                    ),
                ],
            }
        )
        html = self._render_report(order_with_advance)
        self.assertIn("Invoice Plan", html)
        self.assertIn("Total", html)

    def test_report_currency_display(self):
        """Test that currency values are displayed in the report."""
        html = self._render_report(self.sale_order)
        self.assertIn("oe_currency_value", html.lower())
