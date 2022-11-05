import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-product_sold_by_delivery_week',
        'odoo13-addon-sale_comment_template',
        'odoo13-addon-sale_layout_category_hide_detail',
        'odoo13-addon-sale_order_line_position',
        'odoo13-addon-sale_order_product_recommendation_product_sold_by_delivery_week',
        'odoo13-addon-sale_order_report_product_image',
        'odoo13-addon-sale_report_country_state',
        'odoo13-addon-sale_report_delivered',
        'odoo13-addon-sale_report_delivered_brand',
        'odoo13-addon-sale_report_delivered_elaboration',
        'odoo13-addon-sale_report_delivered_partner_priority',
        'odoo13-addon-sale_report_delivered_subtotal',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
