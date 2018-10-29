# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2018 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SaleReport(models.Model):
    _inherit = "sale.report"

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str = select_str.replace(
            'sum(p.weight * l.product_uom_qty / u.factor * u2.factor) '
            'as weight,',
            'CASE'
            '    WHEN u.category_id = imd.res_id'
            '    THEN SUM(l.product_uom_qty / u.factor * u2.factor)'
            '    ELSE SUM(p.weight * l.product_uom_qty / u.factor * u2.factor)'
            'END AS weight,'
        )
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
