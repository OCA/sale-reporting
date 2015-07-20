# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

import calendar
from datetime import date
from dateutil import relativedelta
import json

from openerp import api, fields, models, tools


class CRMCaseSection(models.Model):
    _inherit = 'crm.case.section'

    @api.multi
    def _get_base_sale_orders_data(self):
        obj = self.pool['sale.order']
        month_begin = date.today().replace(day=1)
        date_begin = (
            month_begin -
            relativedelta.relativedelta(months=self._period_number - 1)
            ).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        date_end = month_begin.replace(
            day=calendar.monthrange(month_begin.year, month_begin.month)[1]
            ).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)

        created_domain = [('state', '=', 'draft'),
                          ('date_order', '>=', date_begin),
                          ('date_order', '<=', date_end)]
        validated_domain = [('state', 'not in', ['draft', 'sent', 'cancel']),
                            ('date_order', '>=', date_begin),
                            ('date_order', '<=', date_end)]

        for section in self:
            section.monthly_quoted = json.dumps(
                self._crm_case_section__get_bar_values(
                    obj,
                    [('section_id', '=', section.id)] + created_domain,
                    ['amount_base_total', 'date_order'],
                    'amount_base_total', 'date_order'
                ))
            section.monthly_confirmed = json.dumps(
                self._crm_case_section__get_bar_values(
                    obj,
                    [('section_id', '=', section.id)] + validated_domain,
                    ['amount_base_untaxed', 'date_order'],
                    'amount_base_untaxed', 'date_order'
                ))

    monthly_quoted = fields.Char(compute="_get_base_sale_orders_data")
    monthly_confirmed = fields.Char(compute="_get_base_sale_orders_data")
