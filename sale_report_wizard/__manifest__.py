# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Sale Report Wizard",
    "summary": """
        Wizard allowing to chose a report,
        and specifying the date range and the time steps""",
    "version": "12.0.1.0.0",
    "category": "Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "sale",
        "point_of_sale",
    ],
    "excludes": [],
    "data": [
        "views/menuitem.xml",
        "views/sale_reports_config_views.xml",
        "wizard/sale_report_wizard.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
    ],
    "demo": [],
    "qweb": [],
}
