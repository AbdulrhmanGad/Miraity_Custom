from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ar_name = fields.Char('Arabic Brand Name')
    brand_id = fields.Many2one('product.brand', string='Brand', help='Select a brand for this product')
    sku_no = fields.Char('Sku No', readonly=True)
    ready_test_qty = fields.Float(string="Sample", )
    magento_qty = fields.Float(string="Magento Qty", )
    magento_test_qty = fields.Float(string="Magento Sample", )
    e_commerce = fields.Boolean(string="E-Commerce",  )
    active = fields.Boolean('Active', default=True, help="Set active to false to hide the Brand without removing it.")

    def get_first_child(self, categ_id):
        if categ_id.parent_id.parent_id:
            self.get_first_child(categ_id.parent_id)
        else:
            return categ_id

    @api.model
    def create(self, values):
        categ_id = self.env['product.category'].browse(values['categ_id'])
        category_id = self.env['product.category']
        if categ_id.parent_id.parent_id:
            category_id = self.get_first_child(categ_id.parent_id)
        else:
            category_id = categ_id
        print(">>>>>>>category_id>>>>>>>.", category_id)
        if category_id:
            seq = category_id.product_count
            config = self.env['res.config.settings'].search([], order='id desc', limit=1)
            print(">>>>>>>>>>>>>>.", config)
            print(config.short_description ,"and",  category_id.name,"and", seq)
            if config.short_description and category_id.name and seq:
                values['sku_no'] = config.short_description + category_id.name[:2] + str(seq).zfill(6)
                category_id.product_count += 1
        return super(ProductTemplate, self).create(values)
