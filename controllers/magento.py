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
