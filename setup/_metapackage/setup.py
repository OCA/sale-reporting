import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-sale-reporting",
    description="Meta package for oca-sale-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-sale_comment_template',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
