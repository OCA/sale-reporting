# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    disable_sale_position_recompute = fields.Boolean(
        related="company_id.disable_sale_position_recompute",
        readonly=False,
    )
