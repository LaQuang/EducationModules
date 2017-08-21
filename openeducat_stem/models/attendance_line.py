# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpAttendanceLine(models.Model):
	_inherit = 'op.attendance.line'

	x_partner_id = fields.Float(string='Partner id', readonly=True, compute='_get_x_partner_id')

	x_payment_state = fields.Char(string='Payment state', readonly=True, compute='_get_x_payment_state')

	x_invoice_id = fields.Many2one('account.invoice', string='Invoice', store=True, copy=True)

	@api.depends('student_id', 'batch_id')
	def _get_x_payment_state(self):
		for record in self:
		    application = self.env['op.admission'].search([('student_id', '=', record.student_id.id), ('batch_id', '=', record.batch_id.id)], limit=1)
		    if application:
		        record['x_payment_state'] = application['x_payment_state']
		    else:
		    	record['x_payment_state'] = ''

	@api.depends('student_id')
	def _get_x_partner_id(self):
		for record in self:
		    if record.student_id:
		        record['x_partner_id'] = record.student_id.commercial_partner_id.id
		    else:
		    	record['x_partner_id'] = False