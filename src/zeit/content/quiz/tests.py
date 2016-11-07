from zeit.cms.testing import copy_inherited_functions
import gocept.httpserverlayer.custom
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


class QuizUpdaterRequestHandler(gocept.httpserverlayer.custom.RequestHandler):

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


HTTP_LAYER = gocept.httpserverlayer.custom.Layer(
    QuizUpdaterRequestHandler, name='HTTPLayer', module=__name__)


product_config = """\
<product-config zeit.content.quiz>
    url http://localhost:{port}/quizupdate
</product-config>
"""


class ZCMLLayer(zeit.cms.testing.ZCMLLayer):

    defaultBases = (HTTP_LAYER,)

    def setUp(self):
        self.product_config = self.product_config.format(
            port=self['http_port'])
        super(ZCMLLayer, self).setUp()


ZCML_LAYER = ZCMLLayer(
    'ftesting.zcml',
    product_config=zeit.cms.testing.cms_product_config + product_config)


class QuizSourceTest(
        zeit.cms.content.tests.test_contentsource.ContentSourceBase,
        zeit.cms.testing.FunctionalTestCase):

    layer = ZCML_LAYER

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
        layer=ZCML_LAYER))
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'updater.txt',
        layer=ZCML_LAYER))
    suite.addTest(unittest.makeSuite(QuizSourceTest))
    return suite
