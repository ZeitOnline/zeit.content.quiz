# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.app.container.interfaces
import zope.interface
import zope.schema

import zeit.cms.content.interfaces
import zeit.cms.content.field

from zeit.cms.i18n import MessageFactory as _


class IContainer(zeit.cms.content.interfaces.IXMLRepresentation):
    """Container that stores its children inside its own xml representation."""

    def content_modified():
        """Notify the container that content has changed."""


class IReadQuiz(zeit.cms.content.interfaces.ICommonMetadata, 
                zeit.cms.content.interfaces.IXMLContent,
                zope.app.container.interfaces.IReadContainer,
                IContainer):
    """Read methods for quiz."""


class IWriteQuiz(zope.app.container.interfaces.IWriteContainer):
    """Write methods for quiz."""


class IQuiz(IReadQuiz, IWriteQuiz):
    """Quiz content type."""


class IQuizContent(zope.interface.Interface):
    """Sub-objects of a quiz.
    """

    title = zope.schema.TextLine(title=_('Title'), required=False)


class IReadQuestion(zope.app.container.interfaces.IReadContainer,
                    zeit.cms.content.interfaces.IXMLRepresentation,
                    IQuizContent,
                    IContainer):
    """Read methods for question."""


class IWriteQuestion(zope.app.container.interfaces.IWriteContainer):
    """Write methods for question."""


class IQuestion(IReadQuestion, IWriteQuestion):
    """Question content type."""


class IAnswer(zeit.cms.content.interfaces.IXMLRepresentation, IQuizContent):
    """Answer content type."""

    correct = zope.schema.Bool(title=_('Correct?'))
