from odoo import models,fields
from random import randint
from odoo.exceptions import ValidationError
import requests
import base64


class ThinkPcSites(models.Model):
    _name ="plc.sites"
    _description = "Think Sites"
    _rec_name = 'name'
    _inherit = ['mail.thread']


    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Sites Name')
    x_simpro_site_id = fields.Char('Simpro Site Id')
    zone = fields.Char('Zone')
    city = fields.Char('City')
    street = fields.Char('Street Address')
    street2 = fields.Char('Street Address')
    zip = fields.Char('Zip Code')
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    # billing_address = fields.Text('Billing Address')
    # billing_contact = fields.Char('Billing Contact')
    # billing_city = fields.Char('Billing City')
    # billing_state_id = fields.Many2one('res.country.state', 'Billing State')
    # billing_zip_code = fields.Char('Billing ZIP Code')
    siteid = fields.Integer('Site ID')
    customer_id = fields.Many2one('res.partner','Customer', domain=[('is_customer', '!=', False)])
    contact_id = fields.Many2one('res.partner','Primary Contact', domain=[('is_contact', '!=', False)])
    parent_id = fields.Many2one('plc.sites','Parent Id')
    child_ids = fields.One2many('plc.sites', 'parent_id', string='Contact', domain=[('active', '=', True)])
    customer_assets_ids = fields.One2many('thinkplc.assets', 'site_id', string='Customer Assets')
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    comment = fields.Html(string='Notes')
    email = fields.Char()
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)
    is_site_address = fields.Boolean('Is Address')
    contact_ids = fields.Many2many(comodel_name="res.partner",
        relation="site_con_rel",
        column1="stite_id",
        column2="con_id",
        string="Contacts",domain=[("is_contact", "!=", False)])
    avatar_128 = fields.Image("Avatar 128",  compute_sudo=True)

    def _create_multiple_contacts(self,odoo_site_id,simpro_site_id,company_url,company_id,headers):
        url = f'{company_url}api/v1.0/companies/{company_id}/sites/{simpro_site_id}/contacts/'
        contacts = self.env['res.partner']
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            data = response.json()
        except Exception as e:
            raise Exception(f"Attachments Fetch Error: {str(e)}")
        for record in data:
            contact_id = record.get('ID')
            find_contact = contacts.search([('x_simpro_contact_id', '=', contact_id), ('is_contact','!=', False)], limit=1)
            if find_contact:
                odoo_site_id.write({
                    'contact_ids' : [(4, find_contact.id)]
                    })

    def _create_customer_address(self, parent_id, billing_address, country_id):
        customer = self.env['plc.sites']
        state = self.env['res.country.state']
        state_id = False
        if parent_id.country_id:
            state_id = state.search([('code','=',billing_address.get('State')), ('country_id','=',parent_id.country_id.id)], limit=1)
        values = {
                'is_site_address' : True,
                'street' : billing_address.get('Address'),
                'city' : billing_address.get('City'),
                'zip' : billing_address.get('PostalCode'),
                'street' : billing_address.get('Address'),
                'country_id' : parent_id.country_id.id if parent_id.country_id else False,
                'state_id' : state_id.id if state_id else False,
                'parent_id' : parent_id.id,                
            }

        parent_customer = customer.create(values)

    def _get_attachment_of_asset(self, simpro_assets_id, odoo_new_asset, headers, site_id):
        company_url = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company_url')
        company_id = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company') or 0
        
        attachemenrt_url = f'{company_url}api/v1.0/companies/{0}/sites/{site_id}/assets/{simpro_assets_id}/attachments/files/'
        print('\n\n attachemenrt_url',attachemenrt_url)
        try:
            response = requests.get(attachemenrt_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get Assets: {response.text}")
            attachments = response.json()
        except Exception as e:
            raise Exception(f"Attachments Fetch Error: {str(e)}")

        for attachment in attachments:
            attachment_id = attachment.get('ID')
            file_name = attachment.get('Filename')
            attachemenrt__ids = f'{company_url}api/v1.0/companies/{0}/sites/{site_id}/assets/{simpro_assets_id}/attachments/files/{attachment_id}?display=Base64'
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
                'res_model': 'thinkplc.assets',
                'res_id': odoo_new_asset.id,
                'mimetype': result_json.get('MimeType'),
            })

    def _create_assets_of_sites(self, company_id, company_url, site_id, existing_odoo_site, headers):
        url = f'{company_url}api/v1.0/companies/{company_id}/sites/{site_id}/assets/'
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            data = response.json()
        except Exception as e:
            raise Exception(f"Attachments Fetch Error: {str(e)}")
        print('\n data',data)

        asset = self.env['thinkplc.assets']
        assets_type = self.env['thinkplc.assets.type']
        for assets in data:
            assets_id = assets.get('ID')
            assets_url = f'{company_url}api/v1.0/companies/{company_id}/sites/{site_id}/assets/{assets_id}'
            response = requests.get(assets_url, headers=headers)
            try:
                response = requests.get(assets_url, headers=headers)
                if response.status_code != 200:
                    raise Exception(f"Failed to get contacts: {response.text}")
                data = response.json()
                print('\n\n assets',data)
            except Exception as e:
                raise Exception(f"Assets Fetch Error: {str(e)}")
            AssetType = data.get('AssetType')
            asset_id = None
            parent_id = None
            if data.get('ParentID'):
                parent_asset = asset.search([('simpro_asset_id','=',data.get('ParentID'))], limit=1)
                if parent_asset:
                    parent_asset.write({
                        'related_asset_id':data.get('ParentID')
                        })

            if AssetType.get('ID') and AssetType.get('Name'):
                odoo_assets = assets_type.search([('name','=', AssetType.get('Name')), ('simpro_asset_id','=',AssetType.get('ID'))])
                if odoo_assets:
                    asset_id = odoo_assets.id
                else:
                    value = {
                        'name' : AssetType.get('Name'),
                        'simpro_id' : AssetType.get('ID')
                        }
                    new_asset_type = assets_type.create(value)
                    asset_id = new_asset_type.id
            value = {
                'simpro_asset_id' : assets_id,
                'asset_type_id' : asset_id,
                'site_id' : existing_odoo_site.id
                }
            new_asset = asset.create(value)
            self._get_attachment_of_asset(assets_id, new_asset, headers, site_id)
            print('\n new asset connected to site',new_asset ,'site id: ',existing_odoo_site)


    def _cron_get_simpro_sites(self):
        company_url = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company_url')
        company_id = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.company') or 0
        access_token = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.access_token')
        page_size = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.page_size')
        page = self.env['ir.config_parameter'].sudo().get_param('ehcs_simpro_integration.page')

        # === STEP 1: Use the provided token directly ===
        # access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        if not access_token:
            raise ValidationError("Please Enter Access Token \nSetting > Simpro Integration")

        if not company_url:
            raise ValidationError("Please Set Your Company Simpro Url\n setting > Simpro Integration")

        country = self.env['res.country']
        new_sites = self.env['plc.sites']
        contacts = self.env['res.partner']
        miss_records = self.env['product.miss.records']
        state = self.env['res.country.state']
        
        # === STEP 2: API endpoint for Sites ===
        site_url = f'{company_url}api/v1.0/companies/{company_id}/sites/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        params = {
            "pageSize": page_size,
            "page": page
            }

        try:
            response = requests.get(site_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            sites = response.json()
        except Exception as e:
            raise Exception(f"Sites Fetch Error: {str(e)}")

        for site in sites:
            site_id = site.get('ID')
            specific_site_url = f'{company_url}api/v1.0/companies/{company_id}/sites/{site_id}'
            detail_res = requests.get(specific_site_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch Sites")
                continue
            data = detail_res.json() 
            # print('\n\n d`ata',data)
            site_name = data.get('Name')

            if not site_name:
                st = miss_records.search([('x_simpro_types','=','site'), ('simpro_id','=',data.get('ID'))])
                if not st:
                    miss_record = miss_records.create({
                        'simpro_id' : data.get('ID'),
                        'site_zip_code' : data.get('PostalCode'),
                        'x_simpro_types' : 'site',
                        })
                    print('\nRecord was skiped ann log created',miss_record)
                continue

            existing = self.env['plc.sites'].search([('x_simpro_site_id', '=', site_id)], limit=1)
            if existing:
                self._create_assets_of_sites(company_id, company_url, site_id, existing, headers)
                print("Site Already Created",existing)
                continue

            billing_address = data.get('BillingAddress')
            addresh = data.get('Address')
            country_id = country.search([("name",'=',addresh.get('Country'))])
            primary_contact = data.get('PrimaryContact')
            primary_contact_id = primary_contact.get('Contact')
            customers = data.get('Customers')
            if customers:
                customer_id = customers[0]
            state_id = state.search([('code','=',addresh.get('State')), ('country_id','=',country_id.id)], limit=1)

            existing_contact = False
            existing_customer = False
            if primary_contact_id:
                existing_contact = contacts.search([('x_simpro_contact_id', '=', primary_contact_id.get('ID')), ('is_contact','!=', False)], limit=1)
            if customers and customer_id.get('ID'):
                existing_customer = contacts.search([('x_simpro_contact_id', '=', customer_id.get('ID')), ('is_customer','!=', False)], limit=1)

            values = {
                'name': data.get('Name'),
                'zone': data.get('Zone'),
                'street': addresh.get('Address'),
                'zip': addresh.get('PostalCode'),
                'city': addresh.get('City'),
                'country_id' : country_id.id if country_id else False,
                'state_id' : state_id.id if state_id else False,
                'x_simpro_site_id': site_id,
                'contact_id': existing_contact.id if existing_contact else False,
                'customer_id': existing_customer.id if existing_customer else False,
            }

            odoo_site = new_sites.create(values)
            print('\n Created new site', odoo_site)
            self._create_assets_of_sites(company_id, company_url, site_id, odoo_site, headers)
            self._create_multiple_contacts(odoo_site,site_id,company_url,company_id,headers)
            if billing_address.get('Address') or billing_address.get('City'):
                self._create_customer_address(odoo_site, billing_address, country_id)
