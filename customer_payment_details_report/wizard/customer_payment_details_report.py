from odoo import api, fields, models, _
from odoo.exceptions import Warning


class CustomerPaymentDetailsReport(models.Model):
    _name = 'customer.payment.details.report'

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    def customer_payment_details_report_xlsx(self):
        date_from = self.from_date.strftime('%d-%m-%Y')
        date_to = self.to_date.strftime('%d-%m-%Y')

        if self.from_date > self.to_date:
            raise Warning(_("From Date is GreaterThan To Date"))
        else:
            filter_cdtn = ''' where am.move_type = 'out_invoice' and
                 am.invoice_date between '%s' AND '%s'
                 ''' % (date_from, date_to)

            query = '''SELECT rp.name as partner_name, count(am.id) as total_sale_count, sum(am.amount_total_signed) as total,
                        (sum(am.amount_total_signed)-sum(am.amount_residual_signed)) as paid_amount, sum(am.amount_residual_signed) as balance_amount,
                        MIN(am.invoice_date) AS first_invoice_date
                        FROM account_move as am
                        left join res_partner as rp on rp.id = am.partner_id
                        %s
                        group by(rp.name) ''' % (filter_cdtn)

            self._cr.execute(query)
            account_move_ids = self._cr.dictfetchall()


            data = {
                'ids': self.ids,
                'model': self._name,
                'form_data':account_move_ids,
                'start': date_from,
                'end':date_to,
                'company_name': self.company_id.name,
                'com_street': self.company_id.street,
                'com_street2': self.company_id.street2,
                'com_city': self.company_id.city,
                'com_state': self.company_id.state_id.name,
                'com_zip': self.company_id.zip,
                'com_country': self.company_id.country_id.name,
                'com_phone': self.company_id.phone,
                'com_email': self.company_id.email,
            }

            return self.env.ref('customer_payment_details_report.customer_payment_details_report_pdf').report_action(self, data=data)

