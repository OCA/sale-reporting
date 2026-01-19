# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    display_base_price_discount_report = fields.Boolean(
        string="Display base price discount on reports",
        help="Check this if you want to display this on reports",
    )
    display_crossed_base_price_report = fields.Boolean(
        string="Display crossed base price on reports",
        help="Check this if you want to display this on reports",
    )
