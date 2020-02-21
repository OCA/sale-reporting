import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-sale_layout_category_hide_detail',
        'odoo13-addon-sale_report_delivered_subtotal',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
