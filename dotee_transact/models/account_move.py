# -*- coding: utf-8 -*-
from odoo import api, fields, models, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"
    
    period = fields.Integer('Number of months', default=1)

    dotee_total_overdue = fields.Monetary('Total Amount Overdue', compute="_total_overdue_calculation")
    
    def _total_overdue_calculation(self):
        for line in self:
            line.dotee_total_overdue = line.x_studio_total_overdue - line.amount_total
            
class AccountMoveDoteeLine(models.Model):
#     _name = 'dotee-transact.dotee-transact'
#     _description = 'dotee-transact.dotee-transact'
    _inherit = "account.move.line"

    unit_vacant = fields.Integer('Vacant Unit', digits='Product Price')
    
    # quantity = fields.Integer(string='Quantity',
    #     default=1, digits='Product Unit of Measure',
    #     help="The optional quantity expressed by this line, eg: number of product sold. "
    #          "The quantity is not a legal requirement but is very useful for some reports.")
    
    period = fields.Integer(related='move_id.period', store=True)

    x_studio_structure = fields.Char('Structure',related='product_id.x_studio_property_tariff')
    
    
#     @api.onchange ('price_unit', 'quantity', 'discount')
#     @api.depends('price_unit', 'quantity', 'discount', 'period', 'price_subtotal')
#     def _compute_period_to_total(self):
#         for line in self:
#             if(line.period > 1):
#                 self.price_subtotal = line.price_subtotal * line.period

#     @api.onchange ('unit_vacant')
#     @api.depends('price_unit', 'unit_vacant', 'price_subtotal', 'quantity', 'discount', 'price_unit_wo_discount')
#     def _compute_price(self):
#         #"""Compute the amounts of the SO line."""
#         # AccountTax = self.env['account.tax']
#         for line in self:
#             if(line.quantity < line.unit_vacant):
#                 raise ValidationError("Vacant cannot be greater than quantity.")
#             # price = AccountTax._fix_tax_included_price(line.price_unit, line.product_id.sudo().taxes_id, AccountTax)
#             # line.price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
#             # line.price_subtotal -= float(line.unit_vacant * line.price_unit)
#             line.price_unit_wo_discount = line.price_unit * (1 - (line.discount / 100.0))
#             subtotal = line.quantity * line.price_unit_wo_discount
#             line.price_subtotal = subtotal - (line.price_unit_wo_discount * line.unit_vacant)
            # price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            # if line.product_uom_qty and line.receive_in_advance:
            #     price = price - (line.receive_in_advance/line.product_uom_qty)
            # taxes = line.tax_id.compute_all(price, line.order_id.currency_id, product=line.product_id, partner=line.order_id.partner_shipping_id)
#             line.update({
#                 # 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
#                 # 'price_total': taxes['total_included'],
#                 # 'unit_vacant': line.unit_vacant,
#                 'price_subtotal': line.price_subtotal
#             })  

#     @api.model_create_multi
#     def create(self, vals_list):

#         for vals in vals_list:
#             subtotal = vals['price_subtotal'] - (vals['price_unit'] * vals['unit_vacant'])
#             period = vals['period']
#             if(period > 1):
#                     subtotal = subtotal * period
            
#             vals['price_subtotal'] = float(subtotal)
# #             raise UserError(vals['price_subtotal'])

#         lines = super(AccountMoveDoteeLine, self).create(vals_list)
        
# #         raise UserError(vals['price_subtotal'])
# #         lines = super(AccountMoveDoteeLine, self).create(vals_list)

#         moves = lines.mapped('move_id')
#         if self._context.get('check_move_validity', True):
#             moves._check_balanced()
#         moves._check_fiscalyear_lock_date()
#         lines._check_tax_lock_date()

#         return lines


#     def _get_price_total_and_subtotal(self, price_unit=None, quantity=None, discount=None, currency=None, product=None, partner=None, taxes=None, move_type=None, unit_vacant=None, period=None):
#         self.ensure_one()
#         return self._get_price_total_and_subtotal_model(
#             price_unit=price_unit or self.price_unit,
#             quantity=quantity or self.quantity,
#             discount=discount or self.discount,
#             currency=currency or self.currency_id,
#             product=product or self.product_id,
#             partner=partner or self.partner_id,
#             taxes=taxes or self.tax_ids,
#             move_type=move_type or self.move_id.type,
#             unit_vacant=unit_vacant or self.unit_vacant,
#             period=period or self.period,
#         )
    
    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        
        res = super(AccountMoveDoteeLine, self)._get_price_total_and_subtotal_model(price_unit, quantity, discount, currency, product, partner, taxes, move_type)
#         price_unit_wo_discount = res['price_unit'] * (1 - (discount / 100.0))
#         subtotal = res['price_subtotal'] - (price_unit * self.unit_vacant)
        
#         if(self.period > 1):
#                 subtotal = subtotal * self.period
# #         raise UserError(subtotal)
#         res['price_subtotal'] = subtotal
        return res
    
    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        ''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
        in some business fields (affecting the 'price_subtotal' field).

        :param price_subtotal:  The untaxed amount.
        :param move_type:       The type of the move.
        :param currency:        The line's currency.
        :param company:         The move's company.
        :param date:            The move's date.
        :return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1
        price_subtotal *= sign
        
#         raise UserError(price_subtotal)
        
#         price_subtotal = price_subtotal - float(self.price_unit *  self.unit_vacant)
        
#         if(self.period > 1):
#                 price_subtotal = price_subtotal * self.period

        if currency and currency != company.currency_id:
            # Multi-currencies.
            balance = currency._convert(price_subtotal, company.currency_id, company, date)
            return {
                'amount_currency': price_subtotal,
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
            }
        else:
            # Single-currency.
            return {
                'amount_currency': 0.0,
                'debit': price_subtotal > 0.0 and price_subtotal or 0.0,
                'credit': price_subtotal < 0.0 and -price_subtotal or 0.0,
            }

    
    # @api.depends('unit_vacant', 'price_unit', 'quantity', 'discount', 'analytic_account_id.pricelist_id')
    # def _compute_price_subtotal(self):
    #     AccountTax = self.env['account.tax']
    #     for line in self:
    #         price = AccountTax._fix_tax_included_price(line.price_unit, line.product_id.sudo().taxes_id, AccountTax)
    #         line.price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
    #         line.price_subtotal -= float(line.unit_vacant * line.price_unit)
    #         if line.analytic_account_id.pricelist_id.sudo().currency_id:
    #             line.price_subtotal = line.analytic_account_id.pricelist_id.sudo().currency_id.round(line.price_subtotal)



#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    