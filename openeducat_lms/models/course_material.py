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

import re

from odoo import models, api, fields, _
from odoo.addons.website.models.website import slug
from odoo.tools import image
from odoo.tools.translate import html_translate


class OpCourseMaterial(models.Model):
    _name = 'op.material'
    _inherit = ['mail.thread',
                'website.seo.metadata', 'website.published.mixin']
    _description = 'Material'

    image = fields.Binary('Image', attachment=True)
    image_medium = fields.Binary('Medium', compute="_get_image",
                                 store=True, attachment=True)
    image_thumb = fields.Binary('Thumbnail', compute="_get_image",
                                store=True, attachment=True)

    @api.depends('image')
    def _get_image(self):
        for record in self:
            if record.image:
                record.image_medium = image.crop_image(
                    record.image, type='top', ratio=(4, 3), thumbnail_ratio=4)
                record.image_thumb = image.crop_image(
                    record.image, type='top', ratio=(4, 3), thumbnail_ratio=6)
            else:
                record.image_medium = False
                record.iamge_thumb = False

    name = fields.Char('Title', required=True, translate=True)
    short_description = fields.Text('Short Description')
    full_description = fields.Html('Full Description',
                                   translate=html_translate,
                                   sanitize_attributes=False)

    auto_publish = fields.Boolean('Auto Publish')
    auto_publish_type = fields.Selection([('wait_until', 'Wait Until'),
                                          ('wait_until_duration', 'Wait Until Duration')])
    wait_until_date = fields.Date('Wait Until')
    wait_until_duration = fields.Integer('Wait Until Duration')
    wait_until_duration_period = fields.Selection([('minutes', 'Minutes'),
                                                   ('hours', 'Hours'),
                                                   ('days', 'Days'),
                                                   ('weeks', 'Weeks'),
                                                   ('months', 'Months'),
                                                   ('years', 'Years')], 'Wait at least period')

    user_id = fields.Many2one(
        'res.users', 'User', default=lambda self: self.env.uid, required=True)
    category_id = fields.Many2one('op.course.category', string="Category")

    material_type = fields.Selection([
        ('video', 'Video'), ('audio', 'Audio'), ('document', 'Document/PDF'),
        ('infographic', 'Image'), ('quiz', 'Quiz'), ('text', 'Text')], string='Material Type',
        required=True, default='video')
    quiz_id = fields.Many2one('op.quiz', 'Quiz')
    datas = fields.Binary('Content', attachment=True)
    url = fields.Char('Document URL', help="Youtube or Google Document URL")
    document_id = fields.Char(
        'Document ID', help="Youtube or Google Document ID")
    total_time = fields.Float(
        'Total Time (HH:MM)', required=True,
        help='Approx time to complete this material')

    @api.onchange('url')
    def on_change_url(self):
        self.ensure_one()
        if self.url:
            res = self._parse_document_url(self.url)
            if res.get('error'):
                raise Warning(_('Could not fetch data from url. Document or \
                access right not available:\n%s') % res['error'])
            values = res['values']
            if not values.get('document_id'):
                raise Warning(
                    _('Please enter valid Youtube or Google Doc URL'))
            for key, value in values.iteritems():
                setattr(self, key, value)

    # website
    date_published = fields.Datetime('Publish Date')
    website_message_ids = fields.One2many(
        'mail.message', 'res_id',
        domain=lambda self: [
            ('model', '=', self._name), ('message_type', '=', 'comment')],
        string='Website Messages', help="Website communication history")
    likes = fields.Integer('Likes')
    dislikes = fields.Integer('Dislikes')
    material_views = fields.Integer('# of Website Views')
    embed_views = fields.Integer('# of Embedded Views')
    total_views = fields.Integer(
        "Total # Views", default="0", compute='_compute_total', store=True)

    @api.depends('material_views', 'embed_views')
    def _compute_total(self):
        for record in self:
            record.total_views = record.material_views + record.embed_views
#
    embed_code = fields.Text(
        'Embed Code', readonly=True, compute='_get_embed_code')

    def _get_embed_code(self):
        for record in self:
            if record.datas and (record.material_type == 'infographic' and not record.document_id):
                record.embed_code = '<iframe src="/materials/embed/%s?page=1" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                    record.id, 315, 420)
            elif record.datas and (record.material_type == 'document' and not record.document_id):
                record.embed_code = '<iframe src="/materials/embed/%s?page=1" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                    record.id, 315, 420)
            elif record.material_type == 'video' and record.document_id:
                record.embed_code = '<iframe src="//www.youtube.com/embed/%s?theme=light" allowFullScreen="true" frameborder="0"></iframe>' % (
                    record.document_id)
            elif record.material_type == 'video' and record.datas:
                record.embed_code = '<video controls controlsList="nodownload"><source class="audio" src="data:video/mp4;base64,%s"></video>' % record.datas
            elif record.material_type == 'audio':
                record.embed_code = '<audio controls controlsList="nodownload"><source class="audio" src="data:audio/mp3;base64,%s"></audio>' % record.datas
            elif record.material_type == 'text':
                record.embed_code = '<p>%s</p>' % record.text
            else:
                record.embed_code = False

    @api.multi
    @api.depends('name')
    def _compute_website_url(self):
        super(OpCourseMaterial, self)._compute_website_url()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        for material in self:
            if material.id:
                if self.env.registry.get('link.tracker'):
                    url = self.env['link.tracker'].sudo().create(
                        {'url': '%s/course/material/%s' % (base_url, slug(material))}).short_url
                else:
                    url = '%s/course/material/%s' % (base_url, slug(material))
                material.website_url = url

    @api.multi
    def website_lms_publish_button(self):
        self.ensure_one()
        return self.write({'website_published': not self.website_published})

    def _find_document_data_from_url(self, url):
        expr = re.compile(
            r'^.*((youtu.be/)|(v/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*')
        arg = expr.match(url)
        document_id = arg and arg.group(7) or False
        if document_id:
            return ('youtube', document_id)

        expr = re.compile(
            r'(^https:\/\/docs.google.com|^https:\/\/drive.google.com).*\/d\/([^\/]*)')
        arg = expr.match(url)
        document_id = arg and arg.group(2) or False
        if document_id:
            return ('google', document_id)
        return (None, False)

    def _parse_document_url(self, url, only_preview_fields=False):
        document_source, document_id = self._find_document_data_from_url(url)
        return document_id and {'values': {'material_type': 'video',
                                           'document_id': document_id}} or {'error': _('Unknown document')}

    #stem translate
    material_version_ids = fields.One2many(
        'op.material.version', 'material_id', 'Material version')

    text = fields.Text(String='Content')
    #stem translate
