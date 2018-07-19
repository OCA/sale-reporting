# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA (http://www.camptocamp.com)
# @author Vincent Renaville
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleConditionText(models.Model):
    """Sale order Textual information"""

    _name = "sale.condition_text"
    _description = "sale conditions"

    name = fields.Char(
        'Condition summary',
        required=True,
    )
    condition_type = fields.Selection(
        [('header', 'Top condition'),
         ('footer', 'Bottom condition')],
        'Type',
        required=True,
    )
    text = fields.Html(
        'Condition',
        translate=True,
        required=True,
    )
    lang = fields.Char(
        'Language',
        default=lambda self: self.env.lang or 'en_US',
    )


class SaleOrder(models.Model):
    """Adds condition to SO"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    text_condition1 = fields.Many2one(
        'sale.condition_text',
        'Header condition',
        domain=[('condition_type', '=', 'header')]
    )
    text_condition2 = fields.Many2one(
        'sale.condition_text',
        'Footer condition',
        domain=[('condition_type', '=', 'footer')]
    )
    note1 = fields.Html('Header')
    note2 = fields.Html('Footer')

    @api.onchange('text_condition1', 'partner_id')
    def set_header(self):
        if self.text_condition1 and not self.partner_id:
            raise UserError(_("No Customer Defined Before choosing condition"
                              " text select a customer."))
        ctx = dict(self._context)
        lang = self.partner_id.lang or 'en_US'
        self.text_condition1.with_context(ctx).write({'lang': lang})
        if self.text_condition1:
            self.note1 = self.text_condition1.text

    @api.onchange('text_condition2', 'partner_id')
    def set_footer(self):
        if self.text_condition2 and not self.partner_id:
            raise UserError(_("No Customer Defined Before choosing condition"
                              " text select a customer."))
        ctx = dict(self._context)
        lang = self.partner_id.lang or 'en_US'
        self.text_condition2.with_context(ctx).write({'lang': lang})
        if self.text_condition2:
            self.note2 = self.text_condition2.text

    @api.onchange('note1')
    def set_condition_header(self):
        if self.text_condition1 and self.note1 != self.text_condition1.text:
            self.text_condition1.text = self.note1

    @api.onchange('note2')
    def set_condition_header(self):
        if self.text_condition2 and self.note2 != self.text_condition2.text:
            self.text_condition2.text = self.note2

    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        xml = 'sale.report_saleorder'
        return self.env['report'].get_action(self, xml)


class SaleOrderLine(models.Model):
    """Add HTML note to sale order lines"""

    _inherit = "sale.order.line"

    formatted_note = fields.Html('Formatted Note')
