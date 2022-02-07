# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    show_details = fields.Boolean(default=True)
    show_subtotal = fields.Boolean(default=True)
    show_line_amount = fields.Boolean(default=True)
