# -*- coding: utf-8 -*-
from odoo import http

# class OpeneducatStem(http.Controller):
#     @http.route('/openeducat_stem/openeducat_stem/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_stem/openeducat_stem/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_stem.listing', {
#             'root': '/openeducat_stem/openeducat_stem',
#             'objects': http.request.env['openeducat_stem.openeducat_stem'].search([]),
#         })

#     @http.route('/openeducat_stem/openeducat_stem/objects/<model("openeducat_stem.openeducat_stem"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_stem.object', {
#             'object': obj
#         })