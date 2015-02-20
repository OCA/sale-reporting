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

{
    'name': 'Sales analysis reporting in base currency',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Others',
    'summary': 'Sales Analysis use consistant line price',
    'description': """
Sales analysis reporting in base currency
=========================================
When you have several invoices, Odoo displays the
total amounts for a defined period in the Reporting
Module, Sales Analysis entry. This total is wrong
if you have made sales in different currencies as
Odoo ignores currencies in this instance.

This module therefore allows the system to assign a
converted amount in the default company currency
and associates it to a sale.order made in a
different currency. The rate is chosen when the
sales order is set to done.

The sales analysis reporting tool is therefore
modified to present a consistent total for your
sales in your base currency.

This module has dependencies to :
---------------------------------
* account

**Warning : this module will not work in a multi
company setup**

Contributors
------------
* Loïc Faure-Lacroix <loic.lacroix@savoirfairelinux.com>
""",
    'depends': [
        'sales_analysis_converting_sale_order_line_in_base_currency',
        'sales_analysis_reporting_in_base_currency_inherited',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
    ],
    'installable': True,
}
