# -*- coding: utf-8 -*-
#   Copyright 2017 Camptocamp SA (http://www.camptocamp.com)
#   @author Guewen Baconnier Vincent Renaville
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sales Order Report With Note',
    'version': '10.0.1.0.0',
    'category': 'Reports/Qweb',
    'license': 'AGPL-3',
    "author": "Camptocamp SA,"
              "Eficent, "
              "Serpent CS,"
              "Odoo Community Association (OCA)",
    'website': "https://odoo-community.org/",
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/report_saleorder_qweb.xml',
        'views/sale_view.xml'
    ],
    'installable': True,
}
