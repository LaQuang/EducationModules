# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api


class OpCourseEnrollment(models.Model):

    _name = "op.course.enrollment"
    _rec_name = "user_id"

    course_id = fields.Many2one('op.course', 'Course')
    navigation_policy = fields.Selection(related='course_id.navigation_policy',
                                         string='Navigation Policy')
    user_id = fields.Many2one('res.users', 'User')
    enrollment_date = fields.Datetime('Enrollment Date',
                                      default=fields.Datetime.now())
    completion_date = fields.Datetime('Completion Date')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'In Progress'),
                              ('done', 'Done')],
                             'State', default='draft')
    enrollment_material_line = fields.One2many('op.course.enrollment.material',
                                               'enrollment_id',
                                               string='Materials',
                                               order='sequence asc')
    completed_percentage = fields.Integer(
        compute="_compute_completed_percentage", string="Completed Percentage",
        store=True)

    @api.multi
    @api.depends('course_id.training_material', 'enrollment_material_line')
    def _compute_completed_percentage(self):
        for enrollment in self:
            if not enrollment.course_id.training_material == 0:
                enrollment.completed_percentage = (len(
                    enrollment.enrollment_material_line) * 100) / enrollment.course_id.training_material
            else:
                enrollment.completed_percentage = 0


class OpCourseEnrollmentMaterial(models.Model):

    _name = 'op.course.enrollment.material'
    _rec_name = 'enrollment_id'

    enrollment_id = fields.Many2one('op.course.enrollment', 'Enrollment',
                                    ondelete='cascade')
    course_id = fields.Many2one(
        related='enrollment_id.course_id', string='Course')
    section_id = fields.Many2one('op.course.section', 'Section')
    material_id = fields.Many2one('op.material', 'Material')
    completed = fields.Boolean('Completed')
    completed_date = fields.Datetime('Completed Time')
    last_access_date = fields.Datetime('Last Access Time')
