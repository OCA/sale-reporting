# Copyright 2026 ACSONE SA/NV (<https://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleReport(BaseCommon):
    def test_report(self):
        # Check the report is still well printed
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [Command.create({"name": "Test"})],
            }
        )
        report = self.env.ref("sale.action_report_saleorder")

        report._render_qweb_html("sale.action_report_saleorder", order.ids)
