# -*- coding: utf-8 -*-
# Copyright (c) 2008-2009 gocept gmbh & co. kg
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

ANSWER_TEMPLATE = u"""\
<answer xmlns:py="http://codespeak.net/lxml/objectify/pytype" />"""


class Answer(zeit.content.quiz.container.Contained,
             zeit.content.quiz.quiz.ContentBase):
    """A possible answer to a question of a quiz.

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IAnswer,
                              zope.app.container.interfaces.IContained)

    correct = zeit.cms.content.property.ObjectPathProperty('.correct')

    default_template = ANSWER_TEMPLATE

    @rwproperty.getproperty
    def answer(self):
        return self.convert.to_html(self.get_node('text'))

    @rwproperty.setproperty
    def answer(self, value):
        return self.convert.from_html(self.get_node('text'), value)

    def __eq__(self, other):
        if not zeit.content.quiz.interfaces.IAnswer.providedBy(other):
            return False
        return self.xml == other.xml

    def __ne__(self, other):
        return not (self == other)


answerFactory = zeit.content.quiz.container.xml_tree_content_adapter(Answer)


@zope.component.adapter(zeit.content.quiz.interfaces.IAnswer)
@zope.interface.implementer(zeit.content.quiz.interfaces.IQuestion)
def get_question(context):
    return context.__parent__
