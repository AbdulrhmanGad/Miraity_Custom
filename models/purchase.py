from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('received', 'Received'),
                                            ('warehouse', 'Warehouse'), ])


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sample_qty = fields.Float(string="Sample Qty", )
