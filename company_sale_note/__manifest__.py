# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Company sale note",
    'summary': """
        This module add a note field on the company who'll be printed on every
        sale reports.""",
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/sale-reporting",
    'category': 'sale',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'document',
    ],
    'data': [
        'views/sale_config_settings.xml',
        'reports/report_saleorder_document.xml'
    ]
}
