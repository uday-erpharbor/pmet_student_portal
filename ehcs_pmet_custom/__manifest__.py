# -*- coding: utf-8 -*-
{
    'name': 'EHCS PMET CUSTOM',
    'author': 'ERP Harbor Consulting Services',
    'category': 'Sales',
    'summary': 'EHCS PMET CUSTOM',
    'website': 'http://www.erpharbor.com',
    'version': '18.0.1.0.0',
    'description': "",
    'depends': ['hr','mail'],
    'demo' : [],
    "data" : [   
        'security/ir.model.access.csv',
        'data/data.xml',
        "views/hr.xml",
        "views/course.xml",
        # "views/expence.xml",
        "views/student_alumni.xml",
    ],
    'installable': True,
}
