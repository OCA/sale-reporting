# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_tax_column_in_report = fields.Boolean(
        compute="_compute_show_tax_column_in_report"
    )

    def _compute_show_tax_column_in_report(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            first_line_tax_group = next(
                iter(order_lines), order_lines
            ).tax_ids.tax_group_id
            # Mixed group taxes, let's show them for clarity
            order.show_tax_column_in_report = any(
                first_line_tax_group != line.tax_ids.tax_group_id
                for line in order_lines
            )
