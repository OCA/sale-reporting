import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-sale_backorder',
        'odoo12-addon-sale_comment_template',
        'odoo12-addon-sale_layout_category_hide_detail',
        'odoo12-addon-sale_order_report_product_image',
        'odoo12-addon-sale_report_country_state',
        'odoo12-addon-sale_report_delivered_subtotal',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
