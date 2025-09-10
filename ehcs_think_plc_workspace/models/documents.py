from odoo import models,fields,api, _


class Document(models.Model):
    _inherit = "documents.document"

    customer_id = fields.Many2one('res.partner','Customer Id')
 
    @api.model
    def create(self, vals):
        res = super(Document, self).create(vals)
        
        return res
