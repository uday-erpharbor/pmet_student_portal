from odoo import fields, models, api
# import json


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    global_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        related='company_id.global_field_ids',
        string="Global Fields",
        help="Fields that search in search view.",
        domain=[('model_id.model', '=', 'sale.order')],
    )

    global_inv_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        related='company_id.global_inv_field_ids',
        string="Global Fields",
        help="Fields that search in search view.",
        domain=[('model_id.model', '=', 'account.move')],
    )

    global_po_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        related='company_id.global_po_field_ids',
        string="Global Fields",
        help="Fields that search in search view.",
        domain=[('model_id.model', '=', 'purchase.order')],
    )
