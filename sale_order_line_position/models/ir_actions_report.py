# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def render_qweb_pdf(self, res_ids=None, data=None):
        self.sale_recompute_positions(res_ids)
        return super().render_qweb_pdf(res_ids, data)

    def sale_recompute_positions(self, res_ids):
        if self.model == "sale.order":
            sales = self.env["sale.order"].browse(res_ids)
            sales.recompute_positions()
