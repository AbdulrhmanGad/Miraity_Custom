# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Warehouse(http.Controller):
    @http.route('/create/transfer', type='json', auth='public')
    def create_transfer(self, **kw):
        model = http.request.env['warehouse.api']
        response = model.create_transfer(kw)
        return response