from odoo import models,fields


class ThinkPcSites(models.Model):
	_name ="product.manufacturer"
	_description = 'Manufacturer'

	name = fields.Char('Manufacturer Name')
	simpro_id = fields.Char('Simpro Id')
