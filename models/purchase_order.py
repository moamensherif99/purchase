from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('waiting', 'Waiting For Approval'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    exceed_discount_limit = fields.Boolean()

    def button_confirm(self):

        res = super(PurchaseOrder, self).button_confirm()
        for rec in self:
            if self.env.user.has_group('purchase.group_purchase_manager'):
                if rec.state == 'waiting':
                    rec.state = 'purchase'
                continue
            if rec.exceed_discount_limit:
                rec.state = 'waiting'
        return res