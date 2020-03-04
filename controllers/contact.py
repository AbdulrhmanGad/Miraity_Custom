# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Contact(http.Controller):
    @http.route('/MG/PRProducts', type='json', auth='public')
    def create_related_products(self, **kw):
        model = http.request.env['contact.api']
        response = model.create_related_products(kw)
        return response

    @http.route('/MG/PRPartner', type='json', auth='public')
    def create_related_partner(self, **kw):
        model = http.request.env['contact.api']
        response = model.create_related_partner(kw)
        return response

    @http.route('/MG/PRCheque', type='json', auth='public')
    def create_cheques(self, **kw):
        model = http.request.env['contact.api']
        response = model.create_cheques(kw)
        return response
