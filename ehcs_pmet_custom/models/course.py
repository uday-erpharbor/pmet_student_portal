from odoo import models,fields


class Course(models.Model):
	_name ="course.course"
	_description = "Couse information"
	_inherit = ['mail.thread.cc', 'mail.activity.mixin']

	name = fields.Char('Course', required=True, tracking=True)
	partner_id = fields.Many2one('res.partner',"partner")
