# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleReport(models.Model):
    _inherit = "sale.report"

    def _available_additional_pos_fields(self):
        res = super()._available_additional_pos_fields()
        res["product_tag_id"] = "fpt.id"
        return res

    def _from_pos(self):
        res = super()._from_pos()
        res += """
            LEFT JOIN first_product_tag fpt ON (t.id = fpt.product_template_id)
        """
        return res

    def _group_by_pos(self):
        res = super()._group_by_pos()
        res += ",fpt.id"
        return res
