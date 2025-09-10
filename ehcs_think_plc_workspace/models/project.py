from odoo import models,fields,api, _
from datetime import datetime


class Project(models.Model):
    _inherit = "project.project"

    def _create_folders(self,vals, ids):
        if vals.get('sale_id') and vals.get('sale_partner_id'):
            document = self.env['documents.document']
            current_year = datetime.now().year
            
            customer = self.env['res.partner'].search([('id','=',vals.get('sale_partner_id'))], limit=1)
            find_folder = self.env['documents.document'].search([('name','=',customer.name), ('customer_id','=', customer.id), ('active','=', True)])   
            if not find_folder:
                customer._create_folder_of_customer(customer)
            
            year_folder = self.env['documents.document'].search([('customer_id','=', vals.get('sale_partner_id')),('name','=',current_year)])
            if find_folder and not year_folder:
                customer._create_new_year_folder_of_customer(customer,find_folder)
            find_job_folder = self.env['documents.document'].search([('folder_id','=', year_folder.id),('name','=','Job Details'), ('customer_id','=',vals.get('sale_partner_id')), ('active','=',True), ('folder_id','=',year_folder.id)], limit=1)
            
            if find_job_folder:
                project_folder = {
                    'name': self.name,
                    'type': 'folder',
                    'active' : True,
                    'customer_id' : vals.get('sale_partner_id'),
                    'folder_id' : find_job_folder.id,
                }
                new_project_folder = document.create(project_folder)

        if vals.get('partner_id') and vals.get('sale_line_id'):
            document = self.env['documents.document']
            current_year = datetime.now().year

            customer = self.env['res.partner'].search([('id','=',vals.get('partner_id'))], limit=1)
            find_folder = self.env['documents.document'].search([('name','=',customer.name), ('customer_id','=', customer.id), ('active','=', True)])   
            if not find_folder:
                customer._create_folder_of_customer(customer)

            year_folder = self.env['documents.document'].search([('customer_id','=', vals.get('partner_id')),('name','=',current_year)])
            if find_folder and not year_folder:
                customer._create_new_year_folder_of_customer(customer,find_folder)

            find_job_folder = self.env['documents.document'].search([('folder_id','=', year_folder.id),('name','=','Job Details'), ('customer_id','=',vals.get('partner_id')), ('active','=',True), ('folder_id','=',year_folder.id)], limit=1)

            if find_job_folder:
                project_folder = {
                    'name': self.name,
                    'type': 'folder',
                    'active' : True,
                    'customer_id' : vals.get('partner_id'),
                    'folder_id' : find_job_folder.id,
                }
                new_project_folder = document.create(project_folder)

            
    @api.model
    def create(self, vals):
        res = super(Project, self).create(vals)  
        res._create_folders(vals, res.id)
        return res


class ProjectTask(models.Model):
    _inherit = "project.task"


    def _create_folders_of_task(self,vals):
      if vals.get('project_id'):
        document = self.env['documents.document']
        project = self.env['project.project'].search([('id','=',vals.get('project_id'))], limit=1)
        project_folder = self.env['documents.document'].search([('name','=',project.name)], limit=1)
        customer_id = False
        if project.is_customize_proj_create:
            customer_id = project.sale_partner_id.id
        if project.partner_id:
            customer_id = project.partner_id.id
        if project_folder:
            value = {
                'name' : vals.get('name'),
                'active' : True,
                'folder_id' : project_folder.id,
                'customer_id' : customer_id,
                'type': 'folder'
                }
            new_task_folder = document.create(value)

    @api.model
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        res._create_folders_of_task(vals)
        return res
