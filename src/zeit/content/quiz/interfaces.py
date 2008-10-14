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


class IReadQuiz(
    zeit.cms.content.interfaces.ICommonMetadata,
    zeit.cms.content.interfaces.IXMLContent,
    zope.app.container.interfaces.IReadContainer):
    """Read methods for quiz."""


class IWriteQuiz(zope.app.container.interfaces.IWriteContainer):
    """Write methods for quiz."""


class IQuiz(IReadQuiz, IWriteQuiz):
    """Quiz content type."""


class IReadQuestion(
    zeit.cms.interfaces.ICMSContent,
    zope.app.container.interfaces.IReadContainer):
    """Read methods for question."""

    title = zope.schema.TextLine(title=_('Title'), required=False)
    text = zeit.cms.content.field.XMLTree(title=_('Question'))


class IWriteQuestion(zope.app.container.interfaces.IWriteContainer):
    """Write methods for question."""


class IQuestion(IReadQuestion, IWriteQuestion):
    """Question content type."""
