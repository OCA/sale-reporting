# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    show_details = fields.Boolean(default=True)
    show_section_subtotal = fields.Boolean(
        default=True,
        help="Uncheck this if you want to hide the subtotal on section part",
    )
    show_subtotal = fields.Boolean(default=True)
    show_line_amount = fields.Boolean(default=True)

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update(
            show_details=self.show_details,
            show_subtotal=self.show_subtotal,
            show_line_amount=self.show_line_amount,
            show_section_subtotal=self.show_section_subtotal,
        )
        return res
