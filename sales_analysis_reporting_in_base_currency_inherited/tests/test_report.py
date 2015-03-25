from openerp.tests import common


class TestReport(common.TransactionCase):

    def setUp(self):
        super(TestReport, self).setUp()
        self.context = {}

        self.sale_report_m = self.registry('sale.report')
        self.sale_order_m = self.registry('sale.order')

    def make_lines(self, *args):
        return map(lambda x: (0, 0, x), args)

    def test_load_report(self):
        cr, uid, context = self.cr, self.uid, self.context

        ids = self.sale_report_m.search(cr, uid, [], context=context)

        self.sale_order_m.create(cr, uid, {
            "name": "Sale report test",
            "partner_id": self.ref("base.res_partner_1"),
            "partner_invoice_id": self.ref("base.res_partner_1"),
            "partner_shipping_id": self.ref("base.res_partner_1"),
            "pricelist_id": self.ref("product.list0"),
            "order_line": self.make_lines(
                {
                    "name": "product_7",
                    "product_id": self.ref("product.product_product_7"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                },
                {
                    "name": "product_3",
                    "product_id": self.ref("product.product_product_3"),
                    "product_uom_qty": 1,
                    "price_unit": 10,
                }
            )

        }, context=context)

        ids2 = self.sale_report_m.search(cr, uid, [], context=context)
        report_obj = self.sale_report_m.browse(cr, uid, max(ids2))

        self.assertEqual(len(ids2) - len(ids), 2)
        # Currency not added to lines so 0 we can't calculate the price
        # without currency
        self.assertEqual(report_obj.price_total_calculated, 0)
