# Copyright 2021-2022 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class DocumentTc(models.Model):
    _name = "document.tc"
    _description = "Terms and Conditions Documents"

    document = fields.Binary("Attached Document")
    name = fields.Char("Document Name")
    active = fields.Boolean(default=True)
