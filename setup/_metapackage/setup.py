import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-product_sold_by_delivery_week>=16.0dev,<16.1dev',
        'odoo-addon-sale_comment_template>=16.0dev,<16.1dev',
        'odoo-addon-sale_layout_category_hide_detail>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_line_position>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_product_recommendation_product_sold_by_delivery_week>=16.0dev,<16.1dev',
        'odoo-addon-sale_order_report_product_image>=16.0dev,<16.1dev',
        'odoo-addon-sale_packaging_report>=16.0dev,<16.1dev',
        'odoo-addon-sale_report_delivered>=16.0dev,<16.1dev',
        'odoo-addon-sale_report_delivered_subtotal>=16.0dev,<16.1dev',
        'odoo-addon-sale_report_delivered_volume>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
