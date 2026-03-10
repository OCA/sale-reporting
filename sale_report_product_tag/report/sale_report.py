# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    product_tag_id = fields.Many2one("product.tag", string="Product Tag", readonly=True)

    def _with_sale(self):
        with_ = super()._with_sale()
        res = (
            (with_ + "," if with_ else "")
            + """
            first_product_tag AS (
                SELECT
                    pt.id AS product_template_id,
                    (array_agg(ptg.id))[1] AS id
                FROM product_template pt
                LEFT JOIN product_tag_product_template_rel ptgpt ON
                    (pt.id = ptgpt.product_template_id)
                LEFT JOIN product_tag ptg ON (ptgpt.product_tag_id = ptg.id)
                GROUP BY pt.id
            )"""
        )
        return res

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["product_tag_id"] = "fpt.id"
        return res

    def _from_sale(self):
        res = super()._from_sale()
        res += "LEFT JOIN first_product_tag fpt ON (t.id = fpt.product_template_id)"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ",fpt.id"
        return res
