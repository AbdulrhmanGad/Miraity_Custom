# -*- coding: utf-8 -*-
from odoo import api, fields, models
import secrets


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_account_prefix = fields.Boolean(string="Enable Prefix",config_parameter='base_setup.is_prefix',  default_model="res.company")

    account_payable_id = fields.Many2one(comodel_name="account.account", string="Account Payable",
                                        config_parameter='base_setup.account_payable_id', )
    account_receive_id = fields.Many2one(comodel_name="account.account", string="Account Receive",
                                        config_parameter='base_setup.account_receive_id', )
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse",
                                   config_parameter='base_setup.warehouse_id', default_model="sale.order")
    sample_warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse",
                                   config_parameter='base_setup.sample_warehouse_id', )
    outsource_warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse",
                                   config_parameter='base_setup.outsource_warehouse_id', )
    token_key = fields.Char(string="Token Key", config_parameter='base_setup.token', )
    short_description = fields.Char(string="Short Description", config_parameter='base_setup.short_description', )
    call_center_token = fields.Char(string="Call Center Token Key", config_parameter='base_setup.call_center_token', )

    def generate_call_center_token(self):
        for rec in self:
            self.env['ir.config_parameter'].sudo().set_param('base_setup.call_center_token', secrets.token_hex(20))
