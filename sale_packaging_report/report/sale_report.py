# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)


from odoo import fields, models


class Name(models.AbstractModel):
    _inherit = "sale.report"

    product_packaging_id = fields.Many2one(
        "uom.uom",
        string="Packaging",
        readonly=True,
    )
    product_packaging_qty = fields.Float(string="Packaging Qty", readonly=True)
    product_packaging_qty_delivered = fields.Float(
        string="Packaging Delivered Qty",
        readonly=True,
    )

    def _select_additional_fields(self):
        result = super()._select_additional_fields()
        return dict(
            result,
            product_packaging_id="l.product_uom_id",
            product_packaging_qty="SUM(l.product_uom_qty)",
            product_packaging_qty_delivered="COALESCE(SUM(l.qty_delivered), 0)",
        )

    def _group_by_sale(self):
        result = super()._group_by_sale()
        return f"{result}, l.product_uom_id"
