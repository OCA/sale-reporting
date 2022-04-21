# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multicompany_reporting_currency = fields.Many2one(
        "res.currency",
        config_parameter="base_multicompany_reporting_currency.multicompany_reporting_currency",
    )
