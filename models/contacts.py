from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char(string="Code", readonly=True)
    is_sales_channel = fields.Boolean(string="Sales Channel", )
    is_commission = fields.Boolean(string="Commission", )
    rate = fields.Float(string="Rate", )
    is_date = fields.Boolean(string="With date")
    start_date = fields.Date(string="Start Date", required=False, )
    end_date = fields.Date(string="End Date", required=False, )
    partner_related_ids = fields.One2many(comodel_name="partner.related.partners", inverse_name="partner_id",
                                          string="Related Partners", )
    products_related_ids = fields.One2many(comodel_name="partner.related.products", inverse_name="partner_id",
                                           string="Related Products", )
    channel_type = fields.Selection(string="Type", selection=[('1', 'Company'),
                                                              ('2', 'Celebrity'),
                                                              ('3', 'Makeup Artist'),
                                                              ], )

    @api.onchange('channel_type')
    @api.constrains('channel_type')
    def _constrains_channel_type(self):
        for rec in self:
            if not rec.env.user.has_group('sales_team.group_sale_manager'):
                if rec.channel_type == '1':
                    raise ValidationError(_(" Unable to Save Type With Company. Please contact your Administrator"))

    @api.model
    def create(self, values):
        if self.env.user.company_id:
            print(self.env.user.company_id)
            sequence = self.env.user.company_id.partner_count
            seq = sequence + 1
            values['code'] = 'CT' + str(seq).zfill(4)
            self.env.user.company_id.partner_count += 1
        return super(ResPartner, self).create(values)


class RelatedPartner(models.Model):
    _name = 'partner.related.partners'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    related_partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    commission = fields.Float(string="Commission", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)


class RelatedProducts(models.Model):
    _name = 'partner.related.products'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    product_id = fields.Many2one(comodel_name="product.template", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", )
    is_active = fields.Boolean(string="Active", default=True)
