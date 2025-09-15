# -*- coding: utf-8 -*-
"""This model is used to detect, which all options want to hide from the
    specified group and model"""
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models


class ModelAccessRights(models.Model):
    """This class is used to detect, which all options want to hide from the
    specified group and model"""
    _name = 'access.right'
    _inherit = 'mail.thread'
    _description = 'Manage Modules Access Control'
    _res_name = 'user_id'

    model_ids = fields.Many2many(
                'ir.model',
                'access_right_ddir_model_rels',   # relation table name
                'ddddddd',             # column for this model
                'model_id',                    # column for ir.model
                string="Models",
                required=True,
                help="Select one or more models"
            )
    groups_id = fields.Many2one('res.groups',
                                help="select the group")
    is_delete = fields.Boolean(string="Delete", help="hide the delete option")
    is_export = fields.Boolean(string="Export",
                               help="hide the 'Export All'"
                                    " option from list view")
    is_create_or_update = fields.Boolean(string="Create/Update",
                                         help="hide the create option from list"
                                              " as well as form view")
    is_archive = fields.Boolean(string="Archive/UnArchive",
                                help="hide the archive option")
    restriction_type = fields.Selection([
        ('user', 'User Wise'),
        ('group', 'Group Wise')
    ], 'Restriction Type',required=True,default="user")
    user_id = fields.Many2one('res.users',
                                help="select the user")

    @api.model
    def hide_buttons(self):
        """This function contains a query  that detects which all options want
        to hide, in which model,and to which user groups"""
        access_right_rec = self.sudo().search_read([], [
            'model_ids', 'is_delete',
            'is_export', 'is_create_or_update',
            'is_archive', 'restriction_type',
            'user_id', 'groups_id'
        ])
        print('\n\n access_right_rec', access_right_rec)

        for dic in access_right_rec:
            # model_ids is already list of int (IDs)
            models = self.env['ir.model'].sudo().browse(dic['model_ids'])
            model_names = models.mapped('model')

            if dic['restriction_type'] == "group" and dic['groups_id']:
                ir_data = self.env['ir.model.data'].sudo().search([
                    ('model', '=', 'res.groups'),
                    ('res_id', '=', dic['groups_id'][0])
                ], limit=1)
                group_name = ir_data.name
                module_name = ir_data.module
            else:
                group_name = False
                module_name = False

            dic.update({
                'models': model_names,   # <-- now it’s a list of model technical names
                'group_name': group_name,
                'module': module_name,
                'restriction_type': dic['restriction_type'],
                'user': dic['user_id']
            })
            print('\n\n dic', dic)
        return access_right_rec
