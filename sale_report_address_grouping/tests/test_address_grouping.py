# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAdressGrouping(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.partner_obj = cls.env["res.partner"]

        cls.company = cls.partner_obj.create({"name": "A great Company"})

        cls.contact_1 = cls.partner_obj.create(
            {
                "name": "Contact 1",
                "parent_id": cls.company.id,
                "type": "delivery",
            }
        )

        cls.contact_2 = cls.partner_obj.create(
            {
                "name": "Contact 2",
                "parent_id": cls.company.id,
                "type": "invoice",
            }
        )

        cls.sale = cls.env["sale.order"].create(
            {
                "partner_id": cls.company.id,
                "partner_invoice_id": cls.contact_2.id,
                "partner_shipping_id": cls.contact_1.id,
            }
        )

    def test_no_grouping(self):
        """
        Invoicing and Shipping addresses are different and different
        from partner_id
        """
        addresses = self.sale.get_partner_addresses()
        i = 0
        for key, value in addresses.items():
            if i == 0:
                self.assertEqual(key, self.contact_2)
                self.assertEqual(value, "Invoicing Address:")
            if i == 1:
                self.assertEqual(key, self.contact_1)
                self.assertEqual(value, "Shipping Address:")
            i += 1

    def test_grouping(self):
        """
        Shipping and Invoicing addresses are the same
        """
        self.sale.partner_shipping_id = self.contact_2
        addresses = self.sale.get_partner_addresses()
        for key, value in addresses.items():
            self.assertEqual(key, self.contact_2)
            self.assertEqual(value, "Invoicing/Shipping Address:")

    def test_unique_address(self):
        """
        All addresses are the same
        """
        self.sale.partner_shipping_id = self.company
        self.sale.partner_invoice_id = self.company
        addresses = self.sale.get_partner_addresses()
        self.assertFalse(addresses)

    def test_same_invoicing(self):
        """
        Invoicing address and partner_id are the same
        """
        self.sale.partner_invoice_id = self.company
        addresses = self.sale.get_partner_addresses()
        for key, value in addresses.items():
            self.assertEqual(key, self.contact_1)
            self.assertEqual(value, "Shipping Address:")

    def test_same_shipping(self):
        """
        Shipping address and partner_id are the same
        """
        self.sale.partner_shipping_id = self.company
        addresses = self.sale.get_partner_addresses()
        for key, value in addresses.items():
            self.assertEqual(key, self.contact_2)
            self.assertEqual(value, "Invoicing Address:")
