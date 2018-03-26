# -*- coding: utf-8 -*-
# 2018 Exo Software, Lda.
# 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    product_image_size = fields.Integer(
        help="Maximum size (in millimeters) for product images in sales "
        "orders and quotations. The default value is 20mm.")

    @api.model
    def get_default_product_image_size(self, fields):  \
            # pylint: disable=redefined-outer-name, unused-argument
        return {
            'product_image_size': self.env['ir.values'].get_default(
                'sale.config.settings', 'product_image_size') or 20
        }

    @api.multi
    def set_default_product_image_size(self):
        ir_values = self.env['ir.values']
        if self.env['res.users'].has_group('sales_team.group_sale_manager'):
            ir_values = ir_values.sudo()
        ir_values.set_default('sale.config.settings', 'product_image_size',
                              self.product_image_size)

    @api.constrains('product_image_size')
    def _check_product_image_size(self):
        if not 5 <= self.product_image_size <= 50:
            raise ValidationError(_(
                "Invalid product image size: %s. Please choose "
                "a number between 5 and 50.") % self.product_image_size)
