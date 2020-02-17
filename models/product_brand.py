from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Product Brand"

    code = fields.Char('Code', )
    name = fields.Char('Brand Name', required=True)
    ar_name = fields.Char('Arabic Brand Name')
    description = fields.Text(translate=True)
    partner_id = fields.Many2one('res.partner', string='Partner', help='Select a partner for this brand if any.',
                                 ondelete='restrict')
    logo = fields.Binary('Logo File', attachment=True)
    product_ids = fields.One2many('product.template', 'brand_id', string='Brand Products', )
    products_count = fields.Integer(string='Number of products', compute='_compute_products_count', )
    active = fields.Boolean('Active', default=True, help="Set active to false to hide the Brand without removing it.")

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('product.brand') or '/'
        values['code'] = seq
        return super(ProductBrand, self).create(values)

    @api.depends('product_ids')
    def _compute_products_count(self):
        for brand in self:
            brand.products_count = len(brand.product_ids)

