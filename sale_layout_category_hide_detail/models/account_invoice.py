# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def order_lines_layouted(self):
        report_pages = super(AccountInvoice, self).order_lines_layouted()
        return self.env['sale.order'].lines_layouted_hide_details(report_pages)
