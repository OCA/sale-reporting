# Copyright 2022 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


from odoo import fields

from odoo.addons.sale.tests.common import TestSaleCommon


class TestAmountMulticompanyReportingCurrency(TestSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.currency_swiss_id = cls.env.ref("base.CHF").id
        cls.currency_euro_id = cls.env.ref("base.EUR").id
        cls.belgium = cls.env.ref("base.be").id
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_a.id,
                "partner_invoice_id": cls.partner_a.id,
                "partner_shipping_id": cls.partner_a.id,
                "pricelist_id": cls.company_data["default_pricelist"].id,
            }
        )
        cls.sale_order.pricelist_id.currency_id = cls.currency_euro_id
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1.01,
                "currency_id": cls.currency_swiss_id,
                "company_id": cls.env.company.id,
            }
        )
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1,
                "currency_id": cls.currency_euro_id,
                "company_id": cls.env.company.id,
            }
        )

    def test_amount_multicompany_reporting_currency(self):
        # Order currency is in EUR, Amount Multicompany Reporting Currency is CHF
        self.env["res.config.settings"].create(
            {"multicompany_reporting_currency": self.currency_swiss_id}
        ).execute()

        self.sol_product_order = self.env["sale.order.line"].create(
            {
                "name": self.company_data["product_order_no"].name,
                "product_id": self.company_data["product_order_no"].id,
                "product_uom_qty": 2,
                "product_uom": self.company_data["product_order_no"].uom_id.id,
                "price_unit": 500,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )
        self.assertEqual(self.sale_order.amount_multicompany_reporting_currency, 1010)
        # Order currency is in EUR, Amount Multicompany Reporting Currency is EUR
        self.env["res.config.settings"].create(
            {"multicompany_reporting_currency": self.currency_euro_id}
        ).execute()
        self.sol_serv_deliver = self.env["sale.order.line"].create(
            {
                "name": self.company_data["product_service_delivery"].name,
                "product_id": self.company_data["product_service_delivery"].id,
                "product_uom_qty": 1,
                "product_uom": self.company_data["product_service_delivery"].uom_id.id,
                "price_unit": 750,
                "order_id": self.sale_order.id,
                "tax_id": False,
            }
        )
        self.assertEqual(self.sale_order.amount_multicompany_reporting_currency, 1750)
        # if we remove Currency from Sale Order we expect currency_rate to be 1.0
        self.sale_order.currency_id = False
        self.sol_product_order.price_unit = 250
        self.sol_serv_deliver.price_unit = 100
        self.assertEqual(self.sale_order.amount_multicompany_reporting_currency, 600)
