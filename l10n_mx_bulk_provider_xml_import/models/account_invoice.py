# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    filter_product_code = fields.Char()
    filter_product_name = fields.Char()

    @api.onchange('filter_product_code')
    def _onchange_filter_product_code(self):

        result = {}

        if self.filter_product_code:
            search_domain = [('default_code', '=', self.filter_product_code)]
            domain = {
                'product_id': search_domain,
            }
            result['domain'] = domain

        return result