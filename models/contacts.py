from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_sales_channel = fields.Boolean(string="Sales Channel", )
    is_commission = fields.Boolean(string="Commission", )
    rate = fields.Float(string="Rate", )
    is_date = fields.Boolean(string="With date")
    start_date = fields.Date(string="Start Date", required=False, )
    end_date = fields.Date(string="End Date", required=False, )
    partner_related_ids = fields.One2many(comodel_name="partner.related.partners", inverse_name="partner_id",
                                          string="Related Partners",   )
    products_related_ids = fields.One2many(comodel_name="partner.related.products", inverse_name="partner_id",
                                          string="Related Products",  )
    channel_type = fields.Selection(string="Type", selection=[('company', 'Company'),
                                                              ('celebrity', 'Celebrity'),
                                                              ('makeup', 'Makeup Artist'),
                                                              ],)


class RelatedPartner(models.Model):
    _name = 'partner.related.partners'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    related_partner_id = fields.Many2one(comodel_name="res.partner", required=True )
    commission = fields.Float(string="Commission", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date",required=True )


class RelatedProducts(models.Model):
    _name = 'partner.related.products'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    product_id = fields.Many2one(comodel_name="product.template", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date",)
    is_active = fields.Boolean(string="Active", default=True)
