from odoo import models, fields, api


class InheritModel(models.Model):
    # _name = "res.users"
    _inherit = "res.users"

    property_ids = fields.Many2many("estate.property", "user_ids", string="property ids")

    # @api.depends('agreement_school')
    # def _compute_property(self):
    #     stud_obj = self.env['estate.property']
    #     for agreement in self:
    #         stud_ids = stud_obj.search([('school', '=', agreement.agreement_school.id)]).ids
    #         agreement.student_ids = [(6, 0, stud_ids)]


