# Copyright (C) 2022 - TODAY, Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    last_date_delivered = fields.Datetime(
        string="Date Delivered", compute="_compute_last_date_delivered", store=True
    )
    last_bill_date = fields.Datetime(
        string="Bill Date", compute="_compute_last_bill_date", store=True
    )
    uninvoiced_goods_delivered_qty = fields.Float(
        string="UIGD Qty",
        compute="_compute_uigd_qty",
        store=True,
        help="Un-Invoiced Goods Delivered Qty",
    )
    bo_qty = fields.Float(string="Backorder Qty", compute="_compute_bo_qty", store=True)
    uninvoiced_goods_delivered_value = fields.Monetary(
        string="UIGD Value",
        compute="_compute_uigd_value",
        store=True,
        help="Un-Invoiced Goods Delivered Value",
    )
    bo_value = fields.Monetary(
        string="Backorder Value", compute="_compute_bo_value", store=True
    )
    product_type = fields.Selection(
        string="Product Type", related="product_id.product_tmpl_id.type"
    )

    @api.depends("qty_delivered", "product_uom_qty")
    def _compute_bo_qty(self):
        for line in self:
            line.bo_qty = line.product_uom_qty - line.qty_delivered

    @api.depends("qty_delivered", "qty_invoiced")
    def _compute_uigd_qty(self):
        for line in self:
            line.uninvoiced_goods_delivered_qty = line.qty_delivered - line.qty_invoiced

    @api.depends("uninvoiced_goods_delivered_qty", "price_unit")
    def _compute_uigd_value(self):
        for line in self:
            line.uninvoiced_goods_delivered_value = (
                line.uninvoiced_goods_delivered_qty * line.price_unit
            )

    @api.depends("bo_qty", "price_unit")
    def _compute_bo_value(self):
        for line in self:
            line.bo_value = line.bo_qty * line.price_unit

    @api.depends("qty_delivered", "qty_invoiced")
    def _compute_last_date_delivered(self):
        for line in self:
            moves = line.move_ids.sorted("id", reverse=True).filtered(
                lambda move: move.state != "done"
                or move.location_dest_id.usage != "customer"
                or not move.to_refund
            )
            line.last_date_delivered = moves and moves[0].date or False

    @api.depends("qty_delivered", "qty_invoiced")
    def _compute_last_bill_date(self):
        for line in self:
            invoices = line.invoice_lines.sorted("id", reverse=True).filtered(
                lambda inv: inv.move_id.state != "cancel"
                or inv.move_id.move_type == "out_invoice"
                or inv.move_id.date
            )
            line.last_bill_date = invoices and invoices[0].move_id.date or False
