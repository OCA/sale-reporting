# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestSaleOrderWeekDay(Common):
    def test_week_day(self):
        """The Day of Week is computed correctly."""
        for sale_order in self.sale_orders:
            self.assertEqual(
                sale_order.create_date_week_day, str(sale_order.create_date.weekday())
            )
            self.assertEqual(
                sale_order.date_order_week_day, str(sale_order.date_order.weekday())
            )
