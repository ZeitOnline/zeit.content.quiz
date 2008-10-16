# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.component
import zope.interface

import zeit.cms.content.property
import zeit.wysiwyg.html

import zeit.content.quiz.interfaces
import zeit.content.quiz.container


QUESTION_TEMPLATE = u"""\
<question xmlns:py="http://codespeak.net/lxml/objectify/pytype">
    <head/>
    <body>
      <text/>
    </body>
</question>"""


class Question(zeit.content.quiz.container.Container):
    """A question in a quiz.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyObject(
    ...     zeit.content.quiz.interfaces.IQuestion, Question())
    True

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IQuestion)

    title = zeit.cms.content.property.Structure('.body.title')

    default_template = QUESTION_TEMPLATE

    def _iter_xml_children(self):
        for child in self.xml['body'].getchildren():
            if child.tag == 'answer':
                yield child


questionFactory = zeit.content.quiz.container.xml_tree_content_adapter(
    Question)


class QuestionHTMLContent(zeit.wysiwyg.html.HTMLContentBase):
    """HTML content of an article."""

    zope.component.adapts(zeit.content.quiz.interfaces.IQuestion)

    def get_tree(self):
        return self.context.xml['body']['text']
