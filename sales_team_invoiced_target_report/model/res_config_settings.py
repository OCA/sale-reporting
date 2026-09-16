from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sales_team_invoiced_domain = fields.Char(
        related="company_id.sales_team_invoiced_domain", readonly=False
    )
