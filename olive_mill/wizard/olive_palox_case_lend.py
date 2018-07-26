# -*- coding: utf-8 -*-
# Copyright 2018 Barroux Abbey (https://www.barroux.org/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class OlivePaloxCaseLend(models.TransientModel):
    _name = 'olive.palox.case.lend'
    _description = 'Wizard to Lend Olive Palox and/or Cases'

    partner_id = fields.Many2one(
        'res.partner', string='Olive Farmer', required=True)
    palox_ids = fields.Many2many(
        'olive.palox', string='Lended Palox',
        domain=[('borrower_partner_id', '=', False)])
    regular_case_qty = fields.Integer(string='Lended Case Qty')
    organic_case_qty = fields.Integer(string='Lended Organic Case Qty')

    def validate(self):
        self.ensure_one()
        if self.palox_ids:
            self.palox_ids.write({
                'borrower_partner_id': self.partner_id.id,
                'borrowed_date': fields.Date.context_today(self),
                })
        if self.regular_case_qty < 0 or self.organic_case_qty < 0:
            raise UserError(_(
                "The quantity of cases to lend must be positive"))
        if self.regular_case_qty > 0 or self.organic_case_qty > 0:
            self.env['olive.lended.case'].create({
                'partner_id': self.partner_id.id,
                'regular_qty': self.regular_case_qty,
                'organic_qty': self.organic_case_qty,
                })
        return
