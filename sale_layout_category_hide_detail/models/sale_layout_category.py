# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    hide_details = fields.Boolean(
        string="Hide details",
    )
