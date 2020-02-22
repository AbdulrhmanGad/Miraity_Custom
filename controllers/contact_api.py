# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models
from datetime import date, datetime



class AbstractContactApi(models.AbstractModel):
    _name = 'contact.api'

    #  {"jsonrpc": "2.0","params":{"token": "583eb6fe45dab22785b65a7713cb32092a1d423b","order":"S00040","products":[
    #  	{"sku": "MIRSa000037","qty":"1"}
    #  ] }}
    def create_related_products(self, kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.magento_user_id.id:
            if config.magento_token and config.magento_token == kw['token']:
                partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['code'])])
                if partner_id:
                    if partner_id.is_sales_channel == True:
                        for product in kw['products']:
                            product_id = http.request.env['product.template'].sudo().search([('sku_no', '=', product['sku'])])
                            start_date = datetime.strptime(product['start_date'], '%Y-%m-%d')
                            end_date = datetime.strptime(product['end_date'], '%Y-%m-%d')
                            if len(product_id) == 0:
                                return {
                                    'success': False,
                                    'message': 'One or More products Not Founded !!',
                                    'code': '305',
                                    'ID': None,
                                }
                            if  start_date>  end_date:
                                return {
                                    'success': False,
                                    'message': 'End Date Must be Greater Than Start Date ',
                                    'code': '308',
                                    'ID': None,
                                }

                        for product in kw['products']:
                            product_id = http.request.env['product.template'].sudo().search([('sku_no', '=', product['sku'])])
                            start_date = datetime.strptime(product['start_date'], '%Y-%m-%d')
                            end_date = datetime.strptime(product['end_date'], '%Y-%m-%d')
                            http.request.env['partner.related.products'].sudo().create({
                                'partner_id': partner_id.id,
                                'product_id': product_id.id,
                                'start_date': start_date,
                                'end_date': end_date,
                            })
                    else:
                        return {
                            'success': False,
                            'message': 'Contact is not Sales Channel',
                            'code': '307',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'NO Contact With this Code',
                        'code': '306',
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

    # {"jsonrpc": "2.0", "params": {"token": "583eb6fe45dab22785b65a7713cb32092a1d423b", "code": "CT0001", "partners": [
    #     {"code": "CT0019", "commission": "500", "start_date": "2020-2-20", "end_date": "2020-2-24"}
    # ]}}

    def create_related_partner(self, kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.magento_user_id.id:
            if config.magento_token and config.magento_token == kw['token']:
                main_partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['code'])])
                if main_partner_id:
                    if main_partner_id.is_sales_channel == True:
                        for partner in kw['partners']:
                            partner_id = http.request.env['res.partner'].sudo().search(
                                [('code', '=', partner['code'])])
                            start_date = datetime.strptime(partner['start_date'], '%Y-%m-%d')
                            end_date = datetime.strptime(partner['end_date'], '%Y-%m-%d')
                            if len(partner_id) == 0:
                                return {
                                    'success': False,
                                    'message': 'One or More Contact Not Founded !!',
                                    'code': '305',
                                    'ID': None,
                                }
                            if start_date > end_date:
                                return {
                                    'success': False,
                                    'message': 'End Date Must be Greater Than Start Date ',
                                    'code': '308',
                                    'ID': None,
                                }


                        for partner in kw['partners']:
                            partner_id = http.request.env['res.partner'].sudo().search(
                                [('code', '=', partner['code'])])
                            start_date = datetime.strptime(partner['start_date'], '%Y-%m-%d')
                            end_date = datetime.strptime(partner['end_date'], '%Y-%m-%d')
                            http.request.env['partner.related.partners'].sudo().create({
                                'partner_id': main_partner_id.id,
                                'related_partner_id': partner_id.id,
                                'commission': partner['commission'],
                                'start_date': start_date,
                                'end_date': end_date,
                            })
                            return {
                                'success': True,
                                'message': 'Contact/s Created',
                            }
                    else:
                        return {
                            'success': False,
                            'message': 'Contact is not Sales Channel',
                            'code': '307',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'NO Contact With this Code',
                        'code': '306',
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

    def create_cheques(self, kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.magento_user_id.id:
            if config.magento_token and config.magento_token == kw['token']:
                partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['code'])])
                if partner_id:
                    if partner_id.is_sales_channel == True:
                        try:
                            float(kw['value'])
                            http.request.env['partner.related.cheque'].sudo().create({
                                'partner_id': partner_id.id,
                                'value': kw['value'],
                                'date': date.today(),
                            })
                            return {
                                'success': False,
                                'message': 'Cheque Added',
                            }
                        except:
                            return {
                                'success': False,
                                'message': 'Cheque Value Must be Numbers and  Positive',
                                'code': '308',
                                'ID': None,
                            }
                    else:
                        return {
                            'success': False,
                            'message': 'Contact is not Sales Channel',
                            'code': '307',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'NO Contact With this Code',
                        'code': '306',
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