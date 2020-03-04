# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractProductApi(models.AbstractModel):
    _name = 'product.api'

    #  {"jsonrpc": "2.0","params": {"product": "", "partner": "", "review": "5"}}
    def create_product_review(self, kw):
        auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        if int(magento_user_id) == int(auth_user):
            if magento_token and magento_token == kw['token']:
                product_id = http.request.env['product.template'].sudo().search([('sku_no', '=', kw['product'])])
                partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['partner'])])
                if product_id:
                    if partner_id:
                        if 1 <= int(kw['review']) <= 5:
                            review_id = http.request.env['product.review'].create({
                                'product_id': product_id.id,
                                'partner_id': partner_id.id,
                                'is_sale_channel': partner_id.id,
                                'review': kw['review'],
                            })
                            return {
                                'success': True,
                                'message': 'Thanks For your Review',
                                'code': '406',
                                'ID': review_id.id,
                            }
                        else:
                            return {
                                'success': False,
                                'message': 'Review code Out Of Range, Must be one of [ 1, 2, 3, 4, 5 ] ',
                                'code': '405',
                                'ID': None,
                            }
                    else:
                        return {
                            'success': False,
                            'message': 'Contact Not found, please Check Contact Code ',
                            'code': '403',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'Product Not found, please Check Product Code ',
                        'code': '402',
                        'ID': None,
                    }
            else:
                args = {
                    'success': False,
                    'message': 'Failed Token error',
                    'code': '102',
                    'ID': None,
                }
        else:
            args = {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '1000002',
                'ID': None,
            }
        http.request.env['authenticate.api'].logout()
        return args


        # else:
        #     return {
        #         'success': False,
        #         'message': 'Please, Contact Administrator to Allow Warehouse Setting User',
        #         'code': '401',
        #         'ID': None,
        #     }
