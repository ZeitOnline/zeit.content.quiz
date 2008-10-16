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


class IReadContainer(zeit.cms.content.interfaces.IXMLContent,
                     zope.app.container.interfaces.IReadContainer):
    pass


class IWriteContainer(zope.app.container.interfaces.IWriteContainer):
    pass


class IContainer(IReadContainer, IWriteContainer):
    pass


class IReadQuiz(zeit.cms.content.interfaces.ICommonMetadata, IReadContainer):
    """Read methods for quiz."""


class IWriteQuiz(IWriteContainer):
    """Write methods for quiz."""


class IQuiz(IReadQuiz, IWriteQuiz):
    """Quiz content type."""


class IReadQuestion(IReadContainer):
    """Read methods for question."""

    title = zope.schema.TextLine(title=_('Title'), required=False)


class IWriteQuestion(IWriteContainer):
    """Write methods for question."""


class IQuestion(IReadQuestion, IWriteQuestion):
    """Question content type."""


class IAnswer(zeit.cms.content.interfaces.IXMLContent):
    """Answer content type."""
    
    title = zope.schema.TextLine(title=_('Title'), required=False)
