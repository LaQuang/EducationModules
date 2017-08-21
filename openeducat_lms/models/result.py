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

from odoo import models, api


class OpQuizResult(models.Model):
    _inherit = 'op.quiz.result'

    @api.multi
    def get_answer_data(self):
        wrong_answers = []
        not_attempt_answer = []
        right_answers = []
        for line in self.line_ids:
            if not line.given_answer:
                not_attempt_answer.append(
                    {'question': line.name, 'answer': line.answer or ''})
            elif line.answer == line.given_answer:
                right_answers.append(
                    {'question': line.name, 'answer': line.answer})
            else:
                wrong_answers.append({
                    'question': line.name,
                    'given_answer': line.given_answer,
                    'answer': line.answer or '',
                })
        quiz = self.quiz_id
        display_wrong_ans = 0
        if quiz.wrong_ans and wrong_answers:
            display_wrong_ans = 1
        display_true_ans = 0
        if quiz.right_ans and right_answers:
            display_true_ans = 1
        not_attempt_ans = 0
        if quiz.not_attempt_ans and not_attempt_answer:
            not_attempt_ans = 1
        message = ''
        is_message = 0
        for msg in quiz.message_ids:
            result_to = msg.result_to
            result_from = msg.result_from
            if (self.score <= result_to) and (self.score >= result_from):
                message = msg.message
                is_message = 1
        return {
            'wrong_answer': wrong_answers,
            'not_attempt_answer': not_attempt_answer,
            'right_answers': right_answers,
            'total_question': self.total_question,
            'total_correct': self.total_correct,
            'total_incorrect': self.total_incorrect,
            'total_marks': self.total_marks,
            'received_marks': self.received_marks,
            'percentage': self.score,
            'display_wrong_ans': display_wrong_ans,
            'display_true_ans': display_true_ans,
            'not_attempt_ans': not_attempt_ans,
            'message': message,
            'is_message': is_message
        }
