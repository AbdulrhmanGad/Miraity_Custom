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
    examination_warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="ْxamination  Warehouse",
                                   config_parameter='base_setup.examination_warehouse_id', )
    outsource_warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse",
                                   config_parameter='base_setup.outsource_warehouse_id', )

    call_center_token = fields.Char(string="Call Center Token Key", config_parameter='base_setup.call_center_token', )
    call_center_token_len = fields.Integer(string="WH Token Length",)
    call_center_user_id = fields.Many2one(comodel_name="res.users", config_parameter='base_setup.call_center_user_id', )
    helpdesk_team_id = fields.Many2one(comodel_name="helpdesk.team", config_parameter='base_setup.helpdesk_team_id', )

    warehouse_token = fields.Char(string="WH Token Key", config_parameter='base_setup.warehouse_token', )
    warehouse_token_len = fields.Integer(string="WH Token Length",)
    wh_user_id = fields.Many2one(comodel_name="res.users", config_parameter='base_setup.wh_user_id', )

    magento_token = fields.Char(string="Magento Token Key", config_parameter='base_setup.magento_token', )
    magento_token_len = fields.Integer(string="WH Token Length",)
    magento_user_id = fields.Many2one(comodel_name="res.users", config_parameter='base_setup.magento_user_id', )
    magento_helpdesk_team_id = fields.Many2one(comodel_name="helpdesk.team", config_parameter='base_setup.magento_helpdesk_team_id', )


    short_description = fields.Char(string="Short Description", size=1, config_parameter='base_setup.short_description', )

    def generate_call_center_token(self):
            self.env['ir.config_parameter'].sudo().set_param('base_setup.call_center_token', secrets.token_hex(20))

    def generate_warehouse_token(self):
            self.env['ir.config_parameter'].sudo().set_param('base_setup.warehouse_token', secrets.token_hex(20))

    def generate_magento_token(self):
            self.env['ir.config_parameter'].sudo().set_param('base_setup.magento_token', secrets.token_hex(20))
