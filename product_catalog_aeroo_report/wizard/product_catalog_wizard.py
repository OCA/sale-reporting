# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, _


class product_catalog(models.TransientModel):
    _name = 'product_catalog'
    _description = 'Wizard to generate the Product Catalog Report with Aeroo'

    product_catalog_report_id = fields.Many2one(
        'product.product_catalog_report',
        'Product Catalog',
        required=True)

    def generate_report(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]

        catalog = wizard.product_catalog_report_id
        if not catalog:
            return {'type': 'ir.actions.act_window_close'}

        return self.pool['product.product_catalog_report'].generate_report(
            cr, uid, [catalog.id], context)
