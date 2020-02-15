# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Customer(http.Controller):

    # this search for customer name, phone, mobile, email
    # {"jsonrpc": "2.0","params":{"name":"1014527537"}}
    # {"jsonrpc": "2.0","params":{"token": "MIR123456789","name":"Abdulrhman"}}
    @http.route('/search/customer', type='json', auth='user')
    def search_customer(self, **kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.call_center_token and config.call_center_token == kw['token']:
            customer_ids = http.request.env['res.partner'].search(['|', '|', '|', ('name', 'ilike', kw['name']),
                                                                   ('phone', 'ilike', kw['name']),
                                                                   ('mobile', 'ilike', kw['name']),
                                                                   ('code', 'ilike', kw['name']),
                                                                   ])
            customers = []
            for customer in customer_ids:
                customers.append({'name': customer.name})
            return {'success': True, 'message': "Success", 'customers': customers}
        else:
            args = {
                'success': False,
                'message': ' ',
                'code': '102',
                'ID': None,
            }

            return args

    @http.route('/search/order', type='json', auth='user')
    def search_order(self, **kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.call_center_token and config.call_center_token == kw['token']:
            customer_ids = http.request.env['res.partner'].search(['|', '|', '|', '|', ('name', 'ilike', kw['name']),
                                                                   ('phone', 'ilike', kw['name']),
                                                                   ('mobile', 'ilike', kw['name']),
                                                                   ('code', 'ilike', kw['name']),
                                                                   ('email', 'ilike', kw['name']),
                                                                   ])
            orders = []
            for customer in customer_ids:
                print(">>>>>>>>>>",customer)
                sale_ids = http.request.env['sale.order'].search([('partner_id', '=', customer.id)])
                order = []
                print(">>>>>>>>>>.",sale_ids)
                for sale in sale_ids:
                    order.append({
                        'order': sale.name,
                        'date': sale.date_order,
                        'shipping_no': sale.shipping_no,
                        'status': sale.state,
                    })
                    print(sale)
                orders.append({'customer': customer.name,
                               'order': order})

            return {
                'success': True,
                'message': "Success",
                'orders': orders}
        else:
            args = {
                'success': False,
                'message': 'Failed Token error',
                'code': '102',
                'ID': None,
            }

            return args

    # {"jsonrpc": "2.0","params":{"name":"S00005"}}
    @http.route('/search/order/products', type='json', auth='user')
    def search_order_products(self, **kw):
        config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
        if config.call_center_token and config.call_center_token == kw['token']:
            sale_id = http.request.env['sale.order'].search([('name', '=', kw['name'])])
            order = []
            for sale in sale_id.order_line:
                order.append({
                    'product': sale.product_id.name,
                    'date': sale.order_id.date_order,
                    'shipping_no': sale.order_id.shipping_no,
                    'status': sale.order_id.state,
                })
            return {'success': True, 'message': "Success", 'order': sale_id.name, 'products': order}
        else:
            args = {
                'success': False,
                'message': 'Failed Token error',
                'code': '102',
                'ID': None,
            }

            return args

    # {"jsonrpc": "2.0","params":{
    # "token": "378751c6d257696d6079548cdce82c6c1c90d549",
    # "name":"Ticket from API",
    # "customer_code":"CT0003",
    # "sale_order":"S00039",
    # "product_sku":"werSa000030"
    # }}
    @http.route('/create/ticket', type='json', auth='user')
    def create_ticket(self, **kw):
        print("ALL       ",http.request.env['res.config.settings'].search([], order='id desc',))
        config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
        session = request.env['ir.http'].session_info()
        if session['uid'] and  session['uid'] ==  config.call_center_user_id:
            if config.helpdesk_team_id and config.call_center_token and config.call_center_token == kw['token']:
                partner_id = http.request.env['res.partner'].search([('code', '=', kw['customer_code'])])
                sale_id = http.request.env['sale.order'].search([('name', '=', kw['sale_order'])])
                product_id = http.request.env['product.product'].search([('sku_no', '=', kw['product_sku'])], limit=1)
                if partner_id and sale_id and product_id and kw['name']:
                    http.request.env['helpdesk.ticket'].create({
                        'partner_id': partner_id.id,
                        'sale_order_id': sale_id.id,
                        'product_id': product_id.id,
                        'team_id': config.helpdesk_team_id.id,
                        'priority': kw['priority'],
                        'name': kw['name']   ,
                    })
                    return {'success': True, 'message': "Success, Ticket created", }
            else:
                args = {
                    'success': False,
                    'message': 'Failed Token error',
                    'code': '102',
                    'ID': None,
                }

                return args
        else:
            args = {
                'success': False,
                'message': 'User error',
                'code': '1000002',
                'ID': None,
            }

            return args
