from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrderGiftReplace(models.TransientModel):
    _name = 'sale.order.gift.replacement'
    _description = 'sale order gift or replacement'

    is_gift = fields.Boolean(string="Gift", )
    is_replacement = fields.Boolean(string="Replacement", )
    product_id = fields.Many2one(comodel_name="product.product", string="product", )
    ticket_id = fields.Many2one(comodel_name="helpdesk.ticket", string="Ticket")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = {}
        for rec in self:
            if rec.is_gift:
                res['domain'] = {'product_id': [('is_gift', '=', 1)]}
        return res

    def create_ticket_number(self, code):
        sale_ids = self.env['sale.order'].search([('ticket_no', '=', code)])
        while len(sale_ids) >= 1:
            code = self.ticket_id.partner_id.random_number(8)
            self.create_ticket_number(code)
        return code

    def action_apply(self):
        for rec in self:
            if rec.is_gift:
                if rec.ticket_id.partner_id:
                    if rec.ticket_id.sale_order_id:
                        if rec.product_id:
                            if rec.product_id.sku_no:
                                sale_id = self.env['sale.order'].create({
                                    'partner_id': rec.ticket_id.partner_id.id,
                                    'ticket_no': 'GIFT' + str(
                                        self.create_ticket_number(self.ticket_id.partner_id.random_number(8))),
                                    'ticket_id': (4, rec.ticket_id.id),
                                    'miraity_type': 'gift',
                                })
                                self.env['sale.order.line'].create({
                                    'order_id': sale_id.id,
                                    'product_id': rec.product_id.id,
                                    'name': "[" + rec.product_id.sku_no + "]" + rec.product_id.name,
                                    'product_uom_qty': 1,
                                    'price_unit': 0,
                                })

                            else:
                                raise ValidationError(_("SKU Number for Product Missed"))
                            rec.ticket_id.gift_created = 1
                            rec.ticket_id.sale_order = sale_id.id
                        else:
                            raise ValidationError(_("product is required"))
                    else:
                        raise ValidationError(_("Sale order is required"))
                else:
                    raise ValidationError(_("Customer is required"))
            elif rec.is_replacement:
                if rec.ticket_id.replacement_id:
                    raise ValidationError(_("Replacement Already Created !!"))
                else:
                    if rec.ticket_id.partner_id:
                        if rec.ticket_id.sale_order_id:
                            if rec.product_id:
                                if rec.product_id.sku_no:
                                    sale_id = self.env['sale.order'].create({
                                        'ticket_id': (4, rec.ticket_id.id),
                                        'partner_id': rec.ticket_id.partner_id.id,
                                        'ticket_no': 'RPLC' + str(
                                            self.create_ticket_number(self.ticket_id.partner_id.random_number(8))),
                                        'miraity_type': 'replacement',  # XXXXX I think it Should be replacement
                                    })
                                    self.env['sale.order.line'].create({
                                        'order_id': sale_id.id,
                                        'product_id': rec.product_id.id,
                                        'name': "[" + rec.product_id.sku_no + "]" + rec.product_id.name,
                                        'product_uom_qty': 1,
                                        'price_unit': 0,
                                    })
                                else:
                                    raise ValidationError(_("SKU Number for Product Missed"))
                                rec.ticket_id.replacement_created = 1
                                rec.ticket_id.replacement_id = sale_id.id
                            else:
                                raise ValidationError(_("product is required"))
                        else:
                            raise ValidationError(_("Sale order is required"))
                    else:
                        raise ValidationError(_("Customer is required"))


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    code = fields.Char(string="Code", required=False, )
    action_type = fields.Selection(string="Type", selection=[('return', 'Return'), ('refund', 'Refund'), ])
    use_replacement = fields.Boolean(related='team_id.use_replacement', string='Use Replacement')
    sale_order = fields.Many2one(comodel_name="sale.order", string="Gift", )
    sale_order_gift_id = fields.Many2one(comodel_name="sale.order", string="Gift", ) # will remove
    replacement_id = fields.Many2one(comodel_name="sale.order", string="replacement", ) # will remove
    sale_order = fields.Many2one(comodel_name="sale.order", string="Gift", )
    origin = fields.Char(related="sale_order.ticket_no", required=False, )
    use_gift = fields.Boolean(related='team_id.use_gift', string='Use Gifts')
    gift_created = fields.Boolean(string="Gift created !", )
    replacement_created = fields.Boolean(string="Replacement created !", )

    def create_gift(self):
        for rec in self:
            if rec.sale_order:
                raise ValidationError(_("Gift - Replacement Already Created !!"))
            else:
                if rec.sale_order_id and rec.product_id:
                    view = self.env.ref('Miraity_Custom.sale_order_gift_replacement_view')
                    return {
                        'name': _("You Will Create Sale Order"),
                        'view_mode': 'form',
                        'view_id': view.id,
                        'res_id': False,
                        'context': {'default_is_gift': 1, 'default_ticket_id': self.id},
                        'view_type': 'form',
                        'res_model': 'sale.order.gift.replacement',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                    }
                else:
                    raise ValidationError(_("Please Enter Sale Order Number and it's product"))

    def create_replacement(self):
        for rec in self:
            if rec.replacement_id:
                raise ValidationError(_("Gift - Replacement Already Created !!"))
            else:
                if rec.sale_order_id and rec.product_id:
                    view = self.env.ref('Miraity_Custom.sale_order_gift_replacement_view')
                    return {
                        'name': _("You Will Create Sale Order"),
                        'view_mode': 'form',
                        'view_id': view.id,
                        'res_id': False,
                        'context': {'default_is_replacement': 1, 'default_ticket_id': self.id},
                        'view_type': 'form',
                        'res_model': 'sale.order.gift.replacement',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                    }
                else:
                    raise ValidationError(_("Please Enter Sale Order Number and it's product"))

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
    code = fields.Char(string="Code", required=False, )


class HelpDeskTeam(models.Model):
    _inherit = "helpdesk.team"

    use_replacement = fields.Boolean('Replacement')
    use_gift = fields.Boolean('Gift')
