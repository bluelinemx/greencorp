# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MrpProductionCost(models.AbstractModel):
    _name = 'report.mrp_production_cost.mrp_production_cost_report'

    @api.multi
    def get_data(self, productions):

        data = {
            'lines': [],
            'total': 0,
            'reserved_price': 0,
            'pending_price': 0,
            'currency': self.env.user.company_id.currency_id
        }

        product_lines = []
        PurchaseOrder = self.env['purchase.order'].sudo()

        for mo in productions:

            bom = mo.bom_id

            attributes = []
            for value in mo.product_id.attribute_value_ids:
                attributes += [(value.attribute_id.name, value.name)]

            product_line = {'order': mo, 'bom': bom, 'name': mo.product_id.name,
                            'lines': [],
                            'product_id': mo.product_id,
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

                seller_price = None

                self.env.cr.execute("select purchase_order.partner_id, price_unit from purchase_order_line INNER JOIN purchase_order ON (purchase_order.id=purchase_order_line.order_id) WHERE product_id=%s AND purchase_order.state IN ('purchase', 'done') ORDER BY purchase_order.id DESC LIMIT 1" % (product.id, ))

                item = self.env.cr.fetchone()

                if item:
                    seller_price = item[1]
                elif len(product.seller_ids) > 0:
                    seller_price = product.seller_ids[-1].price

                product_price = seller_price if seller_price is not None else product.standard_price
                price_uom = move.product_uom._compute_price(product_price, move.product_uom)

                lot_names = ','.join(
                    [lot for lot in move.active_move_line_ids.mapped('lot_id').mapped('name') if lot is not False])

                line = {
                    'product_id': product,
                    'lot_names': lot_names,
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

            data['total'] += product_line['total']
            data['reserved_price'] += product_line['total_reserved_price']
            data['pending_price'] += product_line['total_pending_price']

            product_lines += [product_line]

        data['lines'] = product_lines

        return data

    @api.model
    def get_report_values(self, docids, data=None):
        productions = self.env['mrp.production'].browse(docids)
        data = self.get_data(productions)
        return data
