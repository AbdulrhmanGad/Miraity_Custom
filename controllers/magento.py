# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Magento(http.Controller):

    @http.route('/create/sale/order', type='json', auth='public')
    def create_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_sale_order(kw)
        return response

    @http.route('/receive/sale/order', type='json', auth='public')
    def receive_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.receive_sale_order(kw)
        return response

    @http.route('/update/sale/order', type='json', auth='public')
    def update_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.update_sale_order(kw)
        return response

    @http.route('/magento/create/ticket', type='json', auth='public')
    def update_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_ticket(kw)
        return response

    #  {"jsonrpc": "2.0","params": {"name": "Mohammmed API", "phone": "00244126090", "mobile": "01014527537", "email": "aaa@gmail.com"}}
    @http.route('/create/contacts', type='json', auth='public')
    def update_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_contact(kw)
        return response

    @http.route('/test', type='json', auth='public')
    def update_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.test(kw)
        return response
