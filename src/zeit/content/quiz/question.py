# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.component
import zope.interface

import zeit.cms.connector
import zeit.cms.content.adapter
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

    zope.interface.implements(zeit.content.quiz.interfaces.IQuestion)

    title = zeit.cms.content.property.Structure('.body.title')

    default_template = QUESTION_TEMPLATE

    def _iter_xml_children(self):
        for child in self.xml['body'].getchildren():
            if child.tag == 'answer':
                yield child


questionFactory = zeit.cms.content.adapter.xmlContentFactory(Question)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'question')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IQuestion)(resourceFactory)


class QuestionHTMLContent(zeit.wysiwyg.html.HTMLContentBase):
    """HTML content of an article."""

    zope.component.adapts(zeit.content.quiz.interfaces.IQuestion)

    def get_tree(self):
        return self.context.xml['body']['text']
