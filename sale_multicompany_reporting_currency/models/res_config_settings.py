# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    amount_option = fields.Selection(related="company_id.amount_option", readonly=False)

    def set_values(self):
        sale_order = self.env["sale.order"]
        applied_currency = sale_order._get_multicompany_reporting_currency_id()
        super().set_values()
        to_apply_currency = self.multicompany_reporting_currency
        if applied_currency.id != to_apply_currency.id:
            sale_order.search([]).write(
                {"multicompany_reporting_currency_id": to_apply_currency.id}
            )
        return True
