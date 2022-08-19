# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @property
    def address_fields(self):
        return [
            ("partner_invoice_id", _("Invoicing")),
            ("partner_shipping_id", _("Shipping")),
        ]

    def get_partner_addresses(self):
        """
        Returns a list of tuples corresponding to :
        - Name (a concatenation of same adresses - same partner with type)
        - Partners

        The partner field is added only if it is not the same partner
        as partner_id field.
        """
        addresses = {}
        for address, a_type in self.address_fields:
            partner_address = self[address]
            if partner_address != self.partner_id and partner_address not in addresses:
                addresses[partner_address] = [a_type]
            elif partner_address != self.partner_id and partner_address in addresses:
                addresses[partner_address].extend([a_type])
        res = {}
        for address, a_types in addresses.items():
            res[address] = "/".join(a_types) + " " + _("Address:")

        return res
