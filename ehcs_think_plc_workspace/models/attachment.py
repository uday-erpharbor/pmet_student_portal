from odoo import models, api

class Attachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, vals):
        attachment = super().create(vals)
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
                self.env['documents.document'].create({
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
                ('name', '=', 'Quotes'),
            ], limit=1)

            if customer_folder:
                # Link attachment to the folder in Documents
                self.env['documents.document'].create({
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
                ('customer_id', '=', site.id),
                ('name', '=', site.name),
            ], limit=1)

            if customer_folder:
                # Link attachment to the folder in Documents
                self.env['documents.document'].create({
                    'name': attachment.name,
                    'attachment_id': attachment.id,
                    'folder_id': customer_folder.id,
                    'owner_id': self.env.user.id,
                })

        return attachment
