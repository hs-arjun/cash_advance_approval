from odoo import fields, models, api


class InheritPayment(models.Model):
    _inherit = 'account.payment'

    employee = fields.Many2one('hr.employee', string="Employee")
