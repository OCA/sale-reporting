# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests import SavepointCase


class TestSaleInvoiceDate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.product = cls.env.ref("product.product_product_10")
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.display_name,
                            "product_id": cls.product.id,
                            "product_uom_qty": 10.0,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": cls.product.list_price,
                        },
                    )
                ],
            }
        )
        cls.order.action_confirm()

    def test_sale_report(self):
        # Case 1: No delivery date
        res = self.env["sale.report"].read_group(
            [("order_id", "in", self.order.ids)],
            fields=["delivery_date"],
            groupby=["delivery_date"],
            lazy=False,
        )
        self.assertEqual(res[0]["delivery_date"], False, "No delivery yet")
        # Case 2: Partial delivery date
        with freeze_time("2022-05-15"):
            picking = self.order.picking_ids
            picking.move_line_ids.qty_done = 5.0
            picking._action_done()
        self.env["base"].flush()
        res = self.env["sale.report"].read_group(
            [("order_id", "in", self.order.ids)],
            fields=["delivery_date"],
            groupby=["delivery_date"],
            lazy=False,
        )
        self.assertEqual(res[0]["delivery_date"], "May 2022")
        # Case 3: Fullfiled backorder
        with freeze_time("2022-06-15"):
            backorder = self.order.picking_ids - picking
            backorder.move_line_ids.qty_done = 5.0
            backorder._action_done()
        self.env["base"].flush()
        res = self.env["sale.report"].read_group(
            [("order_id", "in", self.order.ids)],
            fields=["delivery_date"],
            groupby=["delivery_date"],
            lazy=False,
        )
        self.assertEqual(res[0]["delivery_date"], "June 2022", "Last delivery date")
