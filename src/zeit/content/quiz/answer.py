# -*- coding: utf-8 -*-
# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import rwproperty
import zope.app.container.interfaces
import zope.component
import zope.interface

import zeit.cms.content.property
import zeit.wysiwyg.html
import zeit.wysiwyg.interfaces

import zeit.content.quiz.interfaces
import zeit.content.quiz.container


ANSWER_TEMPLATE = u"""\
<answer xmlns:py="http://codespeak.net/lxml/objectify/pytype">
  <text/>
  <explanation/>
</answer>"""


class Answer(zeit.content.quiz.container.Contained):
    """A possible answer to a question of a quiz.

    """
    zope.interface.implements(zeit.content.quiz.interfaces.IAnswer,
                              zope.app.container.interfaces.IContained)

    title = zeit.cms.content.property.Structure('.title')
    correct = zeit.cms.content.property.ObjectPathProperty('.correct')

    @rwproperty.getproperty
    def answer(self):
        return self.convert.to_html(self.xml['text'])

    @rwproperty.setproperty
    def answer(self, value):
        return self.convert.from_html(self.xml['text'], value)

    @rwproperty.getproperty
    def explanation(self):
        return self.convert.to_html(self.xml['explanation'])

    @rwproperty.setproperty
    def explanation(self, value):
        return self.convert.from_html(self.xml['explanation'], value)

    @property
    def convert(self):
        return zeit.wysiwyg.interfaces.IHTMLConverter(self)


    default_template = ANSWER_TEMPLATE


answerFactory = zeit.content.quiz.container.xml_tree_content_adapter(Answer)
