{
    'name': 'Miraity Custom',
    'version': '1',
    'summary': 'Miraity Custom Work1',
    'description': 'Customization made for miraity company, include contact, purchase, sales, Inventory, sales modifications ',
    'category': 'Operations',
    'author': 'Ahmed Maher',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'stock', 'account', 'sale', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/company.xml',
        'views/contacts.xml',
        'views/logistics_warehouse.xml',
        'views/product_category.xml',
        'views/products_brand_view.xml',
        'views/purchase.xml',
        'views/sale_order.xml',
        'views/settings.xml',
        'wizard/wizard.xml',
        'wizard/purchase.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
