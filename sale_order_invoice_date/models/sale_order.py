# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_date = fields.Date(compute="_compute_invoice_date", store=True)

    @api.depends("order_line.invoice_date")
    def _compute_invoice_date(self):
        data = {}
        invoiced = self.filtered(lambda rec: rec.invoice_status == "invoiced")
        if invoiced.ids:
            groups = self.env["sale.order.line"].read_group(
                domain=[("order_id", "in", invoiced.ids)],
                fields=["order_id", "invoice_date:max"],
                groupby=["order_id"],
            )
            data = {g["order_id"][0]: g["invoice_date"] for g in groups}
        for rec in self:
            rec.invoice_date = data.get(rec.id, False)
