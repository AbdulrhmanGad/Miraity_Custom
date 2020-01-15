from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = "Product Brand"
    _order = 'name'

    name = fields.Char('Brand Name', required=True)
    description = fields.Text(translate=True)
    internal_reference = fields.Integer(string='Internal Reference')
    partner_id = fields.Many2one('res.partner', string='Partner', help='Select a partner for this brand if any.',
                                 ondelete='restrict')
    logo = fields.Binary('Logo File', attachment=True)
    product_ids = fields.One2many('product.template', 'brand_id', string='Brand Products', )
    products_count = fields.Integer(string='Number of products', compute='_compute_products_count', )
    active = fields.Boolean('Active', default=True)

    @api.depends('product_ids')
    def _compute_products_count(self):
        for brand in self:
            brand.products_count = len(brand.product_ids)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product'
    )
    sku_no = fields.Char('Sku No')