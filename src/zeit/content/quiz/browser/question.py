# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import zope.app.container.interfaces
import zope.component
import zope.event
import zope.formlib.form
import zope.lifecycleevent

import zeit.content.quiz.browser.quiz
import zeit.content.quiz.interfaces
import zeit.content.quiz.question
import zeit.wysiwyg.interfaces
from zeit.content.quiz.i18n import MessageFactory as _

class FormBase(object):

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IQuestion).select('title') +
        zope.formlib.form.FormFields(
            zeit.wysiwyg.interfaces.IHTMLContent))


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    title = _("Add question")
    factory = zeit.content.quiz.question.Question
    checkout = False
    next_view = 'addAnswer.html'
    cancel_next_view = 'questions.html'

    def suggestName(self, object):
        return object.title or u''


class EditForm(zeit.content.quiz.browser.quiz.EditFormBase, FormBase):

    title = _("Edit question")
    redirect_to_parent_after_edit = True
    redirect_to_view = 'questions.html'
