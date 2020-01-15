{
    'name': 'Miraity Custom',
    'version': '1',
    'summary': 'Miraity Custom Work',
    'description': 'Customization made for miraity company , include contact,purchase,sales,Inventory,sales modifications ',
    'category': 'Operations',
    'author': 'Ahmed Maher',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/products_brand_view.xml',
    ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
