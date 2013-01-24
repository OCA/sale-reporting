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
from openerp.osv import orm, fields


class SaleConditionText(orm.Model):
    """Sale order Textual information"""
    _name = "sale.condition_text"
    _description = "sale conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header', 'Top condition'),
                                  ('footer', 'Bottom condition')],
                                 'type', required=True),
        'text': fields.text('Condition', translate=True, required=True)}


class SaleOrder(orm.Model):
    """Adds condition to SO"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    _columns = {'text_condition1_webkit': fields.many2one('sale.condition_text', 'Header'),
                'text_condition2_webkit': fields.many2one('sale.condition_text', 'Footer'),
                'note1': fields.text('Header'),
                'note2': fields.text('Footer')}

    def _set_condition(self, cursor, uid, inv_id, commentid, key):
        """Set the text of the notes in invoices"""
        if not commentid:
            return {}
        try:
            lang = self.browse(cursor, uid, inv_id)[0].partner_id.lang
        except Exception, exc:
            lang = 'en_US'
        cond = self.pool.get('sale.condition_text').browse(cursor, uid,
                                                           commentid, {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cursor, uid, inv_id, commentid):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note1')

    def set_footer(self, cursor, uid, inv_id, commentid):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note2')
