# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models


class AbstractWarehouseApi(models.AbstractModel):
    _name = 'warehouse.api'
    _description='warehouse api'

    def create_transfer(self, kw):
        config = http.request.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if config.wh_user_id.id:
            # print(">>session<<", request.env['ir.http'].session_info())
            if config.warehouse_token and config.warehouse_token == kw['token']:
                location_id = http.request.env['stock.location'].search([('code', '=', kw['source'])])
                location_dest_id = http.request.env['stock.location'].search([('code', '=', kw['destination'])])
                product_id = http.request.env['product.product'].search([('sku_no', '=', kw['product_sku'])])
                if location_id and location_dest_id :
                    pass
                    if location_id.usage != 'view' and location_id.usage != 'view':
                        if product_id:
                            pass

                            picking_id = http.request.env['stock.picking'].create({
                                'picking_type_id' : "XXXXXX" ,
                                'location_id' : location_id.id,
                                'location_dest_id' : location_dest_id.id,
                            })
                            http.request.env['stock.move.line'].create({
                                'picking_id': picking_id.id,
                                'product_id': product_id.id,
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id,
                                'qty_done': kw['quantity'],
                            })
                        else:
                            return {
                                'success': False,
                                'message': 'There is no Product with this SKU Number',
                                'code': '205',
                                'ID': None,
                            }
                    else:
                        return {
                            'success': False,
                            'message': 'One or More location are not allowed, Please Call Administrator to Fix it',
                            'code': '204',
                            'ID': None,
                        }
                else:
                    return {
                        'success': False,
                        'message': 'Source Location or Destination Location Missed',
                        'code': '203',
                        'ID': None,
                    }

            else:
                return {
                    'success': False,
                    'message': 'Token ERROR',
                    'code': '202',
                    'ID': None,
                }
        else:
            return {
                'success': False,
                'message': 'Please, Contact Administrator to Allow Warehouse Setting User',
                'code': '201',
                'ID': None,
            }
