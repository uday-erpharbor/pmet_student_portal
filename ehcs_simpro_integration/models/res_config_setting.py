from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    company_url = fields.Char('Company Url', config_parameter='ehcs_simpro_integration.company_url')
    company = fields.Integer('Company Id', config_parameter='ehcs_simpro_integration.company')
    access_token = fields.Char('Access Token', config_parameter='ehcs_simpro_integration.access_token')
    page_size = fields.Integer('How Many Records You Will Get(0-250)', config_parameter='ehcs_simpro_integration.page_size')
    page = fields.Integer('Page Number', config_parameter='ehcs_simpro_integration.page')


class Company(models.Model):
    _inherit = 'res.company'

    page_number = fields.Integer('Page Number')
