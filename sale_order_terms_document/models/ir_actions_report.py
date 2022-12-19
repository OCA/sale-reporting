# Copyright 2021-2022 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import io

from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    # ------------------------------------------------------
    # Actions
    # ------------------------------------------------------
    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        # If model is sale.order, Get the file attached to
        # the sale order and merge file after report
        if pdf_content and self.xml_id == "sale.action_report_saleorder":
            pdf_data = io.BytesIO(pdf_content)
            file1 = PdfFileReader(stream=pdf_data)

            # Get the corresponding Documents choosen
            if len(res_ids) == 1:
                obj = self.env[self.model].browse(res_ids)
                if obj.tc_id:
                    page = obj.tc_id
                    page_data = io.BytesIO(base64.b64decode(page.document))
                    file2 = PdfFileReader(stream=page_data)

                    # Read a template PDF
                    output = PdfFileWriter()

                    # Add all report pages
                    output.appendPagesFromReader(file1)

                    # Add the requested page from template pdf
                    output.appendPagesFromReader(file2)

                    output_stream = io.BytesIO()
                    output.write(output_stream)

                    pdf_content = output_stream.getvalue()
        return super()._post_pdf(save_in_attachment, pdf_content, res_ids)
