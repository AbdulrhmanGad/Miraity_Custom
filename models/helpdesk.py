from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    code = fields.Char(string="Code", required=False, )
    action_type = fields.Selection(string="Type", selection=[('return', 'Return'), ('refund', 'Refund'), ])
    use_replacement = fields.Boolean(related='team_id.use_replacement', string='Use Replacement')
    sale_order_gift_id = fields.Many2one(comodel_name="sale.order", string="Gift number", )
    use_gift = fields.Boolean(related='team_id.use_gift', string='Use Gifts')
    gift_created = fields.Boolean(string="gift created !", )

    def create_gift(self):
        for rec in self:
            if rec.gift_created:
                raise ValidationError(_("Gift Already Created !!"))
            else:
                if rec.partner_id:
                    if rec.sale_order_id:
                        if rec.product_id:
                            sale_id = self.env['sale.order'].create({
                                'ticket_id': rec.id,
                                'partner_id': rec.partner_id.id,
                                'miraity_type': 'gift',
                            })
                            self.env['sale.order.line'].create({
                                'order_id': sale_id.id,
                                'product_id': rec.product_id.id,
                                'name': "[" + rec.product_id.sku_no + "]" + rec.product_id.name,
                                'product_uom_qty': 1,
                                'price_unit': 0,
                            })
                            rec.gift_created = 1
                            rec.sale_order_gift_id = sale_id.id
                        else:
                            raise ValidationError(_("product is required"))
                    else:
                        raise ValidationError(_("Sale order is required"))
                else:
                    raise ValidationError(_("Customer is required"))

    def create_replacement(self):
        for rec in self:
            raise ValidationError(_("NOT IMPLEMENTED YET !!!"))

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or '/'
        values['code'] = seq
        return super(HelpDeskTicket, self).create(values)

    @api.onchange('sale_order_id', 'product_id')
    def _onchange_product_sale_order_id(self):

        res = {}
        prod_ids = []
        for record in self:
            for line in record.sale_order_id.order_line:
                if line.product_id.id not in prod_ids:
                    prod_ids.append(line.product_id.id)
            if len(prod_ids) > 0:
                res['domain'] = {'product_id': [('id', 'in', prod_ids)]}
            else:
                res['domain'] = {'product_id': [('id', '=', False)]}
            return res


class HelpDeskTicketType(models.Model):
    _inherit = 'helpdesk.ticket.type'
    code = fields.Char(string="Code",  required=False, )


class HelpDeskTeam(models.Model):
    _inherit = "helpdesk.team"

    use_replacement = fields.Boolean('Replacement')
    use_gift = fields.Boolean('Gift')

