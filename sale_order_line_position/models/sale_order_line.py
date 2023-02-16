# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    position = fields.Integer(readonly=True, index=True, default=False)
    position_formatted = fields.Char(compute="_compute_position_formatted")

    @api.depends("position")
    def _compute_position_formatted(self):
        for record in self:
            record.position_formatted = record._format_position(record.position)

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = self._add_next_position_on_new_line(vals_list)
        return super().create(vals_list)

    def unlink(self):
        sales = self.mapped("order_id")
        res = super().unlink()
        for sale in sales:
            sale.recompute_positions()
        return res

    def _add_next_position_on_new_line(self, vals_list):
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

    @api.model
    def _format_position(self, position):
        if not position:
            return ""
        return str(position).zfill(3)
