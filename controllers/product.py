# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Product(http.Controller):
    @http.route('/MG/PReview', type='json', auth='public')
    def create_product_review(self, **kw):
        http.request.env['ir.config_parameter'].sudo().get_param('base_setup.call_center_token')
        model = http.request.env['product.api']
        response = model.create_product_review(kw)
        return response