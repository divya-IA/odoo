from odoo import models, fields


class TagModel(models.Model):
    _name = "estate.property.tag"
    _description="real estate tag"
    _order = "name asc"


    name = fields.Char("Name", required=True)
    # color=fields.Integer("Color")
    _sql_constraints = [
        ('uniq_name',
         'UNIQUE (Name)',
         ' this tag already exists !')]