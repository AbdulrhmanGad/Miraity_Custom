# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractMagentoApi(models.AbstractModel):
    _name = 'authenticate.api'

    # {"jsonrpc": "2.0","params":{"db":"odoo13","login":"admin","password":"admin"}}
    # @http.route('/web/session/authenticate', type='json', auth='none')
    def authenticate(self, db, login, password, base_location=None):
        try:
            request.session.authenticate(db, login, password)
            # session =  request.env['ir.http'].session_info()
            # session['uid']
            return request.session.uid
        except:
            return False

    # @http.route('/web/session/logout', type='json', auth='none')
    def logout(self):
        request.session.logout()