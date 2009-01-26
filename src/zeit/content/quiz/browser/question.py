# Copyright (c) 2008-2009 gocept gmbh & co. kg
# See also LICENSE.txt

import gocept.form.grouped
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

    form_fields = zope.formlib.form.FormFields(
        zeit.content.quiz.interfaces.IQuestion).omit('xml')

    field_groups = (
        gocept.form.grouped.RemainingFields(
            _('Question'),
            css_class='full-width wide-widgets'),)


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    title = _("Add question")
    factory = zeit.content.quiz.question.Question
    checkout = False
    next_view = 'addAnswer.html'
    cancel_next_view = 'questions.html'

    add_answer = False

    def suggestName(self, object):
        return object.title or u''

    @zope.formlib.form.action(_('Apply'),
                              condition=zope.formlib.form.haveInputWidgets)
    def handle_apply(self, action, data):
        self.createAndAdd(data)
        self.status = _('Added question.')

    @zope.formlib.form.action(_('Apply and add answer'),
                              condition=zope.formlib.form.haveInputWidgets)
    def handle_apply_and_add_answer(self, action, data):
        self.createAndAdd(data)
        self.add_answer = True
        self.status = _('Added question.')

    @zope.formlib.form.action(_("Cancel"), validator=lambda *a: ())
    def cancel(self, action, data):
        self.status = _('Cancelled')
        pass

    def nextURL(self):
        if self.add_answer:
            return self.url(self._created_object, self.next_view)
        return self.cancelNextURL()


class EditForm(FormBase, zeit.content.quiz.browser.quiz.EditFormBase):

    title = _("Edit question")
    redirect_to_parent_after_edit = True
    redirect_to_view = 'questions.html'
