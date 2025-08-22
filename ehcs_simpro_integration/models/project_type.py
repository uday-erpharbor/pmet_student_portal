from odoo import models,fields, api
from odoo.exceptions import ValidationError
import requests

class ProjectType(models.Model):
    _name ="think.project.type"
    _description = "Project Type "

    name = fields.Char('Type', required=True)

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Project type already exists!')
            ]
