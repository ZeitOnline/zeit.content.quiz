# Copyright (c) 2007-2009 gocept gmbh & co. kg
# See also LICENSE.txt

import BaseHTTPServer
import persistent
import pkg_resources
import random
import threading
import unittest
import zeit.cms.content.tests.test_contentsource
import zeit.cms.testing
import zeit.content.quiz.container
import zeit.content.quiz.source
import zope.app.testing.functional
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


class QuizUpdaterRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

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


httpd_port = random.randint(30000, 40000)


def start_quiz_updater_httpd():
    def run():
        server_address = ('localhost', httpd_port)
        httpd = BaseHTTPServer.HTTPServer(
            server_address, QuizUpdaterRequestHandler)
        httpd.handle_request()
    t = threading.Thread(target=run)
    t.start()


QuizLayer = zope.app.testing.functional.ZCMLLayer(
    pkg_resources.resource_filename(__name__, 'ftesting.zcml'),
    __name__, 'QuizLayer', allow_teardown=True)


class QuizSourceTest(
    zeit.cms.content.tests.test_contentsource.ContentSourceTest):

    layer = QuizLayer

    source = zeit.content.quiz.source.quizSource
    expected_types = ['quiz']



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
        product_config={
            'zeit.content.quiz': {
                'url': 'http://localhost:%s/quizupdate' % httpd_port}},
        layer=QuizLayer))
    suite.addTest(unittest.makeSuite(QuizSourceTest))
    return suite
