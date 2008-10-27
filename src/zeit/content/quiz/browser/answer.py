# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import gocept.form.grouped
import os.path
import zope.app.container.interfaces
import zope.app.pagetemplate
import zope.component
import zope.event
import zope.formlib.form
import zope.lifecycleevent

import zeit.content.quiz.answer
import zeit.content.quiz.browser.quiz
import zeit.content.quiz.interfaces
import zeit.wysiwyg.interfaces
from zeit.content.quiz.i18n import MessageFactory as _


class FormBase(object):

    def questions_url(self):
        quiz = zeit.content.quiz.interfaces.IQuiz(self.context)
        return self.url(quiz, '@@questions.html')

    field_groups = (
        gocept.form.grouped.RemainingFields(
            _('Question'),
            css_class='full-width wide-widgets'),)


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    title = _("Add answer")
    factory = zeit.content.quiz.answer.Answer
    checkout = False
    add_answer = False

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IAnswer).select(
            'title', 'correct', 'answer', 'explanation'))

    @zope.formlib.form.action(_('Apply'),
                              condition=zope.formlib.form.haveInputWidgets)
    def handle_apply(self, action, data):
        self.createAndAdd(data)
        self.status = _('Added answer.')

    @zope.formlib.form.action(_('Apply and add answer'),
                              condition=zope.formlib.form.haveInputWidgets)
    def handle_apply_and_add_answer(self, action, data):
        self.createAndAdd(data)
        self.add_answer = True
        self.status = _('Added answer.')

    @zope.formlib.form.action(_("Cancel"), validator=lambda *a: ())
    def cancel(self, action, data):
        self.status = _('Cancelled.')

    def nextURL(self):
        if self.add_answer:
            return self.url('@@addAnswer.html')
        return self.cancelNextURL()

    def cancelNextURL(self):
        return self.questions_url()

    def suggestName(self, object):
        return object.title or u''


class EditForm(FormBase, zeit.content.quiz.browser.quiz.EditFormBase):

    title = _("Edit answer")

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IQuestion, prefix='q',
            for_display=True).select(
            'q.title', 'q.question') +
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IAnswer).select(
            'title', 'correct', 'answer', 'explanation'))

    field_groups = (
        gocept.form.grouped.Fields(
            title=_(u'Question'),
            fields=('q.title', 'q.question'),
            css_class='full-width wide-widgets'),
        gocept.form.grouped.RemainingFields(
            title=_(u'Answer'),
            css_class='full-width wide-widgets'),
        )

    def nextURL(self):
        return self.questions_url()
