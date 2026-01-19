# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    display_base_price_discount_report = fields.Boolean(
        related="company_id.display_base_price_discount_report"
    )
    display_crossed_base_price_report = fields.Boolean(
        related="company_id.display_crossed_base_price_report",
    )
