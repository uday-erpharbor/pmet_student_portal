from odoo import models, fields, api


class ThinkPlcAsset(models.Model):
    _name = "thinkplc.assets"
    _description = "Customer Assets"
    _inherit = ['mail.thread']
    _rec_name = 'asset_type_id'

    name = fields.Char('Name', required=True,copy=False,readonly=True,default=lambda self: ('New'))
    asset_type_id = fields.Many2one('thinkplc.assets.type','Customer Asset Type', required=True)
    site_id = fields.Many2one('plc.sites', 'Site', required=True)
    related_asset_id = fields.Many2one('thinkplc.assets', 'Related Asset')
    simpro_asset_id = fields.Char('Simpro Id')
    machine_system_name = fields.Char('* MACHINE/SYSTEM NAME')
    assoc_prod_line = fields.Char('ASSOC. PRODUCTION LINE')
    plc_model = fields.Char('PLC MODEL')
    con_means = fields.Char('CONNECTION MEANS')
    plc_software_version_name = fields.Char('PLC SOFTWARE VERSION/NAME')
    program_password = fields.Char('PROGRAM PASSWORD')
    safety_password = fields.Char('SAFETY PASSWORD')

    @api.model
    def create(self,vals):        
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('thinkplc.assets') or _('New')
        res = super().create(vals)
        return res

class ThinkPlcAssetType(models.Model):
    _name = "thinkplc.assets.type"
    _inherit = ['mail.thread']

    name = fields.Char('Name')
    simpro_id = fields.Char('Simpro Id')
