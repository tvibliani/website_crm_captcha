{
    'name': 'Captcha - Contact Form',
    'category': 'Website',
    'website': 'https://github.com/tvibliani/website_crm_captcha',
    'license': 'AGPL-3',
    'summary': 'Captcha for Contact Form',
    'version': '8.0.1.0.0',
    'description': """
Odoo Contact Form Captcha
=========================

        """,
    'author': 'Temur',
    'depends': ['website_crm'],
    'external_dependencies': {'python': ['captcha']},
    'data': [
        'views/website_crm_captcha.xml',
    ],
    'installable': True,
    'auto_install': False,
}
