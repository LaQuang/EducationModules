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


from odoo import http

from odoo.addons.website_sale.controllers.website_mail import WebsiteMailController
from odoo.http import request


class CourseWebsiteController(WebsiteMailController):

    @http.route()
    def chatter_json(self, res_model='', res_id=None, message='', **kw):
        message_data = super(CourseWebsiteController, self).chatter_json(
            res_model, res_id, message, **kw)
        if message_data and kw.get('rating'):
            rating = request.env['rating.rating'].create({
                'rating': float(kw.get('rating')),
                'res_model': res_model,
                'res_id': res_id,
                'message_id': message_data['id'],
                'consumed': True,
            })
            message_data.update({
                'rating_default_value': rating.rating,
                'rating_disabled': True,
            })
        return message_data
