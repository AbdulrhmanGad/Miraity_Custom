from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for rec in self:
            rec.purchase_id.state = 'received'
        return res