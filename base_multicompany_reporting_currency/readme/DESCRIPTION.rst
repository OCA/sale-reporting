In Odoo standard, when it comes to reporting in a multicompany and multicurrency environment, it should be done on the invoices. (Cf Fabien Pinckaers tweet: https://twitter.com/fpodoo/status/1511831215673913344)
Nonetheless, some companies do not use the Invoicing or Accounting app in Odoo. For example, when using only CRM and Sales.
With this module, we introduce the concept of currency for reporting to be set in General Settings.
This way we can reuse the idea behind https://github.com/OCA/sale-workflow/tree/10.0/sale_company_currency, but with a predefined currency.

This Module adds a setting in General Settings to set multicompany reporting currency which be applied to all companies.
Multicompany reporting currency field will be used in other dependent modules to compare amounts in different companies and documents.
NB: This module does not provide any feature itself.
You should install `sale_multicompany_reporting_currency` from https://github.com/OCA/sale-reporting or `crm_multicompany_reporting_currency` from https://github.com/OCA/crm to have additional Total (Multicompany Reporting Currency) field.
