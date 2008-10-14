# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.interface

import zeit.cms.content.metadata
import zeit.cms.repository.repository

import zeit.content.quiz.interfaces

QUIZ_TEMPLATE = u"""\
<quiz xmlns:py="http://codespeak.net/lxml/objectify/pytype">
    <head/>
    <body/>
</quiz>"""


class Quiz(zeit.cms.repository.repository.Container,
           zeit.cms.content.metadata.CommonMetadata):
    """Quiz"""

    zope.interface.implements(zeit.content.quiz.interfaces.IQuiz)

    default_template = QUIZ_TEMPLATE


quizFactory = zeit.cms.content.adapter.xmlContentFactory(Quiz)


resourceFactory = zeit.cms.connector.xmlContentToResourceAdapterFactory(
    'quiz')
resourceFactory = zope.component.adapter(
    zeit.content.quiz.interfaces.IQuiz)(resourceFactory)


@zope.component.adapter(zeit.content.quiz.interfaces.IQuiz)
@zope.interface.implementer(zeit.cms.workingcopy.interfaces.ILocalContent)
def local_content_adapter(context):
    repository = zope.component.getUtility(
        zeit.cms.repository.interfaces.IRepository)
    content = repository.getCopyOf(context.uniqueId)
    repository_properties = zeit.connector.interfaces.IWebDAVProperties(
        context)
    zope.interface.directlyProvides(
        content, zeit.cms.workingcopy.interfaces.ILocalContent)
    new_properties = zeit.connector.interfaces.IWebDAVProperties(content)
    new_properties.update(repository_properties)
    return content
