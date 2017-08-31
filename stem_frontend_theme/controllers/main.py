# -*- coding: utf-8 -*-
from odoo import http

class Stem(http.Controller):
    @http.route('/home', auth='user', website=True)
    def home(self, **kw):
        online_free_courses = http.request.env['op.course'].sudo().search(
            [('online_course', '=', True), ('type', '=', 'free')], limit=3, order='create_date desc')
        return http.request.render('stem_frontend_theme.stem_home', { 'online_free_courses': online_free_courses })