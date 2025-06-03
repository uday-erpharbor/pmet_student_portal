# -*- coding: utf-8 -*-
{
    'name': 'EHCS Global Search',
    'version': '16.0',
    'summary': 'EHCS Global Search',
    'description': """
        search a multiple fields values in global search filter.
     """,
    'author': 'ERP Harbor Consulting Services',
    'website': 'www.erpharbor.com',
    'depends': ['sale_management','account','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_compnay_views.xml',
        'views/res_config_view.xml',
        'views/sale_order_view.xml',
    ],
    'assets': {},
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
