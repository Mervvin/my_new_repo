# -*- coding: utf-8 -*-
{
    "name" : "Customer Payment Details Report",
    "version" : "14.1",
    "sequence":-100,
    "category" : "accounting",
    "depends" : ['base','account'],
    "author": "Odoo",
    'summary': "customer payment details",
    "description": """customer payment details""",
    "website" : "http://github.in/",
    "data": [
        'security/ir.model.access.csv',
        'wizard/customer_payment_details_report.xml',
        'report/customer_payment_details_report_pdf.xml',
        'report/customer_payment_details_report_template.xml',
    ],
    "auto_install": False,
    "installable": True,
}

