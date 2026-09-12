import ast
import json
import random
from datetime import date

from babel.dates import format_date
from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.fields import Domain
from odoo.release import version
from odoo.tools import SQL


class CrmTeam(models.Model):
    _inherit = "crm.team"

    opportunities_count = fields.Integer(
        string="# Opportunities", compute="_compute_opportunities_data"
    )
    opportunities_amount = fields.Monetary(
        string="Opportunities Revenues", compute="_compute_opportunities_data"
    )
    opportunities_overdue_count = fields.Integer(
        string="# Overdue Opportunities", compute="_compute_opportunities_overdue_data"
    )
    opportunities_overdue_amount = fields.Monetary(
        string="Overdue Opportunities Revenues",
        compute="_compute_opportunities_overdue_data",
    )
    quotations_count = fields.Integer(
        compute="_compute_quotations_to_invoice",
        string="Number of quotations to invoice",
        readonly=True,
    )
    quotations_amount = fields.Float(
        compute="_compute_quotations_to_invoice",
        string="Amount of quotations to invoice",
        readonly=True,
    )
    sales_to_invoice_count = fields.Integer(
        compute="_compute_sales_to_invoice",
        string="Number of sales to invoice",
        readonly=True,
    )
    dashboard_graph_data = fields.Text(compute="_compute_dashboard_graph")

    def _prepare_invoice_domain(self):
        today = fields.Date.context_today(self.env.user)
        return Domain(
            [
                ("move_type", "in", ["out_invoice", "out_refund", "out_receipt"]),
                ("team_id", "in", self.ids),
                ("date", ">=", today.replace(day=1)),
                ("date", "<=", today),
            ]
        )

    def _compute_invoiced(self):
        if not self:
            return
        domain_list = ast.literal_eval(self.env.company.sales_team_invoiced_domain)
        if not domain_list:
            return super()._compute_invoiced()
        invoiced_domain = Domain.AND([self._prepare_invoice_domain(), domain_list])
        team_data = self.env["account.move"]._read_group(
            invoiced_domain,
            groupby=["team_id"],
            aggregates=["amount_untaxed_signed:sum"],
        )
        team_dict = dict(team_data)
        for team in self:
            team.invoiced = team_dict.get(team) or 0.0

    # Recovered from Odoo 19
    def _compute_opportunities_data(self):
        opportunity_data = self.env["crm.lead"]._read_group(
            [
                ("team_id", "in", self.ids),
                ("probability", "<", 100),
                ("type", "=", "opportunity"),
            ],
            ["team_id"],
            ["__count", "expected_revenue:sum"],
        )
        counts_amounts = {
            team.id: (count, expected_revenue_sum)
            for team, count, expected_revenue_sum in opportunity_data
        }
        for team in self:
            team.opportunities_count, team.opportunities_amount = counts_amounts.get(
                team.id, (0, 0)
            )

    def _compute_opportunities_overdue_data(self):
        opportunity_data = self.env["crm.lead"]._read_group(
            [
                ("team_id", "in", self.ids),
                ("probability", "<", 100),
                ("type", "=", "opportunity"),
                ("date_deadline", "<", fields.Date.to_string(fields.Datetime.now())),
            ],
            ["team_id"],
            ["__count", "expected_revenue:sum"],
        )
        counts_amounts = {
            team.id: (count, expected_revenue_sum)
            for team, count, expected_revenue_sum in opportunity_data
        }
        for team in self:
            team.opportunities_overdue_count, team.opportunities_overdue_amount = (
                counts_amounts.get(team.id, (0, 0))
            )

    def _compute_quotations_to_invoice(self):
        query = self.env["sale.order"]._search(
            [("team_id", "in", self.ids), ("state", "in", ("draft", "sent"))]
        )
        select_sql = SQL(
            """
            SELECT team_id, count(*), sum(amount_total /
                CASE COALESCE(currency_rate, 0)
                WHEN 0 THEN 1.0
                ELSE currency_rate
                END
            ) as amount_total
            FROM sale_order
            WHERE %s
            GROUP BY team_id
        """,
            query.where_clause or SQL("TRUE"),
        )
        self.env.cr.execute(select_sql)
        quotation_data = self.env.cr.dictfetchall()
        teams = self.browse()
        for data in quotation_data:
            team = self.browse(data["team_id"])
            team.quotations_amount = data["amount_total"]
            team.quotations_count = data["count"]
            teams |= team
        remaining = self - teams
        remaining.quotations_amount = 0
        remaining.quotations_count = 0

    def _compute_sales_to_invoice(self):
        sale_order_data = self.env["sale.order"]._read_group(
            [
                ("team_id", "in", self.ids),
                ("invoice_status", "=", "to invoice"),
            ],
            ["team_id"],
            ["__count"],
        )
        data_map = {team.id: count for team, count in sale_order_data}
        for team in self:
            team.sales_to_invoice_count = data_map.get(team.id, 0.0)

    def _compute_dashboard_graph(self):
        for team in self:
            team.dashboard_graph_data = json.dumps(team._get_dashboard_graph_data())

    def _graph_get_dates(self, today):
        """return a coherent start and end date for the dashboard graph covering
        a month period grouped by week."""
        start_date = today - relativedelta(months=1)
        # we take the start of the following week if we group by week
        # (to avoid having twice the same week from different month)
        start_date += relativedelta(days=8 - start_date.isocalendar()[2])
        return [start_date, today]

    def _graph_get_model(self):
        if self._in_sale_scope():
            return "sale.report"

    def _graph_date_column(self):
        return "date"

    def _graph_x_query(self):
        return SQL("EXTRACT(WEEK FROM %s)", SQL.identifier(self._graph_date_column()))

    def _graph_y_query(self):
        if self.use_opportunities and self.env.context.get("in_sales_app"):
            return SQL("SUM(price_subtotal)")

    def _extra_sql_conditions(self):
        if self.use_opportunities and self.env.context.get("in_sales_app"):
            return SQL("AND state = 'sale'")
        return SQL("")

    def _graph_title_and_key(self):
        """Returns an array containing the appropriate graph title and key respectively.

        The key is for lineCharts, to have the on-hover label.
        """
        if self.env.context.get("in_sales_app"):
            return ["", self.env._("Sales: Untaxed Total")]
        return super()._graph_title_and_key()

    def _graph_data(self, start_date, end_date):
        """return format should be an iterable of dicts that contain
        {'x_value': ..., 'y_value': ...}
        x_values should be weeks.
        y_values are floats.
        """
        # apply rules
        dashboard_graph_model = self._graph_get_model()
        GraphModel = self.env[dashboard_graph_model].with_company(self.company_id)
        extra_conditions = self._extra_sql_conditions()
        where_query = GraphModel._search([])
        if where_query.where_clause:
            extra_conditions = SQL(
                "%s AND %s", extra_conditions, where_query.where_clause
            )
        query = SQL(
            """SELECT %(x_query)s as x_value, %(y_query)s as y_value
                FROM %(table)s
            WHERE team_id = %(team_id)s
                AND DATE(%(date_column)s) >= %(start_date)s
                AND DATE(%(date_column)s) <= %(end_date)s
                %(extra_conditions)s
            GROUP BY x_value;""",
            x_query=self._graph_x_query(),
            y_query=self._graph_y_query(),
            table=where_query.from_clause,
            team_id=self.id,
            date_column=SQL.identifier(self._graph_date_column()),
            start_date=start_date,
            end_date=end_date,
            extra_conditions=extra_conditions,
        )

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def _get_dashboard_graph_data(self):
        def get_week_name(start_date, locale):
            """Generates a week name (string) from a datetime according to the locale:
            E.g.: locale    start_date (datetime)      return string
                  "en_US"      November 16th           "16-22 Nov"
                  "en_US"      December 28th           "28 Dec-3 Jan"
            """
            if (start_date + relativedelta(days=6)).month == start_date.month:
                short_name_from = format_date(start_date, "d", locale=locale)
            else:
                short_name_from = format_date(start_date, "d MMM", locale=locale)
            short_name_to = format_date(
                start_date + relativedelta(days=6), "d MMM", locale=locale
            )
            return short_name_from + "-" + short_name_to

        self.ensure_one()
        values = []
        today = fields.Date.from_string(fields.Date.context_today(self))
        start_date, end_date = self._graph_get_dates(today)
        graph_data = self._graph_data(start_date, end_date)
        x_field = "label"
        y_field = "value"
        # generate all required x_fields and update the y_values where we have
        # data for them
        locale = self.env.context.get("lang") or "en_US"
        weeks_in_start_year = int(
            date(start_date.year, 12, 28).isocalendar()[1]
        )  # This date is always in the last week of ISO years
        week_count = (
            end_date.isocalendar()[1] - start_date.isocalendar()[1]
        ) % weeks_in_start_year + 1
        for week in range(week_count):
            short_name = get_week_name(
                start_date + relativedelta(days=7 * week), locale
            )
            values.append(
                {
                    x_field: short_name,
                    y_field: 0,
                    "type": "future" if week + 1 == week_count else "past",
                }
            )

        for data_item in graph_data:
            index = int(
                (data_item.get("x_value") - start_date.isocalendar()[1])
                % weeks_in_start_year
            )
            values[index][y_field] = data_item.get("y_value")
        [graph_title, graph_key] = self._graph_title_and_key()
        color = "#875A7B" if "+e" in version else "#7c7bad"
        # If no actual data available, show some sample data
        if not graph_data:
            graph_key = self.env._("Sample data")
            for value in values:
                value["type"] = "o_sample_data"
                # we use unrealistic values for the sample data
                value["value"] = random.randint(0, 20)
        return [
            {
                "values": values,
                "area": True,
                "title": graph_title,
                "key": graph_key,
                "color": color,
            }
        ]
