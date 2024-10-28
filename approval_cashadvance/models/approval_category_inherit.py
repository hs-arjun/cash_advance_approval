from odoo import fields, models, api, _


class ApprovalCategoryInherit(models.Model):
    _inherit = 'approval.category'

    approval_type = fields.Selection(
        selection_add=[
            ('purchase', "Create RFQ's"),
            ('cash_advance', 'Cash Advance')
        ]
    )


class ApprovalRequestInherit(models.Model):
    _inherit = 'approval.request'

    sales_order_id = fields.Many2one('sale.order', string="Related Sales Order")

    def create_cash_advance(self):
        """ Create and/or modify Sales Orders. """
        self.ensure_one()
        # Define the customer for the Sales Order (e.g., use self.partner_id or define the logic to get customer)
        customer = self.request_owner_id  # Adjust this line based on your model's setup
        # Create a blank Sales Order
        so_vals = {
            'partner_id': customer.id,
            'origin': self.name,  # Set origin as the approval request's name
            # Add any additional fields if needed
        }
        sales_order = self.env['sale.order'].create(so_vals)
        # Store the sales order reference if needed for future actions
        self.sales_order_id = sales_order.id  # Assuming you've added a Many2one field `sales_order_id`

    def action_open_sales_orders(self):
        """Open related Sales Orders created by this approval request."""
        self.ensure_one()
        if not self.sales_order_id:
            raise ValueError(_("No Sales Order is linked to this Approval Request."))
        # Define the domain to open the related sales order
        domain = [('id', '=', self.sales_order_id.id)]
        action = {
            'name': _('Sales Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'target': 'current',
            'domain': domain,
        }
        return action