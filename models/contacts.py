from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char(string="Code", readonly=True)
    code2 = fields.Char(string="Code2", readonly=True)
    is_sales_channel = fields.Boolean(string="Sales Channel", )
    is_customer = fields.Boolean(string="Customer", )
    is_vendor = fields.Boolean(string="vendor", )
    is_commission = fields.Boolean(string="Commission", )
    rate = fields.Float(string="Rate", )
    is_date = fields.Boolean(string="With date")
    start_date = fields.Date(string="Start Date", required=False, )
    end_date = fields.Date(string="End Date", required=False, )
    partner_related_ids = fields.One2many(comodel_name="partner.related.partners", inverse_name="partner_id",
                                          string="Related Partners", )
    products_related_ids = fields.One2many(comodel_name="partner.related.products", inverse_name="partner_id",
                                           string="Related Products", )
    cheque_related_ids = fields.One2many(comodel_name="partner.related.cheque", inverse_name="partner_id",
                                         string="Related Cheques", track_visibility='always')
    channel_type = fields.Selection(string="Type", selection=[('1', 'Company'),
                                                              ('2', 'Celebrity'),
                                                              ('3', 'Makeup Artist'),
                                                              ], )
    order_all = fields.Float(string="Order All", )
    order_paid = fields.Float(string="Order Paid", )
    order_pending = fields.Float(string="Order Pending", )
    balance_all = fields.Float(string="Balance All", )
    balance_paid = fields.Float(string="Balance Paid", )
    balance_pending = fields.Float(string="Balance Pending", )

    @api.onchange('is_customer')
    def _onchange_is_customer(self):
        for rec in self:
            if rec.is_customer:
                rec.customer_rank += 1
            else:
                rec.customer_rank -= 1

    @api.onchange('is_vendor')
    def _onchange_is_vendor(self):
        for rec in self:
            if rec.is_vendor:
                rec.supplier_rank += 1
            else:
                rec.supplier_rank -= 1

    @api.onchange('channel_type')
    @api.constrains('channel_type')
    def _constrains_channel_type(self):
        for rec in self:
            if not rec.env.user.has_group('sales_team.group_sale_manager'):
                if rec.channel_type == '1':
                    raise ValidationError(_(" Unable to Save Type With Company. Please contact your Administrator"))
            # if rec.channel_type == '2' or rec.channel_type == '3' and rec.is_sales_channel == False:
            #     raise ValidationError(_("Contact must be sales channel"))

    @api.model
    def create(self, values):
        if self.env.user.company_id:
            sequence = self.env.user.company_id.partner_count
            code2 = self.env['ir.sequence'].next_by_code('res.partner') or '/'
            seq = sequence + 1
            values['code'] = 'CT' + str(seq).zfill(4)
            values['code2'] = str(code2)
            self.env.user.company_id.partner_count += 1
        return super(ResPartner, self).create(values)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        super(ResPartner, self).name_search(name)
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', '|', ('mobile', '=ilike', name), ('email', '=ilike', name),
                      ('name', '=ilike', name), ('phone', operator, name), ('code', operator, name)]
        results = self.search(domain + args, limit=limit)
        return results.name_get()


class RelatedPartner(models.Model):
    _name = 'partner.related.partners'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    related_partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    commission = fields.Float(string="Commission", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    # @api.onchange('related_partner_id')
    # def _onchange_related_partner_id(self):
    #     for rec in self:
    #         partner_id = rec.partner_id.id
    #         print(">>>>>>>part<<<<",partner_id)
    #         res = {}
    #         if partner_id:
    #             res['domain'] = {
    #                 'related_partner_id': [('id', '!=', partner_id), ('is_sales_channel', '=', True),
    #                                        ('channel_type', '!=', 'company')]}
    #         return res


class RelatedProducts(models.Model):
    _name = 'partner.related.products'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    product_id = fields.Many2one(comodel_name="product.template", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", )
    is_active = fields.Boolean(string="Active", default=True)


class RelatedPartnerCheque(models.Model):
    _name = 'partner.related.cheque'

    partner_id = fields.Many2one(comodel_name="res.partner", track_visibility='onchange')
    value = fields.Float(string="Value", track_visibility='onchange')
    date = fields.Date(string="Date", track_visibility='onchange')
