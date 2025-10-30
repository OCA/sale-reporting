# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    multicompany_reporting_amount = fields.Selection(
        [
            ("total", "Amount total"),
            ("untaxed", "Untaxed Amount"),
        ],
        default="total",
    )

    @api.model
    def _recompute_multicompany_reporting_currency(self):
        """Recompute the multicompany reporting currency amount for all records

        This method is called when the multicompany reporting parameters are modified,
        to trigger a recomputation of the reporting currency amount for all records
        across all companies.

        Override and implement this method in downstream modules.
        """

    @api.model
    def _get_multicompany_reporting_currency(self):
        """Get the multicompany reporting currency record from the config parameter"""
        return self.env["res.currency"].browse(
            int(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param(
                    "base_multicompany_reporting_currency.multicompany_reporting_currency"
                )
            )
        )
