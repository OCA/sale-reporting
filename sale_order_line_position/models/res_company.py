# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    disable_sale_position_recompute = fields.Boolean(
        string="Do not recompute positions on sale orders"
    )
