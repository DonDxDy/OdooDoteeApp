# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HousingStructures(models.Model):
    _name = 'dotee_transact.res.partner.housing_structures'
    _description = 'Housing Structures'

    name = fields.Char()
    allow_discounts = fields.Boolean("Allow Discounts")
    balanta = fields.Char()
    discount_age = fields.Float(store=True)
    discount_amount = fields.Float(store=True, compute="_calculate_discount", default = 0.00)
    list_price = fields.Float(store=True, compute="_calculate_list_price")
    product_id = fields.Many2one('product.template', string='Product', Index=True)
    property_category = fields.Char()
    unit = fields.Integer()
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True)
    unit_audit = fields.Integer()
    unit_price = fields.Monetary()
    subtotal = fields.Monetary(compute="_calculate_subtotal", store=True)
    total_price = fields.Monetary(compute="_calculate_total_price", store=True)
    unoccupied = fields.Integer()
    unoccupied_audit = fields.Integer()
    property_type = fields.Selection([], string = 'Type', readonly=True, track_visibility='always')

    @api.depends('unit', 'unit_price')
    def _calculate_subtotal(self):
        for record in self:
            record.subtotal = float(record.unit * record.unit_price)

    @api.depends('subtotal', 'discount_amount')
    def _calculate_total_price(self):
        for record in self:
            record.total_price = float(record.subtotal - record.discount_amount)

    @api.depends('unoccupied', 'discount_age', 'list_price')
    def _calculate_discount(self):
        for record in self: 
            record.discount_amount = float((record.unit - record.unoccupied) * ((record.discount_age/100.0) * record.list_price))

    @api.depends('product_id')
    def _calculate_list_price(self):
        for record in self: 
            record.list_price = record.product_id.list_price

