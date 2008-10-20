# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.app.container.interfaces
import zope.component
import zope.interface

import zeit.cms.content.property
import zeit.wysiwyg.html

import zeit.content.quiz.interfaces
import zeit.content.quiz.container


ANSWER_TEMPLATE = u"""\
<answer xmlns:py="http://codespeak.net/lxml/objectify/pytype">
  <text/>
</answer>"""


class Answer(zeit.content.quiz.container.Contained):
    """A possible answer to a question of a quiz.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyObject(
    ...     zeit.content.quiz.interfaces.IAnswer, Answer())
    True
    >>> zope.interface.verify.verifyObject(
    ...     zope.app.container.interfaces.IContained, Answer())
    True

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IAnswer,
                              zope.app.container.interfaces.IContained)

    title = zeit.cms.content.property.Structure('.title')

    default_template = ANSWER_TEMPLATE


answerFactory = zeit.content.quiz.container.xml_tree_content_adapter(Answer)


class AnswerHTMLContent(zeit.wysiwyg.html.HTMLContentBase):
    """HTML content of an article."""

    zope.component.adapts(zeit.content.quiz.interfaces.IAnswer)

    def get_tree(self):
        return self.context.xml['text']
