# -*- coding: utf-8 -*-
# Copyright 2013-2014 Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{"name": "Sale Comments",
 "summary": "Comments texts templates on Sale documents",
 "version": "10.0.1.2.0",
 "category": "Sale",
 "website": "https://github.com/OCA/sale-reporting",
 "author": "Camptocamp, Odoo Community Association (OCA)",
 "license": "AGPL-3",
 "depends": ["sale",
             "invoice_comment_template",
             ],
 "data": ['security/ir.model.access.csv',
          'views/sale_order_view.xml',
          'views/base_comment_template_view.xml',
          'views/report_saleorder.xml',
          ],
 'installable': True,
 }
