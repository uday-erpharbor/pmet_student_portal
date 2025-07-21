from odoo import models,fields


class ThinkPcSites(models.Model):
	_name ="plc.sites"
	_description = "Think Sites"
	_rec_name = 'name'

	name = fields.Char('Sites Name')
	zone = fields.Char('Zone')
	city = fields.Char('City')
	street_address = fields.Text('Street Address')
	zip = fields.Char('Zip Code')
	state_id = fields.Many2one('res.country.state', 'State')
	country_id = fields.Many2one('res.country', 'Country')
	billing_address = fields.Text('Billing Address')
	billing_contact = fields.Char('Billing Contact')
	billing_city = fields.Char('Billing City')
	billing_state_id = fields.Many2one('res.country.state', 'Billing State')
	billing_zip_code = fields.Char('Billing ZIP Code')
	siteid = fields.Integer('Site ID')
	customer_id = fields.Many2one('res.partner','Customer', domain=[('x_simpro_types', '=', 'customer')])
	contact_id = fields.Many2one('res.partner','Customer', domain=[('x_simpro_types', '=', 'contact')])
