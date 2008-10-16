# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.component
import zope.interface

import zeit.cms.connector
import zeit.cms.content.adapter
import zeit.cms.content.property
import zeit.cms.content.xmlsupport
import zeit.wysiwyg.html

import zeit.content.quiz.interfaces


ANSWER_TEMPLATE = u"""\
<answer xmlns:py="http://codespeak.net/lxml/objectify/pytype">
    <head/>
    <body>
      <text/>
    </body>
</answer>"""


class Answer(zeit.cms.content.xmlsupport.XMLContentBase):
    """A possible answer to a question of a quiz.

    >>> import zope.interface.verify
    >>> zope.interface.verify.verifyObject(
    ...     zeit.content.quiz.interfaces.IAnswer, Answer())
    True
    
    """
    zope.interface.implements(zeit.content.quiz.interfaces.IAnswer)

    title = zeit.cms.content.property.Structure('.body.title')

    default_template = ANSWER_TEMPLATE


answerFactory = zeit.cms.content.adapter.xmlContentFactory(Answer)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'answer')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IAnswer)(resourceFactory)


class AnswerHTMLContent(zeit.wysiwyg.html.HTMLContentBase):
    """HTML content of an article."""

    zope.component.adapts(zeit.content.quiz.interfaces.IAnswer)

    def get_tree(self):
        return self.context.xml['body']['text']
