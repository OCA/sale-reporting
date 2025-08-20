# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_tax_column_in_report = fields.Boolean(
        compute="_compute_show_tax_column_in_report"
    )

    def _compute_show_tax_column_in_report(self):
        self.show_tax_column_in_report = True
        for order in self.filtered("order_line"):
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            # Can be a recordset if several taxes apply
            first_line_tax_group = fields.first(order_lines).tax_id.tax_group_id
            # Mixed group taxes, let's show them for clarity
            order.show_tax_column_in_report = (
                first_line_tax_group != order_lines.tax_id.tax_group_id
            )
