# from odoo import models,fields


# class Expense(models.Model):
#     _name ="student.expence"
#     _description = "Couse information"
#     _inherit = ['mail.thread.cc', 'mail.activity.mixin']

#     name = fields.Char('Expence', required=True, tracking=True)
#     price = fields.Float('Total Expence')
#     receipt = fields.Image('Upload Receipt')
#     acedemic_id = fields.Many2one('hr.employee','Student', domain="[('is_pmet_studet_record','=',True)]")
