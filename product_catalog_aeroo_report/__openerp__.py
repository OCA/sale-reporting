# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ADHOC SA (<http://adhoc.com.ar>).
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
##############################################################################
{
    'name': 'Product Catalog Aeroo Report',
    'version': '1.0',
    'category': 'Aeroo Reporting',
    'sequence': 14,
    'summary': '',
    'description': """
Product Catalog Aeroo Report
============================
    """,
    'author':  'ADHOC',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'product',
        'report_aeroo',
    ],
    'data': [
        'wizard/product_catalog_wizard.xml',
        'security/ir.model.access.csv',
        'product_catalog.xml',
        'report/product_catalog_view.xml'
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
