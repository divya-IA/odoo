from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError


class TestModel(models.Model):
    _name = "estate.property"
    _description = "real estate module"
    _order = "id desc"
    # _inherit="res.users.inherit"

    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date Availability", default=date.today() + timedelta(days=90),
                                    copy=False)  # date formate is %y-%m-%d
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area(sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area(sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean("Active")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sales_person = fields.Many2one('res.users', string='Salesman', index=True, default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer ids")
    estate_tag_ids = fields.Many2many("estate.property.tag",relation="estate_property_estate_tag_ids", string="tags")
    total_area = fields.Float("Total Area(sqm)", compute="_compute_total")
    best_price = fields.Float("Best Offer", compute="_compute_best_price", stored=True)
    selling_price = fields.Float("Selling Price", copy=False, compute="status_accept_acttion")

    model_id = fields.Many2one("estate.property.type")
    name = fields.Char("Title", required=True)
    expected_price = fields.Float("Expected Price", required=True, store=True)
    state = fields.Selection(string="State", required=True, copy=False, store=True,
                             selection=[('new', 'New'), ('offerRc', 'Offer Received'), ('offerAc', 'Offer Accepted'),
                                        ('sold', 'Sold'), ('canceled', 'Canceled')], default='new')
    user_ids=fields.Many2one("res.users",string="User ids")

    _sql_constraints = [
        ('check_expected', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive')
    ]

    @api.depends('agreement_school')
    def _compute_students(self):
        stud_obj = self.env['abby.student']
        for agreement in self:
            # Search students belongs to the school of the agreement
            stud_ids = stud_obj.search([('school', '=', agreement.agreement_school.id)]).ids
            agreement.student_ids = [(6, 0, stud_ids)]
    # @api.ondelete(at_uninstall=False)
    # def _unlink_if_user_inactive(self):
    #     for data in self:
    #         if data.state != "new" and data.state != "canceled":
    #             raise UserError("only new or canceled can delete")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            data = list(record.offer_ids.mapped('price'))
            max = 0
            for i in data:
                if i > max:
                    max = i
            record.best_price = max
        return True

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError('Canceled can not be Sold')

    def action_set_cancel(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError('Sold can not be Canceled')

    @api.depends("offer_ids.price")
    def status_accept_acttion(self):
        max = 0
        data = list(self.offer_ids.mapped('price'))
        for i in data:
            if i > max:
                max = i
        self.selling_price = max
        data2 = list(self.mapped('offer_ids'))
        for i in data2:
            if i.price == max:
                self.buyer = i.partner_id
        return True

    # @api.constrains('expected_price')
    # def _check_expected_price(self):
    #     for record in self:
    #         if ((90/record.expected_price)*100) > record.selling_price:
    #             raise ValidationError("The selling price cannot less then 90% of expected price")
    # _constraints = [
    #     (_check_expected_price, 'The selling price cannot less then 90% of expected price.', ['expected_price'])
    # ]
