from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import re


class ProductBrand(models.Model):
    _inherit = 'product.category'

    short_name = fields.Char(string="Short Name", size=1)
    product_count = fields.Integer(string="product sequence", )
    active = fields.Boolean('Active', default=True, help="Set active to false to hide the Category without removing it.")

    @api.constrains('short_name')
    @api.onchange('short_name')
    def _onchange_short_name(self):
        for rec in self:
            if rec.short_name:
                if not re.match("^[a-zA-Z]*$", rec.short_name):
                    raise ValidationError(_("Short Code Must be only letters"))


