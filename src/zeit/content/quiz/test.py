# Copyright (c) 2007-2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import os
import unittest

import persistent
import zope.app.testing.functional
import zope.testing.doctest

import zeit.cms.testing
import zeit.content.quiz.container


class PersistentContainer(persistent.Persistent,
                          zeit.content.quiz.container.Container,
                          zeit.cms.content.xmlsupport.XMLRepresentationBase):

    default_template = "<persistentcontainer />"

    def _get_persistent_container(self):
        return self


class Container(zeit.content.quiz.container.Container,
                zeit.content.quiz.container.Contained):

    default_template = "<container />"

    def _get_persistent_container(self):
        return self.__parent__


class Contained(zeit.content.quiz.container.Contained):

    default_template = "<contained />"


QuizLayer = zope.app.testing.functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),
    __name__, 'QuizLayer', allow_teardown=True)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zope.testing.doctest.DocTestSuite(
            'zeit.content.quiz.container'))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
            'quiz.txt',
            'container.txt',
            'question.txt',
            'answer.txt',
            layer=QuizLayer))
    return suite
