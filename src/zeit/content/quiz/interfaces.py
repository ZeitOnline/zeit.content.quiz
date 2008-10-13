# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import zope.app.container.interfaces
import zope.interface

import zeit.cms.content.interfaces


class IQuiz(zope.interface.Interface):
    """Quiz content type."""


class IReadQuiz(
    zeit.cms.content.interfaces.ICommonMetadata,
    zeit.cms.content.interfaces.IXMLContent,
    zope.app.container.interfaces.IReadContainer):
    """Read methods for quiz."""


class IWriteQuiz(zope.app.container.interfaces.IWriteContainer):
    """Write methods for quiz."""
