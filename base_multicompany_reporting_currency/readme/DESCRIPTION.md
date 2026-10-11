In Odoo standard, when it comes to reporting in a multicompany and
multicurrency environment, it should be done on the invoices.
(Cf Fabien Pinckaers tweet: <https://twitter.com/fpodoo/status/1511831215673913344>)

Nonetheless, some companies do not use the Invoicing or Accounting app in Odoo.
For example, when using only CRM and Sales. With this module, we introduce
the concept of currency for reporting to be set in General Settings.
This way we can reuse the idea behind
<https://github.com/OCA/sale-workflow/tree/10.0/sale_company_currency>,
but with a predefined currency.

This module adds:
- a setting in General Settings to set multicompany reporting currency which be applied
  to all companies
- a system parameter to store the chosen multicompany reporting currency DB-wide
- a mixin model to inherit for handling all basic operations - eg: automatically update
  the multicompany reporting currency on a model's records when the settings change
- a company-specific setting to choose which amount (total or untaxed) should be used
  for the multicompany reporting, for apps that report on documents with taxes

Multicompany reporting currency field will be used in other dependent modules to
compare amounts in different companies and documents.

NB: This module does not provide any feature for specific apps.
You should install ``sale_multicompany_reporting_currency`` from
<https://github.com/OCA/sale-reporting> or
``crm_multicompany_reporting_currency`` from <https://github.com/OCA/crm> to
have additional Total (Multicompany Reporting Currency) fields on specific apps.
