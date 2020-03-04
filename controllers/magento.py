# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Magento(http.Controller):

    @http.route('/Mg/CSOrder', type='json', auth='public')
    def create_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_sale_order(kw)
        return response

    @http.route('/MG/RSOrder', type='json', auth='public')
    def receive_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.receive_sale_order(kw)
        return response

    @http.route('/MG/USOrder', type='json', auth='public')
    def update_sale_order(self, **kw):
        model = http.request.env['magento.api']
        response = model.update_sale_order(kw)
        return response

    @http.route('/Mg/Ticket', type='json', auth='public')
    def create_ticket(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_ticket(kw)
        return response

    # {
    #     "jsonrpc": "2.0",
    #     "params":{
    #         "token": "53f233638d1e67bd118797b45edc14f8d645b644",
    #        "name":"Ticket from API",
    #        "customer_code":"CT0001",
    #        "priority":"1"
    # }}

    @http.route('/Mg/STicket', type='json', auth='public')
    def create_small_ticket(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_small_ticket(kw)
        return response

    # {
    #     "jsonrpc": "2.0",
    #     "params": {
    #         "token": "583eb6fe45dab22785b65a7713cb32092a1d423b",
    #         "name": "Mohammmed API",
    #         "phone": "00244126090",
    #         "mobile": "01014527537",
    #         "email": "aaa@gmail.com",
    #         "website": "website.com"
    # }}

    @http.route('/MG/CContacts', type='json', auth='public')
    def create_contact(self, **kw):
        model = http.request.env['magento.api']
        response = model.create_contact(kw)
        return response
