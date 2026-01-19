# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Report Crossed Out Original Price",
    "version": "18.0.1.0.0",
    "author": "Sygel, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "license": "AGPL-3",
    "category": "Sales",
    "summary": "Sale report crossed out original price when a discount exists",
    "depends": ["sale", "sale_order_line_base_price_and_has_discount"],
    "data": ["reports/report_saleorder_document.xml", "views/res_config_settings.xml"],
    "installable": True,
}
