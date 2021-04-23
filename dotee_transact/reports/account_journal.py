import datefinder
import datetime
import time
from dateutil.relativedelta import *
from odoo import api, models, _
from odoo.exceptions import UserError

class ReportJournal(models.AbstractModel):
    _name = 'report.dotee_transact.dotee_billing_invoice'
    _description = 'Account Journal Report'
#     _inherit = 'report.account.report_journal'

    
    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': self.env['account.move'],
#             'data': data,
            'docs': self.env['account.move'].browse(docids),
#             'time': time,
            'datetime': datetime,
            'relativedelta': relativedelta,
            'datefinder': datefinder,
        }