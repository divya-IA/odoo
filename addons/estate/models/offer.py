import logging

from odoo import models, fields, api
from datetime import timedelta, date
from . import model


class OfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "real estate offer"
    _order = "price desc"


    price = fields.Float("Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property Id", required=True)
    validity = fields.Integer("Validity(days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date", inverse="_inverse_date")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)','The offer price must be strictly positive'),
    ]


    @api.depends("validity")
    def _compute_date(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_date(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    @api.onchange("status")
    def action_accept(self):
        for record in self:
            record.status = "accepted"
            val =model.TestModel(self.partner_id,self.price,"nm")
            self.env['estate.property'].status_accept_acttion()

            # model.TestModel.buyer=record.partner_id
            # model.TestModel.button_act(model.TestModel())
            # model.TestModel.selling_price=record.price

            # val=model.TestModel
            # val.selling_price = val.best_price
            # val.buyer = self.partner_id
        # return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        # return True
