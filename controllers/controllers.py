# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import  request


class CreateContact(http.Controller):
    # {"jsonrpc": "2.0","params":{"db":"odoo13","login":"admin","password":"admin"}}
    @http.route('/web/session/auth', type='json', auth='none')
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    # {"jsonrpc": "2.0","params": {"name": "FROM API"}}
    @http.route('/create/contact', type='json', auth='user')
    def create_contact(self, **kw):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if request.jsonrequest:
            print("rec" , kw)
            if kw['name']:
                vals = {
                    'name': kw['name'],
                    'property_account_payable_id': 1,
                    'property_account_receivable_id': 1,
                }
                new_contact = request.env['res.partner'].sudo().create(vals)
                args= {
                    'success':True,
                    'message':Success,
                    'ID':new_contact.id,
                }
            return args
        else:
            args = {
                'success': False,
                'message': 'Failed',
                'ID': none,
            }
            return args

