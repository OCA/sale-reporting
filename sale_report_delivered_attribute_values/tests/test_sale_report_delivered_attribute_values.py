# Copyright 2025 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from odoo.fields import Command
from odoo.tests import Form, common


class TestSaleReportDeliveredAttributeValues(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        # Create product
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Adidas Hoodie",
                "type": "product",
                "sale_ok": True,
            }
        )
        # Create attributes and attribute values
        cls.trademark_attribute = cls.env["product.attribute"].create(
            {
                "name": "Trademark",
                "display_type": "pills",
                "create_variant": "no_variant",
                "value_ids": [
                    Command.create({"name": "Adidas"}),
                ],
            }
        )
        cls.size_attribute = cls.env["product.attribute"].create(
            {
                "name": "Size",
                "display_type": "pills",
                "create_variant": "always",
                "value_ids": [
                    Command.create({"name": "M"}),
                    Command.create({"name": "L"}),
                ],
            }
        )
        # Assign attributes to product template
        cls.env["product.template.attribute.line"].create(
            [
                {
                    "product_tmpl_id": cls.product_template.id,
                    "attribute_id": cls.trademark_attribute.id,
                    "value_ids": [Command.set(cls.trademark_attribute.value_ids.ids)],
                },
                {
                    "product_tmpl_id": cls.product_template.id,
                    "attribute_id": cls.size_attribute.id,
                    "value_ids": [Command.set(cls.size_attribute.value_ids.ids)],
                },
            ]
        )
        # Create quants
        for product in cls.product_template.product_variant_ids:
            res = product.action_update_quantity_on_hand()
            quant_form = Form(
                cls.env["stock.quant"].with_context(**res["context"]),
                view="stock.view_stock_quant_tree_inventory_editable",
            )
            quant_form.inventory_quantity = 1
            quant_form.location_id = cls.env.ref("stock.stock_location_stock")
            return quant_form.save()

    def _create_and_complete_order(self, product):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = product
            line_form.product_uom_qty = 1
        order = order_form.save()
        order.action_confirm()
        order.picking_ids.action_confirm()
        order.picking_ids.move_ids.write({"quantity_done": 1.0})
        order.picking_ids.button_validate()
        self.env.flush_all()
        return order

    def test_report_delivered_attribute_values(self):
        sale1 = self._create_and_complete_order(
            self.product_template.product_variant_ids[0]
        )
        sale2 = self._create_and_complete_order(
            self.product_template.product_variant_ids[1]
        )
        # Check order 1
        report_lines = self.env["sale.report.delivered"].search(
            [
                ("order_id", "=", sale1.id),
            ]
        )
        self.assertEqual(len(report_lines), 1)
        self.assertEqual(len(report_lines.all_product_attribute_value_ids), 2)
        self.assertEqual(
            report_lines.all_product_attribute_value_ids,
            sale1.order_line.all_product_attribute_value_ids,
        )
        self.assertEqual(report_lines.sale_line_id, sale1.order_line)
        # Check order 2
        report_lines = self.env["sale.report.delivered"].search(
            [
                ("order_id", "=", sale2.id),
            ]
        )
        self.assertEqual(len(report_lines), 1)
        self.assertEqual(len(report_lines.all_product_attribute_value_ids), 2)
        self.assertEqual(
            report_lines.all_product_attribute_value_ids,
            sale2.order_line.all_product_attribute_value_ids,
        )
        self.assertEqual(report_lines.sale_line_id, sale2.order_line)
        # Check attribute TRADEMARK value
        report_lines = self.env["sale.report.delivered"].search(
            [
                (
                    "all_product_attribute_value_ids",
                    "in",
                    self.trademark_attribute.value_ids.ids,
                ),
            ]
        )
        self.assertEqual(len(report_lines), 2)
        # Check attribute SIZE value 1
        report_lines = self.env["sale.report.delivered"].search(
            [
                (
                    "all_product_attribute_value_ids",
                    "in",
                    self.size_attribute.value_ids[0].ids,
                ),
            ]
        )
        self.assertEqual(len(report_lines), 1)
        # Check attribute SIZE value 2
        report_lines = self.env["sale.report.delivered"].search(
            [
                (
                    "all_product_attribute_value_ids",
                    "in",
                    self.size_attribute.value_ids[1].ids,
                ),
            ]
        )
        self.assertEqual(len(report_lines), 1)
