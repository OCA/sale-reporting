# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ReportAllChannelsSales(models.Model):
    _inherit = "report.all.channels.sales"

    seller_id = fields.Many2one(
        related='product_id.seller_ids.name',
        domain=[('supplier', '=', True)],
    )
