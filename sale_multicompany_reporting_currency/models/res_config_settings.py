# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def set_values(self):
        super().set_values()
        self.env["sale.order"].search([]).write(
            {
                "multicompany_reporting_currency_id": self.multicompany_reporting_currency.id
            }
        )
        return True
