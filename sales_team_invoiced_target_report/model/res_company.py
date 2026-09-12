from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sales_team_invoiced_domain = fields.Char(
        default="[('payment_state', 'in', ['in_payment', 'paid', 'reversed'])]"
    )
