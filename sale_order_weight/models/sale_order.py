# Copyright 2016 Andrea Cometa - Apulia Software
# License AGPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def total_weight(self):
        """
        Returns total weight from a specified sale order
        """
        return self.mapped("order_line").total_weight()
