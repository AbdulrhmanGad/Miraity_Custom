# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Customer(http.Controller):

    # this search for customer name, phone, mobile, email
    # {"jsonrpc": "2.0","params":{"name":"1014527537"}}
    # {"jsonrpc": "2.0","params":{"token": "MIR123456789","name":"Abdulrhman"}}
    @http.route('/search/customer', type='json', auth='public')
    def search_customer(self, **kw):
        model = http.request.env['call.center.api']
        response = model.search_customer(kw)
        return response

    @http.route('/search/order', type='json', auth='public')
    def search_order(self, **kw):
        model = http.request.env['call.center.api']
        response = model.search_order(kw)
        return response

    # {"jsonrpc": "2.0","params":{"name":"S00005"}}
    @http.route('/search/order/products', type='json', auth='public')
    def search_order_products(self, **kw):
        model = http.request.env['call.center.api']
        response = model.search_order_products(kw)
        return response

    # {"jsonrpc": "2.0","params":{
    # "token": "378751c6d257696d6079548cdce82c6c1c90d549",
    # "name":"Ticket from API",
    # "customer_code":"CT0003",
    # "sale_order":"S00039",
    # "product_sku":"werSa000030",
    # "priority":"1"
    # }}
    @http.route('/create/ticket', type='json', auth='public')
    def create_ticket(self, **kw):
        model = http.request.env['call.center.api']
        response = model.create_ticket(kw)
        return response
