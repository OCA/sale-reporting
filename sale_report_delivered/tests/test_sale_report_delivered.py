# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import Form, common, new_test_user
from odoo.tests.common import users


class TestSaleReportDeliveredBase(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.admin = cls.env.ref("base.user_admin")
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": cls.company.currency_id.id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test partner", "property_product_pricelist": cls.pricelist.id}
        )
        cls.user = new_test_user(
            cls.env,
            login="test_user-sale_report_delivered",
            name="test_user-one",
            groups="sales_team.group_sale_manager",
        )
        group_sale_manager = cls.env.ref("sales_team.group_sale_manager")
        group_sale_manager.write({"users": [(4, cls.admin.id)]})

    @classmethod
    def _create_product(
        cls, name, ptype, list_price=10.0, standard_price=0.0, stock_qty=0
    ):
        """Create a product and optionally add stock for storable products."""
        ptype = ptype or "product"
        product = cls.env["product.product"].create(
            {
                "name": name,
                "type": ptype,
                "list_price": list_price,
                "standard_price": standard_price,
            }
        )
        if ptype == "product" and stock_qty > 0:
            cls._create_stock_quant(product, stock_qty)
        return product

    @classmethod
    def _create_stock_quant(cls, product, qty=1):
        """Add stock for a storable product in the default Stock location."""
        res = product.action_update_quantity_on_hand()
        quant_form = Form(
            cls.env["stock.quant"].with_context(**res["context"]),
            view="stock.view_stock_quant_tree_inventory_editable",
        )
        quant_form.inventory_quantity = qty
        quant_form.location_id = cls.env.ref("stock.stock_location_stock")
        return quant_form.save()

    @classmethod
    def _create_order(cls, product, qty=1, price=None, confirm=False):
        """Create a draft sale order (does NOT confirm)."""
        order_form = Form(cls.env["sale.order"])
        order_form.partner_id = cls.partner
        with order_form.order_line.new() as line_form:
            line_form.product_id = product
            line_form.product_uom_qty = qty
            if price is not None:
                line_form.price_unit = price
        order = order_form.save()
        if confirm:
            order.action_confirm()
        return order

    @classmethod
    def _validate_pickings(cls, pickings, qty_done):
        """Confirm and validate a pickings with the given done qty."""
        pickings.action_confirm()
        pickings.move_ids.write({"quantity_done": qty_done})
        res = pickings.button_validate()
        if isinstance(res, dict) and res.get("res_model") == "stock.immediate.transfer":
            wizard_form = Form(cls.env[res["res_model"]].with_context(**res["context"]))
            wizard = wizard_form.save()
            wizard.process()

    @classmethod
    def _create_return(cls, picking, qty, to_refund=True):
        """Create and validate a return picking from an existing delivery.

        Uses the stock.return.picking wizard for proper location handling,
        then fixes sale_line_id and to_refund via raw SQL after validation,
        and recreates the report view.
        """
        return_wizard_form = Form(
            cls.env["stock.return.picking"].with_context(
                active_id=picking.id,
                active_model="stock.picking",
            )
        )
        with return_wizard_form.product_return_moves.edit(0) as line:
            line.quantity = qty
        return_wizard = return_wizard_form.save()
        return_wizard.product_return_moves.write({"to_refund": to_refund})
        return_picking_id, _ = return_wizard._create_returns()
        return_picking = cls.env["stock.picking"].browse(return_picking_id)
        return_picking.move_ids.write({"quantity_done": qty})
        res = return_picking.button_validate()
        if isinstance(res, dict) and res.get("res_model") == "stock.immediate.transfer":
            wizard_form = Form(cls.env[res["res_model"]].with_context(**res["context"]))
            wizard = wizard_form.save()
            wizard.process()
        return return_picking

    @classmethod
    def _create_dropship_picking(cls, order, qty):
        """Create and validate a dropship picking (supplier→customer).

        The SQL view requires supplier→customer location usage *and*
        svl.quantity < 0 for the dropship delivery row to be included.
        """
        supplier_loc = cls.env.ref("stock.stock_location_suppliers")
        customer_loc = cls.env.ref("stock.stock_location_customers")
        # Cancel the default outgoing picking and delete it to avoid conflicts
        order.picking_ids.filtered(
            lambda p: p.state not in ("done", "cancel")
        ).action_cancel()
        order.picking_ids.unlink()
        # Create a new picking + move + SVL from scratch via raw SQL for full
        # control of all values needed by the view
        cls.env.cr.execute(
            "INSERT INTO stock_picking "
            "(location_id, location_dest_id, state, picking_type_id, "
            " move_type, company_id, create_date, write_date) "
            "VALUES (%s, %s, 'done', %s, 'direct', %s, NOW(), NOW()) "
            "RETURNING id",
            (
                supplier_loc.id,
                customer_loc.id,
                cls.env.ref("stock.picking_type_out").id,
                cls.company.id,
            ),
        )
        picking_id = cls.env.cr.fetchone()[0]
        # Create a stock move linked to the sale line
        cls.env.cr.execute(
            "INSERT INTO stock_move "
            "(name, product_id, product_uom_qty, product_uom, "
            " quantity_done, location_id, location_dest_id, "
            " picking_id, sale_line_id, state, company_id, "
            " procure_method, date, "
            " create_date, write_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'done', %s, "
            "'make_to_stock', NOW(), "
            "NOW(), NOW()) RETURNING id",
            (
                "Dropship delivery",
                order.order_line.product_id.id,
                qty,
                order.order_line.product_uom.id,
                qty,
                supplier_loc.id,
                customer_loc.id,
                picking_id,
                order.order_line.id,
                cls.company.id,
            ),
        )
        move_id = cls.env.cr.fetchone()[0]
        # Insert SVL with negative quantity — required by the view
        # (svl.quantity < 0 in the _sub_where filter)
        cls.env.cr.execute(
            "INSERT INTO stock_valuation_layer "
            "(company_id, product_id, quantity, "
            " unit_cost, value, remaining_qty, stock_move_id, description, "
            " create_date, write_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())",
            (
                cls.company.id,
                order.order_line.product_id.id,
                -qty,
                0.0,
                0.0,
                -qty,
                move_id,
                "Dropship test delivery",
            ),
        )
        cls.env.invalidate_all()
        cls.env["sale.report.delivered"].init()
        cls.env.invalidate_all()
        return cls.env["stock.picking"].browse(picking_id)

    @classmethod
    def _create_dropship_return(cls, order, delivery_picking, qty):
        """Create and validate a dropship return picking (customer→supplier).

        The SQL view requires customer→supplier location usage *and*
        svl.quantity > 0 for the return row to be included.  It does NOT
        require to_refund.

        Uses raw SQL to avoid ORM side effects.
        """
        supplier_loc = cls.env.ref("stock.stock_location_suppliers")
        customer_loc = cls.env.ref("stock.stock_location_customers")
        cls.env.cr.execute(
            "INSERT INTO stock_picking "
            "(location_id, location_dest_id, state, picking_type_id, "
            " move_type, company_id, create_date, write_date) "
            "VALUES (%s, %s, 'done', %s, 'direct', %s, NOW(), NOW()) "
            "RETURNING id",
            (
                customer_loc.id,
                supplier_loc.id,
                cls.env.ref("stock.picking_type_in").id,
                cls.company.id,
            ),
        )
        return_picking_id = cls.env.cr.fetchone()[0]
        cls.env.cr.execute(
            "INSERT INTO stock_move "
            "(name, product_id, product_uom_qty, product_uom, "
            " quantity_done, location_id, location_dest_id, "
            " picking_id, sale_line_id, state, company_id, "
            " procure_method, date, "
            " create_date, write_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'done', %s, "
            "'make_to_stock', NOW(), "
            "NOW(), NOW()) RETURNING id",
            (
                "Dropship return",
                order.order_line.product_id.id,
                qty,
                order.order_line.product_uom.id,
                qty,
                customer_loc.id,
                supplier_loc.id,
                return_picking_id,
                order.order_line.id,
                cls.company.id,
            ),
        )
        return_move_id = cls.env.cr.fetchone()[0]
        cls.env.cr.execute(
            "INSERT INTO stock_valuation_layer "
            "(company_id, product_id, quantity, "
            " unit_cost, value, remaining_qty, stock_move_id, description, "
            " create_date, write_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())",
            (
                cls.company.id,
                order.order_line.product_id.id,
                qty,
                0.0,
                0.0,
                qty,
                return_move_id,
                "Dropship test return",
            ),
        )
        cls.env.invalidate_all()
        cls.env["sale.report.delivered"].init()
        cls.env.invalidate_all()
        return cls.env["stock.picking"].browse(return_picking_id)


class TestSaleReportDelivered(TestSaleReportDeliveredBase):
    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_misc(self):
        product = self._create_product(
            "Test product", "product", list_price=10, stock_qty=1
        )
        service = self._create_product("Test service", "service", list_price=10)
        order_1 = self._create_order(product, confirm=True)
        order_2 = self._create_order(service, confirm=True)
        orders = order_1 + order_2
        self._validate_pickings(orders.picking_ids, 1.0)
        self.env.invalidate_all()
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", orders.ids)]
        )
        self.assertIn(order_1, items.mapped("order_id"))
        self.assertNotIn(order_2, items.mapped("order_id"))
        self.assertIn(order_1.picking_ids, items.mapped("picking_id"))
        self.assertIn(product, items.mapped("product_id"))
        self.assertNotIn(service, items.mapped("product_id"))

    def _test_sale_report_delivered_read_group(self):
        product = self._create_product(
            "Test product", "product", list_price=10, standard_price=3, stock_qty=1
        )
        service = self._create_product("Test service", "service", list_price=10)
        order_1 = self._create_order(product, confirm=True)
        order_2 = self._create_order(service, confirm=True)
        orders = order_1 + order_2
        self._validate_pickings(orders.picking_ids, 1.0)
        self.env.invalidate_all()
        res = self.env["sale.report.delivered"].read_group(
            domain=[("order_id", "in", orders.ids)],
            fields=[
                "order_id",
                "margin_percent:sum",
                "price_subtotal:sum",
                "margin:sum",
            ],
            groupby=["order_id"],
        )
        self.assertAlmostEqual(res[0]["margin_percent"], 70.00)

    @users("admin")
    def test_sale_report_delivered_read_group_admin(self):
        self._test_sale_report_delivered_read_group()

    @users("test_user-sale_report_delivered")
    def test_sale_report_delivered_read_group(self):
        self._test_sale_report_delivered_read_group()

    def test_sale_report_delivered_and_svl_adjustment(self):
        product = self._create_product(
            "Test product", "product", list_price=10, stock_qty=1
        )
        order_1 = self._create_order(product, confirm=True)
        self._validate_pickings(order_1.picking_ids, 1.0)
        self.env.invalidate_all()
        move = order_1.order_line.move_ids
        item = self.env["sale.report.delivered"].search(
            [("product_id", "=", product.id), ("order_id", "=", order_1.id)]
        )
        self.assertAlmostEqual(item.product_uom_qty, 1)
        self.assertEqual(len(move.stock_valuation_layer_ids), 1)
        # The user modifies the done ml and an adjustment layer is made
        move.move_line_ids.qty_done = 0.7
        self.assertEqual(len(move.stock_valuation_layer_ids), 2)
        self.env.invalidate_all()
        item = self.env["sale.report.delivered"].search(
            [("product_id", "=", product.id), ("order_id", "=", order_1.id)]
        )
        self.assertAlmostEqual(item.product_uom_qty, 0.7)

    @users("admin")
    def test_sale_report_delivered_return_and_svl_adjustment(self):
        """Delivery (qty=2) + return (qty=1, to_refund=True)."""
        product = self._create_product(
            "Test return product", "product", list_price=10, stock_qty=2
        )
        order = self._create_order(product, qty=2, confirm=True)
        picking = order.picking_ids
        self._validate_pickings(picking, 2)
        return_picking = self._create_return(picking, 1, to_refund=True)
        self.env.invalidate_all()
        items = self.env["sale.report.delivered"].read_group(
            domain=[("product_id", "=", product.id), ("order_id", "=", order.id)],
            fields=["picking_id", "product_uom_qty:sum", "price_subtotal:sum"],
            groupby=["picking_id"],
        )
        self.assertEqual(len(items), 2)
        delivery_item = [r for r in items if r["picking_id"][0] == picking.id][0]
        return_item = [r for r in items if r["picking_id"][0] == return_picking.id][0]
        self.assertAlmostEqual(abs(delivery_item["product_uom_qty"]), 2)
        self.assertAlmostEqual(abs(return_item["product_uom_qty"]), 1)
        # The user modifies the done ml and an adjustment layer is made
        return_move = return_picking.move_ids
        return_move.move_line_ids.qty_done = 0.7
        self.assertEqual(len(return_move.stock_valuation_layer_ids), 2)
        self.env.invalidate_all()
        items = self.env["sale.report.delivered"].read_group(
            domain=[("product_id", "=", product.id), ("order_id", "=", order.id)],
            fields=["picking_id", "product_uom_qty:sum", "price_subtotal:sum"],
            groupby=["picking_id"],
        )
        self.assertEqual(len(items), 2)
        delivery_item = [r for r in items if r["picking_id"][0] == picking.id][0]
        return_item = [r for r in items if r["picking_id"][0] == return_picking.id][0]
        self.assertAlmostEqual(abs(delivery_item["product_uom_qty"]), 2)
        self.assertAlmostEqual(abs(return_item["product_uom_qty"]), 0.7)

    # ------------------------------------------------------------------------
    # Deliberately NOT testing Dropship modification: known bug in ROADMAP.rst
    # ------------------------------------------------------------------------

    @users("admin")
    def test_sale_report_delivered_dropship(self):
        """Dropship delivery: supplier -> customer, qty=2, price=10."""
        product = self._create_product(
            "Test dropship product", "product", list_price=10
        )
        order = self._create_order(product, qty=2, price=10, confirm=True)
        picking = self._create_dropship_picking(order, 2)
        item = self.env["sale.report.delivered"].search(
            [("product_id", "=", product.id), ("order_id", "=", order.id)]
        )
        self.assertEqual(len(item), 1)
        self.assertAlmostEqual(item.product_uom_qty, 2)
        self.assertAlmostEqual(item.price_subtotal, 20)
        self.assertEqual(item.picking_id, picking)

    @users("admin")
    def test_sale_report_delivered_dropship_return(self):
        """Dropship delivery (qty=2) + return (qty=1) customer->supplier."""
        product = self._create_product(
            "Test dropship ret product", "product", list_price=10
        )
        order = self._create_order(product, qty=2, confirm=True)
        delivery_picking = self._create_dropship_picking(order, 2)
        return_picking = self._create_dropship_return(order, delivery_picking, 1)
        items = self.env["sale.report.delivered"].read_group(
            domain=[("product_id", "=", product.id), ("order_id", "=", order.id)],
            fields=["picking_id", "product_uom_qty:sum", "price_subtotal:sum"],
            groupby=["picking_id"],
        )
        self.assertEqual(len(items), 2)
        delivery_item = [r for r in items if r["picking_id"][0] == delivery_picking.id][
            0
        ]
        return_item = [r for r in items if r["picking_id"][0] == return_picking.id][0]
        self.assertAlmostEqual(abs(delivery_item["product_uom_qty"]), 2)
        self.assertAlmostEqual(abs(return_item["product_uom_qty"]), 1)
