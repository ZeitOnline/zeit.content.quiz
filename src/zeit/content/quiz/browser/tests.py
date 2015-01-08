
import unittest
import zeit.cms.testing
import zeit.content.quiz.tests


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        layer=zeit.content.quiz.tests.ZCML_LAYER))
    return suite
