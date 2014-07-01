# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2011 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi, Vincent Renaville, Guewen Baconnier
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields, osv
from openerp import netsvc
from openerp.tools.translate import _


class SaleConditionText(orm.Model):
    """Sale order Textual information"""
    _name = "sale.condition_text"
    _description = "sale conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header', 'Top condition'),
                                  ('footer', 'Bottom condition')],
                                 'type', required=True),
        'text': fields.html('Condition', translate=True, required=True)}


class SaleOrder(orm.Model):
    """Adds condition to SO"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    _columns = {'text_condition1': fields.many2one('sale.condition_text', 'Header',
                                                   domain=[('type', '=', 'header')]),
                'text_condition2': fields.many2one('sale.condition_text', 'Footer',
                                                   domain=[('type', '=', 'footer')]),
                'note1': fields.html('Header'),
                'note2': fields.html('Footer')}

    def _set_condition(self, cursor, uid, inv_id, commentid, key, partner_id=False):
        """Set the text of the notes in invoices"""
        if not commentid:
            return {}
        if not partner_id:
            raise osv.except_osv(_('No Customer Defined !'), _('Before choosing condition text select a customer.'))
        lang = self.pool.get('res.partner').browse(cursor, uid, partner_id).lang or 'en_US'
        cond = self.pool.get('sale.condition_text').browse(cursor, uid,
                                                           commentid, {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cursor, uid, inv_id, commentid, partner_id=False):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note1', partner_id)

    def set_footer(self, cursor, uid, inv_id, commentid, partner_id=False):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note2', partner_id)

    def print_quotation(self, cursor, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cursor)
        datas = {'model': 'sale.order',
                 'ids': ids,
                 'form': self.read(cursor, uid, ids[0], context=context),
                 }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'sale.order.webkit',
                'datas': datas, 'nodestroy': True}


class SaleOrderLine(orm.Model):
    """ADD HTML note to sale order lines"""

    _inherit = "sale.order.line"

    _columns = {'formatted_note': fields.html('Formatted Note')}
