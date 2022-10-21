# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class SaleReportsConfig(models.Model):
    _name = "sale.reports.config"
    _description = "Sale Reports Configuration"

    name = fields.Char("Name")
    view = fields.Char("XML ID of the View")
    view_mode = fields.Char("View Mode")
    domain = fields.Char("Domain")
    limit = fields.Integer("Limit of Rows (tree only)")
    search_view = fields.Char("XML ID of a Search View")
    model = fields.Char("Model Name")
