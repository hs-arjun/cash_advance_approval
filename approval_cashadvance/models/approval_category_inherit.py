from odoo import fields, models, api, _


class ApprovalCategoryInherit(models.Model):
    _inherit = 'approval.category'

    approval_type = fields.Selection(
        selection_add=[
            ('purchase', "Create RFQ's"),
            ('cash_advance', 'Cash Advance')
        ]
    )
    employee = fields.Many2one('hr.employee', string="Employee")


class ApprovalRequestInherit(models.Model):
    _inherit = 'approval.request'

    payment_id = fields.Many2one('account.payment', string="Related Payment")
    employee = fields.Many2one('hr.employee', string="Employee")
    payment_count = fields.Integer(string="Payment Count", compute="_compute_payment_count", store=True)

    @api.depends('payment_id')
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = self.env['account.payment'].search_count([('approval_request_id', '=', record.id)])

    def create_cash_advance(self):
        """ Create and/or modify Sales Orders. """
        self.ensure_one()
        employee = self.employee
        # Find the "Cash Advance" journal
        cash_advance_journal = self.env['account.journal'].search([('name', '=', 'Cash Advance')], limit=1)
        if not cash_advance_journal:
            raise ValueError(
                _("Cash Advance journal not found. Please create it in Accounting > Configuration > Journals."))
        # Prepare payment values
        payment_vals = {
            'employee': employee.id,
            'amount': self.amount,  # Use appropriate amount field
            'journal_id': cash_advance_journal.id,
            'payment_type': 'outbound',  # Adjust based on payment type
            'approval_request_id': self.id,
        }
        # Create the Account Payment
        payment = self.env['account.payment'].create(payment_vals)
        # Link the payment to the approval request
        self.payment_id = payment.id

    def action_open_cash_advance(self):
        """Open related Sales Orders created by this approval request."""
        self.ensure_one()
        # Check if `sales_order_id` is set and valid
        if not self.payment_id:
            raise ValueError(_("No Cash Advance is linked to this Approval Request."))
        # Define the domain to open the related sales order
        return {
            'name': _('Cash Advance'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'res_id': self.payment_id.id,
            'target': 'current',
        }

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    approval_request_id = fields.Many2one('approval.request', string="Approval Request", help="The related approval request for this payment.")