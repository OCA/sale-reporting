# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import models


class Name(models.AbstractModel):
    _inherit = "sale.report.delivered"

    def _sub_select_signed_qty(self):
        """Case for the signed quantity of Deposits"""
        res = super()._sub_select_signed_qty()
        deposit_sub_select_signed_qty = """
        WHEN (
            source_location.usage = 'internal' AND
            dest_location.usage = 'internal' AND
            s.customer_deposit is TRUE
            )
            THEN 1
        """
        return res + deposit_sub_select_signed_qty

    def _sub_where(self):
        """Add the case for Deposits"""
        res = super()._sub_where()
        deposit_sub_where = """ OR (
            source_location.usage = 'internal' AND
            dest_location.usage = 'internal' AND
            s.customer_deposit
        )"""
        return res + deposit_sub_where
