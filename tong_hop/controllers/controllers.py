# -*- coding: utf-8 -*-
from odoo import http

# class TongHop(http.Controller):
#     @http.route('/tong_hop/tong_hop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tong_hop/tong_hop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tong_hop.listing', {
#             'root': '/tong_hop/tong_hop',
#             'objects': http.request.env['tong_hop.tong_hop'].search([]),
#         })

#     @http.route('/tong_hop/tong_hop/objects/<model("tong_hop.tong_hop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tong_hop.object', {
#             'object': obj
#         })