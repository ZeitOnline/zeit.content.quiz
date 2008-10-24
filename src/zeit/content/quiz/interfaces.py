# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zc.form.field
import zope.app.container.interfaces
import zope.interface
import zope.schema

import zeit.cms.content.interfaces
import zeit.cms.content.field

from zeit.cms.i18n import MessageFactory as _


class IReadContainer(zope.app.container.interfaces.IReadContainer,
                     zeit.cms.content.interfaces.IXMLRepresentation):
    """Read-only container that stores its children inside its own xml
    representation."""

    def content_modified():
        """Notify the container that content has changed."""


class IWriteContainer(zope.app.container.interfaces.IWriteContainer):
    """Writeable container that stores its children inside its own xml
    representation."""

    def updateOrder(order):
        """Revise the order of keys, replacing the current ordering.

        order is a list or a tuple containing the set of existing keys in
        the new order. `order` must contain ``len(keys())`` items and cannot
        contain duplicate keys.

        Raises ``TypeError`` if order is not a tuple or a list.

        Raises ``ValueError`` if order contains an invalid set of keys.

        Analogous to zope.app.container.interfaces.IOrderedContainer.
        """


class IReadQuiz(zeit.cms.content.interfaces.ICommonMetadata, 
                zeit.cms.content.interfaces.IXMLContent,
                IReadContainer):
    """Read methods for quiz."""


class IWriteQuiz(IWriteContainer):
    """Write methods for quiz."""


class IQuiz(IReadQuiz, IWriteQuiz):
    """Quiz content type."""


class IQuizContent(zope.interface.Interface):
    """Sub-objects of a quiz.
    """

    title = zope.schema.TextLine(title=_('Title'), required=False)


class IReadQuestion(IQuizContent, IReadContainer):
    """Read methods for question."""


class IWriteQuestion(IWriteContainer):
    """Write methods for question."""

    question = zc.form.field.HTMLSnippet(title=_("Text"), required=False)


class IQuestion(IReadQuestion, IWriteQuestion):
    """Question content type."""


class IAnswer(zeit.cms.content.interfaces.IXMLRepresentation, IQuizContent):
    """Answer content type."""

    correct = zope.schema.Bool(title=_('Correct?'))
    answer = zc.form.field.HTMLSnippet(title=_("Text"))
    explanation = zc.form.field.HTMLSnippet(
        title=_("Explanation"), required=False)
