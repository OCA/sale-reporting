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

    def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
        if fields is None:
            fields = {}
        select_str = """ ,
            partner.state_id as state_id
        """
        fields.update({
            'state_id': select_str,
        })
        groupby += """,
            partner.state_id
        """
        return super()._query(with_clause=with_clause, fields=fields,
                              groupby=groupby, from_clause=from_clause)
