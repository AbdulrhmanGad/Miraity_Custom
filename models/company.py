# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_count = fields.Integer(string="product sequence", )
    partner_count = fields.Integer(string="Contact sequence", )
    acc_receive_prefix = fields.Integer(string="Account Receivable Prefix")
    acc_payable_prefix = fields.Integer(string="Account Payable Prefix")
    account_sequence = fields.Integer(string="Account Payable sequence" , default=10)

    sku_short = fields.Char(string="Sku Short", size=3)
