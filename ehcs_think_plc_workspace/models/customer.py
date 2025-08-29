from odoo import models,fields,api, _


class Customer(models.Model):
    _inherit = "res.partner"


    def _create_folder_of_customer(self, customer_id):
        Documnet = self.env['documents.document']
        Customer_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : customer_id.name,
            'customer_id' : customer_id.id,
            })
        Job_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Job',
            'folder_id' : Customer_folder.id,
            'customer_id' : customer_id.id,
            })
        Quotes_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Quotes',
            'folder_id' : Customer_folder.id,
            'customer_id' : customer_id.id
            })
        Sites_assets_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Site & Assets',
            'folder_id' : Customer_folder.id,
            'customer_id' : customer_id.id,
            })
        Sites_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Sites',
            'folder_id' : Sites_assets_folder.id,
            'customer_id' : customer_id.id,
            })
        assets_folder = Documnet.create({
            'type' : 'folder',
            'active' : True,
            'name' : 'Assets',
            'folder_id' : Sites_assets_folder.id,
            'customer_id' : customer_id.id,
            })

    @api.model
    def create(self, vals):
        res = super(Customer, self).create(vals)  
        res._create_folder_of_customer(res)
        return res
