# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import gocept.form.action
import zope.cachedescriptors.property
import zope.formlib.form
import zope.traversing.browser.interfaces

import zeit.cms.browser.form
import zeit.cms.content.browser.form
import zeit.cms.content.interfaces
import zeit.cms.interfaces

from zeit.cms.i18n import MessageFactory as _

import zeit.content.quiz.interfaces
import zeit.content.quiz.quiz


class Questions(object):

    @zope.cachedescriptors.property.Lazy
    def metadata(self):
        return zeit.cms.content.interfaces.ICommonMetadata(self.context)


class QuizFormBase(object):

    form_fields = zope.formlib.form.FormFields(
        zeit.cms.interfaces.ICMSContent,
        zeit.cms.syndication.interfaces.IAutomaticMetadataUpdate,
        zeit.cms.content.interfaces.ICommonMetadata)


class AddQuiz(QuizFormBase,
              zeit.cms.content.browser.form.CommonMetadataAddForm):

    title = _("Add quiz")
    factory = zeit.content.quiz.quiz.Quiz
    next_view = 'addQuestion.html'
    form_fields = QuizFormBase.form_fields.omit(
        'automaticMetadataUpdateDisabled')


class EditQuiz(QuizFormBase,
               zeit.cms.content.browser.form.CommonMetadataEditForm):

    title = _("Edit quiz")


class DisplayQuiz(QuizFormBase,
                  zeit.cms.content.browser.form.CommonMetadataDisplayForm):

    title = _("View quiz metadata")


class EditFormBase(zeit.cms.browser.form.EditForm):

    @zope.formlib.form.action(
        _('Apply'), condition=zope.formlib.form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        self.applyChanges(data)

    @gocept.form.action.confirm(
        _('Delete'),
        name='delete',
        confirm_message=_('Really delete?'),
        condition=zope.formlib.form.haveInputWidgets,
        )
    def handle_delete(self, action, data):
        parent = self.context.__parent__
        del parent[self.context.__name__]
        candidate = parent
        while not IQuiz.providedBy(candidate):
            candidate = candidate.__parent__
        else:
            quiz = candidate
        next_url = zope.component.getMultiAdapter(
            (quiz, self.request),
            zope.traversing.browser.interfaces.IAbsoluteURL)()
        self.request.response.redirect(next_url + '/@@questions.html')
