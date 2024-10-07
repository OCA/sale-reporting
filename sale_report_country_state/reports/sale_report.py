# Copyright 2020 Tecnativa - David Vidal
# Copyright 2024 Tecnativa - Carlos López
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Customer State",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["state_id"] = "partner.state_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ", partner.state_id"
        return res
