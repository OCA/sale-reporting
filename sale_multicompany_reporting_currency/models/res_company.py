# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _recompute_multicompany_reporting_currency(self):
        # OVERRIDE to apply the change to sale.order(s)
        res = super()._recompute_multicompany_reporting_currency()
        reporting_currency = self._get_multicompany_reporting_currency()
        domain = [("multicompany_reporting_currency_id", "!=", reporting_currency.id)]
        records = self.env["sale.order"].sudo().search(domain)  # sudo for multi-company
        records.multicompany_reporting_currency_id = reporting_currency
        return res
