# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_count = fields.Integer(string="product sequence", )
    partner_count = fields.Integer(string="product sequence", )
