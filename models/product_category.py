from odoo import api, fields, models


class ProductBrand(models.Model):
    _inherit = 'product.category'

    short_name = fields.Char(string="Short Name", size=2)
    sequence_count = fields.Char(string="Sequence counter", )