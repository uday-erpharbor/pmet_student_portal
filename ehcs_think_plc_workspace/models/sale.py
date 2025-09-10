from odoo import models,fields,api, _
from datetime import datetime


class Sale(models.Model):
    _inherit = "sale.order"


    @api.model
    def create(self, vals):
        res = super(Sale, self).create(vals)
        current_year = datetime.now().year
        document = self.env['documents.document']
        customer = self.env['res.partner'].search([('id','=',vals.get('partner_id'))], limit=1)
        find_folder = self.env['documents.document'].search([('name','=',customer.name), ('customer_id','=', customer.id), ('active','=', True)])
        if not find_folder:
            customer._create_folder_of_customer(customer) 
        year_folder = self.env['documents.document'].search([('customer_id','=', vals.get('partner_id')),('name','=',current_year)])
        if find_folder and not year_folder:
            customer._create_new_year_folder_of_customer(customer, find_folder)    
        quote_folder = self.env['documents.document'].search([('name','=','Quotes'), ('customer_id','=', vals.get('partner_id')), ('folder_id','=',year_folder.id)], limit=1)  
        if quote_folder:
            value = {
                'name' : res.display_name,
                'type' : 'folder',
                'active' : True,
                'folder_id' : quote_folder.id,
                'customer_id' : vals.get('partner_id'),
                }
            new_sale_folder = document.create(value)
        return res