# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import gocept.form.action
import xml.sax.saxutils
import zeit.cms.browser.form
import zeit.cms.content.browser.form
import zeit.cms.content.interfaces
import zeit.cms.interfaces
import zeit.content.quiz.interfaces
import zeit.content.quiz.quiz
import zope.cachedescriptors.property
import zope.formlib.form
import zope.traversing.browser.interfaces
from zeit.content.quiz.i18n import MessageFactory as _


class Questions(object):

    title = _('Quiz overview')

    @zope.cachedescriptors.property.Lazy
    def metadata(self):
        return zeit.cms.content.interfaces.ICommonMetadata(self.context)

    def update(self):
        super(Questions, self).update()
        if 'apply' not in self.request.form:
            return
        questions = self.request.form.get('__quiz__')
        self.context.updateOrder(questions)
        for q_name in questions:
            answers = self.request.form.get(q_name, ())
            self.context[q_name].updateOrder(answers)


class QuizFormBase(object):

    form_fields = (
        zope.formlib.form.FormFields(
            zeit.cms.interfaces.ICMSContent,
            zeit.cms.syndication.interfaces.IAutomaticMetadataUpdate,
            zeit.cms.content.interfaces.ICommonMetadata
        ).omit('commentsAllowed') +
        zope.formlib.form.FormFields(
            zeit.content.quiz.interfaces.IQuiz).select('commentsAllowed'))



class AddQuiz(QuizFormBase,
              zeit.cms.content.browser.form.CommonMetadataAddForm):

    title = _("Add quiz")
    factory = zeit.content.quiz.quiz.Quiz
    next_view = 'edit.html'
    form_fields = QuizFormBase.form_fields.omit(
        'automaticMetadataUpdateDisabled')


class EditQuiz(QuizFormBase,
               zeit.cms.content.browser.form.CommonMetadataEditForm):

    title = _("Edit quiz")


class DisplayQuiz(QuizFormBase,
                  zeit.cms.content.browser.form.CommonMetadataDisplayForm):

    title = _("View quiz")


# quiz content


class EditFormBase(zeit.cms.browser.form.EditForm):
    """Base class for edit views of various sub-objects of a quiz.
    """

    deleted = False

    @zope.formlib.form.action(
        _('Apply'), condition=zope.formlib.form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        self.applyChanges(data)

    @gocept.form.action.confirm(
        _('Delete'),
        name='delete',
        confirm_message=_('delete-item-confirmation',
                          default=u'Really delete?'),
        condition=zope.formlib.form.haveInputWidgets,
        )
    def handle_delete(self, action, data):
        self.quiz = zeit.content.quiz.interfaces.IQuiz(self.context)
        parent = self.context.__parent__
        del parent[self.context.__name__]
        self.status = _('Item was deleted.')
        self.deleted = True

    def nextURL(self):
        if self.deleted:
            return self.url(self.quiz, '@@questions.html')
        return super(EditFormBase, self).nextURL()


@zope.component.adapter(zeit.content.quiz.interfaces.IQuestion,
                        zeit.cms.browser.interfaces.ICMSLayer)
@zope.interface.implementer(zope.publisher.interfaces.browser.IBrowserView)
def question_display_title(context, request):
    if context.title:
        return xml.sax.saxutils.escape(context.title)
    return context.question


@zope.component.adapter(zeit.content.quiz.interfaces.IAnswer,
                        zeit.cms.browser.interfaces.ICMSLayer)
@zope.interface.implementer(zope.publisher.interfaces.browser.IBrowserView)
def answer_display_title(context, request):
    if context.title:
        return xml.sax.saxutils.escape(context.title)
    return context.answer
