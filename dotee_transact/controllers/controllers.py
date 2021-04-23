# -*- coding: utf-8 -*-
# from odoo import http


# class Dotee-transact(http.Controller):
#     @http.route('/dotee-transact/dotee-transact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dotee-transact/dotee-transact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dotee-transact.listing', {
#             'root': '/dotee-transact/dotee-transact',
#             'objects': http.request.env['dotee-transact.dotee-transact'].search([]),
#         })

#     @http.route('/dotee-transact/dotee-transact/objects/<model("dotee-transact.dotee-transact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dotee-transact.object', {
#             'object': obj
#         })
