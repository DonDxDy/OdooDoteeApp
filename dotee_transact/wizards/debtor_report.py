# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ProjectCreateSalesOrderInherit(models.TransientModel):
    _name = 'res.partner.debtor.wizard'
    _description = 'Debtor Report Wizard'
    
    report_type = fields.Selection([
        ('report_1', 'Debtor Detail List'),
        ('report_2', 'Debtor Summary List')
    ])
    start_date = fields.Date()
    end_date = fields.Date()
    
    def print_report(self):
#         data = {

# #             'ids': self.ids,

# #             'model': self.env['res.partner'],

#             'form': {
#                 'report_type': self.report_type,

#                 'start_date': self.start_date,

#                 'end_date': self.end_date,

#             },

#         }
        return self.env.ref('dotee_transact.dotee_debtor_report').report_action(self)