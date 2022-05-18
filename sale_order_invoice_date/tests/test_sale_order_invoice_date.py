# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import SavepointCase


class TestSaleInvoiceDate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "invoice_policy": "order",
                "list_price": 10.0,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_uom_qty": 5.0,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": cls.product.list_price,
                        },
                    )
                ],
            }
        )
        cls.order.action_confirm()

    def _create_invoice(self, order, quantity=None, invoice_date=None, post=True):
        invoice_vals = order._prepare_invoice()
        invoice_line_vals = order.order_line._prepare_invoice_line()
        if quantity is not None:
            invoice_line_vals["quantity"] = quantity
        invoice_vals["invoice_line_ids"].append((0, 0, invoice_line_vals))
        if invoice_date is not None:
            invoice_vals["invoice_date"] = invoice_date
        invoice = self.env["account.move"].create(invoice_vals)
        if post:
            invoice.action_post()
        return invoice

    def test_sale_invoice_date(self):
        self.assertFalse(self.order.invoice_date)
        self.assertFalse(self.order.order_line.invoice_date)
        self._create_invoice(self.order, quantity=1.0, invoice_date="2022-01-01")
        self.assertFalse(self.order.invoice_date)
        self.assertFalse(self.order.order_line.invoice_date)
        self._create_invoice(self.order, quantity=2.0, invoice_date="2022-01-02")
        self.assertFalse(self.order.invoice_date)
        self.assertFalse(self.order.order_line.invoice_date)
        self._create_invoice(self.order, quantity=2.0, invoice_date="2022-01-03")
        self.assertEqual(
            self.order.order_line.invoice_date,
            fields.Date.to_date("2022-01-03"),
        )
        self.assertEqual(
            self.order.invoice_date,
            fields.Date.to_date("2022-01-03"),
        )

    def test_sale_report(self):
        self._create_invoice(self.order, quantity=5.0, invoice_date="2022-01-03")
        self.env["base"].flush()
        res = self.env["sale.report"].read_group(
            [("order_id", "in", self.order.ids)],
            fields=["invoice_date"],
            groupby=["invoice_date"],
            lazy=False,
        )
        self.assertEqual(res[0]["invoice_date"], "January 2022")
