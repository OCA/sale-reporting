# Copyright 2025 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAmountMulticompanyReportingCurrency(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.currency_swiss = cls.env.ref("base.CHF")
        cls.currency_euro = cls.env.ref("base.EUR")
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Tax with price include",
                "amount": 10,
            }
        )
        cls.invoice = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner_a.id,
                "invoice_date": fields.Date.today(),
                "currency_id": cls.currency_euro.id,
                "invoice_line_ids": [
                    (
                        0,
                        None,
                        {
                            "product_id": cls.product_a.id,
                            "quantity": 2,
                            "price_unit": 500,
                            "tax_ids": [(6, 0, cls.tax.ids)],
                        },
                    ),
                ],
            }
        )
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1.0038,
                "currency_id": cls.currency_swiss.id,
                "company_id": cls.env.company.id,
            }
        )
        cls.env["res.currency.rate"].create(
            {
                "name": fields.Date.today(),
                "rate": 1,
                "currency_id": cls.currency_euro.id,
                "company_id": cls.env.company.id,
            }
        )

    def test_amount_multicompany_reporting_currency(self):
        # Move currency is in EUR, Amount Multicompany Reporting Currency is CHF
        # Total amount used for reporting
        self.env["res.config.settings"].create(
            {
                "multicompany_reporting_currency": self.currency_swiss.id,
                "multicompany_reporting_amount": "total",
            }
        ).execute()

        self.assertAlmostEqual(
            self.invoice.amount_multicompany_reporting_currency, 1104.18
        )

        # Untaxed amount used for reporting
        self.env["res.config.settings"].create(
            {
                "multicompany_reporting_amount": "untaxed",
            }
        ).execute()

        self.assertAlmostEqual(
            self.invoice.amount_multicompany_reporting_currency, 1003.8
        )

        # Switch reporting currency to EUR (same than move)
        self.env["res.config.settings"].create(
            {
                "multicompany_reporting_currency": self.currency_euro.id,
                "multicompany_reporting_amount": "untaxed",
            }
        ).execute()

        self.assertAlmostEqual(
            self.invoice.amount_multicompany_reporting_currency, 1000
        )

        # Switch to total amount used for reporting
        self.env["res.config.settings"].create(
            {
                "multicompany_reporting_amount": "total",
            }
        ).execute()

        self.assertAlmostEqual(
            self.invoice.amount_multicompany_reporting_currency, 1100
        )
