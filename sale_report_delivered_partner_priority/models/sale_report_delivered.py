# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleReportDelivered(models.Model):
    _inherit = "sale.report.delivered"

    priority_id = fields.Many2one(comodel_name="partner.priority", string="Priority")

    def _select(self):
        select_str = super()._select()
        select_str += ", sub.priority_id"
        return select_str

    def _sub_select(self):
        sub_select_str = super()._sub_select()
        sub_select_str += ", partner.priority_id as priority_id"
        return sub_select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", sub.priority_id"
        return group_by_str
