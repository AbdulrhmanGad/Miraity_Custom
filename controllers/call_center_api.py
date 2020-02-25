# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractCallCenterApi(models.AbstractModel):
    _name = 'call.center.api'

    def search_customer(self, kw):
        call_center_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_user_id')
        call_center_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        if call_center_user_id.id:
            if call_center_token and call_center_token == kw['token']:
                customer_ids = http.request.env['res.partner'].search(['|', '|', '|', ('name', 'ilike', kw['name']),
                                                                       ('phone', 'ilike', kw['name']),
                                                                       ('mobile', 'ilike', kw['name']),
                                                                       ('code', 'ilike', kw['name']),
                                                                       ])
                customers = []
                for customer in customer_ids:
                    customers.append({'name': customer.name})
                return {'success': True, 'message': "Success", 'customers': customers}
            else:
                return {
                    'success': False,
                    'message': 'Token ERROR',
                    'code': '102',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Call Center Setting User',
                'code': '101',
                'ID': None,
            }

    def search_order(self, kw):

        call_center_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_user_id')
        call_center_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        if call_center_user_id.id:
            if call_center_token and call_center_token == kw['token']:
                customer_ids = http.request.env['res.partner'].search(
                    ['|', '|', '|', '|', ('name', 'ilike', kw['name']),
                     ('phone', 'ilike', kw['name']),
                     ('mobile', 'ilike', kw['name']),
                     ('code', 'ilike', kw['name']),
                     ('email', 'ilike', kw['name']),
                     ])
                orders = []
                for customer in customer_ids:
                    sale_ids = http.request.env['sale.order'].search([('partner_id', '=', customer.id)])
                    order = []
                    for sale in sale_ids:
                        order.append({
                            'order': sale.name,
                            'date': sale.date_order,
                            'shipping_no': sale.shipping_no,
                            'status': sale.state,
                        })
                    orders.append({'customer': customer.name,
                                   'order': order})

                return {
                    'success': True,
                    'message': "Success",
                    'orders': orders}
            else:
                args = {
                    'success': False,
                    'message': 'Failed Token error',
                    'code': '102',
                    'ID': None,
                }

                return args
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Call Center Setting User',
                'code': '101',
                'ID': None,
            }

    def search_order_products(self, kw):

        call_center_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_user_id')
        call_center_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        if call_center_user_id.id:
            if call_center_token and call_center_token == kw['token']:
                sale_id = http.request.env['sale.order'].search([('name', '=', kw['name'])])
                order = []
                for sale in sale_id.order_line:
                    order.append({
                        'product': sale.product_id.name,
                        'shipping_no': sale.order_id.shipping_no,
                    })
                return {
                    'success': True,
                    'message': "Success",
                    'order': sale_id.name,
                    'date': sale.order_id.date_order,
                    'status': sale.order_id.state,
                    'products': order
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed Token error',
                    'code': '102',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Call Center Setting User',
                'code': '101',
                'ID': None,
            }

    def create_ticket(self, kw):
        call_center_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_user_id')
        call_center_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        helpdesk_team_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.helpdesk_team_id')
        if call_center_user_id:
            if helpdesk_team_id:
                if call_center_token and call_center_token == kw['token']:
                    partner_id = http.request.env['res.partner'].search([('code', '=', kw['customer_code'])])
                    sale_id = http.request.env['sale.order'].search([('name', '=', kw['sale_order'])])
                    product_id = http.request.env['product.product'].search([('sku_no', '=', kw['product_sku'])],
                                                                            limit=1)
                    if partner_id and sale_id and product_id and kw['name']:
                        http.request.env['helpdesk.ticket'].create({
                            'partner_id': partner_id.id,
                            'sale_order_id': sale_id.id,
                            'product_id': product_id.id,
                            'team_id': helpdesk_team_id.id,
                            'priority': kw['priority'],
                            'name': kw['name'],
                        })
                        return {'success': True, 'message': "Success, Ticket created", }
                else:
                    return {
                        'success': False,
                        'message': 'Failed Token error',
                        'code': '102',
                        'ID': None,
                    }
            else:
                return {
                    'success': False,
                    'message': 'Please, Contact Administrator to Allow Help Desk Team Setting User!!',
                    'code': '103',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Call Center Setting User',
                'code': '101',
                'ID': None,
            }

    def create_stock(self, kw):
        # request.session.authenticate('odoo13', kw['login'], kw['password'])
        # session = request.env['ir.http'].session_info()
        # if session:
        wh_user_id = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.wh_user_id')
        call_center_token = http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        if wh_user_id.id:
            if call_center_token and call_center_token == kw['token']:
                purchase_id = http.request.env['purchase.order'].sudo().search([('name', '=', kw['po_number'])])
                for pick in purchase_id.picking_ids:
                    pick.partner_id = purchase_id.partner_id.id
                    if pick.state not in ['done', 'cancel']:
                        for move in pick.move_ids_without_package:
                            for product in kw['products']:
                                if product['sku_no'] == move.product_id.sku_no:
                                    move.quantity_done = product['delivered_qty']
                        pick.button_validate()

                return {'success': True, 'message': "Success", 'code': '555'}
            else:
                args = {
                    'success': False,
                    'message': 'Failed Token error',
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


