from odoo import models, fields


class TypeModel(models.Model):
    _name = "estate.property.type"
    _description = "real estate type"
    _order = "sequence"

    sequence=fields.Integer("Sequence" ,default=1)
    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "model_id")

    _sql_constraints = [
        ('uniq_name',
         'UNIQUE (Name)',
         'A property type already exists !')]

