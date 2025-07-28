# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_taxes_on_report_saleorder_document = fields.Boolean(
        string="Taxes",
        implied_group="sale_order_report_without_tax_col.group_taxes_on_report_saleorder_document",
    )
