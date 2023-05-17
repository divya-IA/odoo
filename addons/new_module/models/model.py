from odoo import models, fields, api


class Ref(models.Model):
    _name = "reference.reference"
    _description = "Reference Module"

    employee_name = fields.Many2one('hr.employee', string="Employee Name")
    report_to = fields.Many2many('hr.employee',string='Report')



    # @api.depends('report_to')
    # def _compute_employee_ids(self):
    #     for record in self:
    #         employees = self.env['hr.employee'].search([])
    #         employee_tuples = [(employee.id, employee.name) for employee in employees]
    #         record.report_to = employee_tuples


    # @api.model
    # def default_get(self, fields):
    #     res = super(Ref, self).default_get(fields)
    #     res['note'] = 'NEW Record Created'
    #     return res
    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('note'):
    #         vals['note'] = 'New Record'
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('reference.reference') or _('New')
    #     res = super(Ref, self).create(vals)
    #     return res

    # def init(self):
    #     """ Event Question main report """
    #     tools.drop_view_if_exists(self._cr, 'report_employee_new')
    #     self._cr.execute(""" CREATE VIEW report_employee_new AS (
    #                 SELECT x_employee_name, x_reference_name
    # FROM ir_module_module
    # )""")
