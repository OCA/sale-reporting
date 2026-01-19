# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    display_base_price_discount_report = fields.Boolean(
        related="company_id.display_base_price_discount_report",
        readonly=False,
    )
    display_crossed_base_price_report = fields.Boolean(
        related="company_id.display_crossed_base_price_report",
        readonly=False,
    )
