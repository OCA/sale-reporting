# -*- coding: utf-8 -*-
# 2018 Exo Software, Lda.
# 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_product_image_size(self):
        return self.env['ir.values'].get_default(
            'sale.config.settings', 'product_image_size', 20)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_image = fields.Binary(
        related='product_id.image_small')
