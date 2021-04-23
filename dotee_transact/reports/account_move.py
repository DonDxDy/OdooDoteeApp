from odoo import api, models
from odoo.exceptions import AccessError, UserError, ValidationError

class DebtorReport(models.AbstractModel):
    _name = 'report.dotee_transact.debtor_report_invoice'
    _description = 'Debtor Report'
    
#     def partner_invoices(self, data):
#         debtor_list = []
        
#         query = """
#             select "street".x_name, "partner".x_customer_payment_id, "partner".name, "partner".street,  "partner".x_studio_computed_charge, to_char("partner".x_studio_last_payment_date,'DD-MON-YYYY'), "partner".x_studio_last_payment_date, sum(partner.x_studio_arrears)
#             FROM res_partner partner
#             INNER JOIN x_res_country_state_province_ward_street street ON "street".id = "partner".x_studio_analytics_street
#             where "partner".x_studio_arrears > 0
#             group by rollup(street.x_name), partner.x_customer_payment_id, partner.name, partner.street, partner.x_studio_computed_charge, partner.x_studio_last_payment_date
#             ORDER BY street.x_name"""
#         self.env.cr.execute(query)
#         res = self.env.cr.dictfetchall()
#         return res
    
    def streets(self, data):
        params = [self.env.company.id]
        query = """select id, x_name as name from x_res_country_state_province_ward_street 
        where id in (select x_studio_analytics_street from res_partner where x_studio_arrears > 0 and company_id = %s)
        group by id, x_name order by x_name
        """
        
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res

    def lines(self, data, partner_id):
        params = [partner_id, self.env.company.id]
        query = """select x_customer_payment_id as payment_id, name, street, x_studio_full_house_structure as property_structure, x_studio_computed_charge as computed_charge, x_studio_last_payment_date as last_payment_date, case when x_studio_last_payment_date IS NULL then 0.00 ELSE x_studio_last_payment_amount end as last_payment_amount, x_studio_arrears as arrears
        from res_partner 
        where x_studio_analytics_street = %s and x_studio_arrears > 0 and company_id = %s
        """
        
        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()
        return res
    
    def sum_arrears_total(self, data, partner_id, field):
        params = [partner_id, self.env.company.id]
        query = """select sum(""" + field + """) as total_arrears from res_partner
        where  x_studio_analytics_street = %s and x_studio_arrears > 0 and company_id = %s"""
        self.env.cr.execute(query, tuple(params))
        
        contemp = self.env.cr.fetchone()
        if contemp is not None:
            result = contemp[0] or 0.0
        return result
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
#         if not data.get('form'):
#             raise UserError(_("Form content is missing, this report cannot be printed."))
            
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner.debtor.wizard',
            'docs': self.env['res.partner.debtor.wizard'].browse(docids),
            'data': data,
            'streets': self.streets,
            'lines': self.lines,
            'sum_arrears_total': self.sum_arrears_total,
            'company': self.env.company

        }