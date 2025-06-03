# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    global_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        string="Global Fields",
        domain=[('model_id.model', '=', 'sale.order')],
    )

    global_inv_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        string="Global Fields",
        domain=[('model_id.model', '=', 'account.move')],
    )

    global_po_field_ids = fields.Many2many(
        "ir.model.fields",
        "gloabl_ir_fields_rel",
        string="Global Fields",
        domain=[('model_id.model', '=', 'purchase.order')],
    )
