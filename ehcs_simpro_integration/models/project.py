from odoo import api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    x_studio_job_project_type = fields.Selection([
        ('SE', 'SE Service'),
        ('PR', 'PR Electro/Mech Automation Project'),
        ('PA', 'PA Parts Only'),
        ('BP', 'BP Build to print'),
        ('EL', 'EL Automation Project - Electrical'),
        ('ME', 'ME Automation Project - Mechanical'),
        ('TR', 'TR Training'),
        ('WA', 'WA Warranty repair'),
    ], string='Job / Project Type')
    think_job_number = fields.Char('Job Number', readonly=True)
    sale_partner_id = fields.Many2one('res.partner','Customer')
    sale_id = fields.Many2one('sale.order','Sale order')
    primary_customer = fields.Many2one('res.partner', 'Primary contact', domain=[('type','=','contact'),('is_contact', '=', True)])
    is_customize_proj_create = fields.Boolean()
    quotes_name = fields.Char(compute='_compute_quote_name')

    def _compute_quote_name(self):
        for rec in self:
            rec.quotes_name = ''
            if rec.reinvoiced_sale_order_id:
                rec.quotes_name = rec.reinvoiced_sale_order_id.quote_name
            if rec.sale_id:
                rec.quotes_name = rec.sale_id.quote_name


# class ProjectTask(models.Model):
#     _inherit = "project.task"

#     @api.model
#     def create(self, vals):
#         res = super(ProjectTask, self).create(vals)
#         if vals.get('partner_id'):
#             customer_folder = self.env['documents.document'].search([
#                 ('type', '=', 'folder'),
#                 ('customer_id', '=', vals.get('partner_id')),
#                 ('name', '=', 'Job')], limit=1)
#             if customer_folder:
#                 site_folder = self.env['documents.document'].create({
#                     'type' : 'folder',
#                     'active' : True,
#                     'name' : vals.get('name'),
#                     'customer_id' : res.id,
#                     'folder_id' : customer_folder.id,
#                 })
#         return res
