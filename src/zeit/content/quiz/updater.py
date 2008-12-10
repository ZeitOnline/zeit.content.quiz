# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
"""Connection to the actual quiz system."""

import urllib
import urllib2
import zope.app.appsetup.product
import zope.interface
import zope.component
import zeit.content.quiz.interfaces


class Updater(object):

    zope.component.adapts(zeit.content.quiz.interfaces.IQuiz)
    zope.interface.implements(zeit.content.quiz.interfaces.IQuizUpdater)

    def __init__(self, context):
       self.context = context

    def update(self):
        response = urllib2.urlopen(self.get_url(), self.get_data())

    def get_url(self):
        config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.content.quiz')
        return config['url']

    def get_data(self):
        data = dict(
            quiz_id=self.context.uniqueId,
            action='preview',
            xml=zeit.cms.content.interfaces.IXMLSource(self.context))
        return urllib.urlencode(sorted(data.items()))
