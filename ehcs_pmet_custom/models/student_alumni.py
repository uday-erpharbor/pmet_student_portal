from odoo import models,fields


class Course(models.Model):
	_name ="student.alumni"
	_description = "Student Alumni"
	_inherit = ['mail.thread.cc', 'mail.activity.mixin']
	_rec_name = 'student_id'

	name = fields.Char('Name', tracking=True)
	student_id = fields.Many2one('hr.employee','Student', domain="[('is_pmet_studet_record','=',True)]")
	current_position_id = fields.Many2one('hr.job','Current Position')
	city = fields.Char('Which City')
	achievements_ids = fields.Many2many(comodel_name="student.achievements",
								        relation="stud_achivmnet",
								        column1="stud_id",
								        column2="achivement_id",
								        string="Achievements",)
								
