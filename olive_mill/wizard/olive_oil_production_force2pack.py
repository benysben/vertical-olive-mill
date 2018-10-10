# -*- coding: utf-8 -*-
# Copyright 2018 Barroux Abbey (https://www.barroux.org/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

MIN_RATIO = 5
MAX_RATIO = 35


class OliveOilProductionForce2Pack(models.TransientModel):
    _name = 'olive.oil.production.force2pack'
    _description = 'Olive Oil Production Force2Pack'

    olive_oil_production_id = fields.Many2one(
        'olive.oil.production', string='Olive Oil Production', required=True)
    palox_id = fields.Many2one(
        related='olive_oil_production_id.palox_id', readonly=True)
    oil_product_id = fields.Many2one(
        related='olive_oil_production_id.oil_product_id', readonly=True)
    global_ratio = fields.Float(
        related='olive_oil_production_id.ratio', readonly=True,
        string='Global Ratio')
    arrival_line_id = fields.Many2one(
        'olive.arrival.line', required=True, string='Production Line')
    force_ratio = fields.Float(
        string='Force Ratio', digits=dp.get_precision('Olive Oil Ratio'),
        required=True)

    def validate(self):
        self.ensure_one()
        prod = self.olive_oil_production_id
        line = self.arrival_line_id
        assert line.production_id == prod, 'Line not attached to production'
        if self.force_ratio > MAX_RATIO or self.force_ratio < MIN_RATIO:
            raise UserError(_(
                "The ratio (%s) is not realistic.") % self.ratio)
        prod.set_qty_on_lines(
            force_ratio=(self.arrival_line_id, self.force_ratio))
        prod.force2pack()
        return True