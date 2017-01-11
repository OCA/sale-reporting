# -*- coding: utf-8 -*-
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models
import openerp.addons.decimal_precision as dp


class SaleReport(models.Model):
    _inherit = "sale.report"

    weight = fields.Float(digits=dp.get_precision('Stock Weight'))

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            , CASE
                WHEN u.category_id = imd.res_id
                THEN SUM(l.product_uom_qty / u.factor * u2.factor)
                ELSE SUM(p.weight * l.product_uom_qty / u.factor * u2.factor)
            END AS weight
            """
        return select_str

    def _from(self):
        from_str = super(SaleReport, self)._from()
        from_str += """
            JOIN ir_model_data imd
                ON (imd.module = 'product' AND
                    imd.name = 'product_uom_categ_kgm')
            """
        return from_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += ", p.weight, u.category_id, imd.res_id"
        return group_by_str
