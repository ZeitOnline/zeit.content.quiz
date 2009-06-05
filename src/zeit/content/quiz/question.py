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
import zeit.wysiwyg.html

import zeit.content.quiz.interfaces
import zeit.content.quiz.container
import zeit.content.quiz.quiz


QUESTION_TEMPLATE = u"""\
<question xmlns:py="http://codespeak.net/lxml/objectify/pytype" />"""


class Question(zeit.content.quiz.container.Container,
               zeit.content.quiz.container.Contained,
               zeit.content.quiz.quiz.ContentBase):
    """A question in a quiz.
    """
    zope.interface.implements(zeit.content.quiz.interfaces.IQuestion,
                              zope.app.container.interfaces.IContained)

    default_template = QUESTION_TEMPLATE

    @rwproperty.getproperty
    def question(self):
        return self.convert.to_html(self.get_node('text'))

    @rwproperty.setproperty
    def question(self, value):
        self.convert.from_html(self.get_node('text'), value)

    def _iter_xml_children(self):
        for child in self.xml.getchildren():
            if child.tag == 'answer':
                yield child

    def _get_persistent_container(self):
        return zeit.content.quiz.interfaces.IQuiz(self)


questionFactory = zeit.content.quiz.container.xml_tree_content_adapter(
    Question)


class QuestionHTMLContent(zeit.wysiwyg.html.HTMLContentBase):
    """HTML content of an article."""

    zope.component.adapts(zeit.content.quiz.interfaces.IQuestion)

    def get_tree(self):
        try:
            node = self.context.xml['text']
        except AttributeError:
            node = lxml.objectify.Element('text')
            self.context.xml.append(node)
        return node
