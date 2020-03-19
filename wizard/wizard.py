# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError
from odoo import api, fields, models
from random import randint


class MissingProductSku(models.TransientModel):
    _name = 'miss.product.sku'
    _description = 'Missing Product Sku'

    res_ids = fields.Many2many(comodel_name="product.template", )
    to_magento = fields.Boolean(string="To Magento", )

    def action_apply(self):
        for rec in self:
            short_description = self.env['ir.config_parameter'].sudo().get_param('base_setup.short_description')
            product_ids = self.env['product.template'].search([('sku_no', '=', False)])
            for product in product_ids:
                if product.categ_id.parent_id and product.seller_ids:
                    if product.seller_ids[0] and product.seller_ids[0].name.supplier_no != False:
                        seq = product.categ_id.product_count
                        if product.seller_ids[0].name.products_count == 0:
                            product.seller_ids[0].name.products_count = 1
                        if product.categ_id.parent_id.parent_id and product.categ_id.short_name and\
                            product.categ_id.parent_id.short_name and product.categ_id.parent_id.parent_id.short_name:
                            sku_no = short_description.upper() + \
                                 str(product.categ_id.parent_id.parent_id.short_name[:1]) + \
                                 str(product.categ_id.parent_id.short_name[:1]) + \
                                 str(product.categ_id.short_name[:1]) + \
                                 product.seller_ids[0].name.supplier_no + \
                                 str(randint(0, 9999)).zfill(4)
                            product_id = self.env['product.product'].search([('sku_no', '=', sku_no)])
                            if product_id:
                                self.action_apply()
                            else:
                                product.sku_no = sku_no
                        product.categ_id.product_count += 1
                        product.seller_ids[0].name.products_count += 1
                if rec.to_magento:
                    pass
        return {'type': 'ir.actions.act_window_close'}


class ContactMissCode(models.TransientModel):
    _name = 'miss.contact.code'
    _description = 'Missing Contact Code'

    res_ids = fields.Many2many(comodel_name="res.partner", )

    def action_apply(self):
        for rec in self:
            contact_ids = self.env['res.partner'].search([('code', '=', False)])
            for contact in contact_ids:
                # sequence = self.env.user.company_id.partner_count
                # seq = sequence + 1

                contact.code = 'CT' + str(contact.check_partner_code(randint(0, 999999))).zfill(6)
                self.env.user.company_id.partner_count += 1

            contact2_ids = self.env['res.partner'].search([('supplier_no', '=', False)])
            for contact in contact2_ids:
                if contact.supplier_rank:
                    # supplier_no = self.env['ir.sequence'].next_by_code('res.partner') or '/'
                    supplier_no = str(contact.check_supplier_no(randint(0, 9999))).zfill(4)
                    contact.supplier_no = str(supplier_no)
        return {'type': 'ir.actions.act_window_close'}
