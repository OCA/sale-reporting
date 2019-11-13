# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    add_page_break = fields.Boolean(
        string="Insert page break after",
        default=False)
    show_details = fields.Boolean(
        string="Show details",
        default=True)
    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)


