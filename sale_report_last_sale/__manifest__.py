# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Report Last Sale',
    'summary': 'Adds a report view to show how many days '
               'have passed since a partner ordered a product',
    'version': '11.0.1.1.0',
    'depends': [
        'sale',
    ],
    'author': 'Ivan Todorovich,'
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'data': [
        'reports/sale_last_sale_report.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'category': 'Sale',
    'installable': True,
}
