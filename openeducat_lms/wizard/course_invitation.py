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


class CourseInvitation(models.TransientModel):
    _name = 'course.invitaiton'

    user_ids = fields.Many2many(
        'res.users', 'user_course_invitation_rel', 'invitation_id', 'user_id',
        'Users')

    @api.one
    def send_invitation(self):
        parameter = self.env['ir.config_parameter'].sudo().search(
            [('key', '=', 'web.base.url')])
        url = parameter[0].value
        course_url = url + '/courses'
        template_id = self.env.ref(
            'openeducat_lms.email_template_course_invitation_mail')
        user_email = ''
        user = self.env['res.users'].browse(self.env.uid)
        active_id = self.env.context.get('active_id', False)
        course = self.env['op.course'].browse(active_id)
        for user in self.user_ids:
            if user.partner_id and user.partner_id.email:
                if user_email:
                    user_email = user_email + ',' + user.partner_id.email
                else:
                    user_email = user.partner_id.email
        if user_email:
            template_id.email_to = user_email
            body_html = "<p>Hello,</p>\n<p>You are invited from %s to " \
                        "Enroll Course: '%s' .</p>\n%s" % (user.name,
                                                           course.name,
                                                           course_url)
            template_id.body_html = body_html
            template_id.send_mail(active_id, force_send=True)
        user_ids = course.invited_users_ids.ids
        invite_uid = self.user_ids.ids
        total_invite_uid = list(set(user_ids + invite_uid))
        course.invited_users_ids = [[6, 0, total_invite_uid]]
        return True
