# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import api, fields, models, tools


class SaleReportDeliverd(models.Model):
    _name = "sale.report.delivered"
    _description = "Sales Delivered Analysis Report"
    _auto = False
    _rec_name = "date"
    _order = "date desc"

    name = fields.Char("Order Reference", readonly=True)
    date = fields.Datetime(readonly=True)
    product_id = fields.Many2one("product.product", "Product Variant", readonly=True)
    product_uom = fields.Many2one("uom.uom", "Unit of Measure", readonly=True)
    product_uom_qty = fields.Float("Qty", readonly=True)
    partner_id = fields.Many2one("res.partner", "Customer", readonly=True)
    company_id = fields.Many2one("res.company", "Company", readonly=True)
    user_from_partner_id = fields.Many2one(
        "res.users", "Salesperson From Partner", readonly=True
    )
    user_id = fields.Many2one("res.users", "Salesperson", readonly=True)
    price_subtotal = fields.Float("Untaxed total delivered", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", "Product", readonly=True)
    categ_id = fields.Many2one("product.category", "Product Category", readonly=True)
    nbr = fields.Integer("# of Lines", readonly=True)
    pricelist_id = fields.Many2one("product.pricelist", "Pricelist", readonly=True)
    analytic_account_id = fields.Many2one(
        "account.analytic.account", "Analytic Account", readonly=True
    )
    team_id = fields.Many2one("crm.team", "Sales Team", readonly=True)
    country_id = fields.Many2one("res.country", "Customer Country", readonly=True)
    industry_id = fields.Many2one(
        "res.partner.industry", "Customer Industry", readonly=True
    )
    commercial_partner_id = fields.Many2one(
        "res.partner", "Customer Entity", readonly=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft Quotation"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("done", "Sales Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        readonly=True,
    )
    weight = fields.Float("Gross Weight", readonly=True)
    volume = fields.Float(readonly=True)
    campaign_id = fields.Many2one("utm.campaign", "Campaign")
    medium_id = fields.Many2one("utm.medium", "Medium")
    source_id = fields.Many2one("utm.source", "Source")
    order_id = fields.Many2one("sale.order", "Order", readonly=True)
    picking_id = fields.Many2one("stock.picking", "Picking", readonly=True)
    amount_cost = fields.Float("Amount cost", readonly=True)
    margin = fields.Float("Margin delivered", readonly=True)
    margin_percent = fields.Float(string="Margin delivered(%)", readonly=True)

    def _select(self):
        select_str = """
            SELECT
            min(sub.id) AS id,
            sub.product_id,
            sub.template_name,
            sub.product_uom,
            count(*) as nbr,
            sub.order_name as name,
            sub.date,
            sub.state,
            sub.partner_id,
            sub.user_from_partner_id,
            sub.user_id,
            sub.company_id,
            sub.campaign_id,
            sub.medium_id,
            sub.source_id,
            sub.categ_id,
            sub.pricelist_id,
            sub.analytic_account_id ,
            sub.team_id,
            sub.product_tmpl_id,
            sub.country_id,
            sub.industry_id,
            sub.commercial_partner_id,
            sum(signed_qty * sub.weight) as weight,
            sum(signed_qty * sub.volume) as volume,
            sub.order_id,
            sub.picking_id,
            sum(signed_qty * unsigned_product_uom_qty) AS product_uom_qty,
            sum(signed_qty * unsigned_price_subtotal) AS price_subtotal,
            CASE
                WHEN BOOL_OR(sub.amount_cost is not NULL)
                    THEN sum(-sub.amount_cost)
                ELSE sum(
                    signed_qty * ROUND(
                        sub.unsigned_purchase_price * unsigned_product_uom_qty,
                        sub.decimal_places
                    )
                )
            END AS amount_cost,
            CASE
                WHEN BOOL_OR(sub.amount_cost is not NULL)
                    THEN sum(
                        signed_qty * unsigned_price_subtotal + COALESCE(
                            sub.amount_cost, 0.0
                        )
                    )
                ELSE sum(
                    signed_qty * unsigned_price_subtotal - (
                        signed_qty * ROUND(
                            sub.unsigned_purchase_price * unsigned_product_uom_qty,
                            sub.decimal_places
                        )
                    )
                )
            END AS margin,
            0 AS margin_percent
        """
        return select_str

    def _sub_select_signed_qty(self):
        """Sub select to calculate the cases for the signed quantity"""
        return """
        WHEN source_location.usage = 'internal' AND dest_location.usage = 'customer'
            THEN 1
        WHEN source_location.usage = 'customer' AND dest_location.usage = 'internal'
            THEN -1
        WHEN source_location.usage = 'supplier' AND dest_location.usage = 'customer'
            THEN 1
        WHEN source_location.usage = 'customer' AND dest_location.usage = 'supplier'
            THEN -1
        """

    def _sub_select(self):
        sub_select_str = """
            SELECT
            sol.id AS id,
            sol.product_id as product_id,
            t.name as template_name,
            t.uom_id as product_uom,
            cur.decimal_places,
            CASE
              WHEN dest_location.usage IS NULL
                THEN 1
              {sub_select_signed_qty}
              ELSE 0
            END AS signed_qty,
            (CASE WHEN t.type IN ('product', 'consu') THEN COALESCE(sm.product_uom_qty, 0.0)
                ELSE sol.product_uom_qty END) / u.factor *
                u2.factor as unsigned_product_uom_qty,
            ROUND(COALESCE(sm.product_uom_qty * sol.price_reduce, sol.price_subtotal) /
                CASE COALESCE(s.currency_rate, 0)
                    WHEN 0 THEN 1.0 ELSE s.currency_rate END, cur.decimal_places)
                     as unsigned_price_subtotal,
            s.name as order_name,
            COALESCE(sm.date, s.effective_date, s.date_order) as date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            s.campaign_id as campaign_id,
            s.medium_id as medium_id,
            s.source_id as source_id,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            p.product_tmpl_id,
            partner.user_id as user_from_partner_id,
            partner.country_id as country_id,
            partner.industry_id as industry_id,
            partner.commercial_partner_id as commercial_partner_id,
            p.weight * sm.product_uom_qty / u.factor * u2.factor as weight,
            p.volume * sm.product_uom_qty / u.factor * u2.factor as volume,
            s.id as order_id,
            sp.id as picking_id,
            sol.purchase_price AS unsigned_purchase_price,
            ROUND(svl.value, cur.decimal_places) AS amount_cost
        """.format(
            sub_select_signed_qty=self._sub_select_signed_qty()
        )
        return sub_select_str

    def _from(self):
        from_str = """
            FROM sale_order_line sol
        LEFT JOIN stock_move sm ON (sol.id = sm.sale_line_id)
        join sale_order s on (sol.order_id=s.id)
        join res_partner partner on s.partner_id = partner.id
        left join product_product p on (sol.product_id=p.id)
        left join product_template t on (p.product_tmpl_id=t.id)
        left join uom_uom u on (u.id=sol.product_uom)
        left join uom_uom u2 on (u2.id=t.uom_id)
        left join product_pricelist pp on (s.pricelist_id = pp.id)
        LEFT JOIN
            stock_location dest_location ON sm.location_dest_id = dest_location.id
        LEFT JOIN
            stock_location source_location ON sm.location_id = source_location.id
        LEFT JOIN stock_valuation_layer svl ON svl.stock_move_id = sm.id
        LEFT JOIN stock_picking sp ON sp.id = sm.picking_id
        LEFT JOIN res_currency as cur ON cur.id = sol.currency_id
        """
        return from_str

    def _sub_where(self):
        """
        Take into account only stock moves from:

        Outgoing: Internal to Customer
        Returns: Customer to Internal + to_refund
        Dropship: Supplier to Customer
        Dropship return: Customer to Supplier
        """
        return """
        (
            source_location.usage = 'internal' AND
            dest_location.usage = 'customer'
        ) OR
        (
            source_location.usage = 'customer' AND
            dest_location.usage = 'internal' AND
            sm.to_refund
        ) OR
        (
            source_location.usage = 'supplier' AND
            dest_location.usage = 'customer' AND
            svl.quantity < 0
        ) OR
        (
            source_location.usage = 'customer' AND
            dest_location.usage = 'supplier' AND
            svl.quantity > 0
        )
        """

    def _where(self):
        """Where clause with only done mvoes or without state"""
        return """
            WHERE (sm.state = 'done' OR sm.state IS NULL) AND ({sub_where})
        """.format(
            sub_where=self._sub_where()
        )

    def _group_by(self):
        group_by_str = """
        GROUP BY sub.product_id,
            sub.template_name,
            sub.order_id,
            sub.picking_id,
            sub.product_uom,
            sub.categ_id,
            sub.order_name,
            sub.date,
            sub.partner_id,
            sub.user_from_partner_id,
            sub.user_id,
            sub.state,
            sub.company_id,
            sub.campaign_id,
            sub.medium_id,
            sub.source_id,
            sub.pricelist_id,
            sub.analytic_account_id,
            sub.team_id,
            sub.product_tmpl_id,
            sub.country_id,
            sub.industry_id,
            sub.commercial_partner_id
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s AS (
            %s
            FROM (
                %s %s %s
            ) AS sub %s)""",
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._sub_select()),
                AsIs(self._from()),
                AsIs(self._where()),
                AsIs(self._group_by()),
            ),
        )

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        res = super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
        if "margin_percent:sum" not in fields:
            return res
        full_fields = all(x in fields for x in {"price_subtotal:sum", "margin:sum"})
        for line in res:
            if full_fields and line["price_subtotal"]:
                line["margin_percent"] = (line["margin"] / line["price_subtotal"]) * 100
        return res
