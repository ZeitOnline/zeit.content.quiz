# Copyright (c) 2007-2009 gocept gmbh & co. kg
# See also LICENSE.txt

from zeit.cms.testing import copy_inherited_functions
import persistent
import unittest
import zeit.cms.content.tests.test_contentsource
import zeit.cms.testing
import zeit.content.quiz.container
import zeit.content.quiz.source
import zope.testing.doctest


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


class QuizUpdaterRequestHandler(zeit.cms.testing.BaseHTTPRequestHandler):

    posts_received = []
    response = 200

    def do_POST(self):
        length = int(self.headers['content-length'])
        self.posts_received.append(dict(
            path=self.path,
            data=self.rfile.read(length),
        ))
        self.send_response(self.response)
        self.end_headers()

    def log_message(self, format, *args):
        pass


QuizHTTPLayer, httpd_port = zeit.cms.testing.HTTPServerLayer(
    QuizUpdaterRequestHandler)


product_config = """\
<product-config zeit.content.quiz>
    url http://localhost:%s/quizupdate
</product-config>
""" % (httpd_port,)


QuizZCMLLayer = zeit.cms.testing.ZCMLLayer(
    'ftesting.zcml',
    product_config=zeit.cms.testing.cms_product_config + product_config)


class QuizLayer(QuizZCMLLayer, QuizHTTPLayer):

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class QuizSourceTest(
    zeit.cms.content.tests.test_contentsource.ContentSourceBase,
    zeit.cms.testing.FunctionalTestCase):

    layer = QuizLayer

    source = zeit.content.quiz.source.quizSource
    expected_types = ['quiz']

    copy_inherited_functions(
        zeit.cms.content.tests.test_contentsource.ContentSourceBase, locals())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zope.testing.doctest.DocTestSuite(
        'zeit.content.quiz.container'))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'answer.txt',
        'container.txt',
        'question.txt',
        'quiz.txt',
        'text-index.txt',
        layer=QuizLayer))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'updater.txt',
        layer=QuizLayer))
    suite.addTest(unittest.makeSuite(QuizSourceTest))
    return suite
