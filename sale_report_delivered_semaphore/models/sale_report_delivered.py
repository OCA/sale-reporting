# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleReportDelivered(models.Model):
    _inherit = "sale.report.delivered"

    semaphore = fields.Selection(
        [
            ("success", "🟢"),
            ("warning", "🟡"),
            ("danger", "🔴"),
        ],
    )

    def _select(self):
        select_str = super()._select()
        select_str += ", sub.semaphore"
        return select_str

    def _sub_select(self):
        sub_select_str = super()._sub_select()
        sub_select_str += ", sol.semaphore as semaphore"
        return sub_select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", sub.semaphore"
        return group_by_str
