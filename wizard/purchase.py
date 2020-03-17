# -*- coding: utf-8 -*-
import logging
from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError
from odoo import api, fields, models


class PurchaseOrderWizard(models.TransientModel):
    _name = 'wizard.purchase.order'
    _description = 'Sent purchase order to magento'

    res_ids = fields.Many2many(comodel_name="purchase.order", )

    def action_apply(self):
        return {'type': 'ir.actions.act_window_close'}
