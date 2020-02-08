# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_account_prefix = fields.Boolean(string="Enable Prefix",config_parameter='base_setup.is_prefix',  default_model="res.company")

    account_payable_id = fields.Many2one(comodel_name="account.account", string="Account Payable",
                                        config_parameter='base_setup.account_payable_id', )
    account_receive_id = fields.Many2one(comodel_name="account.account", string="Account Receive",
                                        config_parameter='base_setup.account_receive_id', )
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse",
                                   config_parameter='base_setup.warehouse_id', default_model="sale.order")
    token_key = fields.Char(string="Token Key", config_parameter='base_setup.token', )