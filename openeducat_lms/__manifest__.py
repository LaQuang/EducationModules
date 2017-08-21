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

{
    'name': 'OpenEduCat LMS',
    'version': '1.0.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'LMS',
    'complexity': "easy",
    'description': """
        This module provide feature of LMS.
    """,
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': ['openeducat_core', 'website_portal', 'website_mail', 'rating',
                'openeducat_quiz', 'auth_signup'],
    'data': [
        'security/op_lms_security.xml',
        'security/ir.model.access.csv',
        'wizard/course_invitation_view.xml',
        'data/course_invitation.xml',
        'data/material_reminder.xml',
        'views/quiz_view.xml',
        'views/assets.xml',
        'views/course_catagory_view.xml',
        'views/course_view.xml',
        'views/faculty_view.xml',
        'views/course_detail.xml',
        'views/course_material.xml',
        'views/course_enrollment_view.xml',
        'views/website_lms.xml',
        'views/lms_embed.xml',
        'views/material_version_embed.xml',
        'views/rating_template.xml',
        'dashboard/openeducat_lms_dashboard_view.xml',
        'views/menu_view.xml',
        'views/material_detail_view.xml',
        'views/my_courses.xml',
    ],
    'demo': [
        'demo/op_course_category_data.xml',
        'demo/op_material_data.xml',
        'demo/op_course_data.xml',
        'demo/op_course_section_data.xml',
        'demo/op_course_material_data.xml',
        'demo/res_users_data.xml',
        'demo/enrollement_demo_data.xml',
        'demo/rating_message_data.xml',
    ],
    'qweb': [
        'static/src/xml/openeducat_lms_dashboard.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 100,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': 'https://www.openeducat.org/plans'
}
