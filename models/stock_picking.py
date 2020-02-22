from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    code = fields.Char(string="Code", required=False, )

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('stock.location') or '/'
        values['code'] = seq
        return super(StockLocation, self).create(values)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            rec.purchase_id.state = 'received'
        return res