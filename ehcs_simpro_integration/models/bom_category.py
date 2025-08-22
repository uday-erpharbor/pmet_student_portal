from odoo import models,fields, api
import requests


class ThinkPcSites(models.Model):
    _name ="bom.category"
    _description = "Pre Bulieds "
    _rec_name = 'complete_name'

    name = fields.Char('Name')
    parent_id = fields.Many2one('bom.category','Parent Category')
    x_simpro_id = fields.Char('Simpro Id')
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _cron_get_simpro_bom_groups(self):
        company_url = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company_url')
        company_id = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company') or 0
        access_token = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.access_token')
        page_size = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.page_size')
        page = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.page')

        # === STEP 1: Use the provided token directly ===
        if not access_token:
            raise ValidationError("Please Enter Access Token \nSetting > Simpro Integration")

        if not company_url:
            raise ValidationError("Please Set Your Company Simpro Url\n setting > Simpro Integration")
        
        # access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        # === STEP 2: Call Simpro API ===
        group_url = f'{company_url}api/v1.0/companies/{company_id}/prebuildGroups/'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        try:
            response = requests.get(group_url, headers=headers, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Failed to get products: {response.text}")
            groups = response.json()
        except Exception as e:
            raise Exception(f"Group Fetch Error: {str(e)}")
        print('\n\n groups',groups)
        print('\n\n len',len(groups))
        
        category = self.env['bom.category']
        for group in groups:
            group_id = group.get('ID')
            specific_group_url = f'{company_url}api/v1.0/companies/{company_id}/prebuildGroups/{group_id}'
            detail_res = requests.get(specific_group_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch Groups")
                continue
            data = detail_res.json() 
            print('\n\n data',data)

            parent_group = data.get('ParentGroup')
            existing_group = self.env['bom.category'].search([('x_simpro_id', '=', group_id), ('name','=', data.get('Name'))], limit=1)
            if existing_group:
                print(f"Group Has already created:",existing_group)
                continue
            
            if parent_group:
                existing_parent_group = self.env['bom.category'].search([('x_simpro_id', '=', parent_group.get('ID')), ('name','=', parent_group.get('Name'))], limit=1)
                if existing_parent_group:
                    parent_group_id = existing_parent_group.id
                if not existing_parent_group:
                    value = {
                        'name' : parent_group.get('Name'),
                        'x_simpro_id' : parent_group.get('ID'),
                        }
                    parent_category = category.create(value)
                    parent_group_id = parent_category.id

            values = {
                'name' : group.get('Name'),
                'parent_id' : parent_group_id if parent_group else False,
                'x_simpro_id' : group_id
                }
            categorys = category.create(values)
            print('\n Category Created',categorys)

