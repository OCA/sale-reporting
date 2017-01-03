# -*- coding: utf-8 -*-
# © 2013-2014 Nicolas Bessi (Camptocamp SA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
 'name': 'Sale Comments',
 'summary': 'Comments texts templates on Sale documents',
 'version': '9.0.1.0.0',
 'license': 'AGPL-3',
 'depends': ['sale',
             'invoice_comment_template',
             ],
 'author': 'Camptocamp,Odoo Community Association (OCA)',
 'data': ['data/sale_order_view.xml',
          'data/base_comment_template_view.xml',
          'views/report_saleorder.xml',
          'security/ir.model.access.csv',
          ],
 'category': 'Sale',
 'installable': True,
}
