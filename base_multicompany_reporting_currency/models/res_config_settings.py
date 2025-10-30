# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multicompany_reporting_currency = fields.Many2one(
        "res.currency",
        config_parameter="base_multicompany_reporting_currency.multicompany_reporting_currency",
    )
    multicompany_reporting_amount = fields.Selection(
        related="company_id.multicompany_reporting_amount",
        readonly=False,
    )

    def set_values(self):
        applied_currency = self.env[
            "res.company"
        ]._get_multicompany_reporting_currency()
        super().set_values()
        to_apply_currency = self.multicompany_reporting_currency
        if applied_currency != to_apply_currency:
            self.env["res.company"]._recompute_multicompany_reporting_currency()
        return True
