# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleReportDeliveredVolume(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "test",
                "type": "consu",
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
                            "product_uom_qty": 3.0,
                            "qty_delivered": 2.0,
                        },
                    ),
                    Command.create({"display_type": "line_section", "name": "Section"}),
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 5.0,
                            "qty_delivered": 4.0,
                        },
                    ),
                ],
            }
        )

    def test_volume_delivered_computation(self):
        self.order.action_confirm()
        reference_value = f"sale.order,{self.order.id}"

        sale_report = self.env["sale.report"].search(
            [("order_reference", "=", reference_value)]
        )
        self.assertTrue(
            sale_report,
            f"No sale report entries found for order_reference {reference_value}",
        )

        expected_volume = sum(
            [
                line.product_id.volume
                * line.qty_delivered
                / line.product_uom.factor
                * line.product_id.uom_id.factor
                for line in self.order.order_line
                if line.product_id
            ]
        )

        for report_line in sale_report:
            self.assertAlmostEqual(
                report_line.volume_delivered,
                expected_volume,
                places=2,
                msg=f"Volume delivered mismatch for report line {report_line.id}",
            )
