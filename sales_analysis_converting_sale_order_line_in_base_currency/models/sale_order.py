# -*- encoding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - present Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
###############################################################################
from openerp.osv import fields, orm
from openerp.addons.decimal_precision import get_precision


class SaleOrder(orm.Model):

    """Override the sale.order model."""

    _inherit = 'sale.order'

    _columns = {
        'converted_amount_total': fields.function(
            lambda self, *a, **b: self._compute_converted_total(*a, **b),
            method=True,
            type='float',
            digits_compute=get_precision("Product Price"),
            string='Converted Amount',
        ),
        'converted_amount_total_untaxed': fields.function(
            lambda self, *a, **b: self._compute_converted_total(*a, **b),
            method=True,
            type='float',
            digits_compute=get_precision("Product Price"),
            string='Converted Amount',
        ),
        'company_currency_id': fields.related(
            'company_id',
            'currency_id',
            type="many2one",
            relation="res.currency",
            string="Company Currency",
            readonly=True,
            store=True
        ),
    }

    def _compute_converted_total(self, cr, uid, ids, field_name, arg, context):
        res = {}

        for obj in self.browse(cr, uid, ids, context=context):
            total = 0
            for line in obj.order_line:
                total += line.converted_amount_subtotal
            res[obj.id] = total

        return res

    def action_button_confirm(self, cr, uid, ids, context=None):
        """
        Convert unit_price using the line and company currencies.

        Convert price using the currency if necessary or set the
        lst_price if no conversion is necessary. The reason to skip
        the conversion is to reduce the amount of error with roundings.
        """
        base_func = super(SaleOrder, self).action_button_confirm
        base_func(cr, uid, ids, context=context)

        for o in self.browse(cr, uid, ids, context=context):
            base_currency = o.company_id.currency_id.rate

            for line in o.order_line:
                new_price = line.compute_amount_currency(base_currency)
                line.write({
                    "amount_currency_calculated": new_price
                })
