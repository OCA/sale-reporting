import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-sale_order_line_position>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_report_product_image>=16.0dev,<16.1dev',
        'odoo-addon-sale_report_delivered>=16.0dev,<16.1dev',
        'odoo-addon-sale_report_delivered_subtotal>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
