# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleReportPackaging(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.uom_unit = cls.env["uom.uom"].create(
            {
                "name": "Test Unit",
                "relative_factor": 1.0,
                "relative_uom_id": False,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "uom_id": cls.uom_unit.id,
            }
        )
        cls.uom_dozen = cls.env["uom.uom"].create(
            {
                "name": "Dozen",
                "relative_factor": 12.0,
                "relative_uom_id": cls.uom_unit.id,
            }
        )
        cls.product.write(
            {
                "uom_ids": [Command.link(cls.uom_dozen.id)],
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom_id": cls.uom_dozen.id,
                            "product_uom_qty": 2.0,
                        },
                    )
                ],
            }
        )

    def test_product_packaging_report_values(self):
        self.order.action_confirm()

        self.env.invalidate_all()
        sale_report = self.env["sale.report"]._read_group(
            domain=[("order_reference", "=", f"sale.order,{self.order.id}")],
            groupby=["product_packaging_id"],
            aggregates=[
                "product_packaging_qty:sum",
                "product_packaging_qty_delivered:sum",
            ],
        )

        self.assertTrue(sale_report, "No sale report entries found for the sale order.")

        report_entry = sale_report[0]
        self.assertEqual(
            report_entry[0].id,
            self.uom_dozen.id,
            "Incorrect product packaging in the report.",
        )
        self.assertEqual(
            report_entry[1],
            2,
            "Incorrect product packaging quantity in the report.",
        )
        self.assertEqual(
            report_entry[2],
            0,
            "Incorrect product packaging delivered quantity in the report.",
        )
