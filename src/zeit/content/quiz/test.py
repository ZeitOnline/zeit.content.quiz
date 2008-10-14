# Copyright (c) 2007-2008 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import os
import unittest

import zope.app.testing.functional
import zope.testing.doctest

import zeit.cms.testing


QuizLayer = zope.app.testing.functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),
    __name__, 'QuizLayer', allow_teardown=True)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zope.testing.doctest.DocFileSuite(
            'question.txt'))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
            'quiz.txt',
            layer=QuizLayer))
    return suite
