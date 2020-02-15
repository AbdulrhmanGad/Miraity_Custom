# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Authenticate(http.Controller):

    # {"jsonrpc": "2.0","params":{"db":"odoo13","login":"admin","password":"admin"}}
    @http.route('/web/session/authenticate', type='json', auth='none')
    def authenticate(self, db, login, password, base_location=None):
        try:
            request.session.authenticate(db, login, password)
            # return request.env['ir.http'].session_info()
            return {'success': True, 'message': "Success", }
        except:
            return {'success': False, 'code': '101', 'message': "Authenticate Error", }

