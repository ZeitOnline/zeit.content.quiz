# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.interface

import zeit.cms.content.property
import zeit.content.quiz.interfaces
import zeit.content.quiz.container


QUESTION_TEMPLATE = u"""\
<question xmlns:py="http://codespeak.net/lxml/objectify/pytype">
    <head/>
    <body/>
</question>"""


class Question(zeit.content.quiz.container.Container):

    zope.interface.implements(zeit.content.quiz.interfaces.IQuestion)

    title = zeit.cms.content.property.Structure(
        '.body.title')
    text = zeit.cms.content.property.ObjectPathProperty(
        '.body.text')
    default_template = QUESTION_TEMPLATE


questionFactory = zeit.cms.content.adapter.xmlContentFactory(Question)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'question')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IQuestion)(resourceFactory)
