# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014 Camptocamp SA (http://www.camptocamp.com)
#     @author Romain Deheele, Vincent Renaville
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

{'name': 'Sale Order ProForma',
 'summary': 'New webkit report',
 'version': '1.1.1',
 'category': 'Reports/Webkit',
 'description': """
Sale order webkit
=================

* Add a sale ProForma webkit report on Sale Order.

Depends on base_headers_webkit community addon available here:
`https://launchpad.net/webkit-utils <https://launchpad.net/webkit-utils>`_

Contributors
------------

 * Romain Deheele <romain.deheele@camptocamp.com>
 * Vincent Renaville <vincent.renaville@camptocamp.com>
    """,
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'website': 'http://www.camptocamp.com',
 'license': 'AGPL-3',
 'depends': ['base', 'report_webkit', 'base_headers_webkit', 'sale'],
 'data': ['report.xml',
          ],
 'demo_xml': [],
 'test': [],
 'installable': False,
 'active': False,
 }
