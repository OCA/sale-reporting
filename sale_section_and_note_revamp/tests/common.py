# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo.addons.sale.tests.common import TestSaleCommon


class TestDisplayLineMixinCommon(TestSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        SaleOrder = cls.env["sale.order"]
        SaleOrderLine = cls.env["sale.order.line"]

        # create a generic Sale Order with all classical products and empty pricelist
        cls.sale_order = SaleOrder.create(
            {
                "partner_id": cls.partner_a.id,
                "partner_invoice_id": cls.partner_a.id,
                "partner_shipping_id": cls.partner_a.id,
                "pricelist_id": cls.company_data["default_pricelist"].id,
            }
        )

        cls.sol_section_1 = SaleOrderLine.create(
            {
                "sequence": 1,
                "order_id": cls.sale_order.id,
                "display_type": "line_section",
                "name": "Sample Section",
            }
        )
        cls.sol_product_order = SaleOrderLine.create(
            {
                "sequence": 2,
                "name": cls.company_data["product_order_no"].name,
                "product_id": cls.company_data["product_order_no"].id,
                "product_uom_qty": 2,
                "product_uom": cls.company_data["product_order_no"].uom_id.id,
                "price_unit": cls.company_data["product_order_no"].list_price,
                "order_id": cls.sale_order.id,
                "tax_id": False,
            }
        )
        cls.sol_serv_deliver = SaleOrderLine.create(
            {
                "sequence": 3,
                "name": cls.company_data["product_service_delivery"].name,
                "product_id": cls.company_data["product_service_delivery"].id,
                "product_uom_qty": 2,
                "product_uom": cls.company_data["product_service_delivery"].uom_id.id,
                "price_unit": cls.company_data["product_service_delivery"].list_price,
                "order_id": cls.sale_order.id,
                "tax_id": False,
            }
        )
        cls.sol_note_1 = SaleOrderLine.create(
            {
                "sequence": 4,
                "order_id": cls.sale_order.id,
                "display_type": "line_note",
                "name": "Sample Note 1",
            }
        )
        cls.sol_serv_order = SaleOrderLine.create(
            {
                "sequence": 5,
                "name": cls.company_data["product_service_order"].name,
                "product_id": cls.company_data["product_service_order"].id,
                "product_uom_qty": 2,
                "product_uom": cls.company_data["product_service_order"].uom_id.id,
                "price_unit": cls.company_data["product_service_order"].list_price,
                "order_id": cls.sale_order.id,
                "tax_id": False,
            }
        )
        cls.sol_section_2 = SaleOrderLine.create(
            {
                "sequence": 6,
                "order_id": cls.sale_order.id,
                "display_type": "line_section",
                "name": "Sample Section 2",
            }
        )
        cls.sol_product_deliver = SaleOrderLine.create(
            {
                "sequence": 7,
                "name": cls.company_data["product_delivery_no"].name,
                "product_id": cls.company_data["product_delivery_no"].id,
                "product_uom_qty": 2,
                "product_uom": cls.company_data["product_delivery_no"].uom_id.id,
                "price_unit": cls.company_data["product_delivery_no"].list_price,
                "order_id": cls.sale_order.id,
                "tax_id": False,
            }
        )
        cls.sol_note_2 = SaleOrderLine.create(
            {
                "sequence": 8,
                "order_id": cls.sale_order.id,
                "display_type": "line_note",
                "name": "Sample Note 2",
            }
        )
