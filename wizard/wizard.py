# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError
from odoo import api, fields, models


class MissingProductSku(models.TransientModel):
    _name = 'miss.product.sku'
    _description = 'Missing Product Sku'

    res_ids = fields.Many2many(comodel_name="product.template", )
    is_all = fields.Boolean(string="", )

    def action_apply(self):
        for rec in self:
            if rec.is_all:
                product_ids = self.env['product.template'].search([('sku_no', '=', False)])
                print(len(product_ids))
                for product in product_ids:
                    category_id = product.get_first_child(product.categ_id.parent_id)
                    if category_id:
                        seq = category_id.product_count
                        product.sku_no = self.env.user.company_id.sku_short + category_id.name[:2] + str(seq).zfill(6)
                        category_id.product_count += 1
            else:
                for product in rec.res_ids:
                    category_id = product.get_first_child(product.categ_id.parent_id)
                    if category_id:
                        seq = category_id.product_count
                        product.sku_no = self.env.user.company_id.sku_short + category_id.name[:2] + str(seq).zfill(6)
                        category_id.product_count += 1
        return {'type': 'ir.actions.act_window_close'}


class ContactMissCode(models.TransientModel):
    _name = 'miss.contact.code'
    _description = 'Missing Contact Code'

    res_ids = fields.Many2many(comodel_name="res.partner", )
    is_all = fields.Boolean(string="", )

    def action_apply(self):
        for rec in self:
            if rec.is_all:
                contact_ids = self.env['res.partner'].search([('code', '=', False)])
                for contact in contact_ids:
                    sequence = self.env.user.company_id.partner_count
                    seq = sequence + 1
                    contact.code = 'CT' + str(seq).zfill(4)
                    self.env.user.company_id.partner_count += 1
            else:
                for contact in rec.res_ids:
                    sequence = self.env.user.company_id.partner_count
                    seq = sequence + 1
                    contact.code = 'CT' + str(seq).zfill(4)
                    self.env.user.company_id.partner_count += 1
        return {'type': 'ir.actions.act_window_close'}
