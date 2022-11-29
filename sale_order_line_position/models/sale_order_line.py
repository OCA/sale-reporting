# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = ["sale.order.line", "order.line.position.mixin"]

    def _add_next_position_on_new_line(self, vals_list):
        """Compute the nex position for the line"""
        sale_ids = [
            line["order_id"]
            for line in vals_list
            if not line.get("display_type") and line.get("order_id")
        ]
        if sale_ids:
            ids = tuple(set(sale_ids))
            self.flush()
            query = """
            SELECT order_id, max(position) FROM sale_order_line
            WHERE order_id in %s GROUP BY order_id;
            """
            self.env.cr.execute(query, (ids,))
            default_pos = {key: 1 for key in ids}
            existing_pos = {
                order_id: pos + 1 for order_id, pos in self.env.cr.fetchall()
            }
            sale_pos = {**default_pos, **existing_pos}
            for line in vals_list:
                if not line.get("display_type"):
                    line["position"] = sale_pos[line["order_id"]]
                    sale_pos[line["order_id"]] += 1
        return vals_list
