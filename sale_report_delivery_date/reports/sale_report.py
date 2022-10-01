# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    delivery_date = fields.Datetime(readonly=True)

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        if not fields:
            fields = {}
        with_sale_order_line_delivery_dates = """
            sale_order_line_delivery_date AS (
                SELECT
                    m.sale_line_id AS id,
                    MAX(date) AS delivery_date
                FROM stock_move m
                WHERE m.state = 'done'
                AND m.sale_line_id IS NOT NULL
                GROUP BY m.sale_line_id
            )
        """
        with_clause = (
            with_sale_order_line_delivery_dates
            if not with_clause
            else ", ".join([with_clause, with_sale_order_line_delivery_dates])
        )
        return super()._query(
            with_clause=with_clause,
            fields=fields,
            groupby=groupby,
            from_clause=from_clause,
        )

    def _from_sale(self, from_clause=""):
        res = super()._from_sale(from_clause=from_clause)
        res += """
            LEFT JOIN sale_order_line_delivery_date soldd ON l.id = soldd.id
        """
        return res

    def _select_sale(self, fields=None):
        res = super()._select_sale(fields=fields)
        res += ", soldd.delivery_date"
        return res

    def _group_by_sale(self, groupby=""):
        res = super()._group_by_sale(groupby=groupby)
        res += ", soldd.delivery_date"
        return res
