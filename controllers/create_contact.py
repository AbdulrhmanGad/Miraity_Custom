# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import  request


class CreateContact(http.Controller):

    #  {"jsonrpc": "2.0","params": {"name": "Mohammmed API", "phone": "00244126090", "mobile": "01014527537", "email": "aaa@gmail.com"}}
    @http.route('/create/contact', type='json', method=['POST'], auth='user')
    def create_contact(self, **kw):
        if request.jsonrequest:
            config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
            session = request.env['ir.http'].session_info()

            if session['uid'] and session['uid'] == config.magento_user_id.id:
                if config.magento_token and config.magento_token == kw['token']:
                    if config.is_account_prefix == True:
                        last_receive_account_id = http.request.env['account.account'].search([('code', 'ilike', config.account_receive_id.code)], order=' id desc', limit=1)
                        last_payable_account_id = http.request.env['account.account'].search([('code', 'ilike', config.account_payable_id.code)], order='id desc', limit=1)

                        if last_receive_account_id == config.account_receive_id:
                            rec_code = int(config.account_receive_id.code)*10+1
                        else:
                            rec_code = int(last_receive_account_id.code)+1
                        print(last_payable_account_id ,'==', config.account_payable_id)
                        if last_payable_account_id == config.account_payable_id:
                            print("last_payable_account_id", last_payable_account_id.code,">>>>>>>. ", config.account_payable_id.code)
                            pre_code = int(config.account_payable_id.code)*10+1
                        else:
                            pre_code = int(last_payable_account_id.code)+1
                            print(">pre ", pre_code)
                        account_receive_id = http.request.env['account.account'].sudo().create({
                            'name': kw['name'],
                            'code': rec_code,
                            'company_id': http.request.env.user.company_id.id,
                            'user_type_id': http.request.env['account.account.type'].sudo().search([], order='id desc', limit=1).id
                        })

                        account_payable_id = http.request.env['account.account'].sudo().create({
                            'name': kw['name'],
                            'code': pre_code,
                            'company_id': http.request.env.user.company_id.id,
                            'user_type_id': http.request.env['account.account.type'].sudo().search([], order='id desc', limit=1).id
                        })
                        if account_payable_id and account_receive_id:
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
                                'message': 'Failed, Can not create account payable or account receive',
                                'code': '201',
                                'ID': None,
                            }
                            return args
                    else:
                        try:
                            vals = {
                                'name': kw['name'],
                                'phone': kw['phone'],
                                'mobile': kw['mobile'],
                                'email': kw['email'],
                            }
                            new_contact = request.env['res.partner'].sudo().create(vals)
                            args = {
                                'success': True,
                                'message': "Success",
                                'ID': new_contact.id,
                            }
                            return args
                        except:
                            args = {
                                'success': False,
                                'message': 'Failed, KEYS Does not Match check spilling',
                                'code': '202',
                                'ID': None,
                            }
                else:
                    args = {
                        'success': False,
                        'message': 'Failed Token error',
                        'code': '102',
                        'ID': None,
                    }
            else:
                args = {
                    'success': False,
                    'message': 'User error',
                    'code': '1000002',
                    'ID': None,
                }

        return args

