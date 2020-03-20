from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ticket_no = fields.Char(string="Ticket NO", required=False, )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sale', 'Approved'),
        ('sent', 'Quotation Sent'),
        ('picking', 'Picking'),
        ('packing', 'Packing'),
        ('delivery', 'On Delivery'),
        ('reschedule', 'Reschedule'),
        ('cancel_request', 'Cancel Request'),
        ('cancel', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('close', 'Closed'),
        ('done', 'done'),  # Is was ('done', 'Locked'), Abdulrhman Changed IT
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    miraity_type = fields.Selection(string="Miraity Type", selection=[('celebrity', 'Celebrity'),
                                                                      ('gift', 'Gift'),
                                                                      ('replacement', 'Replacement'),
                                                                      ])
    is_sales_channel = fields.Boolean(related="partner_id.is_sales_channel")
    shipping_no = fields.Char(string="Shipping No", )
    ticket_id = fields.One2many(comodel_name="helpdesk.ticket", inverse_name="sale_order",  string="Ticket")
    company_id = fields.Many2one('res.company', string='Company', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    payment_method = fields.Selection(string="", selection=[('1', 'cash'), ('2', 'bank'), ], required=False, )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self:
            if not rec.order_line:
                raise ValidationError(_("Please Enter Lines"))
        return res

    ticket_count = fields.Integer(string='Tickets', compute='_compute_tickets')

    def action_view_tickets(self):
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_my').read()[0]
        return action

    @api.depends('ticket_id')
    def _compute_tickets(self):
        for order in self:
            order.ticket_count = len(order.ticket_id)

    # @api.constrains('shipping_no')
    # def _onchange_shipping_no(self):
    #     for rec in self:
    #         if rec.status == "" and rec.shipping_no == False:
    #             pass


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_sample = fields.Boolean(string="Sample", )
    celebrity_id = fields.Many2one("res.partner", string="Celebrity",  )