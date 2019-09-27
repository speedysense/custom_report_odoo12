# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class SaleSummaryReportWizard(models.TransientModel):
    _name = 'sale.summary.report.wizard'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start, 'date_end': self.date_end,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report_odoo12.sale_summary_report').report_action(
            self, data=data)


class ReportSaleSummaryReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_odoo12.sale_summary_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']

        SO = self.env['sale.order']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        docs = []
        while start_date <= end_date:
            date = start_date
            start_date += delta

            print(date, start_date)
            orders = SO.search([
                ('confirmation_date', '>=', date.strftime(DATETIME_FORMAT)),
                ('confirmation_date', '<', start_date.strftime(DATETIME_FORMAT)),
                ('state', 'in', ['sale', 'done'])
            ])

            total_orders = len(orders)
            amount_total = sum(order.amount_total for order in orders)

            docs.append({
                'date': date.strftime("%Y-%m-%d"),
                'total_orders': total_orders,
                'amount_total': amount_total,
                'company': self.env.user.company_id
            })

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }
