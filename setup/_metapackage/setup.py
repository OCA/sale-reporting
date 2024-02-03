import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_multicompany_reporting_currency>=15.0dev,<15.1dev',
        'odoo-addon-product_sold_by_delivery_week>=15.0dev,<15.1dev',
        'odoo-addon-sale_comment_template>=15.0dev,<15.1dev',
        'odoo-addon-sale_layout_category_hide_detail>=15.0dev,<15.1dev',
        'odoo-addon-sale_multicompany_reporting_currency>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_line_position>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_product_recommendation_product_sold_by_delivery_week>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_report_customer_lead>=15.0dev,<15.1dev',
        'odoo-addon-sale_order_report_product_image>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered_brand>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered_elaboration>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered_partner_priority>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered_subtotal>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_delivered_volume>=15.0dev,<15.1dev',
        'odoo-addon-sale_report_salesman>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
