# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.osv.expression import AND, OR

_logger = logging.getLogger(__name__)


def extract_global_search(args):
    """ Function to extract 'global_search' and its value"""
    global_search = None
    print("\n\n\n args",args)
    for item in args:
        if isinstance(item, list) and item[0] == 'global_search':
            global_search = item
            break
    return global_search


class Account(models.Model):
    _inherit = 'account.move'

    global_search = fields.Char(string="Global Search")

    # def _custom_args(self, args, operator, custom_args):
    #     """append custom args and domain"""
    #     #Ex. args = ['&', '&', '|', ['is_sample', '!=', True], ['is_collateral', '!=', True], ['state', 'in', ['draft', 'sent']], ['global_search', 'ilike', 'test']]
    #     operators = []
    #     conditions = []
    #     # Iterate over the args list to split operators and conditions
    #     for item in args:
    #         # print("ARGS item", item)
    #         if item in ['&', '|']:
    #             operators.append(item)
    #         else:
    #             if item[0] == 'global_search':
    #                 conditions.append(['name', item[1], item[2]])
    #             else:
    #                 conditions.append(item)
    #     # Iterate over the Custom args list to split operators and conditions
    #     for item in custom_args:
    #         # print("Custom ARGS item", operator, item)
    #         operators.append(operator)
    #         conditions.append(item)
    #     return operators + conditions

    def _remove_global_args(self, args):
        """remove global consition from args domain"""
        operators = []
        conditions = []
        for item in args:
            # print("\n\n ARGS item", item)
            if item in ['&', '|']:
                operators.append(item)
            else:
                if item[0] == 'global_search':
                    if '&' in operators:
                        operators.remove('&')
                    continue;
                else:
                    conditions.append(item)
        return operators + conditions

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Global search filter in search view"""
        # Extract 'global_search' and it's value
        global_search = extract_global_search(args)
        # print("\n\n\n kkkllkllklklklklkl",global_search)
        if global_search:
            globalfield = global_search[0]
            operator = global_search[1]
            value = global_search[2]
            # print(f"Field: {globalfield}, Operator: {operator}, Value: {value}")
            # We add conditions for all fields. You can modify this to include the fields you need.
            # Ex. global_field_ids = ['name', 'partner_id', 'state', 'amount_total', 'user_id']
            global_field_ids = self.env.company and self.env.company.sudo().global_inv_field_ids
            # All configure fields
            global_args = []
            for field in global_field_ids:
                # Ex. global_args = [('name', 'ilike', 'test')]
                global_args = OR([global_args, [(field.name, 'ilike', value)]])
                # globalarg = self._custom_args(args, operator, global_args)
                # global_args.append(globalarg) 
            try:
                newargs = self._remove_global_args(args)
                args = AND([newargs, global_args])
            except Exception as Ex:
                _logger.error('Error : %s', Ex)

        return super(Account, self).search(args, offset, limit, order, count)

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,
                       lazy=True, expand=False, expand_limit=None, expand_orderby=False):
        """
        Override the web_read_group method to handle custom domain logic (e.g., handling global_search).
        """
        # Extract and remove global_search from the domain
        global_search = extract_global_search(domain)

        # If we have global_search, process it
        if global_search:
            value = global_search[2]

            # Define the fields for global search (this can be customized)
            global_field_ids = self.env.company and self.env.company.sudo().global_field_ids or []

            # Modify the domain to include global search for these fields
            global_args = []
            global_fields = global_field_ids.mapped('name')
            fields += global_fields
            for field in global_field_ids:
                # Construct global search conditions using the value
                global_args = OR([global_args, [(field.name, 'ilike', value)]])

            try:
                # Remove the original global_search condition from the domain
                domain = self._remove_global_args(domain)
                # Combine the modified domain with global_args (using AND to include both)
                domain = AND([domain, global_args])
            except Exception as Ex:
                _logger.error('Error : %s', Ex)

        groups = self._web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, expand,
                                      expand_limit, expand_orderby)

        if not groups:
            length = 0
        elif limit and len(groups) == limit:
            # We need to fetch all groups to know the total number
            # this cannot be done all at once to avoid MemoryError
            length = limit
            chunk_size = 100000
            while True:
                more = len(self.read_group(domain, ['display_name'], groupby, offset=length, limit=chunk_size, lazy=True))
                length += more
                if more < chunk_size:
                    break
        else:
            length = len(groups) + offset
        return {
            'groups': groups,
            'length': length
        }
