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

import sys

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html.parser
    import urllib.request
    import urllib.parse

agent = {'User-Agent':
"Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}

import re
import base64

from odoo import models, api, fields, _

def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html.parser.HTMLParser()
    return (parser.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto"):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default

    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?
    """
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    if (sys.version_info[0] < 3):
        to_translate = urllib.quote_plus(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib2.Request(link, headers=agent)
        raw_data = urllib2.urlopen(request).read()
    else:
        to_translate = urllib.parse.quote(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)

class OpMaterialVersion(models.Model):
    _name = 'op.material.version'

    _inherit = ['website.published.mixin']

    _description = 'Material version'

    translator_id = fields.Many2one(
        'res.users', 'Translator')

    language = fields.Selection([
        ('vi', 'Vietnamese'), ('en', 'English'), ('ja', 'Japanese'), ('fr', 'French'), ('de', 'German')], string='Language',
        required=True)

    version_type = fields.Selection([
        ('text', 'Text'), ('file', 'File')], string='Translation type',
        required=True, default='text')

    text = fields.Text(string="Content")

    datas = fields.Binary('Content', attachment=True)

    material_id = fields.Many2one('op.material', 'Material', required=True)

    material_type = fields.Char('Material type', compute='_get_material_type')

    material_text = fields.Char('Material text', compute='_get_material_text')

    state = fields.Selection([
        ('waiting', "Waiting"),
        ('translating', "Translating"),
        ('translated', "Translated"),
        ('approved', "Approved"),
    ])

    embed_code = fields.Text(
        'Embed Code', readonly=True, compute='_get_embed_code')

    def _get_embed_code(self):
        for record in self:
            if record.version_type == 'file' and record.datas:
                record.embed_code = '<iframe src="/material_versions/embed/%s?page=1" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                    record.id, 315, 420)
                #'<iframe src="/web/content/op.material.version/%s/datas" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
            elif record.version_type == 'text':
                record.embed_code = '<p>%s</p>' % record.text   
            else:
                record.embed_code = False

    @api.multi
    def action_wait(self):
        self.state = 'waiting'

    @api.multi
    def action_claim(self):
        self.state = 'translating'
        self.translator_id = self.env.uid

    @api.multi
    def action_complete(self):
        self.state = 'translated'

    @api.multi
    def action_approve(self):
        self.state = 'approved'

    @api.multi
    def action_auto_translate(self):
        self.version_type = 'text'
        self.text = translate(self.material_id.text, self.language)

    @api.multi
    def website_lms_publish_button(self):
        self.ensure_one()
        return self.write({'website_published': not self.website_published})

    @api.depends('material_id')
    def _get_material_type(self):
        for r in self:
            if r.material_id:
                r.material_type = r.material_id.material_type
            else:
                r.material_type = False

    @api.depends('material_id')
    def _get_material_text(self):
        for r in self:
            if r.material_id and r.material_id.material_type == 'text' and r.material_id.text:
                r.material_text = r.material_id.text
            else:
                r.material_text = False




