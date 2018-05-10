# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    currency_id = fields.Many2one('res.currency', 'Currency', related='product_id.product_tmpl_id.company_id.currency_id')

    production_unit_price = fields.Monetary("Total Unit Price", currency_field='currency_id', compute='_compute_production_costs')
    total_reserved_price = fields.Monetary("Total Reserved Price", currency_field='currency_id', compute='_compute_production_costs')
    total_pending_price = fields.Monetary("Total Pending Price", currency_field='currency_id', compute='_compute_production_costs')
    total_production_price = fields.Monetary("Total Price", currency_field='currency_id', compute='_compute_production_costs')

    @api.one
    @api.depends('product_id', 'product_qty', 'move_raw_ids')
    def _compute_production_costs(self):
        ReportDataModel = self.env['report.mrp_production_cost.mrp_production_cost_report']

        result = ReportDataModel.get_data(self)

        if result:

            data = result['orders'][0]

            self.total_production_price = data.get('total')
            self.total_reserved_price = data.get('total_reserved_price')
            self.total_pending_price = data.get('total_pending_price')
            self.production_unit_price = data.get('unit_total')

