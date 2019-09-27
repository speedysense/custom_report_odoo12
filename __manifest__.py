# -*- coding: utf-8 -*-

{
    "name": "Custom Report Odoo 12",
    "category": "Hidden",
    "author": "",
    "summary": "Sales summary report",
    "version": "1.0",
    "description": """
Sample custom report for daily sale summary in Odoo
        """,
    "depends": ["sale_management"],
    "data": [
        'data/data.xml',
        'wizard/sale_order_summary_wizard.xml',
        'report/sale_summary.xml',
    ],
    "installable": True,
}
