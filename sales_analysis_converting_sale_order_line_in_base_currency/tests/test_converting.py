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
from openerp.tests import common
from openerp.addons.decimal_precision import get_precision


class TestConvertingPrice(common.TransactionCase):

    def setUp(self):
        super(TestConvertingPrice, self).setUp()
        self.context = {}

        self.sale_report_m = self.registry('sale.report')
        self.sale_order_m = self.registry('sale.order')
        self.user_m = self.registry('res.users')
        self.pricelist_m = self.registry('product.pricelist')

    def make_lines(self, *args):
        return map(lambda x: (0, 0, x), args)

    def test_converting_same_currency(self):
        cr, uid, context = self.cr, self.uid, self.context

        user_obj = self.user_m.browse(cr, uid, uid, context=context)
        pricelist_id = self.ref("product.list0")
        pricelist_obj = self.pricelist_m.browse(
            cr, uid, pricelist_id, context=context
        )

        currency_id = user_obj.company_id.currency_id

        self.assertEqual(currency_id.id, pricelist_obj.currency_id.id)

        sale_order_id = self.sale_order_m.create(cr, uid, {
            "name": "Sale report test",
            "partner_id": self.ref("base.res_partner_1"),
            "partner_invoice_id": self.ref("base.res_partner_1"),
            "partner_shipping_id": self.ref("base.res_partner_1"),
            "pricelist_id": self.ref("product.list0"),
            "order_line": self.make_lines(
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                    "currency_id": currency_id.id,
                }
            )
        }, context=context)

        report_obj = self.sale_order_m.browse(
            cr, uid, sale_order_id, context=context
        )
        # Currency not added to lines so 0 we can't calculate the price
        # without currency
        self.assertEqual(report_obj.order_line[0].amount_currency_calculated,
                         10)

    def test_converting_different_currencies(self):
        cr, uid, context = self.cr, self.uid, self.context

        user_obj = self.user_m.browse(cr, uid, uid, context=context)
        pricelist_id = self.ref("product.list0")
        pricelist_obj = self.pricelist_m.browse(
            cr, uid, pricelist_id, context=context
        )

        currency_id = user_obj.company_id.currency_id
        currency_cad_id = self.ref('base.CAD')

        self.assertEqual(currency_id.id, pricelist_obj.currency_id.id)

        sale_order_id = self.sale_order_m.create(cr, uid, {
            "name": "Sale report test",
            "partner_id": self.ref("base.res_partner_1"),
            "partner_invoice_id": self.ref("base.res_partner_1"),
            "partner_shipping_id": self.ref("base.res_partner_1"),
            "pricelist_id": self.ref("product.list0"),
            "order_line": self.make_lines(
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 20,
                    "currency_id": currency_id.id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                    "currency_id": currency_cad_id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 15,
                    "currency_id": currency_cad_id,
                }
            )
        }, context=context)

        report_obj = self.sale_order_m.browse(
            cr, uid, sale_order_id, context=context
        )

        precision = get_precision("Account")(cr)[1]

        for line in report_obj.order_line:

            exchange = currency_id.rate / line.currency_id.rate
            new_price = exchange * line.price_unit
            self.assertEqual(line.amount_currency_calculated,
                             round(new_price, precision))

    def test_converting_different_currencies_write(self):
        cr, uid, context = self.cr, self.uid, self.context

        user_obj = self.user_m.browse(cr, uid, uid, context=context)
        pricelist_id = self.ref("product.list0")
        pricelist_obj = self.pricelist_m.browse(
            cr, uid, pricelist_id, context=context
        )

        currency_id = user_obj.company_id.currency_id
        currency_cad_id = self.ref('base.CAD')

        self.assertEqual(currency_id.id, pricelist_obj.currency_id.id)

        sale_order_id = self.sale_order_m.create(cr, uid, {
            "name": "Sale report test",
            "partner_id": self.ref("base.res_partner_1"),
            "partner_invoice_id": self.ref("base.res_partner_1"),
            "partner_shipping_id": self.ref("base.res_partner_1"),
            "pricelist_id": self.ref("product.list0"),
            "order_line": self.make_lines(
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 20,
                    "currency_id": currency_id.id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                    "currency_id": currency_cad_id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 15,
                    "currency_id": currency_cad_id,
                }
            )
        }, context=context)

        report_obj = self.sale_order_m.browse(
            cr, uid, sale_order_id, context=context
        )

        precision = get_precision("Account")(cr)[1]

        for line in report_obj.order_line:

            exchange = currency_id.rate / line.currency_id.rate
            new_price = exchange * line.price_unit
            self.assertEqual(line.amount_currency_calculated,
                             round(new_price, precision))

            line.write({"price_unit": 30}, context=context)
            line.refresh()

            self.assertEqual(line.price_unit, 30, "Price should be 30")
            self.assertEqual(line.amount_currency_calculated,
                             round(30 * exchange, precision))
