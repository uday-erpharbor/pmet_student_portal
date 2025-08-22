from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    x_studio_job_project_type = fields.Selection([
        ('SE', 'SE Service'),
        ('PR', 'PR Electro/Mech Automation Project'),
        ('PA', 'PA Parts Only'),
        ('BP', 'BP Build to print'),
        ('EL', 'EL Automation Project - Electrical'),
        ('ME', 'ME Automation Project - Mechanical'),
        ('TR', 'TR Training'),
        ('WA', 'WA Warranty repair'),
    ], string='Job / Project Type')
    think_job_number = fields.Char('Job Number', readonly=True)
