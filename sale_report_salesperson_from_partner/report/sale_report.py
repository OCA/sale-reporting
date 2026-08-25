from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    user_from_partner_id = fields.Many2one(
        "res.users",
        string="Salesperson From Partner",
        readonly=True,
    )

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """,partner.user_id"""
        return res

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["user_from_partner_id"] = "partner.user_id"
        return res
