# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Sale Report Top Categories",
    "summary": """
        Add Product Top Category to Sale Report""",
    "version": "12.0.1.0.0",
    "category": "Sale",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "maintainers": ["victor-champonnois"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "product_top_category",
        "sale_report_wizard",
        "sale",
    ],
    "excludes": [],
    "data": ["data/data.xml"],
    "demo": [],
    "qweb": [],
}
