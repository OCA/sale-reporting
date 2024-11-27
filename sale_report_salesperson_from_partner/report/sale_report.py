from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    user_from_partner_id = fields.Many2one(
        "res.users",
        string="Salesperson From Partner",
        readonly=True,
    )

    def _group_by_sale(self, groupby=""):
        res = super()._group_by_sale(groupby)
        res += """,partner.user_id"""
        return res

    def _select_additional_fields(self, fields):
        fields["user_from_partner_id"] = ", partner.user_id as user_from_partner_id"
        return super()._select_additional_fields(fields)
