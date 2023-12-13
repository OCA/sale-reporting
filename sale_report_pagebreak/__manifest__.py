# Copyright 2023 CGI37 (https://www.cgi37.com).
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale report page break",
    "summary": "Control Page Breaks in PDF sale report",
    "version": "14.0.1.0.0",
    "author": "Pierre Verkest, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-reporting",
    "license": "AGPL-3",
    "category": "Sales",
    "depends": ["sale", "report_qweb_table_pagebreak"],
    "data": [
        "reports/sale_report.xml",
    ],
    "maintainers": ["petrus-v"],
}
