from odoo import models, fields, api
import requests

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def trigger_csv_export(self):
        production_url = self.env['ir.config_parameter'].sudo().get_param('ehcs_n8n_configuration.production_url') 
        if production_url:
            for record in self:
                if record.state == 'done' and record.picking_type_id.code == 'outgoing' and record.sale_id:
                    person_full_name = record.name
                    company = record.company_id.name
                    sipping_city = record.partner_id.city
                    shiping_address = record.partner_id.name
                    phone = record.partner_id.phone
                    total_weight = record.weight_bulk
                    sale_order_number = record.sale_id.name
                    data = {
                        "person_full_name": person_full_name or '',
                        "company": company or '',
                        "sipping_city": sipping_city or '',
                        "shiping_address": shiping_address or '',
                        "phone": phone or '',
                        "total_weight": total_weight or '',
                        "sale_order_number": sale_order_number or '',
                        "id": record.id,
                    }
                    response = requests.post(production_url, json=data)
                    if response.status_code != 200:
                        raise Warning("\nFailed to trigger CSV export: \n" + response.text)

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.trigger_csv_export()
        return res
