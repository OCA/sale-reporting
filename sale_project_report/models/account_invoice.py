# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    project_ids = fields.Many2many(
        comodel_name="project.project",
        compute="_compute_project_ids",
    )

    @api.depends("line_ids.sale_line_ids.order_id.project_id")
    def _compute_project_ids(self):
        for move in self:
            move.project_ids = move.line_ids.sale_line_ids.order_id.project_id
