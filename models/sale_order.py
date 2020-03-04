from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('picking', 'Picking'),
        ('packing', 'Packing'),
        ('delivery', 'On Delivery'),
        ('delivered', 'Delivered'),
        ('sale', 'Sales Order'),
        ('done', 'done'),  # Is was ('done', 'Locked'), Abdulrhman Changed IT
        ('cancel_request', 'Cancel Request'),
        ('reschedule', 'Reschedule'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    miraity_type = fields.Selection(string="Miraity Type", selection=[('celebrity', 'Celebrity'),
                                                                      ('gift', 'Gift'),
                                                                      ])
    is_sales_channel = fields.Boolean(related="partner_id.is_sales_channel")
    shipping_no = fields.Char(string="Shipping No", )
    ticket_id = fields.Many2one(comodel_name="helpdesk.ticket", string="Ticket" )
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    payment_method = fields.Selection(string="", selection=[('1', 'cash'), ('2', 'bank'), ], required=False, )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if not rec.order_line:
                raise ValidationError(_("Please Enter Lines"))
        return  res


    # @api.constrains('shipping_no')
    # def _onchange_shipping_no(self):
    #     for rec in self:
    #         if rec.status == "" and rec.shipping_no == False:
    #             pass

