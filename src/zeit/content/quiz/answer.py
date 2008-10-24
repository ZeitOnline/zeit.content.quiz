# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import lxml.objectify
import rwproperty
import zope.app.container.interfaces
import zope.component
import zope.interface

import zeit.cms.content.property

import zeit.content.quiz.interfaces
import zeit.content.quiz.container
import zeit.content.quiz.quiz

ANSWER_TEMPLATE = u"""
<answer xmlns:py="http://codespeak.net/lxml/objectify/pytype" />"""


class Answer(zeit.content.quiz.container.Contained,
             zeit.content.quiz.quiz.ContentBase):
    """A possible answer to a question of a quiz.

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IAnswer,
                              zope.app.container.interfaces.IContained)

    default_template = ANSWER_TEMPLATE

    correct = zeit.cms.content.property.ObjectPathProperty('.correct')

    @rwproperty.getproperty
    def answer(self):
        return self.convert.to_html(self.get_node('text'))

    @rwproperty.setproperty
    def answer(self, value):
        return self.convert.from_html(self.get_node('text'), value)

    @rwproperty.getproperty
    def explanation(self):
        return self.convert.to_html(self.get_node('explanation'))

    @rwproperty.setproperty
    def explanation(self, value):
        return self.convert.from_html(self.get_node('explanation'), value)



answerFactory = zeit.content.quiz.container.xml_tree_content_adapter(Answer)


@zope.component.adapter(zeit.content.quiz.interfaces.IAnswer)
@zope.interface.implementer(zeit.content.quiz.interfaces.IQuestion)
def get_question(context):
    return context.__parent__
