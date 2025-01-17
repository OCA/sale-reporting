# Copyright 2020 Tecnativa - David Vidal
# Copyright 2024 Tecnativa - Carlos López
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleReportCountryState(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.country = cls.env["res.country"].create({"name": "Country1", "code": "C1"})
        cls.state = cls.env["res.country.state"].create(
            {"name": "State1", "code": "S1", "country_id": cls.country.id}
        )
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.partner.write({"state_id": cls.state.id})
        cls.product = cls.env.ref("product.product_product_9")

        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 3.0,
                        },
                    ),
                    Command.create({"display_type": "line_section", "name": "Section"}),
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "product_uom": cls.product.uom_id.id,
                            "product_uom_qty": 5.0,
                        },
                    ),
                ],
            }
        )

    def test_sale_report_state_field(self):
        self.order.action_confirm()

        sale_report = self.env["sale.report"].search(
            [("order_reference", "=", f"sale.order,{self.order.id}")]
        )

        self.assertTrue(
            sale_report,
            f"No sale report entries found for "
            f"order_reference 'sale.order,{self.order.id}'",
        )

        for report_line in sale_report:
            self.assertEqual(
                report_line.state_id.id,
                self.partner.state_id.id,
                f"Sale Report ID {report_line.id} has incorrect state_id. "
                f"Expected {self.partner.state_id.id}, "
                f"found {report_line.state_id.id}.",
            )

    def test_group_by_sale_report(self):
        self.order.action_confirm()

        select_fields = self.env["sale.report"]._select_additional_fields()
        group_by_fields = self.env["sale.report"]._group_by_sale()

        self.assertIn(
            "partner.state_id",
            select_fields.values(),
            "'partner.state_id' is not in the select fields of sale.report.",
        )

        self.assertIn(
            "partner.state_id",
            group_by_fields,
            "'partner.state_id' is not in the GROUP BY clause of sale.report.",
        )
