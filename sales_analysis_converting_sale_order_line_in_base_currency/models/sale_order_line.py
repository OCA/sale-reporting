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


class SaleOrderLine(orm.Model):

    """Override the sale.order.line model."""

    _inherit = 'sale.order.line'

    _columns = {
        "currency_id": fields.many2one(
            'res.currency', 'Currency'
        ),
        "amount_currency_calculated": fields.float(
            'Amount converted',
            readonly=True,
            digits_compute=get_precision("Account"),
        ),
        "converted_amount_subtotal": fields.function(
            lambda self, *a, **b: self._compute_converted_subtotal(*a, **b),
            method=True,
            type='float',
            digits_compute=get_precision("Account"),
            string='Converted Subtotal',
        ),
    }

    def _compute_converted_subtotal(
        self, cr, uid, ids, field_name, arg, context
    ):
        res = {}

        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = obj.amount_currency_calculated * obj.product_uom_qty

        return res

    def _compute_currency(
        self, cr, uid, base_currency, line_currency, lst_price,
        line_price, context=None
    ):
        """Compute the base price of the product."""
        decimal_precision = self.pool['decimal.precision']
        precision = decimal_precision.precision_get(cr, uid, 'Account')

        if line_currency:
            price_unit = None

            if lst_price:
                to_currency = (line_currency / float(base_currency))
                price_unit = lst_price * to_currency
                price_unit = round(price_unit, precision)

            if price_unit != line_price:
                to_base = (base_currency / float(line_currency))
                # If price don't match, it means that the line_price
                # isn't purely dependent on lst_price
                return line_price * to_base

        # Otherwise return the line_price
        return line_price

    def compute_amount_currency(
        self, cr, uid, ids, base_currency, context=None
    ):
        """
        Compute the converted price for line with different currencies.

        Check if the price_unit is simply converted from
        from lst_price without discount or any other changes.
        If it's simply a currency conversion then don't convert
        it back to the base_currency (prevent errors)
        If the price isn't only dependent on lst_price, then
        convert it back to base_currency.
        """
        line = self.browse(cr, uid, ids[0])

        lst_price = line.product_id.lst_price
        line_currency = line.currency_id.rate
        line_price = line.price_unit

        return self._compute_currency(
            cr, uid,
            base_currency,
            line_currency,
            lst_price,
            line_price,
            context
        )

    def compute_draft_line_base_currency(
        self, cr, uid, values, context=None
    ):
        """
        Update the values with the computed amount calculated.

        It used the user_id to get the company_id as during the create
        method, the company_id isn't always saved. But the company_id
        should be the user_id's company so we can get it from there.
        """
        predicate_keys = [
            'order_id', 'product_id', 'currency_id', 'price_unit'
        ]
        has_keys = reduce(lambda r, key: r and key in values,
                          predicate_keys,
                          True)

        if not has_keys:
            return

        sale_model = self.pool['sale.order']
        product_model = self.pool['product.product']
        cur_model = self.pool['res.currency']

        order_id = sale_model.browse(cr, uid, values['order_id'])
        product_id = product_model.browse(cr, uid, values['product_id'])
        currency_id = cur_model.browse(cr, uid, values['currency_id'])

        base_currency = order_id.user_id.company_id.currency_id.rate
        lst_price = product_id.lst_price
        line_currency = currency_id.rate
        line_price = values['price_unit']

        new_price = self._compute_currency(
            cr, uid,
            base_currency,
            line_currency,
            lst_price,
            line_price,
            context
        )
        values["amount_currency_calculated"] = new_price

    def create(self, cr, uid, values, context=None):
        """Add the amount_currency_calculated to new record."""
        self.compute_draft_line_base_currency(cr, uid, values, context=context)
        base_func = super(SaleOrderLine, self).create
        return base_func(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        """Update the amount_currency_calculated to draft lines."""
        base_func = super(SaleOrderLine, self).write
        ret = True

        for line in self.browse(cr, uid, ids, context=context):

            defaults = values.copy()

            if 'order_id' not in defaults and line.order_id.id:
                defaults['order_id'] = line.order_id.id

            if 'product_id' not in defaults and line.product_id.id:
                defaults['product_id'] = line.product_id.id

            if ('currency_id' not in defaults and
                    line.currency_id.id):
                defaults['currency_id'] = line.currency_id.id

            if 'price_unit' not in defaults:
                defaults['price_unit'] = line.price_unit

            if line.state == 'draft':
                self.compute_draft_line_base_currency(
                    cr, uid, defaults, context=context
                )

            base_ret = base_func(cr, uid, [line.id], defaults, context=context)
            ret = ret and base_ret

        return ret

    def product_id_change(
        self, cr, uid, ids, pricelist, product, qty=0,
        uom=False, qty_uos=0, uos=False, name='', partner_id=False,
        lang=False, update_tax=True, date_order=False, packaging=False,
        fiscal_position=False, flag=False, context=None
    ):
        """
        Add the currency_id to the view.

        The currency_id is necessary on order lines. It is then
        used to recompute the actual base price of the item.

        As price_unit can be different from the lst_price, it's not certain
        that we can always use the lst_price everywhere.
        """
        res = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position,
            flag=flag, context=context
        )

        if product and 'value' in res:

            lists = self.pool['product.pricelist']
            price_list = lists.browse(cr, uid, pricelist)
            currency_id = price_list.currency_id

            res['value']['currency_id'] = currency_id.id

        return res
