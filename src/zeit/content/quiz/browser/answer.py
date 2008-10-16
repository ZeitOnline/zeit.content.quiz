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
import zope.traversing.browser.interfaces

import zeit.wysiwyg.interfaces

import zeit.content.quiz.interfaces
import zeit.content.quiz.answer


class FormBase(object):

    form_fields = (
        zope.formlib.form.Fields(
            zeit.content.quiz.interfaces.IAnswer).select('title') +
        zope.formlib.form.FormFields(
            zeit.wysiwyg.interfaces.IHTMLContent))


class AddForm(FormBase, zeit.cms.browser.form.AddForm):

    factory = zeit.content.quiz.answer.Answer
    checkout = False
    cancel_next_view = 'answers.html'

    def nextURL(self):
        url = zope.component.getMultiAdapter(
            (self.context, self.request),
            zope.traversing.browser.interfaces.IAbsoluteURL)()
        return url + '/@@answers.html'

    def suggestName(self, object):
        return object.title


class EditForm(FormBase, zeit.cms.browser.form.EditForm):
    
    redirect_to_parent_after_edit = True
    redirect_to_view = 'answers.html'
