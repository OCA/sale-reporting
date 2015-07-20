.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Sale reporting in company currency
==================================

This module records sale order prices in company currency along with the
pricelist currency and changes the Sales Team tickers and Dashboard to use
that.

Usage
=====

There are new stored fields on Sale Order and line objects usable in views and
reports.

The Sales Team tickers on the kanban view (except the 'Invoiced' ticker) now
show the amount in company currency.

Known issues / Roadmap
======================

* The currency conversion might be redone in some circumstances when the sale
  order is modified.
* Users having access to multiple companies with differing currencies might
  still get a useless cross-currency sum in some reports.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/sale-reporting/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/sale-reporting/issues/new?body=module:%20sale_report_company_currency%0Aversion:%201.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Ondřej Kuzník <ondrej.kuznik@credativ.co.uk>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
