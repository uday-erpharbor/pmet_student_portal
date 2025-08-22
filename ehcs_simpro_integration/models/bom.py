from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    category_id = fields.Many2one('bom.category', 'Category')
    x_simpro_group_id = fields.Char('Simpro Id')
    reason = fields.Char('Reason')
    description = fields.Html('Description')
    note = fields.Html('Notes')

    def get_attachments(self, prebuildID, headers, bom_id):
        company_url = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company_url')
        company_id = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company') or 0
        
        attachemenrt_url = f'{company_url}api/v1.0/companies/{company_id}/prebuilds/{prebuildID}/attachments/files/'

        try:
            response = requests.get(attachemenrt_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get bom: {response.text}")
            attachments = response.json()
        except Exception as e:
            raise Exception(f"Attachments Fetch Error: {str(e)}")

        # print('\n\n attachment',attachments)
        for attachment in attachments:
            attachment_id = attachment.get('ID')
            file_name = attachment.get('Filename')
            attachemenrt__ids = f'{company_url}api/v1.0/companies/{company_id}/prebuilds/{prebuildID}/attachments/files/{attachment_id}?display=Base64'
            response = requests.get(attachemenrt__ids, headers=headers)
            if response.status_code != 200:
                print(f"Failed to download: {file_name}")
                continue

            result_json = response.json()
            base64_data = result_json.get('Base64Data')
    
            if not base64_data:
                print(f"No Base64Data for: {file_name}")
                continue

            new_attachment = self.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': base64_data,
                'res_model': 'mrp.bom',
                'res_id': bom_id,
                'mimetype': result_json.get('MimeType'),
            })

    def _cron_get_simpro_prebuilds(self):
        IrConfig = self.env['ir.config_parameter'].sudo()
        simpro_url = IrConfig.get_param('ehcs_simpro_integration.company_url')
        company_id = IrConfig.get_param('ehcs_simpro_integration.company') or 0
        access_token = IrConfig.get_param('ehcs_simpro_integration.access_token')
        page_size = IrConfig.get_param('ehcs_simpro_integration.page_size')
        page = IrConfig.get_param('ehcs_simpro_integration.page')

        if not access_token:
            raise ValidationError("Please enter the Access Token in Settings > Simpro Integration")
        if not simpro_url:
            raise ValidationError("Please set the Company Simpro URL in Settings > Simpro Integration")

        # Build the API URL
        prebuilds_url = f'{simpro_url}api/v1.0/companies/{company_id}/prebuilds/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        params = {
            "pageSize": page_size,
            "page": page
        }

        try:
            response = requests.get(prebuilds_url, headers=headers, params=params)
            response.raise_for_status()
            prebuilds = response.json()
        except Exception as e:
            raise Exception(f"Error fetching prebuilds: {str(e)}")

        print('\nPrebuilds:', prebuilds)

        BomModel = self.env['mrp.bom']
        ProductModel = self.env['product.template']
        MissRecordModel = self.env['product.miss.records']
        BomCategoryModel = self.env['bom.category']

        for prebuild in prebuilds:
            prebuild_id = prebuild.get('ID')
            prebuild_href = prebuild.get('_href')

            # Get full prebuild detail
            prebuild_detail_url = f'{simpro_url[:-1]}{prebuild_href}'
            try:
                detail_response = requests.get(prebuild_detail_url, headers=headers)
                detail_response.raise_for_status()
                prebuild_data = detail_response.json()
            except:
                print(f"Failed to fetch details for Prebuild ID: {prebuild_id}")
                continue

            print('\nPrebuild Detail:', prebuild_data)

            # Skip if BoM already exists
            existing_bom = BomModel.search([('x_simpro_group_id', '=', prebuild_data.get('ID'))], limit=1)

            if existing_bom:
                print("BoM already exists:", existing_bom)
                continue

            part_number = prebuild_data.get('PartNo')
            if not part_number:
                already_missing = MissRecordModel.search([
                    ('simpro_id', '=', prebuild_data.get('ID')),
                    ('x_simpro_types', '=', 'bom')
                ])
                if not already_missing:
                    missing_log = MissRecordModel.create({
                        'simpro_id': prebuild_data.get('ID'),
                        'name': prebuild_data.get('Name'),
                        'x_simpro_types': 'bom',
                        'reason': 'Product part number not found',
                    })
                    print('\nMissed BoM log created:', missing_log)
                continue

            # Find or create product
            product = ProductModel.search([('default_code', '=', part_number)], limit=1)
            if not product:
                product = ProductModel.create({
                    'name': prebuild_data.get('Name'),
                    'default_code': part_number,
                    'x_simpro_product_id': 'missbomproduct',
                    'list_price': prebuild_data.get('Materials'),
                    'standard_price': prebuild_data.get('TotalInc'),
                })

            # Handle BoM Category
            bom_category_data = prebuild_data.get('Group')
            bom_category_id = False

            if bom_category_data and bom_category_data.get('ID'):
                existing_category = BomCategoryModel.search([
                    ('x_simpro_id', '=', bom_category_data.get('ID')),
                    ('name', '=', bom_category_data.get('Name'))
                ], limit=1)

                if not existing_category:
                    parent_group_data = bom_category_data.get('ParentGroup')
                    parent_category = False
                    if parent_group_data:
                        parent_category = BomCategoryModel.search([
                            ('x_simpro_id', '=', parent_group_data.get('ID')),
                            ('name', '=', parent_group_data.get('Name'))
                        ], limit=1)
                        if not parent_category:
                            new_category = BomCategoryModel.create({
                                'name': parent_group_data.get('Name'),
                                'x_simpro_id': parent_group_data.get('ID'),
                            })

                    new_category = BomCategoryModel.create({
                        'name': bom_category_data.get('Name'),
                        'x_simpro_id': bom_category_data.get('ID'),
                        'parent_id': parent_category.id if parent_category else False,
                    })
                    bom_category_id = new_category.id
                else:
                    bom_category_id = existing_category.id

            # Create the BoM
            new_bom = BomModel.create({
                'product_tmpl_id': product.id,
                'category_id': bom_category_id,
                'x_simpro_group_id': prebuild_data.get('ID'),
                'note': prebuild_data.get('Notes'),
                'description': prebuild_data.get('Description'),
            })

            # Fetch catalog items (BoM lines)
            catalog_url = f'{simpro_url}api/v1.0/companies/{company_id}/prebuilds/{prebuild_id}/catalogs/'
            try:
                catalog_response = requests.get(catalog_url, headers=headers)
                catalog_response.raise_for_status()
                catalog_items = catalog_response.json()
            except:
                print(f"Failed to fetch catalog for Prebuild ID: {prebuild_id}")
                continue

            print('\nCatalog Items:', catalog_items)

            bom_lines = []
            for item in catalog_items:
                catalog_product = item.get('Catalog')
                if not catalog_product:
                    continue

                component_product = ProductModel.search([
                    ('x_simpro_product_id', '=', catalog_product.get('ID')),
                    ('default_code', '=', catalog_product.get('PartNo'))
                ], limit=1)

                if not component_product:
                    component_product = ProductModel.create({
                        'name': catalog_product.get('Name'),
                        'x_simpro_product_id': catalog_product.get('ID'),
                        'default_code': catalog_product.get('PartNo'),
                        'standard_price': catalog_product.get('TradePrice'),
                        'categ_id': 1,  # fallback to a generic category
                        'x_simpro_display_order': catalog_product.get('DisplayOrder'),
                    })
                    print('\nCreated new component product:', component_product)

                bom_lines.append((0, 0, {
                    'product_id': component_product.id,
                    'product_qty': item.get('Quantity'),
                }))

            # Assign BoM lines
            try:
                new_bom.write({'bom_line_ids': bom_lines})
            except ValidationError as e:
                print(f"BoM skipped due to cycle: {e}")
                new_bom.unlink()
                continue
            print('\nBoM created successfully:', new_bom)

            # Optional: fetch & attach files
            self.get_attachments(prebuild_data.get('ID'), headers, new_bom.id)
