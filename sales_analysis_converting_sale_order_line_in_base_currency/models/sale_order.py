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
from openerp.osv import fields, osv


class SaleOrder(osv.osv):

    """Override the sale.order model."""

    _inherit = 'sale.order'

    def action_button_confirm(self, cr, uid, ids, context=None):
        """
        Convert unit_price using the line and company currencies.

        Convert price using the currency if necessary or set the
        lst_price if no conversion is necessary. The reason to skip
        the conversion is to reduce the amount of error with roundings.
        """
        base_func = super(SaleOrder, self).action_button_confirm
        base_func(cr, uid, ids, context=context)

        for o in self.browse(cr, uid, ids):
            base_currency = o.company_id.currency_id.rate

            for line in o.order_line:
                new_price = line.compute_amount_currency(base_currency)
                line.write({
                    "amount_currency_calculated": new_price
                })


class SaleOrderLine(osv.osv):

    """Override the sale.order.line model."""

    _inherit = 'sale.order.line'

    _columns = {
        "order_line_currency": fields.many2one(
            'res.currency', 'Currency'
        ),
        "amount_currency_calculated": fields.float(
            'Amount converted', readonly=True
        ),
    }

    def _compute_currency(
        self, cr, uid, base_currency, line_currency, lst_price,
        line_price, context=None
    ):
        """Compute the base price of the product."""
        decimal_precision = self.pool['decimal.precision']
        precision = decimal_precision.precision_get(cr, uid, 'Account')

        if line_currency:
            to_currency = (line_currency / base_currency)
            to_base = (base_currency / line_currency)

            price_unit = lst_price * to_currency
            price_unit = round(price_unit, precision)

            if price_unit != line_price:
                # If price don't match, it means that the line_price
                # isn't purely dependent on lst_price
                return line_price * to_base

        # Otherwise return the lst_price
        return lst_price

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
        line_currency = line.order_line_currency.rate
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
        sale_model = self.pool['sale.order']
        product_model = self.pool['product.product']
        cur_model = self.pool['res.currency']

        order_id = sale_model.browse(cr, uid, values['order_id'])
        product_id = product_model.browse(cr, uid, values['product_id'])
        currency_id = cur_model.browse(cr, uid, values['order_line_currency'])

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
        line = self.browse(cr, uid, ids[0])

        if line.state == 'draft':
            defaults = {
                'order_id': line.order_id.id,
                'product_id': line.product_id.id,
                'order_line_currency': line.order_line_currency.id,
            }

            defaults.update(values)
            values = defaults
            self.compute_draft_line_base_currency(
                cr, uid, values, context=context
            )

        base_func = super(SaleOrderLine, self).write
        return base_func(cr, uid, ids, values, context=context)

    def product_id_change(
        self, cr, uid, ids, pricelist, product, qty=0,
        uom=False, qty_uos=0, uos=False, name='', partner_id=False,
        lang=False, update_tax=True, date_order=False, packaging=False,
        fiscal_position=False, flag=False, context=None
    ):
        """
        Add the order_line_currency to the view.

        The order_line_currency is necessary on order lines. It is then
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

            res['value']['order_line_currency'] = currency_id.id

        return res
