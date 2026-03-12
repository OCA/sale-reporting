# Copyright 2026 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, models


class SaleReportDelivered(models.Model):
    _name = "sale.report.delivered"
    _inherit = [
        "sale.report.delivered",
        "product.price.compliance.threshold.tier.mixin",
    ]

    @api.model
    def _get_price_compliance_selection_tiers(self):
        """Dislay texts on selection instead of icon colors."""
        return self._get_price_compliance_selection_tiers_text()

    def _select(self):
        res = super()._select()
        res += ", sub.price_compliance_tier"
        return res

    def _sub_select(self):
        res = super()._sub_select()
        res += ", sol.price_compliance_tier as price_compliance_tier"
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ", sub.price_compliance_tier"
        return res
