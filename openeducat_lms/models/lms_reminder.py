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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import models, fields


class MaterialReminder(models.Model):
    _name = 'material.reminder'

    date = fields.Date('Sent Date')
    material_id = fields.Many2one('op.material', 'Material')
    course_id = fields.Many2one('op.course', 'Course')
    enrollment_id = fields.Many2one('op.course.enrollment', 'Enrollment')
    user_id = fields.Many2one('res.users', 'User')
    template_id = fields.Many2one('mail.template', 'Emails')

    def get_base_domain(self):
        return self.env['ir.config_parameter'].get_param('web.base.url')

    def send_reminder(self):
        material_ids = self.env['op.material'].search(
            [('auto_publish', '=', True)])
        today_date = datetime.today().date()
        template_id = self.env.ref(
            'openeducat_lms.email_template_material_publish_mail')
        url = self.get_base_domain() + '/my-courses'
        for material in material_ids:
            course_material_ids = self.env['op.course.material'].search(
                [('material_id', '=', material.id)])
            course_ids = []
            str1 = "<p>Hello,</p><p>"
            str2 = " has been published.<br></p> "
            str4 = "<a href='%s' target='_blank'>%s</a>" % (url, url)
            str3 = "material '%s'" % material.name
            mail_html = str1 + str3 + str2 + str4
            if material.auto_publish_type == 'wait_until':
                date = material.wait_until_date

                if str(today_date) == str(date):

                    for cmaterial in course_material_ids:
                        course_ids.append(cmaterial.section_id.course_id.id)
                    enrollment_ids = self.env['op.course.enrollment'].search(
                        [('course_id', 'in', course_ids)])
                    for enrollment in enrollment_ids:
                        reminder_ids = self.env['material.reminder'].search(
                            [('enrollment_id', '=', enrollment.id),
                             ('material_id', '=', material.id)])
                        if reminder_ids:
                            continue
                        user_email = enrollment.user_id.partner_id.email or ''
                        template_id.email_to = user_email
                        template_id.body_html = mail_html
                        template_id.subject = "'%s' Now Available" % material.name
                        template_id.send_mail(enrollment.id, force_send=True)
                        self.env['material.reminder'].create({
                            'enrollment_id': enrollment.id,
                            'course_id': enrollment.course_id.id,
                            'user_id': enrollment.user_id.id,
                            'material_id': material.id,
                            'date': datetime.today().date(),
                            'template_id': template_id.id
                        })
            elif material.auto_publish_type == 'wait_until_duration':
                for cmaterial in course_material_ids:
                    course_ids.append(cmaterial.section_id.course_id.id)
                enrollment_ids = self.env['op.course.enrollment'].search(
                    [('course_id', 'in', course_ids)])
                for enrollment in enrollment_ids:

                    reminder_ids = self.env[
                        'material.reminder'].search(
                        [('enrollment_id', '=', enrollment.id),
                         ('material_id', '=', material.id)])
                    if reminder_ids:
                        continue
                    temp = False
                    days = 0
                    if material.wait_until_duration_period == 'minutes':
                        if material.wait_until_duration:
                            days = int(material.wait_until_duration / 1440)
                    elif material.wait_until_duration_period == 'hours':
                        if material.wait_until_duration:
                            days = int(material.wait_until_duration / 24)
                    elif material.wait_until_duration_period == 'days':
                        days = material.wait_until_duration or 0
                    elif material.wait_until_duration_period == 'weeks':
                        if material.wait_until_duration:
                            days = int(material.wait_until_duration * 7)
                    if days > 0:
                        enroll_date = (
                            datetime.strptime(
                                enrollment.enrollment_date,
                                '%Y-%m-%d %H:%M:%S') + timedelta(
                                days=1)).date()
                        if str(enroll_date) == str(today_date):
                            temp = True
                    month = 0
                    if material.wait_until_duration_period == 'months':
                        month = material.wait_until_duration or 0
                    elif material.wait_until_duration_period == 'years':
                        if material.wait_until_duration:
                            month = material.wait_until_duration * 12
                    if month > 0:
                        enroll_date = (
                            datetime.strptime(
                                enrollment.enrollment_date,
                                '%Y-%m-%d %H:%M:%S') + relativedelta(
                                months=month)).date()
                        if str(enroll_date) == str(today_date):
                            temp = True
                    if temp:
                        user_email = enrollment.user_id.partner_id.email or ''
                        template_id.email_to = user_email
                        template_id.body_html = mail_html
                        template_id.subject = "'%s' Now Available" % material.name
                        template_id.send_mail(enrollment.id, force_send=True)
                        self.env['material.reminder'].create({
                            'enrollment_id': enrollment.id,
                            'course_id': enrollment.course_id.id,
                            'user_id': enrollment.user_id.id,
                            'material_id': material.id,
                            'date': datetime.today().date(),
                            'template_id': template_id.id
                        })
