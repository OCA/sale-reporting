# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    group_currency_id = fields.Many2one(
        "res.currency", compute="_compute_group_currency_id"
    )
    currency_rate = fields.Float(
        compute="_compute_currency_rate", store=True, digits=(12, 6)
    )
    amount_group_currency = fields.Monetary(
        currency_field="group_currency_id",
        compute="_compute_amount_group_currency",
        store=True,
        index=True,
        readonly=True,
    )

    def _compute_group_currency_id(self):
        group_currency_parameter = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_group_currency.group_currency_id")
        )
        group_currency_id = self.env["res.currency"].browse(
            int(group_currency_parameter)
        )
        for record in self:
            record.group_currency_id = group_currency_id

    @api.depends("date_open", "company_id", "group_currency_id")
    def _compute_currency_rate(self):
        # similar to currency_rate on sale.order
        for record in self:
            if (
                record.group_currency_id and record.company_currency
            ):  # the following crashes if any one is undefined
                record.currency_rate = self.env["res.currency"]._get_conversion_rate(
                    record.group_currency_id,
                    record.company_currency,
                    record.company_id,
                    record.date_open,
                )
            else:
                record.currency_rate = 1.0

    @api.depends("expected_revenue", "currency_rate", "group_currency_id")
    def _compute_amount_group_currency(self):
        for record in self:
            if record.company_currency == record.group_currency_id:
                to_amount = record.expected_revenue
            else:
                to_amount = record.expected_revenue / record.currency_rate
            record.amount_group_currency = to_amount
