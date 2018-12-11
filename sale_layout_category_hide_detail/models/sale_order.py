# Copyright 2018 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def lines_layouted_hide_details(self, report_pages):
        if self.user_has_groups('sale.group_sale_layout'):
            for page in report_pages:
                for cat_dict in page:
                    lines = cat_dict['lines']
                    category = lines and lines[0].layout_category_id
                    hide_details = category and category.hide_details
                    subtotal = sum(l.price_subtotal for l in lines)
                    cat_dict.update(
                        hide_details=hide_details,
                        lines_subtotal=subtotal,
                    )
                    if hide_details:
                        cat_dict.update(lines=list())
        return report_pages

    @api.multi
    def order_lines_layouted(self):
        report_pages = super(SaleOrder, self).order_lines_layouted()
        return self.lines_layouted_hide_details(report_pages)
