from odoo import models, api

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        attachment = super().create(vals)
        document_model = self.env['documents.document']
        if attachment.res_model == 'res.partner' and attachment.res_id:
            partner = self.env['res.partner'].browse(attachment.res_id)
            # Find the main folder for the customer
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', partner.id),
                ('name', '=', partner.name),
            ], limit=1)
            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        if attachment.res_model == 'sale.order' and attachment.res_id:
            so = self.env['sale.order'].browse(attachment.res_id)
            # Find the main folder for the customer
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', so.partner_id.id),
                ('name', '=', so.display_name),
            ], limit=1)
            print('\n\n so.display_name',so.display_name)
            print('\n\n customer_folder',customer_folder)
            print('\n\n customer_folder',customer_folder)
            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        if attachment.res_model == 'plc.sites' and attachment.res_id:
            site = self.env['plc.sites'].browse(attachment.res_id)
            # Find the main folder for the customer(sites)
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', site.customer_id.id),
                ('name', '=', site.name),
            ], limit=1)

            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        if attachment.res_model == 'thinkplc.assets' and attachment.res_id:
            task = self.env['thinkplc.assets'].browse(attachment.res_id)
            # Find the main folder for the customer(sites)
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', task.site_id.customer_id.id),
                ('name', '=', 'Assets'),
            ], limit=1)
            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        if attachment.res_model == 'project.project' and attachment.res_id:
            project = self.env['project.project'].browse(attachment.res_id)
            customer_id = False
            if project:
                if project.is_customize_proj_create:
                    customer_id = project.sale_partner_id.id
                if project.partner_id:
                    customer_id = project.partner_id.id
            # Find the main folder for the customer(sites)
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', customer_id),
                ('name', '=', project.name),
            ], limit=1)
            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })
        if attachment.res_model == 'project.task' and attachment.res_id:
            project = self.env['project.task'].browse(attachment.res_id)
            if project.project_id:
                if project.project_id.is_customize_proj_create:
                    customer_id = project.project_id.sale_partner_id.id
                if project.project_id.partner_id:
                    customer_id = project.project_id.partner_id.id
            # Find the main folder for the customer(sites)
            customer_folder = self.env['documents.document'].search([
                ('type', '=', 'folder'),
                ('customer_id', '=', customer_id),
                ('name', '=', project.name),
            ], limit=1)
            
            if customer_folder:
                # Link attachment to the folder in Documents
                new_doc = document_model.create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        return attachment
