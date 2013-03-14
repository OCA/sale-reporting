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

{'name': 'HTML note in product reported in sale order report',
 'version': '1.0.1',
 'category': 'other',
 'description': """
Sale product note
=================

Replaces sale descritpion in product by a HTML field.
Then it adds this description into the HTML note
of the sale order line when product is changed""",
 'author': 'Camptocamp',
 'website': 'http://www.camptocamp.com',
 'depends': ['product', 'sale', 'sale_order_webkit'],
 'init_xml': [],
 'update_xml': [],
 'demo_xml': [],
 'test': [],
 'installable': True,
 'active': False,
 }
