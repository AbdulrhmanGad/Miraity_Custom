from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = 'product.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Product Brand"

    code = fields.Char('Code', )
    name = fields.Char('Brand Name', required=True)
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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand', help='Select a brand for this product')
    sku_no = fields.Char('Sku No', readonly=True)
    ready_test_qty = fields.Float(string="Sample", )
    magento_qty = fields.Float(string="Magento Qty", )
    magento_test_qty = fields.Float(string="Magento Sample", )
    e_commerce = fields.Boolean(string="E-Commerce",  )

    def get_first_child(self, categ_id):
        if categ_id.parent_id.parent_id:
            self.get_first_child(categ_id.parent_id)
        else:
            return categ_id

    @api.model
    def create(self, values):
        self.env.user.company_id.short_description
        categ_id = self.env['product.category'].browse(values['categ_id'])
        category_id = self.get_first_child(categ_id.parent_id)
        if category_id:
            seq = category_id.product_count
            config = self.env['res.config.settings'].search([], order='id desc', limit=1)
            values['sku_no'] = config.short_description + category_id.name[:2] + str(seq).zfill(6)
            category_id.product_count += 1
        return super(ProductTemplate, self).create(values)
