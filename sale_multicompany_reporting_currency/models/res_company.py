# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    amount_option = fields.Selection(
        [
            ("total", "Amount total"),
            ("untaxed", "Untaxed Amount"),
        ],
        default="total",
    )
