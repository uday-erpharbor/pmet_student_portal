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

    # @api.model
    # def get_values(self):
    #     # Retrieve the stored global field IDs from ir.config_parameter and assign them to the field
    #     res = super(ResConfigSettings, self).get_values()

    #     # Retrieve the stored value from the ir.config_parameter, if it exists
    #     stored_global_field_ids = self.env['ir.config_parameter'].sudo().get_param('ehcs_global_search.global_field_ids', '[]')

    #     try:
    #         # Deserialize the stored JSON string into a list of field IDs
    #         field_ids = json.loads(stored_global_field_ids)
    #         # Retrieve the Many2many records by their IDs
    #         global_field_records = self.env['ir.model.fields'].browse(field_ids)
    #         res['global_field_ids'] = global_field_records
    #     except (ValueError, TypeError):
    #         # In case of any error in deserialization, set to empty
    #         res['global_field_ids'] = self.global_field_ids

    #     return res

    # def set_values(self):
    #     super(ResConfigSettings, self).set_values()

    #     # Serialize the global_field_ids to a list of IDs (as a JSON string)
    #     if self.global_field_ids:
    #         field_ids = self.global_field_ids.ids
    #         # Serialize the list of IDs to a JSON string
    #         self.env['ir.config_parameter'].set_param("ehcs_global_search.global_field_ids", json.dumps(field_ids))
    #     else:
    #         # If no fields are selected, store None or an empty list
    #         self.env['ir.config_parameter'].set_param("ehcs_global_search.global_field_ids", '[]')
