# -*- coding: utf-8 -*-
# from odoo import http


# class MiraityCustomization(http.Controller):
#     @http.route('/miraity_customization/miraity_customization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/miraity_customization/miraity_customization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('miraity_customization.listing', {
#             'root': '/miraity_customization/miraity_customization',
#             'objects': http.request.env['miraity_customization.miraity_customization'].search([]),
#         })

#     @http.route('/miraity_customization/miraity_customization/objects/<model("miraity_customization.miraity_customization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('miraity_customization.object', {
#             'object': obj
#         })
