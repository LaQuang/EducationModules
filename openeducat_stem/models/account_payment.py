# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_payment(models.Model):
	_inherit = 'account.payment'

	x_admission_id = fields.Many2one('op.admission', string='Application', store=True, copy=True)