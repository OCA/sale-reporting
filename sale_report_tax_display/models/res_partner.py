# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    report_show_line_subtotals = fields.Selection(
        string="Show Line Subtotals",
        selection=[
            ("tax_included", "Tax Included"),
            ("tax_excluded", "Tax Excluded"),
        ],
        default="tax_excluded",
        help="""
            Tax Excluded: Hides the tax lines on SO and invoice reports.
            Tax Included: Shows the tax lines on SO and invoice reports.
        """,
    )

    show_tax_calculation = fields.Boolean(
        "Show tax calculation ?",
        default=True,
        help="Hide the tax calculation at the end of the SO and invoice reports.",
    )
