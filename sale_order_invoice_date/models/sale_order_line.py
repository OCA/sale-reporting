# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    invoice_date = fields.Date(compute="_compute_invoice_date", store=True)

    @api.depends("invoice_status", "invoice_lines.move_id.invoice_date")
    def _compute_invoice_date(self):
        invoiced = self.filtered(lambda rec: rec.invoice_status == "invoiced")
        not_invoiced = self - invoiced
        not_invoiced.invoice_date = False
        for rec in invoiced:
            rec.invoice_date = max(
                [d for d in rec.invoice_lines.move_id.mapped("invoice_date") if d],
                default=False,
            )
