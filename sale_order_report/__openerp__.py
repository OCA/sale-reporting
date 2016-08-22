# -*- coding: utf-8 -*-
# Copyright (c) 2014 Camptocamp SA (http://www.camptocamp.com)
# @author Guewen Baconnier Vincent Renaville
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sales Order Report with Notes',
    'version': '8.0.1.0.0',
    'category': 'Reports/Qweb',
    'license': 'AGPL-3',
    "author": "Camptocamp SA,"
              "Eficent Business and IT Consulting Services S.L., ",
    'website': "https://odoo-community.org/",
    'depends': ['sale'],
    'data': ['security/ir.model.access.csv',
              'report/sale_report.xml',
              'views/report_saleorder_qweb.xml',
              'views/sale_view.xml'],
    'installable': True,
}
