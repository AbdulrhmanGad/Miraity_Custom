# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Stock(http.Controller):

    # this search for customer name, phone, mobile, email
    # {"jsonrpc": "2.0","params":{"name":"1014527537"}}
    # {"jsonrpc": "2.0","params":{"token": "MIR123456789","name":"Abdulrhman"}}
    @http.route('/create/stock', type='json', auth='public')
    def create_stock(self, **kw):
        print(">>>>>>>>>>>>>>>>", kw)
        model = http.request.env['call.center.api']
        response = model.create_stock(kw)
        print(response)
        return response
