from odoo import models, fields, api, _
from datetime import datetime, date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
    think_job_number = fields.Char('Job Number',copy=False,readonly=True,default=lambda self: ('')) 
    site_id = fields.Many2one('plc.sites', 'Site', domain="[('customer_id', '=', partner_id)]")

    # def write(self,vals):
    #     res = super(SaleOrder, self).write(vals)
    #     if 'x_studio_job_project_type' in vals:
    #         for rec in self:
    #             if rec.state == 'sale':
    #                 next_seq = self.env['ir.sequence'].next_by_code('think.job.number') or _('')
    #                 current_year = datetime.now().year
    #                 t_j_n = self.x_studio_job_project_type
    #                 self.think_job_number = (f'{t_j_n}{current_year}{next_seq}')        
    #     return res

    def action_confirm(self):
        Project = self.env['project.project']
        if self.x_studio_job_project_type:
            t_j_n = self.x_studio_job_project_type
            next_seq = self.env['ir.sequence'].next_by_code('think.job.number') or _('')
            current_year = datetime.now().year
            self.think_job_number = (f'{t_j_n}{current_year}{next_seq}')
            project_only_sol_count = self.env['sale.order.line'].search_count([
                ('order_id', '=', self.id),
                ('product_id.service_tracking', 'in', ['project_only', 'task_in_project']),
            ])
            if project_only_sol_count == 0:
                new_project = Project.create({
                    'name' : self.think_job_number,
                    'reinvoiced_sale_order_id' : self.id,
                    'sale_order_id' : self.id,
                    'x_studio_job_project_type' : self.x_studio_job_project_type,
                    'think_job_number' : self.think_job_number
                    })
                self.project_id = new_project.id
        res =  super(SaleOrder, self).action_confirm()
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _timesheet_create_project_prepare_values(self):
        """Generate project values"""
        # create the project or duplicate one
        if self.order_id.x_studio_job_project_type:
            name = self.order_id.think_job_number
        else:
            name = '%s - %s' % (self.order_id.client_order_ref, self.order_id.name) if self.order_id.client_order_ref else self.order_id.name
        
        return {
            'name': name,
            'account_id': self.env.context.get('project_account_id') or self.order_id.project_account_id.id or self.env['account.analytic.account'].create(self.order_id._prepare_analytic_account_data()).id,
            'partner_id': self.order_id.partner_id.id,
            'sale_line_id': self.id,
            'active': True,
            'company_id': self.company_id.id,
            'allow_billable': True,
            'user_id': self.product_id.project_template_id.user_id.id,
            'think_job_number': self.order_id.think_job_number,
            'x_studio_job_project_type': self.order_id.x_studio_job_project_type,
        }

    def _timesheet_create_project(self):
        """ Generate project for the given so line, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        values = self._timesheet_create_project_prepare_values()
        project_template = self.product_id.project_template_id
        if project_template:
            if self.order_id.x_studio_job_project_type:
                values['name'] = self.order_id.think_job_number
            else:
                values['name'] = "%s - %s" % (values['name'], project_template.name)
            project = project_template.copy(values)
            project.tasks.write({
                'sale_line_id': self.id,
                'partner_id': self.order_id.partner_id.id,
            })
            # duplicating a project doesn't set the SO on sub-tasks
            project.tasks.filtered('parent_id').write({
                'sale_line_id': self.id,
                'sale_order_id': self.order_id.id,
            })
        else:
            project_only_sol_count = self.env['sale.order.line'].search_count([
                ('order_id', '=', self.order_id.id),
                ('product_id.service_tracking', 'in', ['project_only', 'task_in_project']),
            ])
            if project_only_sol_count == 1:
                if self.order_id.x_studio_job_project_type:
                    values['name'] = values['name'] = self.order_id.think_job_number
                else:
                    values['name'] = "%s - [%s] %s" % (values['name'], self.product_id.default_code, self.product_id.name) if self.product_id.default_code else "%s - %s" % (values['name'], self.product_id.name)
            values.update(self._timesheet_create_project_account_vals(self.order_id.project_id))
            project = self.env['project.project'].create(values)

        # Avoid new tasks to go to 'Undefined Stage'
        if not project.type_ids:
            project.type_ids = self.env['project.task.type'].create([{
                'name': name,
                'fold': fold,
                'sequence': sequence,
            } for name, fold, sequence in [
                (_('To Do'), False, 5),
                (_('In Progress'), False, 10),
                (_('Done'), False, 15),
                (_('Cancelled'), True, 20),
            ]])

        # link project as generated by current so line
        self.write({'project_id': project.id})
        project.reinvoiced_sale_order_id = self.order_id
        return project