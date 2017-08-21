# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpAdmission(models.Model):
	_inherit = 'op.admission'

	x_payment_ids = fields.One2many('account.payment', 'x_admission_id', string='Payments', store=True, domain=[('state', '!=', 'draft')])

	x_payment_state = fields.Char(string='Payment state', readonly=True, compute='_get_x_payment_state')

	@api.multi
	@api.depends('application_number', 'batch_id')
	def name_get(self):
		result = []

		for record in self:
			if record.batch_id:
				batch_name = record.batch_id.name
			else:
				batch_name = 'No batch'

			name = record.application_number + ' - ' + batch_name
			
			result.append((record.id, name))

		return result

	@api.depends('x_payment_ids')
	def _get_x_payment_state(self):
		for record in self:
		    count = len(record['x_payment_ids'])
		    if count > 0:
		        record['x_payment_state'] = '<div class="text-center"><span class="fa fa-check text-success"></span></div>'
		    else:
		        record['x_payment_state'] = '<div class="text-center"><span class="fa fa-times-circle text-danger"></span></div>'