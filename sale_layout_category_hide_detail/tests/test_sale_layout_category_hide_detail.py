# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common


class TestSaleLastPriceInfo(common.TransactionCase):

    def setUp(self):
        super(TestSaleLastPriceInfo, self).setUp()

        # partner
        partner_1 = self.env.ref('base.res_partner_1')
        # Products
        product_product_16 = self.env.ref('product.product_product_16')
        product_product_24 = self.env.ref('product.product_product_24')
        product_order_01 = self.env.ref('product.product_order_01')
        # Report Layout Categories
        self.sale_layout_cat_1 = self.env.ref('sale.sale_layout_cat_1')
        self.sale_layout_cat_2 = self.env.ref('sale.sale_layout_cat_2')

        self.sale_order = self.env['sale.order'].create({
            'partner_id': partner_1.id,
            'order_line': [
                (0, 0, {
                    'name': product_product_16.name,
                    'product_id': product_product_16.id,
                    'layout_category_id': self.sale_layout_cat_1.id,
                    'product_uom_qty': 1,
                    'price_unit': 100,
                }),
                (0, 0, {
                    'name': product_product_24.name,
                    'product_id': product_product_24.id,
                    'layout_category_id': self.sale_layout_cat_1.id,
                    'product_uom_qty': 1,
                    'price_unit': 200,
                }),
                (0, 0, {
                    'name': product_order_01.name,
                    'product_id': product_order_01.id,
                    'layout_category_id': self.sale_layout_cat_2.id,
                    'product_uom_qty': 1,
                    'price_unit': 300,
                }),
            ],
        })
        config = self.env['res.config.settings'].create({})
        config.group_sale_layout = True
        config.execute()

    def test_sale_order_order_lines_layouted(self):
        self.check_order_lines_layouted(self.sale_order)

    def test_account_invoice_order_lines_layouted(self):
        # Confirm sale order
        self.sale_order.action_confirm()

        # Create invoice from self.sale_order
        context = {
            "active_model": 'sale.order',
            "active_ids": [self.sale_order.id],
            "active_id": self.sale_order.id,
            "open_invoices": True,
        }
        payment = self.env['sale.advance.payment.inv'].create({
            'advance_payment_method': 'all',
        })
        action_invoice = payment.with_context(context).create_invoices()
        invoice_id = action_invoice['res_id']
        invoice = self.env['account.invoice'].browse(invoice_id)

        # Check hide_details
        self.check_order_lines_layouted(invoice)

    def check_order_lines_layouted(self, obj):
        report_pages = obj.order_lines_layouted()

        # There are two pages because sale_layout_cat_1.pagebreak == True
        # In the first page is sale_layout_cat_1
        self.assertEqual(report_pages[0][0]['name'],
                         self.sale_layout_cat_1.name)
        # In the second page is sale_layout_cat_2
        self.assertEqual(report_pages[1][0]['name'],
                         self.sale_layout_cat_2.name)

        # After set self.sale_layout_cat_1.hide_details = True the returned
        # list of order_lines_layouted method will be different,
        # sale_layout_cat_1 dict will have the followings changes:
        #   - Set 'hide_details' on True
        #   - Set 'lines' empty
        # The other layout dict (sale_layout_cat_2 dict) wont be affected
        self.sale_layout_cat_1.hide_details = True
        report_pages_hide_details = obj.order_lines_layouted()

        report_pages[0][0].update(
            hide_details=True,
            lines=list(),
        )
        self.assertEqual(report_pages[0][0], report_pages_hide_details[0][0])
        self.assertEqual(report_pages[1][0], report_pages_hide_details[1][0])
