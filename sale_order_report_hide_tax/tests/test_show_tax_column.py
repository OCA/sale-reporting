# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestShowTaxColumnInReport(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )
        cls.tax_group_1 = cls.env["account.tax.group"].create(
            {
                "name": "VAT Group 1",
            }
        )
        cls.tax_group_2 = cls.env["account.tax.group"].create(
            {
                "name": "VAT Group 2",
            }
        )
        cls.tax_group_3 = cls.env["account.tax.group"].create(
            {
                "name": "VAT Group 3",
            }
        )
        cls.tax_1 = cls.env["account.tax"].create(
            {
                "name": "Tax 1",
                "amount": 10,
                "amount_type": "percent",
                "tax_group_id": cls.tax_group_1.id,
            }
        )
        cls.tax_2 = cls.env["account.tax"].create(
            {
                "name": "Tax 2",
                "amount": 5,
                "amount_type": "percent",
                "tax_group_id": cls.tax_group_2.id,
            }
        )
        cls.tax_3 = cls.env["account.tax"].create(
            {
                "name": "Tax 3",
                "amount": 5,
                "amount_type": "percent",
                "tax_group_id": cls.tax_group_2.id,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
            }
        )
        cls.report = cls.env["ir.actions.report"]._get_report_from_name(
            "sale.report_saleorder"
        )

    def test_same_tax_group_hides_tax_column(self):
        self.order.order_line = [
            Command.clear(),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 1",
                    "product_uom_qty": 1,
                    "price_unit": 100,
                    "tax_id": [(6, 0, [self.tax_1.id])],
                }
            ),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 2",
                    "product_uom_qty": 1,
                    "price_unit": 50,
                    "tax_id": [(6, 0, [self.tax_1.id])],
                }
            ),
        ]
        result = self.report._render_qweb_html("sale.report_saleorder", [self.order.id])
        html = result[0].decode("utf-8")
        self.assertNotIn(
            "Taxes",
            html,
            """Tax column should be hidden when all taxes
                belong to the same tax group""",
        )

    def test_mixed_tax_groups_show_tax_column(self):
        self.order.order_line = [
            Command.clear(),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 1",
                    "product_uom_qty": 1,
                    "price_unit": 100,
                    "tax_id": [(6, 0, [self.tax_1.id])],
                }
            ),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 2",
                    "product_uom_qty": 1,
                    "price_unit": 50,
                    "tax_id": [(6, 0, [self.tax_2.id])],
                }
            ),
        ]
        result = self.report._render_qweb_html("sale.report_saleorder", [self.order.id])
        html = result[0].decode("utf-8")
        self.assertIn(
            "Taxes",
            html,
            """The tax column should be displayed when taxes
                belong to different tax groups""",
        )

    def test_mixed_tax_groups_single_line_sow_tax_column(self):
        self.order.order_line = [
            Command.clear(),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 1",
                    "product_uom_qty": 1,
                    "price_unit": 100,
                    "tax_id": [(6, 0, [self.tax_1.id, self.tax_2.id])],
                }
            ),
            Command.create(
                {
                    "product_id": self.product.id,
                    "name": "Line 1",
                    "product_uom_qty": 1,
                    "price_unit": 100,
                    "tax_id": [(6, 0, [self.tax_3.id])],
                }
            ),
        ]
        result = self.report._render_qweb_html("sale.report_saleorder", [self.order.id])
        html = result[0].decode("utf-8")
        self.assertIn(
            "Taxes",
            html,
            """The tax column should be displayed when taxes
                belong to different tax groups""",
        )
