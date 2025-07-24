from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    production_url = fields.Char("Production URL",config_parameter=
        'ehcs_n8n_configuration.production_url')
