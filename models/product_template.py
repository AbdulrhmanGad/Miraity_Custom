from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'


    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'sku_no'])
        return [(template.id, '%s%s' % (template.sku_no and '[%s] ' % template.sku_no or '', template.name))
                for template in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        super(ProductProduct, self).name_search(name)
        args = args or []
        domain = []
        if name:
            domain = ['|', '|',('sku_no', operator, name), ('name', operator, name), ('default_code', operator, name)]
        results = self.search(domain + args, limit=limit)
        return results.name_get()


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    ar_name = fields.Char('Arabic Brand Name')
    brand_id = fields.Many2one('product.brand', string='Brand', help='Select a brand for this product')
    sku_no = fields.Char('Sku No', readonly=True, copy=False)
    ready_test_qty = fields.Float(string="Sample", )
    magento_qty = fields.Float(string="Magento Qty", )
    magento_test_qty = fields.Float(string="Magento Sample", )
    e_commerce = fields.Boolean(string="E-Commerce", )
    active = fields.Boolean('Active', default=True, help="Set active to false to hide the Brand without removing it.")
    is_gift = fields.Boolean(string="Gift")
    review_ids = fields.One2many(comodel_name="product.review", inverse_name="product_id", string="Product Review", )

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'sku_no'])
        return [(template.id, '%s%s' % (template.sku_no and '[%s] ' % template.sku_no or '', template.name))
                for template in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        super(ProductTemplate, self).name_search(name)
        args = args or []
        domain = []
        if name:
            domain = ['|', '|',('sku_no', operator, name), ('name', operator, name), ('default_code', operator, name)]
        results = self.search(domain + args, limit=limit)
        return results.name_get()

    # def get_first_child(self, categ_id):
    #     if categ_id.parent_id.parent_id:
    #         self.get_first_child(categ_id.parent_id)
    #     else:
    #         return categ_id
    #
    # @api.model
    # def create(self, values):
    #     categ_id = self.env['product.category'].browse(values['categ_id'])
    #     category_id = self.env['product.category']
    #     if categ_id.parent_id.parent_id:
    #         category_id = self.get_first_child(categ_id.parent_id)
    #     else:
    #         category_id = categ_id
    #     if category_id:
    #         seq = category_id.product_count
    #         short_description = self.env['ir.config_parameter'].sudo().get_param('base_setup.short_description')
    #         if short_description and category_id.name and seq:
    #             values['sku_no'] = str(short_description + category_id.name[:2] + str(seq).zfill(6)).upper()
    #             category_id.product_count += 1
    #     return super(ProductTemplate, self).create(values)


class SaleChannelReview(models.Model):
    _name = 'product.review'

    product_id = fields.Many2one(comodel_name="product.template",)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    is_sale_channel = fields.Boolean(string="Sale Channel?", )
    review = fields.Selection(string="Review", selection=[
        ('1', '1 Star'),
        ('2', '2 Star'),
        ('3', '3 Star'),
        ('4', '4 Star'),
        ('5', '5 Star'),
    ], required=True, )
    note = fields.Text(string="Note", required=False, )
