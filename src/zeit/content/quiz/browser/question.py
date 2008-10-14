# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.event
import zope.formlib.form
import zope.lifecycleevent
import zope.app.container.interfaces
import zope.traversing.browser.interfaces
import zope.component

import zeit.content.quiz.interfaces
import zeit.content.quiz.question


class AddForm(zope.formlib.form.AddForm):

    form_fields = zope.formlib.form.Fields(
        zeit.content.quiz.interfaces.IQuestion).omit('__name__')

    def createAndAdd(self, data):
        question = zeit.content.quiz.question.Question()
        for key, value in data.items():
            setattr(question, key, value)
        zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(question))
        name_chooser = zope.app.container.interfaces.INameChooser(self.context)
        name = name_chooser.chooseName(data['title'] or '', question)
        self.context[name] = question
        self._finished_add = True
        return question

    def nextURL(self):
        url = zope.component.getMultiAdapter(
            (self.context, self.request),
            zope.traversing.browser.interfaces.IAbsoluteURL)()
        return url + '/@@questions.html'
