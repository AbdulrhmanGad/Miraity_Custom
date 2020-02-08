# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Customer(http.Controller):

    # this search for customer name, phone, mobile, email
    # {"jsonrpc": "2.0","params":{"name":"1014527537"}}
    # {"jsonrpc": "2.0","params":{"token": "MIR123456789","name":"Abdulrhman"}}
    @http.route('/search/customer', type='json', auth='user')
    def search_customer(self, **kw):
        config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
        if config.token_key and config.token_key == kw['token']:
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
                'message': 'Failed Token error',
                'ID': None,
            }

            return args

    # @http.route('/search/customer/orders', type='json', auth='user')
    # def search_customer_orders(self, **kw):
    #     sale_id = http.request.env['sale.order'].search([('name', 'ilike', kw['name'])])
    #     products = []
    #     for line in sale_id:
    #         products.append({
    #             'product': line.product_id.name,
    #             'label': line.name,
    #             'quantity': line.quantity,
    #         })
    #
    #     return {'success': True, 'message': "Success", 'products': products}

    @http.route('/search/order', type='json', auth='user')
    def search_order(self, **kw):
        config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
        if config.token_key and config.token_key == kw['token']:
            customer_ids = http.request.env['res.partner'].search(['|', '|', '|', '|', ('name', 'ilike', kw['name']),
                                                                   ('phone', 'ilike', kw['name']),
                                                                   ('mobile', 'ilike', kw['name']),
                                                                   ('code', 'ilike', kw['name']),
                                                                   ('email', 'ilike', kw['name']),
                                                                   ])
            orders = []
            for customer in customer_ids:
                sale_ids = http.request.env['sale.order'].search([('partner_id', '=', customer.id)])
                order = []
                for sale in sale_ids:
                    order.append({
                        'order': sale.name,
                        'date': sale.date_order,
                        'shipping_no': sale.shipping_no,
                        'status': sale.state,
                    })
                orders.append({'customer': customer.name,
                               'order': order})

            return {'success': True, 'message': "Success", 'orders': orders}
        else:
            args = {
                'success': False,
                'message': 'Failed Token error',
                'ID': None,
            }

            return args

    # {"jsonrpc": "2.0","params":{"name":"S00005"}}
    @http.route('/search/order/products', type='json', auth='user')
    def search_order_products(self, **kw):
        config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
        if config.token_key and config.token_key == kw['token']:
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
                'ID': None,
            }

            return args
