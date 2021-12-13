# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleLayoutCategoryHideDetail(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleLayoutCategoryHideDetail, cls).setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Producto test", "type": "consu", "invoice_policy": "order"}
        )
        cls.partner = cls.env["res.partner"].create({"name": "partner_test"})
        cls.sale_order = cls.env["sale.order"].create({"partner_id": cls.partner.id})
        cls.so_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 10,
            }
        )
        cls.so_line.product_id_change()
        cls.sale_order.action_confirm()

    def test_prepare_invoice_line(self):
        res = self.so_line._prepare_invoice_line()
        self.assertEqual(res["quantity"], 10)
        self.assertEqual(res["product_id"], self.product.id)
        self.assertEqual(res["show_details"], True)
        self.assertEqual(res["show_subtotal"], True)
        self.so_line.write({"show_details": False, "show_subtotal": False})
        res = self.so_line._prepare_invoice_line()
        self.assertEqual(res["quantity"], 10)
        self.assertEqual(res["product_id"], self.product.id)
        self.assertEqual(res["show_details"], False)
        self.assertEqual(res["show_subtotal"], False)

    def test_create_invoices(self):
        self.so_line.write({"show_details": False, "show_subtotal": False})
        invoice = self.sale_order._create_invoices()
        self.assertEqual(invoice.invoice_line_ids.show_details, False)
        self.assertEqual(invoice.invoice_line_ids.show_subtotal, False)
