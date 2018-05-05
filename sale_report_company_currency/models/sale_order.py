# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_base_total = fields.Float(
        'Currency Total', compute='_amount_base_all', store=True)
    amount_base_untaxed = fields.Float(
        'Currency Untaxed', compute='_amount_base_all', store=True)
    amount_base_tax = fields.Float(
        'Currency Tax', compute='_amount_base_all', store=True)

    @api.multi
    @api.depends('amount_total', 'amount_tax', 'amount_untaxed')
    def _amount_base_all(self):
        for order in self:
            total = order.amount_total
            tax = order.amount_tax
            untaxed = order.amount_untaxed

            order_currency = order.pricelist_id.currency_id
            company_currency = order.company_id.currency_id
            if order_currency != company_currency:
                total = order_currency.compute(total, company_currency)
                tax = order_currency.compute(tax, company_currency)
                untaxed = order_currency.compute(untaxed, company_currency)

            order.amount_base_total = total
            order.amount_base_tax = tax
            order.amount_base_untaxed = untaxed


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_base_subtotal = fields.Float(
        'Currency Subtotal', compute='_base_amount_line', store=True)

    @api.multi
    @api.depends('product_id', 'product_uom_qty', 'price_unit', 'discount',
                 'order_id.partner_id', 'order_id.pricelist_id',
                 'order_id.pricelist_id.currency_id')
    def _base_amount_line(self):
        for line in self:
            price = line.price_subtotal

            order_currency = line.order_id.pricelist_id.currency_id
            company_currency = line.order_id.company_id.currency_id
            if order_currency != company_currency:
                price = order_currency.compute(price, company_currency)

            line.price_base_subtotal = price
