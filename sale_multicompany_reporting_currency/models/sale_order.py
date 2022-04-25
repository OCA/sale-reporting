# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_multicompany_reporting_currency_id(self):
        multicompany_reporting_currency_parameter = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "base_multicompany_reporting_currency.multicompany_reporting_currency"
            )
        )
        return self.env["res.currency"].browse(
            int(multicompany_reporting_currency_parameter)
        )

    multicompany_reporting_currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_multicompany_reporting_currency_id",
        readonly=True,
        store=True,
        default=_get_multicompany_reporting_currency_id,
    )
    amount_multicompany_reporting_currency = fields.Monetary(
        currency_field="multicompany_reporting_currency_id",
        compute="_compute_amount_multicompany_reporting_currency",
        store=True,
        index=True,
        readonly=True,
    )

    @api.depends("pricelist_id.currency_id")
    def _compute_multicompany_reporting_currency_id(self):
        multicompany_reporting_currency_id = (
            self._get_multicompany_reporting_currency_id()
        )
        for record in self:
            record.multicompany_reporting_currency_id = (
                multicompany_reporting_currency_id
            )

    @api.depends(
        "pricelist_id", "date_order", "company_id", "multicompany_reporting_currency_id"
    )
    def _compute_currency_rate(self):
        super()._compute_currency_rate()
        for record in self:
            if (
                record.multicompany_reporting_currency_id and record.currency_id
            ):  # the following crashes if any one is undefined
                record.currency_rate = self.env["res.currency"]._get_conversion_rate(
                    record.multicompany_reporting_currency_id,
                    record.currency_id,
                    record.company_id,
                    record.date_order,
                )
        return True

    @api.depends("amount_total", "currency_rate", "multicompany_reporting_currency_id")
    def _compute_amount_multicompany_reporting_currency(self):
        for record in self:
            if record.currency_id == record.multicompany_reporting_currency_id:
                to_amount = record.amount_total
            else:
                to_amount = record.amount_total / record.currency_rate
            record.amount_multicompany_reporting_currency = to_amount
