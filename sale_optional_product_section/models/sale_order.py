# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    sequence = fields.Integer(required=True, default=10)
    display_type = fields.Selection(
        [("line_section", "Section"), ("line_note", "Note")],
        default=False,
        help="Technical field for UX purpose.",
    )
    product_id = fields.Many2one(required=False)
    uom_id = fields.Many2one(required=False)
