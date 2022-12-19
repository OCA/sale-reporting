#  Copyright 2021-2022 Le Filament (<https://le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "sale_order_terms_document",
    "summary": "Attach Terms & Condtions PDF to sale report PDF",
    "version": "14.0.1.0.0",
    "development_status": "Production/Stable",
    "website": "https://github.com/OCA/sale-reporting",
    "author": "Le Filament, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "templates/sale_portal.xml",
        "views/sale_views.xml",
        "views/document_tc_views.xml",
    ],
}
