from odoo import api, fields, models


class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    code = fields.Char(string="Code", required=False, )

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or '/'
        values['code'] = seq
        return super(HelpDeskTicket, self).create(values)


