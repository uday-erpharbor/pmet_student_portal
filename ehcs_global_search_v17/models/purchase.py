# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.osv.expression import AND, OR

_logger = logging.getLogger(__name__)


def extract_global_search(args):
    """ Extract 'global_search' from the domain. """
    for item in args:
        if isinstance(item, list) and item[0] == 'global_search':
            return item  # Return the complete condition
    return None


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    global_search = fields.Char(string="Global Search")


    def _remove_global_args(self, args):
        """remove global consition from args domain"""
        operators = []
        conditions = []
        for item in args:
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
    def _search(self, domain, offset=0, limit=None, order=None):
        # Extract 'global_search' from the domain
        global_search = extract_global_search(domain)

        if global_search:
            globalfield = global_search[0]
            operator = global_search[1]
            value = global_search[2]

            # Get global field IDs from the company
            global_po_field_ids = self.env.company and self.env.company.sudo().global_po_field_ids

            global_args = []
            for field in global_po_field_ids:
                # Ex. global_args = [('name', 'ilike', 'test')]
                new_condition = [(field.name, 'ilike', value)]
                global_args = OR([global_args, new_condition]) if global_args else new_condition
            try:
                newargs = self._remove_global_args(domain)
                domain = AND([newargs, global_args])
            except Exception as Ex:
                _logger.error('Error : %s',Ex)
        return super(PurchaseOrder, self)._search(domain, offset=offset, limit=limit, order=order)

    @api.model
    def web_read_group(self, domain, fields, groupby, limit=None, offset=0, orderby=False,
                       lazy=True):
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

        groups = self._web_read_group(domain, fields, groupby, limit, offset, orderby, lazy, )

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
