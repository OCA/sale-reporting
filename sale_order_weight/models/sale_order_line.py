#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def total_weight(self):
        """Returns total weight for sale order lines in self."""
        lines_weight = 0.0
        for line in self:
            if line.product_id:
                lines_weight += line.product_id.weight * line.product_uom_qty
        return lines_weight
