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
from zeit.cms.i18n import MessageFactory as _

import zeit.wysiwyg.interfaces

import zeit.content.quiz.interfaces
import zeit.content.quiz.question
import zeit.content.quiz.browser.quiz

class FormBase(object):

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IQuestion).select('title') +
        zope.formlib.form.FormFields(
            zeit.wysiwyg.interfaces.IHTMLContent))


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    factory = zeit.content.quiz.question.Question
    checkout = False
    next_view = 'addAnswer.html'
    cancel_next_view = 'questions.html'

    def suggestName(self, object):
        return object.title or u''


class EditForm(zeit.content.quiz.browser.quiz.EditFormBase, FormBase):

    redirect_to_view = 'answers.html'
    template = zope.app.pagetemplate.ViewPageTemplateFile(
        os.path.join(os.path.dirname(__file__), 'question-edit-form.pt'))
