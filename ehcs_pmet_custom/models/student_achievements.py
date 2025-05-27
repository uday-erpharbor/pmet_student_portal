from odoo import models,fields


class Achievements(models.Model):
	_name ="student.achievements"
	_description= "Student Achievements"

	name = fields.Char('Achievements', required=True)
