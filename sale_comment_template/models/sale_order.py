# -*- coding: utf-8 -*-
# © 2013-2014  Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class SaleOrder(models.Model):
    """Add text comment"""
    _inherit = "sale.order"

    comment_template1_id = fields.Many2one('base.comment.template',
                                           string='Top Comment Template')
    comment_template2_id = fields.Many2one('base.comment.template',
                                           string='Bottom Comment Template')
    note1 = fields.Html('Top Comment')
    note2 = fields.Html('Bottom Comment')

    @api.onchange('comment_template1_id')
    def onchange_set_note1(self):
        comment = self.comment_template1_id
        if comment:
            self.note1 = comment.get_value(self, self.partner_id.id)

    @api.onchange('comment_template2_id')
    def onchange_set_note2(self):
        comment = self.comment_template2_id
        if comment:
            self.note2 = comment.get_value(self, self.partner_id.id)

    @api.multi
    def _prepare_invoice(self):
        """
        Add in the dict of values to create the new invoice for a sales order.
        """
        self.ensure_one()
        invoice_values = super(SaleOrder, self)._prepare_invoice()
        invoice_values.update({
            'comment_template1_id': self.comment_template1_id.id,
            'comment_template2_id': self.comment_template2_id.id,
            'note1': self.note1,
            'note2': self.note2,
        })
        return invoice_values
