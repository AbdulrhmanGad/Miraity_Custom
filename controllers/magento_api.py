# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractMagentoApi(models.AbstractModel):
    _name = 'magento.api'

    # {"jsonrpc": "2.0",
    #  "params": {"token": "583eb6fe45dab22785b65a7713cb32092a1d423b", "customer": "CT0004", "products": [
    #      {"sku": "MIROSP00010023", "quantity": "1", "price_unit": "5"}
    #  ]}}
    def create_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo')
        auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
        if int(magento_user_id) == int(auth_user):
            if magento_token and magento_token == kw['token']:
                partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['customer'])])
                shipping_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['shipping_address'])])
                if partner_id:
                    if 'products' in kw:
                        for product in kw['products']:
                            product_id = http.request.env['product.product'].sudo().search(
                                [('sku_no', '=', product['sku'])])
                            if len(product_id) == 0:
                                http.request.env['authenticate.api'].logout()
                                return {
                                    'success': False,
                                    'message': 'One or More products Not Founded !!',
                                    'code': '305',
                                    'ID': None,
                                }
                    else:
                        return {
                            'success': False,
                            'message': 'Please enter Product for sale order',
                            'code': '310',
                            'ID': None,
                        }
                    sale_id = http.request.env['sale.order'].sudo().create({
                        'partner_id': partner_id.id,
                        'partner_shipping_id': shipping_id.id,
                        'payment_method': '1' if int(kw['payment']) == 1 else '2' if int(kw['payment']) == 2 else False,
                    })
                    for product in kw['products']:
                        product_id = http.request.env['product.product'].sudo().search(
                            [('sku_no', '=', product['sku'])])
                        http.request.env['sale.order.line'].sudo().create({
                            'order_id': sale_id.id,
                            'product_id': product_id.id,
                            'sample': True if kw['sample'] == 1 else False,
                            'name': "[" + product_id.sku_no + "]" + product_id.name,
                            'product_uom_qty': product['quantity'],
                            'price_unit': product['price_unit'],
                        })
                    http.request.env['authenticate.api'].logout()
                    return {'success': True, 'message': "Success, sale order created %s" % sale_id.name}
                else:
                    http.request.env['authenticate.api'].logout()
                    return {
                        'success': False,
                        'message': 'Check Contact code',
                        'code': '309',
                        'ID': None,
                    }
            else:
                http.request.env['authenticate.api'].logout()
                return {
                    'success': False,
                    'message': 'Magento Token ERROR Check the correct of it',
                    'code': '302',
                    'ID': None,
                }
        else:
            http.request.env['authenticate.api'].logout()
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }

    #  {"jsonrpc": "2.0","params":{"token": "583eb6fe45dab22785b65a7713cb32092a1d423b","order":"S00040","products":[
    #  	{"sku": "MIRSa000037","qty":"1"}
    #  ] }}

    def receive_sale_order(self, kw):
        try:

            magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
            magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
            # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo') # Localhost
            auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo') # test server
            if int(magento_user_id) == int(auth_user):
                if magento_token and magento_token == kw['token']:
                    sale_id = http.request.env['sale.order'].sudo().search([('name', '=', kw['order'])])
                    if sale_id:
                        sale_id.action_confirm()
                        for pick in sale_id.picking_ids:
                            if len(kw['products']) != 0:
                                products = []
                                for line in pick.move_line_ids_without_package:
                                    products.append(line.product_id.sku_no)
                                    for product in kw['products']:
                                        if product['sku'] not in products:
                                            http.request.env['authenticate.api'].logout()
                                            return {
                                                'success': False,
                                                'message': 'One or More products Not Founded !!',
                                                'code': '305',
                                                'ID': None,
                                            }
                                for line in pick.move_line_ids_without_package:
                                    for product in kw['products']:
                                        if line.product_id.sku_no == product['sku']:
                                            line.qty_done = product['qty']
                                pick.button_validate()
                                if pick.state != 'done':
                                    backorder_ids = http.request.env['stock.backorder.confirmation'].sudo().search([('pick_ids', '=', pick.id)])
                                    for backorder in backorder_ids:
                                        backorder.process_cancel_backorder()
                                http.request.env['authenticate.api'].logout()
                                return {
                                    'success': True,
                                    'message': 'Done',
                                    'code': '307',
                                }

                            else:
                                http.request.env['authenticate.api'].logout()
                                return {
                                    'success': False,
                                    'message': 'NO Products !!',
                                    'code': '304',
                                    'ID': None,
                                }
                    else:
                        http.request.env['authenticate.api'].logout()
                        return {
                            'success': False,
                            'message': 'No Sale Order With this Code',
                            'code': '303',
                            'ID': None,
                        }

                    # return {'success': True, 'message': "Success", 'code': '555'}
                else:
                    http.request.env['authenticate.api'].logout()
                    return {
                        'success': False,
                        'message': 'Invalid Token',
                        'code': '302',
                        'ID': None,
                    }
            else:
                return {
                    'success': False,
                    'message': 'Please, Contact Administrator to Allow Magento Setting User',
                    'code': '301',
                    'ID': None,
                }
        except:
            return {
                'success': False,
                'message': 'Pffffffffffffff',
                'code': '301',
                'ID': None,
            }

    # picking
    # packing
    # delivery
    # delivered
    # sale
    def update_sale_order(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        magento_helpdesk_team_id = http.request.env['ir.config_parameter'].sudo().get_param(
            'base_setup.magento_helpdesk_team_id')
        # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo')
        auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
        if int(magento_user_id) == int(auth_user):
            if magento_token and magento_token == kw['token']:
                sale_id = http.request.env['sale.order'].sudo().search([('name', '=', kw['order'])])
                if len(sale_id) != 0:
                    try:
                        sale_id.write({"state": kw['state']})
                        http.request.env['authenticate.api'].logout()
                        ##################### Ticket Create if state cancelled ###############################
                        if int(kw['state']) == 6:
                            ticket = http.request.env['helpdesk.ticket'].sudo().create({
                                'partner_id': sale_id.partner_id.id,
                                'sale_order_id': sale_id.id,
                                'team_id': int(magento_helpdesk_team_id),
                                'priority': 3,
                                'name': "Cancelled Ordered",
                            })
                        ####################################################
                        return {'success': True, 'code': '308',
                                'message': "Success, sale order state is %s" % kw['state'], }
                    except:
                        http.request.env['authenticate.api'].logout()
                        return {
                            'success': False,
                            'message': 'sale order has not state with %s' % kw['state'],
                            'code': '306',
                            'ID': None,
                        }
                else:
                    http.request.env['authenticate.api'].logout()
                    return {
                        'success': False,
                        'message': 'No Sale Order With this Code',
                        'code': '303',
                        'ID': None,
                    }
            else:
                http.request.env['authenticate.api'].logout()
                return {
                    'success': False,
                    'message': 'Invalid Token',
                    'code': '302',
                    'ID': None,
                }
        else:
            http.request.env['authenticate.api'].logout()
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }

    def create_ticket(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        magento_helpdesk_team_id = http.request.env['ir.config_parameter'].sudo().get_param(
            'base_setup.magento_helpdesk_team_id')
        # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo')
        auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
        if int(magento_user_id) == int(auth_user):
            if magento_helpdesk_team_id:
                if magento_token and magento_token == kw['token']:
                    partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['customer_code'])])
                    product_id = http.request.env['product.product'].sudo().search([('sku_no', '=', kw['product_sku'])],
                                                                                   limit=1)
                    if partner_id and product_id and kw['name']:
                        ticket = http.request.env['helpdesk.ticket'].sudo().create({
                            'partner_id': partner_id.id,
                            'product_id': product_id.id,
                            'team_id': int(magento_helpdesk_team_id),
                            'priority': kw['priority'],
                            'name': kw['name'],
                        })
                        http.request.env['authenticate.api'].logout()
                        return {'success': True, 'message': "Success, Ticket created %s" % ticket.code}
                    else:
                        http.request.env['authenticate.api'].logout()
                        return {
                            'success': False,
                            'message': 'Check Contact code or Product code',
                            'code': '102',
                            'ID': None,
                        }
                else:
                    http.request.env['authenticate.api'].logout()
                    return {
                        'success': False,
                        'message': 'Failed Token error',
                        'code': '102',
                        'ID': None,
                    }
            else:
                http.request.env['authenticate.api'].logout()
                return {
                    'success': False,
                    'message': 'Please, Contact Administrator to Allow Magento HelpDesk Team ',
                    'code': '302',
                    'ID': None,
                }
        else:
            http.request.env['authenticate.api'].logout()
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }

    def create_small_ticket(self, kw):
        magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
        magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
        magento_helpdesk_team_id = http.request.env['ir.config_parameter'].sudo().get_param(
            'base_setup.magento_helpdesk_team_id')
        # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo')
        auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
        if int(magento_user_id) == int(auth_user):
            if magento_helpdesk_team_id:
                if magento_token and magento_token == kw['token']:
                    partner_id = http.request.env['res.partner'].sudo().search([('code', '=', kw['customer_code'])])
                    if partner_id and kw['name']:
                        ticket = http.request.env['helpdesk.ticket'].sudo().create({
                            'partner_id': partner_id.id,
                            'team_id': int(magento_helpdesk_team_id),
                            'priority': kw['priority'],
                            'description': kw['description'],
                            'name': kw['name'],
                        })
                        http.request.env['authenticate.api'].logout()
                        return {'success': True, 'message': "Success, Ticket created %s" % ticket.code}
                    else:
                        http.request.env['authenticate.api'].logout()
                        return {
                            'success': False,
                            'message': 'Check Contact code or Product code',
                            'code': '102',
                            'ID': None,
                        }
                else:
                    http.request.env['authenticate.api'].logout()
                    return {
                        'success': False,
                        'message': 'Failed Token error',
                        'code': '102',
                        'ID': None,
                    }
            else:
                http.request.env['authenticate.api'].logout()
                return {
                    'success': False,
                    'message': 'Please, Contact Administrator to Allow Magento HelpDesk Team ',
                    'code': '302',
                    'ID': None,
                }
        else:
            http.request.env['authenticate.api'].logout()
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Magento Setting User',
                'code': '301',
                'ID': None,
            }

    # {
    #     "jsonrpc": "2.0",
    #     "params":
    #         {
    #             "token": "ceaab57d23fcc80144e3b143be1112ce3d159ba2",
    #             "name": "7777",
    #             "phone": "00244126090",
    #             "mobile": "01014527537",
    #             "email": "aaa@gmail.com",
    #             "website": "website.com",
    #             "is_channel": 1,
    #             "channel": "2",
    #             "address_name": "",
    #             "address_phone": ""
    #         }
    # }

    def create_contact(self, kw):
            # auth_user = http.request.env['authenticate.api'].authenticate('odoo13', 'demo', 'demo')
            auth_user = http.request.env['authenticate.api'].authenticate('erp', 'demo', 'demo')
            magento_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_user_id')
            magento_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.magento_token')
            is_account_prefix = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.is_account_prefix')
            account_receive_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.account_receive_id')
            account_payable_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.account_payable_id')
            if int(magento_user_id) == int(auth_user):
                if magento_token and magento_token == kw['token']:
                    if is_account_prefix == True:
                        last_receive_account_id = http.request.env['account.account'].search([('code', 'ilike', account_receive_id.code)], order=' id desc', limit=1)
                        last_payable_account_id = http.request.env['account.account'].search([('code', 'ilike', account_payable_id.code)], order='id desc', limit=1)

                        if last_receive_account_id == account_receive_id:
                            rec_code = int(account_receive_id.code)*10+1
                        else:
                            rec_code = int(last_receive_account_id.code)+1
                        if last_payable_account_id == account_payable_id:
                            pre_code = int(account_payable_id.code)*10+1
                        else:
                            pre_code = int(last_payable_account_id.code)+1
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
                                'company_type': 'person',
                                'website': kw['website'],
                                'is_sales_channel': kw['is_channel'],
                                'channel_type': '3' if kw['channel'] == '3' else '2' if kw['channel'] == '2' else False ,
                                'property_account_payable_id': account_receive_id.id,
                                'property_account_receivable_id': account_payable_id,

                            }
                            new_contact = request.env['res.partner'].sudo().create(vals)
                            if kw['address']:
                                for address in kw['address']:
                                    country_id = http.request.env['res.country'].sudo().search(
                                        [('name', '=', address["country"])])
                                    request.env['res.partner'].sudo().create({
                                        'parent_id': new_contact.id,
                                        'type': "delivery",
                                        'name': address["name"],
                                        'phone': address["phone"],
                                        'mobile': address["mobile"],
                                        'street': address["street"],
                                        'city': address["city"],
                                        'country_id': country_id,
                                        'zip': address["zip"],
                                        'comment': address["comment"],
                                    })

                            args= {
                                'success':True,
                                'message':"Success",
                                'ID':new_contact.id,
                            }
                            http.request.env['authenticate.api'].logout()
                            return args
                        else:
                            args = {
                                'success': False,
                                'message': 'Failed, Can not create account payable or account receive',
                                'code': '201',
                                'ID': None,
                            }
                            http.request.env['authenticate.api'].logout()
                            return args
                    else:
                            vals = {
                                'name': kw['name'],
                                'phone': kw['phone'],
                                'mobile': kw['mobile'],
                                'email': kw['email'],
                                'company_type': 'person',
                                'website': kw['website'],
                                'is_sales_channel': kw['is_channel'],
                                'channel_type': '3' if kw['channel'] == '3' else '2' if kw['channel'] == '2' else False ,
                            }
                            new_contact = request.env['res.partner'].sudo().create(vals)
                            if kw['address']:
                                for address in kw['address']:
                                    country_id = http.request.env['res.country'].sudo().search([('name', '=', address["country"])])
                                    request.env['res.partner'].sudo().create({
                                        'parent_id': new_contact.id,
                                        'type': "delivery",
                                        'name': address["name"],
                                        'phone': address["phone"],
                                        'mobile': address["mobile"],
                                        'street': address["street"],
                                        'city': address["city"],
                                        'country_id': country_id,
                                        'zip': address["zip"],
                                        'comment': address["comment"],
                                    })
                            args = {
                                'success': True,
                                'message': "Success",
                                'ID': "Contact ID is %s " %new_contact.code,
                            }
                            http.request.env['authenticate.api'].logout()
                            return args

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
                    'message': 'Please, Contact Administrator to Allow Magento Setting User',
                    'code': '1000002',
                    'ID': None,
                }
            http.request.env['authenticate.api'].logout()
            return args