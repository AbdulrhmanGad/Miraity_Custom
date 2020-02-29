from odoo import api, fields, models


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    code = fields.Char(string="Code", required=False, )
    product_id = fields.Many2one('product.product', string='Product', help="Product concerned by the ticket")

    action_type = fields.Selection(string="", selection=[('return', 'Return'), ('refund', 'Refund'), ])

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or '/'
        values['code'] = seq
        return super(HelpDeskTicket, self).create(values)

    @api.onchange('sale_order_id', 'product_id')
    def _onchange_product_sale_order_id(self):
        for rec in self:
            res = {}
            products = []
            for line in rec.sale_order_id.order_line:
                products.append(line.product_id.id)
            if len(products)> 0:
                print(">>><<<<<<", len(products))
                res['domain'] = {'product_id': [('id', 'in', products)]}
            else:
                res['domain'] = {'product_id': [('id', '=', False)]}


class HelpDeskTicketType(models.Model):
    _inherit = 'helpdesk.ticket.type'
    code = fields.Char(string="Code",  required=True, )

