# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleReportPackaging(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_9")
        cls.product_packaging = cls.env["product.packaging"].create(
            {
                "name": "Box of 12",
                "qty": 12,
                "product_id": cls.product.id,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 24.0,
                            "product_packaging_id": cls.product_packaging.id,
                            "product_packaging_qty": 2,
                        },
                    )
                ],
            }
        )

    def test_product_packaging_fields_in_report(self):
        self.order.action_confirm()

        select_fields = self.env["sale.report"]._select_additional_fields()
        group_by_fields = self.env["sale.report"]._group_by_sale()
        from_clause = self.env["sale.report"]._from_sale()

        self.assertIn(
            "product_packaging_id",
            select_fields,
            "'product_packaging_id' is not in the select fields.",
        )
        self.assertIn(
            "product_packaging_qty",
            select_fields,
            "'product_packaging_qty' is not in the select fields.",
        )
        self.assertIn(
            "product_packaging_qty_delivered",
            select_fields,
            "'product_packaging_qty_delivered' is not in the select fields.",
        )

        self.assertIn(
            "l.product_packaging_id",
            group_by_fields,
            "'product_packaging_id' is not in the GROUP BY clause.",
        )

        self.assertIn(
            "LEFT JOIN product_packaging",
            from_clause,
            "LEFT JOIN with 'product_packaging' is missing in the FROM clause.",
        )

    def test_product_packaging_report_values(self):
        self.order.action_confirm()
        self.env.invalidate_all()
        sale_report = self.env["sale.report"].read_group(
            domain=[("order_reference", "=", f"sale.order,{self.order.id}")],
            fields=[
                "product_packaging_id",
                "product_packaging_qty",
                "product_packaging_qty_delivered",
            ],
            groupby=["product_packaging_id"],
        )
        self.assertTrue(sale_report, "No sale report entries found for the sale order.")
        report_entry = sale_report[0]
        self.assertEqual(
            report_entry["product_packaging_id"][0],
            self.product_packaging.id,
            "Incorrect product packaging in the report.",
        )
        self.assertEqual(
            report_entry["product_packaging_qty"],
            2,
            "Incorrect product packaging quantity in the report.",
        )
        self.assertEqual(
            report_entry["product_packaging_qty_delivered"],
            0,
            "Incorrect product packaging delivered quantity in the report.",
        )
