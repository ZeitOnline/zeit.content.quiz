# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import os.path
import zope.app.container.interfaces
import zope.app.pagetemplate
import zope.component
import zope.event
import zope.formlib.form
import zope.lifecycleevent

import zeit.wysiwyg.interfaces

from zeit.cms.i18n import MessageFactory as _

import zeit.content.quiz.interfaces
import zeit.content.quiz.answer
import zeit.content.quiz.browser.quiz


class FormBase(object):

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IAnswer).select(
            'title', 'correct', 'answer', 'explanation'))

    def questions_url(self):
        quiz = zeit.content.quiz.interfaces.IQuiz(self.context)
        url = zope.component.getMultiAdapter(
            (quiz, self.request), name="absolute_url")()
        return url + '/@@questions.html'


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    title = _("Add answer")
    factory = zeit.content.quiz.answer.Answer
    checkout = False

    def nextURL(self):
        url = zope.component.getMultiAdapter(
            (self.context, self.request), name="absolute_url")()
        return url + '/@@addAnswer.html'

    def cancelNextURL(self):
        return self.questions_url()

    def suggestName(self, object):
        return object.title or u''


class EditForm(FormBase, zeit.content.quiz.browser.quiz.EditFormBase):

    title = _("Edit answer")

    def nextURL(self):
        return self.questions_url()
