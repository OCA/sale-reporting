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
import time

from openerp.report import report_sxw
from openerp import pooler


class SaleOrderReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(SaleOrderReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time,
                                  'company_vat': self._get_company_vat,
                                  'show_discount': self._show_discount,
                                  })

    def _show_discount(self, uid, context=None):
        """ check if the user belongs to group_discount_per_so_line group
        """
        cr = self.cr
        pool = pooler.get_pool(self.cr.dbname)
        res_users_obj = pool.get('res.users')
        model_data_obj = pool.get('ir.model.data')
        try:
            group_id = model_data_obj.get_object_reference(
                cr,
                uid,
                'sale',
                'group_discount_per_so_line')[1]
        except ValueError:
            # group named group_discount_per_so_line doesn't exist
            return False
        groups = res_users_obj.browse(cr, uid, uid, context=context).groups_id
        return any(x for x in groups if x.id == group_id)

    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(
            self.cr, self.uid, self.uid
        ).company_id.partner_id.vat
        return company_vat

report_sxw.report_sxw('report.sale.order.webkit',
                      'sale.order',
                      'addons/sale_report_webkit/report/sale_order.mako',
                      parser=SaleOrderReport)
