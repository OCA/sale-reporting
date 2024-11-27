from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_from_partner_id = fields.Many2one(
        string="Salesperson From Partner", related="partner_id.user_id", store=True
    )
