from odoo import models, fields, api


class ThinkPlcAsset(models.Model):
    _name = "thinkplc.assets"
    _description = "Customer Assets"
    _inherit = ['mail.thread']
    _rec_name = 'asset_type_id'

    name = fields.Char('Customer Asset Type')
    asset_type_id = fields.Many2one('thinkplc.assets.type','Customer Asset Type')
    site_id = fields.Many2one('plc.sites', 'Site')
    related_asset_id = fields.Many2one('thinkplc.assets', 'Related Asset')
    simpro_asset_id = fields.Char('Simpro Id')
    machine_system_name = fields.Char('* MACHINE/SYSTEM NAME')
    assoc_prod_line = fields.Char('ASSOC. PRODUCTION LINE')

    # Voltage Selection
    voltage = fields.Selection([
        ('Not Selected', 'Not Selected'),
        ('480VAC', '480VAC'),
        ('240VAC', '240VAC'),
        ('208VAC', '208VAC'),
        ('120VAC', '120VAC'),
        ('24VDC', '24VDC'),
        ('OTHER', 'OTHER'),
        ('N/A', 'N/A'),
    ], string="* VOLTAGE")

    # PLC Manufacturer Selection
    plc_manufacturer = fields.Selection([
        ('SIEMENS', 'SIEMENS'),
        ('ALLEN BRADLEY', 'ALLEN BRADLEY'),
        ('OMRON', 'OMRON'),
        ('MITSUBISHI', 'MITSUBISHI'),
        ('AUTOMATION DIRECT - DIRECT LOGIX', 'AUTOMATION DIRECT - DIRECT LOGIX'),
        ('UNITRONICS', 'UNITRONICS'),
        ('PHOENIX CONTACT', 'PHOENIX CONTACT'),
        ('EXOR', 'EXOR'),
        ('GE', 'GE'),
        ('EMERSON', 'EMERSON'),
        ('OTHER', 'OTHER'),
        ('N/A', 'N/A'),
    ], string="* PLC MANUFACTURE")

    # PLC Development Software
    plc_dev_software = fields.Selection([
        ('STEP7 Simatic Manager', 'STEP7 Simatic Manager'),
        ('STEP5', 'STEP5'),
        ('TIA Portal', 'TIA Portal'),
        ('RSlogix 5', 'RSlogix 5'),
        ('RSlogix 500', 'RSlogix 500'),
        ('RSlogix 5000', 'RSlogix 5000'),
        ('Studio 5000', 'Studio 5000'),
        ('Connected Component Workbench', 'Connected Component Workbench'),
        ('GX developer', 'GX developer'),
    ], string="PLC DEVELOPMENT SOFTWARE")

    # Fieldbus Communications
    fieldbus_comms = fields.Selection([
        ('ETHERNET IP', 'ETHERNET IP'),
        ('PROFINET', 'PROFINET'),
        ('MODBUS TCP', 'MODBUS TCP'),
        ('PROFIBUS', 'PROFIBUS'),
        ('DEVICENET', 'DEVICENET'),
        ('CONTROLNET', 'CONTROLNET'),
        ('RS232', 'RS232'),
        ('MODBUS 485', 'MODBUS 485'),
        ('OTHER', 'OTHER'),
        ('N/A', 'N/A'),
    ], string="* FIELD BUS COMMS")

    safety_cpu = fields.Selection([
        ('YES','YES'),('NO','NO')
        ], string='SAFETY CPU?')

    redu_controllers = fields.Selection([
        ('YES','YES'),('NO','NO')
        ], string='REDUNDANT CONTROLLERS?')

    plc_model = fields.Char('PLC MODEL')
    con_means = fields.Char('CONNECTION MEANS')
    plc_software_version_name = fields.Char('PLC SOFTWARE VERSION/NAME')
    program_password = fields.Char('PROGRAM PASSWORD')
    safety_password = fields.Char('SAFETY PASSWORD')


class ThinkPlcAssetType(models.Model):
    _name = "thinkplc.assets.type"

    name = fields.Char('Name', required=True)
    simpro_id = fields.Char('Simpro Id')
