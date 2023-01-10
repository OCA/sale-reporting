# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.tools import float_is_zero


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
    multicompany_reporting_currency_rate = fields.Float(
        compute="_compute_multicompany_reporting_currency_rate",
        store=True,
        digits=(12, 6),
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
    def _compute_multicompany_reporting_currency_rate(self):
        for record in self:
            if not record.company_id:
                record.multicompany_reporting_currency_rate = (
                    record.multicompany_reporting_currency_id.with_context(
                        date=record.date_order
                    ).rate
                    or 1.0
                )
            elif (
                record.currency_id and record.multicompany_reporting_currency_id
            ):  # the following crashes if any one is undefined
                record.multicompany_reporting_currency_rate = self.env[
                    "res.currency"
                ]._get_conversion_rate(
                    record.currency_id,
                    record.multicompany_reporting_currency_id,
                    record.company_id,
                    record.date_order,
                )
            else:
                record.multicompany_reporting_currency_rate = 1.0

    @api.depends(
        "amount_total",
        "multicompany_reporting_currency_id",
        "multicompany_reporting_currency_rate",
    )
    def _compute_amount_multicompany_reporting_currency(self):
        for record in self:
            reporting_amount = (
                record.amount_total
                if (record.company_id.amount_option == "total")
                else record.amount_untaxed
            )
            if (
                record.currency_id == record.multicompany_reporting_currency_id
            ) or float_is_zero(
                record.multicompany_reporting_currency_rate,
                precision_rounding=(
                    record.currency_id or self.env.company.currency_id
                ).rounding,
            ):
                to_amount = reporting_amount
            else:
                to_amount = (
                    reporting_amount * record.multicompany_reporting_currency_rate
                )
            record.amount_multicompany_reporting_currency = to_amount
