# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    acc_receive_prefix = fields.Integer(string="Account Receivable Prefix",
                                      config_parameter='base_setup.acc_receive_prefix')
    acc_payable_prefix = fields.Integer(string="Account Payable Prefix",
                                      config_parameter='base_setup.acc_payable_prefix')
