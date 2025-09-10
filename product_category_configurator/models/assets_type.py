# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'thinkplc.assets.type'

    item_generate_fields_ids = fields.One2many(
        'item.generate.field', 'product_categery_id',
        'Item Generate Fields', copy=True
    )

    def action_import_options(self):
        """ Returns action window with Import Options Wizard'"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import Options'),
            'res_model': 'wiz.import.option',
            'view_mode': 'form',
            'view_id': self.env.ref('product_category_configurator.wiz_import_option_view').id,
            'target': 'new',
            'context': self.env.context,

        }
