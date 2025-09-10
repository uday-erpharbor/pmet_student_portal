# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ItemGenerateField(models.Model):
    _name = "item.generate.field"
    _description = 'Item Generate Field'

    name = fields.Char(string="Label", required=True)
    sequence = fields.Integer(default=1)
    field_type = fields.Selection([
        ('short', 'Short (25 Char Max)'),
        ('medium', 'Medium (40 Char Max)'),
        ('long', 'Long (No Char Limits)'),
        ('integer', 'Integer'),
        ('checkbox', 'Checkbox'),
        ('option', 'Option'),
        ('date', 'Date'),
    ], string="Field Type", default="short", required=True)
    length = fields.Integer(string="Character Length", default=25, compute='_compute_length')
    is_required = fields.Boolean(string="Mandatory",
        help="If field selected field will be mandatory in configurator")
    options_ids = fields.One2many(
        'item.generate.field.selection', 'item_id', 'Item Generate Fields Selection', copy=True)
    product_categery_id = fields.Many2one(
        "thinkplc.assets.type", string="Product Category")
    title_sequence = fields.Integer(
        "Title Sequence", default=0,
        help="User can change the sequence of the product title"
    )
    desc_sequence = fields.Integer(
        "Description Sequence", default=0,
        help="User can change sequence of product description")

    def action_configure_options(self):
        self.ensure_one()
        return {
            'name': _("Configure Option(s)"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'item.generate.field',
            'target': 'new',
        }

#    @api.model
#    def get_next_title_sequence(self):
#        """Get the next sequence number"""
#        last_record = self.search([], order="title_sequence desc", limit=1)
#        return (last_record.title_sequence or 0) + 1

#    @api.model
#    def get_next_desc_sequence(self):
#        """Get the next sequence number"""
#        last_record = self.search([], order="desc_sequence desc", limit=1)
#        return (last_record.desc_sequence or 0) + 1

#    @api.model_create_multi
#    def create(self, vals_list):
#        """Ensure sequence is correctly set when creating a record"""
#        for vals in vals_list:
#            if "title_sequence" not in vals or vals["title_sequence"] == 0:
#                vals["title_sequence"] = self.get_next_title_sequence()
#            if "desc_sequence" not in vals or vals["desc_sequence"] == 0:
#                vals["desc_sequence"] = self.get_next_desc_sequence()
#        return super(ItemGenerateField, self).create(vals)

#    @api.onchange('title_sequence')
#    def onchange_title_sequence(self):
#        """Automatically update other title_sequence values if sequence is changed"""
#        if not self.title_sequence:
#            return
#        # Fetch all records where title_sequence is greater than or equal to the new value
#        next_seqs = self.search([
#            ('title_sequence', '>=', self.title_sequence), ('id', '!=', self._origin.id)
#        ], order="title_sequence")
#        sequence = self.title_sequence
#        for rec in next_seqs:
#            sequence += 1
#            rec.title_sequence = sequence

#    @api.onchange('desc_sequence')
#    def onchange_desc_sequence(self):
#        """Automatically update other desc_sequence values if sequence is changed"""
#        if not self.desc_sequence:
#            return
#        # Fetch all records where desc_sequence is greater than or equal to the new value
#        next_seqs = self.search([
#            ('desc_sequence', '>=', self.desc_sequence), ('id', '!=', self._origin.id)
#        ], order="desc_sequence")
#        sequence = self.desc_sequence
#        for rec in next_seqs:
#            sequence += 1
#            rec.desc_sequence = sequence

    @api.depends('field_type')
    def _compute_length(self):
        """field type wise set value length"""
        for rec in self:
            rec.length = 999
            if rec.field_type == 'short':
                rec.length = 25
            elif rec.field_type == 'medium':
                rec.length = 40
        return True


class ItemGenerateFieldSelection(models.Model):
    _name = "item.generate.field.selection"
    _description = 'Item Generate Field Selection'

    sequence = fields.Integer(default=1)
    name = fields.Char(string="name", required=True)
    item_id = fields.Many2one("item.generate.field", "Item Generate Field")
    field_type = fields.Selection(related='item_id.field_type')
