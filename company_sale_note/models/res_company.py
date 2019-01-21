# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_note_place = fields.Selection(
        selection=[
            ('no', 'Disable'),
            ('before', 'Before sale note'),
            ('after', 'At the end of document (after fiscal position note)'),
        ],
        default="no",
        required=True,
        help="Define on where to place the additional sale note on the "
             "sale report",
    )
    sale_note = fields.Html(
        help="Note who'll be printed on every sale related to this company",
    )
