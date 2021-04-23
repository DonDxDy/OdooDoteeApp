# -*- coding: utf-8 -*-

from odoo import api, fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import format_date, float_compare
# from odoo import models, fields, api

class Subscription(models.Model):
    _inherit = 'sale.subscription'

    period = fields.Integer('Number of months', default=1)
    
    def _prepare_dotee_invoice_data(self):
        res = self._prepare_invoice_data()
        res['period'] = self.period
        return res
        
    def _prepare_dotee_invoice_line(self, line, fiscal_position, date_start=False, date_stop=False):
        res = self._prepare_invoice_line(line, fiscal_position, date_start, date_stop)
#         if(line.period > 1):
#             res['price_unit'] = line.price_unit * line.period
        quantity = line.quantity - line.unit_vacant
        if(line.period > 1):
            quantity = quantity * line.period
        res['quantity'] = quantity
        res['unit_vacant'] = line.unit_vacant
        res['period'] = line.period
        return res
    
    def _prepare_dotee_invoice_lines(self, fiscal_position):
        self.ensure_one()
        revenue_date_start = self.recurring_next_date
        periods = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}
        revenue_date_stop = revenue_date_start + relativedelta(**{periods[self.recurring_rule_type]: self.recurring_interval}) - relativedelta(days=1)
        return [(0, 0, self._prepare_dotee_invoice_line(line, fiscal_position, revenue_date_start, revenue_date_stop)) for line in self.recurring_invoice_line_ids]

    
    def _prepare_invoice(self):
        invoice = self._prepare_dotee_invoice_data()
        invoice['invoice_line_ids'] = self._prepare_dotee_invoice_lines(invoice['fiscal_position_id'])
        return invoice

class SubscriptionLine(models.Model):
#     _name = 'dotee-transact.dotee-transact'
#     _description = 'dotee-transact.dotee-transact'
    _inherit = 'sale.subscription.line'
    
    unit_vacant = fields.Integer('Vacant Unit', required=True, digits='Product Price')
    # quantity = fields.Integer(string='Quantity', help="Quantity that will be invoiced.", default=1, digits='Product Unit of Measure')
    period = fields.Integer(related='analytic_account_id.period', store=True)
    price_subtotal = fields.Float(compute='_compute_price_subtotal', string='Subtotal', digits='Account', store=True)

    @api.onchange('period')
    @api.depends('price_unit', 'period')
    def _compute_period_price(self):
        for line in self:
            if(line.period > 1):
                line.price_unit = line.price_unit * line.period
                line.write({
                    'price_unit' : line.price_unit
                })

    @api.onchange ('unit_vacant')
    @api.depends('price_unit', 'unit_vacant', 'price_subtotal', 'quantity', 'discount', 'analytic_account_id.pricelist_id')
    def _compute_price(self):
        #"""Compute the amounts of the SO line."""
        AccountTax = self.env['account.tax']
        for line in self:
            if(line.quantity < line.unit_vacant):
                raise ValidationError("Vacant cannot be greater than quantity.")
            price = AccountTax._fix_tax_included_price(line.price_unit, line.product_id.sudo().taxes_id, AccountTax)
            subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
            subtotal = subtotal - float(line.unit_vacant * line.price_unit)
            if(line.period > 1):
                subtotal = subtotal * line.period
            line.price_subtotal = subtotal
                
            # price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            # if line.product_uom_qty and line.receive_in_advance:
            #     price = price - (line.receive_in_advance/line.product_uom_qty)
            # taxes = line.tax_id.compute_all(price, line.order_id.currency_id, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                # 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                # 'price_total': taxes['total_included'],
                #'unit_vacant': line.unit_vacant,
                'price_subtotal': line.price_subtotal
            })  

    @api.depends('unit_vacant', 'price_unit', 'quantity', 'discount', 'analytic_account_id.pricelist_id', 'period')
    def _compute_price_subtotal(self):
        AccountTax = self.env['account.tax']
        for line in self:
            price = AccountTax._fix_tax_included_price(line.price_unit, line.product_id.sudo().taxes_id, AccountTax)
            subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
            subtotal = subtotal - float(line.unit_vacant * line.price_unit)
            if(line.period > 1):
                subtotal = subtotal * line.period
            line.price_subtotal = subtotal
            
            if line.analytic_account_id.pricelist_id.sudo().currency_id:
                line.price_subtotal = line.analytic_account_id.pricelist_id.sudo().currency_id.round(line.price_subtotal)
