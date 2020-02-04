from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_sales_channel = fields.Boolean(related="partner_id.is_sales_channel")
    shipping_no = fields.Float(string="Shipping No",  )

    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    warehouse_id = fields.Many2one(comodel_name="stock.warehouse", string="Test Warehouse")

    # @api.constrains('shipping_no')
    # def _onchange_shipping_no(self):
    #     for rec in self:
    #         if rec.status == "" and rec.shipping_no == False:
    #             pass

