# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Warehouse(http.Controller):

    # this search for customer name, phone, mobile, email
    # {"jsonrpc": "2.0","params":{"name":"1014527537"}}
    # {"jsonrpc": "2.0","params":{"token": "MIR123456789","name":"Abdulrhman"}}
    @http.route('/create/stock', type='json', auth='user')
    def create_stock(self, **kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.call_center_token and config.call_center_token == kw['token']:
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

            return args
