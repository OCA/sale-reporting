# Copyright 2024 Tecnativa - Carolina Fernandez
from odoo.tests.common import TransactionCase

from ..hooks import uninstall_hook


class TestUninstallHook(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_sale_salesman = cls.env.ref("sales_team.group_sale_salesman")

    def test_uninstall_hook(self):
        menu_sale_report = self.env.ref(
            "sale.menu_sale_report", raise_if_not_found=False
        )
        self.assertIn(self.group_sale_salesman, menu_sale_report.groups_id)
        uninstall_hook(self.cr, self.registry)
        self.assertNotIn(self.group_sale_salesman, menu_sale_report.groups_id)
