# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractMagentoApi(models.AbstractModel):
    _name = 'magento.api'

    #  {"jsonrpc": "2.0","params":{"token": "583eb6fe45dab22785b65a7713cb32092a1d423b","order":"S00040","products":[
    #  	{"sku": "MIRSa000037","qty":"1"}
    #  ] }}
    def receive_sale_order(self, kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        print(http.request.env['res.config.settings'].sudo().search([], order='id desc',))
        print(http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1).magento_user_id)
        if config.magento_user_id:
            if config.magento_token and config.magento_token == kw['token']:
                sale_id = http.request.env['sale.order'].sudo().search([('name', '=', kw['order'])])
                if sale_id:
                    sale_id.action_confirm()
                    for pick in sale_id.picking_ids:
                        if len(kw['products']) != 0:
                            products = []
                            for line in pick.move_line_ids_without_package:
                                products.append(line.product_id.sku_no)
                                for product in kw['products']:
                                    if product['sku'] not in products:
                                        return {
                                            'success': False,
                                            'message': 'One or More products Not Founded !!',
                                            'code': '305',
                                            'ID': None,
                                        }
                            for line in pick.move_line_ids_without_package:
                                for product in kw['products']:
                                    if line.product_id.sku_no == product['sku']:
                                        line.qty_done = product['qty']
                                        return {
                                            'success': False,
                                            'message': 'Done',
                                            'code': '307',
                                            'ID': None,
                                        }

                        else:
                            return {
                                'success': False,
                                'message': 'NO Products !!',
                                'code': '304',
                                'ID': None,
                            }
                else:
                    return {
                        'success': False,
                        'message': 'No Sale Order With this Code',
                        'code': '303',
                        'ID': None,
                    }

                # return {'success': True, 'message': "Success", 'code': '555'}
            else:
                return {
                    'success': False,
                    'message': 'Invalid Token',
                    'code': '302',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }

    #picking
    #packing
    #delivery
    #delivered
    #sale
    def update_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')

        if magento_user_id.id:
            if magento_token and magento_token == kw['token']:
                sale_id = http.request.env['sale.order'].sudo().search([('name', '=', kw['order'])])
                if len(sale_id) != 0:
                    try:
                        sale_id.write({"state": kw['state']})
                        return {'success': True,'code': '308', 'message': "Success, sale order state is %s" % kw['state'], }
                    except:
                        return {
                            'success': False,
                            'message': 'sale order has not state with %s' % kw['state'] ,
                            'code': '306',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'No Sale Order With this Code',
                        'code': '303',
                        'ID': None,
                    }
            else:
                return {
                    'success': False,
                    'message': 'Invalid Token',
                    'code': '302',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }
