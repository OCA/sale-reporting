# -*- coding: utf-8 -*-
#
#
#    Author: Nicolas Bessi
#    Copyright 2013-2014 Camptocamp SA
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
#
from openerp.osv import orm, fields


class SaleOrder(orm.Model):
    """Add text comment"""

    _inherit = "sale.order"
    _columns = {
        'comment_template1_id': fields.many2one(
            'base.comment.template',
            'Top Comment Template'),
        'comment_template2_id': fields.many2one(
            'base.comment.template',
            'Bottom Comment Template'),
        'note1': fields.html('Top Comment'),
        'note2': fields.html('Bottom Comment'),
    }

    def set_comment(self, cr, uid, cond_id, field_name, partner_id):
        if not cond_id:
            return {'value': {field_name: ''}}
        cond_obj = self.pool['base.comment.template']
        text = cond_obj.get_value(cr, uid, cond_id, partner_id)
        return {'value': {field_name: text}}

    def set_note1(self, cr, uid, so_id, cond_id, partner_id):
        return self.set_comment(cr, uid, cond_id, 'note1', partner_id)

    def set_note2(self, cr, uid, so_id, cond_id, partner_id):
        return self.set_comment(cr, uid, cond_id, 'note2', partner_id)

    def action_invoice_create(self, cr, uid, ids,
                              grouped=False,
                              states=None,
                              date_invoice=False, context=None):
        # function is design to return only one id
        invoice_obj = self.pool['account.invoice']
        _super = super(SaleOrder, self)
        _super_kwargs = {'grouped': grouped,
                         'date_invoice': date_invoice,
                         'context': context,
                         }
        if states is not None:
            # do not pass the 'states' when None so
            # _super.action_invoice_create will use its default value,
            # which is ['confirmed', 'done', 'exception']
            _super_kwargs['states'] = states
        inv_id = _super.action_invoice_create(cr, uid, ids, **_super_kwargs)

        invoice = invoice_obj.browse(cr, uid, inv_id, context=context)
        if isinstance(ids, (tuple, list)):
            assert len(ids) == 1, "1 ID expected, got: %s" % (ids, )
            ids = ids[0]

        order = self.browse(cr, uid, ids, context=context)
        inv_data = {'comment_template1_id': order.comment_template1_id.id,
                    'comment_template2_id': order.comment_template2_id.id,
                    'note1': order.note1,
                    'note2': order.note2}
        invoice.write(inv_data)
        return inv_id
