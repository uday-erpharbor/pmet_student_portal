from odoo import models,fields,api, _
from datetime import datetime


class Customer(models.Model):
    _inherit = "res.partner"


    def _create_folder_of_customer(self, customer_id):
        Documnet = self.env['documents.document']
        current_year = datetime.now().year
        Customer_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : customer_id.name,
            'customer_id' : customer_id.id,
            })
        year_folder = self.env['documents.document'].search([('name','=',current_year), ('customer_id','=', customer_id.id), ('folder_id','=', customer_id.id)])
        if not year_folder:
            year_folder = Documnet.create({
                'type' : 'folder',
                'active' : True,
                'name' : current_year,
                'folder_id' : Customer_folder.id,
                'customer_id' : customer_id.id,
                })
        job_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Job Details',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        design_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Design',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        integration_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Integration',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        production_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Production',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        correspondencece_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Correspondence',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        Quotes_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Quotes',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        Sites_assets_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Site & Assets',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id,
            })
        Sites_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Sites',
            'folder_id' : Sites_assets_folder.id,
            'customer_id' : customer_id.id,
            })
        # assets_folder = Documnet.create({
        #     'type' : 'folder',
        #     'active' : True,
        #     'name' : 'Assets',
        #     'folder_id' : Sites_folder.id,
        #     'customer_id' : customer_id.id,
        #     })

    def _create_new_year_folder_of_customer(self, customer_id, main_folder_id):
        Documnet = self.env['documents.document']
        current_year = datetime.now().year
        year_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : current_year,
            'folder_id' : main_folder_id.id,
            'customer_id' : customer_id.id,
            })
        job_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Job Details',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        design_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Design',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        integration_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Integration',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        production_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Production',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        correspondencece_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Correspondence',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        Quotes_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Quotes',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id
            })
        Sites_assets_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Site & Assets',
            'folder_id' : year_folder.id,
            'customer_id' : customer_id.id,
            })
        Sites_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Sites',
            'folder_id' : Sites_assets_folder.id,
            'customer_id' : customer_id.id,
            })
        # assets_folder = Documnet.create({
        #     'type' : 'folder',
        #     'active' : True,
        #     'name' : 'Assets',
        #     'folder_id' : Sites_folder.id,
        #     'customer_id' : customer_id.id,
        #     })

    @api.model
    def create(self, vals):
        res = super(Customer, self).create(vals)  
        if vals.get('type'):
            if vals.get('type') not in ['invoice','delivery','followup','other']: 
                res._create_folder_of_customer(res)
        return res
