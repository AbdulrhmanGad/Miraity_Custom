# -*- coding: utf-8 -*-
import logging
from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError
from odoo import api, fields, models


class ProductCategoryWizard(models.TransientModel):
    _name = 'wizard.product.category'
    _description = 'add sequence to category'

    def action_apply(self):
        for rec in self:
            categ_ids = self.env['product.category'].search([('code', '=', False)])
            for categ in categ_ids:
                if categ.code == False:
                    seq = self.env['ir.sequence'].next_by_code('product.category') or '/'
                    categ.code = seq
        return {'type': 'ir.actions.act_window_close'}
