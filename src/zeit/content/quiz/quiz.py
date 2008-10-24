# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import lxml.objectify
import zope.component
import zope.interface

import zeit.cms.connector
import zeit.cms.content.adapter
import zeit.cms.content.metadata
import zeit.cms.interfaces
import zeit.wysiwyg.interfaces

import zeit.content.quiz.interfaces
import zeit.content.quiz.container


QUIZ_TEMPLATE = u"""\
<quiz xmlns:py="http://codespeak.net/lxml/objectify/pytype">
</quiz>"""


class Quiz(zeit.content.quiz.container.Container,
           zeit.cms.content.metadata.CommonMetadata):
    """Quiz"""

    zope.interface.implements(zeit.content.quiz.interfaces.IQuiz,
                              zeit.cms.interfaces.IEditorialContent)

    default_template = QUIZ_TEMPLATE

    def _iter_xml_children(self):
        for child in self.xml.getchildren():
            if child.tag == 'question':
                yield child

    def _get_persistent_container(self):
        return self


quizFactory = zeit.cms.content.adapter.xmlContentFactory(Quiz)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'quiz')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IQuiz)(resourceFactory)


@zope.component.adapter(zeit.content.quiz.interfaces.IQuizContent)
@zope.interface.implementer(zeit.content.quiz.interfaces.IQuiz)
def quiz_for_content(context):
    candidate = context
    while not zeit.content.quiz.interfaces.IQuiz.providedBy(candidate):
        candidate = candidate.__parent__
    return candidate


class ContentBase(object):
    """Base class for questions and answers."""

    title = zeit.cms.content.property.ObjectPathProperty('.title')

    def get_node(self, name):
        try:
            node = self.xml[name]
        except AttributeError:
            node = lxml.objectify.Element(name)
            self.xml.append(node)
        return node

    @property
    def convert(self):
        return zeit.wysiwyg.interfaces.IHTMLConverter(self)
