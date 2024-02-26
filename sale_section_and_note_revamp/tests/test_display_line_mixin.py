# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged

from .common import TestDisplayLineMixinCommon


@tagged("post_install", "-at_install")
class TestDisplayLineMixin(TestDisplayLineMixinCommon):
    def test_01_is_section(self):
        self.assertTrue(self.sol_section_1.is_section())
        self.assertFalse(self.sol_product_order.is_section())

    def test_02_is_note(self):
        self.assertTrue(self.sol_note_1.is_note())
        self.assertFalse(self.sol_serv_deliver.is_note())

    def test_03_get_section(self):
        section = self.sol_product_order.get_section()
        self.assertEqual(section, self.sol_section_1)

        # Taking the third line to ensure we execute twice the while loop
        # We are expecting the first SOL to be a section
        third_line = self.sale_order.order_line[2]
        self.assertEqual(third_line.get_section(), self.sol_section_1)

    def test_04_get_note(self):
        note = self.sol_serv_deliver.get_note()
        self.assertEqual(note, self.sol_note_1)

    def test_05_get_section_subtotal(self):
        section_subtotal = self.sol_section_1.get_section_subtotal(
            fields=["price_total"]
        )
        expected_subtotal = sum(
            [
                self.sol_product_order.price_total,
                self.sol_serv_deliver.price_total,
                self.sol_serv_order.price_total,
            ]
        )
        # Check if the calculated subtotal matches the expected subtotal
        self.assertEqual(section_subtotal["price_total"], expected_subtotal)

    def test_06_prepare_section_or_note_values(self):
        with self.assertRaises(NotImplementedError):
            self.sol_product_order.prepare_section_or_note_values(self.sol_section_1)

    def test_07_inject_sections_and_notes(self):
        with self.assertRaises(NotImplementedError):
            self.sol_product_order.inject_sections_and_notes()

    def _assert_previous_next_line(self, order):
        sorted_lines = order.order_line.sorted()
        for i, sol in enumerate(sorted_lines):
            if i == 0:
                self.assertFalse(sol.previous_line_id)
                self.assertEqual(sol.next_line_id, sorted_lines[i + 1])
            elif i == len(order.order_line) - 1:
                self.assertEqual(sol.previous_line_id, sorted_lines[i - 1])
                self.assertFalse(sol.next_line_id)
            else:
                self.assertEqual(sol.previous_line_id, sorted_lines[i - 1])
                self.assertEqual(sol.next_line_id, sorted_lines[i + 1])

    def test_08_previous_next_line_calculation(self):
        self._assert_previous_next_line(self.sale_order)
        # Switch first and second lines
        first_line = self.sale_order.order_line[0]
        second_line = self.sale_order.order_line[1]
        first_line_sequence = first_line.sequence
        first_line.sequence = second_line.sequence
        second_line.sequence = first_line_sequence
        self._assert_previous_next_line(self.sale_order)
        # Switch last and penultimate lines
        last_line = self.sale_order.order_line[-1]
        penultimate_line = self.sale_order.order_line[-2]
        last_line_sequence = last_line.sequence
        last_line_sequence = penultimate_line.sequence
        penultimate_line.sequence = last_line_sequence
        self._assert_previous_next_line(self.sale_order)

    def test_09_insert_new_line_after(self):
        first_line = self.sale_order.order_line[0]
        second_line = self.sale_order.order_line[1]
        third_line = self.sale_order.order_line[2]
        penultimate_line = self.sale_order.order_line[-2]
        last_line = self.sale_order.order_line[-1]
        self.assertEqual(first_line.next_line_id, second_line)

        # we move the second line after the penultimate line
        penultimate_line.add_line(second_line)
        self.assertEqual(penultimate_line.next_line_id, second_line)
        self.assertEqual(last_line.previous_line_id, second_line)

        self.assertEqual(first_line.next_line_id, third_line)
        self.assertEqual(third_line.previous_line_id, first_line)

    def test_10_insert_new_line_before(self):
        first_line = self.sale_order.order_line[0]
        second_line = self.sale_order.order_line[1]
        penultimate_line = self.sale_order.order_line[-2]
        last_line = self.sale_order.order_line[-1]
        self.assertEqual(first_line.next_line_id, second_line)

        # we move the second line before the last line
        last_line.add_line(second_line, before=True)
        self.assertEqual(last_line.previous_line_id, second_line)
        self.assertEqual(penultimate_line.next_line_id, second_line)
        self.assertEqual(second_line.next_line_id, last_line)
        self.assertEqual(second_line.previous_line_id, penultimate_line)

    def test_12_has_section(self):
        self.assertTrue(self.sol_serv_deliver.has_section())
