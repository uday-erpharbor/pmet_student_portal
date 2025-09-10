# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "EHCS Product Category Configurator",
    'version': '18.0.1.0.0',
    'category': 'Product',
    'summary': "Configure your product category",
    'description': "",
    'website': 'https://www.erpharbor.com',
    'depends': [
        'ehcs_simpro_integration', 'web'
    ],
    'data': [
        "security/ir.model.access.csv",
        # 'wizard/wiz_import_option_views.xml',
        'views/assets_type.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'product_category_configurator/static/src/**/*',
        ],
    },
    'auto_install': True,
    'license': 'LGPL-3',
}
