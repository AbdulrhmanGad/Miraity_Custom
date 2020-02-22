# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Magento(http.Controller):
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