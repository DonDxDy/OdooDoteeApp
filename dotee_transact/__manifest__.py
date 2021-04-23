
# -*- coding: utf-8 -*-
{
    'name': "dotee-transact",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale_subscription'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_view.xml',
        'views/subscription_view.xml',
        # 'views/templates.xml',
		'wizards/res_partner_report_button.xml',
        'wizards/view_debtor_report.xml',
        'reports/report_billing_header.xml',
        'reports/report_header_footer.xml',
        'reports/dotee_account_report.xml',
		'reports/dotee_billing_report.xml',
		'reports/debtor_report.xml',
        'reports/report.xml',
    ],
	#'qweb': ['static/src/xml/tree_view_button.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
