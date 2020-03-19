from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char(string="Internal Reference", readonly=True)
    supplier_no = fields.Char(string="Supplier No", readonly=True)
    is_sales_channel = fields.Boolean(string="Sales Channel", )
    liability_account_id = fields.Many2one(comodel_name="account.account", string="Liability Account")
    is_customer = fields.Boolean(string="Customer", )
    is_vendor = fields.Boolean(string="vendor", )
    is_commission = fields.Boolean(string="Commission", )
    rate = fields.Float(string="Rate", )
    is_date = fields.Boolean(string="With date")
    start_date = fields.Date(string="Start Date", required=False, )
    end_date = fields.Date(string="End Date", required=False, )
    partner_related_ids = fields.One2many(comodel_name="partner.related.partners", inverse_name="partner_id",
                                          string="Related Partners", )
    products_related_ids = fields.One2many(comodel_name="partner.related.products", inverse_name="partner_id",
                                           string="Related Products", )
    cheque_related_ids = fields.One2many(comodel_name="partner.related.cheque", inverse_name="partner_id",
                                         string="Related Cheques", track_visibility='always')
    channel_type = fields.Selection(string="Type", selection=[('1', 'Company'),
                                                              ('2', 'Celebrity'),
                                                              ('3', 'Makeup Artist'),
                                                              ], )
    order_all = fields.Float(string="Order All", compute="_compute_orders")
    order_paid = fields.Float(string="Order Paid", )
    order_pending = fields.Float(string="Order Pending")
    balance_all = fields.Float(string="Balance All", )
    balance_paid = fields.Float(string="Balance Paid", )
    balance_pending = fields.Float(string="Balance Pending", )
    sale_order_line_ids = fields.One2many(comodel_name="sale.order.line", inverse_name="celebrity_id", )

    contract_period = fields.Integer(string="Contract Period", size=2)
    company_percentage = fields.Integer(string="Company Percentage", size=2)
    po_sample = fields.Integer(string="Purchase Order Samples - per product", size=2)
    sample_marketing = fields.Integer(string="1st samples for marketing - per product", size=3)
    order_prepare_time = fields.Integer(string="order preparation time  - with days", size=3)
    return_before_expiry = fields.Integer(string="return before expiry - with days", size=3)
    commercial_reg = fields.Char(string="Commercial REG")

    vendor_product_ids = fields.One2many(comodel_name="product.supplierinfo", inverse_name="name",
                                         string="Vendor related Product")

    products_count = fields.Integer(string="products count",compute="_compute_products_count")

    @api.depends('vendor_product_ids')
    def _compute_products_count(self):
        for rec in self:
            products = []
            for line in rec.vendor_product_ids:
                if line.name == rec:
                    products.append(line.product_tmpl_id.id)
            rec.products_count = len(products)

    def action_view_products(self):
        for rec in self:
            products = []
            action = self.env.ref('sale.product_template_action').read()[0]
            for line in rec.vendor_product_ids:
                if line.name == rec:
                    products.append(line.product_tmpl_id.id)
            action['domain'] = [('id', 'in', products)]
            return action

    @api.depends('sale_order_line_ids')
    def _compute_orders(self):

        for rec in self:
            all = paid = 0
            for line in rec.sale_order_line_ids:
                if line.order_id.state not in ['draft', 'cancel', 'close']:
                    all += line.price_subtotal
                    if line.invoice_status == 'invoiced':
                        paid += line.price_subtotal
            rec.order_all = all
            rec.order_paid = paid
            rec.order_pending = rec.order_all - rec.order_paid

    @api.constrains('partner_related_ids', 'partner_related_ids.related_partner_id')
    def _constrains_partner_related_ids(self):
        for rec in self:
            for line in rec.partner_related_ids:
                if line.related_partner_id == rec:
                    raise ValidationError(_("Related Partner Can not be Current Contact"))

    @api.onchange('is_customer')
    def _onchange_is_customer(self):
        for rec in self:
            if rec.is_customer:
                rec.customer_rank += 1
            else:
                rec.customer_rank -= 1

    @api.onchange('is_vendor')
    def _onchange_is_vendor(self):
        for rec in self:
            if rec.is_vendor:
                rec.supplier_rank += 1
            else:
                rec.supplier_rank -= 1

    @api.onchange('channel_type')
    @api.constrains('channel_type')
    def _constrains_channel_type(self):
        for rec in self:
            if not rec.env.user.has_group('sales_team.group_sale_manager'):
                if rec.channel_type == '1':
                    raise ValidationError(_(" Unable to Save Type With Company. Please contact your Administrator"))
            # if rec.channel_type == '2' or rec.channel_type == '3' and rec.is_sales_channel == False:
            #     raise ValidationError(_("Contact must be sales channel"))

    @api.model
    def create(self, values):
        res = super(ResPartner, self).create(values)
        if self.env.user.company_id:
            sequence = self.env.user.company_id.partner_count
            seq = sequence + 1
            values['code'] = 'CT' + str(seq).zfill(4)
            if 'supplier_rank' in values:
                supplier_no = self.env['ir.sequence'].next_by_code('res.partner') or '/'
                self.supplier_no = str(supplier_no)
                res['supplier_no'] = str(supplier_no)
            self.env.user.company_id.partner_count += 1
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        super(ResPartner, self).name_search(name)
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', '|', ('mobile', operator, name), ('email', operator, name),
                      ('name', operator, name), ('phone', operator, name), ('code', operator, name)]
        results = self.search(domain + args, limit=limit)
        return results.name_get()


class RelatedPartner(models.Model):
    _name = 'partner.related.partners'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    related_partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    commission = fields.Float(string="Commission", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    # @api.onchange('related_partner_id')
    # def _onchange_related_partner_id(self):
    #     for rec in self:
    #         partner_id = rec.partner_id.id
    #         print(">>>>>>>part<<<<",partner_id)
    #         res = {}
    #         if partner_id:
    #             res['domain'] = {
    #                 'related_partner_id': [('id', '!=', partner_id), ('is_sales_channel', '=', True),
    #                                        ('channel_type', '!=', 'company')]}
    #         return res


class RelatedProducts(models.Model):
    _name = 'partner.related.products'

    partner_id = fields.Many2one(comodel_name="res.partner", )
    product_id = fields.Many2one(comodel_name="product.template", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", )
    is_active = fields.Boolean(string="Active", default=True)


class RelatedPartnerCheque(models.Model):
    _name = 'partner.related.cheque'

    partner_id = fields.Many2one(comodel_name="res.partner", track_visibility='onchange')
    value = fields.Float(string="Value", track_visibility='onchange')
    date = fields.Date(string="Date", track_visibility='onchange')
    today = fields.Date(string="Date", required=True, default=date.today(), track_visibility='onchange', readonly=True)

