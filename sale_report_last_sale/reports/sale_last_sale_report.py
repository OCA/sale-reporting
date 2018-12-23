# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools


class SaleLastSaleReport(models.Model):
    _name = 'sale.last.sale.report'
    _description = 'Last Sale Statistics'
    _auto = False
    _order = 'id'

    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    product_category_id = fields.Many2one(
        'product.category',
        'Product Category',
        readonly=True)

    date_order = fields.Date(
        'Order Date',
        group_operator='max',
        readonly=True)

    days_since = fields.Integer(
        'Days Since',
        group_operator='min',
        readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'sale_last_sale_report')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sale_last_sale_report AS (
            SELECT
            ROW_NUMBER() OVER() AS id,
            product_product.id AS product_id,
            sale_order.company_id AS company_id,
            res_partner.commercial_partner_id AS partner_id,
            product_template.categ_id as product_category_id,
            MAX(sale_order.date_order)::date AS date_order,

            -- Computed Fields
            MIN(
                DATE_PART(
                    'day',
                    NOW()::timestamp - sale_order.date_order::timestamp
                )
            ) AS days_since

            FROM sale_order_line
            INNER JOIN sale_order
            ON (sale_order_line.order_id = sale_order.id)
            INNER JOIN res_partner
            ON (sale_order.partner_id = res_partner.id)
            INNER JOIN product_product
            ON (sale_order_line.product_id = product_product.id)
            INNER JOIN product_template
            ON (product_product.product_tmpl_id = product_template.id)

            -- Only confirmed sale orders
            WHERE sale_order.state IN ('sale', 'done')

            GROUP BY
                product_product.id,                 --product_id
                sale_order.company_id,              --company_id
                res_partner.commercial_partner_id,  --partner_id
                product_template.categ_id           --product_category_id
        )""")
