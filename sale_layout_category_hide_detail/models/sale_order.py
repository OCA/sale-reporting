# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_details = fields.Boolean(default=True)
    show_subtotal = fields.Boolean(default=True)
    show_price = fields.Boolean(default=True)

    def _prepare_invoice_line(self):
        res = super()._prepare_invoice_line()
        res.update(show_details=self.show_details,
                   show_subtotal=self.show_subtotal,
                   show_price=self.show_price)
        return res
