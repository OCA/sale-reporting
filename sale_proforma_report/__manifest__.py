# -*- coding: utf-8 -*-
# Copyright 2016 OdooMRP Team
# Copyright 2016 AvanzOSC (<http://www.avanzosc.es>)
# Copyright 2016 Tecnativa (<http://www.tecnativa.com>)
# Copyright 2016-17 Eficent Business and IT Consulting Services, S.L.
#                (<http://www.eficent.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Proforma Report",
    "version": "10.0.1.0.0",
    "depends": [
        "sale",
    ],
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Tecnativa,"
              "Eficent",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-reporting",
    "summary": "Proforma report option in sale orders",
    "data": [
        "views/sale_order_view.xml",
        "views/report_saleorder.xml",
    ],
    "installable": True,
}
