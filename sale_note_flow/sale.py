# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi
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
from openerp.osv import orm


class SaleOrder(orm.Model):

    _inherit = "sale.order"

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(SaleOrder, self)._prepare_invoice(cr, uid, order,
                                                      lines, context=context)
        res.update({'note1': order.note1, 'note2': order.note2})
        return res


class SaleOrderline(orm.Model):

    _inherit = "sale.order.line"

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        res = super(SaleOrderline, self)._prepare_order_line_invoice_line(cr, uid, line,
                                                                          account_id=False,
                                                                          context=context)
        res.update({'formatted_note': line.formatted_note})
        return res
