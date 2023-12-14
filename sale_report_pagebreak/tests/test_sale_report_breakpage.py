from lxml import html

from odoo.tests.common import TransactionCase
from odoo.tools.image import image_data_uri


class TestSaleReportAvoidPageBreakInSection(TransactionCase):
    def test_sale_report_with_section(self):

        sale_order = self.env.ref("sale.sale_order_7")
        for i, line in enumerate(sale_order.order_line):
            line.sequence = i * 10
        sale_order.order_line.create(
            {
                "name": "Section name",
                "order_id": sale_order.id,
                "display_type": "line_section",
                "sequence": 15,
            }
        )
        doc = html.document_fromstring(
            self.env["ir.qweb"]
            ._render(
                "sale.report_saleorder_document",
                values={
                    "doc": sale_order,
                    "env": self.env,
                    "company": self.env.company,
                    "image_data_uri": image_data_uri,
                },
            )
            .decode("utf-8")
        )
        self.assertEqual(
            len(doc.find('.//table[@style="page-break-inside: avoid"]')), 2
        )

    def test_sale_report_without_section(self):
        sale_order = self.env.ref("sale.sale_order_7")
        doc = html.document_fromstring(
            self.env["ir.qweb"]
            ._render(
                "sale.report_saleorder_document",
                values={
                    "doc": sale_order,
                    "env": self.env,
                    "company": self.env.company,
                    "image_data_uri": image_data_uri,
                },
            )
            .decode("utf-8")
        )
        self.assertFalse(doc.find('.//table[@style="page-break-inside: avoid"]'))
