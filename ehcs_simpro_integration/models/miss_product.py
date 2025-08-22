from odoo import models,fields


class ThinkPcSites(models.Model):
    _name ="product.miss.records"

    name = fields.Char('Name')
    simpro_id = fields.Char('Simpro Id')
    x_simpro_types = fields.Selection([('vendore','Vendors'), ('contact','Contact'), ('customer','Customer'), ('product','Product'), ('contractor','Contractor'), ('site','Sites'), ('bom','Bom')], string='Type')
    product_price = fields.Float('Price')
    email = fields.Float('Email')
    site_zip_code = fields.Char('Zip Code')
    reason = fields.Char('Reason')
