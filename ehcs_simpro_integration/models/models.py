# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import base64

class ProductCategory(models.Model):
    _inherit = 'product.category'
   
    x_simpro_group_id = fields.Char(string="Simpro Group ID")


class Product(models.Model):
    _inherit = 'product.template'

    # Add a custom field to store Simpro contact ID
    x_simpro_product_id = fields.Char(string="Simpro Product ID")
    x_simpro_upc = fields.Char("UPC")
    x_simpro_vendore_part_number = fields.Char('Vendor Part Number')
    x_simpro_search_terms = fields.Char("Search Terms")
    x_simpro_is_favorite = fields.Boolean('Favorite')
    x_simpro_is_inventory = fields.Boolean('Inventory')
    x_simpro_is_assets = fields.Boolean('Assets')
    x_simpro_trade_price = fields.Float('Trade Price')
    x_simpro_display_order = fields.Float('Display Order')




    #get group of product means category
    def _cron_get_simpro_group(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'

        # === STEP 2: Call Simpro API ===
        group_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/catalogGroups/'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }

        try:
            response = requests.get(group_url, headers=headers, timeout=30)
            if response.status_code != 200:
                raise Exception(f"Failed to get products: {response.text}")
            groups = response.json()
            print('\n\n groups',groups)
        except Exception as e:
            raise Exception(f"Group Fetch Error: {str(e)}")

        category = self.env['product.category']
        
        for group in groups:
            group_id = group.get('ID')
            specific_group_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/catalogGroups/{group_id}'
            detail_res = requests.get(specific_group_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch Groups")
                continue
            data = detail_res.json() 
            print("\n\n data",data)

            parent_group = data.get('ParentGroup')
            existing_group = self.env['product.category'].search([('x_simpro_group_id', '=', group_id), ('name','=', data.get('Name'))], limit=1)
            if existing_group:
                print(f"Group Has already created:",existing_group)
                continue
            if parent_group:
                existing_parent_group = self.env['product.category'].search([('x_simpro_group_id', '=', parent_group.get('ID')), ('name','=', parent_group.get('Name'))], limit=1)
                print('\n existing_parent_group',existing_parent_group)
                if existing_parent_group:
                    parent_group_id = existing_parent_group.id
                if not existing_parent_group:
                    value = {
                        'name' : parent_group.get('Name'),
                        'x_simpro_group_id' : parent_group.get('ID'),
                        }
                    parent_category = category.create(value)
                    parent_group_id = parent_category.id
            values = {
                'name' : group.get('Name'),
                'parent_id' : parent_group_id if parent_group else False,
                'x_simpro_group_id' : group_id
                }
            categorys = category.create(values)
            print('\n\n Category Created',categorys)


    def _cron_get_simpro_product_data(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        prod = self.env['product.template']
        categorys = self.env['product.category']
        vendor_parner = self.env['res.partner']
        
        # === STEP 2: Call Simpro API ===
        catalog_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/catalogs/'

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        params = {
            "pageSize": 200,
            "page": 1
            }

        #connect api and get data
        try:
            response = requests.get(catalog_url, headers=headers, timeout=30, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get products: {response.text}")
            products = response.json()
            print('\n\n products',products)
            print('\n\n products',len(products))
        except Exception as e:
            raise Exception(f"Catalog Fetch Error: {str(e)}")

        #create product
        for product in products:
            product_id = product.get('ID')
            specific_product_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/catalogs/{product_id}'
            detail_res = requests.get(specific_product_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch Product")
                continue

            data = detail_res.json() 
            name = data.get('Name') or data.get('PartNo')
            if not name:
                print("No name or part number found, skipping.")
                continue

            existing = prod.search([('x_simpro_product_id', '=', data.get('ID')), ('default_code','=', data.get('PartNo'))], limit=1)
            print('\n\n data',data)
            if existing:
                print("Product Already Created",existing)
                continue

            vendors = data.get('Vendors')

            # Handle category
            category = data.get('Group')
            category_id = False
            if category:
                print("\n\n category",category)
                existing_category = categorys.search([
                    ('x_simpro_group_id', '=', category.get('ID')),
                    ('name', '=', category.get('Name'))
                ], limit=1)
                if existing_category:
                    category_id = existing_category.id
                else:
                    new_category = categorys.create({
                        'name': category.get('Name'),
                        'x_simpro_group_id': category.get('ID')
                    })
                    category_id = new_category.id

            print('\n\n category_id',category_id)
            values = {
                    'name' : name,
                    'default_code' : data.get('PartNo'),
                    'list_price' : data.get('SellPrice'),
                    'categ_id' : category_id if category_id else 1,
                    'x_simpro_vendore_part_number' : data.get('VendorPartNo'),
                    'x_simpro_upc' : data.get('UPC'),
                    'x_simpro_search_terms' : data.get('SearchTerm'),
                    'x_simpro_is_favorite' :  data.get('IsFavorite'),
                    'x_simpro_is_inventory' : data.get('IsInventory'),
                    'x_simpro_is_assets' : data.get('IsAsset'),
                    'x_simpro_trade_price' : data.get('TradePrice'),
                    'x_simpro_display_order' : data.get('DisplayOrder'),
                }

            product_template =  prod.create(values)
            vendor_lines = []
            if vendors:
                print("\n\n vendors",vendors)
                for vendor in vendors:
                    vendor_id = vendor.get('Vendor')
                    v_id = vendor_id.get('ID')
                    odoo_vendor_id = vendor_parner.search([('x_simpro_contact_id','=',v_id), ('x_simpro_types','=','vendore')])
                    print('\n\n odoo_vendor_id',odoo_vendor_id)
                    vendor_lines.append((0, 0, {
                            'partner_id' : odoo_vendor_id.id,
                            'product_tmpl_id' : product_template.id,
                            'discount' : vendor.get('Discount'),
                            'min_qty' : vendor.get('VendorQuantity'),
                        }))

            product_template.write({
                'seller_ids' : vendor_lines
                })
            print('\n\n Product Created',product_template)

























class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Add a custom field to store Simpro contact ID
    x_simpro_contact_id = fields.Char(string="Simpro ID", index=True)
    x_simpro_company_fax = fields.Char('Company Fax')
    x_simpro_types = fields.Selection([('vendore','Vendors'), ('contact','Contact'), ('customer','Customer'), ('contractor','Contractor')])
    site_ids = fields.One2many('plc.sites','customer_id','Sites')
    contact_site_ids = fields.One2many('plc.sites','contact_id','Sites')
    simpro_id = fields.Many2one('res.partner', domain=[('is_contact', '!=', False)], string='Primary Contact')
    simpro_site_ids = fields.One2many('res.partner','simpro_id','Sites')
    is_customer = fields.Boolean('Is Customer')
    is_vendor = fields.Boolean('Is Vendor')
    is_contact = fields.Boolean('Is Contact')
    is_sites = fields.Boolean('Is Sites')
    is_contractor = fields.Boolean('Is Contractor')

# ------------------inside code is for get data and uper side is for devloping----------------------------------------------------------------------------------------------

    def get_attachments(self, external_id, headers, customer_id, value):
        # headers = {
        #     'Authorization': 'Bearer 37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b',
        #     'Content-Type': 'application/pdf'
        # }

        if value == 'customer':
            attachemenrt_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/customers/{external_id}/attachments/files/'
        if value == 'vendors':
            attachemenrt_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/vendors/{external_id}/attachments/files/'
        if value == 'contractor':
            attachemenrt_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/contractors/{external_id}/attachments/files/'
        
        try:
            response = requests.get(attachemenrt_url, headers=headers)
            print("\n\n response",response.headers)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            attachments = response.json()
            print("\n\n attachments",attachments)
        except Exception as e:
            raise Exception(f"Attachments Fetch Error: {str(e)}")

        for attachment in attachments:
            attachment_id = attachment.get('ID')
            file_name = attachment.get('Filename')
            if value == 'customer':
                attachemenrt__ids = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/customers/{external_id}/attachments/files/{attachment_id}?display=Base64'
            if value == 'vendors':
                attachemenrt__ids = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/vendors/{external_id}/attachments/files/{attachment_id}?display=Base64'
            if value == 'contractor':
                attachemenrt__ids = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/contractors/{external_id}/attachments/files/{attachment_id}?display=Base64'

            response = requests.get(attachemenrt__ids, headers=headers)
            print(f"Downloading {file_name} | Size: {len(response.content)} bytes")

            if response.status_code != 200:
                print(f"Failed to download: {file_name}")
                continue

            result_json = response.json()
            base64_data = result_json.get('Base64Data')
            if not base64_data:
                print(f"No Base64Data for: {file_name}")
                continue

            print('\n\n response',response)
            print('\n\n headers',response.headers)

            # print('\n\n content',response.content)
            new_attachment = self.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': base64_data,
                'res_model': 'res.partner',
                'res_id': customer_id,
                'mimetype': 'application/pdf',
            })
            print('\n\n new_attach',new_attachment)

    #for create child address of customer
    def _create_customer_address(self, parent_id, billing_address):
        customer = self.env['res.partner']
        country = self.env['res.country'].search([("name",'=',billing_address.get('Country'))])
        values = {
                'type' : 'invoice',
                'street' : billing_address.get('Address'),
                'city' : billing_address.get('City'),
                'zip' : billing_address.get('PostalCode'),
                'street' : billing_address.get('Address'),
                'country_id' : country.id if country else False,
                'parent_id' : parent_id
            }
        parent_customer = customer.create(values)

    #this method will get a customer not contact just name add by mistake
    def _cron_get_simpro_contacts(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        country = self.env['res.country']
        customer = self.env['res.partner']
        
        # === STEP 2: API endpoint for contacts ===
        contact_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/customers/companies/'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        
        #this is for which page of simpro and how many conatact you will get
        params = {
            "pageSize": 1,
            "page": 1
            }
        
        try:
            response = requests.get(contact_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            contacts = response.json()
            print('\n\n contact',contacts)
            print('\n\n contact',len(contacts))
        except Exception as e:
            raise Exception(f"Contact Fetch Error: {str(e)}")
        
        # === STEP 3: Create or Update Contacts in Odoo ===
        for contact in contacts:
            external_id = contact.get('ID')  # Simpro contact ID
            specific_contact_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/customers/companies/{external_id}'
            detail_res = requests.get(specific_contact_url, headers=headers)
           
            if detail_res.status_code != 200:
                print(f"Failed to fetch customer")
                continue
            data = detail_res.json() 
            print("\n\n dddata",data)
            
            addresh = data.get('Address')
            customer_name = contact.get('CompanyName')
            billing_address = data.get('BillingAddress')

            if not customer_name:
                continue
            # print('\nn kokok')
            # existing = self.env['res.partner'].search([('email', '=', data.get('Email')), ('x_simpro_contact_id','=', external_id)], limit=1)
            country_id = country.search([("name",'=',addresh.get('Country'))]) 
            # print('\n\n csdsd',country_id)
            # if existing:
            #     print("Customer Already Created",existing)
            #     continue
            
            values = {
                'x_simpro_types' : 'customer',
                'is_customer' : 1,
                'company_type' : 'company',
                'name': 'uday-balas',
                'email': data.get('email'),
                'phone': data.get('phone'),
                'street': addresh.get('Address'),
                'zip': addresh.get('PostalCode'),
                'city': addresh.get('City'),
                'x_simpro_company_fax': data.get('Fax'),
                'country_id' : country_id.id if country_id else False,
                'x_simpro_contact_id': external_id,
                'vat' : data.get('EIN')
            }    
            cus = customer.create(values)
            
            ##for create attachments of customer
            self.get_attachments(external_id,headers,cus.id,'customer')
         
            ##create customer address
            # if billing_address:
            #     self._create_customer_address(cus.id, billing_address)

            print('\n\n customer created',cus)
            


# -------------------------------------------------------------------------------
    
    def _cron_get_simpro_vendors(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        country = self.env['res.country']
        customer = self.env['res.partner']
        
        # === STEP 2: API endpoint for contacts ===
        contact_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/vendors/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        params = {
            "pageSize": 100,
            "page": 1
            }

        try:
            response = requests.get(contact_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            contacts = response.json()
            print('\n\n contact',contacts)
            print('\n\n contact',len(contacts))
        except Exception as e:
            raise Exception(f"Contact Fetch Error: {str(e)}")

        # # === STEP 3: Create or Update Contacts in Odoo ===

        for contact in contacts:
            external_id = contact.get('ID')  # Simpro contact ID
            specific_contact_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/vendors/{external_id}'
            detail_res = requests.get(specific_contact_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch vendors")
                continue
            data = detail_res.json() 
            
            print("\n\n data",data)
            customer_name = contact.get('Name')
            addresh = data.get('Address')
            billing_address = data.get('BillingAddress')
            
            if not customer_name:
                continue
            
            existing = self.env['res.partner'].search([('email', '=', data.get('Email')), ('x_simpro_contact_id','=', external_id)], limit=1)
            country_id = country.search([("name",'=',addresh.get('Country'))]) 
            
            # if existing:
            #     print("Vendors Already Created",existing)
            #     continue

            values = {
                'x_simpro_types': 'vendore',
                'is_vendor': 1,
                'company_type' : 'company',
                'name': contact.get('Name'),
                'email': data.get('Email'),
                'phone': data.get('Phone'),
                'street': addresh.get('Address'),
                'zip': addresh.get('PostalCode'),
                'city': addresh.get('City'),
                'x_simpro_company_fax': data.get('Fax'),
                'country_id' : country_id.id if country_id else False,
                'x_simpro_contact_id': external_id,
                'vat' : data.get('EIN')
            }

            vendors = customer.create(values)
            print('\n\n vendors created',vendors)

            # for create attachments of vendor
            # self.get_attachments(external_id,headers,vendors.id,'vendors')

            #create customer address
            # if billing_address:
                # self._create_customer_address(vendors.id, billing_address)


    #this script is for contact
    def _cron_get_simpro_con(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        country = self.env['res.country']
        customer = self.env['res.partner']
        
        # === STEP 2: API endpoint for contacts ===
        contact_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/contacts/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        params = {
            "pageSize": 100,
            "page": 13
            }    
        try:
            response = requests.get(contact_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            contacts = response.json()
            # print('\n\n contact',contacts)
            # print('\n\n contact',len(contacts))
        except Exception as e:
            raise Exception(f"Contact Fetch Error: {str(e)}")

        for contact in contacts:
            external_id = contact.get('ID')  # Simpro contact ID
            specific_contact_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/contacts/{external_id}'
            detail_res = requests.get(specific_contact_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch customer")
                continue
            data = detail_res.json() 
            print("\n\n data",data)
            
            customer_name = contact.get('GivenName')
        
            if not customer_name:
                continue

            existing = self.env['res.partner'].search([('email', '=', data.get('Email')), ('x_simpro_contact_id','=', external_id)], limit=1)
            
            if existing:
                print("Vendors Already Created",existing)
                continue

            values = {
                'x_simpro_types': 'contact',
                'is_customer': 1,
                'company_type' : 'company',
                'name': f'{data.get("GivenName")} {data.get("FamilyName")}',
                'email': data.get('Email'),
                'phone': data.get('CellPhone'),
                'mobile': data.get('WorkPhone'),
                'comment': data.get('Notes'),
                'x_simpro_company_fax': data.get('Fax'),
                'x_simpro_contact_id': external_id,
            }
            contact = customer.create(values)
            print('\n\n contact created', contact)

    def _cron_get_simpro_sites(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        country = self.env['res.country']
        new_sites = self.env['res.partner']
        
        # === STEP 2: API endpoint for Sites ===
        site_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/sites/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        params = {
            "pageSize": 250,
            "page": 2
            }
        try:
            response = requests.get(site_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get contacts: {response.text}")
            sites = response.json()
            print('\n\n sites',sites)
            print('\n\n sites',len(sites))
        except Exception as e:
            raise Exception(f"Sites Fetch Error: {str(e)}")

        for site in sites:
            site_id = site.get('ID')
            specific_site_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/sites/{site_id}'
            detail_res = requests.get(specific_site_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch customer")
                continue
            data = detail_res.json() 
            print("\n\n data",data)

            site_name = data.get('Name')

            if not site_name:
                continue

            existing = self.env['res.partner'].search([('x_simpro_contact_id', '=', data.get('ID')), ('is_sites','!=', False), ('name','=', data.get('Name'))], limit=1)
            print('\n\n existing',existing)
            if existing:
                print("Site Already Created",existing)
                continue

            billing_address = data.get('BillingAddress')
            addresh = data.get('Address')
            country_id = country.search([("name",'=',addresh.get('Country'))])
            primary_contact = data.get('PrimaryContact')
            primary_contact_id = primary_contact.get('Contact')
            print('\n\n billing_address',billing_address)
            print('\n\n primary_contact_id',primary_contact_id)

            values = {
                'is_sites': 1,
                'company_type' : 'company',
                'name': data.get('Name'),
                'street': addresh.get('Address'),
                'zip': addresh.get('PostalCode'),
                'city': addresh.get('City'),
                'country_id' : country_id.id if country_id else False,
                'x_simpro_contact_id': site_id,
            }

            odoo_site = new_sites.create(values)
            print('\n\n Created new site', odoo_site)

            if primary_contact_id:
                existing_contact = new_sites.search([('x_simpro_contact_id', '=', primary_contact_id.get('ID')), ('is_contact','!=', False), ('email','=', primary_contact_id.get('Email'))], limit=1)
                if existing_contact:
                    odoo_site.write({
                        'simpro_id' : existing_contact.id
                        })
                print('\n\n existing_contact',existing_contact)

            # create customer address
            if billing_address.get('Address') or billing_address.get('City'):
                self._create_customer_address(odoo_site.id, billing_address)


#-----------------------------------------------------------------------------------------------
#this is for contractor ------------------------------------------------------------------------

    #create primary contact for contractor
    def _create_primary_contact(self, parent_id, primary_contact):
        customer = self.env['res.partner']
        values = {
                    'type' : 'other',
                    'email' : primary_contact.get('Email'),
                    'phone' : primary_contact.get('WorkPhone'),
                    'mobile' : primary_contact.get('CellPhone'),
                    'parent_id' : parent_id           
                }
        primary_contact = customer.create(values)


    def _cron_get_simpro_contractor(self):
        # === STEP 1: Use the provided token directly ===
        access_token = '37a421022e74dd11d9cfc1f000f9c6d88f8d8c2b'
        country = self.env['res.country']
        create_contractors = self.env['res.partner']
        
        # === STEP 2: API endpoint for contacts ===
        contractor_url = 'https://think-plc.simprosuite.com/api/v1.0/companies/0/contractors/'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        }
        
        params = {
            "pageSize": 50,
            "page": 1
            }

        try:
            response = requests.get(contractor_url, headers=headers, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to get Contractor: {response.text}")
            contractors = response.json()
            print('\n\n contractor',contractors)
            print('\n\n contractor',len(contractors))
        except Exception as e:
            raise Exception(f"Contractor Fetch Error: {str(e)}")

        # # === STEP 3: Create or Update Contractor in Odoo ===

        for contractor in contractors:
            external_id = contractor.get('ID')
            specific_contractor_url = f'https://think-plc.simprosuite.com/api/v1.0/companies/0/contractors/{external_id}'
            detail_res = requests.get(specific_contractor_url, headers=headers)
            if detail_res.status_code != 200:
                print(f"Failed to fetch vendors")
                continue
            data = detail_res.json() 
            print("\n\n data",data)

            existing = self.env['res.partner'].search([('x_simpro_contact_id', '=', data.get('ID')), ('is_contractor','!=', False), ('name', '=', data.get('Name'))], limit=1)
            
            if existing:
                print("Contractor Already Created",existing)
                continue

            primary_contact = data.get('PrimaryContact')
            print('\n\n primary_contact',primary_contact)
            addresh = data.get('Address')
            country_id = country.search([("name",'=',addresh.get('Country'))])

            values = {
                'x_simpro_types' : 'contractor',
                'is_contractor' : 1,
                'company_type' : 'company',
                'name': data.get('Name'),
                'street': addresh.get('Address'),
                'zip': addresh.get('PostalCode'),
                'city': addresh.get('City'),
                'country_id' : country_id.id if country_id else False,
                'x_simpro_contact_id': external_id,
                'vat' : data.get('EIN')
            }

            new_contractor = create_contractors.create(values)
            print("\n\n new_contractor",new_contractor)
            # for create attachments of vendor
            # self.get_attachments(external_id,headers,new_contractor.id,'contractor')

            ## create customer address
            if primary_contact.get('Email'):
                self._create_primary_contact(new_contractor.id, primary_contact)