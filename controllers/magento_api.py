# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractMagentoApi(models.AbstractModel):
    _name = 'magento.api'


    # {"jsonrpc": "2.0",
    #  "params": {"token": "ceaab57d23fcc80144e3b143be1112ce3d159ba2", "customer": "CT0002", "products": [
    #      {"sku": "222Sa000034", "quantity": "1", "price_unit": "5" },
    #      {"sku": "222Sa000034", "quantity": "1", "price_unit": "5" }
    #  ]}}
    def create_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        if magento_user_id:
            if magento_token and magento_token == kw['token']:
                partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['customer'])])
                if partner_id:
                    for product in kw['products']:
                        product_id = http.request.env['product.product'].sudo().search(
                            [('sku_no', '=', product['sku'])])
                        if len(product_id) == 0:
                            return {
                                'success': False,
                                'message': 'One or More products Not Founded !!',
                                'code': '305',
                                'ID': None,
                            }

                    sale_id = http.request.env['sale.order'].sudo().create({
                        'partner_id': partner_id.id,
                    })
                    for product in kw['products']:
                        product_id = http.request.env['product.product'].sudo().search(
                            [('sku_no', '=', product['sku'])])
                        http.request.env['sale.order.line'].sudo().create({
                            'order_id': sale_id.id,
                            'product_id': product_id.id,
                            'name': "[" + product_id.sku_no + "]" + product_id.name,
                            'product_uom_qty': product['quantity'],
                            'price_unit': product['price_unit'],
                        })

                    return {'success': True, 'message': "Success, sale order created %s" % sale_id.name}
                else:
                    return {
                        'success': False,
                        'message': 'Check Contact code',
                        'code': '309',
                        'ID': None,
                    }
            else:
                return {
                    'success': False,
                    'message': 'Magento Token ERROR Check the correct of it',
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

    #  {"jsonrpc": "2.0","params":{"token": "583eb6fe45dab22785b65a7713cb32092a1d423b","order":"S00040","products":[
    #  	{"sku": "MIRSa000037","qty":"1"}
    #  ] }}
    def receive_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        if magento_user_id:
            if magento_token and magento_token == kw['token']:
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
                            pick.button_validate()
                            return {
                                'success': False,
                                'message': 'Done',
                                'code': '307',
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

    # picking
    # packing
    # delivery
    # delivered
    # sale
    def update_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')

        if magento_user_id:
            if magento_token and magento_token == kw['token']:
                sale_id = http.request.env['sale.order'].sudo().search([('name', '=', kw['order'])])
                if len(sale_id) != 0:
                    try:
                        sale_id.write({"state": kw['state']})
                        return {'success': True, 'code': '308',
                                'message': "Success, sale order state is %s" % kw['state'], }
                    except:
                        return {
                            'success': False,
                            'message': 'sale order has not state with %s' % kw['state'],
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

    def create_ticket(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        magento_helpdesk_team_id = http.request.env['ir.config_parameter'].sudo().get_param(
            'base_setup.magento_helpdesk_team_id')
        if magento_user_id:
            if magento_helpdesk_team_id:
                if magento_token and magento_token == kw['token']:
                    partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['customer_code'])])
                    product_id = http.request.env['product.product'].sudo().search([('sku_no', '=', kw['product_sku'])],
                                                                                   limit=1)
                    if partner_id and product_id and kw['name']:
                        ticket = http.request.env['helpdesk.ticket'].sudo().create({
                            'partner_id': partner_id.id,
                            'product_id': product_id.id,
                            'team_id': int(magento_helpdesk_team_id),
                            'priority': kw['priority'],
                            'name': kw['name'],
                        })
                        return {'success': True, 'message': "Success, Ticket created %s" % ticket.code}
                    else:
                        return {
                            'success': False,
                            'message': 'Check Contact code or Product code',
                            'code': '102',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'Failed Token error',
                        'code': '102',
                        'ID': None,
                    }
            else:
                return {
                    'success': False,
                    'message': 'Please, Contact Administrator to Allow Magento HelpDesk Team ',
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
