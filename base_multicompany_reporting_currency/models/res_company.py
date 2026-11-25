# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    multicompany_reporting_amount = fields.Selection(
        [
            ("total", "Amount total"),
            ("untaxed", "Untaxed Amount"),
        ],
        default="total",
    )
