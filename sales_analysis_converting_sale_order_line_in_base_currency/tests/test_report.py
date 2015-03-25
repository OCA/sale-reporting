from openerp.tests import common


class TestReport(common.TransactionCase):

    def setUp(self):
        super(TestReport, self).setUp()
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
                    "order_line_currency": currency_id.id,
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
                    "order_line_currency": currency_id.id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                    "order_line_currency": currency_cad_id,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 15,
                    "order_line_currency": currency_cad_id,
                }
            )
        }, context=context)

        report_obj = self.sale_order_m.browse(
            cr, uid, sale_order_id, context=context
        )

        for line in report_obj.order_line:

            exchange = currency_id.rate / line.order_line_currency.rate
            new_price = exchange * line.price_unit
            self.assertAlmostEqual(line.amount_currency_calculated,
                                   new_price, 6)
