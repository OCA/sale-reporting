# Copyright 2021-2022 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tc_id = fields.Many2one("document.tc", string="Terms And Conditions (PDF)")
