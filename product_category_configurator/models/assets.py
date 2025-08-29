# -*- coding: utf-8 -*-
from odoo.fields import Command
from odoo import api, fields, models


class ThinkPcSites(models.Model):
    _inherit = 'thinkplc.assets'

    item_generate_field_value_ids = fields.One2many(
        'item.generate.field.value', 'product_id', 'Item Generate Field Value',
        copy=True
    )
    is_category_configurable = fields.Boolean(
        "Is a configurable category", compute='_compute_has_configurable'
    )
    item_description = fields.Text("Description", compute="_compute_item")

    # @api.onchange('asset_type_id')
    # def _onchange_on_asset_type_id(self):
    #     print("\n\n dddd")
    #     for rec in self:
    #         rec.item_generate_field_value_ids = False

    def _compute_has_configurable(self):
        """Show/Hide category configurator button"""
        self.is_category_configurable = False
        for product in self:
            product.is_category_configurable = product and product.id and product.asset_type_id

    @api.depends('name', 'item_generate_field_value_ids', 'item_generate_field_value_ids.name')
    def _compute_item(self):
        for product in self:
            item_description = ''
            if product and product.item_generate_field_value_ids:
                dynamic_desc = []
                item_generate_field_values = product.item_generate_field_value_ids
                for line in item_generate_field_values.filtered(lambda l: l.item_id.title_sequence > 0).sorted(
                        lambda l: l.item_id.title_sequence):
                    desc_value = ''
                    if line.field_type == 'checkbox':
                        if line.name == 'True':
                            desc_value = line.item_id.name
                    else:
                        desc_value = line.name
                    if desc_value:
                        dynamic_desc.append(desc_value)
                product.name = ' '.join(dynamic_desc) + ' ' + product.asset_type_id.name

                # .filtered(lambda l: l.item_id.desc_sequence > 0)
                item_description = product.name + '\n' + '\n'.join(
                    f"{line.item_id.name} : {line.name}" for line in item_generate_field_values.sorted(
                        lambda l: l.item_id.desc_sequence)) or ''
            product.item_description = item_description
        return True

    def copy(self, default=None):
        "Copy the item_generate_field_value_ids field"
        new_product = super().copy(default=default)
        for product in self:
            new_item_values = [
                Command.create(line_vals)
                for line_vals in product.item_generate_field_value_ids.copy_data()
            ]
            new_product.write({'item_generate_field_value_ids': new_item_values})
        return new_product


class ItemGenerateFieldValue(models.Model):
    _name = "item.generate.field.value"
    _description = 'Item Generate Field Value'

    name = fields.Char("Value")
    item_id = fields.Many2one("item.generate.field", "Item Generate Field")
    product_id = fields.Many2one("thinkplc.assets", "Product", copy=False)
    field_type = fields.Selection(related='item_id.field_type', store=True)

    @api.depends('item_id')
    def _compute_display_name(self):
        for value in self:
            value.display_name = f"{value.item_id.name}: {value.name}"
