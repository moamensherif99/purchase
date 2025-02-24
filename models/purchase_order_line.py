from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.constrains('discount')
    def _check_discount_limit(self):
        for rec in self:
            manger_group = self.env.ref('purchase.group_purchase_manager')
            if manger_group and manger_group in self.env.user.groups_id:
                continue
            elif rec.order_id.exceed_discount_limit:
                continue
            elif rec.discount:
                if rec.product_id.discount_limit == 0 and rec.discount > rec.product_id.discount_limit:
                    raise ValidationError(
                        f"Discount limit exceeded! The maximum discount allowed for this product is {rec.product_id.discount_limit}%."
                    )
                elif rec.discount > rec.product_id.discount_limit:
                    raise ValidationError(
                        f"Discount limit exceeded! The maximum discount allowed for this product is {rec.product_id.discount_limit}%."
                    )
