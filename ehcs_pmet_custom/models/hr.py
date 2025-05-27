from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime,date


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    student_name = fields.Char('Name')
    reference = fields.Char(string= "Order Reference", required=True, copy=False, readonly=True, default=lambda self: ('New'))
    is_pmet_studet_record = fields.Boolean()
    roll_number = fields.Integer(string="Roll Number",default=0)
    birth_date = fields.Date(string="Date of Birth", required=True,default=datetime.now())
    age = fields.Integer('Age', compute='_compute_age')
    contact_ralation = fields.Selection([("father","Father"),("mother","Mother"),("brother","Brother"),('other','Other')],string="Student Relation")
    academic_ids = fields.One2many('academic.info.line', 'acedemic_id', 'Academic Line')
    # expence_ids = fields.One2many('student.expence', 'acedemic_id', 'Expence')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            record.age = False
            if record.birth_date:
                today = date.today()
                delta = relativedelta(today, record.birth_date)
                record.age = delta.years

    @api.model
    def create(self,vals):
        if vals.get('reference',_('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('pmet.student') or _('New')
        res = super(HrEmployee, self).create(vals)
        return res


class InfoLine(models.Model):
    _name = "academic.info.line"
    _description = 'Academic Information'
    _rec_name = 'course_id'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    name = fields.Char('Name of Course')
    course_id = fields.Many2one('course.course','Name of Course')
    percentage = fields.Float('Percentage')
    year = fields.Integer('Year Of Passing')
    board_name = fields.Char("Board/ University Name")
    state_id = fields.Many2one('res.country.state','State')
    trail = fields.Selection([("first","First"),("second","Second"),("third","Third"),('more','More Then Three')],string="Try")
    sheet_number = fields.Char('Sheet Number')
    document = fields.Image(string="Upload Document", compute_sudo=True)
    acedemic_id = fields.Many2one('hr.employee','Student',domain="[('is_pmet_studet_record','=',True)]")
