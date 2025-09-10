# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import Controller, request, route


class CategoryConfiguratorController(Controller):

    @route(route='/product_category_configurator/get_option_values', type='json', auth='user', methods=['POST'])
    def product_category_configurator_get_option(self, item_id, value):
        """ Get the item option"""
        option = request.env['item.generate.field.selection'].search([
            ('id', '=', value),
            ('item_id', '=', item_id)
        ], limit=1)
        return option.id if option else 'none'

    @route(route='/product_category_configurator/get_values', type='json', auth='user')
    def get_product_configurator_values(
        self,
        product_id=None,
        product_template_id=None,
        category_id=None,
        company_id=None,
    ):
        """ Return all product information needed for the product configurator"""
        if company_id:
            request.update_context(allowed_company_ids=[company_id])
        product = request.env['thinkplc.assets'].browse(product_id)
        product_template = request.env['thinkplc.assets'].browse(product_template_id)
        product_category = request.env['thinkplc.assets.type'].browse(category_id)

        value = False
        # Selected Value
        selected_item_ids = []
        for line in product.item_generate_field_value_ids:
            value = line.name or ''
            # If field_type is 'option', get the matching option ID
            if line.item_id.field_type == 'option':
                option = request.env['item.generate.field.selection'].search([
                    ('name', '=', value),
                    ('item_id', '=', line.item_id.id)
                ], limit=1)
                value = option.id if option else ''
            elif line.item_id.field_type == 'checkbox':
                value = str(value).lower() in ['true', '1', 'yes', 'on']
            # Create the selected item dictionary
            selected_item_ids.append({
                'id': line.id,
                'item_id': line.item_id.id,
                'product_id': line.product_id.id,
                'field_type': line.item_id.field_type,
                'value': value  # Store option ID instead of name
            })

        item_ids_dict = {}
        for line in product_category.item_generate_fields_ids.sorted(lambda x: x.sequence or x.id):
            item_line_dict = {
                'id': line.id,
                'label': line.name,
                'field_type': line.field_type,
                'length': line.length,
                'options': [{'id': option.id, 'sequence': option.sequence, 'name': option.name} for option in line.options_ids],
                'required': str(line.is_required).lower(),
                'value': value or ''
            }
            # If the ID already exists, update it; otherwise, add a new entry
            item_ids_dict[line.id] = item_line_dict
        # Convert dictionary values to a list
        item_ids = list(item_ids_dict.values())

        return dict(
            categories=[
                dict(
                    product_template_id = product_template,
                    category_id = product_category.id,
                    category_name = product_category.name,
                    product_name = product.name,
                    item_ids = item_ids,
                )
            ],
            selectedItemIds= selected_item_ids,
        )

    @route('/product_category_configurator/create_product_item', type='json', auth='user', methods=['POST'])
    def product_category_configurator_create_product(self, product_id, category_id, item_ids):
        """Create or update product with dynamic item values."""
        category = request.env['thinkplc.assets.type'].browse(category_id)
        product = request.env['thinkplc.assets'].browse(product_id)
        IGFV = request.env['item.generate.field.value']
        # Item line name type wise
        field_value_mapping = {
            'option': lambda item: request.env['item.generate.field.selection'].browse(int(item['value'])).name if item['value'] != 'none' else 'None',
            'integer': lambda item: item['value'],
            'checkbox': lambda item: str(item['value']),
            'default': lambda item: item['value']
        }
        for item in item_ids:
            # Get existing field values for the item
            existing_item = product.item_generate_field_value_ids.filtered(
                lambda l: l.item_id.id == int(item['item_id'])
            )
            item_value = field_value_mapping.get(item['field_type'], field_value_mapping['default'])(item)
            item_line_dict = {'name': item_value or '', 'item_id': item['item_id'], 'product_id': product.id}
            # Update existing record or create new one
            if existing_item:
                existing_item.write(item_line_dict)
            else:
                IGFV.create(item_line_dict)
        # Update product name and description
        product._compute_item()
        return product.id
