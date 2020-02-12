# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="Partner's State",
        readonly=True,
    )

    def _select(self):
        select_str = super()._select()
        select_str += """,
            partner.state_id as state_id
        """
        return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += """,
            partner.state_id
        """
        return group_by_str
