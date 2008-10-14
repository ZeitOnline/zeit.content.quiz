# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.interface

import zeit.cms.content.xmlsupport

import zeit.content.quiz.interfaces


QUESTION_TEMPLATE = u"""\
<question xmlns:py="http://codespeak.net/lxml/objectify/pytype">
    <head/>
    <body/>
</question>"""


class Question(zeit.cms.content.xmlsupport.XMLContentBase,
               zeit.cms.repository.repository.Container):

    zope.interface.implements(zeit.content.quiz.interfaces.IQuestion)

    title = u''
    text = None
    default_template = QUESTION_TEMPLATE


questionFactory = zeit.cms.content.adapter.xmlContentFactory(Question)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'question')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IQuestion)(resourceFactory)
