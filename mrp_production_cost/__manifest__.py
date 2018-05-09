# -*- coding: utf-8 -*-
{
    'name': "mrp_production_cost",

    'summary': """
        Allows to check costs of a manufacturing order before it is done""",

    'description': """
        Allows to check costs of a manufacturing order before it is done
    """,

    'author': "Yusnel Rojas Garcia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',

        'report/mrp_production_cost_report_templates.xml',
        'report/mrp_report_views_main.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}