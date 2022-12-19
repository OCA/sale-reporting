# © 2021-2022 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import io

from odoo import http
from odoo.http import request
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/my/orders/tcs/<int:tc_id>"], type="http", auth="public", website=True
    )
    def download_tc(self, tc_id):
        document_tc = request.env["document.tc"].sudo().browse(tc_id)
        if document_tc:
            file_base64 = base64.b64decode(document_tc.document)
            file_data = io.BytesIO(file_base64)
            mimetype = guess_mimetype(file_base64, default="application/pdf")
            return http.send_file(
                file_data, filename=document_tc.name, mimetype=mimetype
            )
        else:
            return request.not_found()
