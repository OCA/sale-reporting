# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo import tests


class Common(tests.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "Test customer",
            }
        )

        cls.sale_orders = cls.env["sale.order"].create(
            [
                {
                    "partner_id": cls.customer.id,
                    "date_order": datetime.datetime(2020, 1, day_number),
                }
                for day_number in range(1, 10)
            ]
        )
