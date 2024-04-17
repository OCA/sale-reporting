# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        self.sale_recompute_positions(report_ref, res_ids)
        return super()._render_qweb_pdf(report_ref, res_ids, data)

    def sale_recompute_positions(self, report_ref, res_ids):
        report_sudo = self._get_report(report_ref)
        if report_sudo.model == "sale.order":
            sales = self.env["sale.order"].browse(res_ids)
            sales.recompute_positions()
