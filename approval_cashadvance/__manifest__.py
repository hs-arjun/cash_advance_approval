# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Approval Cash Advance',
    'description': """
    Approval cash advance
    =================
    test purpose.
    """,
    'category': 'Accounting/Accounting',
    'sequence': 32,
    'depends': ['approvals', 'account_accountant'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/approval_request_form.xml',
    ],
    # 'license': 'OEEL-1',
    'auto_install': False,
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
}
