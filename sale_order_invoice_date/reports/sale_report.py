# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    invoice_date = fields.Date(readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["invoice_date"] = "l.invoice_date"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,
            l.invoice_date"""
        return res
