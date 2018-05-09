# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MrpProductionCost(models.AbstractModel):
    _name = 'report.mrp_production_cost.mrp_production_cost_report'

    @api.multi
    def get_data(self, productions):
        product_lines = []

        for mo in productions:

            bom = mo.bom_id

            attributes = []
            for value in mo.product_id.attribute_value_ids:
                attributes += [(value.attribute_id.name, value.name)]

            product_line = {'order': mo, 'bom': bom, 'name': mo.product_id.name,
                            'lines': [],
                            'available_lines': [],
                            'pending_lines': [],
                            'total': 0.0,
                            'unit_total': 0.0,
                            'total_reserved_price': 0.0,
                            'total_pending_price': 0.0,
                            'currency': self.env.user.company_id.currency_id,
                            'product_uom_qty': mo.product_qty,
                            'product_uom': bom.product_uom_id,
                            'attributes': attributes}

            for move in mo.move_raw_ids:
                product = move.product_id

                price_uom = move.product_uom._compute_price(product.standard_price, move.product_uom)

                line = {
                    'product_id': product,
                    'product_uom_qty': move.product_qty,
                    'reserved_qty': move.reserved_availability,
                    'pending_qty': move.product_qty - move.reserved_availability,
                    'product_uom': move.product_uom,
                    'price_unit': price_uom,
                    'total_price': price_uom * move.product_qty,
                    'total_reserved_price': price_uom * move.reserved_availability,
                    'total_pending_price': price_uom * (move.product_qty - move.reserved_availability),
                }

                product_line['lines'] += [line]

                product_line['total'] += line['total_price']
                product_line['unit_total'] += line['price_unit']
                product_line['total_reserved_price'] += line['total_reserved_price']
                product_line['total_pending_price'] += line['total_pending_price']

            product_lines += [product_line]

        return product_lines

    @api.model
    def get_report_values(self, docids, data=None):
        productions = self.env['mrp.production'].browse(docids)
        res = self.get_data(productions)
        return {'lines': res}
