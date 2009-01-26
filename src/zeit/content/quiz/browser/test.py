# -*- coding: utf-8 -*-
# Copyright (c) 2008-2009 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$

import unittest

import zeit.cms.testing
import zeit.content.quiz.test


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        layer=zeit.content.quiz.test.QuizLayer))
    return suite
