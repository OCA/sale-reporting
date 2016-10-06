# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Nicolas Bessi
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

{'name': 'HTML note from sale order in invoice',
 'version': '1.0.0',
 'category': 'other',
 'description': """
Sale order to invoice notes
===========================

This module forwards the `note` field of sale order lines to the
`note` field of invoice line when an invoice in generated from a sale
order.
""",
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'website': 'http://www.camptocamp.com',
 'license': 'AGPL-3',
 'depends': ['html_invoice_product_note',
             'html_sale_product_note',
             'invoice_webkit',
             'sale_order_webkit'],
 'data': [],
 'test': [],
 'installable': False,
 'active': False,
 }
