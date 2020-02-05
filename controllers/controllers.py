# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import  request


class CreateContact(http.Controller):
    
    # {"jsonrpc": "2.0","params":{"db":"odoo13","login":"admin","password":"admin"}}
    @http.route('/web/session/authauthenticate',type='json', auth='none')
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        # return request.env['ir.http'].session_info()
        return  { 'success':True, 'message':"Success", }

    #  {"jsonrpc": "2.0","params": {"name": "MOhammmed API", "phone": "00244126090", "mobile": "01014527537", "email": "aaa@gmail.com"}}
    @http.route('/create/contact', type='json', auth='user')
    def create_contact(self, **kw):
        if request.jsonrequest:
            config = http.request.env['res.config.settings'].search([], order='id desc', limit=1)
            acc_receive_prefix = config.acc_receive_prefix
            account_receive_id = http.request.env['account.account'].sudo().create({
                'name': acc_receive_prefix,
                'code': request.env.user.company_id.account_sequence,
                'company_id': http.request.env.user.company_id.id,
                'user_type_id': http.request.env['account.account.type'].sudo().search([], order='id desc', limit=1).id
            })
            request.env.user.company_id.account_sequence += 1

            acc_payable_prefix = config.acc_payable_prefix

            account_payable_id = request.env['account.account'].sudo().create({
                'name': acc_payable_prefix,
                'code': request.env.user.company_id.account_sequence,
                'company_id': request.env.user.company_id.id,
                'user_type_id': request.env['account.account.type'].search([], order='id desc', limit=1).id
            })
            request.env.user.company_id.account_sequence +=1
            if kw['name']:
                vals = {
                    'name': kw['name'],
                    'phone': kw['phone'],
                    'mobile': kw['mobile'],
                    'email': kw['email'],
                    'property_account_payable_id': account_receive_id.id,
                    'property_account_receivable_id': account_payable_id,
                }
                new_contact = request.env['res.partner'].sudo().create(vals)
                args= {
                    'success':True,
                    'message':"Success",
                    'ID':new_contact.id,
                }
                return args
        else:
            args = {
                'success': False,
                'message': 'Failed',
                'ID': None,
            }
            return args

